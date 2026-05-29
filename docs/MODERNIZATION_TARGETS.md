# Modernization Targets

This is not an implementation plan. It is a risk-ranked map for later continuity work.

## Preserve First

- Keep raw archives immutable.
- Keep a behavior test corpus from the original.
- Preserve default templates and bundled docs.
- Preserve URL behavior and template tags before internal rewrites.

## Highest Risk Targets

- Database API: replace `mysql_*` through a compatibility layer before larger changes.
- Regex API: replace `ereg*` and `split()` with equivalent PCRE/string behavior.
- Password storage: migrate MD5 hashes to modern password hashes on login.
- Upload validation: validate decoded images, extension, MIME, size, dimensions, and storage paths.
- SQL construction: parameterize all queries and review admin filters.
- Session/cookie security: modern cookie flags and CSRF defaults.

## Medium Risk Targets

- Strict SQL-mode compatible schema.
- Config file generation and secret handling.
- EXIF parser replacement or wrapper.
- Thumbnail memory limits and large camera-image handling.
- Addon isolation and trust model.
- Apache/mod_rewrite compatibility.

## Low Risk Targets

- Documentation cleanup.
- Local development container.
- Read-only archive browser.
- Static screenshots of original admin and front templates.

