# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Project Is

**PixelPost Mark II** is a digital archaeology and continuation project for the historic Pixelpost photoblogging platform. It has two components:

1. **`markii/`** — A Python CLI toolkit for parsing, inventorying, and matching historical PixelPost data (media archaeology)
2. **`pixelpostii/`** — A modern Flask photoblog, spiritually successor to the original Pixelpost

The original Pixelpost artifacts in `archive/` are treated as preserved specimens — never modified.

## Commands

This project uses `uv` for Python environment management. All commands assume an active venv or `uv run` prefix.

```bash
# Run tests
pytest

# Run a single test file
pytest tests/test_pixelpostii_app.py

# Run a single test by name
pytest tests/test_pixelpostii_app.py::test_publish_post_redirects

# Run the modern photoblog app
pixelpostii
# or: python -m pixelpostii.app

# Run the archaeology CLI
markii --help
markii inventory-media <source-dir>
markii parse-pixelpost-xml <export.xml>
markii match-media
markii archive-inventory
markii write-matches

# Start the historical restoration environment (PHP 5.6 + MariaDB)
docker compose -f docker/pixelpost-restoration-lab.compose.yml up

# Start the modern containerized Pixelpost (historical PHP runtime)
docker compose -f docker/compose.pixelpost.yml up
```

## Environment Variables

**PixelPost II (modern app):**
- `PIXELPOSTII_SECRET` — Flask session secret (default: `dev-secret-change-me`)
- `PIXELPOSTII_PASSWORD` — Admin password for publishing (default: `darkroom`)
- `PORT` — HTTP port (default: `5001`)

**Historical Docker runtime:**
- See `docker/pixelpost.env.example` for `PIXELPOST_HTTP_PORT`, `PIXELPOST_WORKSPACE`, `PIXELPOST_PLATFORM`

## Architecture

### markii CLI (archaeology toolkit)

The data flow through the toolkit is linear and pipeline-oriented:

```
PixelPost XML export
  → parse-pixelpost-xml  →  Normalized records (posts, attachments, comments, categories, tags)
  → inventory-media      →  Artifact catalog (checksums, JPEG dimensions, EXIF)
  → match-media          →  Confidence-scored matches (exact / high / probable / ambiguous / unmatched)
  → write-matches        →  SQLite provenance archive
  → reports/             →  Markdown + JSON output
```

**Media Matching** (`markii/media/matcher.py`): Multi-signal confidence scoring using attachment filename, body `<img>` src, post parent, thumbnail rules, timestamp correlation, URL domain, and hash identity. The philosophy is "unresolved is better than wrong" — ambiguous matches are preserved, not forced.

**Provenance Archive** (`markii/storage/archive.py`): SQLite schema with `import_runs`, `source_artifacts`, and `provenance_events` tables. Foreign keys are enforced. Every match decision, orphan classification, and conflict resolution is recorded with who ran what, when.

CLI entry point: `markii/cli/main.py` → routes subcommands to modules in `markii/importers/`, `markii/media/`, `markii/provenance/`, `markii/reports/`.

### pixelpostii Flask app

Single-file app logic in `pixelpostii/app.py`. SQLite backend (WAL mode) via `pixelpostii/models/post.py`.

**Key design decisions:**
- One image required per post (image is mandatory)
- Slugs are auto-generated from title (lowercase, alphanumeric, hyphenated) and enforced unique in the DB
- Images stored with UUID filenames under an `uploads/` directory
- Homepage always shows the latest published post
- Chronological prev/next navigation only — no feeds, no tags, no search
- Single-user password auth via session (no accounts table)
- JPEG, PNG, GIF, WebP accepted; MIME type validated on upload

**Routes:** `/login`, `/logout`, `/` (latest post), `/post/<slug>`, `/new` (admin only)

### Testing

Tests live in `tests/`. The Flask app tests (`test_pixelpostii_app.py`) use a temporary SQLite database and upload folder per test, with mock JPEG bytes for upload tests. The 48-test suite covers the full nine-step publish workflow: auth, empty state, redirect on publish, persistence, draft visibility, validation (title/image/file type), slug uniqueness, single-post view, and prev/next navigation.

## Key Conventions

- **Confidence over completeness in matching:** The matcher must never force a low-confidence match. Unmatched/ambiguous results are valid and expected outputs.
- **Provenance is append-only:** Archive records capture history; existing records are not mutated.
- **SQLite WAL mode everywhere:** Both the archaeology archive and the Flask app enable `PRAGMA journal_mode=WAL` on every connection.
- **No external database required:** Both components run on SQLite; no Postgres or MySQL needed for development.
- **Historical PHP environment is read-only archaeology:** Changes to `archive/` or `docker/historical/` should preserve authenticity, not modernize.
