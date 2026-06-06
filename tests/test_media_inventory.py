import json
import tempfile
import unittest
from pathlib import Path

from markii.media.inventory import inventory_sources
from markii.reports.inventory import write_inventory_reports


FIXTURE = Path(__file__).parent / "fixtures" / "media-inventory"


class MediaInventoryTests(unittest.TestCase):
    def test_inventory_classifies_files_and_detects_duplicates(self):
        result = inventory_sources([FIXTURE])

        self.assertEqual(result.summary.total_files_scanned, 6)
        self.assertEqual(result.summary.xml_count, 2)
        self.assertEqual(result.summary.pixelpost_xml_count, 1)
        self.assertEqual(result.summary.wordpress_wxr_count, 1)
        self.assertEqual(result.summary.jpeg_count, 2)
        self.assertEqual(result.summary.thumbnail_count, 1)
        self.assertEqual(result.summary.unsupported_count, 1)
        self.assertEqual(result.summary.duplicate_filename_count, 1)
        self.assertEqual(result.summary.duplicate_hash_count, 1)

        jpeg = next(artifact for artifact in result.artifacts if artifact.filename == "photo.jpg")
        self.assertEqual((jpeg.image_width, jpeg.image_height), (3, 2))
        self.assertEqual(len(jpeg.sha256), 64)

    def test_report_files_are_written(self):
        result = inventory_sources([FIXTURE])
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir)
            write_inventory_reports(result, output)
            markdown = output / "media-inventory.md"
            json_report = output / "media-inventory.json"

            self.assertTrue(markdown.exists())
            self.assertTrue(json_report.exists())
            data = json.loads(json_report.read_text(encoding="utf-8"))
            self.assertEqual(data["summary"]["total_files_scanned"], 6)
            self.assertIn("Artifact Inventory", markdown.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()

