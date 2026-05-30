# First Boot Execution Report

## Scope

Requested phase: runtime execution attempt for original untouched Pixelpost releases in isolated, non-destructive restoration containers.

Date of attempt: 2026-05-28, America/Phoenix.

Primary goal: determine whether the original Pixelpost releases can boot, install, initialize a database, load admin, upload images, generate thumbnails, and extract EXIF without patching source.

## Preservation Rule Applied

The preserved extraction trees under `archive/original-pixelpost/extracted/` were not modified.

Separate first-boot restoration copies were created under `docker/restoration-workspaces/`:

- `docker/restoration-workspaces/pixelpost-1.3-first-boot`
- `docker/restoration-workspaces/pixelpost-1.4-first-boot`
- `docker/restoration-workspaces/pixelpost-1.4.1-first-boot`
- `docker/restoration-workspaces/pixelpost-1.4.2-first-boot`
- `docker/restoration-workspaces/pixelpost-1.7.3-first-boot`

These are disposable testing workspaces. Any future installer-generated files, database configs, uploaded test images, thumbnails, or runtime logs should be created only inside these restoration workspaces or inside containers mounted from them.

## Environment Reconstruction Status

Historical runtime target inferred from Pixelpost documentation:

- Apache or Windows IIS
- PHP 4.3.0 or higher
- GD with JPEG support
- MySQL 3.24.58 or higher

No working local container/runtime environment was available in this Codex shell at the time of this attempt.

Commands attempted:

```text
$ docker --version
zsh:1: command not found: docker

$ podman --version
zsh:1: command not found: podman

$ colima version
zsh:1: command not found: colima

$ qemu-system-x86_64 --version
zsh:1: command not found: qemu-system-x86_64

$ php -v
zsh:1: command not found: php

$ mysql --version
zsh:1: command not found: mysql

$ brew --version
zsh:1: command not found: brew

$ nix --version
zsh:1: command not found: nix
```

Bundled Codex workspace dependencies were checked. Node.js and Python runtimes are available, but no PHP, MySQL, Docker, Podman, Colima, Nix, Homebrew, or QEMU runtime was exposed.

## Execution Attempt Results

Because no container engine, PHP runtime, or MySQL runtime was available, no HTTP first boot could be executed in this pass.

| Check | Result | Notes |
| --- | --- | --- |
| Installer boots | Not executed | Blocked before HTTP/PHP runtime could start. |
| Admin panel loads | Not executed | Blocked before installer/admin could be served. |
| Database initialization works | Not executed | Blocked by missing MySQL/MariaDB runtime. |
| Uploads function | Not executed | Requires completed install and writable test workspace. |
| Thumbnail generation functions | Not executed | Requires PHP GD runtime and upload test fixture. |
| EXIF extraction functions | Not executed | Requires PHP runtime and EXIF-capable image fixture. |
| Runtime warnings/errors | Environment errors captured above | No Pixelpost PHP warnings were produced because PHP did not run. |

## Runtime Failure Log

The first concrete failure is environment-level, not application-level:

```text
No container engine available: docker, podman, colima, and qemu-system-x86_64 were not found.
No PHP runtime available: php was not found.
No MySQL client/runtime available: mysql was not found.
No local package/runtime bootstrapper available: brew and nix were not found.
```

This prevents non-destructive containerized first-boot testing in the current shell.

## Required Next Step

Provision an isolated historical runtime before retrying first boot. Recommended target:

- Container engine: Docker or Podman
- Web runtime: Apache + PHP 5.6 with `mysql` extension and GD enabled
- Database: MySQL 5.5 or compatible MariaDB configured with non-strict SQL mode
- Mount source read-only from `archive/original-pixelpost/extracted/`
- Copy source into a writable container volume for installer-generated files
- Persist database and upload directories only in restoration workspace volumes

The first runtime to test should be Pixelpost 1.7.3, because it is the final preserved release. After that, test 1.4.2, 1.4.1, 1.4, and 1.3 for lineage.

## Planned First-Boot Matrix

When a container runtime is available, run this sequence for each release:

