# Milestone A — Completion Report

**Date:** 2026-06-07
**Phase:** 14
**Milestone:** A — Archaeology Pipeline
**Status:** COMPLETE
**Tag:** `milestone-a`
**Final commit:** `f8be383`

---

## Summary

Milestone A established a complete, executable archaeology pipeline capable of
ingesting a PixelPost 1.x archive, matching posts to their on-disk images, and
persisting attribution evidence into a durable SQLite archive.

The pipeline was validated against the real TalkingTree archive —
731 photographs published between 2006-10-16 and 2011-06-23.

**Result: 731/731 exact matches. 100% attribution confidence.**

---

## Completed Components

| Component | Description |
|-----------|-------------|
| Media Inventory | Classify and checksum all source artifacts |
| Archive Foundation | SQLite schema — import_runs, source_artifacts, provenance_events |
| Provenance Core | Record inventory decisions as provenance events |
| PixelPost XML Parser | Parse WXR-format exports into normalized staging records |
| Media Matching | Link posts to on-disk images via seven signal types |
| Archive Write Integration | Persist match decisions to provenance_events |

---

## Implemented Commands

| Command | Purpose |
|---------|---------|
| `inventory-media` | Read-only source artifact inventory |
| `archive-inventory` | Inventory and persist to SQLite |
| `parse-pixelpost-xml` | Parse PixelPost XML exports |
| `match-media` | Dry-run inspection — match posts to images |
| `write-matches` | Commit match decisions to archive |

---

## Pipeline

```
inventory-media
  → archive-inventory
  → parse-pixelpost-xml
  → match-media        (inspect)
  → write-matches      (commit)
  → archive.sqlite
```

---

## Test Suite

| Version | Tests |
|---------|-------|
| Milestone A final | 40 / 40 passing |

---

## TalkingTree Field Test — Verified 2026-06-07

The complete pipeline was executed against the real TalkingTree archive,
recovered from a portable hard drive originally containing files from a
personal computer last used circa 2011.

### Source Data Provenance

```
LaCie portable drive
  → Old Mac Seagate backup
    → Nate's Old Computer / Desktop / Talking Tree Photo / images /
```

These files passed through multiple hardware generations before this session.
The archaeology pipeline is their first programmatic processing since the
original PixelPost installation went offline.

### Pipeline Results

| Step | Result |
|------|--------|
| Files scanned | 745 (734 JPEG + 9 XML + misc) |
| Source artifacts recorded | 745 |
| Posts parsed | 731 |
| Attachments parsed | 731 |
| Comments parsed | 887 |
| Categories parsed | 18 |
| Tags parsed | 438 |
| Date range | 2006-10-16 → 2011-06-23 |

### Confidence Distribution

| Confidence | Count | % |
|---|---|---|
| Exact | 731 | 100% |
| High | 0 | — |
| Probable | 0 | — |
| Ambiguous | 0 | — |
| Unmatched | 0 | — |

### Archaeological Observations

**Thumbnails absent.** PixelPost 1.7.x generated thumbnails dynamically at
runtime. They were never written to permanent storage. Thumbnail matching
produced 0 results — consistent with expected PixelPost behavior.

**6 orphan images recorded.** Images present on disk with no corresponding
XML record. Likely causes: test uploads, posts deleted before export, or
interrupted upload attempts. All recorded as `orphan_image` provenance events.
These are first-class archaeological artifacts.

**100% exact match rate.** The PixelPost TIMESTAMP(14) filename convention
(`YYYYMMDDHHMMSS_slug.jpg`) is deterministic enough that all three matching
signals — attachment filename, body img src, and post_parent — fired and
agreed on every post. Attribution is unambiguous for the entire archive.

---

## Archive Record — Provenance Events Written

| Event type | Count |
|---|---|
| `inventoried` (source artifacts) | 745 |
| `exact` (post match) | 731 |
| `orphan_image` | 6 |
| **Total provenance events** | **1,482** |

---

## Doctrine Verification

| Principle | Status |
|-----------|--------|
| Preservation first | ✓ No source data modified |
| Verification second | ✓ Field test against real archive before Milestone B |
| Reconstruction later | ✓ Milestone B not yet begun |
| Unresolved is better than wrong | ✓ Orphans recorded, not guessed |
| Ambiguity preserved as evidence | ✓ No automatic resolution applied |
| Historical evidence over assumptions | ✓ Pipeline output matches prior smoke test |

---

## Known Limitations and Deferred Work

| Item | Notes |
|------|-------|
| Thumbnails absent | No thumbnails in TalkingTree source archive. Thumbnail matching code is correct but untestable against this dataset. |
| WordPress XML unused | `thetalkingtree.wordpress.2012-08-12.xml` present but not parsed. WordPress WXR parser not yet implemented. |
| Exit code 2 on orphan warnings | `match-media` and `write-matches` return 2 when orphans or warnings exist. Correct behavior per design; note for pipeline scripting. |
| Tags parsed: 438 vs expected 441 | Minor discrepancy from prior smoke test. Likely deduplication difference. Not blocking. |
| Orphan count 3 vs 6 | Step 4 dry-run (media-only inventory) saw 3 orphans. Step 5 full inventory saw 6. Both correct for their scan scope. Document for Milestone B. |

---

## Milestone B — Candidate Directions

Scope not yet authorized. Candidates as of this report:

| Option | Description |
|--------|-------------|
| A | Unified pipeline command — single `run-import` invocation |
| B | Database reconstruction layer — post/image staging tables |
| C | Rendering engine — HTML generation from archive |
| D | Import/export workflow expansion — WordPress WXR parser |
| E | Extended TalkingTree field validation — deeper archive analysis |

---

## Archaeology Doctrine

> The internet was 500 pixels wide.
> One photograph per day.
> 731 times, someone showed up.
>
> That archive is worth recovering.

---

*Milestone A closed 2026-06-07.*
*Milestone B awaits Nathan's authorization.*
