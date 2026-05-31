# Pixelpost 1.7.3 Historical Runtime Command Transcript

Date: 2026-05-30 America/Phoenix / 2026-05-31 UTC

Target: VPS #1, `/opt/pixelpost-restoration-lab`

Isolation controls:

- Candidate databases ran on per-test Docker networks created with `--internal`.
- No candidate database container published a host port.
- No Traefik labels or routing were used.
- No firewall changes were made.
- Pixelpost ran from disposable workspace copies under `/opt/pixelpost-restoration-lab/workspaces/`.
- The read-only source specimen remained under `/opt/pixelpost-restoration-lab/archive-readonly/pixelpost-1.7.3`.

## Acquisition probe

```text
docker pull mtirsel/mysql-5.1:latest
docker pull ggmartinez/mysql:5.1
docker pull tommi2day/mysql51:latest
docker pull kuborgh/mysql-5.0:latest
```

Full output:

```text
docs/restoration/evidence/1.7.3-historical-runtime/image-pull-probes.log
```

## MySQL 5.0 wrapper build

The `kuborgh/mysql-5.0:latest` image exited with `chown: invalid user: mysql`. A minimal wrapper was built for acquisition testing only:

```text
cat > /opt/pixelpost-restoration-lab/docker/historical/mysql50-kuborgh-user/Dockerfile
docker build -t pixelpost-lab-mysql-5.0-kuborgh-user /opt/pixelpost-restoration-lab/docker/historical/mysql50-kuborgh-user
```

The Dockerfile is recorded at:

```text
docker/historical/mysql50-kuborgh-user/Dockerfile
```

The wrapper still did not produce a ready MySQL 5.0 server in this test pass.

## Historical installer-chain execution

```text
scp /private/tmp/run-historical-dbcompat-173.sh root@2.24.122.151:/opt/pixelpost-restoration-lab/reports/run-historical-dbcompat-173.sh

ssh -o BatchMode=yes root@2.24.122.151 'chmod +x /opt/pixelpost-restoration-lab/reports/run-historical-dbcompat-173.sh; /opt/pixelpost-restoration-lab/reports/run-historical-dbcompat-173.sh'
```

Final evidence directory on VPS:

```text
/opt/pixelpost-restoration-lab/reports/historical-dbcompat-1.7.3-20260531T015611Z
```

Local copied evidence:

```text
docs/restoration/evidence/1.7.3-historical-runtime/mysql50-kuborgh.log
docs/restoration/evidence/1.7.3-historical-runtime/mysql50-kuborgh-user.log
docs/restoration/evidence/1.7.3-historical-runtime/mysql51-ggmartinez.log
docs/restoration/evidence/1.7.3-historical-runtime/mysql51-tommi2day.log
```
