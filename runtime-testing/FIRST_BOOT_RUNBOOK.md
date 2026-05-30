# First Boot Runbook

## Prerequisite

Install a container runtime that provides `docker` and `docker compose`.

The current Codex shell does not expose Docker, Podman, PHP, or MySQL. These commands currently fail:

```text
docker --version
podman --version
php -v
mysql --version
```

## Reset A Disposable Workspace

From the repository root:

```bash
tools/reset-first-boot-workspace.sh 1.7.3
```

Supported versions:

- `1.3`
- `1.4`
- `1.4.1`
- `1.4.2`
- `1.7.3`

## Start The Historical Runtime

```bash
cd docker
docker compose --env-file pixelpost.env.example -f compose.pixelpost.yml up --build
```

Open:

```text
http://localhost:8080/admin/install.php
```

## Installer Values

Use throwaway local credentials:

```text
Database host: db
Database name: pixelpost
Database user: pixelpost
Database password: pixelpost
Table prefix: pixelpost_
Admin username: archaeologist
Admin password: pixelpost-local-only
```

## Logs

Runtime logs should appear under:

```text
docker/runtime/apache-logs/
```

Database files are under:

```text
docker/runtime/mariadb/
```

Both paths are ignored by git.

## Stop And Reset

```bash
cd docker
docker compose -f compose.pixelpost.yml down
```

To test again from a clean Pixelpost source workspace:

```bash
tools/reset-first-boot-workspace.sh 1.7.3
```

To clear database state, remove `docker/runtime/mariadb/` manually after stopping containers.

