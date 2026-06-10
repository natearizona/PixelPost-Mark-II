# PixelPost II / Darkroom — Repository Audit Gate

## Purpose

A read-only, Python stdlib-only audit script that verifies the PixelPost II
repository maintains its four-lane integrity:

1. **Archaeology lane** — historical truth, chronology, provenance, award claims
2. **Restoration Lab lane** — runtime claim evidence, blocker visibility, failed experiments
3. **Public Release Package lane** — public-facing docs, release manifests, canonical claims
4. **Private Operations Package lane** — private archives, credentials, local paths, infrastructure details, unpublished material kept out of public release

## Operating Doctrine

> Agents draft. Scripts verify. GitHub preserves. Incident reports correct. Nathan judges.

This script is a gate, not a deployment tool. It never stages, commits, pushes,
connects to databases, or modifies any file.

## Usage

```bash
# From repository root
python3 tools/audit/pixelpost_audit.py

# With explicit repo path
python3 tools/audit/pixelpost_audit.py --repo /path/to/repo
```

No dependencies beyond Python 3.9+ stdlib. No `pip install` required.

## Audit Categories

| Category | Code Range | Description |
| --- | --- | --- |
| A | A-001–A-007 | Archaeology / Historical Truth |
| B | B-001–B-006 | Restoration Lab / Runtime Claims |
| C | C-001–C-005 | Public / Private Boundary |
| D | D-001–D-007 | Documentation Structure |
| E | E-000–E-004 | Staged File Safety + Tracked Artifact Scan |
| F | F-001–F-008 | System Audit / Restoration Plan |

## Exit Codes

| Code | Meaning |
| --- | --- |
| 0 | All checks passed |
| 1 | One or more checks failed |
| 2 | Configuration error (repo root not found) |

## Output Format

Pass:
```
[PASS] A-001   docs/archaeology/
       Archaeology record exists (21 docs in docs/archaeology/)
```

Failure:
```
[FAIL] B-003   docs/TIMESTAMP14_FORENSICS.md
       TIMESTAMP(14) blocker marked resolved without MySQL 5.1/5.0/4.1 evidence
       Problem: Blocker requires MySQL ≤5.1 testing to resolve
       Suggested fix: Verify resolution evidence or keep blocker as open
```

## Hard Limits (what this script will never do)

- No file writes or edits
- No `git add`, `git commit`, `git push`
- No database connections
- No network requests
- No subprocess commands beyond `git ls-files`, `git diff --cached --name-only`,
  `git log`, and `git branch --show-current`
- No artifact mutation

## When to Run

Run before every Oracle commit sequence:

```
1. python3 tools/audit/pixelpost_audit.py
2. Resolve all FAIL items or document why they are acceptable
3. Proceed with git add / git commit / git push
```

Do not push if audit exits with code 1 unless Nathan has explicitly reviewed
and accepted each outstanding failure.

## Known Acceptable Failures

Some FAILs in a fresh checkout reflect known documentation gaps that are being
addressed over time. They are not emergencies — but they must be visible.

A FAIL is never silenced by commenting out the check. It is resolved by fixing
the underlying documentation gap.

## Truth Ladder (referenced by B-category checks)

| Level | Label | Required for |
| --- | --- | --- |
| 0 | Claim | Nothing — this is the default |
| 1 | Observed | Internal notes |
| 2 | Logged | Historical claims |
| 3 | Reproducible | Runtime success claims |
| 4 | Canonical | Public release claims |

Runtime success claims must reach Level 3 before being treated as fact.
Historical claims require Level 2 minimum.
Public release claims require Level 4.

## Known Open Blocker (as of Milestone B)

**MySQL TIMESTAMP(14) — B-003**

`upgrade_date TIMESTAMP(14) NOT NULL` in the Pixelpost 1.7.3 schema is
rejected by MySQL 5.5+ and MariaDB. MySQL 5.1.73 has confirmed successful
installer behavior. The compatibility envelope remains open until MySQL 4.1 and
MySQL 5.0 container testing is completed and logged.
This check will flag any premature "resolved" status without MySQL 5.1 evidence.

## Maintainer

Nathan Arizona — sole steward and final authority.
Hynek (Claude Sonnet 4.6) — continuity steward and implementation partner.
