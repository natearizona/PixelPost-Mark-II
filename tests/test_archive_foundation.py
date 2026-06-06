import sqlite3
import tempfile
import unittest
from pathlib import Path

from markii.media.inventory import inventory_sources
from markii.provenance.inventory_archive import record_inventory
from markii.reports.archive import write_archive_record_reports
from markii.storage.archive import fetch_counts


FIXTURE = Path(__file__).parent / "fixtures" / "media-inventory"


class ArchiveFoundationTests(unittest.TestCase):
    def test_inventory_artifacts_are_persisted_with_provenance(self):
        inventory = inventory_sources([FIXTURE], profile="fixture")
        with tempfile.TemporaryDirectory() as temp_dir:
            archive_path = Path(temp_dir) / "archive.sqlite"
            result = record_inventory(inventory, archive_path, profile="fixture")

            self.assertTrue(archive_path.exists())
            self.assertEqual(result.status, "completed")
            self.assertEqual(result.source_artifact_count, 6)
            self.assertEqual(result.provenance_event_count, 6)

            counts = fetch_counts(archive_path)
            self.assertEqual(counts["source_artifacts"], 6)
            self.assertEqual(counts["import_runs"], 1)
            self.assertEqual(counts["provenance_events"], 6)

            with sqlite3.connect(archive_path) as connection:
                row = connection.execute(
                    """
                    SELECT source_path, filename, artifact_type, file_size, sha256, detection_rule
                    FROM source_artifacts
                    WHERE filename = 'photo.jpg'
                    ORDER BY source_path
                    LIMIT 1
                    """
                ).fetchone()
            self.assertIn("photo.jpg", row[0])
            self.assertEqual(row[1], "photo.jpg")
            self.assertEqual(row[2], "jpeg")
            self.assertEqual(row[3], 41)
            self.assertEqual(len(row[4]), 64)
            self.assertEqual(row[5], "jpeg extension")

    def test_repeatable_execution_adds_run_and_events_without_duplicating_artifacts(self):
        inventory = inventory_sources([FIXTURE], profile="fixture")
        with tempfile.TemporaryDirectory() as temp_dir:
            archive_path = Path(temp_dir) / "archive.sqlite"
            record_inventory(inventory, archive_path, profile="fixture")
            record_inventory(inventory, archive_path, profile="fixture")

            counts = fetch_counts(archive_path)
            self.assertEqual(counts["source_artifacts"], 6)
            self.assertEqual(counts["import_runs"], 2)
            self.assertEqual(counts["provenance_events"], 12)

    def test_archive_verification_report_is_written(self):
        inventory = inventory_sources([FIXTURE], profile="fixture")
        with tempfile.TemporaryDirectory() as temp_dir:
            archive_path = Path(temp_dir) / "archive.sqlite"
            output = Path(temp_dir) / "reports"
            result = record_inventory(inventory, archive_path, profile="fixture")
            write_archive_record_reports(result, output)

            self.assertTrue((output / "archive-verification.md").exists())
            self.assertTrue((output / "archive-verification.json").exists())


if __name__ == "__main__":
    unittest.main()
