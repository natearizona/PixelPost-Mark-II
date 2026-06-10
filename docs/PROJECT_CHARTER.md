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

## Public Repository

This repository is public. All tracked content has passed governance review to verify that no private infrastructure paths, server credentials, or operational details are present.

The private/public boundary is maintained through a separate infrastructure archive. The public doctrine: evidence shows what Pixelpost did. It does not show where tests were executed or how files moved between machines.

## Four Lanes

This project operates across four distinct lanes. Each lane has its own boundary, source of truth, and evidence standard. No lane may contaminate another.

**Lane 1 — Archaeology**
Historical recovery of TalkingTree / Pixelpost records: dates, EXIF, publication chronology, awards, sources, screenshots, archives, and provenance. Source of truth: recovered artifacts and their chain-of-custody records. Evidence standard: Level 2 minimum (logged).

**Lane 2 — Restoration Lab**
Executable legacy runtime experiments for Pixelpost 1.7.3. PHP, MySQL, Apache, GD/JPEG, filesystem permissions, installer behavior, and compatibility findings. Source of truth: runtime logs, transcripts, and screenshots from controlled lab copies. Evidence standard: Level 3 minimum (reproducible). Runtime success claims require transcript or log citation.

**Lane 3 — Public Release Package**
Public-facing documentation, tooling, and archaeology findings cleared for publication. Source of truth: `origin/main` on GitHub. Evidence standard: Level 4 (canonical). Nothing reaches this lane without Nathan's authorization.

**Lane 4 — Private Operations Package**
Private infrastructure, live server credentials, deployment paths, personal archives, and unpublished material. Source of truth: private operations repository (not this repo). This material must never cross into the public release package.

## Source Of Truth

| Lane | Source of truth |
| --- | --- |
| Archaeology | Recovered artifacts and chain-of-custody records |
| Restoration Lab | Runtime logs, transcripts, and screenshots from lab copies |
| Public Release | `origin/main` — GitHub |
| Private Operations | Private operations repository |

## Truth Ladder

No claim may move from observation to canonical state by narrative summary alone.

| Level | Label | Required for |
| --- | --- | --- |
| 0 | Claim | Starting point only |
| 1 | Observed | Internal notes |
| 2 | Logged | Historical archaeology claims |
| 3 | Reproducible | Runtime success claims |
| 4 | Canonical | Public release claims |

A claim that has not reached the required level for its context must be marked provisional or unverified. Narrative summaries do not advance a claim up the ladder.

## Stewardship

Nathan Arizona is the steward and final decision authority for this project.

No content is staged, committed, pushed, deployed, or published without Nathan's authorization. Agents draft. Scripts verify. GitHub preserves. Incident reports correct. Nathan judges.

