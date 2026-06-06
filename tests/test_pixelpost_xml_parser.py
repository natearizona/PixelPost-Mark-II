import json
import tempfile
import unittest
from pathlib import Path

from markii.importers.pixelpost_xml import parse_pixelpost_exports
from markii.reports.pixelpost_parse import write_pixelpost_parse_reports


FIXTURE = Path(__file__).parent / "fixtures" / "pixelpost-xml"


class PixelPostXmlParserTests(unittest.TestCase):
    def test_parser_extracts_posts_attachments_comments_and_taxonomies(self):
        result = parse_pixelpost_exports([FIXTURE])

        self.assertEqual(result.status, "completed")
        self.assertEqual(len(result.source_files), 1)
        self.assertEqual(len(result.posts), 1)
        self.assertEqual(len(result.attachments), 1)
        self.assertEqual(len(result.comments), 2)
        self.assertEqual(len(result.categories), 1)
        self.assertEqual(len(result.tags), 1)

        post = result.posts[0]
        self.assertEqual(post.legacy_id, "101")
        self.assertEqual(post.title, "Red Rock Morning")
        self.assertEqual(post.slug, "red-rock-morning")
        self.assertEqual(post.publication_date, "2008-01-01 01:01:01")
        self.assertEqual(post.status, "publish")
        self.assertIn("Morning light over red rock.", post.body)
        self.assertEqual(post.guid, "http://talkingtree.org/?p=101")

        attachment = result.attachments[0]
        self.assertEqual(attachment.legacy_id, "102")
        self.assertEqual(attachment.filename_candidate, "20080101010101_red-rock.jpg")
        self.assertEqual(attachment.post_parent, "101")
        self.assertEqual(attachment.guid, "http://talkingtree.org/images/20080101010101_red-rock.jpg")

        comment = result.comments[1]
        self.assertEqual(comment.legacy_id, "9002")
        self.assertEqual(comment.post_id, "101")
        self.assertEqual(comment.author, "Another Visitor")
        self.assertEqual(comment.author_email, "another@example.invalid")
        self.assertEqual(comment.approval_status, "0")
        self.assertEqual(comment.parent_id, "9001")

        self.assertEqual(result.summary.date_range["earliest"], "2008-01-01 01:01:01")
        self.assertEqual(result.summary.date_range["latest"], "2008-01-01 01:01:01")
        self.assertEqual(result.summary.duplicate_ids, {})

    def test_reports_are_written(self):
        result = parse_pixelpost_exports([FIXTURE])
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir)
            write_pixelpost_parse_reports(result, output)

            markdown = output / "pixelpost-parse-report.md"
            json_report = output / "pixelpost-parse-report.json"
            self.assertTrue(markdown.exists())
            self.assertTrue(json_report.exists())
            data = json.loads(json_report.read_text(encoding="utf-8"))
            self.assertEqual(data["summary"]["posts_parsed"], 1)
            self.assertIn("Red Rock Morning", markdown.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
