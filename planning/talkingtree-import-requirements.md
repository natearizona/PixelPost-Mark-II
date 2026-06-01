# TalkingTree Import Requirements

Phase: Product Definition

Status: design only. No import is performed by this document.

## Import Objective

Reconstruct the TalkingTree photoblog content layer inside PixelPost Mark II from surviving exports and media, while preserving chronology, captions, comments, categories, tags, image relationships, and provenance.

## Source Inputs

Primary inputs:

- nine PixelPost export XML files from 2011-06-25
- surviving JPEG image directory
- surviving thumbnail directory
- WordPress WXR exports from 2012 for comparison and fallback

Known recovered content:

- 731 PixelPost-era post records
- 731 attachment records
- 731 matched JPEG references
- 731 matched thumbnails
- 887 comments
- 18 categories
- 441 tags
- date range 2006-10-16 through 2011-06-23
- three extra JPEGs not yet tied to XML records

## Import Rules

### Preservation Rules

- Never modify source artifacts.
- Treat imported records as derived reconstruction.
- Preserve original filenames.
- Preserve source file path in import provenance.
- Preserve hashes for every source media file.
- Keep raw source excerpts or source line references in import logs where practical.
- Mark unresolved files instead of guessing silently.

### Chronology Rules

- Use PixelPost XML `wp:post_date` as the primary post date.
- Preserve `pubDate` and `wp:post_date_gmt` as secondary source fields.
- Do not reorder posts based on filesystem modification time.
- Preserve future/past semantics if present.
- Generate archive URLs from preserved dates unless a legacy permalink exists.

### Image Relationship Rules

- Match post-to-image by filename found in `content:encoded`.
- Confirm against attachment record and enclosure URL when available.
- Match thumbnails by `thumb_` prefix and original filename.
- Store unresolved images as media candidates, not posts.
- Store orphan attachment records as warnings.

### Comment Rules

- Preserve comment author name.
- Preserve author URL.
- Preserve author email only in protected import metadata or hashed form.
- Preserve comment date and approval status.
- Preserve comment body exactly enough for display, with safe rendering.
- Preserve original comment IDs as legacy IDs.
- Do not infer missing threading unless parent IDs exist.

### Category Rules

- Preserve category names and slugs.
- Preserve all category assignments.
- Preserve empty categories if they appear in source definitions.
- Avoid merging categories unless exact normalized slug matches.

### Tag Rules

- Preserve tag names and slugs.
- Preserve all tag assignments.
- Keep original capitalization as display text where possible.

### EXIF Rules

- The PixelPost XML exports do not contain structured EXIF.
- Mark imported XML EXIF status as `absent_from_export`.
- A later approved import pass may extract EXIF from surviving JPEGs.
- If JPEG EXIF extraction is performed, record it as reconstructed-from-image, not original PixelPost database EXIF.
- GPS data must default to private until reviewed.

## Required Import Report

Every TalkingTree import run must produce:

- source artifact list
- source hashes
- import timestamp
- importer version
- post count
- image count
- thumbnail count
- category count
- tag count
- comment count
- unresolved media count
- duplicate filename count
- missing image count
- missing thumbnail count
- EXIF extraction status
- warnings and errors

## Required Data Fields

### Post

- title
- slug
- caption/body
- publication date
- source XML file
- source legacy ID
- source permalink or generated legacy URL
- status

### Image

- original filename
- storage filename
- source path
- source hash
- width
- height
- file size
- matched thumbnail path
- matched thumbnail hash

### Comment

- legacy ID
- post legacy ID
- author name
- author URL
- author email hash
- comment body
- created date
- approval status

### Provenance

- source file path
- source artifact hash
- imported field name
- original source value
- normalization rule used
- conflict decision if any

## Conflict Rules

| Conflict | Resolution |
| --- | --- |
| PixelPost XML vs WordPress WXR title mismatch | Prefer PixelPost XML for PixelPost-era posts; log WordPress value. |
| PixelPost XML vs WordPress WXR date mismatch | Prefer PixelPost XML; log mismatch. |
| Missing image but present attachment | Create unresolved media warning. |
| Image present but no XML post | Create orphan media candidate. |
| Duplicate slug | Preserve legacy slug and append stable Mark II suffix only if required for routing. |
| Duplicate filename | Preserve both records with hash-based disambiguation. |

## Acceptance Criteria

The import is acceptable when:

- all 731 XML post records import
- all 731 matched JPEGs link to posts
- all 731 matched thumbnails link to images
- all 887 comments attach to intended posts
- all 18 categories exist
- all 441 tags exist
- archive chronology matches the recovered XML
- unresolved files are reported, not hidden
- import can be repeated from scratch with the same result

## Open Issues

- Original PixelPost SQL is absent.
- Original PixelPost template is absent.
- Original addon directory is absent.
- Structured original PixelPost EXIF table data is absent.
- Three JPEGs remain unresolved candidates.

## Product Implication

TalkingTree import should be treated as the first serious Mark II fixture. It represents a real historical photoblog with enough surviving data to test the product against preservation requirements from day one.
