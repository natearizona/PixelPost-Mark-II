import json
from pathlib import Path

from markii.media.inventory import InventoryResult


def write_inventory_reports(result: InventoryResult, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "media-inventory.json").write_text(
        json.dumps(result.to_dict(), indent=2, sort_keys=True),
        encoding="utf-8",
    )
    (output_dir / "media-inventory.md").write_text(
        render_inventory_markdown(result),
        encoding="utf-8",
    )


def render_inventory_markdown(result: InventoryResult) -> str:
    summary = result.summary
    lines = [
        "# Media Inventory",
        "",
        "## Sources",
        "",
    ]
    for source in result.sources:
        lines.append(f"- `{source}`")

    lines.extend(
        [
            "",
            "## Summary",
            "",
            "| Metric | Count |",
            "| --- | ---: |",
            f"| Total files scanned | {summary.total_files_scanned} |",
            f"| XML files | {summary.xml_count} |",
            f"| PixelPost XML files | {summary.pixelpost_xml_count} |",
            f"| WordPress WXR files | {summary.wordpress_wxr_count} |",
            f"| JPEG originals | {summary.jpeg_count} |",
            f"| Thumbnails | {summary.thumbnail_count} |",
            f"| Unknown files | {summary.unknown_count} |",
            f"| Unsupported files | {summary.unsupported_count} |",
            f"| Unreadable files | {summary.unreadable_files} |",
            f"| Duplicate filenames | {summary.duplicate_filename_count} |",
            f"| Duplicate hashes | {summary.duplicate_hash_count} |",
            "",
            "## Warnings",
            "",
        ]
    )

    if summary.warnings:
        lines.extend(f"- {warning}" for warning in summary.warnings)
    else:
        lines.append("- None")

    lines.extend(["", "## Duplicate Filenames", ""])
    _append_duplicate_section(lines, result.duplicate_filenames)

    lines.extend(["", "## Duplicate Hashes", ""])
    _append_duplicate_section(lines, result.duplicate_hashes)

    lines.extend(
        [
            "",
            "## Artifact Inventory",
            "",
            "| Type | Filename | Size | SHA-256 | Dimensions | Rule |",
            "| --- | --- | ---: | --- | --- | --- |",
        ]
    )
    for artifact in result.artifacts:
        dimensions = ""
        if artifact.image_width is not None and artifact.image_height is not None:
            dimensions = f"{artifact.image_width}x{artifact.image_height}"
        digest = artifact.sha256 or ""
        digest_display = digest[:16] + "..." if digest else ""
        lines.append(
            "| "
            + " | ".join(
                [
                    artifact.artifact_type,
                    f"`{artifact.filename}`",
                    str(artifact.file_size if artifact.file_size is not None else ""),
                    f"`{digest_display}`",
                    dimensions,
                    artifact.detection_rule,
                ]
            )
            + " |"
        )

    lines.append("")
    return "\n".join(lines)


def _append_duplicate_section(lines: list[str], duplicates: dict[str, list[str]]) -> None:
    if not duplicates:
        lines.append("- None")
        return
    for key, paths in sorted(duplicates.items()):
        lines.append(f"- `{key}`")
        for path in paths:
            lines.append(f"  - `{path}`")

