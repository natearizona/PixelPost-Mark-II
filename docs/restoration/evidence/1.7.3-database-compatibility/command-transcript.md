# Pixelpost 1.7.3 Database Compatibility Command Transcript

Date: 2026-05-30 America/Phoenix / 2026-05-31 UTC

Target: VPS #1, `/opt/pixelpost-restoration-lab`

Isolation controls:

- Docker networks created per candidate with `--internal`.
- Database containers had no published ports.
- PHP runner used a disposable workspace copy under `/opt/pixelpost-restoration-lab/workspaces/`.
- Archive specimen remained at `/opt/pixelpost-restoration-lab/archive-readonly/pixelpost-1.7.3`.
- No Traefik labels or routing were used.
- No firewall changes were made.

## Candidate image availability probes

```text
docker pull mysql:4.1
Error response from daemon: failed to resolve reference "docker.io/library/mysql:4.1": docker.io/library/mysql:4.1: not found

docker pull mysql:5.0
Error response from daemon: failed to resolve reference "docker.io/library/mysql:5.0": docker.io/library/mysql:5.0: not found

docker pull mysql:5.1
Error response from daemon: failed to resolve reference "docker.io/library/mysql:5.1": docker.io/library/mysql:5.1: not found

docker pull mysql:5.5
Digest: sha256:12da85ab88aedfdf39455872fb044f607c32fdc233cd59f1d26769fbf439b045
Status: Image is up to date for mysql:5.5

docker pull mariadb:5.5
Digest: sha256:8665c074af5a5fb7e04b9570fcf8551e9d82955182be50375d5013838d4f9137
Status: Image is up to date for mariadb:5.5
```

## PHP image availability probes

```text
docker pull php:5.2-apache
Error response from daemon: failed to resolve reference "docker.io/library/php:5.2-apache": docker.io/library/php:5.2-apache: not found

docker pull php:5.3-apache
Error response from daemon: not implemented: media type "application/vnd.docker.distribution.manifest.v1+prettyjws" is no longer supported since containerd v2.1

docker pull php:5.4-apache
Error response from daemon: not implemented: media type "application/vnd.docker.distribution.manifest.v1+prettyjws" is no longer supported since containerd v2.1

docker pull php:5.6-apache
Digest: sha256:0a40fd273961b99d8afe69a61a68c73c04bc0caa9de384d3b2dd9e7986eec86d
Status: Downloaded newer image for php:5.6-apache
```

## Execution commands

```text
scp /private/tmp/run-dbcompat-173.sh root@2.24.122.151:/opt/pixelpost-restoration-lab/reports/run-dbcompat-173.sh

ssh -o BatchMode=yes root@2.24.122.151 'chmod +x /opt/pixelpost-restoration-lab/reports/run-dbcompat-173.sh; /opt/pixelpost-restoration-lab/reports/run-dbcompat-173.sh'
```

Final evidence directory on VPS:

```text
/opt/pixelpost-restoration-lab/reports/dbcompat-1.7.3-20260531T000320Z
```

Local copied evidence:

```text
docs/restoration/evidence/1.7.3-database-compatibility/mysql55.log
docs/restoration/evidence/1.7.3-database-compatibility/mariadb55.log
```
