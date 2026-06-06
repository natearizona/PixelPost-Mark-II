# Phase 14 Step 4 — Media Matching: Design Review and Lock

**Status:** LOCKED — approved for implementation

**Review Date:** 2026-06-05

**Reviewed Against:** `docs/phase13-media-matching-design.md`

**Reviewed By:** Hynek (Claude Code) acting as cross-project coordinator

**Authorized By:** Nathan Arizona (steward — approval required before implementation begins)

---

## Purpose of This Document

This is the formal review of the Media Matching design. It does three things:

1. Evaluates the design document for correctness, consistency, and completeness
2. Resolves all open questions with locked decisions
3. Corrects two inconsistencies found during review

The design document remains the primary specification. This review document records what was changed and why. Implementation follows from both documents read together, with this review superseding where they conflict.

---

## Review Finding: Two Inconsistencies

### Inconsistency 1 — Confidence Level `exact`: criteria conflict

The confidence table defines `exact` as:

> Signal 1 (attachment_filename) + Signal 3 (post_parent) corroborates + Signal 2 (body_img_src) corroborates. All three agree.

The matching algorithm pseudocode defines `exact` as:

> primary signal + 2+ corroborating → exact

These are different criteria. The table requires both primary signals to fire. The algorithm permits one primary with two corroborations.

**Resolution:** The table is correct. The algorithm pseudocode is imprecise.

`exact` requires:
- Signal 1 (attachment_filename) fires — attachment record in XML names this file
- Signal 2 (body_img_src) fires — post body img src names this file
- Both point to the same on-disk artifact
- Signal 3 (post_parent) confirms the attachment-to-post link

Three independent source paths agree: the attachment record, the post body, and the relational join. This is the strongest achievable evidence in an XML export.

If Signal 2 cannot fire (post body is empty or has no img src), the best achievable confidence is `high`, not `exact`.

**Algorithm pseudocode correction (applies to implementation):**

```
assign confidence:
  Signal 1 AND Signal 2 agree on same file, AND Signal 3 confirmed → exact
  one primary fires AND at least one corroborating signal confirmed → high
  one primary fires, no corroboration available, no contradiction → probable
```

---

### Inconsistency 2 — Orphan reason `no_attachment_record` is ambiguous

The design defines two reasons that are not clearly distinct:

- `no_matching_post` — no XML post references this filename
- `no_attachment_record` — inventory filename has no corresponding attachment record

If no XML post references the filename, then by definition there is also no attachment record for it. The two reasons overlap.

**Resolution:** Replace both with a cleaner two-reason taxonomy.

**Locked orphan reason taxonomy:**

| Reason | Meaning |
| --- | --- |
| `no_xml_reference` | This filename appears in no XML signal — neither in any attachment record's filename_candidate nor in any post body's img src. There is no archaeological link between this file and any known post. |
| `ambiguity_unresolved` | This file was a candidate for at least one post match, but that match was classified as ambiguous and not resolved. The file is not attributed to any post until ambiguity is resolved by the operator. |

These two cases cover the complete population of orphan artifacts.

---

## Open Questions: Locked Decisions

### Question 1 — Timestamp tolerance for Signal 5

**Decision: same-calendar-day.**

Timestamp correlation is a corroborating signal only. It does not decide a match. It adds one unit of corroborating evidence when the filename's embedded timestamp falls on the same calendar day as the post's publication date.

Rationale:
- Pixelpost's filename timestamp reflects upload time, not publication time. A photographer may upload in the morning and publish in the evening; exact-second or same-hour matching would produce false negatives.
- Same-calendar-day is generous enough to capture the legitimate upload-same-day-as-publish pattern without introducing cross-day false positives.
- This signal is one corroborating vote among several. It cannot alone push confidence from `probable` to `high`. Over-precision here has no benefit.

**Locked rule:** Signal 5 fires if the 8-digit date prefix of the filename (`YYYYMMDD`) matches the calendar date extracted from `ParsedPost.publication_date`. Time components are ignored.

If the filename does not begin with a 14-digit timestamp prefix, Signal 5 is not evaluated for that post.

---

### Question 2 — Ambiguity resolution workflow in the report

**Decision: purely descriptive. Surface raw evidence. No suggested resolution path.**

When a match is ambiguous, the report records all candidate paths, the signals that produced each candidate, the SHA-256 of each candidate, image dimensions of each candidate, and file sizes. The operator has the raw data.

Rationale:
- Adding suggested resolution steps encodes assumptions about what is correct.
- The report cannot know whether the operator has external evidence (original hard drive, cloud backup, Wayback Machine captures) that changes the resolution.
- Archaeology principle: record evidence, not verdicts.

