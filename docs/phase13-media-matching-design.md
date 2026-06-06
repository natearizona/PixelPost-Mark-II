# Phase 14 Step 4 — Media Matching: Design Document

**Status:** Design review. No implementation code exists yet.

**Authored:** 2026-06-05

**Constraint:** Implementation may not begin until this document is reviewed and approved.

---

## Purpose

Media matching links parsed XML records (posts, attachments) to on-disk media artifacts (JPEGs, thumbnails) recovered from the original photoblog archive.

The goal is not simply to pair files with posts. The goal is to produce an honest archaeological record: which files can be linked to which posts, at what confidence, and with what evidence. Files that cannot be linked are not discarded — they are recorded as first-class orphan artifacts.

---

## Inputs

| Input | Source | Description |
| --- | --- | --- |
| `PixelPostParseResult` | `markii.importers.pixelpost_xml` | Parsed posts, attachments, taxonomy |
| `InventoryResult` | `markii.media.inventory` | Classified on-disk artifacts with SHA-256, dimensions, paths |

The matcher receives both inputs and produces a `MediaMatchResult`.

---

## Matching Signals

Seven signals are defined. Each signal has a type, a strength classification, and a description of what it matches.

### Signal 1 — Attachment Filename (`attachment_filename`)

**Strength: primary**

`ParsedAttachment.filename_candidate` is extracted from `wp:attachment_url` during XML parsing. This is the most direct link: the XML explicitly declares what file belonged to each post.

Match condition: `attachment.filename_candidate == artifact.filename` (case-insensitive).

**Prerequisite:** `ParsedAttachment` must carry `post_parent` (the `wp:post_parent` field) so the attachment can be joined to its parent post. This field is present in the XML but not yet captured by the parser.

### Signal 2 — Body Image URL (`body_img_src`)

**Strength: primary**

`ParsedPost.body` contains the raw `content:encoded` HTML. Pixelpost exports embed an `<img src="...">` tag pointing to the full image URL. The filename is extracted from the src path.

Match condition: `Path(urlparse(src).path).name == artifact.filename` (case-insensitive).

This is a direct cross-check: if the attachment record and the post body agree on the filename, confidence increases.

### Signal 3 — Post Parent Join (`post_parent`)

**Strength: corroborating**

When an attachment item carries `wp:post_parent` equal to a post's `wp:post_id`, that attachment is explicitly linked to the post by the exporter. This is a relational signal — it confirms the intended association even if filenames are generic.

Used to corroborate Signal 1 or 2. Not used alone as a primary match signal.

### Signal 4 — Thumbnail Naming Convention (`thumbnail_rule`)

**Strength: derived**

Pixelpost names thumbnails `thumb_<original_filename>`. If a primary image match exists at confidence `probable` or better, the corresponding thumbnail is predicted by prepending `thumb_` to the matched filename.

Match condition: `artifact.filename == "thumb_" + matched_primary_filename` (case-insensitive).

This signal is only applied after a primary image is matched. Thumbnails are not independently matched to posts — they are linked through their primary image.

### Signal 5 — Filename Timestamp Correlation (`timestamp_correlation`)

**Strength: corroborating**

Pixelpost filenames carry a 14-digit timestamp prefix: `YYYYMMDDHHMMSS_slug.jpg`. This timestamp can be parsed and compared to `ParsedPost.publication_date`.

Match condition: extracted timestamp matches post date within a defined tolerance (same calendar day, same hour, or exact second).

This is a corroborating signal only. Many posts may share a date, and the timestamp in the filename is often the upload time, not the publication time.

### Signal 6 — URL Domain Consistency (`url_domain`)

**Strength: corroborating**

The domain in `wp:attachment_url` and the domain in the `<img src>` should agree. If they agree and match the known blog domain, this corroborates the association.

Also used to detect anomalies: if attachment_url points to a different domain than img src, flag it in notes.

### Signal 7 — Duplicate Hash (`hash_identity`)

**Strength: tiebreaker**

