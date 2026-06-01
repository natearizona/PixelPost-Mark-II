# Decision Log

Phase: Architecture

Status: archaeology complete enough for MVP planning. Architecture only.

## Governing Principle

```text
PixelPost Mark II
  -> TalkingTree
  -> Someone Else's Historical Photoblog
  -> A New Photoblog Created Tomorrow
```

TalkingTree is the validation fixture. It is not the product.

## Decision 1: MVP Database

Decision:

```text
Use SQLite for the MVP.
```

Rationale:

- simplest database that can preserve a complete photoblog
- portable as a single file
- easy to back up, export, inspect, and restore
- avoids server dependency before the product spine is proven
- fits owned single-site publishing
- supports TalkingTree import scale comfortably

Rejected for MVP:

- PostgreSQL: good later, unnecessary operational weight now
- MySQL/MariaDB: useful for legacy import compatibility, not ideal as the new core dependency

Long-term note:

The schema should not depend on SQLite-only tricks. A later PostgreSQL adapter should remain possible.

## Decision 2: Media Storage

Decision:

```text
Use filesystem media storage.
```

Recommended layout:

```text
media/
  originals/
  derivatives/
    thumbnail/
    small/
    medium/
    large/
```

Rationale:

- matches PixelPost's owned-file spirit
- simple to inspect
- simple to export
- compatible with static rendering
- avoids object storage assumptions

## Decision 3: Checksums

Decision:

```text
Use SHA-256 for source artifacts, originals, derivatives, manifests, and exports.
```

Rationale:

- preservation-grade enough for MVP
- widely supported
- easy to verify outside Mark II

## Decision 4: Provenance

Decision:

```text
Store source artifacts, import runs, and field/entity provenance in SQLite.
```

MVP provenance must record:

- source artifact path
- source artifact SHA-256
- import profile
- source locator
- normalized entity
- conflict decision
- import report reference

Rationale:

- historical imports must be explainable
- new photoblogs also benefit from export traceability
- provenance should be product infrastructure, not TalkingTree-specific notes

## Decision 5: Rendering Model

Decision:

```text
Use static site generation for the MVP.
```

Rationale:

- smallest public runtime surface
- easiest to verify
- simplest hosting
- durable output
- naturally supports export
- preserves PixelPost's page-centered rhythm

Rejected for MVP:

- server-rendered application: useful later for admin, comments, and search
- hybrid approach: unnecessary before static import/render/export is proven

## Decision 6: Canonical URL Structure

Decision:

```text
/YYYY/MM/slug/
```

Required routes:

```text
/
/browse/
/browse/page/2/
/archive/
/archive/YYYY/
/archive/YYYY/MM/
/category/<slug>/
/category/<slug>/page/2/
/tag/<slug>/
/tag/<slug>/page/2/
/YYYY/MM/<slug>/
```

Rationale:

- preserves chronology
- works for historical imports and new posts
- durable and readable
- avoids recreating every legacy query string in the core

Legacy URLs should be stored and optionally exported as redirects.

## Decision 7: Import Architecture

Decision:

```text
Use profile-based importers.
```

Core import pipeline:

```text
discover sources
  -> parse
  -> normalize
  -> match media
  -> resolve conflicts
  -> write archive
  -> record provenance
  -> report
```

Initial profiles:

- PixelPost XML
- WordPress WXR
- TalkingTree reconstruction

Rule:

TalkingTree-specific behavior must live in the TalkingTree profile. It must not leak into the core schema or renderer.

## Decision 8: Export Architecture

Decision:

```text
Export complete archive bundle: JSON manifest + SQLite + media + checksums + provenance + rendered site.
```

Minimum export:

```text
manifest.json
archive.sqlite
checksums.sha256
media/originals/
media/derivatives/
provenance/
reports/
rendered/
```

Rationale:

- user can leave Mark II with the whole archive
- export is inspectable without Mark II
- preserves data, media, metadata, comments, provenance, and rendered pages

## Decision 9: MVP Milestones

### Milestone A: Normalized Archive

Demonstrates:

- SQLite schema
- media inventory
- PixelPost XML import
- normalized posts/images/comments/categories/tags
- import report

### Milestone B: Browsable Photoblog

Demonstrates:

- home page
- image pages
- browse page
- archive pages
- category pages
- tag pages
- imported comments display

### Milestone C: Portable Archive

Demonstrates:

- JSON manifest
- checksums
- SQLite export
- media bundle
- rendered static site
- provenance/report bundle

## Complexity Audit

### Avoid: React-First Architecture

Reason:

- the MVP is archive rendering, not a client application
- static HTML is easier to preserve and export
- React can be introduced later for admin UI if needed

### Avoid: Headless CMS Pattern

Reason:

- Mark II is not a generic content backend
- image-first archive behavior should remain native
- headless architecture adds API and frontend complexity before the model is proven

### Avoid: Laravel-Scale Complexity

Reason:

- full framework scaffolding may bury the core preservation model
- MVP needs import/render/export spine first
- a smaller PHP stack can be considered later if live admin becomes the next phase

### Avoid: SaaS Assumptions

Reason:

- PixelPost spirit is independent ownership
- multi-tenant billing, accounts, cloud storage, and hosted identity are not MVP concerns

### Avoid: Cloud Dependencies

Reason:

- historical archives should be reproducible locally
- object storage and managed databases complicate preservation and export

### Avoid: Premature Features

Do not build before MVP proof:

- live upload admin
- comment submission
- theme editor
- plugin system
- search server
- analytics
- social graph
- public installer
- multi-user roles
- image AI features

## Greatest Long-Term Risks

| Risk | Why It Matters | Mitigation |
| --- | --- | --- |
| Hardcoding TalkingTree | Turns Mark II into a one-site reconstruction tool | Keep TalkingTree in importer/profile/fixture only. |
| Overbuilding CMS features | Delays proof of photoblog spine | Build storage/import/render/export first. |
| Weak provenance | Undermines historical trust | Store source artifacts, checksums, import runs, and decisions. |
| Poor export model | Recreates platform lock-in | Make export a first-class MVP feature. |
| URL instability | Breaks archive value | Use durable canonical URLs and legacy redirect maps. |
| Cloud dependency | Reduces independence and reproducibility | Keep MVP local-file and SQLite based. |

## Final Conclusions

### Smallest Architecture

```text
SQLite + filesystem media + profile importers + static renderer + complete export bundle
```

### Architecture That Best Preserves PixelPost's Spirit

An owned, file-backed, chronological image archive with static public pages and portable exports.

### Highest-Risk Architectural Decisions

- React-first public frontend
- headless CMS abstraction
- hardcoded TalkingTree logic
- SaaS or cloud-first deployment
- postponing export/provenance until later

### Prototype Difficulty

```text
Moderate
```

The rendering is straightforward. The meaningful difficulty is import correctness, provenance, media matching, and keeping the architecture small.
