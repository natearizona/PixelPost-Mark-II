# MVP Build Order

Phase: PixelPost Archaeology Phase 11 - Prototype Architecture

Status: design only.

## Build Principle

Build the spine before the creature:

```text
storage -> import -> render -> export
```

Do not start with admin UI, theming complexity, or deployment polish.

## Dependency-Ordered Sequence

### Step 1: Schema Definition

Define SQLite schema for:

- posts
- images
- image derivatives
- EXIF records
- comments
- categories
- tags
- provenance
- import runs
- source artifacts

Exit criteria:

- schema can represent TalkingTree and a new photoblog post

### Step 2: Media Inventory

Design/import media inventory:

- walk source media directories
- compute SHA-256
- capture dimensions
- index filenames
- detect duplicates

Exit criteria:

- image and thumbnail files can be identified without copying source artifacts

### Step 3: PixelPost XML Import

Import:

- posts
- attachments
- categories
- tags
- comments
- image references

Exit criteria:

- PixelPost XML maps into normalized staging records

### Step 4: Media Matching

Match:

- post image reference to original image
- thumbnail to original image
- attachment record to post

Exit criteria:

- import report shows matched, missing, duplicate, and orphan media

### Step 5: Archive Write

Write normalized records into SQLite.

Exit criteria:

- 731-post TalkingTree fixture can be represented
- a minimal new-photoblog fixture can also be represented

### Step 6: Static Renderer

Generate:

- home page
- image page
- browse page
- archive page
- category page
- tag page

Exit criteria:

- complete browsable photoblog exists on disk

### Step 7: Comment Rendering

Display imported comments per image page.

Exit criteria:

- imported comments appear on correct posts

### Step 8: Export Manifest

Generate:

- `manifest.json`
- `checksums.sha256`
- media inventory
- import report references

Exit criteria:

- user can inspect what was imported and what files belong to the archive

### Step 9: Verification Fixture

Verify:

- expected counts
- sample page titles
- sample image filenames
- archive date range
- category/tag counts
- comment counts

Exit criteria:

- prototype can demonstrate TalkingTree reconstruction without special core logic

## Milestones

### Milestone A: Normalized Archive

Smallest demonstrable result:

- SQLite archive exists
- source artifacts are inventoried
- posts/images/comments/categories/tags are imported
- import report exists

This proves the data model.

### Milestone B: Browsable Photoblog

Smallest demonstrable result:

- static home page
- static image pages
- browse grid
- archive pages
- category/tag pages
- comments display

This proves PixelPost Mark II can render a complete photoblog.

### Milestone C: Portable Archive

Smallest demonstrable result:

- export manifest
- checksums
- SQLite copy
- media bundle
- rendered static site

This proves the user can leave with the archive intact.

## Smallest Possible Demonstrable Prototype

The smallest prototype worth building is:

```text
PixelPost XML import + media matching + static render + export manifest
```

It does not need:

- admin login
- live upload
- comment form
- search
- theme editor
- Docker deployment

## Choices To Avoid Before MVP Is Proven

- React SPA
- Laravel-scale full CMS rewrite
- multi-tenant architecture
- public hosted service
- plugin system
- generalized page builder
- live comment submission
- automatic modernization of historical content
- background job system
- external search service
- object storage requirement

## Decisions That Create Unnecessary Complexity

- choosing PostgreSQL before SQLite is proven
- building admin UI before import correctness
- building live uploads before historical rendering
- treating TalkingTree as hardcoded product logic
- requiring containers for local prototype use
- supporting every WordPress feature during MVP
- implementing full-text search before archive pages exist
- implementing multiple themes before one good default exists

## Prototype Difficulty

Estimated difficulty:

```text
Moderate
```

Reason:

- storage and static rendering are straightforward
- the hard part is import correctness, provenance, media matching, and not overbuilding

## Final Questions

### What is the smallest architecture capable of importing TalkingTree and rendering a complete photoblog?

SQLite, filesystem media, profile-based importer, static renderer, and portable export manifest.

### What architectural choices should be avoided before the MVP is proven?

Avoid full CMS architecture, social features, live admin complexity, cloud assumptions, object storage requirements, and hardcoded TalkingTree logic.

### What technical decisions would create unnecessary complexity?

Choosing a large framework or multi-service deployment before the data model, importer, renderer, and export loop are proven would create unnecessary complexity.
