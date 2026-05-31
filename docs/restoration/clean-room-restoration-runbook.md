# Pixelpost 1.7.3 Clean-Room Restoration Runbook

Question: Can a second operator reproduce this restoration from documented instructions alone?

Answer: yes, if they have the listed artifacts and Docker images. This runbook describes the repeatable lab path verified in Phase 5.

## Required Artifacts

| Artifact | Purpose | Required Value |
| --- | --- | --- |
| Pixelpost 1.7.3 source tree | Application specimen | Read-only source copied into disposable workspaces |
| Raw source archive hash | Provenance check | `0553abce0a647ff226d117de0893f903697910761aabf680fad5ce3ed693d98a` |
| Extracted source tree hash | Integrity check | `8498093b0f50c9f03cf56191cec1b9fb4f52649aac9451abf85682c6424bd05b` |
| PHP runtime image | Web/runtime execution | `pixelpost-restoration-lab-pixelpost-php`, PHP `5.6.40` |
| MySQL runtime image | Historical database runtime | `ggmartinez/mysql:5.1`, digest `sha256:db6468ed7a662a0efd5aee985b9e5a0c5b6c43732bc22c72a950624ba3349ba2` |
| EXIF JPEG fixture | Upload/thumbnail/EXIF validation | `test-image-exif-320x240.jpg` |

The PHP runtime image must provide:

- PHP `5.6.40`
- legacy `mysql` extension
- GD
- EXIF support
- Apache

## Directory Layout

Create or verify:

```text
/opt/pixelpost-restoration-lab
/opt/pixelpost-restoration-lab/archive-readonly/pixelpost-1.7.3
/opt/pixelpost-restoration-lab/workspaces
/opt/pixelpost-restoration-lab/db
/opt/pixelpost-restoration-lab/reports
```

The source specimen remains read-only under `archive-readonly`. Runtime work uses a disposable copy under `workspaces`.

## Clean Workspace

```text
LAB=/opt/pixelpost-restoration-lab
ARCHIVE="$LAB/archive-readonly/pixelpost-1.7.3"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
LABEL="repeat-173-$STAMP"
RUN="$LAB/reports/$LABEL"
WS="$LAB/workspaces/$LABEL"
DBDIR="$LAB/db/$LABEL"
NET="pp-$LABEL-net"
DB="pp-$LABEL-db"
PHP="pp-$LABEL-php"
TEST_IMAGE="$LAB/reports/phase5-test-image-exif-320x240.jpg"

mkdir -p "$RUN" "$WS" "$DBDIR"
cp -a "$ARCHIVE/." "$WS/"
chown -R 33:33 "$WS"
chmod -R u+rwX,go-rwx "$WS"
```

Expected checkpoint:

```text
SOURCE_TREE_SHA256=8498093b0f50c9f03cf56191cec1b9fb4f52649aac9451abf85682c6424bd05b
```

## Isolated Runtime

```text
docker network create --internal "$NET"
docker run -d --name "$DB" --network "$NET" --network-alias db ggmartinez/mysql:5.1
```

Wait for database readiness:

```text
for i in $(seq 1 60); do
  if docker exec "$DB" mysql -uroot -e 'SELECT 1' >/dev/null 2>&1; then break; fi
  sleep 2
done
```

Create the disposable test database:

```text
docker exec "$DB" mysql -uroot -e "CREATE DATABASE IF NOT EXISTS pixelpost; GRANT ALL PRIVILEGES ON pixelpost.* TO 'pixelpost'@'%' IDENTIFIED BY 'pixelpostpass'; GRANT ALL PRIVILEGES ON pixelpost.* TO 'pixelpost'@'localhost' IDENTIFIED BY 'pixelpostpass'; FLUSH PRIVILEGES;"
```

Expected checkpoint:

```text
SELECT VERSION() AS version;
5.1.73
```

## Install Pixelpost

Generate `includes/pixelpost.php` only inside the disposable workspace copy. Then execute Pixelpost's original installer schema/store routines through PHP.

Expected install-runner outcome:

