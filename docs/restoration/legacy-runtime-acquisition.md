# Legacy Runtime Acquisition

Question: Can a historically aligned MySQL runtime be acquired reproducibly enough to test unmodified Pixelpost 1.7.3?

Answer: yes for MySQL 5.1. A runnable MySQL 5.1.73 container was acquired through `ggmartinez/mysql:5.1` and used successfully for installer-chain testing. MySQL 5.0 and alternate MySQL 5.1 candidates remain acquisition failures in this pass. MySQL 4.1 remains unacquired.

## Source Specimen

- Release under test: Pixelpost 1.7.3
- Raw archive SHA-256: `0553abce0a647ff226d117de0893f903697910761aabf680fad5ce3ed693d98a`
- Archive tree SHA-256 captured by test runner: `8498093b0f50c9f03cf56191cec1b9fb4f52649aac9451abf85682c6424bd05b`

## Acquisition Attempts

| Candidate | Method | Reproducibility | Licensing Concerns | Technical Viability | Restoration Suitability |
| --- | --- | --- | --- | --- | --- |
| MySQL 4.1 official image | `docker pull mysql:4.1` from Docker Hub official namespace | Not reproducible in current lab | Normal MySQL image license review would apply if obtained | Not viable: tag not found in prior Phase 2 probe | Not suitable until an executable binary, source build, or preserved image is acquired |
| MySQL 5.0 official image | `docker pull mysql:5.0` from Docker Hub official namespace | Not reproducible in current lab | Normal MySQL image license review would apply if obtained | Not viable: tag not found in prior Phase 2 probe | Not suitable until another runtime is acquired |
| MySQL 5.1 official image | `docker pull mysql:5.1` from Docker Hub official namespace | Not reproducible in current lab | Normal MySQL image license review would apply if obtained | Not viable: tag not found in prior Phase 2 probe | Not suitable through official namespace |
| `mtirsel/mysql-5.1:latest` | Preserved/community Docker image | Not reproducible under current Docker/containerd | Third-party image; underlying MySQL and base OS licenses require review before redistribution | Pull fails because the image uses the deprecated Docker manifest v1 format | Not suitable unless converted or mirrored as OCI/manifest v2 with provenance |
| `ggmartinez/mysql:5.1` | Community-maintained Docker image | Reproducible by digest `sha256:db6468ed7a662a0efd5aee985b9e5a0c5b6c43732bc22c72a950624ba3349ba2` | Third-party image; do not redistribute without license review of image contents and Dockerfile source | Viable: starts MySQL `5.1.73`, accepts connections, supports the test database | Suitable for restoration testing, with provenance warning |
| `tommi2day/mysql51:latest` | Community-maintained Docker image / source-build oriented project | Reproducible by digest `sha256:9692879f2f1b49cfbf4e7b0020f147ac2dc8c71d677f85a380ffaa9ff1c2eb8b` for the pulled image | Third-party image; project appears designed around downloading MySQL archive sources during build, so redistribution needs review | Pull succeeds, but container does not become ready in current lab: `/db` path missing | Not suitable until expected `/db` mount/init contract is documented and made reproducible |
| `kuborgh/mysql-5.0:latest` | Community-maintained Docker image | Reproducible by digest `sha256:467bc4ad7db43010a018b3e6e9dc4a88f8befe786b1be4e2d2018e8ebdfad1b0` for the pulled image | Third-party image; do not redistribute without license review of bundled MySQL/base OS contents | Pull succeeds, but container exits with `chown: invalid user: mysql` | Not suitable unwrapped |
| `pixelpost-lab-mysql-5.0-kuborgh-user:latest` | Local wrapper over `kuborgh/mysql-5.0:latest` adding `mysql` user and data ownership | Reproducible from `docker/historical/mysql50-kuborgh-user/Dockerfile` plus parent digest | Wrapper Dockerfile is ours; parent image contents still require license/provenance review | Build succeeds, but MySQL still does not become ready | Not suitable in this pass |

## External Acquisition References

- `ggmartinez/mysql` Docker Hub page: `https://hub.docker.com/r/ggmartinez/mysql`
- `kuborgh/mysql-5.0` Docker Hub page: `https://hub.docker.com/r/kuborgh/mysql-5.0/`
- `tommi2day/mysql51` Docker Hub page: `https://hub.docker.com/r/tommi2day/mysql51`
- `mtirsel/mysql-5.1` Docker Hub page: `https://hub.docker.com/r/mtirsel/mysql-5.1/`

These references are acquisition leads, not historical authority. Runtime evidence from the isolated lab takes precedence.

## Evidence

- Pull transcript: `docs/restoration/evidence/1.7.3-historical-runtime/image-pull-probes.log`
- MySQL 5.0 original image failure: `docs/restoration/evidence/1.7.3-historical-runtime/mysql50-kuborgh.log`
- MySQL 5.0 wrapper failure: `docs/restoration/evidence/1.7.3-historical-runtime/mysql50-kuborgh-user.log`
- MySQL 5.1 success: `docs/restoration/evidence/1.7.3-historical-runtime/mysql51-ggmartinez.log`
- Alternate MySQL 5.1 failure: `docs/restoration/evidence/1.7.3-historical-runtime/mysql51-tommi2day.log`

## Decision

A historically aligned MySQL runtime can be acquired reproducibly enough for restoration testing: `ggmartinez/mysql:5.1`, observed at runtime as MySQL `5.1.73`.

This does not make the community image preservation-grade. It is a working restoration-lab runtime candidate, not a canonical archival dependency.
