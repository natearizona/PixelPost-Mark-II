import json
from pathlib import Path

from markii.importers.pixelpost_xml import PixelPostParseResult


def write_pixelpost_parse_reports(result: PixelPostParseResult, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "pixelpost-parse-report.json").write_text(
        json.dumps(result.to_dict(), indent=2, sort_keys=True),
        encoding="utf-8",
    )
    (output_dir / "pixelpost-parse-report.md").write_text(
        render_pixelpost_parse_markdown(result),
        encoding="utf-8",
    )


def render_pixelpost_parse_markdown(result: PixelPostParseResult) -> str:
    summary = result.summary
    lines = [
        "# PixelPost Parse Report",
        "",
        "## Result",
        "",
        f"- Status: `{result.status}`",
        "",
        "## Source Files",
        "",
    ]
    lines.extend(f"- `{source}`" for source in result.source_files)
    lines.extend(
        [
            "",
            "## Summary",
            "",
            "| Metric | Count |",
            "| --- | ---: |",
            f"| Source files processed | {len(result.source_files)} |",
            f"| Posts parsed | {summary.posts_parsed} |",
            f"| Attachments parsed | {summary.attachments_parsed} |",
            f"| Comments parsed | {summary.comments_parsed} |",
            f"| Categories parsed | {summary.categories_parsed} |",
            f"| Tags parsed | {summary.tags_parsed} |",
            f"| Parser warnings | {len(summary.parser_warnings)} |",
            f"| Malformed records | {len(summary.malformed_records)} |",
            f"| Duplicate ID groups | {len(summary.duplicate_ids)} |",
            "",
            "## Date Range",
            "",
            f"- Earliest: `{summary.date_range.get('earliest') or ''}`",
            f"- Latest: `{summary.date_range.get('latest') or ''}`",
            "",
            "## Parser Warnings",
            "",
        ]
    )
    lines.extend(_list_or_none(summary.parser_warnings))
    lines.extend(["", "## Malformed Records", ""])
    lines.extend(_list_or_none(summary.malformed_records))
    lines.extend(["", "## Duplicate IDs", ""])
    if summary.duplicate_ids:
        for group, values in summary.duplicate_ids.items():
            lines.append(f"- `{group}`: {', '.join(values)}")
    else:
        lines.append("- None")

    lines.extend(
        [
            "",
            "## Parsed Posts",
            "",
            "| Legacy ID | Date | Status | Slug | Title |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for post in result.posts:
        lines.append(f"| `{post.legacy_id}` | {post.publication_date} | {post.status} | `{post.slug}` | {post.title} |")

    lines.extend(
        [
            "",
            "## Parsed Attachments",
            "",
            "| Legacy ID | Filename Candidate | Attachment URL |",
            "| --- | --- | --- |",
        ]
    )
    for attachment in result.attachments:
        lines.append(f"| `{attachment.legacy_id}` | `{attachment.filename_candidate}` | {attachment.attachment_url} |")

    lines.append("")
    return "\n".join(lines)


def _list_or_none(values: list[str]) -> list[str]:
    if not values:
        return ["- None"]
    return [f"- {value}" for value in values]

