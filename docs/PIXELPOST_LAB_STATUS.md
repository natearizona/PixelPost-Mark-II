# PixelPost Restoration Lab Status

## Current Status

Phase 0 VPS audit is complete.

Docker readiness is confirmed on VPS #1.

No PixelPost Restoration Lab directories, containers, networks, or volumes have been created on the VPS yet.

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

## Proposed Containers

- `pixelpost-php`
- `pixelpost-db`

## Proposed Network

```text
pixelpost-lab-net
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

## Conflicts Avoided By Design

- OpenClaw: no shared network, volume, mount, or route.
- Hermes: no shared `/opt/hermes-uap`, network, or ports.
- MemPalace: no shared network or volume.
- Traefik: no labels, routing, or network integration.
- Telegram services: no shared configuration, secrets, or network.
- WordPress: no WordPress VPS or production site paths used.

## Remote Write Gate

Before creating `/opt/pixelpost-restoration-lab`, the VPS operational charter requires explicit approval after risk and rollback are stated.

## Exact Commands Executed So Far

```bash
ssh -o BatchMode=yes -o ConnectTimeout=8 root@uap.turquoiseufo.tech 'hostname; whoami; uname -a'
ssh-keygen -F uap.turquoiseufo.tech -f ~/.ssh/known_hosts
ssh-keygen -F 2.24.122.151 -f ~/.ssh/known_hosts
dig +short uap.turquoiseufo.tech A
ssh -o BatchMode=yes -o ConnectTimeout=8 root@2.24.122.151 'hostname; whoami; uname -a'
ssh -o BatchMode=yes root@2.24.122.151 'set -u; ... Phase 0 audit commands ...'
ssh -o BatchMode=yes root@2.24.122.151 'set -u; ... Traefik label and docker stats commands ...'
```

Notes:

- Hostname SSH check failed at host-key verification.
- IP SSH check succeeded using existing known-host data.
- `dig` failed locally due sandbox bind restrictions; DNS was not required after successful IP SSH.

## Estimated Path To First Installer Boot

1. Approve VPS write operations for lab creation.
2. Create `/opt/pixelpost-restoration-lab` directory structure.
3. Copy lab Docker definitions into `/opt/pixelpost-restoration-lab/docker`.
4. Copy or place recovered Pixelpost 1.7.3 into `archive-readonly` with read-only permissions.
5. Create a disposable workspace copy.
6. Start Compose with project name `pixelpost-restoration-lab`.
7. Verify port binding is `127.0.0.1:18080` only.
8. Access installer over SSH tunnel.

