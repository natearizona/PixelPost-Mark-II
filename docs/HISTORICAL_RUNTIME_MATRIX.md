# Historical Runtime Matrix

## Scope

This matrix tracks recovered Pixelpost releases and historically plausible runtime candidates. It is an archaeological record, not a modernization plan.

No Pixelpost source files were modified for these findings.

## Evidence Summary

Primary local evidence:

- `archive/original-pixelpost/extracted/pixelpost-1.7.3/ReadMe.txt`
- `archive/original-pixelpost/extracted/pixelpost-1.7.3/admin/install.php`
- `archive/original-pixelpost/extracted/pixelpost-1.7.3/includes/create_tables.php`
- `archive/original-pixelpost/extracted/pixelpost-1.7.3/doc/changelog.txt`
- raw archive metadata from `archive/original-pixelpost/raw/*.zip`

External reference evidence:

- OpenSourceCMS Pixelpost profile: `https://www.opensourcecms.com/pixelpost/`
- MySQL 5.0 date/time documentation: `https://documentation.help/MySQL-5.0/ch11s03.html`
- MySQL old temporal datatype note: `https://dev.mysql.com/blog-archive/mysql-8-0-removing-support-for-old-temporal-datatypes/`

## Matrix

| PixelPost Version | Release Date | PHP Version | MySQL Version | Status | Evidence Source |
| --- | --- | --- | --- | --- | --- |
| 1.3 | Archive file dates: 2004-11-10 to 2004-11-22 | Not fully audited yet | Not fully audited yet | Preserved locally; runtime not attempted in Phase 2 | `sourceforge_pixelpost_1.3.zip`; `admin/install.php` header says Pixelpost 1.3 |
| 1.4 | Archive file dates: 2005-03-29 to 2005-04-13 | PHP 4.3.0+ | MySQL 3.24.58+ | Preserved locally; runtime not attempted in Phase 2 | `ReadMe.txt`; `doc/changelog.txt`; `sourceforge_pixelpost_1.4.zip` |
| 1.4.1 | Archive file dates: 2005-04-20 to 2005-04-24 | PHP 4.3.0+ | MySQL 3.24.58+ | Preserved locally; runtime not attempted in Phase 2 | `pixelpost_1.4.1/ReadMe.txt`; `sourceforge_pixelpost_1.4.1.zip` |
| 1.4.2 | Archive file dates: 2005-07-15 to 2005-07-19 | PHP 4.3.0+ | MySQL 3.24.58+ | Preserved locally; known `TIMESTAMP(14)` appears in `includes/create_tables.php` | `pixelpost_1.4.2/ReadMe.txt`; `includes/create_tables.php:188`; `sourceforge_pixelpost_1.4.2.zip` |
| 1.7.3 | Archive internal dates: 2009-09-02; external profile lists latest stable release date 09/02/2009 | Official docs: PHP 4.3.0+; installer check: PHP >= 4.3.3; tested with PHP 5.6 | Official docs: MySQL 3.24.58+; external profile says MySQL 3.23.58+; tested with MariaDB 10.3, MySQL 5.5, MariaDB 5.5, MariaDB 5.5 MAXDB | Installer launches and config generation passes; database finalization fails on `TIMESTAMP(14)` in all tested DB containers | `ReadMe.txt:1`, `ReadMe.txt:70-73`, `admin/install.php:13`, `install-lang-english.php:199`, `includes/create_tables.php:126`, OpenSourceCMS |

## Runtime Candidate Results

| Candidate | Container Status | Installer Launch | Config Generation | Database Initialization | Notes |
| --- | --- | --- | --- | --- | --- |
| PHP 5.6 + MariaDB 10.3 | Built and ran | Pass | Pass | Fail | `TIMESTAMP(14)` rejected: precision maximum 6 |
| PHP 5.6 + MySQL 5.5 | Pulled and ran | Pass | Pass | Fail | `TIMESTAMP(14)` rejected as SQL syntax near `(14)` |
| PHP 5.6 + MariaDB 5.5 | Pulled and ran | Pass | Pass | Fail | `TIMESTAMP(14)` rejected: precision maximum 6 |
| PHP 5.6 + MariaDB 5.5 + MAXDB SQL mode | Ran with `MAXDB` active | Pass | Pass | Fail | MySQL-compatible `MAXDB` mode did not alter MariaDB 5.5 behavior enough to accept `TIMESTAMP(14)` |
| MySQL 4.x official image | Not available | Not attempted | Not attempted | Not attempted | `mysql:4`, `mysql:4.1` not found |
| MySQL 5.0 official/vendor image | Not available | Not attempted | Not attempted | Not attempted | `mysql:5.0`, `mysql/mysql-server:5.0` not found |
| MySQL 5.1 official/vendor image | Not available | Not attempted | Not attempted | Not attempted | `mysql:5.1`, `mysql/mysql-server:5.1` not found |

## Current Recommendation

The next historically accurate candidate should be a containerized MySQL 4.0 or Oracle MySQL 5.0 runtime, preferably built from verifiable archival packages or source with recorded provenance.

Do not patch Pixelpost source until this runtime gap is understood.
