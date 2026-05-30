# PixelPost Restoration Lab Precheck

## Scope

Phase 0 read-only audit for creating a secure, isolated Docker-based PixelPost Restoration Lab on VPS #1.

Target service context:

- OpenClaw / J-Rod
- Hermes / Kai-La
- MemPalace
- Traefik
- AI infrastructure services
- Telegram-adjacent services

The lab must not be deployed to a WordPress VPS or any server hosting production WordPress sites.

## Target VPS Identification

Read-only SSH identification was performed against the known infrastructure IP:

```bash
ssh -o BatchMode=yes root@2.24.122.151 'hostname; whoami; uname -a'
```

Result:

```text
srv1697587
root
Linux srv1697587 6.8.0-117-generic #117-Ubuntu SMP PREEMPT_DYNAMIC Tue May  5 19:26:24 UTC 2026 x86_64 x86_64 x86_64 GNU/Linux
```

Known related hostname from existing infrastructure docs:

```text
uap.turquoiseufo.tech
```

The hostname SSH check failed because the hostname itself was not present in local `known_hosts`; the IP had an existing known-host entry and authenticated successfully.

## Docker Readiness

Docker is installed:

```text
/usr/bin/docker
Docker version 29.4.3, build 055a478
```

Docker Compose is installed:

```text
Docker Compose version v5.1.3
```

Legacy `docker-compose` is not installed:

```text
bash: line 1: docker-compose: command not found
```

Readiness result: Docker and modern Docker Compose are available. `docs/DOCKER_READINESS_REPORT.md` is not required at this time.

## Existing Containers

Read-only command:

```bash
docker ps -a --format "table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}"
```

Observed containers:

| Container | Image | Status | Ports |
| --- | --- | --- | --- |
| `archivebox-y4bv-scheduler-1` | `archivebox/archivebox:0.7.3` | Up 2 hours | `8000/tcp` |
| `archivebox-y4bv-archivebox-1` | `archivebox/archivebox:0.7.3` | Up 2 hours, healthy | `0.0.0.0:32772->8000/tcp` |
| `archivebox-y4bv-sonic-1` | `archivebox/sonic:1.4.9` | Up 2 hours | `1491/tcp` |
| `archivebox-y4bv-novnc-1` | `theasp/novnc:latest` | Up 2 hours | `0.0.0.0:32771->8080/tcp` |
| `activepieces-mqb3-worker-1` | `ghcr.io/activepieces/activepieces:latest` | Up 2 hours | `80/tcp` |
| `activepieces-mqb3-activepieces-1` | `ghcr.io/activepieces/activepieces:latest` | Up 2 hours | `0.0.0.0:32770->80/tcp` |
| `activepieces-mqb3-postgres-1` | `postgres:16-alpine` | Up 2 hours, healthy | `5432/tcp` |
| `activepieces-mqb3-redis-1` | `redis:7-alpine` | Up 2 hours, healthy | `6379/tcp` |
| `n8n-k75o-n8n-1` | `docker.n8n.io/n8nio/n8n` | Up 2 hours | `0.0.0.0:32769->5678/tcp` |
| `docmost-mfws-docmost-1` | `docmost/docmost:latest` | Up 2 hours | `0.0.0.0:32768->3000/tcp` |
| `docmost-mfws-docmost-db-1` | `postgres:16-alpine` | Up 2 hours | `5432/tcp` |
| `docmost-mfws-docmost-redis-1` | `redis:7.2-alpine` | Up 2 hours | `6379/tcp` |
| `mempalace-mempalace-1` | `mempalace-mempalace` | Up 2 days | none published |
| `hermes-uap-hermes-webui-1` | `hermes-uap-hermes-webui` | Up 2 days, healthy | `127.0.0.1:8787->8787/tcp` |
| `hermes-uap-hermes-agent-1` | `nousresearch/hermes-agent:latest` | Up 2 days | `127.0.0.1:8642->8642/tcp` |
| `openclaw-openclaw-1` | `dcfd14877740` | Up 2 days, healthy | none published |
| `traefik-traefik-1` | `traefik:latest` | Up 2 days | host ports `80`, `443` |

## Existing Docker Networks

