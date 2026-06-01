# Prototype Architecture

Phase: PixelPost Archaeology Phase 11 - Prototype Architecture

Status: design only. No application code, deployment, containers, or prototype build are introduced by this document.

## Guiding Principle

```text
PixelPost Mark II
  -> TalkingTree
  -> Someone Else's Photoblog
  -> A New Photoblog Created Tomorrow
```

TalkingTree is a validation fixture. It is not the product boundary.

## Product Boundary

PixelPost Mark II is a small image-first photoblog engine with import/export discipline.

The core platform should know about:

- photographs
- posts
- chronology
- captions
- comments
- categories
- tags
- EXIF
- media files
- provenance
- exports

The core platform should not know hardcoded facts about:

- TalkingTree directory names
- TalkingTree post counts
- TalkingTree categories
- one user's migration history
- one historical theme

Those belong in import profiles and validation fixtures.

## Smallest Technical Shape

The smallest useful MVP has four layers:

1. Storage layer
2. Import layer
3. Rendering layer
4. Export layer

```text
source artifacts
  -> import profile
  -> normalized Mark II archive
  -> rendered photoblog
  -> portable export
```

## Recommended MVP Architecture

| Layer | MVP Choice | Reason |
| --- | --- | --- |
| Database | SQLite | Small, portable, enough for an owned photoblog and import fixture. |
| Media storage | Filesystem | Matches PixelPost spirit; easy backup and checksum verification. |
| Import execution | Command-line import jobs | Keeps MVP focused on correctness before admin UI. |
| Rendering | Static generation first | Produces durable pages, simple hosting, easy verification. |
| Export | Manifest + media + SQLite dump | Lets user leave with complete archive. |

## Why SQLite First

SQLite is the right prototype database because:

- the archive is owned by one site
- deployment is simple
- backups are simple
- the database file can travel with the media
- import tests can be repeated easily
- the MVP does not need multi-tenant scaling

PostgreSQL can be supported later if Mark II grows into heavier deployments. MySQL compatibility may matter for historical migration tooling, but it should not drive the new core.

## Core Modules

### Archive Core

Owns normalized data models:

- post
- image
- image derivative
- EXIF
- comment
- category
- tag
- provenance event
- import run

### Import Core

Defines common importer contracts:

- read source
- normalize records
- match media
- resolve conflicts
- write records
- produce report

Import profiles plug into this layer.

### Render Core

Reads normalized Mark II archive data and emits:

- home page
- image page
- browse page
- archive page
- category page
- tag page
- feed files

### Export Core

Exports:

- JSON manifest
- SQLite database
- original media
- derived media
- checksums
- import reports
- optional static site bundle

## MVP Non-Goals

- web-based installer
- web-based admin upload
- user registration
- social following
- plugin marketplace
- headless CMS API
- real-time image processing service
- multi-site hosting
- theme editor
- comments submission

These can come later only after the import/render/export spine is proven.

## Final Architecture Answer

The smallest architecture capable of importing TalkingTree and rendering a complete photoblog is:

```text
SQLite + filesystem media + import profiles + static renderer + portable export manifest
```

This is general enough for TalkingTree, another historical PixelPost photoblog, and a new photoblog created tomorrow.
