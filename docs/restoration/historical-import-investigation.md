# Pixelpost 1.7.3 Historical Import Investigation

Question: What artifacts are required to restore an original Pixelpost site?

Answer: a restorable historical Pixelpost site requires both a database export and filesystem artifacts. The database alone is not sufficient because image filenames are stored in the database while image and thumbnail bytes live on disk.

## Official/Bundle Evidence

Bundled upgrade documentation instructs operators to back up both:

- Pixelpost database tables through MySQL administration export.
- The full Pixelpost installation folder, especially `includes/pixelpost.php`.

Relevant bundled files:

- `doc/upgrade.txt`
- `doc/upgrade.html`
- `doc/install.txt`
- `includes/pixelpost-sample.php`

The project documentation assumes external database export tooling such as MySQL administration or phpMyAdmin. No bundled first-party importer/exporter for complete site migration was found in source inspection.

## Required Import Artifacts

| Artifact | Required | Why |
| --- | --- | --- |
| SQL dump of Pixelpost tables | Yes | Stores posts, config, categories, comments, tags, EXIF, version state |
| `images/` directory | Yes | Original uploaded JPEG files referenced by `pixelpost_pixelpost.image` |
| `thumbnails/` directory | Strongly recommended | Existing generated thumbnails; may be regenerated if originals and GD workflow are available |
| `includes/pixelpost.php` | Yes or reconstructable | Database host/user/password/database/prefix; prefix is critical |
| `templates/` directory | Required for original appearance | Active template name is stored in config, but template files are on disk |
| `addons/` directory | Required if site used addons | Addon state is tracked in DB, code is on disk |
| `language/` directory changes | Required if customized | Language file choices are stored in config |
| Pixelpost source version | Required | Determines whether installer upgrade path must run |
| File permissions map | Recommended | `images/`, `thumbnails/`, and `includes/` must be writable during install/restore operations |

## Tables And Relationships

The schema is MyISAM and does not use foreign-key constraints. Relationships are implicit:

| Table | Import Role |
| --- | --- |
| `pixelpost_config` | Site settings, admin credentials, image path, thumbnail path, template, EXIF toggle, feed settings |
| `pixelpost_pixelpost` | Photo posts; `image` field names files in `images/`; `exif_info` stores serialized EXIF |
| `pixelpost_categories` | Category definitions |
| `pixelpost_catassoc` | Joins category IDs to image IDs |
| `pixelpost_tags` | Tags keyed by image ID |
| `pixelpost_comments` | Comments keyed to `parent_id`, which corresponds to image/post ID |
| `pixelpost_visitors` | Visitor/referrer records; useful historically but not required to display images |
| `pixelpost_version` | Upgrade state; installer uses this to decide schema status |
| `pixelpost_addons` | Enabled addon state |
| `pixelpost_banlist` | Spam/moderation data, created after full 1.7.3 config storage |

Evidence:

- `includes/create_tables.php`
- `docs/restoration/evidence/1.7.3-repeatability/pixelpost-repeatability-schema.sql`

## Import Compatibility Notes

SQL dumps from original sites should be restored into a MySQL runtime close to the source era. The verified runtime is MySQL `5.1.73`.

Risks:

- Modern MySQL/MariaDB rejects legacy syntax such as `TIMESTAMP(14)`.
- Dumps may contain MyISAM table options and old character-set assumptions.
- The verified schema dump uses `DEFAULT CHARSET=latin1` for most tables.
- Site text may be mixed encodings depending on original hosting and language files.
- Paths stored in `pixelpost_config.imagepath` and `thumbnailpath` are relative by default and must match the restored filesystem layout.
- `siteurl` may point to the historical domain and may need environment-local adjustment in a disposable restore.
- Addons may depend on removed external services.
- Password hashes are MD5-era and must be treated as sensitive.

## Minimal Restore Procedure

1. Create an isolated MySQL `5.1.73` database.
2. Import the historical SQL dump.
3. Copy historical `images/` into the disposable workspace.
4. Copy historical `thumbnails/` if present.
5. Copy historical `templates/`, `addons/`, `language/`, and any customized files.
6. Reconstruct or copy `includes/pixelpost.php` with the correct table prefix.
7. Start Pixelpost on the verified PHP runtime.
8. Visit `admin/install.php` if `pixelpost_version` is below `1.73`; allow original upgrade chain to run in the disposable workspace/database.
9. Check `pixelpost_config.imagepath`, `thumbnailpath`, `template`, `siteurl`, and language settings.
10. Validate public image page, browse/archive page, category page, comments, feeds, and admin image list.

## Restore Completeness Checklist

A historical content restore is complete only when:

- Every `pixelpost_pixelpost.image` has a matching file in `images/`.
- Every expected thumbnail exists or can be regenerated.
- `pixelpost_catassoc.image_id` values match existing image IDs.
- `pixelpost_catassoc.cat_id` values match existing category IDs.
- `pixelpost_tags.img_id` values match existing image IDs.
- `pixelpost_comments.parent_id` values match existing image IDs.
- EXIF data in `exif_info` unserializes without corruption.
- The active template exists under `templates/`.
- Enabled addons have matching files under `addons/`.
- Feeds render without fatal errors.

## Answer

Historical content can likely be restored when the operator has a complete database dump plus the corresponding filesystem artifacts. The database dump restores metadata and chronology; the filesystem restores the actual photoblog images, thumbnails, templates, addons, and local customizations.

The next executable import test should use a real historical Pixelpost database dump and matching `images/` directory in a disposable workspace. Do not import into the preservation archive and do not perform destructive upgrades on original artifacts.
