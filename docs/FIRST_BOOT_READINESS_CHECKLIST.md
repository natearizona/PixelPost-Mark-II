# First Boot Readiness Checklist

## Scope

Readiness checklist before attempting first execution of Pixelpost 1.7.3 inside PixelPost Restoration Lab.

## Source Tree

- [ ] Confirm preserved source archive exists in `archive-readonly`.
- [ ] Confirm preserved source tree is mounted or stored read-only.
- [ ] Confirm disposable workspace copy exists under `/opt/pixelpost-restoration-lab/workspaces/`.
- [ ] Confirm `index.php` exists.
- [ ] Confirm `admin/install.php` exists.
- [ ] Confirm `admin/index.php` exists.
- [ ] Confirm `includes/create_tables.php` exists.
- [ ] Confirm `includes/functions.php` exists.
- [ ] Confirm `templates/simple/image_template.html` exists.
- [ ] Confirm `language/admin-lang-english.php` exists.
- [ ] Confirm `language/lang-english.php` exists.

## Expected Generated Files

- [ ] Confirm `includes/pixelpost.php` is absent before first install, or document if present.
- [ ] Confirm installer can write `includes/pixelpost.php` inside disposable workspace only.
- [ ] Confirm generated config will not be written to archive-readonly.

## Writable Runtime Paths

- [ ] Confirm disposable workspace `images/` is writable by the PHP container.
- [ ] Confirm disposable workspace `thumbnails/` is writable by the PHP container.
- [ ] Confirm disposable workspace `includes/` is writable if installer config generation is tested.
- [ ] Confirm logs write to `/opt/pixelpost-restoration-lab/logs/`.
- [ ] Confirm database writes to `/opt/pixelpost-restoration-lab/db/`.

## Database Bootstrap

- [ ] Confirm database service starts.
- [ ] Confirm database name is `pixelpost`.
- [ ] Confirm database user is lab-scoped.
- [ ] Confirm no shared database or shared database network is used.
- [ ] Confirm SQL strict mode is disabled or documented.

## Network Isolation

- [ ] Confirm no Traefik labels exist in Compose definition.
- [ ] Confirm lab does not join Traefik network.
- [ ] Confirm lab uses only `pixelpost-lab-net`.
- [ ] Confirm HTTP binds to `127.0.0.1` only.
- [ ] Confirm no public DNS is configured.
- [ ] Confirm access is via SSH tunnel.

## First Browser Target

Expected tunnel:

```bash
ssh -L 18080:127.0.0.1:18080 root@2.24.122.151
```

Expected local browser URL:

```text
http://127.0.0.1:18080/admin/install.php
```

## Stop Condition

Stop immediately if:

- A service binds publicly.
- Compose attempts to join a non-lab network.
- Traefik labels are present.
- Pixelpost source requires patching to continue.
- Installer attempts to write into archive-readonly.
- Existing AI infrastructure containers are affected.

