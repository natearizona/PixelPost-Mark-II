"""Tests for Phase 14 Step 5 — Archive Write Integration.

Verifies that MediaMatchResult and OrphanArtifact records are correctly
persisted into provenance_events without modifying the matching engine.

Fixture reuse: tests/fixtures/media-match/ (same as Step 4 tests).

Post confidence expectations (from Step 4):
  post 101: exact      — matched image + thumbnail
  post 102: high       — matched image + thumbnail
  post 103: probable   — matched image, no thumbnail
  post 104: ambiguous  — no resolved path, ambiguity preserved
  post 105: unmatched  — linked to XML source artifact
"""
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

from markii.importers.pixelpost_xml import parse_pixelpost_exports
from markii.media.inventory import inventory_sources
from markii.media.matcher import match_media
from markii.provenance.match_archive import record_matches


FIXTURE_DIR = Path(__file__).parent / "fixtures" / "media-match"
FIXTURE_XML = FIXTURE_DIR / "pixelpost-export-media-match.xml"
FIXTURE_IMAGES = FIXTURE_DIR / "images"
FIXTURE_THUMBS = FIXTURE_DIR / "thumbnails"


class ArchiveMatchWriteTests(unittest.TestCase):

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        tmp = Path(self._tmp.name)
        self.archive_path = tmp / "test-archive.db"

        # Full inventory: XML + images + thumbnails
        full_inventory = inventory_sources([FIXTURE_XML, FIXTURE_IMAGES, FIXTURE_THUMBS])
        parse_result = parse_pixelpost_exports([FIXTURE_XML])
        self.match_result = match_media(parse_result, full_inventory)
        self.archive_result = record_matches(
            self.match_result, full_inventory, self.archive_path
        )

        # Direct DB access for assertions
        conn = sqlite3.connect(self.archive_path)
        conn.row_factory = sqlite3.Row
        self.events = [dict(r) for r in conn.execute("SELECT * FROM provenance_events").fetchall()]
        self.artifacts = {
            r["id"]: dict(r)
            for r in conn.execute("SELECT * FROM source_artifacts").fetchall()
        }
        conn.close()

        self.events_by_entity = {}
        for e in self.events:
            key = (e["entity_type"], e["entity_id"])
            self.events_by_entity.setdefault(key, []).append(e)

    def tearDown(self):
        self._tmp.cleanup()

    # ------------------------------------------------------------------
    # ArchiveMatchResult structure
    # ------------------------------------------------------------------

    def test_archive_result_has_expected_fields(self):
        r = self.archive_result
        self.assertEqual(r.status, "completed")
        self.assertIsInstance(r.import_run_id, int)
        self.assertGreater(r.match_event_count, 0)
        self.assertGreater(r.orphan_event_count, 0)
        self.assertIn("provenance_events", r.archive_counts)

    # ------------------------------------------------------------------
    # Exact match — post 101
    # ------------------------------------------------------------------

    def test_exact_match_written_with_correct_decision(self):
        events = self.events_by_entity.get(("post", "101"), [])
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["decision"], "exact")

    def test_exact_match_signals_in_notes(self):
        events = self.events_by_entity[("post", "101")]
        notes = json.loads(events[0]["notes"])
        self.assertIn("signals", notes)
        self.assertIsInstance(notes["signals"], list)
        self.assertGreater(len(notes["signals"]), 0)

    def test_exact_match_thumbnail_written(self):
        events = self.events_by_entity.get(("thumbnail", "101"), [])
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["decision"], "exact")

    # ------------------------------------------------------------------
    # Ambiguous match — post 104
    # ------------------------------------------------------------------

    def test_ambiguous_match_written_with_correct_decision(self):
        events = self.events_by_entity.get(("post", "104"), [])
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["decision"], "ambiguous")

    def test_ambiguous_notes_preserve_candidate_paths(self):
        events = self.events_by_entity[("post", "104")]
        notes = json.loads(events[0]["notes"])
        self.assertIn("candidate_count", notes)
        self.assertGreater(notes["candidate_count"], 1)
        self.assertIn("all_candidate_paths", notes)
        self.assertGreater(len(notes["all_candidate_paths"]), 1)

    # ------------------------------------------------------------------
    # Unmatched post — post 105
    # ------------------------------------------------------------------

    def test_unmatched_post_written_with_correct_decision(self):
        events = self.events_by_entity.get(("post", "105"), [])
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["decision"], "unmatched")

    def test_unmatched_post_links_to_xml_artifact(self):
        events = self.events_by_entity[("post", "105")]
        artifact_id = events[0]["source_artifact_id"]
        artifact = self.artifacts[artifact_id]
        self.assertEqual(artifact["artifact_type"], "pixelpost_xml")

    # ------------------------------------------------------------------
    # Orphan image
    # ------------------------------------------------------------------

    def test_orphan_image_written_with_correct_entity_type(self):
        orphan_events = [
            e for e in self.events if e["entity_type"] == "orphan_image"
        ]
        self.assertGreater(len(orphan_events), 0)

    def test_orphan_image_decision_is_correct_reason(self):
        orphan_events = [
            e for e in self.events if e["entity_type"] == "orphan_image"
        ]
        for e in orphan_events:
            self.assertIn(e["decision"], ("no_xml_reference", "ambiguity_unresolved"))

    # ------------------------------------------------------------------
    # Orphan thumbnail
    # ------------------------------------------------------------------

    def test_orphan_thumbnail_written_with_correct_entity_type(self):
        orphan_thumb_events = [
            e for e in self.events if e["entity_type"] == "orphan_thumbnail"
        ]
        self.assertGreater(len(orphan_thumb_events), 0)

    def test_orphan_types_are_distinct(self):
        image_types = {e["entity_type"] for e in self.events if "orphan" in e["entity_type"]}
        self.assertIn("orphan_image", image_types)
        self.assertIn("orphan_thumbnail", image_types)

    # ------------------------------------------------------------------
    # Archive counts
    # ------------------------------------------------------------------

    def test_archive_counts_reflect_all_events(self):
        total_events = self.archive_result.archive_counts["provenance_events"]
        self.assertEqual(total_events, len(self.events))

    def test_all_posts_have_provenance_event(self):
        post_events = [e for e in self.events if e["entity_type"] == "post"]
        post_ids = {e["entity_id"] for e in post_events}
        self.assertEqual(post_ids, {"101", "102", "103", "104", "105"})

    # ------------------------------------------------------------------
    # Idempotency — re-running write-matches must not duplicate records
    # ------------------------------------------------------------------

    def test_rerun_does_not_duplicate_source_artifacts(self):
        full_inventory = inventory_sources([FIXTURE_XML, FIXTURE_IMAGES, FIXTURE_THUMBS])
        parse_result = parse_pixelpost_exports([FIXTURE_XML])
        match_result = match_media(parse_result, full_inventory)
        record_matches(match_result, full_inventory, self.archive_path)

        conn = sqlite3.connect(self.archive_path)
        count = conn.execute("SELECT COUNT(*) FROM source_artifacts").fetchone()[0]
        conn.close()

        # source_artifacts uses UNIQUE(source_path, sha256) — re-run must not grow the table
        original_count = self.archive_result.archive_counts["source_artifacts"]
        self.assertEqual(count, original_count)
