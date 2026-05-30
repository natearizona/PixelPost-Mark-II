# Historical Restoration Status

## Current Mode

PixelPost Mark II remains in digital archaeology mode.

No Pixelpost source code has been modified.
No schema definitions have been patched.
No deprecated PHP functions have been rewritten.

## Exact Version Identification

The active specimen is Pixelpost 1.7.3.

Evidence:

```text
ReadMe.txt:1
Pixelpost version 1.7.3
```

Installer internal version:

```text
admin/install.php:13
define('PP_VERSION', '1.73');
```

Raw archive:

```text
archive/original-pixelpost/raw/phpsources.net_Pixelpost-v1.7.3_435-3.zip
```

Archive internal timestamps:

```text
09-02-2009 17:22-19:24
```

External release-date corroboration:

```text
OpenSourceCMS lists current stable version 1.7.3 and latest stable release date 09/02/2009.
```

Confidence:

```text
High for version number.
Medium-high for release date.
```

The release-date confidence is not marked absolute because the recovered archive source is a mirror and the official Pixelpost site is no longer a stable primary source.

## Historical Runtime Profile

Official bundled requirements from `ReadMe.txt`:

```text
Apache Webserver or Windows IIS
PHP 4.3.0 or higher
PHP with GD-lib and JPG support
MySQL 3.24.58 or higher
```

Installer runtime check from `admin/install/language/install-lang-english.php`:

```text
PHP version > or = 4.3.3
```

Common hosting profile inferred from docs:

- Apache shared hosting or Windows IIS.
- PHP 4.3+ with classic `mysql_*` extension.
- GD with JPEG support.
- MySQL 3.23/3.24/4.x-era tolerance for old timestamp syntax.
- Writable `images/`, `thumbnails/`, and `includes/` during install.

## What Works

In the isolated VPS lab:

```text
Installer launch: works
Requirements page: HTTP 200
Database credential test: HTTP 200
Administrator validation: HTTP 200
Settings validation: HTTP 200
Configuration generation: works
```

Generated file:

```text
/opt/pixelpost-restoration-lab/workspaces/pixelpost-1.7.3-first-boot/includes/pixelpost.php
```

Security controls verified:

```text
127.0.0.1:18080 only
traefik.enable=false
pixelpost-lab-net contains only pixelpost-php and pixelpost-db
archive-readonly specimen is root-owned and read-only
```

## What Fails

Fresh database finalization fails when creating the version table:

```text
includes/create_tables.php:126
`upgrade_date` TIMESTAMP(14) NOT NULL
```

Observed database failures:

```text
MariaDB 10.3: Too big precision 14 specified for 'upgrade_date'. Maximum is 6.
MySQL 5.5: SQL syntax error near '(14) NOT NULL'
MariaDB 5.5: Too big precision 14 specified for 'upgrade_date'. Maximum is 6.
MariaDB 5.5 MAXDB: Too big precision 14 specified for 'upgrade_date'. Maximum is 6.
```

Tables created before failure:

```text
pixelpost_categories
pixelpost_comments
pixelpost_config
pixelpost_pixelpost
pixelpost_visitors
```

Tables not created:

```text
pixelpost_version
pixelpost_catassoc
pixelpost_addons
later upgrade-era tables/columns
```

## Confidence Level

```text
Installer boot: high
Config generation: high
Database mismatch diagnosis: high
Exact successful historical DB runtime: medium-low pending MySQL 4.x/5.0 reconstruction
Need for source patch: not established
```

## Container Runtime Attempts

Tested:

```text
php:5.6-apache + mariadb:10.3
php:5.6-apache + mysql:5.5
php:5.6-apache + mariadb:5.5
php:5.6-apache + mariadb:5.5 + MAXDB SQL mode
```

Unavailable official/vendor image tags:

```text
mysql:4
mysql:4.1
mysql:5.0
mysql:5.1
mysql/mysql-server:5.0
mysql/mysql-server:5.1
```

## Historically Accurate Runtime Recommendation

Recommended next target:

```text
Apache 2.0/2.2
PHP 5.2.x, or PHP 5.0/5.1 if container reconstruction is feasible
Oracle MySQL 4.0.x or 5.0.x
GD 2.x with JPEG support
classic mysql extension
```

Rationale:

- Pixelpost 1.7.3 was packaged on or around 2009-09-02, but it preserves schema syntax from older Pixelpost upgrade paths.
- The bundled docs claim MySQL 3.24.58+ support.
- `TIMESTAMP(14)` appears in 1.4.2 and 1.7.3 schema code.
- MySQL documentation indicates pre-4.1 timestamp behavior differed significantly.
- Tested MySQL/MariaDB 5.5+ family containers do not accept the schema.

## Recommended Next Action

Build a provenance-recorded container for MySQL 4.0 or Oracle MySQL 5.0 from archival packages or source.

Do not patch Pixelpost until that attempt is complete.

If a historically accurate database runtime cannot be reconstructed, the first future restoration shim should be limited to a disposable workspace and documented as:

```text
TIMESTAMP(14) compatibility shim
```

not as a modernization of Pixelpost.

## Sources

- Local source tree: `archive/original-pixelpost/extracted/pixelpost-1.7.3`
- Local raw archive: `archive/original-pixelpost/raw/phpsources.net_Pixelpost-v1.7.3_435-3.zip`
- OpenSourceCMS Pixelpost profile: `https://www.opensourcecms.com/pixelpost/`
- MySQL 5.0 documentation: `https://documentation.help/MySQL-5.0/ch11s03.html`
- MySQL old temporal datatype note: `https://dev.mysql.com/blog-archive/mysql-8-0-removing-support-for-old-temporal-datatypes/`
