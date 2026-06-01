# Storage Design

Phase: PixelPost Archaeology Phase 11 - Prototype Architecture

Status: design only.

## Storage Question

What is the simplest storage layer capable of preserving a historical photoblog?

Answer:

```text
SQLite database + filesystem media directory + checksummed provenance records
```

## Database Recommendation

Use SQLite for the MVP.

| Option | MVP Fit | Notes |
| --- | --- | --- |
| SQLite | Best | Portable, simple, easy backup, enough for single-site archives. |
| PostgreSQL | Later | Strong choice for larger hosted or multi-user deployments, unnecessary for MVP. |
| MySQL/MariaDB | Later / import compatibility | Useful for importing legacy dumps, but not ideal as the new prototype dependency. |

## Persistent Data Model

### `posts`

Represents one public photoblog entry.

Required fields:

- `id`
- `title`
- `slug`
- `caption`
- `body`
- `published_at`
- `status`
- `visibility`
- `primary_image_id`
- `legacy_source`
- `legacy_id`
- `legacy_permalink`
- `created_at`
- `updated_at`

### `images`

Represents an original image artifact.

Required fields:

- `id`
- `original_filename`
- `storage_filename`
- `storage_path`
- `mime_type`
- `width`
- `height`
- `filesize`
- `sha256`
- `captured_at`
- `alt_text`
- `source_artifact_id`
- `created_at`

### `post_images`

Allows one primary image now, multiple images later.

Required fields:

- `post_id`
- `image_id`
- `role`
- `sort_order`

Roles:

- `primary`
- `inline`
- `attachment`

### `image_derivatives`

Represents generated or imported resized media.

Required fields:

- `id`
- `image_id`
- `kind`
- `storage_path`
- `width`
- `height`
- `filesize`
- `sha256`
- `generated_by`

Derivative kinds:

- `thumbnail`
- `small`
- `medium`
- `large`
- `original`

### `exif_records`

Stores raw and normalized camera metadata.

Required fields:

- `id`
- `image_id`
- `raw_json`
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
- `source`

Valid source values:

- `imported_database`
- `extracted_from_image`
- `manual`
- `absent`

### `comments`

Stores per-image/post conversation.

Required fields:

- `id`
- `post_id`
- `author_name`
- `author_url`
- `author_email_hash`
- `body`
- `status`
- `created_at`
- `legacy_id`
- `legacy_parent_id`
- `source_artifact_id`

### `categories`

Required fields:

- `id`
- `name`
- `slug`
- `description`
- `legacy_id`

### `tags`

Required fields:

- `id`
- `name`
- `slug`
- `legacy_id`

### `post_categories`

Required fields:

- `post_id`
- `category_id`

### `post_tags`

Required fields:

- `post_id`
- `tag_id`

### `source_artifacts`

Represents import inputs.

Required fields:

- `id`
- `kind`
- `source_path`
- `original_filename`
- `filesize`
- `sha256`
- `observed_at`
- `notes`

Kinds:

- `pixelpost_xml`
- `wordpress_wxr`
- `image`
- `thumbnail`
- `sql_dump`
- `manual_manifest`

### `provenance_events`

Records how data entered Mark II.

Required fields:

- `id`
- `import_run_id`
- `entity_type`
- `entity_id`
- `field_name`
- `source_artifact_id`
- `source_locator`
- `source_value_hash`
- `normalized_value_hash`
- `decision`
- `notes`

### `import_runs`

Required fields:

- `id`
- `profile_name`
- `started_at`
- `completed_at`
- `status`
- `source_summary_json`
- `result_summary_json`

## Media Storage Layout

Recommended layout:

```text
site/
  archive.sqlite
  media/
    originals/
      aa/
        <sha256>-<original-filename>
    derivatives/
      thumbnail/
      small/
      medium/
      large/
  imports/
    reports/
    manifests/
  exports/
```

Use hash-prefix directories to avoid huge flat folders.

## Checksum Strategy

Compute SHA-256 for:

- every source XML file
- every imported JPEG
- every imported thumbnail
- every generated derivative
- every export manifest
- SQLite export snapshots

Store checksums in `source_artifacts`, `images`, `image_derivatives`, and export manifests.

## Provenance Storage Model

Every imported entity should be traceable back to:

- source artifact
- source field or locator
- import run
- normalization rule
- conflict decision

For MVP, line-level provenance is nice but not required. Field-level provenance with source artifact and source locator is enough.

## Avoid Before MVP

- object storage as a requirement
- distributed databases
- search server
- event-sourcing architecture
- content-addressed storage as the only path format
- multi-tenant schema

## Storage Conclusion

SQLite plus filesystem media is the simplest storage layer capable of preserving a historical photoblog while remaining useful for a new photoblog.
