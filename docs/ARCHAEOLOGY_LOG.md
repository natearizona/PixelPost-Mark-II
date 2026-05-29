# Archaeology Log

## 2026-05-28

Initialized Pixelpost Mark II archaeology workspace.

Recovered and preserved initial source materials:

- Pixelpost 1.7.3 mirror archive from PHP Sources.
- Pixelpost 1.3, 1.4, 1.4.1, and 1.4.2 release archives from SourceForge.

Created raw archive area:

- `archive/original-pixelpost/raw/`

Created extracted inspection area:

- `archive/original-pixelpost/extracted/`

Created initial documentation:

- architecture audit
- routing analysis
- database schema notes
- template system notes
- installer analysis
- upload pipeline notes
- compatibility audit
- historical notes
- modernization target map
- first boot execution report

First runtime execution attempt did not reach Pixelpost. The local shell did not expose Docker, Podman, Colima, QEMU, PHP, MySQL, Homebrew, or Nix.

Disposable first-boot restoration copies were separated under:

- `docker/restoration-workspaces/`

GitHub repository creation was requested, but the GitHub CLI was not available in the shell. Remote creation is paused until GitHub tooling or credentials are available.

