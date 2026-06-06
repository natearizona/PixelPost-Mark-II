from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path

from markii.media.inventory import InventoryResult
from markii.storage.archive import Archive


@dataclass
class ArchiveInventoryResult:
    archive_path: str
    import_run_id: int
    profile_name: str | None
    status: str
    source_artifact_count: int
    provenance_event_count: int
    archive_counts: dict[str, int]

    def to_dict(self):
        return asdict(self)


def record_inventory(
    inventory: InventoryResult,
    archive_path: Path,
    profile: str | None = None,
) -> ArchiveInventoryResult:
    event_count = 0
    with Archive(archive_path) as archive:
        run_id = archive.create_import_run(profile, operation="media_inventory")
        try:
            for artifact in inventory.artifacts:
                artifact_id = archive.upsert_source_artifact(artifact)
                archive.record_provenance_event(
                    import_run_id=run_id,
                    source_artifact_id=artifact_id,
                    entity_type="source_artifact",
                    entity_id=str(artifact_id),
                    decision="inventoried",
                    notes=f"Detected by rule: {artifact.detection_rule}",
                )
                event_count += 1
            archive.complete_import_run(run_id, "completed")
            status = "completed"
        except Exception:
            archive.complete_import_run(run_id, "failed")
            raise
        counts = archive.counts()

    return ArchiveInventoryResult(
        archive_path=str(archive_path),
        import_run_id=run_id,
        profile_name=profile,
        status=status,
        source_artifact_count=inventory.summary.total_files_scanned,
        provenance_event_count=event_count,
        archive_counts=counts,
    )