When multiple on-disk files have identical SHA-256 hashes, they are byte-for-byte copies. If a filename match is found but the artifact has duplicates on disk, all duplicate paths are recorded. The match is not narrowed by hash — identical content in multiple locations is an archaeological observation, not a disambiguation tool.

---

## Confidence Levels

| Level | Value | Criteria |
| --- | --- | --- |
| Exact Match | `exact` | Single candidate. Filename matched via Signal 1 (attachment_filename). Signal 3 (post_parent) corroborates. Signal 2 (body_img_src) corroborates. All three agree. |
| High Confidence | `high` | Single candidate. Filename matched via Signal 1 or Signal 2 (not both required). At least one corroborating signal (Signal 3, 5, or 6) present and consistent. |
| Probable Match | `probable` | Single candidate. Filename matched via exactly one primary signal. No corroboration available (e.g., post body is empty, or no attachment record exists). No contradictions. |
| Ambiguous | `ambiguous` | Multiple candidates with equal primary signal matches that cannot be distinguished. Or conflicting signals that point to different files. Do not silently choose. Record all candidates. |
| Unmatched | `unmatched` | No on-disk artifact matches any signal for this post or attachment. |

### Ambiguity Rule

When multiple on-disk files match the same primary signal for the same post, the matcher **must not choose**. All candidate paths are recorded. Confidence is set to `ambiguous`. The notes field explains the conflict. The operator must resolve.

This applies to:
- Multiple files with the same filename in different directories
- Different files whose filenames both match the same attachment record (e.g., different-sized duplicates with different hashes)

---

## Orphan Media

**Definition:** An on-disk `jpeg` or `thumbnail` artifact that cannot be linked to any post or attachment record at any confidence level.

Orphan artifacts are **not discarded**. They are first-class archaeological artifacts. They appear in a dedicated section of the match result and the report.

Orphan media may represent:
- Images uploaded but never published
- Images from posts that were deleted before the export
- Test uploads or administrative images
- Imported images from a prior migration not reflected in the XML

Each orphan record carries its full artifact metadata: path, filename, SHA-256, file size, image dimensions, and a stated reason for its orphan status.

The reason is one of:
- `no_matching_post` — no XML post references this filename
- `no_attachment_record` — inventory filename has no corresponding attachment record
- `filename_collision_unresolved` — filename matches multiple posts; not attributed to any

---

## Data Structures

### `MatchSignal`

```
MatchSignal:
  signal_type: str          # attachment_filename | body_img_src | post_parent |
                            # thumbnail_rule | timestamp_correlation | url_domain | hash_identity
  matched_value: str        # the value that triggered this signal
                            # (e.g. the filename, the URL, the timestamp string)
  strength: str             # primary | corroborating | derived | tiebreaker
  notes: str                # optional — explains unusual condition or discrepancy
```

### `MediaMatch`

One record per post (not per attachment).

```
MediaMatch:
  post_legacy_id: str               # wp:post_id of the post
  post_slug: str                    # wp:post_name of the post
  post_date: str                    # wp:post_date of the post
  attachment_legacy_id: str | None  # wp:post_id of the linked attachment item, if any
  matched_artifact_path: str | None # absolute path to the matched on-disk JPEG
                                    # None if unmatched or ambiguous
  thumbnail_artifact_path: str | None  # absolute path to matched thumbnail, if found
  confidence: str                   # exact | high | probable | ambiguous | unmatched
  signals: list[MatchSignal]        # all signals evaluated, in order of strength
  candidate_count: int              # number of on-disk files that were considered
  all_candidate_paths: list[str]    # ALL candidates considered — populated even when ambiguous
  notes: list[str]                  # human-readable observations about the match
```

### `OrphanArtifact`

```
OrphanArtifact:
  artifact_path: str        # absolute path to the on-disk file
  filename: str
  artifact_type: str        # jpeg | thumbnail
  sha256: str
  file_size: int | None
  image_width: int | None
  image_height: int | None
  reason: str               # no_matching_post | no_attachment_record | filename_collision_unresolved
```

