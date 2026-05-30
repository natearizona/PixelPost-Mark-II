# Installer Analysis

## Scope

This document describes the Pixelpost 1.7.3 installer and upgrade system as recovered. It also records the architectural implications of the observed `TIMESTAMP(14)` runtime mismatch.

Evidence files:

- `admin/install.php`
- `admin/install/install_functions.php`
- `admin/install/install_schema.php`
- `includes/create_tables.php`
- `includes/functions.php`

## Subsystem Purpose

The installer performs three jobs:

1. guide a new administrator through environment checks and setup,
2. create the database schema and configuration file,
3. upgrade older Pixelpost schemas forward to the current release version.

It is both a first-run wizard and a historical migration runner.

## Major Files Involved

- `admin/install.php`: main installer controller and HTML output.
- `admin/install/install_functions.php`: language handling, hidden form persistence, requirement checks, DB checks, admin/settings validation, configuration generation, addon upgrade helpers.
- `admin/install/install_schema.php`: fall-through switch that calls schema creation/upgrade functions.
- `includes/create_tables.php`: actual schema creation and upgrade functions.
- `includes/pixelpost.php`: generated config file containing database connection values.

## Execution Flow

### Fresh Install

1. `admin/install.php` defines `PP_INSTALL` and `PP_VERSION` as `1.73`.
2. If `../includes/pixelpost.php` exists, the installer tries to connect to MySQL and determine the installed version.
3. If installed version equals `1.73`, the installer redirects to `admin/index.php`.
4. The fresh install UI proceeds through:
   - overview/introduction/license/support,
   - install introduction,
   - requirements,
   - database,
   - administrator,
   - settings,
   - configuration,
   - finalize.
5. Requirement checks verify PHP version, `register_globals` state, `getimagesize`, PCRE UTF-8, GD, and writable `images/` and `thumbnails/`.
6. Database details are tested with `mysql_connect()` and `mysql_select_db()`.
7. Administrator details are validated and carried through hidden fields.
8. Site settings are validated, including trailing slash on the site URL.
9. The installer creates or offers for download `includes/pixelpost.php`.
10. Finalization includes `install_schema.php`, which creates the base v1.3 tables and falls through all upgrade functions until version 1.73.

### Upgrade

1. Existing config is loaded.
2. Current installed version is read from `{prefix}version` when available, or inferred from older config.
3. `install_schema.php` switches on the installed version.
4. Cases deliberately fall through so an old install receives every later upgrade step in sequence.
5. Addons are temporarily deactivated/reactivated during later upgrades.

## Database Interactions

The installer creates and migrates:

- `{prefix}config`
- `{prefix}categories`
- `{prefix}pixelpost`
- `{prefix}comments`
- `{prefix}visitors`
- `{prefix}version`
- `{prefix}catassoc`
- `{prefix}addons`
- `{prefix}tags`

It also writes default values such as:

- template: `simple`
- image path: `../images/`
- thumbnail path: `../thumbnails/`
- title: `Pixelpost`
- subtitle/feed description: `Authentic photoblog flavour`
- default category: `default`

## Configuration File Generation

The installer collects DB host, name, user, password, and table prefix, then writes a PHP config file. Sensitive fields are carried between installer steps using base64 encoding with fixed salt strings and a trailing `+` marker. This is obfuscation for form persistence, not cryptographic protection.

If the config file cannot be written directly, the installer can send it as a download named `pixelpost.php`.

## Runtime Mismatch Evidence

The restoration lab reached installer/database finalization and failed on:

```sql
`upgrade_date` TIMESTAMP(14) NOT NULL
```

This statement appears in `includes/create_tables.php` inside `UpgradeTo14()`, where the version table is created. The failure is significant because it occurs before any Pixelpost source modification. It indicates a database runtime mismatch: the recovered source expects an older MySQL syntax accepted in the historical target environment.

## Original Developer Assumptions

- PHP 4.3.3 or newer is present.
- The legacy `mysql_*` extension is available.
- The database accepts historical MySQL syntax such as `TIMESTAMP(14)`.
- The web server process can create or chmod directories and write `includes/pixelpost.php`.
- The administrator can manually upload a generated config file if automatic writing fails.
- Upgrade history can be encoded as imperative PHP functions instead of declarative migrations.
- Addons may need to be disabled during upgrades to avoid runtime breakage.

## Strengths

- The installer is self-contained and approachable.
- It performs practical shared-hosting checks that mattered to the original audience.
- It supports multilingual installation.
- It includes a config-download fallback for hosts where PHP cannot write files.
- The fall-through upgrade chain preserves a visible release lineage.

## Weaknesses

- Fresh install depends on an old schema plus every historical upgrade step.
- One incompatible historical SQL statement can block the entire install.
- Requirement checks do not account for modern PHP/MySQL incompatibilities.
- Credentials and admin passwords are carried through POST hidden fields.
- Schema migration logic is procedural and hard to replay safely outside the original runtime assumptions.

## Historical Context

The installer reflects shared hosting culture: FTP upload, browser-based setup, writable directories, MySQL credentials from a hosting control panel, and optional manual config-file upload. It was designed to make photoblogging accessible to photographers who were not necessarily programmers.

The restoration lesson is clear: installer behavior is part of the artifact. Before patching schema syntax, Mark II should document what runtime Pixelpost expected and why that runtime accepted it.
