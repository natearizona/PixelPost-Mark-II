"""Tests for Phase 14 Step 4 — Media Matching.

Fixture layout:
  fixtures/media-match/
    pixelpost-export-media-match.xml  — 5 posts, 4 attachment records
    images/
      20080101010101_red-rock.jpg     — exact match for post 101
      20080202020202_canyon-light.jpg — high confidence for post 102
      20080303030303_desert-trail.jpg — probable for post 103
      ambig-mesa.jpg                  — ambiguous candidate A for post 104
      ambig-mesa-copy.jpg             — orphan image (no post references it)
      orphan-sunset.jpg               — orphan image
    thumbnails/
      thumb_20080101010101_red-rock.jpg      — matched thumbnail for post 101
      thumb_20080202020202_canyon-light.jpg  — matched thumbnail for post 102
      ambig-mesa.jpg                         — ambiguous candidate B for post 104 (same filename)
      orphan-thumb.jpg                       — orphan thumbnail

Confidence expectations:
  post 101: exact   — S1 + S2 + S3 all fire and agree
  post 102: high    — S1 + S3 fire, S2 absent (empty body)
  post 103: probable — S2 only, no attachment record, timestamp mismatch
  post 104: ambiguous — two on-disk files named ambig-mesa.jpg
  post 105: unmatched — no img tag, no attachment record
"""
import json
import tempfile
import unittest
from pathlib import Path

from markii.importers.pixelpost_xml import parse_pixelpost_exports
from markii.media.inventory import inventory_sources
from markii.media.matcher import match_media
from markii.reports.media_match import write_media_match_reports


FIXTURE_DIR = Path(__file__).parent / "fixtures" / "media-match"
FIXTURE_XML = FIXTURE_DIR / "pixelpost-export-media-match.xml"
FIXTURE_IMAGES = FIXTURE_DIR / "images"
FIXTURE_THUMBS = FIXTURE_DIR / "thumbnails"