### `MediaMatchSummary`

```
MediaMatchSummary:
  posts_total: int
  matches_exact: int
  matches_high: int
  matches_probable: int
  matches_ambiguous: int
  unmatched_posts: int
  thumbnails_matched: int
  orphan_images: int
  orphan_thumbnails: int
  warnings: list[str]
```

### `MediaMatchResult`

```
MediaMatchResult:
  xml_source_files: list[str]     # paths to XML files parsed
  media_source_dirs: list[str]    # directories inventoried for media
  matches: list[MediaMatch]       # one per post, sorted by post_date ascending
  orphan_media: list[OrphanArtifact]
  summary: MediaMatchSummary
  status: str                     # completed | completed_with_warnings | failed
```

---

## Multi-Candidate Handling

When two or more on-disk artifacts produce an equal primary signal match for the same post, the following rules apply:

1. Set `confidence` to `ambiguous`.
2. Set `matched_artifact_path` to `None`. Do not choose.
3. Populate `all_candidate_paths` with all matching paths.
4. Set `candidate_count` to the number of candidates.
5. Add a note explaining why the match was not resolved.
6. Do not apply Signal 4 (thumbnail rule) when ambiguous.

The operator must resolve ambiguity externally. The report should make the ambiguity clearly visible.

---

## Report Outputs

Two files are written to the output directory specified at invocation.

### `media-match-report.md`

Human-readable Markdown.

Sections:
1. **Summary table** — counts for each confidence level, orphans, thumbnails matched
2. **Match table** — one row per post
   - Columns: `post_id`, `post_date`, `slug`, `confidence`, `matched_file`, `thumbnail_matched`, `candidate_count`
   - Rows sorted by post_date ascending
3. **Ambiguous matches** — expanded detail block for each ambiguous post, listing all candidate paths and the signals that produced them
4. **Unmatched posts** — table of posts with no match and any partial signal evidence
5. **Orphan media** — table of unattributed on-disk files with filename, type, size, dimensions, SHA-256
6. **Warnings** — all parser and match warnings

### `media-match-report.json`

Machine-readable JSON. Contains the full serialized `MediaMatchResult`:

```json
{
  "xml_source_files": [...],
  "media_source_dirs": [...],
  "summary": { ... },
  "matches": [
    {
      "post_legacy_id": "101",
      "post_slug": "red-rock-morning",
      "post_date": "2008-01-01 01:01:01",
      "attachment_legacy_id": "102",
      "matched_artifact_path": "/path/to/images/20080101010101_red-rock.jpg",
      "thumbnail_artifact_path": "/path/to/thumbnails/thumb_20080101010101_red-rock.jpg",
      "confidence": "exact",
      "signals": [
        {
          "signal_type": "attachment_filename",
          "matched_value": "20080101010101_red-rock.jpg",
          "strength": "primary",
          "notes": ""
        },
        {
          "signal_type": "post_parent",
          "matched_value": "101",
          "strength": "corroborating",
          "notes": ""
        },
        {
          "signal_type": "body_img_src",
          "matched_value": "20080101010101_red-rock.jpg",
          "strength": "corroborating",
          "notes": ""
        }
      ],
      "candidate_count": 1,
      "all_candidate_paths": ["/path/to/images/20080101010101_red-rock.jpg"],
      "notes": []
    }
  ],
  "orphan_media": [],
  "status": "completed"
}
```

---

## Matching Algorithm (Pseudocode)

This is a description of the matching logic. It is not implementation code.