**What the ambiguous block does include:**
- All candidate paths
- SHA-256 for each candidate
- Image dimensions for each candidate
- File size for each candidate
- Modification timestamp for each candidate
- The signals that matched each candidate

The operator uses this to decide. The report does not.

---

### Question 3 — Thumbnail orphan classification

**Decision: classified separately in the report, same `OrphanArtifact` structure.**

A thumbnail orphan and an image orphan carry different archaeological meaning:

- An orphaned **image** suggests a post or XML record may be missing entirely.
- An orphaned **thumbnail** suggests the primary image was found (or never cataloged), but the thumbnail survived independently. Thumbnails without a primary image may indicate partial archive recovery.

Both are reported using the same `OrphanArtifact` dataclass. The `artifact_type` field (`jpeg` vs `thumbnail`) already distinguishes them. The report's orphan section presents them in two subsections: **Orphan Images** and **Orphan Thumbnails**, not merged.

**Counts are also tracked separately in `MediaMatchSummary`:** `orphan_images` and `orphan_thumbnails` remain distinct fields.

---

### Question 4 — Multiple img src per post

**Decision: extract all, flag if multiple distinct filenames, treat as ambiguous if they diverge.**

Some posts embed multiple images in `content:encoded`. The design assumed one primary image per post. This assumption cannot hold for all 731 TalkingTree posts.

**Locked rule:**

1. Extract all `<img src="...">` filenames from `ParsedPost.body`.
2. Deduplicate the extracted filenames (case-insensitive).
3. If exactly one unique filename is found: treat as Signal 2 (body_img_src) with that filename.
4. If multiple unique filenames are found:
   - Record each as a separate Signal 2 observation in `signals`.
   - Add a note to `MediaMatch.notes`: `"Multiple distinct img src filenames found in post body: [list]."`
   - If all extracted filenames converge on the same on-disk artifact (same file, different URL paths): treat as one candidate.
   - If they point to different on-disk artifacts: add all to `all_candidate_paths` and mark `confidence=ambiguous`.
5. The match record remains one `MediaMatch` per post. There is no one-to-many structure. Posts with multiple images are represented as ambiguous or notable, not as multiple match records.

---

## Additional Locked Rules

The following rules were implicit in the design but are made explicit here.

### Signal conflict handling

If Signal 1 (attachment_filename) and Signal 2 (body_img_src) identify **different** filenames for the same post:

- Record both as candidates.
- Set `confidence = ambiguous`.
- Add note: `"attachment_url and body img src disagree on filename: [filename-1] vs [filename-2]."`
- Do not choose. Do not attempt to resolve. Record the disagreement.

### Thumbnail matching scope

Signal 4 (thumbnail_rule) is applied only when:

- The primary image match has `confidence in {exact, high, probable}` (not ambiguous, not unmatched)
- The predicted thumbnail filename (`"thumb_" + matched_filename`) exists in the inventory

If multiple thumbnail candidates exist with the same predicted filename (e.g., same name in different directories), treat the same ambiguity rule as applies to primary images: record all, do not choose, set `thumbnail_artifact_path = None`.

### Case sensitivity

All filename comparisons are case-insensitive. Filesystem case behavior varies; the data may have mixed-case artifacts from different operating systems. Normalizing to lowercase for comparison prevents false non-matches.

### Empty body handling

If `ParsedPost.body` is empty or contains no `<img>` tags, Signal 2 produces zero candidates. This is not a warning. It is recorded as a signal absence. The match proceeds on remaining signals.

### Attachment records with no matching post

Some attachment items in the XML may have a `post_parent` that references no known post ID (deleted post, export artifact). These attachment records are noted in `MediaMatchSummary.warnings`. They are not matched to any post. They do not generate orphan records — they are XML orphans, not media orphans.

---

## Locked Data Structures

The structures below supersede any inconsistency with the design document.

### `MatchSignal`

```
MatchSignal:
  signal_type: str     # attachment_filename | body_img_src | post_parent |
                       # thumbnail_rule | timestamp_correlation | url_domain | hash_identity
  matched_value: str   # the value that triggered this signal (filename, timestamp, post_id, etc.)
  strength: str        # primary | corroborating | derived | tiebreaker
  notes: str           # empty string if no anomaly; explanation if anomaly present
```

### `MediaMatch`

