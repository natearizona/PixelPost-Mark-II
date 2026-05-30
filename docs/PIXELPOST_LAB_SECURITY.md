# PixelPost Restoration Lab Security

## Security Model

PixelPost Restoration Lab is a private, disposable restoration environment for historically recovered Pixelpost releases.

It must not be publicly exposed.

## Required Controls

- No public DNS.
- No Traefik routing.
- No Traefik labels.
- No firewall changes.
- No shared mounts with existing AI services.
- No shared databases.
- No shared application networks.
- Localhost-only HTTP binding.
- SSH tunnel access for browser testing.
- Disposable writable workspaces.
- Read-only preservation archive area.

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

