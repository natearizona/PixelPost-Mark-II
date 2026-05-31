# Pixelpost 1.7.3 Repeatability Validation

Question: Was the restoration reproducible?

Answer: yes. Phase 5 repeated the restoration from a fresh disposable workspace, fresh database, fresh internal Docker network, and fresh admin account. The run reached installer version `1.73`, then completed admin login, upload, thumbnail generation, EXIF extraction, and public theme rendering.

## Run Identity

- Report directory: `/opt/pixelpost-restoration-lab/reports/repeat-173-20260531T172345Z`
- Workspace: `/opt/pixelpost-restoration-lab/workspaces/repeat-173-20260531T172345Z`
- Database directory: `/opt/pixelpost-restoration-lab/db/repeat-173-20260531T172345Z`
- Network: `pp-repeat-173-20260531T172345Z-net`
- DB container: `pp-repeat-173-20260531T172345Z-db`
- PHP container: `pp-repeat-173-20260531T172345Z-php`

Source:

```text
SOURCE_TREE_SHA256=8498093b0f50c9f03cf56191cec1b9fb4f52649aac9451abf85682c6424bd05b
RAW_ARCHIVE_SHA256=0553abce0a647ff226d117de0893f903697910761aabf680fad5ce3ed693d98a
```

Images:

```text
MYSQL_IMAGE=sha256:db6468ed7a662a0efd5aee985b9e5a0c5b6c43732bc22c72a950624ba3349ba2
PHP_IMAGE=sha256:c2c3ea3fcfdfc3ec9c94c63825dce2a188be427b2941144f930dc150008d7578
```

## Pass/Fail Matrix

| Checkpoint | Result | Evidence |
| --- | --- | --- |
| Fresh disposable workspace created | Pass | `lab-env.txt` |
| Fresh internal Docker network created | Pass | `lab-env.txt` |
| Fresh MySQL 5.1.73 database created | Pass | `runtime-evidence.txt` |
| Installer schema reaches `1.73` | Pass | `install-runner.log` |
| Admin account created | Pass | `runtime-evidence.txt` |
| Admin login works | Pass | `admin-images.html` |
| Upload succeeds | Pass | `upload-response.html` |
| Database image row created | Pass | `runtime-evidence.txt` |
| Image file stored | Pass | `runtime-evidence.txt` |
| Thumbnail generated | Pass | `runtime-evidence.txt` |
| EXIF extracted | Pass | `runtime-evidence.txt` |
| Public image page renders | Pass | `public-image.html` |
| Archive page renders | Pass | `archive.html` |
| Category page renders | Pass | `category.html` |
| SQL dump export works | Pass | `MYSQLDUMP_OK=1` |

## Installer Evidence

```text
installed_version_after_schema=1.73
installed_version_after_store_vars=1.73
```

Version rows:

```text
1|2026-05-31 17:23:48|1.4
2|2026-05-31 17:23:48|1.41
3|2026-05-31 17:23:48|1.49995
4|2026-05-31 17:23:48|1.59
5|2026-05-31 17:23:48|1.6
6|2026-05-31 17:23:48|1.7
7|2026-05-31 17:23:48|1.71
8|2026-05-31 17:23:48|1.72
9|2026-05-31 17:23:48|1.73
```

## Workflow Evidence

Database image row:

```text
id: 1
datetime: 2026-05-31 03:05:50
headline: Phase 5 Repeatability Pass
image: 20260531172350_phase5-test-image-exif-320x240.jpg
exif_len: 740
```

Files:

```text
images/20260531172350_phase5-test-image-exif-320x240.jpg 5970 bytes
thumbnails/thumb_20260531172350_phase5-test-image-exif-320x240.jpg 1195 bytes
```

Dimensions:

```text
images/20260531172350_phase5-test-image-exif-320x240.jpg 320x240
thumbnails/thumb_20260531172350_phase5-test-image-exif-320x240.jpg 100x75
```

EXIF:

```text
MakeIFD0=PixelPost Lab
ModelIFD0=RestorationCam 173
ExposureTimeSubIFD=1/125 sec
FNumberSubIFD=f 5.6
DateTimeOriginalSubIFD=2008:01:16 19:24:38
FlashSubIFD=No Flash
FocalLengthSubIFD=35 mm
ISOSpeedRatingsSubIFD=200
```

Public render checks:

```text
Phase 5 Repeatability Pass
RestorationCam 173
1/125 sec
f/5.6
Flash: Not Fired
```

Archive/category checks:

```text
archive.html contains thumbnails/thumb_20260531172350_phase5-test-image-exif-320x240.jpg
category.html contains thumbnails/thumb_20260531172350_phase5-test-image-exif-320x240.jpg
```

## Expected Warnings

PHP warnings remain but did not block restoration:

```text
mysql_connect(): The mysql extension is deprecated
Function ereg_replace() is deprecated
Function eregi_replace() is deprecated
Undefined variable: admin_user
```

The `admin_user` notice affects only the final credential display in the scripted install runner. The database confirms the admin account was created as `repeatadmin`.

## Evidence

- `docs/restoration/evidence/1.7.3-repeatability/lab-env.txt`
- `docs/restoration/evidence/1.7.3-repeatability/install-runner.log`
- `docs/restoration/evidence/1.7.3-repeatability/runtime-evidence.txt`
- `docs/restoration/evidence/1.7.3-repeatability/upload-response.html`
- `docs/restoration/evidence/1.7.3-repeatability/public-image.html`
- `docs/restoration/evidence/1.7.3-repeatability/archive.html`
- `docs/restoration/evidence/1.7.3-repeatability/category.html`
- `docs/restoration/evidence/1.7.3-repeatability/admin-images.html`
- `docs/restoration/evidence/1.7.3-repeatability/pixelpost-repeatability-schema.sql`

## Result

The restoration is reproducible. A fresh run using the verified historical runtime completed the same core workflow without source modification.
