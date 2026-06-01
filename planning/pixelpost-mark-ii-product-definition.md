# PixelPost Mark II Product Definition

Phase: Product Definition

Status: archaeology paused. This document does not add new Wayback, award, or provenance research.

## Product Statement

PixelPost Mark II is a modern, independent photoblog platform inspired by the verified behavior of Pixelpost 1.7.3.

It is designed for photographers who want an owned, chronological, image-first publication system: one photograph, one page, one archive, under their own domain.

PixelPost Mark II is not a general CMS, social network, creator platform, or engagement engine.

## Product Doctrine

PixelPost Mark II should preserve the feeling of:

- a durable camera body
- a field notebook
- an independent image archive
- a quiet publishing ritual

It should avoid:

- algorithmic feeds
- follower mechanics
- like counts as primary UI
- engagement dashboards
- heavy page-builder workflows
- framework-showcase complexity

## Essential PixelPost Features

| Feature | Product Requirement |
| --- | --- |
| Image-first posts | A photograph remains the primary publication unit. |
| Chronological homepage | The home page centers the latest eligible image, not a feed of cards. |
| Previous/next navigation | Every image page supports chronological navigation. |
| Browse/archive pages | Visitors can scan the archive by thumbnail grid, month, category, and tag. |
| Editable captions | Each photograph has title/headline, caption/body, publication date, and optional metadata. |
| Categories and tags | Categories and tags organize a personal archive rather than drive engagement. |
| EXIF | Camera metadata is preserved and displayable. |
| Comments | Per-image comments are supported, importable, moderatable, and optional. |
| Feeds | RSS/Atom should remain first-class independent-web outputs. |
| Owned files | Original images, derived images, metadata, comments, and exports are portable. |
| Themes/templates | Site presentation is owner-controlled and not locked into a hosted platform. |
| Calm admin workflow | Upload, caption, categorize, schedule, publish. Nothing else should get in the way. |

## Features That Should Remain Unchanged In Spirit

- Photograph as the center of the site.
- Latest image as the default public experience.
- Chronological archive as narrative structure.
- One-image-per-page viewing rhythm.
- Categories, tags, and dates as archive tools.
- EXIF as photographic context.
- Optional comments attached to the photograph.
- Template-level control over visual identity.
- Lightweight deployment and long-term portability.

These should be modernized technically, but not replaced conceptually.

## Features To Modernize

| Area | Modernization Direction |
| --- | --- |
| Runtime | Use supported PHP or another conservative server runtime; avoid legacy MySQL/PHP assumptions. |
| Database | Use a normalized schema with migrations and exportable data. |
| Authentication | Modern password hashing, session security, CSRF protection, recovery flows. |
| Upload security | Validate MIME/type/content, strip unsafe payloads, scan dimensions, isolate processing. |
| Image processing | Generate responsive derivatives, preserve originals, track checksums. |
| EXIF | Store raw EXIF plus normalized display fields; preserve privacy controls. |
| Templates | Provide editable, versioned themes with safe rendering boundaries. |
| Mobile UI | Make publishing and browsing work naturally on phones. |
| Accessibility | Semantic HTML, alt text, keyboard navigation, contrast, responsive typography. |
| Import/export | Build importer pipelines for PixelPost XML, WordPress WXR, and reconstructed datasets. |
| Backups | First-class database/media export, checksums, and restore documentation. |

## Features To Remove Or Avoid

- Legacy PHP compatibility shims in the product runtime.
- `mysql_*` database APIs.
- Unsafe direct filesystem assumptions.
- Public installer left accessible after setup.
- Unbounded upload trust.
- Plain or weak password storage.
- Template execution that allows arbitrary server-side code.
- Built-in social metrics as the main feedback loop.
- Required cloud services.
- Multi-tenant SaaS assumptions.
- Page builder complexity.

## Modern Mobile-Friendly Experience

### Home Page

Purpose: present the latest eligible photograph as the site's front door.

Required behavior:

- full-width image presentation with caption and date close at hand
- previous/next navigation
- visible archive/browse access
- restrained metadata display
- fast loading through responsive image sizes
- no infinite scroll requirement

### Image Page

Purpose: durable canonical page for one photograph.

Required behavior:

- image, title, date, caption/body
- categories and tags
- EXIF panel, collapsed or compact by default on mobile
- comments, if enabled
- previous/next links
- original/large image access when allowed
- canonical permalink

### Browse Page

Purpose: scan the archive.

Required behavior:

- responsive thumbnail grid
- sort newest/oldest
- filters for category, tag, year/month
- visible counts where useful
- no layout shift from image loading

### Archive Page

Purpose: preserve chronology.

Required behavior:

- year/month hierarchy
- post counts
- compact thumbnail previews
- stable URLs for months and years
- support imported historical chronology exactly

### Search

Purpose: find titles, captions, tags, categories, locations, and comments where allowed.

Required behavior:

- search titles and captions by default
- optional comment search
- filter by date/category/tag
- return image-centered results

