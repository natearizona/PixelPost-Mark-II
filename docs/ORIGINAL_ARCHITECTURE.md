# Original Architecture

## Scope

This document describes the recovered Pixelpost 1.7.3 source tree as a historical software artifact. It is not a modernization plan and it does not prescribe code changes.

Evidence specimen: `archive/original-pixelpost/extracted/pixelpost-1.7.3/`.

## Subsystem Purpose

Pixelpost is a single-purpose photoblog application. Its architecture is organized around one central act: publish a photograph with a title, date, notes, metadata, comments, categories, tags, and template-driven public presentation.

The public site is not a general CMS. The homepage is the current photograph. Browse pages, feeds, comments, archives, and categories orbit that photograph-first center.

## Major Files Involved

- `index.php`: public front controller, template loader, image selector, tag replacer, feed/comment dispatcher.
- `admin/index.php`: admin shell, login/session handling, admin page inclusion.
- `admin/new_image.php`: upload form and photo creation pipeline.
- `admin/images_edit.php`: image listing, editing, deletion, mass actions, category/tag edits.
- `admin/comments.php`: comment moderation and deletion.
- `admin/categories.php`: category administration.
- `admin/options.php`: site, template, thumbnail, feed, comment, spam, and display options.
- `admin/view_addons.php`: addon activation/deactivation interface.
- `admin/install.php`: installer and upgrade entrypoint.
- `admin/install/install_functions.php`: installer validation, form persistence, configuration writing helpers.
- `admin/install/install_schema.php`: fall-through upgrade dispatcher.
- `includes/create_tables.php`: table creation and historical upgrade functions.
- `includes/functions.php`: shared utility, database bootstrap, addons, thumbnails, tags, spam helpers.
- `includes/functions_browse.php`: browse/category/archive/tag listing logic.
- `includes/functions_comments.php`: public comment submission workflow.
- `includes/functions_exif.php`: EXIF extraction, serialization, and template replacement.
- `includes/functions_feeds.php`: RSS, Atom, comment feed generation, feed template tags.
- `templates/{template}/`: editable HTML templates with replacement tags.
- `addons/`: bundled addon scripts registered into named hook workspaces.

## Execution Flow

### Public Request

1. `index.php` disables visible error reporting, defines `PIXELPOST`, loads `includes/pixelpost.php`, includes `includes/functions.php`, and calls `start_mysql(...)`.
2. The single configuration row is loaded from `{prefix}config`.
3. Addons are refreshed from the filesystem and enabled front addons are included.
4. A session starts; front addon workspace `frontpage_init` runs.
5. Request variables such as `x`, `showimage`, `lang`, `popup`, `category`, `archivedate`, and `tag` determine the page mode.
6. Pixelpost loads a template file from the active template directory.
7. If the request needs an image, it queries `{prefix}pixelpost` for either the requested image or the current image. Public visitors only receive images whose `datetime <= current site time`; logged-in admins can preview future images.
8. It builds image, navigation, category, comment, EXIF, feed, and browse variables.
9. Template tags are replaced directly inside the HTML template string.
10. Final HTML is echoed.

### Admin Request

1. `admin/index.php` checks for `../includes/pixelpost.php`; if missing, it redirects to `install.php`.
2. It loads config, shared functions, language files, and starts MySQL.
3. Login compares the submitted password as MD5 against the stored config password.
4. Enabled admin addons are included.
5. The admin shell always includes the major admin modules; each module decides whether to render based on `view`, `x`, `action`, or `id`.

### Installer Request

1. `admin/install.php` defines `PP_VERSION` as `1.73`.
2. If a config file exists, it attempts a MySQL connection and loads `includes/create_tables.php`.
3. Installer functions validate requirements, database details, administrator details, and site settings.
4. During finalization, `admin/install/install_schema.php` runs a fall-through version switch from the installed schema to 1.73.

## Database Interactions

Pixelpost uses the legacy PHP `mysql_*` extension directly. There is no database abstraction layer. Table names are constructed by concatenating `$pixelpost_db_prefix` with table names.

Primary tables:

- `{prefix}config`: single-row configuration.
- `{prefix}pixelpost`: photo posts.
- `{prefix}categories`: category definitions.
- `{prefix}catassoc`: image/category many-to-many associations.
- `{prefix}tags`: image tags and alternate-language tags.
- `{prefix}comments`: comments linked to images through `parent_id`.
- `{prefix}visitors`: visitor and referrer log.
- `{prefix}version`: historical upgrade records.
- `{prefix}addons`: addon registry and enabled state.
- `{prefix}banlist`: anti-spam lists, created lazily.

The schema is imperative. Installation creates an old 1.3-style base schema, then upgrades step by step to later releases.

## Original Developer Assumptions

- The deployment target is shared PHP/MySQL hosting, likely Apache with mod_php.
- The site owner can upload files by FTP and make `images/`, `thumbnails/`, and `includes/` writable during setup.
- A single administrator controls the site.
- One active template directory defines the front-end presentation.
- Direct SQL and global variables are acceptable application glue.
- Images live in the filesystem, while metadata lives in MySQL.
- The front page is the latest eligible photograph, not a stream of mixed content.
- PHP 4.3.3+ era functions such as `mysql_*`, `ereg*`, `split`, and `get_magic_quotes_gpc` are available.

## Strengths

- The architecture is easy to understand once the entrypoints are mapped.
- Templates are plain HTML and can be edited without learning a framework.
- The public model is strongly image-first.
- The file/database split is portable and understandable for photographers on shared hosting.
- The addon hook model is simple and inspectable.
- Scheduled/future-dated images are a built-in publishing behavior.
- The system stores EXIF alongside the post rather than treating it as an afterthought.

## Weaknesses

- Global state makes execution order important and fragile.
- SQL is built inline throughout the codebase.
- The installer couples fresh install and historical migration tightly.
- The template engine lacks a formal escaping model.
- Addons execute arbitrary PHP inside the same process and trust boundary.
- Authentication and session handling reflect the security assumptions of its era.
- The code depends on PHP and MySQL behaviors that no longer exist by default.

## Historical Context

Pixelpost belongs to the independent photoblogging era: personal domains, RSS readers, blogrolls, small communities, and self-hosted publishing. It is not structured like WordPress, where posts, pages, taxonomies, themes, widgets, and plugins form a general-purpose publishing system.

Pixelpost is narrower and calmer. It assumes a photographer wants to publish one photograph at a time, with the photograph as the primary artifact and the writing as supporting context. This narrowness is a core part of its historical value and should be preserved in future Mark II work.

## Preservation Notes

For continuation work, preserve these architectural truths before changing implementation:

- The current photograph is the center of the public site.
- Chronology is a first-class navigation model.
- Images are owned files, not opaque media records.
- Templates are editable artifacts.
- Archives, categories, tags, EXIF, feeds, and comments support the photograph rather than competing with it.
- Lightweight deployment is part of the project identity.
