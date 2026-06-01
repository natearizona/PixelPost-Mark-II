# Rendering Architecture

Phase: PixelPost Archaeology Phase 11 - Prototype Architecture

Status: design only.

## Rendering Question

What rendering approach minimizes complexity while preserving PixelPost behavior?

Answer:

Use static generation for the MVP, backed by normalized Mark II archive data.

## Rendering Recommendation

### MVP

Generate static HTML pages from SQLite and filesystem media.

Why:

- simplest hosting story
- easy verification
- no public runtime security surface for imported archives
- durable URLs
- fast pages
- clear export path
- aligned with archival preservation

### Later

Add server rendering when Mark II gains:

- live admin publishing
- comment submission
- authenticated editing
- search indexes
- dynamic previews

## Required Page Types

### Home Page

URL:

```text
/
```

Behavior:

- shows latest published image by chronology
- includes title, date, caption excerpt, category/tag links
- includes previous image navigation
- links to browse and archive

### Image Page

URL pattern:

```text
/YYYY/MM/slug/
```

Behavior:

- canonical page for one photograph
- displays image, title, date, caption/body
- displays categories, tags, optional EXIF, comments
- includes previous/next links
- preserves imported legacy permalink as metadata

### Browse Page

URL pattern:

```text
/browse/
/browse/page/2/
```

Behavior:

- responsive thumbnail grid
- newest first by default
- stable pagination
- no infinite scroll for MVP

### Archive Page

URL patterns:

```text
/archive/
/archive/YYYY/
/archive/YYYY/MM/
```

Behavior:

- chronological year/month grouping
- counts per month
- optional thumbnail preview rows
- stable archive URLs

### Category Page

URL pattern:

```text
/category/<slug>/
/category/<slug>/page/2/
```

Behavior:

- thumbnail grid filtered by category
- category title and description
- feed link later

### Tag Page

URL pattern:

```text
/tag/<slug>/
/tag/<slug>/page/2/
```

Behavior:

- thumbnail grid filtered by tag
- tag title
- feed link later

## URL Structure

Preferred default:

```text
/YYYY/MM/slug/
```

Reasons:

- preserves chronology
- readable
- compatible with historical photoblog expectations
- works for imported and new posts

Legacy URL preservation:

- store original PixelPost and WordPress URLs
- optionally generate redirect map
- do not force Mark II internals to mimic every legacy query string

## Image Derivative Handling

MVP rendering should support:

- imported thumbnail if present
- generated thumbnail if imported thumbnail absent
- medium/large derivative for responsive display
- original file preserved separately

Generated HTML should use:

- `srcset`
- width/height attributes
- lazy loading for browse grids
- explicit alt text

## Pagination Approach

Use stable page-size pagination.

Recommended defaults:

- browse grid: 48 images per page
- category/tag grid: 48 images per page
- archive month page: full month unless very large, then paginate

Avoid infinite scroll in MVP because it weakens archive durability and complicates verification.

## Template Design

Use a minimal theme layer:

```text
theme/
  layout
  home
  image
  browse
  archive
  category
  tag
  partials/
```

The MVP theme should be editable, but not server-executable. Template rendering should receive structured data and output static HTML.

## Search

Search is not required for the smallest static MVP. Two acceptable early options:

- generate a static JSON search index later
- defer search to version 0.2/0.3

## Avoid Before MVP

- React SPA
- client-side routing
- infinite scroll
- dynamic image proxy
- personalized feeds
- timeline algorithms
- complex block editor
- server-rendered comments

## Rendering Conclusion

Static generation preserves PixelPost's one-image-per-page behavior while minimizing runtime complexity. It also makes export and long-term preservation easier.
