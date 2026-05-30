# Pixelpost 1.7.3 Runtime Inventory

## Restoration Lab Question

Can we make Pixelpost 1.7.3 run?

Based on source inspection alone: yes, likely, but not on a modern PHP 7/8 runtime and not against a modern strict MySQL/MariaDB runtime without either a historically compatible database or a later documented repair step.

This inventory does not patch Pixelpost. It identifies what the unmodified release appears to require before the next execution attempt.

## Release Under Test

- Release: Pixelpost 1.7.3.
- Source tree inspected: `archive/original-pixelpost/extracted/pixelpost-1.7.3/`.
- Raw archive inspected: `archive/original-pixelpost/raw/phpsources.net_Pixelpost-v1.7.3_435-3.zip`.
- Raw archive SHA-256: `0553abce0a647ff226d117de0893f903697910761aabf680fad5ce3ed693d98a`.

Evidence:

- `admin/install.php:13` defines `PP_VERSION` as `1.73`.
- `admin/install/install_schema.php:62-67` upgrades through `1.71`, `1.72`, and `1.73`.

Evidence tier: R2 source evidence.

## Required PHP Version

### Findings

The installer requires PHP `>= 4.3.3` at runtime.

Evidence:

- `admin/install/install_functions.php:301-308` reads `phpversion()` and fails the requirement check when `version_compare($php_version, '4.3.3') < 0`.

### Compatibility Constraints From Source

The unmodified source uses APIs removed from modern PHP:

- `mysql_*` database API throughout core and addons.
- `ereg`, `eregi`, and `ereg_replace`.
- `split()`.
- string offset syntax using braces, for example `$path{...}`.
- `get_magic_quotes_gpc()`.

Evidence:

- `includes/functions.php:504-513` uses `mysql_connect()` and `mysql_select_db()`.
- `includes/functions.php:764-767` uses `mysql_list_fields()`, `mysql_num_fields()`, and `mysql_field_name()`.
- `index.php:93`, `index.php:248`, `index.php:776-822`, and `includes/functions_exif.php:134-224` use `eregi_replace()`, `ereg()`, and `ereg_replace()`.
- `index.php:880`, `admin/new_image.php:117`, and `includes/functions.php:537` use `split()`.
- `includes/functions.php:16` uses brace-style string offset syntax.
- `admin/options.php:26`, `admin/options.php:117`, and `admin/options.php:149` call `get_magic_quotes_gpc()`.

### Likely Runtime Candidate

Assumption R4: PHP 5.2.x or PHP 5.3.x is the strongest first candidate for unmodified execution because it still supports the legacy `mysql_*`, `ereg*`, and `split()` APIs while being newer than the installer minimum. PHP 5.4+ is riskier because deprecated behavior becomes noisier and magic-quotes assumptions diverge further. PHP 7+ and PHP 8+ are not viable for unmodified first boot.

## Required PHP Extensions

### mysql Extension

Required for all database work.

Evidence:

- `admin/install.php:31-33` uses `mysql_connect()` and `mysql_select_db()` before loading schema code.
- `admin/install/install_functions.php:503-510` tests DB credentials with `mysql_connect()` and `mysql_select_db()`.
- `includes/functions.php:492-520` centralizes runtime DB bootstrap around `mysql_connect()` and `mysql_select_db()`.

Evidence tier: R2.

### GD Extension With JPEG Support

Required for installer pass status and thumbnail generation.

Evidence:

- `admin/install/install_functions.php:354-364` requires `gd_info()`.
- `includes/functions.php:203-214` attempts `imagecreatefromjpeg()`, `imagecreatefrompng()`, and `imagecreatefromgif()`.
- `includes/functions.php:226-267` creates truecolor images, resamples/resizes, writes thumbnails with `imagejpeg()`, and chmods the thumbnail file.
- `admin/new_image.php:421-430` only calls `createthumbnail()` when `gd_info()` exists.

Evidence tier: R2.

### PCRE With UTF-8 Support

Required by installer requirement checks and tag handling.

Evidence:

