# PHP 5.6 Apache MariaDB Environment

## Purpose

This environment is for non-destructive first-boot testing of original Pixelpost releases.

It is not a modernization environment. It exists to answer historical runtime questions:

- Does the installer boot?
- Does database initialization complete?
- Does the admin panel load?
- Do uploads, thumbnails, and EXIF extraction work?
- What warnings and errors appear without patching Pixelpost?

## Runtime Choice

Pixelpost 1.x uses PHP-era APIs removed from modern PHP, especially `mysql_*`, `ereg*`, and `split()`.

The first test environment targets:

- Apache HTTPD
- PHP 5.6
- PHP `mysql`, `mysqli`, `gd`, and `exif` extensions
- MariaDB 10.3 with strict SQL mode disabled

PHP 5.6 is not historically exact for early Pixelpost releases, but it is a pragmatic restoration runtime because it still supports the removed `mysql_*` extension while being easier to containerize than PHP 4.x.

## Files

- `docker/compose.pixelpost.yml`
- `docker/historical/php56-apache/Dockerfile`
- `docker/historical/php56-apache/php.ini`
- `docker/historical/php56-apache/apache-vhost.conf`
- `docker/pixelpost.env.example`
- `tools/reset-first-boot-workspace.sh`

## Safety Rules

- Do not mount preserved trees from `archive/original-pixelpost/extracted/` directly as writable web roots.
- Use disposable copies under `docker/restoration-workspaces/`.
- Do not commit generated `includes/pixelpost.php`, uploaded images, thumbnails, databases, or runtime logs.
- Record failures verbatim in `docs/FIRST_BOOT_EXECUTION_REPORT.md`.