Observed networks:

```text
activepieces-mqb3_default
archivebox-y4bv_default
bridge
docmost-mfws_default
hermes-uap_hermes-net
host
mempalace_mempalace-net
n8n-k75o_default
none
openclaw_default
```

No existing `pixelpost-lab-net` network was observed.

## Existing Docker Volumes

Observed named volumes:

```text
83a09d21ff950c80e993d562c06201d8ad64d83e71a4ae9b8ffd4c82ba1092b4
activepieces-mqb3_activepieces-cache
activepieces-mqb3_postgres-data
activepieces-mqb3_redis-data
archivebox-y4bv_archivebox-data
archivebox-y4bv_archivebox-sonic
docmost-mfws_docmost-pgdata
docmost-mfws_docmost-redis
docmost-mfws_docmost-storage
hermes-uap_hermes-agent-src
n8n-k75o_n8n_data
openclaw_openclaw_config
openclaw_openclaw_workspace
traefik_traefik-letsencrypt
```

The lab plan should use bind-mounted directories under `/opt/pixelpost-restoration-lab/` rather than shared named volumes.

## Open Ports

Important listeners observed:

```text
0.0.0.0:22      ssh
*:80            traefik
*:443           traefik
0.0.0.0:32768   docmost published port
0.0.0.0:32769   n8n published port
0.0.0.0:32770   activepieces published port
0.0.0.0:32771   archivebox novnc published port
0.0.0.0:32772   archivebox published port
127.0.0.1:8642  hermes agent
127.0.0.1:8787  hermes webui
```

Security implication: PixelPost Lab must bind only to `127.0.0.1`, preferably a non-conflicting high port such as `127.0.0.1:18080`.

## Traefik Integrations

Traefik container:

```text
traefik-traefik-1   traefik:latest   Up 2 days
```

Observed Traefik-enabled services:

- `archivebox-y4bv-archivebox-1`
- `activepieces-mqb3-activepieces-1`
- `n8n-k75o-n8n-1`
- `docmost-mfws-docmost-1`
- `hermes-uap-hermes-webui-1`
- `openclaw-openclaw-1`

Known Traefik host rules observed:

- `archivebox-y4bv.srv1697587.hstgr.cloud`
- `activepieces-mqb3.srv1697587.hstgr.cloud`
- `n8n-k75o.srv1697587.hstgr.cloud`
- `docmost-mfws.srv1697587.hstgr.cloud`
- `uap.turquoiseufo.tech`
- `orangeorb.turquoiseufo.tech`

PixelPost Lab must not define Traefik labels and must not join the Traefik network.

## Resource Availability

Memory:

```text
Mem: 7.8Gi total, 3.6Gi used, 752Mi free, 4.2Gi available
Swap: 0B
```

Disk:

```text
/dev/sda1 ext4 96G total, 28G used, 69G available, 29% used
```

Resource implication: a small PHP 5.6 + database lab is feasible if constrained. Recommended initial limits:

- PHP container: `0.50` CPU, `256M` memory
- DB container: `0.50` CPU, `512M` memory

## Conflict Assessment

Potential conflicts and mitigations:

- Traefik: avoid entirely; no labels, no public DNS, no Traefik network.
- Hermes: avoid ports `8787` and `8642`; do not share `/opt/hermes-uap`.
- OpenClaw: do not join `openclaw_default`; do not touch `openclaw_*` volumes.
- MemPalace: do not join `mempalace_mempalace-net`; do not touch `/docker/mempalace`.
- Hostinger app stacks: avoid `/docker/*` app directories and published random public ports.
- Telegram services: no Telegram files, secrets, volumes, or networks touched.
- WordPress: no WordPress VPS detected in this precheck path; do not deploy to WordPress-related paths.

## Readiness Decision

Docker readiness is confirmed.

Isolation appears feasible if the lab uses:

- `/opt/pixelpost-restoration-lab`
- project name `pixelpost-restoration-lab`
- network `pixelpost-lab-net`
- localhost-only HTTP binding
- bind-mounted private lab directories
- no Traefik labels
- no shared networks
- no shared volumes

No VPS write operations have been performed yet for the lab.