- `admin/install/install_functions.php:341-348` checks `preg_match('//u', '')`.
- `includes/functions.php:1458-1467` uses Unicode-aware tag cleanup with a `/u` regex and falls back when it fails.

Evidence tier: R2.

### Standard Fileinfo Is Not Required By Source

No source requirement for PHP `fileinfo` was found. Upload validation relies on PHP upload metadata, filename cleanup, and GD/EXIF processing rather than MIME verification.

Evidence:

- `admin/new_image.php:78-99` normalizes the uploaded filename, moves it, records `$_FILES['userfile']['type']`, and checks PHP upload error codes.

Evidence tier: R2.

### XML Parser Support

Likely required only if XML-RPC functionality or related bundled code is exercised.

Evidence:

- `includes/IXR_Library.inc:147-160` uses `xml_parser_create()`, `xml_parser_set_option()`, `xml_set_object()`, `xml_set_element_handler()`, `xml_set_character_data_handler()`, `xml_parse()`, and `xml_parser_free()`.

Evidence tier: R2.

### mail Function

Used for installer credential email and comment/admin email workflows.

Evidence:

- `admin/install/install_functions.php:676-725` builds and sends an installer email with `mail()`.
- `includes/functions_comments.php:232-267` sends comment notification emails with `mail()`.

Evidence tier: R2.

## Database Driver And Server Requirements

### Driver

The application requires PHP's legacy `mysql` extension. It does not use mysqli or PDO.

Evidence:

- Direct use of `mysql_connect()`, `mysql_select_db()`, `mysql_query()`, `mysql_fetch_array()`, `mysql_fetch_row()`, `mysql_insert_id()`, `mysql_real_escape_string()`, `mysql_escape_string()`, and `mysql_list_fields()` throughout core files.

Evidence tier: R2.

### Database Server

The schema requires an old MySQL-compatible server or compatibility mode.

Evidence:

- `includes/create_tables.php:124-129` creates `{prefix}version` with `upgrade_date TIMESTAMP(14) NOT NULL`.
- `includes/create_tables.php:49`, `includes/create_tables.php:62`, and `includes/create_tables.php:74` define `DATETIME NOT NULL DEFAULT '0000-00-00 00:00:00'`.
- `admin/install/install_schema.php:8-67` runs the fresh install through the historical upgrade chain, so fresh install must execute this legacy schema path.

Evidence tier: R2.

Assumption R4: MySQL 4.1 or MySQL 5.0 should be tested before patching because the source expects syntax and default behavior from that era. A permissive MySQL 5.1/5.5 runtime may partially work but has already shown risk around `TIMESTAMP(14)` in lab testing.

## Image Processing Requirements

### Supported Input Extensions

Thumbnail creation directly handles these extensions:

- `jpg`
- `jpeg`
- `png`
- `gif`

Evidence:

- `includes/functions.php:203-214` branches to `imagecreatefromjpeg()`, `imagecreatefrompng()`, or `imagecreatefromgif()` based on file extension.

Evidence tier: R2.

### Thumbnail Output

Thumbnails are always written through `imagejpeg()` as `thumb_{filename}` in the configured thumbnail directory.

Evidence:

- `includes/functions.php:264-267` touches `thumbnailpath/thumb_$file`, writes it with `imagejpeg()`, then chmods it to `0644`.

Evidence tier: R2.

### Crop Support

The default thumbnail function supports crop modes `yes` and `12c`. The `12c` crop path has additional include and JavaScript files.

Evidence:

- `includes/functions.php:245-262` handles crop modes `yes` and `12c`.
- `admin/new_image.php:433-466` branches into the `12c` crop display workflow.
- `includes/12cropimageinc.php:99-107` and `includes/12cropimageinc.php:142-170` use the same GD image creation/resampling functions for crop editing.

Evidence tier: R2.

## EXIF Requirements

Pixelpost does not rely on PHP's native EXIF extension in the inspected path. It includes a bundled EXIF reader and calls `read_exif_data_raw()`.

Evidence:

