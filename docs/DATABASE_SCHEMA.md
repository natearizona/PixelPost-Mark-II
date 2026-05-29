# Database Schema

## Creation And Upgrade Model

Pixelpost begins with a v1.3-era schema in `includes/create_tables.php`, then upgrades forward through a fall-through installer chain in `admin/install/install_schema.php`.

Core tables observed:

- `config`: single-row site/admin configuration.
- `categories`: category definitions.
- `pixelpost`: image posts.
- `comments`: comments tied to image ids.
- `visitors`: visitor log.
- `version`: database version history.
- `catassoc`: many-to-many image/category association.
- `addons`: addon registry with activation state and type.
- `tags`: image tags and alternate-language tags.

## Initial Tables

The v1.3 creation path creates:

- `config` with admin username, MD5 password, email, template, image path, site URL/title, language, calendar, crop, thumbnail dimensions, compression, and date format.
- `categories` with `id` and `name`, seeded with `default`.
- `pixelpost` with `id`, `datetime`, `headline`, `body`, `image`, and legacy single `category`.
- `comments` with `id`, `parent_id`, `datetime`, `ip`, `message`, `name`, and `url`.
- `visitors` with request metadata.

## Later Schema Additions

Major observed upgrades:

- v1.4 adds `version`, `catassoc`, timezone, category glue text, HTML email flag, comment email, indexes, and converts existing image categories into associations.
- v1.5-era upgrades add comments moderation/publish status, addon registry, timestamp and visitorbooking settings.
- v1.6-era upgrades add tags, alternate language fields, Markdown, comment-global/image-specific comment settings, EXIF storage, comment token settings, feed settings, URI/comment anti-spam settings.
- v1.7 adds admin language, separate thumbnail path, subtitle, expanded feed metadata, display order/sort settings, and thumb sharpening.
- v1.7.1 through v1.7.3 mainly advance version rows and deactivate/reactivate bundled addons during upgrade.

## Compatibility Risks

- `DATETIME NOT NULL DEFAULT '0000-00-00 00:00:00'` conflicts with modern MySQL strict SQL modes.
- `TIMESTAMP(14)` is obsolete syntax.
- MySQL `TYPE=` syntax may appear in older lineage releases and would break on modern MySQL.
- Several fields use short `VARCHAR` lengths that may truncate modern URLs, names, paths, and metadata.
- Schema changes are imperative PHP upgrade steps, not declarative migrations.

