# PixelPost Restoration Lab

## Mission

Determine how Pixelpost worked by making recovered releases execute in safe, isolated, reproducible containers.

## Operating Question

Every lab artifact must answer:

```text
Can we make this run?
```

## Lab Boundary

PixelPost Archaeology determines what is historically true.

PixelPost Restoration Lab determines what can be executed, repaired, migrated, or reproduced in a safe container.

The lab is technical. It is not a historical essay track.

## Allowed Work

- Docker and Docker Compose environments.
- PHP compatibility testing.
- Runtime restoration.
- Database migration experiments.
- Theme recovery for executable installs.
- Legacy installer testing.
- Container builds and runtime scripts.
- Error capture, reproduction steps, and pass/fail reports.

## Forbidden Work

- Manifestos.
- Historical speculation.
- Contributor biographies.
- Non-executable cultural commentary.
- Modern feature design unrelated to booting, restoring, migrating, or reproducing Pixelpost.

## Documentation Rule

Every document, commit, test, or report in the Restoration Lab must directly support one or more of these outcomes:

- installer launches,
- configuration can be generated,
- database initializes or migrates,
- admin panel loads,
- image upload works,
- thumbnails generate,
- EXIF extraction works,
- themes render,
- archived installs can be reproduced,
- failures are captured precisely enough to reproduce.

## Commit Rule

Restoration Lab commits should be technical and execution-oriented.

Good commit subjects:

- `Add PHP 5.2 runtime candidate`
- `Document MySQL 4.1 install failure`
- `Add first-boot runbook for Pixelpost 1.7.3`
- `Capture thumbnail generation failure`

Avoid commit subjects that do not describe runnable work or test evidence.

## Testing Rule

Runtime testing must remain isolated:

- no public DNS,
- no Traefik routing,
- no production WordPress VPS,
- no shared databases,
- no shared app networks,
- localhost-only or SSH tunnel access,
- disposable workspace copies only,
- untouched archives remain read-only.

## Current Technical Focus

The immediate Restoration Lab focus is Pixelpost 1.7.3 first boot:

1. identify a runtime that can execute the legacy installer,
2. determine the earliest database version that accepts the schema chain,
3. confirm whether admin login can load,
4. confirm whether image upload creates database rows and files,
5. confirm whether thumbnail generation works,
6. confirm whether EXIF extraction works,
7. document exact failures when any step fails.

## Success Definition

A restoration milestone is successful when it produces reproducible technical evidence:

- container definition,
- exact command sequence,
- exact release under test,
- observed runtime versions,
- pass/fail result,
- logs or screenshots when relevant,
- next executable blocker.
