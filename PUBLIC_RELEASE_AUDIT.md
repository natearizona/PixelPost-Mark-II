# Public Release Audit — PixelPost Mark II

**Audit Date:** 2026-05-30
**Repository:** `natearizona/PixelPost-Mark-II`
**Auditor:** Claude Sonnet 4.6 / Nathan Arizona
**Release Type:** Controlled public archaeology release — Phase I (ARCHAEOLOGY)
**Current Repository Status:** PRIVATE

---

## Purpose

This document records the classification of every tracked file in the repository as:

- `PUBLIC` — safe for public release as-is
- `REVIEW` — requires verification or scrubbing before public release
- `PRIVATE` — contains operational or sensitive information; must not be exposed in a public release

This audit determines whether the repository is ready to be switched from private to public.

---

## Summary Verdict

> **The repository is NOT ready to be made fully public.**

Three files contain the internal VPS #1 IP address (`2.24.122.151`) and SSH access commands referencing the production AI infrastructure server. These must be removed or scrubbed before the repository can be made public.

The archaeological core of the repository — project vision, preservation policy, historical source analysis, PHP runtime research, and Docker restoration tooling — is clean, appropriate, and ready for public release once the three PRIVATE files are resolved.

**Minimum path to public:**

1. Remove or scrub `docs/PIXELPOST_LAB_STATUS.md`
2. Remove or scrub `docs/PIXELPOST_LAB_SECURITY.md`
3. Remove or scrub `docs/FIRST_BOOT_EXECUTION_REPORT.md` (or redact lines 153–220)

Four additional REVIEW files contain references to internal infrastructure service names or operational workflow details that should be evaluated before going public.

---

## Security Scan Results

**Scan performed:** 2026-05-30
**Scope:** All tracked files in the repository

| Finding | Status |
|---|---|
| API tokens / Bearer tokens in tracked files | NONE FOUND ✓ |
| Cloudflare tokens (`cfat_`, `cfut_`) | NONE FOUND ✓ |
| Database passwords (production) | NONE FOUND ✓ |
| Private key content committed | NONE FOUND ✓ |
| GitHub tokens (`ghp_`, `gho_`) in tracked files | NONE FOUND ✓ |
| `.env` files committed | NONE FOUND ✓ (gitignored) |
| Internal VPS IP addresses in tracked files | FOUND — see table below |
| SSH root access commands in tracked files | FOUND — see table below |
| Internal service names (Hermes, OpenClaw, MemPalace) | FOUND — `docs/PIXELPOST_LAB_SECURITY.md`, `docs/PIXELPOST_LAB_PRECHECK.md` |
| Local lab credentials in Docker compose | FOUND — `docker/pixelpost-restoration-lab.compose.yml` (labeled local-only; see REVIEW) |

**Files containing internal VPS IP or SSH references:**

| File | Detail | Classification |
|---|---|---|
| `docs/PIXELPOST_LAB_STATUS.md` | `2.24.122.151`, SSH commands, `root@`, SCP commands, internal VPS paths | PRIVATE |
| `docs/PIXELPOST_LAB_SECURITY.md` | `2.24.122.151`, SSH tunnel command `ssh -L 18080:...root@2.24.122.151` | PRIVATE |
| `docs/FIRST_BOOT_EXECUTION_REPORT.md` | `2.24.122.151` at line 158 (VPS Restoration Lab Execution section) | PRIVATE |

**Conclusion:** No production credentials, API tokens, or private keys are in tracked files.
VPS IP and SSH access patterns are present in three PRIVATE-classified files.
These must be excluded from any public release.

---

## File Classification

### PUBLIC

Files safe for public release without modification. 43 files.

#### Root

| File | Rationale |
|---|---|
| `.gitignore` | Shows responsible secret management. Appropriate to share. |
| `README.md` | Project vision and structure. No sensitive content. |

#### Archive

| File | Rationale |
|---|---|
| `archive/MANIFEST.md` | Archive catalog and inventory. No sensitive content. |
| `archive/provenance/CHAIN_OF_CUSTODY_TEMPLATE.md` | Template document. No sensitive content. |

#### Docker — Historical Environment

