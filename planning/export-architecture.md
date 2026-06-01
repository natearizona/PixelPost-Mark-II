# Export Architecture

Phase: PixelPost Archaeology Phase 11 - Prototype Architecture

Status: design only.

## Export Question

How can a user leave Mark II with their entire archive intact?

Answer:

Every Mark II site should export as a complete portable archive containing database, media, checksums, provenance, rendered pages, and a JSON manifest.

## Export Principle

No lock-in.

PixelPost Mark II should treat export as a core product feature, not an emergency backup afterthought.

## Export Package Layout

Recommended layout:

```text
pixelpost-mark-ii-export-YYYYMMDD/
  manifest.json
  archive.sqlite
  checksums.sha256
  media/
    originals/
    derivatives/
  reports/
    import-runs/
    export-report.json
  rendered/
    index.html
    archive/
    category/
    tag/
    YYYY/
  provenance/
    source-artifacts.json
    provenance-events.json
  README.txt
```

## JSON Manifest Export

`manifest.json` should include:

- export format version
- site title
- generated timestamp
- software version
- post count
- image count
- derivative count
- category count
- tag count
- comment count
- source artifact count
- file inventory
- checksum references

Per-post manifest entries:

- ID
- title
- slug
- published date
- canonical URL
- legacy URL
- image reference
- category references
- tag references
- comment count
- provenance reference

## Media Export

Media export must include:

- original images
- imported thumbnails
- generated derivatives
- unresolved/orphan media candidates when requested

Export must preserve:

- original filenames
- storage filenames
- checksums
- dimensions
- MIME type

## Checksum Export

`checksums.sha256` should include:

- database file
- manifest file
- every original image
- every derivative image
- every import report
- every provenance file

Checksums should also be represented in machine-readable JSON.

## Restoration Export

The export should allow reconstruction of a Mark II site without the original application database server.

Minimum restoration contents:

- SQLite database
- media files
- manifest
- checksums
- provenance records
- import reports

Optional restoration contents:

- rendered static site
- redirect map
- theme files
- source artifact copies if user explicitly includes them

## Static Site Export

Static export should include:

- home page
- image pages
- browse pages
- archive pages
- category pages
- tag pages
- feed files when implemented

This lets a user publish or preserve the photoblog even if they stop running Mark II.

## Interoperability Export

Later formats:

- WordPress WXR
- generic JSON
- CSV index
- RSS feed archive
- IIIF-style manifest if useful for image collections

These are later features. The MVP only needs native JSON manifest plus media and SQLite.

## Provenance Export

Provenance export must preserve:

- source artifact hashes
- import run summaries
- field-level source references where available
- conflict decisions
- unresolved artifact lists

This is essential for historical imports, but also useful for new sites.

## Avoid Before MVP

- proprietary archive bundle
- export requiring cloud services
- export without original media
- export without checksums
- export that loses comments
- export that loses legacy URLs
- export that only produces rendered HTML

## Export Conclusion

A user should be able to leave Mark II with:

```text
all data + all media + all metadata + all comments + all provenance + all checksums
```

The MVP export should be boring, inspectable, and restorable.
