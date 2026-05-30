# PixelPost Restoration Lab Security

## Security Model

PixelPost Restoration Lab is a private, disposable restoration environment for historically recovered Pixelpost releases.

It must not be publicly exposed.

## Required Controls

- No public DNS: satisfied.
- No Traefik routing: satisfied.
- No Traefik labels: satisfied with `traefik.enable=false`.
- No firewall changes: satisfied.
- No shared mounts with existing AI services: satisfied.
- No shared databases: satisfied.
- No shared application networks: satisfied.
- Localhost-only HTTP binding: satisfied with `127.0.0.1:18080`.
- SSH tunnel access for browser testing: required for workstation browser access.
- Disposable writable workspaces: satisfied.
- Read-only preservation archive area: satisfied.

## Network Design

Compose project:

```text
pixelpost-restoration-lab
```

Private bridge network:

```text
pixelpost-lab-net
```

HTTP exposure:

```text
127.0.0.1:18080 -> pixelpost-php:80
```

No service should bind to:

```text
0.0.0.0
```

No service should join:

- Traefik networks
- OpenClaw networks
- Hermes networks
- MemPalace networks
- Hostinger-generated app networks

Observed network membership:

```text
pixelpost-lab-net: pixelpost-php pixelpost-db
```

Observed port binding:

```text
127.0.0.1:18080 -> pixelpost-php:80
```

Observed Traefik label:

```text
traefik.enable=false
```

## Data Isolation

Lab directory:

```text
/opt/pixelpost-restoration-lab
```

All lab data should stay below that path:

- `archive-readonly/`
- `workspaces/`
- `docker/`
- `db/`
- `logs/`
- `reports/`

## Operational Boundary

The lab is allowed to fail loudly. It is not allowed to become a public service.

Historical insecurity in Pixelpost is expected and must remain contained inside the lab.

## Current Security Status

The lab is isolated from the existing AI infrastructure services. The only host port exposed by the lab is bound to localhost on VPS #1. Browser access should use an SSH tunnel:

```bash
ssh -L 18080:127.0.0.1:18080 root@2.24.122.151
```

Then open:

```text
http://127.0.0.1:18080/admin/install.php
```