1. Start web + database services with empty database.
2. Open `/admin/install.php`.
3. Record installer warnings and requirement checks verbatim.
4. Complete install using throwaway credentials.
5. Record generated tables and database version row.
6. Open `/admin/index.php`.
7. Log in.
8. Upload a small JPEG with EXIF.
9. Confirm original image copy, thumbnail creation, and stored EXIF.
10. Upload PNG and GIF fixtures if accepted by the era release.
11. Record all PHP warnings, Apache logs, MySQL errors, and visible UI errors without patching.

## Status

First-boot execution is blocked pending runtime/container availability. Preservation and restoration workspace separation are complete.

## 2026-05-30 Update

A containerized historical runtime scaffold has been added for the next execution attempt:

- `docker/compose.pixelpost.yml`
- `docker/historical/php56-apache/Dockerfile`
- `docker/historical/php56-apache/php.ini`
- `docker/historical/php56-apache/apache-vhost.conf`
- `docker/pixelpost.env.example`
- `tools/reset-first-boot-workspace.sh`
- `docs/historical-environments/PHP56_APACHE_MARIADB.md`
- `runtime-testing/FIRST_BOOT_RUNBOOK.md`

The scaffold initially targeted Apache, PHP 5.6, PHP `mysql`/`mysqli`/`gd`/`exif` extensions, and MariaDB 10.3 with strict SQL mode disabled.

Local verification performed:

```text
tools/reset-first-boot-workspace.sh 1.7.3
reset .../docker/restoration-workspaces/pixelpost-1.7.3-first-boot from .../archive/original-pixelpost/extracted/pixelpost-1.7.3

sh -n tools/reset-first-boot-workspace.sh
bash -n tools/reset-first-boot-workspace.sh
```

The reset helper passed shell syntax validation and successfully recreated a disposable Pixelpost 1.7.3 first-boot workspace. Docker execution remains untested in this shell because no container runtime is currently available.

## 2026-05-30 VPS Restoration Lab Execution

Target VPS:

```text
2.24.122.151
```

Runtime:

- Docker 29.4.3
- Docker Compose 5.1.3
- `pixelpost-php`: Apache with PHP 5.6, `mysql`, `mysqli`, GD, EXIF, and rewrite enabled
- `pixelpost-db`: MariaDB 10.3

Preservation handling:

- Source specimen copied to `/opt/pixelpost-restoration-lab/archive-readonly/pixelpost-1.7.3`.
- Archive specimen permissions set read-only with `chmod -R a-w`.
- Disposable runtime workspace created at `/opt/pixelpost-restoration-lab/workspaces/pixelpost-1.7.3-first-boot`.
- Workspace owned by container web user `33:33`.

Container build notes:

The first PHP image build failed because the retired Debian Stretch package sources in `php:5.6-apache` were no longer available from live Debian mirrors:

```text
E: Failed to fetch http://deb.debian.org/debian/dists/stretch/main/binary-amd64/Packages 404 Not Found
E: Failed to fetch http://security.debian.org/debian-security/dists/stretch/updates/main/binary-amd64/Packages 404 Not Found
```

The Dockerfile was adjusted to use `archive.debian.org`, remove unavailable retired security/update channels, and allow archived unauthenticated package metadata. This is a container-build accommodation only; no Pixelpost source files were patched.

Successful build installed and enabled:

```text
mysql
mysqli
gd
exif
Apache rewrite
```

First installer GET:

```text
URL: http://127.0.0.1:18080/admin/install.php
HTTP status: 200
```

Observed first visible Pixelpost runtime warning:

```text
Deprecated: Function ereg_replace() is deprecated in /var/www/html/admin/install/install_functions.php on line 358
```

Additional warnings appeared from the same deprecated function on lines 157 and 158 while rendering installer language options.

Apache log observation:

```text
AH00558: apache2: Could not reliably determine the server's fully qualified domain name, using 172.16.8.3. Set the 'ServerName' directive globally to suppress this message
```

MariaDB observation:

```text
Version: '10.3.39-MariaDB-1:10.3.39+maria~ubu2004'
mysqld: ready for connections
```

Updated execution matrix:

| Check | Result | Notes |
| --- | --- | --- |
| Installer boots | Passed | `admin/install.php` returned HTTP 200 over localhost-only binding. |
| Admin panel loads | Not executed | Requires installer submission and generated configuration. |
| Database initialization works | Not executed | Installer form has not been submitted. |
| Uploads function | Not executed | Requires completed install. |
| Thumbnail generation functions | Not executed | Requires completed install and test image upload. |
| EXIF extraction functions | Not executed | Requires completed install and EXIF fixture upload. |
| Runtime warnings/errors | Partially captured | `ereg_replace()` deprecations and Apache `ServerName` warning recorded. |

