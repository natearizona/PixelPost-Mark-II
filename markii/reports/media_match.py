"""Report writer for media match results — .md and .json."""
from __future__ import annotations

import json
from pathlib import Path

from markii.media.matcher import MediaMatch, MediaMatchResult, OrphanArtifact


def write_media_match_reports(result: MediaMatchResult, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "media-match-report.json").write_text(
        json.dumps(result.to_dict(), indent=2, sort_keys=True),
        encoding="utf-8",
    )
    (output_dir / "media-match-report.md").write_text(
        render_media_match_markdown(result),
        encoding="utf-8",
    )


def render_media_match_markdown(result: MediaMatchResult) -> str:
    s = result.summary
    lines = [
        "# Media Match Report",
        "",
        f"- Status: `{result.status}`",
        "",
        "## Source Files",
        "",
    ]
    lines.extend(f"- `{f}`" for f in result.xml_source_files)
    lines.extend(["", "## Media Directories", ""])
    lines.extend(f"- `{d}`" for d in result.media_source_dirs)

    lines.extend([
        "",
        "## Summary",
        "",
        "| Metric | Count |",
        "| --- | ---: |",
        f"| Posts total | {s.posts_total} |",
        f"| Exact matches | {s.matches_exact} |",
        f"| High confidence | {s.matches_high} |",
        f"| Probable matches | {s.matches_probable} |",
        f"| Ambiguous | {s.matches_ambiguous} |",
        f"| Unmatched posts | {s.unmatched_posts} |",
        f"| Thumbnails matched | {s.thumbnails_matched} |",
        f"| Orphan images | {s.orphan_images} |",
        f"| Orphan thumbnails | {s.orphan_thumbnails} |",
        "",
        "## Match Table",
        "",
        "| post_id | post_date | slug | confidence | matched_file | thumbnail | signals | candidates |",
        "| --- | --- | --- | --- | --- | --- | --- | ---: |",
    ])

    for m in result.matches:
        matched_file = Path(m.matched_artifact_path).name if m.matched_artifact_path else "—"
        thumbnail = "✓" if m.thumbnail_artifact_path else "—"
        signal_types = ", ".join(s.signal_type for s in m.signals)
        lines.append(
            f"| `{m.post_legacy_id}` | {m.post_date} | `{m.post_slug}` "
            f"| **{m.confidence}** | `{matched_file}` | {thumbnail} "
            f"| {signal_types} | {m.candidate_count} |"
        )

    # Ambiguous section
    ambiguous = [m for m in result.matches if m.confidence == "ambiguous"]
    lines.extend(["", "## Ambiguous Matches", ""])
    if not ambiguous:
        lines.append("None.")
    else:
        for m in ambiguous:
            lines.extend([
                f"### Post `{m.post_legacy_id}` — `{m.post_slug}`",
                "",
                f"- Date: {m.post_date}",
                f"- Attachment: `{m.attachment_legacy_id or '—'}`",
                f"- Candidate count: {m.candidate_count}",
                "",
                "**Candidates:**",
                "",
            ])
            for path in m.all_candidate_paths:
                lines.append(f"- `{path}`")
            if m.notes:
                lines.extend(["", "**Notes:**", ""])
                lines.extend(f"- {note}" for note in m.notes)
            lines.extend(["", "**Signals:**", ""])
            for sig in m.signals:
                note_str = f" — {sig.notes}" if sig.notes else ""
                lines.append(f"- `{sig.signal_type}` ({sig.strength}): `{sig.matched_value}`{note_str}")
            lines.append("")

    # Unmatched section
    unmatched = [m for m in result.matches if m.confidence == "unmatched"]
    lines.extend(["## Unmatched Posts", ""])
    if not unmatched:
        lines.append("None.")
    else:
        lines.extend([
            "| post_id | post_date | slug | partial signals |",
            "| --- | --- | --- | --- |",
        ])
        for m in unmatched:
            partial = ", ".join(s.signal_type for s in m.signals) or "—"
            lines.append(f"| `{m.post_legacy_id}` | {m.post_date} | `{m.post_slug}` | {partial} |")

    # Orphan images section
    orphan_images = [o for o in result.orphan_media if o.artifact_type == "jpeg"]
    lines.extend(["", "## Orphan Images", ""])
    if not orphan_images:
        lines.append("None.")
    else:
        lines.extend([
            "| filename | size | dimensions | SHA-256 | reason |",
            "| --- | --- | --- | --- | --- |",
        ])
        for o in orphan_images:
            dims = f"{o.image_width}×{o.image_height}" if o.image_width and o.image_height else "—"
            size = str(o.file_size) if o.file_size is not None else "—"
            sha = o.sha256[:16] + "…" if len(o.sha256) > 16 else o.sha256
            lines.append(f"| `{o.filename}` | {size} | {dims} | `{sha}` | {o.reason} |")

    # Orphan thumbnails section
    orphan_thumbs = [o for o in result.orphan_media if o.artifact_type == "thumbnail"]
    lines.extend(["", "## Orphan Thumbnails", ""])
    if not orphan_thumbs:
        lines.append("None.")
    else:
        lines.extend([
            "| filename | size | dimensions | SHA-256 | reason |",
            "| --- | --- | --- | --- | --- |",
        ])
        for o in orphan_thumbs:
            dims = f"{o.image_width}×{o.image_height}" if o.image_width and o.image_height else "—"
            size = str(o.file_size) if o.file_size is not None else "—"
            sha = o.sha256[:16] + "…" if len(o.sha256) > 16 else o.sha256
            lines.append(f"| `{o.filename}` | {size} | {dims} | `{sha}` | {o.reason} |")

    # Warnings section
    lines.extend(["", "## Warnings", ""])
    if not s.warnings:
        lines.append("None.")
    else:
        lines.extend(f"- {w}" for w in s.warnings)

    lines.append("")
    return "\n".join(lines)
