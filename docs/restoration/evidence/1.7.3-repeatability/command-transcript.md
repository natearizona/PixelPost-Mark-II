# Pixelpost 1.7.3 Phase 5 Repeatability Command Transcript

Date: 2026-05-31 America/Phoenix / 2026-05-31 UTC

Target: VPS #1, `/opt/pixelpost-restoration-lab`

## Artifact Transfer

The controlled EXIF JPEG from Phase 4 was copied to the VPS for repeatability testing:

```text
scp docs/restoration/evidence/1.7.3-browser-validation/test-image-exif-320x240.jpg root@2.24.122.151:/opt/pixelpost-restoration-lab/reports/phase5-test-image-exif-320x240.jpg
```

## Repeatability Harness

The repeatability harness was copied and executed:

```text
scp /private/tmp/phase5-repeatability.sh root@2.24.122.151:/opt/pixelpost-restoration-lab/reports/phase5-repeatability.sh
ssh -o BatchMode=yes root@2.24.122.151 'chmod +x /opt/pixelpost-restoration-lab/reports/phase5-repeatability.sh; /opt/pixelpost-restoration-lab/reports/phase5-repeatability.sh'
```

The harness created:

```text
RUN_DIR=/opt/pixelpost-restoration-lab/reports/repeat-173-20260531T172345Z
WORKSPACE=/opt/pixelpost-restoration-lab/workspaces/repeat-173-20260531T172345Z
DBDIR=/opt/pixelpost-restoration-lab/db/repeat-173-20260531T172345Z
NETWORK=pp-repeat-173-20260531T172345Z-net
DB_CONTAINER=pp-repeat-173-20260531T172345Z-db
PHP_CONTAINER=pp-repeat-173-20260531T172345Z-php
```

## Evidence Collection

Evidence copied back:

```text
scp root@2.24.122.151:/opt/pixelpost-restoration-lab/reports/repeat-173-20260531T172345Z/lab-env.txt docs/restoration/evidence/1.7.3-repeatability/lab-env.txt
scp root@2.24.122.151:/opt/pixelpost-restoration-lab/reports/repeat-173-20260531T172345Z/install-runner.log docs/restoration/evidence/1.7.3-repeatability/install-runner.log
scp root@2.24.122.151:/opt/pixelpost-restoration-lab/reports/repeat-173-20260531T172345Z/runtime-evidence.txt docs/restoration/evidence/1.7.3-repeatability/runtime-evidence.txt
scp root@2.24.122.151:/opt/pixelpost-restoration-lab/reports/repeat-173-20260531T172345Z/upload-response.html docs/restoration/evidence/1.7.3-repeatability/upload-response.html
scp root@2.24.122.151:/opt/pixelpost-restoration-lab/reports/repeat-173-20260531T172345Z/public-image.html docs/restoration/evidence/1.7.3-repeatability/public-image.html
scp root@2.24.122.151:/opt/pixelpost-restoration-lab/reports/repeat-173-20260531T172345Z/archive.html docs/restoration/evidence/1.7.3-repeatability/archive.html
scp root@2.24.122.151:/opt/pixelpost-restoration-lab/reports/repeat-173-20260531T172345Z/category.html docs/restoration/evidence/1.7.3-repeatability/category.html
scp root@2.24.122.151:/opt/pixelpost-restoration-lab/reports/repeat-173-20260531T172345Z/admin-images.html docs/restoration/evidence/1.7.3-repeatability/admin-images.html
scp root@2.24.122.151:/opt/pixelpost-restoration-lab/reports/repeat-173-20260531T172345Z/mysqldump.stderr docs/restoration/evidence/1.7.3-repeatability/mysqldump.stderr
```

Schema-only dump:

```text
ssh -o BatchMode=yes root@2.24.122.151 'docker exec pp-repeat-173-20260531T172345Z-db mysqldump -uroot --no-data pixelpost' > docs/restoration/evidence/1.7.3-repeatability/pixelpost-repeatability-schema.sql
```

## Notes

The full test SQL dump was generated on the VPS as:

```text
/opt/pixelpost-restoration-lab/reports/repeat-173-20260531T172345Z/pixelpost-repeatability.sql
```

It was not committed because it is runtime debris from a test install and contains generated administrative test data.