```
MediaMatch:
  post_legacy_id: str               # wp:post_id
  post_slug: str                    # wp:post_name
  post_date: str                    # wp:post_date
  attachment_legacy_id: str | None  # wp:post_id of linked attachment item; None if no attachment
  matched_artifact_path: str | None # absolute path; None when confidence is ambiguous or unmatched
  thumbnail_artifact_path: str | None
  confidence: str                   # exact | high | probable | ambiguous | unmatched
  signals: list[MatchSignal]        # all signals evaluated, strongest first
  candidate_count: int
  all_candidate_paths: list[str]    # all paths considered; includes winner if resolved
  notes: list[str]
```

### `OrphanArtifact`

```
OrphanArtifact:
  artifact_path: str
  filename: str
  artifact_type: str     # jpeg | thumbnail
  sha256: str
  file_size: int | None
  image_width: int | None
  image_height: int | None
  reason: str            # no_xml_reference | ambiguity_unresolved
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
  xml_source_files: list[str]
  media_source_dirs: list[str]
  matches: list[MediaMatch]       # sorted by post_date ascending
  orphan_media: list[OrphanArtifact]
  summary: MediaMatchSummary
  status: str                     # completed | completed_with_warnings | failed
```

---

## Locked Confidence Criteria

| Confidence | Value | Criteria |
| --- | --- | --- |
| Exact | `exact` | Signal 1 fires. Signal 2 fires. Both agree on same artifact. Signal 3 (post_parent) confirmed. Single candidate. |
| High | `high` | Signal 1 OR Signal 2 fires (not both required). At least one corroborating signal (Signal 3, 5, or 6) confirmed and consistent. Single candidate. No contradictions. |
| Probable | `probable` | Signal 1 OR Signal 2 fires. Single candidate. No corroboration available. No contradictions. |
| Ambiguous | `ambiguous` | Multiple distinct candidates for the same post. OR Signal 1 and Signal 2 disagree on filename. OR multiple distinct img src filenames map to different artifacts. Do not choose. |
| Unmatched | `unmatched` | No candidate found via any signal. |

---

## Locked Report Structure

### `media-match-report.md` sections (in order)

1. Summary table — confidence counts, thumbnail count, orphan counts
2. Match table — one row per post, sorted by post_date ascending
   - Columns: `post_id` | `post_date` | `slug` | `confidence` | `matched_file` | `thumbnail` | `signals` | `candidates`
3. Ambiguous Matches — one expanded block per ambiguous post with full candidate metadata
4. Unmatched Posts — table with any partial signal evidence available
5. Orphan Images — table: path, filename, size, dimensions, SHA-256, reason
6. Orphan Thumbnails — table: path, filename, size, dimensions, SHA-256, reason
7. Warnings — parser and match warnings

### `media-match-report.json`

Serialized `MediaMatchResult`. All fields present. Arrays empty `[]` when no entries. No fields omitted.

---

## Locked CLI Interface

```
markii match-media \
  --xml <file-or-dir> [--xml <file-or-dir> ...] \
  --media <dir> [--media <dir> ...] \
  --output <dir>
```

Exit codes:
- `0` — completed, all matches at `probable` or better, no orphans
- `2` — completed with warnings — ambiguous, unmatched, or orphan artifacts present
- `1` — failed — parse or inventory error prevented execution

---

## Locked Implementation File List

| File | Action | Scope |
| --- | --- | --- |
| `markii/importers/pixelpost_xml.py` | Modify | Add `post_parent: str` to `ParsedAttachment`; update `_parse_attachment()` to extract `wp:post_parent`; default to `""` if absent |
| `markii/media/matcher.py` | Create | Matching algorithm producing `MediaMatchResult` |
| `markii/reports/media_match.py` | Create | Report writer for `.md` and `.json` |
| `markii/cli/main.py` | Modify | Add `match-media` command |
| `tests/fixtures/media-match/` | Create | XML and JPEG fixtures covering: exact match, high confidence, probable, ambiguous (two candidates), unmatched post, orphan image, orphan thumbnail |
| `tests/test_media_match.py` | Create | Tests for each confidence level; orphan detection; multi-candidate handling; empty body handling |

No other files are in scope for this step.

---

## Scope Boundary (Unchanged)

In scope:
- Linking posts to on-disk images via XML-derived signals
- Confidence classification
- Orphan artifact recording
- Report generation

Out of scope for this step:
- Writing match records to SQLite archive
- Phase IV database reconstruction
- Cross-archive deduplication
- Non-image media matching

---

## Authorization Condition

Implementation may begin when Nathan Arizona confirms this review.

The signal definitions, confidence criteria, orphan taxonomy, open question resolutions, and implementation file list above are locked pending that confirmation.

No code may be written before confirmation is received.