Current status:

First non-destructive runtime boot succeeded. The next step is a controlled installer submission inside the disposable workspace and isolated database.

## 2026-05-30 Installer Submission Attempts

The installer was submitted through Pixelpost's own historical form flow inside disposable workspaces. No Pixelpost source files were patched.

Common test values:

- Database host: `pixelpost-db`
- Database name: `pixelpost`
- Database user: `pixelpost`
- Table prefix: `pixelpost_`
- Admin user: `archivist`
- Site URL: `http://127.0.0.1:18080/`

### MariaDB 10.3

Result:

- Requirements page returned HTTP 200.
- Database credential test returned HTTP 200.
- Administrator validation returned HTTP 200.
- Settings validation returned HTTP 200.
- Configuration step returned HTTP 200 and wrote `includes/pixelpost.php`.
- Finalize returned HTTP 200 but halted during schema creation.

Created tables before failure:

```text
pixelpost_categories
pixelpost_comments
pixelpost_config
pixelpost_pixelpost
pixelpost_visitors
```

Failure:

```text
MySQL Error: Too big precision 14 specified for 'upgrade_date'. Maximum is 6
```

Source location:

```text
includes/create_tables.php:126
`upgrade_date` TIMESTAMP(14) NOT NULL
```

### MySQL 5.5

Official `mysql:5.0` and `mysql:5.1` images were unavailable:

```text
docker.io/library/mysql:5.0: not found
docker.io/library/mysql:5.1: not found
```

The `mysql:5.5` image was available and tested.

Result:

- Configuration writing succeeded.
- Initial tables were created.
- Version table was not created.
- Admin URL returned HTTP 302 after the partial install.

Failure:

```text
MySQL Error: You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near '(14) NOT NULL,
                 `version` FLOAT NOT NULL DEFAULT '0',
```

Database version:

```text
5.5.62
```

### MariaDB 5.5

The `mariadb:5.5` image was available and tested.

Result:

- Requirements, database, administrator, settings, configuration, and finalize requests each returned HTTP 200.
- Configuration step reported: `Your configuration has been successfully created and saved. All tests have passed!`
- `includes/pixelpost.php` was generated in the disposable workspace.
- Initial tables were created.
- Version table was not created.
- Admin URL returned HTTP 302 after the partial install.

Created tables:

```text
pixelpost_categories
pixelpost_comments
pixelpost_config
pixelpost_pixelpost
pixelpost_visitors
```

Counts:

```text
pixelpost_config: 1
pixelpost_categories: 1
pixelpost_pixelpost: 0
```

Failure:

```text
MySQL Error: Too big precision 14 specified for 'upgrade_date'. Maximum is 6.
```

Database version:

```text
5.5.64-MariaDB-1~trusty
```

### MariaDB 5.5 With MAXDB SQL Mode

The lab was reset and rerun with MariaDB 5.5 using:

```text
--sql-mode=MAXDB,NO_ENGINE_SUBSTITUTION
```

The active mode was verified:

```text
PIPES_AS_CONCAT,ANSI_QUOTES,IGNORE_SPACE,MAXDB,NO_KEY_OPTIONS,NO_TABLE_OPTIONS,NO_FIELD_OPTIONS,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION
```

Result:

- Installer launch passed.
- Configuration generation passed.
- Full database finalization failed at the same version-table line.

Failure:

```text
MySQL Error: Too big precision 14 specified for 'upgrade_date'. Maximum is 6.
```

Conclusion:

MariaDB 5.5's MAXDB mode does not provide sufficient compatibility for Pixelpost's `TIMESTAMP(14)` schema.

### Current Runtime Conclusion

Pixelpost 1.7.3 installer boot and configuration generation work in the isolated lab. Full database initialization does not complete on MariaDB 10.3, MySQL 5.5, or MariaDB 5.5 because the historical schema uses `TIMESTAMP(14)`.

Next restoration options:

- Build or locate a more historically authentic MySQL 4.1/5.0 runtime.
- Document a future minimal compatibility shim for `TIMESTAMP(14)` after preservation review.
- Keep the current source tree untouched until the compatibility doctrine is approved.
