"""Media matching engine — links parsed XML records to on-disk artifacts.

Design specification: docs/phase13-media-matching-design-review.md
Confidence levels: exact | high | probable | ambiguous | unmatched
Doctrine: unresolved is better than wrong.
"""
from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from urllib.parse import urlparse

from markii.importers.pixelpost_xml import (
    ParsedAttachment,
    ParsedPost,
    PixelPostParseResult,
)
from markii.media.inventory import Artifact, InventoryResult


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class MatchSignal:
    signal_type: str    # attachment_filename | body_img_src | post_parent |
                        # thumbnail_rule | timestamp_correlation | url_domain | hash_identity
    matched_value: str  # the value that triggered this signal
    strength: str       # primary | corroborating | derived | tiebreaker
    notes: str = ""

    def to_dict(self):
        return asdict(self)


@dataclass
class MediaMatch:
    post_legacy_id: str
    post_slug: str
    post_date: str
    attachment_legacy_id: str | None
    matched_artifact_path: str | None  # None when ambiguous or unmatched
    thumbnail_artifact_path: str | None
    confidence: str                    # exact | high | probable | ambiguous | unmatched
    signals: list[MatchSignal] = field(default_factory=list)
    candidate_count: int = 0
    all_candidate_paths: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def to_dict(self):
        return {
            "post_legacy_id": self.post_legacy_id,
            "post_slug": self.post_slug,
            "post_date": self.post_date,
            "attachment_legacy_id": self.attachment_legacy_id,
            "matched_artifact_path": self.matched_artifact_path,
            "thumbnail_artifact_path": self.thumbnail_artifact_path,
            "confidence": self.confidence,
            "signals": [s.to_dict() for s in self.signals],
            "candidate_count": self.candidate_count,
            "all_candidate_paths": self.all_candidate_paths,
            "notes": self.notes,
        }


@dataclass
class OrphanArtifact:
    artifact_path: str
    filename: str
    artifact_type: str   # jpeg | thumbnail
    sha256: str
    file_size: int | None
    image_width: int | None
    image_height: int | None
    reason: str          # no_xml_reference | ambiguity_unresolved

    def to_dict(self):
        return asdict(self)


@dataclass
class MediaMatchSummary:
    posts_total: int = 0
    matches_exact: int = 0
    matches_high: int = 0
    matches_probable: int = 0
    matches_ambiguous: int = 0
    unmatched_posts: int = 0
    thumbnails_matched: int = 0
    orphan_images: int = 0
    orphan_thumbnails: int = 0
    warnings: list[str] = field(default_factory=list)

    def to_dict(self):
        return asdict(self)