class MediaMatchTests(unittest.TestCase):

    def setUp(self):
        parse_result = parse_pixelpost_exports([FIXTURE_XML])
        inventory = inventory_sources([FIXTURE_IMAGES, FIXTURE_THUMBS])
        self.result = match_media(parse_result, inventory)
        self.by_post_id = {m.post_legacy_id: m for m in self.result.matches}

    # ------------------------------------------------------------------
    # Confidence level tests
    # ------------------------------------------------------------------

    def test_post_101_exact(self):
        m = self.by_post_id["101"]
        self.assertEqual(m.confidence, "exact")
        self.assertIsNotNone(m.matched_artifact_path)
        self.assertIn("20080101010101_red-rock.jpg", m.matched_artifact_path)
        self.assertEqual(m.candidate_count, 1)
        signal_types = [s.signal_type for s in m.signals]
        self.assertIn("attachment_filename", signal_types)
        self.assertIn("body_img_src", signal_types)
        self.assertIn("post_parent", signal_types)

    def test_post_101_thumbnail_matched(self):
        m = self.by_post_id["101"]
        self.assertIsNotNone(m.thumbnail_artifact_path)
        self.assertIn("thumb_20080101010101_red-rock.jpg", m.thumbnail_artifact_path)

    def test_post_102_high_confidence(self):
        m = self.by_post_id["102"]
        self.assertEqual(m.confidence, "high")
        self.assertIsNotNone(m.matched_artifact_path)
        self.assertIn("20080202020202_canyon-light.jpg", m.matched_artifact_path)
        signal_types = [s.signal_type for s in m.signals]
        self.assertIn("attachment_filename", signal_types)
        self.assertIn("post_parent", signal_types)
        self.assertNotIn("body_img_src", signal_types)

    def test_post_102_thumbnail_matched(self):
        m = self.by_post_id["102"]
        self.assertIsNotNone(m.thumbnail_artifact_path)
        self.assertIn("thumb_20080202020202_canyon-light.jpg", m.thumbnail_artifact_path)

    def test_post_103_probable(self):
        m = self.by_post_id["103"]
        self.assertEqual(m.confidence, "probable")
        self.assertIsNotNone(m.matched_artifact_path)
        self.assertIn("20080303030303_desert-trail.jpg", m.matched_artifact_path)
        signal_types = [s.signal_type for s in m.signals]
        self.assertIn("body_img_src", signal_types)
        self.assertNotIn("attachment_filename", signal_types)
        self.assertNotIn("post_parent", signal_types)

    def test_post_104_ambiguous(self):
        m = self.by_post_id["104"]
        self.assertEqual(m.confidence, "ambiguous")
        self.assertIsNone(m.matched_artifact_path)   # do not choose
        self.assertIsNone(m.thumbnail_artifact_path)  # no thumbnail when ambiguous
        self.assertEqual(m.candidate_count, 2)
        self.assertEqual(len(m.all_candidate_paths), 2)

    def test_post_105_unmatched(self):
        m = self.by_post_id["105"]
        self.assertEqual(m.confidence, "unmatched")
        self.assertIsNone(m.matched_artifact_path)
        self.assertEqual(m.candidate_count, 0)

    # ------------------------------------------------------------------
    # Orphan tests
    # ------------------------------------------------------------------

    def test_orphan_images_recorded(self):
        orphan_paths = {o.artifact_path for o in self.result.orphan_media}
        # orphan-sunset.jpg has no post referencing it
        self.assertTrue(
            any("orphan-sunset.jpg" in p for p in orphan_paths),
            f"Expected orphan-sunset.jpg in orphans: {orphan_paths}",
        )

    def test_orphan_thumbnails_recorded(self):
        orphan_paths = {o.artifact_path for o in self.result.orphan_media}
        self.assertTrue(
            any("orphan-thumb.jpg" in p for p in orphan_paths),
            f"Expected orphan-thumb.jpg in orphans: {orphan_paths}",
        )

    def test_orphan_types_distinct(self):
        orphan_images = [o for o in self.result.orphan_media if o.artifact_type == "jpeg"]
        orphan_thumbs = [o for o in self.result.orphan_media if o.artifact_type == "thumbnail"]
        self.assertGreater(len(orphan_images), 0)
        self.assertGreater(len(orphan_thumbs), 0)

    def test_ambiguous_candidates_in_orphans(self):
        # Ambiguous candidates (ambig-mesa.jpg in two locations) should appear
        # in orphan_media with reason=ambiguity_unresolved
        ambig_orphans = [
            o for o in self.result.orphan_media
            if o.reason == "ambiguity_unresolved"
        ]
        self.assertEqual(len(ambig_orphans), 2)

    # ------------------------------------------------------------------
    # Summary tests
    # ------------------------------------------------------------------

    def test_summary_counts(self):
        s = self.result.summary
        self.assertEqual(s.posts_total, 5)
        self.assertEqual(s.matches_exact, 1)
        self.assertEqual(s.matches_high, 1)
        self.assertEqual(s.matches_probable, 1)
        self.assertEqual(s.matches_ambiguous, 1)
        self.assertEqual(s.unmatched_posts, 1)
        self.assertEqual(s.thumbnails_matched, 2)

    def test_status_with_warnings(self):
        # Ambiguous and unmatched posts → completed_with_warnings
        self.assertEqual(self.result.status, "completed_with_warnings")

    # ------------------------------------------------------------------
    # Report output tests
    # ------------------------------------------------------------------

    def test_reports_written(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)
            write_media_match_reports(self.result, output)

            md_path = output / "media-match-report.md"
            json_path = output / "media-match-report.json"
            self.assertTrue(md_path.exists())
            self.assertTrue(json_path.exists())

    def test_json_report_structure(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)
            write_media_match_reports(self.result, output)
            data = json.loads((output / "media-match-report.json").read_text(encoding="utf-8"))

            self.assertIn("matches", data)
            self.assertIn("orphan_media", data)
            self.assertIn("summary", data)
            self.assertIn("status", data)
            self.assertEqual(len(data["matches"]), 5)
            self.assertEqual(data["summary"]["posts_total"], 5)

    def test_markdown_contains_confidence_labels(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)
            write_media_match_reports(self.result, output)
            md = (output / "media-match-report.md").read_text(encoding="utf-8")

            self.assertIn("exact", md)
            self.assertIn("high", md)
            self.assertIn("probable", md)
            self.assertIn("ambiguous", md)
            self.assertIn("unmatched", md)

    def test_matches_sorted_by_date(self):
        dates = [m.post_date for m in self.result.matches]
        self.assertEqual(dates, sorted(dates))

    # ------------------------------------------------------------------
    # Parser prerequisite — post_parent captured
    # ------------------------------------------------------------------

    def test_attachment_post_parent_captured(self):
        parse_result = parse_pixelpost_exports([FIXTURE_XML])
        attachments_by_parent = {a.post_parent: a for a in parse_result.attachments}
        self.assertIn("101", attachments_by_parent)
        self.assertEqual(attachments_by_parent["101"].filename_candidate, "20080101010101_red-rock.jpg")
        self.assertIn("102", attachments_by_parent)
        self.assertIn("104", attachments_by_parent)


if __name__ == "__main__":
    unittest.main()
