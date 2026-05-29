# Original Pixelpost Architecture

## Scope

Primary specimen: Pixelpost v1.7.3, mirrored from PHP Sources and preserved at `archive/original-pixelpost/raw/phpsources.net_Pixelpost-v1.7.3_435-3.zip`.

Lineage specimens: SourceForge releases 1.3, 1.4, 1.4.1, and 1.4.2.

## Top-Level Shape

Pixelpost is a compact procedural PHP/MySQL application. The public site runs through `index.php`; the administration area runs through `admin/index.php`; installer and upgrade behavior runs through `admin/install.php` and helper files in `admin/install/`.

Important directories:

- `admin/`: login, image publishing, category management, options, comments, addon management, password recovery.
- `admin/install/`: installation language files, schema creation, upgrade chain, requirement checks, config generation.
- `addons/`: bundled normal, front, and admin addons.
- `images/`: original uploaded images.
- `thumbnails/`: generated thumbnails.
- `includes/`: database helpers, template helpers, EXIF handling, feed generation, comments, browse behavior, bundled Markdown and XML-RPC support.
- `language/`: public and admin translation files.
- `templates/`: editable HTML template folders, initially `simple` and `horizon`.
- `doc/`: historical documentation, changelog, install/upgrade docs, addon docs, license.

## Runtime Flow

The public entry point loads config, connects to MySQL, fetches the `config` row, refreshes addon metadata, starts a session, and evaluates the `frontpage_init` addon workspace before rendering. The code then selects a language, selects a template file, loads image data, replaces template tags, and emits the final HTML.

The admin entry point redirects to the installer if `includes/pixelpost.php` is missing. Otherwise it loads config, checks the installed version, loads admin and public language files, handles login/session/autologin, refreshes admin addons, then dispatches admin views through `view` and `x` parameters.

## Philosophy Visible In The Code

Pixelpost is image-first and chronology-first. Images are records with a datetime, title, body, image filename, categories, tags, comments, and EXIF. Navigation is built around the latest image, previous/next image, first/last image, thumbnail rows, archives, categories, and browse views.

The application is small enough to understand by reading files directly. Templates are editable HTML with uppercase tags rather than a programming framework. Addons are PHP files discovered from the filesystem and activated from the database. This made the system approachable for photographers and theme authors on shared hosting.

## Era Assumptions

- PHP 4.3+ compatibility was a design target.
- MySQL 3.24.58+ was supported.
- Apache or IIS shared hosting was assumed.
- Direct filesystem writes to `images/`, `thumbnails/`, and `includes/pixelpost.php` were normal.
- `chmod 0777` remediation was considered acceptable during install.
- `mysql_*`, `ereg*`, and `split()` functions were ordinary PHP tools.
- MD5 password hashes were common practice.
- Addons were trusted PHP code.