- `includes/functions_exif.php:10-12` includes `../includes/exifer1_5/exif.php` when running in the admin panel.
- `includes/functions_exif.php:29-51` calls `read_exif_data_raw($uploaded_file,0)`, flattens the result, serializes it, and escapes it for MySQL.
- `admin/new_image.php:102-118` includes `functions_exif.php`, serializes EXIF on upload, and can derive post date from `DateTimeOriginalSubIFD`.
- `includes/functions_exif.php:65-224` renders EXIF values into template tags.

Evidence tier: R2.

Runtime risk:

- `serialize_exif()` assumes `read_exif_data_raw()` returns an array. Execution must verify behavior for images without EXIF.
- EXIF storage requires an active MySQL connection because `mysql_real_escape_string()` is called inside `serialize_exif()`.

## Filesystem Write Paths

### Required Writable Paths

- `images/`
- `thumbnails/`
- `includes/` during config-file generation, unless the downloaded config path is used.

Evidence:

- `admin/install/install_functions.php:370-388` checks/creates/writes `../images/`.
- `admin/install/install_functions.php:394-412` checks/creates/writes `../thumbnails/`.
- `admin/install/install_functions.php:1097-1331` writes `../includes/pixelpost.php`.
- `includes/functions.php:35-52` creates missing directories or chmods existing directories to `0777` when needed.
- `admin/new_image.php:92-95` moves uploaded files to the configured image path and chmods them to `0644`.
- `includes/functions.php:264-267` writes thumbnails and chmods them to `0644`.

Evidence tier: R2.

### Config File Path

Pixelpost expects database configuration at `includes/pixelpost.php`.

Evidence:

- `admin/index.php` redirects to installer when `../includes/pixelpost.php` is missing.
- `admin/install.php:23-35` loads `../includes/pixelpost.php` if present.
- `admin/install.php:58-65` can generate `pixelpost.php` for download.
- `includes/pixelpost-sample.php:43-48` shows required variables: DB host, DB user, DB password, DB name, and table prefix.

Evidence tier: R2.

## Installer Assumptions

### Installer Flow

The installer is browser-driven and form-based.

Evidence:

- `admin/install.php:13` sets the target version.
- `admin/install.php:58-65` handles downloadable config generation.
- `admin/install.php:800-811` finalizes by requiring `install/install_schema.php`, then stores settings when installed version is nonzero.
- `admin/install/install_schema.php:8-67` uses a fall-through switch from current version to `1.73`.

Evidence tier: R2.

### Requirement Checks

The installer checks:

- PHP version >= 4.3.3.
- `register_globals` setting.
- `getimagesize()`.
- PCRE UTF-8 support.
- `gd_info()`.
- `images/` and `thumbnails/` exist and are writable.
- MySQL connection and database selection.

Evidence:

- `admin/install/install_functions.php:295-422` performs PHP/GD/PCRE/filesystem checks.
- `admin/install/install_functions.php:457-519` validates DB host/name/prefix and tests MySQL connection.

Evidence tier: R2.

## Apache And `.htaccess` Assumptions

No `.htaccess` file was found in the inspected Pixelpost 1.7.3 source tree.

Findings:

- Public routing is handled by `index.php` and query parameters.
- Optional rewrite behavior exists as a `$mod_rewrite` variable, but no rewrite file was found in the source tree.

Evidence:

- `index.php:134` changes `$showprefix` when `$mod_rewrite == "1"`.
- Source tree search found no `.htaccess` file.

Evidence tier: R2 for source behavior; R4 for any web-server rewrite behavior until runtime-tested.

## Known Runtime Dependencies

### Required For Core First Boot

- Web server capable of running old PHP as Apache module or CGI/FastCGI.
- PHP 5.2/5.3 candidate with:
  - `mysql`,
  - `gd` with JPEG support,
  - PCRE UTF-8,
  - sessions,
  - standard filesystem functions,
  - `mail()` available or harmless if unconfigured.
- MySQL-compatible database accepting legacy schema syntax.
- Writable workspace copies of `images/`, `thumbnails/`, and `includes/`.

