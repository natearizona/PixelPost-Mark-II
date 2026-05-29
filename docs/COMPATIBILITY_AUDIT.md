# Compatibility Audit

## PHP 8.2+ Breakages

High-confidence breakages:

- `mysql_*` functions were removed in PHP 7.0.
- `ereg()`, `eregi()`, and `eregi_replace()` were removed in PHP 7.0.
- `split()` was removed in PHP 7.0.
- String offset access with curly braces, such as `$path{...}`, is invalid in PHP 8.
- Unquoted constants such as `define(IMAGE_BASE, ...)` rely on legacy behavior and break under modern PHP.
- Many uses of undefined indexes and variables are hidden by `error_reporting(0)` but become noisy or fatal depending on PHP version and error handling.

Likely compatibility issues:

- Bundled `IXR_Library.inc` uses `$HTTP_RAW_POST_DATA`, removed in modern PHP.
- Old EXIF parser code uses removed regex APIs.
- Functions and addons assume pass-by-global procedural state rather than dependency boundaries.

## MySQL/MariaDB Issues

- Requires migration from `mysql_*` to `mysqli` or PDO.
- `0000-00-00 00:00:00` defaults break under strict mode.
- Old timestamp definitions and implicit defaults need review.
- SQL is built by string concatenation; escaping is inconsistent.
- Authenticated admin SQL injection vulnerabilities were publicly reported for Pixelpost 1.7.3.

## Security Concerns

- Admin password is MD5-hashed.
- Remember-me cookie is `sha1(md5_password + REMOTE_ADDR)`.
- Sessions do not use modern cookie attributes.
- CSRF token support exists but is optional and MD5-based.
- Upload handling needs content validation, image decoding safeguards, and extension allowlists.
- Addons execute arbitrary PHP from the filesystem.
- Several security advisories cite SQL injection, XSS, path traversal, and remote code execution risks in Pixelpost 1.7.3 or earlier.

## Minimal Intervention Recommendations

For the next phase, do not redesign. Build a compatibility harness first:

- Record expected behavior with fixtures from the archived source.
- Add a modern PHP runtime smoke-test matrix.
- Catalog all deprecated function calls by file.
- Create a database schema dump after clean install and after upgrade path.
- Create upload fixtures for JPEG, PNG, GIF, large images, EXIF/no-EXIF images, and suspicious filenames.
- Preserve template tag output compatibility before replacing internals.