### Categories

Purpose: broad bodies of work.

Required behavior:

- category landing pages
- title/description
- thumbnail grid
- feed output
- import-safe slug preservation

### Tags

Purpose: flexible subjects, locations, cameras, moods, materials.

Required behavior:

- tag landing pages
- tag cloud/list view
- per-tag feed
- import-safe normalization without losing original text

## Metadata Architecture

### Post Model

The post is the public photoblog entry.

Core fields:

- `id`
- `title`
- `slug`
- `caption`
- `body`
- `published_at`
- `created_at`
- `updated_at`
- `status`
- `visibility`
- `canonical_source`
- `legacy_source_id`
- `legacy_permalink`

Relationships:

- one primary image
- many categories
- many tags
- many comments
- one optional EXIF record through image

### Image Model

The image model preserves the media artifact.

Core fields:

- `id`
- `post_id`
- `original_filename`
- `storage_filename`
- `mime_type`
- `width`
- `height`
- `filesize`
- `sha256`
- `storage_path`
- `alt_text`
- `caption`
- `captured_at`
- `created_at`

Relationships:

- one post
- many derivatives
- one EXIF record

### Image Derivative Model

Core fields:

- `id`
- `image_id`
- `kind`
- `width`
- `height`
- `format`
- `filesize`
- `sha256`
- `storage_path`

Required derivative kinds:

- thumbnail
- small
- medium
- large
- original-preserved

### EXIF Model

Core fields:

- `id`
- `image_id`
- `raw_exif_json`
- `camera_make`
- `camera_model`
- `lens`
- `focal_length`
- `aperture`
- `shutter_speed`
- `iso`
- `flash`
- `captured_at`
- `gps_latitude`
- `gps_longitude`
- `gps_visibility`

Requirement: Mark II must preserve raw EXIF where available and allow privacy-aware display of GPS data.

### Comment Model

Core fields:

- `id`
- `post_id`
- `author_name`
- `author_email_hash`
- `author_url`
- `body`
- `status`
- `created_at`
- `legacy_source_id`
- `legacy_author_email`
- `legacy_author_ip`

Comment status:

- approved
- pending
- spam
- trash
- imported

### Category Model

Core fields:

- `id`
- `name`
- `slug`
- `description`
- `sort_order`
- `legacy_source_id`

### Tag Model

Core fields:

- `id`
- `name`
- `slug`
- `legacy_source_id`

## Import Pipeline

### PixelPost XML Import

Purpose: import WXR-style exports generated from PixelPost content.

Required steps:

1. Parse posts, attachments, categories, tags, comments.
2. Match image filenames in content bodies and attachment records.
3. Preserve original slugs, dates, titles, captions, and comments.
4. Link JPEGs and thumbnails by filename.
5. Produce an import report with counts, warnings, missing files, duplicate filenames, and orphan media.

### WordPress WXR Import

Purpose: import later WordPress migrations while preserving original PixelPost-era chronology.

Required steps:

1. Parse WordPress posts, pages, attachments, comments, categories, tags.
2. Detect PixelPost-origin posts by URL, filename, date, and content pattern.
3. Preserve WordPress-only pages as optional static pages.
4. Avoid overwriting stronger PixelPost-export evidence without an explicit conflict rule.

### TalkingTree Reconstruction Import

Purpose: reconstruct TalkingTree from surviving exports, JPEGs, thumbnails, comments, and public corroboration.

Required steps:

1. Load the nine PixelPost export XML files.
2. Link 731 posts to 731 JPEG references.
3. Link matching thumbnails.
4. Import 887 comments with preserved author/date/content/status.
5. Import 18 categories and 441 tags.
6. Preserve public date range from 2006-10-16 through 2011-06-23.
7. Flag three extra JPEGs as unresolved candidates.
8. Mark EXIF as absent from XML unless extracted from surviving JPEG files in a later approved content import pass.

### Future Export Formats

Mark II should export:

- full site archive: JSON manifest + media files + SQL or SQLite dump
- WXR-compatible export for interoperability
- static HTML archive
- per-post JSON
- CSV index for preservation review
- checksums for all original and derivative images

## Final Questions

### What is PixelPost Mark II?

PixelPost Mark II is an independent, image-first photoblog platform for owned chronological photo publishing, restoration import, and long-term archive portability.

### What makes it different from WordPress?

WordPress starts from generalized posts and pages. PixelPost Mark II starts from the photograph, the image page, the archive, and the photographer's publishing rhythm.

### What makes it different from Instagram?

Instagram is a social feed controlled by a platform. PixelPost Mark II is an owned archive controlled by the photographer, with portable files, durable URLs, RSS, and no engagement-engine center of gravity.

### What is the shortest path to a working prototype?

Build a small Mark II core that can import the TalkingTree reconstruction dataset, render home/image/browse/archive pages, preserve comments/categories/tags, and publish a static or server-rendered photoblog from owned files.
