# Database Schema

## Scope

This document describes the Pixelpost 1.7.3 schema as an evolved historical artifact. It is based on the recovered installer and upgrade code, not a successful modern database install.

Evidence files:

- `includes/create_tables.php`
- `admin/install/install_schema.php`
- `admin/new_image.php`
- `admin/images_edit.php`
- `includes/functions_browse.php`
- `includes/functions_comments.php`
- `includes/functions_exif.php`
- `includes/functions_feeds.php`

## Subsystem Purpose

The database stores photoblog metadata: configuration, image posts, categories, tags, comments, visitor logs, addon state, spam lists, and schema version history. Original image files and thumbnails remain in the filesystem.

## Creation And Upgrade Model

Pixelpost does not define a final schema in one declarative file. It creates a v1.3-era base schema, then upgrades forward through a deliberate fall-through switch in `admin/install/install_schema.php`.

Fresh install path:

1. `Create13Tables($prefix)`
2. `Set_Configuration($prefix)`
3. `UpgradeTo14($prefix)`
4. `UpgradeTo141($prefix)`
5. `UpgradeTo15beta(...)`
6. `UpgradeTo15final(...)`
7. `UpgradeTo16beta(...)`
8. `UpgradeTo16final(...)`
9. `UpgradeTo17(...)`
10. `UpgradeTo171(... '1.71')`
11. `UpgradeTo171(... '1.72')`
12. `UpgradeTo171(... '1.73')`

This means the installer itself preserves release lineage, but it also means fresh installation inherits all historical SQL assumptions.

## Core Tables

### `{prefix}config`

Purpose: single-row site and admin configuration.

Important observed fields:

- `id`
- `admin`
- `password`
- `email`
- `commentemail`
- `template`
- `imagepath`
- `thumbnailpath`
- `siteurl`
- `sitetitle`
- `subtitle`
- `langfile`
- `admin_langfile`
- `altlangfile`
- `calendar`
- `crop`
- `thumbwidth`
- `thumbheight`
- `thumbnumber`
- `compression`
- `thumb_sharpening`
- `dateformat`
- `timezone`
- `catgluestart`
- `catglueend`
- `htmlemailnote`
- `timestamp`
- `visitorbooking`
- `global_comments`
- `markdown`
- `exif`
- `token`
- `token_time`
- `comment_timebetween`
- `max_uri_comments`
- `rsstype`
- `feed_discovery`
- `feed_title`
- `feed_description`
- `feed_copyright`
- `allow_comment_feed`
- `feed_external`
- `feed_external_type`
- `display_order`
- `display_sort_by`

Interactions:

- Public bootstrap reads it every request.
- Admin authentication reads `admin` and `password`.
- Options writes many fields.
- Upload reads image paths, thumbnail settings, comments, EXIF, and language settings.

### `{prefix}pixelpost`

Purpose: core photo post table.

Important observed fields:

- `id`
- `datetime`
- `headline`
- `body`
- `image`
- legacy `category`
- `comments`
- `alt_headline`
- `alt_body`
- `exif_info`

Historical fields `rid`, `rating`, and `score` appear in earlier lineage notes/tests but the recovered 1.7.3 installer centers on the fields above.

Interactions:

- Upload inserts one row per photograph.
- Public front page selects current/latest eligible image.
- `showimage` selects by `id`.
- Browse/feed/archive queries filter and order by `datetime`.
- Admin edit updates date, title, body, image metadata, comments setting, and related tables.

### `{prefix}categories`

Purpose: category definitions.

Fields:

- `id`
- `name`
- `alt_name`

Interactions:

- Installer seeds `default`.
- Admin category manager creates/updates/deletes rows.
- Browse and image pages render category labels.

### `{prefix}catassoc`

Purpose: many-to-many relationship between images and categories.

Fields:

- `id`
- `cat_id`
- `image_id`

Interactions:

- Upload inserts selected categories.
- Edit deletes/reinserts category associations.
- Browse filters by category.
- Public image page renders category links for the current image.