@dataclass
class MediaMatchResult:
    xml_source_files: list[str]
    media_source_dirs: list[str]
    matches: list[MediaMatch]
    orphan_media: list[OrphanArtifact]
    summary: MediaMatchSummary
    status: str  # completed | completed_with_warnings | failed

    def to_dict(self):
        return {
            "xml_source_files": self.xml_source_files,
            "media_source_dirs": self.media_source_dirs,
            "matches": [m.to_dict() for m in self.matches],
            "orphan_media": [o.to_dict() for o in self.orphan_media],
            "summary": self.summary.to_dict(),
            "status": self.status,
        }


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def match_media(
    parse_result: PixelPostParseResult,
    inventory: InventoryResult,
) -> MediaMatchResult:
    """Match parsed XML posts to on-disk media artifacts.

    Returns a MediaMatchResult with one MediaMatch per post, plus
    OrphanArtifact records for any unattributed media.
    """
    # Build lookup indexes
    artifact_index = _build_artifact_index(inventory.artifacts)
    attachment_index = _build_attachment_index(parse_result.attachments)
    post_ids = {p.legacy_id for p in parse_result.posts}

    # Warn about XML-orphan attachments (post_parent references missing post)
    warnings: list[str] = []
    for attachment in parse_result.attachments:
        if attachment.post_parent and attachment.post_parent not in post_ids:
            warnings.append(
                f"Attachment {attachment.legacy_id} references post_parent "
                f"{attachment.post_parent!r} which is not in the parsed post set."
            )

    # Match each post
    matched_paths: set[str] = set()
    ambiguous_paths: set[str] = set()
    matches: list[MediaMatch] = []

    for post in sorted(parse_result.posts, key=lambda p: p.publication_date):
        attachment = attachment_index.get(post.legacy_id)
        match = _match_post(post, attachment, artifact_index, warnings)
        matches.append(match)

        for path in match.all_candidate_paths:
            matched_paths.add(path)
        if match.confidence == "ambiguous":
            for path in match.all_candidate_paths:
                ambiguous_paths.add(path)

    # Collect orphan artifacts
    orphan_media: list[OrphanArtifact] = []
    for artifact in inventory.artifacts:
        if artifact.artifact_type not in ("jpeg", "thumbnail"):
            continue
        if artifact.source_path in matched_paths:
            if artifact.source_path in ambiguous_paths:
                orphan_media.append(OrphanArtifact(
                    artifact_path=artifact.source_path,
                    filename=artifact.filename,
                    artifact_type=artifact.artifact_type,
                    sha256=artifact.sha256 or "",
                    file_size=artifact.file_size,
                    image_width=artifact.image_width,
                    image_height=artifact.image_height,
                    reason="ambiguity_unresolved",
                ))
        else:
            orphan_media.append(OrphanArtifact(
                artifact_path=artifact.source_path,
                filename=artifact.filename,
                artifact_type=artifact.artifact_type,
                sha256=artifact.sha256 or "",
                file_size=artifact.file_size,
                image_width=artifact.image_width,
                image_height=artifact.image_height,
                reason="no_xml_reference",
            ))

    summary = _build_summary(matches, orphan_media, warnings)
    has_warnings = (
        summary.matches_ambiguous > 0
        or summary.unmatched_posts > 0
        or summary.orphan_images > 0
        or summary.orphan_thumbnails > 0
        or summary.warnings
    )
    status = "completed_with_warnings" if has_warnings else "completed"

    return MediaMatchResult(
        xml_source_files=parse_result.source_files,
        media_source_dirs=inventory.sources,
        matches=matches,
        orphan_media=orphan_media,
        summary=summary,
        status=status,
    )


# ---------------------------------------------------------------------------
# Indexing helpers
# ---------------------------------------------------------------------------

def _build_artifact_index(artifacts: list[Artifact]) -> dict[str, list[Artifact]]:
    """Map lowercase filename → list of artifacts with that filename."""
    index: dict[str, list[Artifact]] = {}
    for artifact in artifacts:
        if artifact.artifact_type not in ("jpeg", "thumbnail"):
            continue
        key = artifact.filename.lower()
        index.setdefault(key, []).append(artifact)
    return index


def _build_attachment_index(attachments: list[ParsedAttachment]) -> dict[str, ParsedAttachment]:
    """Map post_parent ID → attachment. First attachment wins on collision."""
    index: dict[str, ParsedAttachment] = {}
    for attachment in attachments:
        if attachment.post_parent and attachment.post_parent not in index:
            index[attachment.post_parent] = attachment
    return index


# ---------------------------------------------------------------------------
# Per-post matching
# ---------------------------------------------------------------------------

