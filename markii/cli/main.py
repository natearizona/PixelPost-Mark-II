import argparse
from pathlib import Path

from markii.importers.pixelpost_xml import parse_pixelpost_exports
from markii.media.inventory import inventory_sources
from markii.provenance.inventory_archive import record_inventory
from markii.reports.archive import write_archive_record_reports
from markii.reports.inventory import write_inventory_reports
from markii.reports.pixelpost_parse import write_pixelpost_parse_reports


def main(argv=None):
    parser = argparse.ArgumentParser(prog="markii")
    subparsers = parser.add_subparsers(dest="command", required=True)

    inventory_parser = subparsers.add_parser(
        "inventory-media",
        help="Create a read-only source artifact inventory.",
    )
    inventory_parser.add_argument(
        "--source",
        action="append",
        required=True,
        help="Source path to scan. May be supplied more than once.",
    )
    inventory_parser.add_argument(
        "--output",
        required=True,
        help="Directory where media-inventory.md and media-inventory.json are written.",
    )
    inventory_parser.add_argument(
        "--profile",
        default=None,
        help="Optional import profile hint for artifact classification.",
    )

    archive_parser = subparsers.add_parser(
        "archive-inventory",
        help="Inventory source artifacts and persist them to a SQLite archive.",
    )
    archive_parser.add_argument(
        "--source",
        action="append",
        required=True,
        help="Source path to scan. May be supplied more than once.",
    )
    archive_parser.add_argument(
        "--archive",
        required=True,
        help="SQLite archive path to create or open.",
    )
    archive_parser.add_argument(
        "--output",
        required=True,
        help="Directory where verification reports are written.",
    )
    archive_parser.add_argument(
        "--profile",
        default=None,
        help="Optional profile name recorded with the inventory run.",
    )

    parse_parser = subparsers.add_parser(
        "parse-pixelpost-xml",
        help="Parse PixelPost XML exports into normalized staging records.",
    )
    parse_parser.add_argument(
        "--xml",
        action="append",
        required=True,
        help="PixelPost XML export file or directory. May be supplied more than once.",
    )
    parse_parser.add_argument(
        "--output",
        required=True,
        help="Directory where pixelpost-parse-report.md and pixelpost-parse-report.json are written.",
    )

    args = parser.parse_args(argv)

    if args.command == "inventory-media":
        sources = [Path(source) for source in args.source]
        output = Path(args.output)
        result = inventory_sources(sources, profile=args.profile)
        write_inventory_reports(result, output)
        print(f"Scanned {result.summary.total_files_scanned} files")
        print(f"Wrote {output / 'media-inventory.md'}")
        print(f"Wrote {output / 'media-inventory.json'}")
        if result.summary.unreadable_files:
            return 2
        return 0

    if args.command == "archive-inventory":
        sources = [Path(source) for source in args.source]
        archive = Path(args.archive)
        output = Path(args.output)
        inventory = inventory_sources(sources, profile=args.profile)
        result = record_inventory(inventory, archive, profile=args.profile)
        write_archive_record_reports(result, output)
        print(f"Scanned {inventory.summary.total_files_scanned} files")
        print(f"Archive {archive}")
        print(f"Recorded import run {result.import_run_id}")
        print(f"Recorded {result.source_artifact_count} source artifacts")
        print(f"Recorded {result.provenance_event_count} provenance events")
        print(f"Wrote {output / 'archive-verification.md'}")
        print(f"Wrote {output / 'archive-verification.json'}")
        if inventory.summary.unreadable_files:
            return 2
        return 0

    if args.command == "parse-pixelpost-xml":
        sources = [Path(source) for source in args.xml]
        output = Path(args.output)
        result = parse_pixelpost_exports(sources)
        write_pixelpost_parse_reports(result, output)
        print(f"Processed {len(result.source_files)} source files")
        print(f"Parsed {len(result.posts)} posts")
        print(f"Parsed {len(result.attachments)} attachments")
        print(f"Parsed {len(result.comments)} comments")
        print(f"Parsed {len(result.categories)} categories")
        print(f"Parsed {len(result.tags)} tags")
        print(f"Wrote {output / 'pixelpost-parse-report.md'}")
        print(f"Wrote {output / 'pixelpost-parse-report.json'}")
        return 0 if result.status == "completed" else 2

    parser.error(f"Unknown command: {args.command}")
    return 2
