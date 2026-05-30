# PixelPost Restoration Lab Status

## Current Status

Phase 0 VPS audit is complete.

Docker readiness is confirmed on VPS #1.

PixelPost Restoration Lab has been created on VPS #1 and is running as an isolated Docker Compose project.

Pixelpost 1.7.3 boots to the installer over a localhost-only binding. Installer submission has been tested in disposable workspaces; configuration generation works, but full database initialization currently stops at the historical `TIMESTAMP(14)` schema definition.

## Target VPS

```text
Host/IP: 2.24.122.151
Hostname: srv1697587
User observed: root
Kernel: Linux 6.8.0-117-generic x86_64
```

## Proposed Lab Path

```text
/opt/pixelpost-restoration-lab
```

Created lab directories:

```text
/opt/pixelpost-restoration-lab
/opt/pixelpost-restoration-lab/archive-readonly
/opt/pixelpost-restoration-lab/workspaces
/opt/pixelpost-restoration-lab/docker
/opt/pixelpost-restoration-lab/db
/opt/pixelpost-restoration-lab/logs
/opt/pixelpost-restoration-lab/reports
```

The directory tree was created as `root:root` with mode `750`.

## Containers Created

- `pixelpost-php`
- `pixelpost-db`

Observed status after first successful start:

```text
pixelpost-php   Up   127.0.0.1:18080->80/tcp
pixelpost-db    Up   3306/tcp, healthy
```

Current database image after compatibility trials:

```text
mariadb:5.5
```

## Network Created

```text
pixelpost-lab-net
```

Observed network membership:

```text
pixelpost-php pixelpost-db
```

## Proposed Access

SSH tunnel only:

```bash
ssh -L 18080:127.0.0.1:18080 root@2.24.122.151
```

Browser:

```text
http://127.0.0.1:18080/admin/install.php
```

Observed VPS-side installer check:

```text
HTTP 200
```

The first visible runtime warning was:

```text
Deprecated: Function ereg_replace() is deprecated in /var/www/html/admin/install/install_functions.php on line 358
```

Additional `ereg_replace()` deprecation warnings appeared while rendering the language selector.

Installer submission findings:

```text
Configuration generation: passed
Initial database table creation: partial
Admin panel load: blocked by incomplete version table
Upload/thumbnail/EXIF tests: blocked pending complete install
```

The blocking schema error is:

```text
MySQL Error: Too big precision 14 specified for 'upgrade_date'. Maximum is 6.
```

The relevant historical source line is:

```text
includes/create_tables.php:126
`upgrade_date` TIMESTAMP(14) NOT NULL
```

## Conflicts Avoided By Design

- OpenClaw: no shared network, volume, mount, or route.
- Hermes: no shared `/opt/hermes-uap`, network, or ports.
- MemPalace: no shared network or volume.
- Traefik: no labels, routing, or network integration.
- Telegram services: no shared configuration, secrets, or network.
- WordPress: no WordPress VPS or production site paths used.

Observed controls:

```text
traefik.enable=false
127.0.0.1:18080 only
no public DNS
no firewall changes
no Traefik network membership
```

Final isolation check:

```text
pixelpost-php   127.0.0.1:18080->80/tcp
pixelpost-db    mariadb:5.5, healthy, no host port
pixelpost-lab-net members: pixelpost-php pixelpost-db
archive-readonly specimen: root:root, read-only
```

## Remote Write Gate

Remote write operations were performed only after stating the intended action, risk, and rollback path in the thread.

## Exact Commands Executed So Far

