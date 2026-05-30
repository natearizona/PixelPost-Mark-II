# Historical Runtime Rationale

## Pixelpost 1.7.3 Runtime Target

Pixelpost 1.7.3 documents these requirements:

- Apache Webserver or Windows IIS
- PHP 4.3.0 or higher
- PHP GD library with JPEG support
- MySQL 3.24.58 or higher
- writable image and thumbnail directories

The source also uses APIs that constrain practical runtime selection:

- `mysql_*` database functions
- `ereg*` regex functions
- `split()`
- GD image functions
- bundled EXIF parser plus PHP EXIF/GD-era assumptions

## Ideal Historical Environment

A historically plausible late-2000s shared-hosting environment would look like:

- Apache 2.0 or 2.2
- PHP 5.2.x or PHP 5.3.x
- MySQL 4.1 or MySQL 5.0
- GD 2.x with JPEG support
- filesystem write access to `images/`, `thumbnails/`, and generated config files
- permissive non-strict MySQL defaults
- no modern HTTPS-only or container assumptions

This would most closely match the era in which Pixelpost 1.7.3 was used.

## Practical Container Environment

The first practical container target is:

- Apache via `php:5.6-apache`
- PHP 5.6
- PHP extensions: `mysql`, `mysqli`, `gd`, `exif`
- MariaDB 10.3
- SQL strict mode disabled
- localhost-only port binding

PHP 5.6 is not perfectly historical, but it is old enough to retain the removed `mysql_*` extension and new enough to be containerized with less archaeology than PHP 4.x or PHP 5.2.

## Required Compromises

- PHP 5.6 is newer than the original minimum PHP 4.3 target.
- MariaDB 10.3 is newer than original MySQL 3.24/4.x/5.0 assumptions.
- Debian Jessie package archives may be needed for old PHP container builds.
- Container networking differs from shared hosting.
- Database hostname will be `pixelpost-db`/Compose service name rather than `localhost`.
- Filesystem ownership may need container-user compatible permissions in disposable workspaces.

## Preservation Boundary

The runtime may be adjusted to emulate historical hosting, but Pixelpost source must not be patched during the restoration phase.

Any runtime workaround must be documented as an environmental compromise, not as a source modernization.