### `{prefix}tags`

Purpose: tag assignments for images, including alternate-language tags.

Fields:

- `img_id`
- `tag`
- `alt_tag`

Interactions:

- Upload and edit normalize free-text tag strings and insert rows.
- Browse supports `x=browse&tag={tag}`.
- Feeds support tag-specific RSS/Atom.

### `{prefix}comments`

Purpose: visitor comments tied to an image.

Important observed fields:

- `id`
- `parent_id`
- `datetime`
- `ip`
- `message`
- `name`
- `url`
- `email`
- `publish`

Interactions:

- Public comment submission inserts rows.
- Public image page reads published comments and counts.
- Admin comments view moderates/deletes.
- Feeds may expose comment feeds.

### `{prefix}visitors`

Purpose: visitor/referrer logging.

Fields:

- `id`
- `datetime`
- `host`
- `referer`
- `ua`
- `ip`
- `ruri`

Interactions:

- Public front controller calls `book_visitor(...)` when visitor booking is enabled and no `lastvisit` cookie exists.
- Admin/stat addons read visitor data.
- Anti-spam helpers can delete bad referrers.

### `{prefix}version`

Purpose: schema version history.

Fields:

- `id`
- `upgrade_date`
- `version`

Important forensic note: `UpgradeTo14()` creates `upgrade_date` as `TIMESTAMP(14) NOT NULL`, which blocks installation on modern MariaDB/MySQL runtimes.

### `{prefix}addons`

Purpose: addon registry.

Fields:

- `id`
- `addon_name`
- `status`
- `type`

Interactions:

- Addon refresh scans `addons/` and syncs records.
- Admin addon page toggles `status`.
- Front/admin bootstrap includes enabled addon files by `type`.

### `{prefix}banlist`

Purpose: anti-spam lists.

Fields:

- `id`
- `moderation_list`
- `blacklist`
- `ref_ban_list`
- `acceptable_num_links`

Interactions:

- Created lazily by `create_banlist()`.
- Public comments check blacklist/moderation lists.
- Admin options/comments update lists.
- Referrer cleanup reads `ref_ban_list`.

## Relationship Model

- One image row has many category associations.
- One category has many image associations.
- One image has many tag rows.
- One image has many comments through `comments.parent_id`.
- Config is effectively singleton.
- Addons are filesystem-backed records, not normalized packages.
- Version rows accumulate upgrade history rather than updating one current-version row.

## Original Developer Assumptions

- MySQL accepts older syntax and permissive defaults.
- Application code can issue schema-altering SQL during web requests.
- Table prefixes allow multiple installs in one database.
- A simple relational model is enough; images stay in directories.
- Serialized EXIF data in a text field is acceptable.
- Visitor logging belongs in the same database as photoblog content.

## Strengths

- The model is understandable and portable.
- Image files are not trapped inside the database.
- Category associations and tags support archival navigation.
- Version history records upgrade steps.
- The schema aligns closely with the photoblog workflow.

## Weaknesses

- Historical SQL syntax breaks in modern runtimes.
- Zero dates and permissive defaults conflict with strict SQL modes.
- There are few explicit foreign keys.
- Serialized EXIF is opaque to SQL.
- Config is a wide singleton row with many unrelated concerns.
- The upgrade chain is imperative and depends on old MySQL/PHP behavior.

## Historical Context

The schema is not trying to model a full CMS. It models a personal image archive: photographs, dates, captions, metadata, categories, tags, comments, and feeds. Its simplicity is part of why Pixelpost could be deployed and understood by photographers on ordinary hosting.

## Preservation Notes

Future work should preserve the conceptual schema even if the physical schema later changes:

- photograph as primary record,
- filesystem-backed image ownership,
- chronology as central index,
- categories/tags as archive aids,
- EXIF attached to images,
- comments as optional per-image context,
- feeds and portable archives as first-class outputs.