```bash
ssh -o BatchMode=yes -o ConnectTimeout=8 root@uap.turquoiseufo.tech 'hostname; whoami; uname -a'
ssh-keygen -F uap.turquoiseufo.tech -f ~/.ssh/known_hosts
ssh-keygen -F 2.24.122.151 -f ~/.ssh/known_hosts
dig +short uap.turquoiseufo.tech A
ssh -o BatchMode=yes -o ConnectTimeout=8 root@2.24.122.151 'hostname; whoami; uname -a'
ssh -o BatchMode=yes root@2.24.122.151 'set -u; ... Phase 0 audit commands ...'
ssh -o BatchMode=yes root@2.24.122.151 'set -u; ... Traefik label and docker stats commands ...'
ssh -o BatchMode=yes root@2.24.122.151 'set -euo pipefail; mkdir -p /opt/pixelpost-restoration-lab/{archive-readonly,workspaces,docker,db,logs,reports}; chown -R root:root /opt/pixelpost-restoration-lab; chmod 750 /opt/pixelpost-restoration-lab /opt/pixelpost-restoration-lab/{archive-readonly,workspaces,docker,db,logs,reports}; find /opt/pixelpost-restoration-lab -maxdepth 2 -type d -printf "%M %u:%g %p\n" | sort'
scp docker/pixelpost-restoration-lab.compose.yml root@2.24.122.151:/opt/pixelpost-restoration-lab/docker/docker-compose.yml
scp -r docker/historical/php56-apache root@2.24.122.151:/opt/pixelpost-restoration-lab/docker/
ssh -o BatchMode=yes root@2.24.122.151 'set -euo pipefail; cd /opt/pixelpost-restoration-lab/docker; docker compose -f docker-compose.yml config --quiet; find /opt/pixelpost-restoration-lab/docker -maxdepth 3 -type f -printf "%M %u:%g %p\n" | sort'
scp -r archive/original-pixelpost/extracted/pixelpost-1.7.3 root@2.24.122.151:/opt/pixelpost-restoration-lab/archive-readonly/
ssh -o BatchMode=yes root@2.24.122.151 'set -euo pipefail; chmod -R a-w /opt/pixelpost-restoration-lab/archive-readonly/pixelpost-1.7.3; cp -a /opt/pixelpost-restoration-lab/archive-readonly/pixelpost-1.7.3 /opt/pixelpost-restoration-lab/workspaces/pixelpost-1.7.3-first-boot; chown -R 33:33 /opt/pixelpost-restoration-lab/workspaces/pixelpost-1.7.3-first-boot; chmod -R u+rwX,go-rwx /opt/pixelpost-restoration-lab/workspaces/pixelpost-1.7.3-first-boot'
scp docker/historical/php56-apache/Dockerfile root@2.24.122.151:/opt/pixelpost-restoration-lab/docker/php56-apache/Dockerfile
ssh -o BatchMode=yes root@2.24.122.151 'set -euo pipefail; cd /opt/pixelpost-restoration-lab/docker; docker compose -p pixelpost-restoration-lab -f docker-compose.yml up -d --build; docker ps --filter label=com.docker.compose.project=pixelpost-restoration-lab --format "table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}"; docker network ls --filter name=pixelpost-lab-net; ss -tulpen | grep -E "18080|pixelpost" || true'
ssh -o BatchMode=yes root@2.24.122.151 'set -euo pipefail; docker ps --filter label=com.docker.compose.project=pixelpost-restoration-lab --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"; docker inspect pixelpost-php --format "{{json .Config.Labels}}"; docker network inspect pixelpost-lab-net --format "{{range .Containers}}{{.Name}} {{end}}"; ss -tulpen | grep 18080; curl -sS -o /tmp/pixelpost-install.html -w "%{http_code}\n" http://127.0.0.1:18080/admin/install.php; sed -n "1,40p" /tmp/pixelpost-install.html; docker logs --tail 80 pixelpost-php 2>&1; docker logs --tail 40 pixelpost-db 2>&1'
ssh -o BatchMode=yes root@2.24.122.151 '... submit installer form flow against MariaDB 10.3 and inspect generated tables/errors ...'
ssh -o BatchMode=yes root@2.24.122.151 'docker pull mysql:5.0'
ssh -o BatchMode=yes root@2.24.122.151 'docker pull mysql:5.1'
ssh -o BatchMode=yes root@2.24.122.151 'docker pull mariadb:5.5'
scp docker/pixelpost-restoration-lab.compose.yml root@2.24.122.151:/opt/pixelpost-restoration-lab/docker/docker-compose.yml
ssh -o BatchMode=yes root@2.24.122.151 '... reset disposable workspace/database and test installer flow against mysql:5.5 ...'
ssh -o BatchMode=yes root@2.24.122.151 '... reset disposable workspace/database and test installer flow against mariadb:5.5 ...'
ssh -o BatchMode=yes root@2.24.122.151 'set -euo pipefail; docker ps --filter label=com.docker.compose.project=pixelpost-restoration-lab --format "table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}"; docker inspect pixelpost-php --format "{{json .Config.Labels}}"; docker network inspect pixelpost-lab-net --format "{{range .Containers}}{{.Name}} {{end}}"; ss -tulpen | grep 18080; find /opt/pixelpost-restoration-lab/archive-readonly/pixelpost-1.7.3 -maxdepth 1 -printf "%M %u:%g %p\n" | sort | head -8'
```

Notes:

- Hostname SSH check failed at host-key verification.
- IP SSH check succeeded using existing known-host data.
- `dig` failed locally due sandbox bind restrictions; DNS was not required after successful IP SSH.

## Estimated Path To Next Runtime Milestone

1. Open an SSH tunnel to `127.0.0.1:18080`.
2. Build or locate a MySQL 4.1/5.0-compatible runtime that accepts `TIMESTAMP(14)`, or approve a documented compatibility shim in a cloned restoration workspace.
3. Rerun installer finalization.
4. Load the admin panel.
5. Upload controlled JPEG fixtures.
6. Record upload, thumbnail, and EXIF behavior.