| File | Rationale |
|---|---|
| `docker/historical/.gitkeep` | Empty structural placeholder. |
| `docker/historical/php56-apache/Dockerfile` | Historical PHP 5.6 + Apache environment definition. Entirely appropriate for a public archaeology project. |
| `docker/historical/php56-apache/apache-vhost.conf` | Generic historical Apache vhost config. No sensitive content. |
| `docker/historical/php56-apache/php.ini` | Historical PHP config for restoration lab. No sensitive content. |
| `docker/pixelpost.env.example` | Example environment file with placeholder values. No real credentials. |
| `docker/restoration-workspaces/.gitkeep` | Empty structural placeholder. |
| `docker/compose.pixelpost.yml` | Local development compose file. Uses obvious placeholder credentials (`pixelpost`/`pixelpost`) for a localhost-only restoration lab — consistent with standard open-source dev tooling. No production credentials. |

#### Docs — Archaeology and Research

| File | Rationale |
|---|---|
| `docs/ADMIN_WORKFLOW.md` | Historical analysis of PixelPost admin interface. Pure archaeology. |
| `docs/ARCHAEOLOGY_LOG.md` | Research log. No sensitive content. |
| `docs/COMPATIBILITY_AUDIT.md` | PHP compatibility analysis of original PixelPost. Pure archaeology. |
| `docs/DATABASE_SCHEMA.md` | Historical PixelPost database schema analysis. Pure archaeology. |
| `docs/FIRST_BOOT_READINESS_CHECKLIST.md` | Generic environment checklist. No VPS references or sensitive content. |
| `docs/HISTORICAL_NOTES.md` | Historical research notes. No sensitive content. |
| `docs/HISTORICAL_RESTORATION_STATUS.md` | Restoration phase status. No sensitive content. |
| `docs/HISTORICAL_RUNTIME_MATRIX.md` | PHP/MySQL runtime compatibility matrix. Pure archaeology. |
| `docs/HISTORICAL_RUNTIME_RATIONALE.md` | Runtime selection rationale. No sensitive content. |
| `docs/INSTALLER_ANALYSIS.md` | Analysis of PixelPost installer behavior. Pure archaeology. |
| `docs/MODERNIZATION_TARGETS.md` | Risk-ranked map of future modernization targets. No sensitive content. |
| `docs/ORIGINAL_ARCHITECTURE.md` | Original PixelPost architecture documentation. Pure archaeology. |
| `docs/PHOTOBLOG_PHILOSOPHY.md` | Essay on photoblogging philosophy and PixelPost's place in history. |
| `docs/PRESERVATION_POLICY.md` | Project preservation policy. Appropriate for public. |
| `docs/PROJECT_CHARTER.md` | Project charter. Appropriate for public. |
| `docs/ROUTING_ANALYSIS.md` | PixelPost routing analysis. Pure archaeology. |
| `docs/ROUTING_MODEL.md` | PixelPost routing model documentation. Pure archaeology. |
| `docs/TEMPLATE_ENGINE.md` | PixelPost template engine analysis. Pure archaeology. |
| `docs/TEMPLATE_SYSTEM.md` | PixelPost template system documentation. Pure archaeology. |
| `docs/TIMESTAMP14_FORENSICS.md` | Historical timestamp forensics. Pure archaeology. |
| `docs/UPLOAD_PIPELINE.md` | PixelPost upload pipeline analysis. Pure archaeology. |
| `docs/audits/.gitkeep` | Empty structural placeholder. |
| `docs/historical-environments/.gitkeep` | Empty structural placeholder. |
| `docs/historical-environments/PHP56_APACHE_MARIADB.md` | Historical environment documentation. No sensitive content. |
| `docs/restoration/.gitkeep` | Empty structural placeholder. |

#### Runtime Testing and Tools

| File | Rationale |
|---|---|
| `runtime-testing/.gitkeep` | Empty structural placeholder. |
| `runtime-testing/FIRST_BOOT_RUNBOOK.md` | Generic runbook. Uses relative paths only. No sensitive content. |
| `tools/.gitkeep` | Empty structural placeholder. |
| `tools/reset-first-boot-workspace.sh` | Shell script using repository-relative paths only. No hardcoded VPS paths or credentials. |

---

### REVIEW

Files that require evaluation or scrubbing before public release. Not blocked by credentials, but contain operational context that warrants review.

