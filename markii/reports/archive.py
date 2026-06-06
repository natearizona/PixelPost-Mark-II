import json
from pathlib import Path

from markii.provenance.inventory_archive import ArchiveInventoryResult


def write_archive_record_reports(result: ArchiveInventoryResult, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "archive-verification.json").write_text(
        json.dumps(result.to_dict(), indent=2, sort_keys=True),
        encoding="utf-8",
    )
    (output_dir / "archive-verification.md").write_text(
        render_archive_record_markdown(result),
        encoding="utf-8",
    )


def render_archive_record_markdown(result: ArchiveInventoryResult) -> str:
    counts = result.archive_counts
    return "\n".join(
        [
            "# Archive Verification",
            "",
            "## Result",
            "",
            f"- Archive: `{result.archive_path}`",
            f"- Import run ID: `{result.import_run_id}`",
            f"- Profile: `{result.profile_name or ''}`",
            f"- Status: `{result.status}`",
            "",
            "## Written This Run",
            "",
            f"- Source artifacts observed: {result.source_artifact_count}",
            f"- Provenance events recorded: {result.provenance_event_count}",
            "",
            "## Archive Counts",
            "",
            "| Table | Count |",
            "| --- | ---: |",
            f"| source_artifacts | {counts.get('source_artifacts', 0)} |",
            f"| import_runs | {counts.get('import_runs', 0)} |",
            f"| provenance_events | {counts.get('provenance_events', 0)} |",
            "",
        ]
    )