def _match_post(
    post: ParsedPost,
    attachment: ParsedAttachment | None,
    artifact_index: dict[str, list[Artifact]],
    warnings: list[str],
) -> MediaMatch:
    signals: list[MatchSignal] = []
    candidates: dict[str, Artifact] = {}  # path → artifact, deduped

    # --- Signal 1: attachment_filename (primary) ---
    attachment_legacy_id: str | None = None
    attachment_filename: str | None = None
    if attachment is not None:
        attachment_legacy_id = attachment.legacy_id
        attachment_filename = attachment.filename_candidate
        if attachment_filename:
            matches_s1 = artifact_index.get(attachment_filename.lower(), [])
            for art in matches_s1:
                candidates[art.source_path] = art
            if matches_s1:
                signals.append(MatchSignal(
                    signal_type="attachment_filename",
                    matched_value=attachment_filename,
                    strength="primary",
                ))

    # --- Signal 2: body_img_src (primary) ---
    body_filenames = _extract_img_filenames(post.body)
    unique_body_filenames = list(dict.fromkeys(f.lower() for f in body_filenames))

    body_signal_note = ""
    if len(unique_body_filenames) > 1:
        body_signal_note = (
            f"Multiple distinct img src filenames found in post body: "
            f"{', '.join(unique_body_filenames)}"
        )

    body_candidates: dict[str, Artifact] = {}
    for bf in unique_body_filenames:
        matches_s2 = artifact_index.get(bf, [])
        for art in matches_s2:
            body_candidates[art.source_path] = art
        if matches_s2:
            signals.append(MatchSignal(
                signal_type="body_img_src",
                matched_value=bf,
                strength="primary",
                notes=body_signal_note if bf == unique_body_filenames[-1] else "",
            ))

    # Merge body candidates into overall candidates
    for path, art in body_candidates.items():
        candidates[path] = art

    # If no primary candidates at all → unmatched
    if not candidates:
        return MediaMatch(
            post_legacy_id=post.legacy_id,
            post_slug=post.slug,
            post_date=post.publication_date,
            attachment_legacy_id=attachment_legacy_id,
            matched_artifact_path=None,
            thumbnail_artifact_path=None,
            confidence="unmatched",
            signals=signals,
            candidate_count=0,
            all_candidate_paths=[],
            notes=["No on-disk artifact matched any signal for this post."],
        )

    # --- Check for signal conflict (S1 and S2 disagree on filename) ---
    s1_candidates = set()
    if attachment_filename:
        for art in artifact_index.get(attachment_filename.lower(), []):
            s1_candidates.add(art.source_path)
    s2_candidates = set(body_candidates.keys())

    signal_conflict = (
        bool(s1_candidates) and bool(s2_candidates)
        and not s1_candidates.intersection(s2_candidates)
    )

    if signal_conflict:
        conflict_note = (
            f"attachment_url and body img src disagree on filename: "
            f"{attachment_filename!r} vs {', '.join(unique_body_filenames)!r}"
        )
        return MediaMatch(
            post_legacy_id=post.legacy_id,
            post_slug=post.slug,
            post_date=post.publication_date,
            attachment_legacy_id=attachment_legacy_id,
            matched_artifact_path=None,
            thumbnail_artifact_path=None,
            confidence="ambiguous",
            signals=signals,
            candidate_count=len(candidates),
            all_candidate_paths=sorted(candidates.keys()),
            notes=[conflict_note],
        )

    # --- Multiple distinct on-disk candidates → ambiguous ---
    if len(candidates) > 1:
        note = f"Multiple distinct candidate artifacts found: {sorted(candidates.keys())}"
        return MediaMatch(
            post_legacy_id=post.legacy_id,
            post_slug=post.slug,
            post_date=post.publication_date,
            attachment_legacy_id=attachment_legacy_id,
            matched_artifact_path=None,
            thumbnail_artifact_path=None,
            confidence="ambiguous",
            signals=signals,
            candidate_count=len(candidates),
            all_candidate_paths=sorted(candidates.keys()),
            notes=[note],
        )

    # --- Single candidate — evaluate corroborating signals ---
    winner = next(iter(candidates.values()))
    corroborating_count = 0

    # Signal 3: post_parent confirmation
    if attachment is not None and attachment.post_parent == post.legacy_id:
        signals.append(MatchSignal(
            signal_type="post_parent",
            matched_value=post.legacy_id,
            strength="corroborating",
        ))
        corroborating_count += 1

    # Signal 5: timestamp correlation (same calendar day)
    if _timestamp_signal_fires(winner.filename, post.publication_date):
        signals.append(MatchSignal(
            signal_type="timestamp_correlation",
            matched_value=winner.filename[:8],
            strength="corroborating",
        ))
        corroborating_count += 1

    # Signal 6: URL domain consistency
    domain_note = _url_domain_signal(attachment, post.body)
    if domain_note == "consistent":
        signals.append(MatchSignal(
            signal_type="url_domain",
            matched_value="consistent",
            strength="corroborating",
        ))
        corroborating_count += 1
    elif domain_note:
        signals.append(MatchSignal(
            signal_type="url_domain",
            matched_value="inconsistent",
            strength="corroborating",
            notes=domain_note,
        ))

    # --- Assign confidence ---
    s1_fired = bool(s1_candidates)
    s2_fired = bool(s2_candidates)

    if s1_fired and s2_fired and attachment is not None and attachment.post_parent == post.legacy_id:
        confidence = "exact"
    elif corroborating_count >= 1:
        confidence = "high"
    else:
        confidence = "probable"

    # Signal 4: thumbnail (derived) — only for probable or better
    thumbnail_path: str | None = None
    predicted_thumb = "thumb_" + winner.filename
    thumb_candidates = artifact_index.get(predicted_thumb.lower(), [])
    if thumb_candidates:
        if len(thumb_candidates) == 1:
            thumbnail_path = thumb_candidates[0].source_path
            signals.append(MatchSignal(
                signal_type="thumbnail_rule",
                matched_value=predicted_thumb,
                strength="derived",
            ))
        else:
            # Multiple thumbnail candidates — do not choose
            signals.append(MatchSignal(
                signal_type="thumbnail_rule",
                matched_value=predicted_thumb,
                strength="derived",
                notes=f"Multiple thumbnail candidates found: {[a.source_path for a in thumb_candidates]}",
            ))

    return MediaMatch(
        post_legacy_id=post.legacy_id,
        post_slug=post.slug,
        post_date=post.publication_date,
        attachment_legacy_id=attachment_legacy_id,
        matched_artifact_path=winner.source_path,
        thumbnail_artifact_path=thumbnail_path,
        confidence=confidence,
        signals=signals,
        candidate_count=1,
        all_candidate_paths=[winner.source_path],
        notes=[],
    )