| File | Reason | Recommended Action |
|---|---|---|
| `docs/PIXELPOST_LAB_PRECHECK.md` | References internal AI service names: Telegram, Traefik, OpenClaw, Hermes, MemPalace. These appear in security isolation checks ("no shared configuration with Telegram services", etc.) and reveal the names of internal AI infrastructure services. | Review whether service name references are acceptable for public. If not, redact service names to generic labels. |
| `docs/REPOSITORY_STATUS.md` | Operational setup log documenting SSH authentication success, exact git push commands, HTTPS failure modes, and remote branch setup process. Reveals internal workflow. No IPs. | Evaluate whether this operational log belongs in the public record. Consider removing or summarizing as a human-readable setup narrative. |
| `docs/GITHUB_PREPARATION.md` | Documents failed GitHub CLI authentication attempts and SSH success. Operational meta-document describing how the repo was set up. No IPs. | Low risk. Consider whether this operational setup doc serves the public archaeology audience. If not, remove. |
| `docker/pixelpost-restoration-lab.compose.yml` | Hard-coded VPS-specific volume paths (`/opt/pixelpost-restoration-lab/...`). Local lab credentials labeled `pixelpost_root_local_only` and `pixelpost_local_only`. Reveals internal VPS directory structure. | Replace hardcoded VPS volume paths with relative or parameterized paths. Standardize with `docker/compose.pixelpost.yml` pattern using env vars. |

---

### PRIVATE

Files that must not be included in any public release of this repository.

| File | Reason |
|---|---|
| `docs/PIXELPOST_LAB_STATUS.md` | VPS #1 IP (`2.24.122.151`), SSH root access commands, SCP commands transferring files to VPS, internal VPS paths, production service context |
| `docs/PIXELPOST_LAB_SECURITY.md` | VPS #1 IP, SSH tunnel command with VPS IP, internal AI service names (OpenClaw, Hermes, MemPalace, Traefik) and network topology |
| `docs/FIRST_BOOT_EXECUTION_REPORT.md` | VPS #1 IP at line 158 in the `2026-05-30 VPS Restoration Lab Execution` section |

**Note on `docs/FIRST_BOOT_EXECUTION_REPORT.md`:** The majority of this document is archaeological and appropriate for public release. Only the `2026-05-30 VPS Restoration Lab Execution` section contains the VPS IP. If the operational execution section (approximately lines 153–220) is removed or replaced with a sanitized summary, the remainder of the document can be promoted to PUBLIC.

---

## Verification Checklist

- [x] No API tokens or credentials in tracked files
- [x] No private keys committed
- [x] No `.env` files committed (gitignored)
- [x] Local lab credentials are labeled local-only and in localhost-bound Docker configs
- [ ] `docs/PIXELPOST_LAB_STATUS.md` removed from public-facing release
- [ ] `docs/PIXELPOST_LAB_SECURITY.md` removed from public-facing release
- [ ] `docs/FIRST_BOOT_EXECUTION_REPORT.md` scrubbed or VPS section removed
- [ ] REVIEW documents evaluated: `PIXELPOST_LAB_PRECHECK.md`, `REPOSITORY_STATUS.md`, `GITHUB_PREPARATION.md`, `docker/pixelpost-restoration-lab.compose.yml`

---

## Recommended Next Steps

### Immediate (before going public)

**Option A — Remove PRIVATE files from tracked history:**

```bash
# Remove PRIVATE files from index and disk
git rm docs/PIXELPOST_LAB_STATUS.md
git rm docs/PIXELPOST_LAB_SECURITY.md
git rm docs/FIRST_BOOT_EXECUTION_REPORT.md   # or scrub and re-add

# Commit the removal
git commit -m "security: remove VPS-referencing operational files before public release"

# If these files have been on remote branches that could be public, rewrite history.
# Otherwise, if visibility was always private, a simple removal commit is sufficient.
```

**Option B — Keep this repo private; create a separate public-facing fork:**

The repository could remain private as the operational record. A clean public fork containing only PUBLIC-classified files could be created for the community-facing release.

Option A is recommended since the repository structure is otherwise clean and the PRIVATE content is limited to three files.

### Near Term

1. Evaluate and resolve REVIEW documents (4 files above)
2. Replace hardcoded VPS paths in `docker/pixelpost-restoration-lab.compose.yml` with env vars
3. Add epistemic labels (`VERIFIED FACT`, `INFERRED`, `RECONSTRUCTION`, `OPEN QUESTION`) to all archaeological documents before public release
4. Consider adding a `CONTRIBUTING.md` for community archaeology contributions
5. Establish whether `archive/original-pixelpost/` (currently untracked) should be published — this requires completed provenance records in `archive/provenance/`

### Ongoing

1. All new archaeology documents should carry explicit epistemic labels
2. Operational session logs (VPS commands, internal infrastructure) belong in `turquoise-ai-infra`, not here
3. This repository's public documents should be scoped to: archaeology, source analysis, historical research, preservation tooling — never infrastructure operations

---

*Audit conducted 2026-05-30. Repository remains private pending checklist completion.*