### Required Only For Specific Features Or Addons

- XML parser functions for bundled IXR XML-RPC library.
- Outbound sockets for Akismet/XML-RPC style calls.
- External `curl` binary may be used by bundled Defensio/Snoopy code if those addons are enabled.

Evidence:

- `includes/IXR_Library.inc:147-160` uses XML parser functions.
- `includes/IXR_Library.inc:508` uses `fsockopen()`.
- `addons/_akismet/front_akismet_comment.php:66` uses `fsockopen()`.
- `addons/_defensio/libraries/Snoopy.class.php:91-96` refers to `/usr/local/bin/curl`, and `Snoopy.class.php:1016` executes curl when that path is used.

Evidence tier: R2.

## Immediate Compatibility Risks

### PHP Blockers

- PHP 7/8 cannot run unmodified source because `mysql_*`, `ereg*`, and `split()` are removed.
- PHP 8 cannot parse brace string offsets such as `$path{strlen($path)-1}`.

Evidence:

- `includes/functions.php:16`.
- `includes/functions.php:504-513`.
- `index.php:93`, `index.php:248`, `index.php:776-822`.
- `admin/new_image.php:117`.

Evidence tier: R2.

### Database Blockers

- `TIMESTAMP(14)` in the version table is a known schema compatibility risk.
- Zero-date defaults may fail under strict SQL modes.

Evidence:

- `includes/create_tables.php:124-129`.
- `includes/create_tables.php:49`, `includes/create_tables.php:62`, `includes/create_tables.php:74`.

Evidence tier: R2.

### Filesystem Blockers

- If `includes/`, `images/`, or `thumbnails/` are not writable in a disposable workspace, installer/config/upload/thumbnail flows will fail.

Evidence:

- `admin/install/install_functions.php:370-412`.
- `admin/install/install_functions.php:1219-1323`.
- `admin/new_image.php:92-95`.
- `includes/functions.php:264-267`.

Evidence tier: R2.

## Likely Runtime Candidates

These are assumptions until tested.

### Candidate A: PHP 5.2 + Apache + MySQL 4.1

R4 assumption. Strong first candidate for unmodified execution because it should retain legacy PHP APIs and has a better chance of accepting old MySQL timestamp syntax.

### Candidate B: PHP 5.2 + Apache + MySQL 5.0

R4 assumption. Also likely plausible for unmodified execution. This should be tested if MySQL 4.1 images are unavailable or unstable.

### Candidate C: PHP 5.3 + Apache + MySQL 5.0

R4 assumption. May run source APIs but could surface more warnings. Use after PHP 5.2 candidates.

### Candidate D: PHP 5.6 + Apache + MariaDB/MySQL 5.5

R1/R2 mixed status from prior lab work: installer can boot far enough to expose DB schema failure, but this is not a clean unmodified first-boot success path because the DB rejects `TIMESTAMP(14)`.

## Next Executable Blocker

The next blocker to resolve by execution is database schema initialization for unmodified Pixelpost 1.7.3:

```sql
`upgrade_date` TIMESTAMP(14) NOT NULL
```

Source location:

- `includes/create_tables.php:124-129`.

Required next test:

1. create a disposable workspace copy of Pixelpost 1.7.3,
2. run it with PHP 5.2 or PHP 5.3 plus legacy `mysql` extension,
3. pair it with MySQL 4.1 first, then MySQL 5.0 if needed,
4. attempt installer finalization without patching source,
5. record whether schema creation reaches version `1.73`.

## Final Answer

Can we make Pixelpost 1.7.3 run?

Source inspection says: likely yes, but the unmodified release needs a legacy runtime. The first credible execution target is PHP 5.2 with Apache and MySQL 4.1 or 5.0, GD/JPEG enabled, PCRE UTF-8 available, writable `images/`, `thumbnails/`, and `includes/`, and no public exposure.

The next executable blocker is not PHP routing or installer discovery. It is the database runtime: find the earliest containerized MySQL version that accepts the unmodified schema chain through `TIMESTAMP(14)` and reaches Pixelpost version `1.73`.