# ---------------------------------------------------------------------------
# Signal helpers
# ---------------------------------------------------------------------------

_IMG_SRC_RE = re.compile(r'<img[^>]+src=["\']([^"\']+)["\']', re.IGNORECASE)


def _extract_img_filenames(body: str) -> list[str]:
    """Extract filenames from all <img src="..."> tags in post body."""
    filenames = []
    for src in _IMG_SRC_RE.findall(body):
        name = Path(urlparse(src).path).name
        if name:
            filenames.append(name)
    return filenames


def _timestamp_signal_fires(filename: str, publication_date: str) -> bool:
    """Signal 5: filename begins with YYYYMMDD matching post publication_date calendar day."""
    if len(filename) < 8 or not filename[:8].isdigit():
        return False
    filename_day = filename[:8]  # YYYYMMDD
    # publication_date format: "2008-01-01 01:01:01"
    post_day = publication_date[:10].replace("-", "")  # YYYYMMDD
    return filename_day == post_day


def _url_domain_signal(attachment: ParsedAttachment | None, body: str) -> str:
    """Signal 6: check URL domain consistency between attachment_url and body img src.

    Returns 'consistent', a note string if inconsistent, or '' if not evaluable.
    """
    if not attachment or not attachment.attachment_url:
        return ""
    attachment_domain = urlparse(attachment.attachment_url).netloc
    if not attachment_domain:
        return ""
    img_urls = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', body, re.IGNORECASE)
    if not img_urls:
        return ""
    body_domains = {urlparse(url).netloc for url in img_urls if urlparse(url).netloc}
    if not body_domains:
        return ""
    if body_domains == {attachment_domain}:
        return "consistent"
    differing = body_domains - {attachment_domain}
    return f"Domain mismatch: attachment_url uses {attachment_domain!r}, body img src uses {sorted(differing)}"


# ---------------------------------------------------------------------------
# Summary builder
# ---------------------------------------------------------------------------

def _build_summary(
    matches: list[MediaMatch],
    orphan_media: list[OrphanArtifact],
    warnings: list[str],
) -> MediaMatchSummary:
    summary = MediaMatchSummary(posts_total=len(matches), warnings=list(warnings))
    for m in matches:
        if m.confidence == "exact":
            summary.matches_exact += 1
        elif m.confidence == "high":
            summary.matches_high += 1
        elif m.confidence == "probable":
            summary.matches_probable += 1
        elif m.confidence == "ambiguous":
            summary.matches_ambiguous += 1
        else:
            summary.unmatched_posts += 1
        if m.thumbnail_artifact_path:
            summary.thumbnails_matched += 1
    for o in orphan_media:
        if o.artifact_type == "thumbnail":
            summary.orphan_thumbnails += 1
        else:
            summary.orphan_images += 1
    return summary
