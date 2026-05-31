# Pixelpost 1.7.3 Browser Validation Command Transcript

Date: 2026-05-30 America/Phoenix / 2026-05-31 UTC

Target: VPS #1, `/opt/pixelpost-restoration-lab`

## Isolation

- PHP and MySQL containers ran on `pp-browser-validation-net`, a Docker network created with `--internal`.
- No public DNS was used.
- No Traefik labels or routing were used.
- No firewall rules were changed.
- HTTP was accessed through an SSH tunnel from the local browser to the PHP container's private Docker bridge address.
- Pixelpost ran from a disposable workspace copy.
- The archive specimen remained read-only.

## Lab Workspace Creation

```text
LAB=/opt/pixelpost-restoration-lab
STAMP=20260531T021851Z
RUN=$LAB/reports/browser-validation-1.7.3-$STAMP
WS=$LAB/workspaces/browser-validation-1.7.3-$STAMP
DBDIR=$LAB/db/browser-validation-1.7.3-$STAMP
mkdir -p "$RUN" "$WS" "$DBDIR"
cp -a "$LAB/archive-readonly/pixelpost-1.7.3/." "$WS/"
chown -R 33:33 "$WS"
chmod -R u+rwX,go-rwx "$WS"
```

## Containers

```text
docker network create --internal pp-browser-validation-net
docker run -d --name pp-browser-db --network pp-browser-validation-net --network-alias db ggmartinez/mysql:5.1
docker exec pp-browser-db mysql -uroot -e "CREATE DATABASE IF NOT EXISTS pixelpost; GRANT ALL PRIVILEGES ON pixelpost.* TO 'pixelpost'@'%' IDENTIFIED BY 'pixelpostpass'; GRANT ALL PRIVILEGES ON pixelpost.* TO 'pixelpost'@'localhost' IDENTIFIED BY 'pixelpostpass'; FLUSH PRIVILEGES;"
docker run -d --name pp-browser-php --network pp-browser-validation-net --network-alias web -v "$WS:/var/www/html" pixelpost-restoration-lab-pixelpost-php
```

Docker did not publish `pp-browser-php` because the container was attached only to an internal network. Browser access used the container-private IP:

```text
ssh -o ServerAliveInterval=30 -o ServerAliveCountMax=3 -N -L 18082:172.16.9.3:80 root@2.24.122.151
```

Local test URL:

```text
http://127.0.0.1:18082/
```

## Installer Browser Flow

The browser visited:

```text
http://127.0.0.1:18082/admin/install.php?view=install&cat=introduction
```

Installer values:

```text
db_host=db
db_name=pixelpost
db_user=pixelpost
db_pass=pixelpostpass
tbl_prefix=pixelpost_
admin_username=archivist
admin_password=pixelpost-test-pass
admin_email=archivist@example.invalid
pp_title=Pixelpost Restoration Lab
pp_sub_title=Phase 4 Browser Validation
pp_path=http://127.0.0.1:18082/
```

The installer generated `includes/pixelpost.php` inside the disposable workspace copy.

## Upload Commands

Browser automation verified admin login and pages. Because the in-app browser API did not expose file input upload in this session, multipart upload was performed through the same localhost SSH tunnel with an authenticated cookie jar.

Login:

```text
curl -sS -c /private/tmp/pixelpost-cookies.txt -b /private/tmp/pixelpost-cookies.txt -d 'user=archivist&password=pixelpost-test-pass' 'http://127.0.0.1:18082/admin/index.php?x=login' -o /private/tmp/pixelpost-login-result.html
```

Initial 1x1 EXIF JPEG upload:

```text
curl -sS -c /private/tmp/pixelpost-cookies.txt -b /private/tmp/pixelpost-cookies.txt -F 'userfile=@docs/restoration/evidence/1.7.3-browser-validation/test-image-exif.jpg;type=image/jpeg' -F 'headline=Phase 4 EXIF Test' -F 'tags=phase4, exif, restoration' -F 'body=Pixelpost Restoration Lab upload workflow test.' -F 'category[]=1' -F 'autodate=0' -F 'post_year=2026' -F 'post_month=05' -F 'post_day=31' -F 'post_hour=02' -F 'post_minute=31' -F 'allow_comments=A' 'http://127.0.0.1:18082/admin/index.php?x=save' -o docs/restoration/evidence/1.7.3-browser-validation/upload-response.html
```

Realistic 320x240 EXIF JPEG upload:

```text
curl -sS -c /private/tmp/pixelpost-cookies.txt -b /private/tmp/pixelpost-cookies.txt -F 'userfile=@docs/restoration/evidence/1.7.3-browser-validation/test-image-exif-320x240.jpg;type=image/jpeg' -F 'headline=Phase 4 EXIF Workflow Pass' -F 'tags=phase4, exif, thumbnail' -F 'body=Pixelpost Restoration Lab end-to-end workflow test.' -F 'category[]=1' -F 'autodate=0' -F 'post_year=2026' -F 'post_month=05' -F 'post_day=31' -F 'post_hour=02' -F 'post_minute=35' -F 'allow_comments=A' 'http://127.0.0.1:18082/admin/index.php?x=save' -o docs/restoration/evidence/1.7.3-browser-validation/upload-response-320x240.html
```

## Evidence Files

- `lab-env.txt`
- `docker-ps.txt`
- `runtime-evidence-final.txt`
- `upload-response.html`
- `upload-response-320x240.html`
- `test-image-exif.jpg`
- `test-image-exif-320x240.jpg`
- `screenshots/`