```text
installed_version_after_schema=1.73
installed_version_after_store_vars=1.73
tables=pixelpost_addons,pixelpost_catassoc,pixelpost_categories,pixelpost_comments,pixelpost_config,pixelpost_pixelpost,pixelpost_tags,pixelpost_version,pixelpost_visitors
```

Expected version rows:

```text
1.4
1.41
1.49995
1.59
1.6
1.7
1.71
1.72
1.73
```

Historical warnings are expected and not blocking:

```text
mysql_connect(): The mysql extension is deprecated
Function ereg_replace() is deprecated
Function eregi_replace() is deprecated
```

## Start HTTP Runtime

```text
docker run -d --name "$PHP" --network "$NET" --network-alias web -v "$WS:/var/www/html" pixelpost-restoration-lab-pixelpost-php
PHP_IP=$(docker inspect "$PHP" --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}')
BASE="http://$PHP_IP"
```

Expected checkpoint:

```text
curl -sS "$BASE/" >/dev/null
```

## Validate Admin Login

```text
curl -sS -c "$RUN/cookies.txt" -b "$RUN/cookies.txt" \
  -d 'user=repeatadmin&password=repeatability-pass' \
  "$BASE/admin/index.php?x=login" \
  -o "$RUN/admin-login.html"
```

Pass checkpoint:

```text
admin-login.html contains New Image
```

## Validate Upload

```text
curl -sS -c "$RUN/cookies.txt" -b "$RUN/cookies.txt" \
  -F "userfile=@$TEST_IMAGE;type=image/jpeg" \
  -F 'headline=Phase 5 Repeatability Pass' \
  -F 'tags=phase5, repeatability, exif' \
  -F 'body=Clean repeatability workflow upload.' \
  -F 'category[]=1' \
  -F 'autodate=0' \
  -F 'post_year=2026' \
  -F 'post_month=05' \
  -F 'post_day=31' \
  -F 'post_hour=03' \
  -F 'post_minute=05' \
  -F 'allow_comments=A' \
  "$BASE/admin/index.php?x=save" \
  -o "$RUN/upload-response.html"
```

Pass checkpoint:

```text
POSTED: Phase 5 Repeatability Pass
```

## Validate Public Rendering

```text
curl -sS "$BASE/" -o "$RUN/public-image.html"
curl -sS "$BASE/index.php?x=browse" -o "$RUN/archive.html"
curl -sS "$BASE/index.php?x=browse&category=1" -o "$RUN/category.html"
curl -sS -b "$RUN/cookies.txt" "$BASE/admin/index.php?view=images" -o "$RUN/admin-images.html"
```

Pass checkpoints:

```text
public-image.html contains Phase 5 Repeatability Pass
public-image.html contains RestorationCam 173
public-image.html contains 1/125 sec
public-image.html contains f/5.6
public-image.html contains Flash: Not Fired
archive.html contains thumbnails/thumb_
category.html contains thumbnails/thumb_
admin-images.html contains Phase 5 Repeatability Pass
```

## Validate Files

Expected:

```text
images/<uploaded-file>.jpg 5970 bytes
thumbnails/thumb_<uploaded-file>.jpg 1195 bytes
```

Expected dimensions:

```text
images/<uploaded-file>.jpg 320x240
thumbnails/thumb_<uploaded-file>.jpg 100x75
```

## Export Test Database

Schema-only:

```text
docker exec "$DB" mysqldump -uroot --no-data pixelpost > "$RUN/pixelpost-repeatability-schema.sql"
```

Full test dump:

```text
docker exec "$DB" mysqldump -uroot pixelpost > "$RUN/pixelpost-repeatability.sql"
```

## Cleanup

After evidence is captured:

```text
docker rm -f "$PHP" "$DB"
docker network rm "$NET"
```

The disposable workspace and report directory may be retained as evidence or deleted after checksums and logs are preserved.

## Result

A second operator can reproduce the restoration from documented instructions if they have the source specimen, the two runtime images, and the EXIF test JPEG.