```
For each post in parse_result.posts:

  1. Collect the attachment record for this post:
     candidate_attachment = attachment where attachment.post_parent == post.legacy_id

  2. Collect primary signal candidates:
     a. If candidate_attachment exists:
        - search inventory for artifact.filename == attachment.filename_candidate
        - record as signal: attachment_filename (primary)
     b. Extract img src filenames from post.body
        - for each src filename, search inventory for matching artifact.filename
        - record as signal: body_img_src (primary)

  3. If no primary candidates found:
     - record MediaMatch with confidence=unmatched

  4. If exactly one candidate found (same file from both signals, or one signal only):
     - evaluate corroborating signals:
       - post_parent linkage confirmed → record signal
       - timestamp in filename matches post_date → record signal
       - URL domains consistent → record signal
     - assign confidence:
       - primary signal + 2+ corroborating → exact
       - primary signal + 1 corroborating → high
       - primary signal only → probable

  5. If multiple distinct candidates:
     - record confidence=ambiguous
     - record all candidate paths
     - do not assign matched_artifact_path

  6. If confidence is probable or better:
     - attempt thumbnail match: search inventory for "thumb_" + matched_filename
     - if found: record thumbnail_artifact_path

For each artifact in inventory where artifact_type in {jpeg, thumbnail}:
  If artifact.source_path not in any match's all_candidate_paths:
    Record as OrphanArtifact
```

---

## Parser Prerequisite

`ParsedAttachment` does not currently capture `wp:post_parent`. Signal 3 (post_parent join) requires this field.

Before implementation, `ParsedAttachment` must be extended:

```
ParsedAttachment:
  legacy_id: str
  attachment_url: str
  filename_candidate: str
  guid: str
  post_parent: str        # ← NEW: wp:post_parent, empty string if absent
  source_file: str
```

The XML parser must be updated to extract `wp:post_parent` for attachment items, in `_parse_attachment()`.

This is a minimal, additive change. It does not affect the existing test fixture, as the fixture already carries `<wp:post_parent>101</wp:post_parent>` — the parser currently ignores it.

---

## CLI Command

A new CLI command `match-media` will be added to `markii.cli.main`.

Arguments:
- `--xml` (repeatable): XML export file or directory of XML files
- `--media` (repeatable): directory containing JPEG images
- `--output`: directory to write report files into

Exit codes:
- `0`: completed, all matches resolved at probable or better
- `2`: completed with warnings — one or more ambiguous, unmatched, or orphan artifacts
- `1`: failed — parse or inventory error prevented matching

---

## Implementation Scope

Implementation requires the following new or modified files:

| File | Action | Purpose |
| --- | --- | --- |
| `markii/importers/pixelpost_xml.py` | Modify | Add `post_parent` to `ParsedAttachment`; update `_parse_attachment()` |
| `markii/media/matcher.py` | Create | Matching algorithm; produces `MediaMatchResult` |
| `markii/reports/media_match.py` | Create | Writes `.md` and `.json` report files |
| `markii/cli/main.py` | Modify | Add `match-media` command |
| `tests/fixtures/media-match/` | Create | Minimal XML + JPEG fixture with known match, ambiguous, orphan cases |
| `tests/test_media_match.py` | Create | Unit tests covering each confidence level and orphan detection |

Implementation may not begin until this document is reviewed.

---

## Scope Boundary

This design covers:

- Linking posts to on-disk images using XML-derived signals
- Confidence classification
- Orphan artifact recording
- Report generation

This design does not cover:

- Writing matched records into the SQLite archive (a later step)
- Reconstructing the Pixelpost database from matched records (Phase IV)
- Deduplication of matched images across multiple archive copies
- Matching addons, templates, or non-image media

---

## Open Questions for Review

1. **Timestamp tolerance:** Signal 5 compares filename timestamp to post date. Should the tolerance be exact-second only, or same-hour, or same-calendar-day? The filename timestamp reflects upload time; the post date may differ.

2. **Ambiguity resolution workflow:** When a match is ambiguous, should the report include a suggested resolution path (e.g., "inspect SHA-256 of candidates against known good archive")? Or remain purely descriptive?

3. **Thumbnail orphan handling:** A thumbnail with no matching primary image is an orphan. Should it be classified separately from image orphans, or treated identically in the report?

4. **Multiple img src per post:** Some posts may embed multiple images in the body. The design assumes one primary image per post. Should multi-image posts be flagged as warnings, or handled with a one-to-many match structure?
