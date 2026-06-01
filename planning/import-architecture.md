# Import Architecture

Phase: PixelPost Archaeology Phase 11 - Prototype Architecture

Status: design only.

## Import Question

How should imports be structured so future import profiles can be added without changing the core platform?

Answer:

Use a common import pipeline with profile-specific readers and mappers.

```text
source artifacts
  -> profile reader
  -> normalized staging records
  -> media matcher
  -> conflict resolver
  -> archive writer
  -> provenance recorder
  -> import report
```

## Import Profiles

### PixelPost XML Importer

Purpose:

- import WXR-style exports produced from PixelPost content

Responsibilities:

- parse XML items
- detect post vs attachment
- extract title, slug, date, caption/body
- extract image filename from `content:encoded`, enclosure, attachment URL
- extract categories and tags
- extract comments
- emit normalized records

### WordPress WXR Importer

Purpose:

- import later WordPress migrations or WordPress-native photoblogs

Responsibilities:

- parse WordPress WXR 1.1/1.2 records
- handle posts, pages, attachments, comments, categories, tags
- preserve WordPress URLs where they are canonical
- support recovery mode for imperfect XML if needed
- identify PixelPost-origin material when imported as comparison data

### TalkingTree Reconstruction Importer

Purpose:

- profile-specific import using known TalkingTree artifact groups

Responsibilities:

- load nine PixelPost XML files as primary source
- match known image and thumbnail directories
- compare WordPress exports as secondary evidence
- enforce TalkingTree validation counts
- report unresolved JPEG candidates

This profile must call the same core import services as any other profile. It must not create special platform records unavailable to other sites.

## Parser Flow

1. Register source artifacts and checksums.
2. Open source file read-only.
3. Parse records into staging structures.
4. Validate required fields.
5. Normalize date, slug, status, title, caption.
6. Extract media references.
7. Extract taxonomy assignments.
8. Extract comments.
9. Write staging summary.

## Media Matching Flow

1. Build media inventory from configured directories.
2. Compute checksums.
3. Index by filename.
4. Index by normalized filename.
5. Match post image references to source images.
6. Match thumbnails by known patterns.
7. Detect duplicates by filename and hash.
8. Detect orphan media.
9. Detect missing media.
10. Emit match report.

Known thumbnail patterns:

- `thumb_<filename>`
- WordPress derivative suffixes such as `-150x150`
- profile-defined historical patterns

## Conflict Handling Flow

Conflicts should be explicit and reportable.

| Conflict | Default MVP Decision |
| --- | --- |
| duplicate source post ID | keep both in staging, block final write until disambiguated |
| duplicate slug | preserve original slug, add stable suffix for route if required |
| date mismatch between sources | prefer primary profile source, record secondary value |
| title mismatch | prefer primary profile source, record secondary value |
| image filename duplicate, same hash | treat as same artifact |
| image filename duplicate, different hash | preserve both, require disambiguated storage paths |
| missing thumbnail | generate derivative later, but mark imported thumbnail absent |
| missing image | import post as unresolved only if profile allows it |

## Provenance Recording Flow

For every imported record, record:

- import run
- source artifact
- entity type
- entity ID
- source locator
- normalized field
- normalization decision
- conflict decision

MVP source locator examples:

- XML filename + item GUID
- XML filename + legacy post ID
- XML filename + comment ID
- media source path

## Import Reporting Flow

Every import produces a human-readable and machine-readable report.

Required report sections:

- import profile
- source artifacts
- source hashes
- parser warnings
- posts imported
- images matched
- thumbnails matched
- comments imported
- categories imported
- tags imported
- missing images
- missing thumbnails
- orphan media
- duplicate slugs
- duplicate filenames
- conflict decisions
- final status

## Profile Interface

Every import profile should provide:

- `discover_sources`
- `parse_sources`
- `map_records`
- `match_media`
- `resolve_conflicts`
- `write_archive`
- `write_report`

This is a design contract, not an implementation requirement for this phase.

## Avoid Before MVP

- graphical import wizard
- auto-repair of historical data
- silent conflict resolution
- cloud import services
- direct source mutation
- hardcoding TalkingTree into the core schema

## Import Conclusion

The import architecture should be profile-based. TalkingTree becomes the first high-value profile, while PixelPost XML and WordPress WXR remain reusable import foundations for other historical photoblogs.
