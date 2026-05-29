# Project Charter

## Name

Pixelpost Mark II

## Purpose

Pixelpost Mark II exists to preserve, study, restore, and eventually continue the Pixelpost photoblogging platform with historical care.

The project begins as software archaeology. It prioritizes evidence, provenance, original behavior, and cultural continuity over modernization.

## Scope Of The Current Phase

Current phase:

- acquire original source materials
- preserve raw artifacts
- document provenance
- inspect original architecture
- reconstruct historical runtimes
- attempt non-destructive first boot
- document compatibility risks

Out of scope for this phase:

- framework migration
- template redesign
- source cleanup
- dependency upgrades
- production deployment
- public launch

## Preservation Doctrine

The original Pixelpost source trees are museum artifacts. They should be handled as historical evidence, not as messy legacy code awaiting cleanup.

No automatic formatting, rewriting, modernization, or dependency replacement should happen inside preserved source trees.

## Branch Strategy

Intended branch strategy:

- `main`: preservation-grade canonical branch. Documentation, verified provenance records, repository policy, and stable archival metadata.
- `restoration/*`: runtime testing, historical boot attempts, container experiments, and first-boot logs.
- `modernization/*`: future compatibility and continuation work after archaeology has established the behavioral contract.
- `research/*`: experimental archaeology, audits, source comparison, Wayback harvesting, and ecosystem mapping.

## Private Repository Policy

This repository should remain private until:

- recovered archives have chain-of-custody records
- provenance gaps are documented
- preservation policy is stable
- runtime restoration boundaries are understood
- public release risk has been reviewed

