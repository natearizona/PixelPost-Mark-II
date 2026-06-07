"""Persist MediaMatchResult evidence into the SQLite archive.

Design principle: match-media remains a dry-run inspection command.
write-matches commits match decisions to the durable archive.

Each MediaMatch produces one provenance_event with entity_type="post".
Each matched thumbnail produces a second provenance_event with entity_type="thumbnail".
Each OrphanArtifact produces one provenance_event with entity_type="orphan_image"
or "orphan_thumbnail".

Unmatched posts are linked to the XML source artifact — evidence that the post
exists in the record without a confirmed image attribution.

Signal evidence is serialized as JSON in the notes field. Ambiguity is
preserved exactly as recorded — no resolution is applied.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from markii.media.inventory import Artifact, InventoryResult
from markii.media.matcher import MediaMatch, MediaMatchResult, OrphanArtifact
from markii.storage.archive import Archive


@dataclass
class ArchiveMatchResult:
    archive_path: str
    import_run_id: int
    status: str
    match_event_count: int
    orphan_event_count: int
    archive_counts: dict[str, int]

    def to_dict(self) -> dict:
        return {
            "archive_path": self.archive_path,
            "import_run_id": self.import_run_id,
            "status": self.status,
            "match_event_count": self.match_event_count,
            "orphan_event_count": self.orphan_event_count,
            "archive_counts": self.archive_counts,
        }


def record_matches(
    match_result: MediaMatchResult,
    inventory: InventoryResult,
    archive_path: Path,
    profile: str | None = None,
) -> ArchiveMatchResult:
    """Write MediaMatchResult records into the SQLite archive.

    The inventory must include both XML source files and media files so that
    every artifact referenced in match_result has a source_artifacts row.
    Pass the result of inventory_sources([xml_paths..., media_dirs...]).
    """
    artifact_by_path: dict[str, Artifact] = {
        a.source_path: a for a in inventory.artifacts
    }
    xml_artifacts = [
        a for a in inventory.artifacts if a.artifact_type == "pixelpost_xml"
    ]

    match_event_count = 0
    orphan_event_count = 0

    with Archive(archive_path) as archive:
        run_id = archive.create_import_run(profile, operation="media_match_write")
        try:
            # Upsert XML artifacts first — used as fallback for unmatched posts
            xml_artifact_ids: dict[str, int] = {}
            for xa in xml_artifacts:
                xml_artifact_ids[xa.source_path] = archive.upsert_source_artifact(xa)

            default_xml_artifact_id: int | None = (
                next(iter(xml_artifact_ids.values())) if xml_artifact_ids else None
            )

            for match in match_result.matches:
                match_event_count += _record_match(
                    archive, run_id, match, artifact_by_path, default_xml_artifact_id
                )

            for orphan in match_result.orphan_media:
                orphan_event_count += _record_orphan(
                    archive, run_id, orphan, artifact_by_path
                )

            archive.complete_import_run(run_id, "completed")
            status = "completed"
        except Exception:
            archive.complete_import_run(run_id, "failed")
            raise

        counts = archive.counts()

    return ArchiveMatchResult(
        archive_path=str(archive_path),
        import_run_id=run_id,
        status=status,
        match_event_count=match_event_count,
        orphan_event_count=orphan_event_count,
        archive_counts=counts,
    )


def _record_match(
    archive: Archive,
    run_id: int,
    match: MediaMatch,
    artifact_by_path: dict[str, Artifact],
    default_xml_artifact_id: int | None,
) -> int:
    """Write provenance events for one MediaMatch. Returns event count written."""
    events_written = 0

    # Resolve the primary image artifact id
    if match.matched_artifact_path and match.matched_artifact_path in artifact_by_path:
        image_artifact = artifact_by_path[match.matched_artifact_path]
        image_artifact_id = archive.upsert_source_artifact(image_artifact)
    else:
        # Unmatched or ambiguous with no resolved path — link to XML source
        if default_xml_artifact_id is None:
            return 0
        image_artifact_id = default_xml_artifact_id

    notes = json.dumps({
        "signals": [s.to_dict() for s in match.signals],
        "candidate_count": match.candidate_count,
        "all_candidate_paths": match.all_candidate_paths,
        "notes": match.notes,
    })

    archive.record_provenance_event(
        import_run_id=run_id,
        source_artifact_id=image_artifact_id,
        entity_type="post",
        entity_id=match.post_legacy_id,
        decision=match.confidence,
        notes=notes,
    )
    events_written += 1

    # Record thumbnail match as a separate provenance event
    if (
        match.thumbnail_artifact_path
        and match.thumbnail_artifact_path in artifact_by_path
    ):
        thumb_artifact = artifact_by_path[match.thumbnail_artifact_path]
        thumb_id = archive.upsert_source_artifact(thumb_artifact)
        archive.record_provenance_event(
            import_run_id=run_id,
            source_artifact_id=thumb_id,
            entity_type="thumbnail",
            entity_id=match.post_legacy_id,
            decision=match.confidence,
            notes=None,
        )
        events_written += 1

    return events_written


def _record_orphan(
    archive: Archive,
    run_id: int,
    orphan: OrphanArtifact,
    artifact_by_path: dict[str, Artifact],
) -> int:
    """Write one provenance event for an OrphanArtifact. Returns 1 on success, 0 if skipped."""
    if orphan.artifact_path not in artifact_by_path:
        return 0

    artifact = artifact_by_path[orphan.artifact_path]
    orphan_id = archive.upsert_source_artifact(artifact)
    entity_type = (
        "orphan_thumbnail" if orphan.artifact_type == "thumbnail" else "orphan_image"
    )
    archive.record_provenance_event(
        import_run_id=run_id,
        source_artifact_id=orphan_id,
        entity_type=entity_type,
        entity_id=orphan.filename,
        decision=orphan.reason,
        notes=None,
    )
    return 1
