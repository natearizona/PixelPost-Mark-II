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

## Uncertainty

Some claims in this project are provisional, estimated, or unverified. This is normal and expected in software archaeology.

Provisional claims must be marked as such. Unverified claims must not be promoted to canonical status without evidence. The absence of certainty is not a flaw — it is an honest record of what is known and what remains unknown.

Do not rewrite uncertain history to make it appear clean.

## Rollback Rule

No restored runtime replaces the public site without Nathan's explicit authorization.

If a runtime experiment corrupts or modifies any preserved artifact, stop immediately. Restore from the last known-good state using the archive manifest. Log the incident before proceeding. Do not attempt recovery by overwriting the original — create a forensic note and escalate to the steward.

## Read-Only Artifact Rule

Original recovered artifacts are never modified in place.

This includes: raw release archives, extracted source trees, original documentation, recovered media files, and exported XML archives. If an artifact must be processed, create a working copy in a restoration workspace. The original stays untouched.

## Release Boundary

Public releases must be generated from an approved manifest, not the whole working directory.

Before release or deployment, confirm:
1. git status is clean on `origin/main`
2. No private material is present in tracked files
3. Nathan has authorized the release
4. Generate from manifest — not from `git push --all`

Public release requires Nathan's explicit authorization. No deployment gate bypasses the steward.

Private operations material, personal archive paths, server credentials, and unpublished content must never cross into the public release package.

## Unresolved Blockers

Known blockers that must remain visible until resolved:

**MySQL TIMESTAMP(14) — OPEN**
MySQL 5.5.62 and MariaDB 5.5.64 installer fail at `{prefix}version TIMESTAMP(14) NOT NULL` in the Pixelpost 1.7.3 schema. This blocker prevents successful installation on modern MySQL/MariaDB.

Status: Resolved by MySQL 5.1.73 (confirmed). MySQL 4.1, 5.0 container testing still needed to establish the full compatibility envelope.

Do not mark this blocker resolved until MySQL ≤5.1 container reproducibility is confirmed and logged.

## Next Safe Experiment

Before any new runtime test:

1. Create a clean lab copy — do not use production data or the original archive tree.
2. Run the experiment in `docker/restoration-workspaces/` or equivalent isolated path.
3. Log the outcome — success or failure — before the container is stopped.
4. If the experiment fails, preserve the failure log as evidence. Do not delete failed experiments.
5. Do not promote "works once" to "restored" without reproducibility at Level 3.

## Publication

Do not make this repository public until the project can explain what it has, where it came from, and how much confidence it has in each artifact.

