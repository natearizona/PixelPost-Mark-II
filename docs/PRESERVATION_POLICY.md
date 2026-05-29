# Preservation Policy

## Core Rule

Preserve first. Understand second. Modernize last.

## Historical Artifacts

Historical artifacts include:

- raw release archives
- extracted original source trees
- original documentation
- templates and themes
- addons and plugins
- screenshots
- forum/wiki/manual captures
- checksums and provenance records

These artifacts must not be modified in place.

## Handling Rules

- Do not auto-format original source.
- Do not update dependencies inside original trees.
- Do not rewrite procedural PHP to modern patterns inside preserved artifacts.
- Do not remove insecure or deprecated behavior before documenting it.
- Do not normalize filenames, line endings, encodings, or directory layouts unless a separate forensic copy is created and the change is logged.
- Do not commit or push recovered archives until provenance verification is complete.

## Restoration Copies

Runtime testing must use cloned restoration workspaces, not preserved archive trees.

Disposable restoration copies belong under `docker/restoration-workspaces/` or another clearly marked runtime-testing path.

Any generated config files, uploaded test images, thumbnails, logs, and databases must stay out of preserved source trees.

## Provenance

Every recovered artifact should receive a chain-of-custody note before it is promoted into canonical archival status.

Minimum required provenance:

- source URL or acquisition path
- retrieval date
- retriever
- hash
- mirror or archive origin
- Wayback timestamp when applicable
- authenticity observations
- known gaps or doubts

## Publication

Do not make this repository public until the project can explain what it has, where it came from, and how much confidence it has in each artifact.

