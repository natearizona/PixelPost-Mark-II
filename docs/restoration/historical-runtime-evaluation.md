# Historical Runtime Evaluation

Question: Can unmodified Pixelpost 1.7.3 complete installer initialization on a historically appropriate MySQL runtime?

Answer: yes. Unmodified Pixelpost 1.7.3 completed the installer schema chain on MySQL `5.1.73` and reached Pixelpost version `1.73`.

Classification: Category A, unmodified Pixelpost installs successfully on a historical runtime.

## Runtime Under Test

Successful database candidate:

- Image: `ggmartinez/mysql:5.1`
- Pulled digest: `sha256:db6468ed7a662a0efd5aee985b9e5a0c5b6c43732bc22c72a950624ba3349ba2`
- Runtime database version: `5.1.73`
- Observed `sql_mode`: empty
- Observed `old_passwords`: `OFF`

PHP runtime:

- Image: `pixelpost-restoration-lab-pixelpost-php`
- PHP version: `5.6.40`
- Legacy `mysql` extension: present
- GD extension: present
- PCRE UTF-8 support: present

Source specimen:

- Release: Pixelpost 1.7.3
- Raw archive SHA-256: `0553abce0a647ff226d117de0893f903697910761aabf680fad5ce3ed693d98a`
- Archive tree SHA-256 captured by runner: `8498093b0f50c9f03cf56191cec1b9fb4f52649aac9451abf85682c6424bd05b`

## Method

The test repeated the prior installer-chain method:

- copy read-only archive specimen into a disposable workspace
- generate `includes/pixelpost.php` only inside the disposable workspace copy
- start the database candidate on an internal Docker network
- bootstrap only the test database and test database user
- run the unmodified Pixelpost installer schema chain:
  - `includes/create_tables.php`
  - `admin/install/install_schema.php`
- inspect tables and `{prefix}version` after execution

No Pixelpost source files or SQL statements were patched.

## Result Matrix

| Candidate | Runtime Version | Database Ready | Accepts `TIMESTAMP(14)` | `{prefix}version` Created | Version `1.73` Reached | Result |
| --- | --- | --- | --- | --- | --- | --- |
| `kuborgh/mysql-5.0:latest` | Not reached | No | Not tested | No | No | Acquisition failure |
| `pixelpost-lab-mysql-5.0-kuborgh-user:latest` | Not reached | No | Not tested | No | No | Wrapper build succeeded, runtime still not ready |
| `ggmartinez/mysql:5.1` | MySQL `5.1.73` | Yes | Yes | Yes | Yes | Pass |
| `tommi2day/mysql51:latest` | Not reached | No | Not tested | No | No | Acquisition/init failure |

## Successful Installer Evidence

Evidence file:

- `docs/restoration/evidence/1.7.3-historical-runtime/mysql51-ggmartinez.log`

Database startup:

```text
version
5.1.73
sql_mode
old_passwords OFF
```

PHP/database connection:

```text
php_version=5.6.40
mysql_ext=yes
gd_ext=yes
pcre_utf8=yes
db_server=5.1.73
```

Installer finalization:

```text
installed_version_after_schema=1.73
installed_version_after_store_vars=1.73
```

Tables after installer-chain execution:

```text
pixelpost_addons
pixelpost_catassoc
pixelpost_categories
pixelpost_comments
pixelpost_config
pixelpost_pixelpost
pixelpost_tags
pixelpost_version
pixelpost_visitors
```

Version rows:

```text
1|2026-05-31 01:56:20|1.4
2|2026-05-31 01:56:20|1.41
3|2026-05-31 01:56:20|1.49995
4|2026-05-31 01:56:20|1.59
5|2026-05-31 01:56:20|1.6
6|2026-05-31 01:56:20|1.7
7|2026-05-31 01:56:20|1.71
8|2026-05-31 01:56:20|1.72
9|2026-05-31 01:56:20|1.73
```

## Warnings

PHP emitted compatibility warnings:

```text
mysql_connect(): The mysql extension is deprecated
Function eregi_replace() is deprecated
Function ereg_replace() is deprecated
```

These did not block installer finalization in the PHP 5.6 test runtime.

The runner also emitted:

```text
Cannot modify header information - headers already sent
```

This remains a non-browser harness artifact and did not block schema finalization.

## Final Questions

1. Can a historically aligned MySQL runtime be acquired reproducibly?

Yes. `ggmartinez/mysql:5.1` was acquired and pinned by digest `sha256:db6468ed7a662a0efd5aee985b9e5a0c5b6c43732bc22c72a950624ba3349ba2`. Runtime evidence identifies it as MySQL `5.1.73`.

2. Does that runtime accept `TIMESTAMP(14)`?

Yes. The schema chain completed past `{prefix}version` creation on MySQL `5.1.73`.

3. Does `{prefix}version` get created?

Yes. The resulting tables include `pixelpost_version`, and version rows were captured.

4. Does installer finalization reach version `1.73`?

Yes. The runner observed `installed_version_after_schema=1.73` and `installed_version_after_store_vars=1.73`.

5. Is Pixelpost 1.7.3 restorable without modifying the recovered release?

Yes for database initialization. The unmodified release can complete installer schema finalization on MySQL `5.1.73`. The next restoration step is browser-level first boot against this runtime: installer page, generated config behavior, admin login, upload, thumbnail generation, EXIF extraction, and theme rendering.
