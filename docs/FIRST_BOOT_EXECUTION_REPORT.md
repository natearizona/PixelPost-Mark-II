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

The scaffold targets Apache, PHP 5.6, PHP `mysql`/`mysqli`/`gd`/`exif` extensions, and MariaDB 10.3 with strict SQL mode disabled.

Local verification performed:

```text
tools/reset-first-boot-workspace.sh 1.7.3
reset .../docker/restoration-workspaces/pixelpost-1.7.3-first-boot from .../archive/original-pixelpost/extracted/pixelpost-1.7.3

sh -n tools/reset-first-boot-workspace.sh
bash -n tools/reset-first-boot-workspace.sh
```

The reset helper passed shell syntax validation and successfully recreated a disposable Pixelpost 1.7.3 first-boot workspace. Docker execution remains untested in this shell because no container runtime is currently available.
