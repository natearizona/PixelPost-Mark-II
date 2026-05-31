# Pixelpost 1.7.3 Database Compatibility

Question: Can unmodified Pixelpost 1.7.3 initialize its database through installer finalization version `1.73`?

Short answer: not with the practical legacy database images currently available in the lab. MariaDB 10.3, MySQL 5.5, MariaDB 5.5, and MariaDB 5.5 with MAXDB SQL mode all run the installer chain but fail when the unmodified source attempts to create `{prefix}version` with `upgrade_date TIMESTAMP(14) NOT NULL`. The MAXDB compatibility mode was tested as a potential workaround and confirmed not sufficient.

## Scope

This test used the recovered Pixelpost 1.7.3 source without editing PHP or SQL. Runtime testing occurred only in disposable workspace copies. The archive specimen remained read-only and untracked.

The installer chain under test was:

- `admin/install/install_schema.php`
- `includes/create_tables.php`
- target final version: `1.73`

Source-derived blocker:

- `includes/create_tables.php:124-129` creates `{prefix}version`.
- `includes/create_tables.php:126` defines `upgrade_date TIMESTAMP(14) NOT NULL`.
- `includes/create_tables.php:131` inserts initial version `1.4`; later upgrade functions continue toward `1.73`.

## Source And Runtime Identity

Recovered source:

- Release under test: Pixelpost 1.7.3
- Raw archive SHA-256: `0553abce0a647ff226d117de0893f903697910761aabf680fad5ce3ed693d98a`
- Archive tree SHA-256 captured by runner: `8498093b0f50c9f03cf56191cec1b9fb4f52649aac9451abf85682c6424bd05b`

PHP runtime:

- Lab image: `pixelpost-restoration-lab-pixelpost-php`
- PHP version observed by runner: `5.6.40`
- Extensions observed by runner: `mysql=yes`, `gd=yes`, `pcre_utf8=yes`
- Database client observed by runner: `mysqlnd 5.0.11-dev - 20120503`

PHP 5.2 was preferred but not available as an official Docker image. PHP 5.3 and PHP 5.4 official images could not be pulled by the current Docker/containerd runtime because their manifest format is no longer supported. PHP 5.6 with the legacy `mysql` extension is therefore the nearest practical web runtime currently available in the lab.

## Candidate Availability

| Candidate | Availability | Evidence |
| --- | --- | --- |
| MySQL 4.1 | Not tested | Official `mysql:4.1` image unavailable: tag not found. |
| MySQL 5.0 | Not tested | Official `mysql:5.0` image unavailable: tag not found. |
| MySQL 5.1 | Not tested | Official `mysql:5.1` image unavailable: tag not found. |
| MySQL 5.5 | Tested | Official `mysql:5.5`, digest `sha256:12da85ab88aedfdf39455872fb044f607c32fdc233cd59f1d26769fbf439b045`. |
| MariaDB 5.5 | Tested as fallback | Official `mariadb:5.5`, digest `sha256:8665c074af5a5fb7e04b9570fcf8551e9d82955182be50375d5013838d4f9137`. |
| MariaDB 5.5 + MAXDB mode | Tested as compatibility workaround | Same image as MariaDB 5.5 above; started with `--sql-mode=MAXDB,NO_ENGINE_SUBSTITUTION`. |
| MariaDB 10.3 | Tested as initial runtime candidate | Official `mariadb:10.3`, version `10.3.39-MariaDB-1:10.3.39+maria~ubu2004`. |

## Pass/Fail Matrix

| Database Version | PHP Version | Installer Loads | Schema Creates | Version 1.73 Reached | Result | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| MySQL 4.1 | Not tested | Not tested | Not tested | Not tested | Blocked | Official Docker image unavailable. A source-built or preserved binary runtime is needed. |
| MySQL 5.0 | Not tested | Not tested | Not tested | Not tested | Blocked | Official Docker image unavailable. A source-built or preserved binary runtime is needed. |
| MySQL 5.1 | Not tested | Not tested | Not tested | Not tested | Blocked | Official Docker image unavailable. A source-built or preserved binary runtime is needed. |
| MySQL 5.5.62 | PHP 5.6.40 | Yes | No | No | Fail | Installer chain runs until `{prefix}version`; MySQL rejects `TIMESTAMP(14)` as SQL syntax. |
| MariaDB 5.5.64 | PHP 5.6.40 | Yes | No | No | Fail | Installer chain runs until `{prefix}version`; MariaDB rejects precision 14 with maximum 6. |
| MariaDB 5.5.64 + MAXDB | PHP 5.6.40 | Yes | No | No | Fail | MAXDB mode active and verified; installer still fails at same `{prefix}version` line. MAXDB compatibility does not resolve `TIMESTAMP(14)`. |
| MariaDB 10.3.39 | PHP 5.6.40 | Yes | No | No | Fail | First runtime tested; installer chain runs through configuration step; fails at `{prefix}version` with same precision error. |

## MySQL 5.5 Result

Evidence file:

- `docs/restoration/evidence/1.7.3-database-compatibility/mysql55.log`

Observed database:

```text
version
5.5.62
sql_mode
```

Observed PHP/database connection:

```text
php_version=5.6.40
mysql_ext=yes
gd_ext=yes
pcre_utf8=yes
db_server=5.5.62
```

Observed failure:

```text
MySQL Error: You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near '(14) NOT NULL,
				 `version` FLOAT NOT NULL DEFAULT '0',
				 PRIMARY KEY  (`id' at line 3
```

Tables created before failure:

```text
pixelpost_categories
pixelpost_comments
pixelpost_config
pixelpost_pixelpost
pixelpost_visitors
```

Version table status:

```text
ERROR 1146 (42S02) at line 1: Table 'pixelpost.pixelpost_version' doesn't exist
```

Interpretation: MySQL 5.5 accepts enough of the installer to create early base tables, but rejects the unmodified version-table SQL. Installer finalization cannot proceed to `1.73`.

## MariaDB 5.5 Result

Evidence file:

- `docs/restoration/evidence/1.7.3-database-compatibility/mariadb55.log`

Observed database:

```text
version
5.5.64-MariaDB-1~trusty
sql_mode
```

Observed PHP/database connection:

```text
php_version=5.6.40
mysql_ext=yes
gd_ext=yes
pcre_utf8=yes
db_server=5.5.64-MariaDB-1~trusty
```

Observed failure:

```text
MySQL Error: Too big precision 14 specified for 'upgrade_date'. Maximum is 6.
```

Tables created before failure:

```text
pixelpost_categories
pixelpost_comments
pixelpost_config
pixelpost_pixelpost
pixelpost_visitors
```

Version table status:

```text
ERROR 1146 (42S02) at line 1: Table 'pixelpost.pixelpost_version' doesn't exist
```

Interpretation: MariaDB 5.5 behaves like the modern MariaDB failure already observed: it allows partial schema creation but rejects `TIMESTAMP(14)`.

## MariaDB 5.5 With MAXDB SQL Mode Result

SQL mode applied:

```text
--sql-mode=MAXDB,NO_ENGINE_SUBSTITUTION
```

Active mode verified before test:

```text
PIPES_AS_CONCAT,ANSI_QUOTES,IGNORE_SPACE,MAXDB,NO_KEY_OPTIONS,NO_TABLE_OPTIONS,NO_FIELD_OPTIONS,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION
```

Observed failure:

```text
MySQL Error: Too big precision 14 specified for 'upgrade_date'. Maximum is 6.
```

Interpretation: MAXDB compatibility mode was tested as a potential workaround for the `TIMESTAMP(14)` rejection. The mode was confirmed active. Installer launch and configuration generation passed. Full database finalization failed at the same `{prefix}version` line. MAXDB mode does not provide sufficient compatibility for the unmodified Pixelpost 1.7.3 schema.

## MariaDB 10.3 Result

Evidence: tested as the initial runtime candidate before lower-version fallbacks were attempted.

Observed database version:

```text
10.3.39-MariaDB-1:10.3.39+maria~ubu2004
```

Installer chain result:

- Requirements page: HTTP 200.
- Database credential test: HTTP 200.
- Administrator validation: HTTP 200.
- Settings validation: HTTP 200.
- Configuration step: HTTP 200; wrote `includes/pixelpost.php`.
- Finalize: HTTP 200; halted during schema creation.

Tables created before failure:

```text
pixelpost_categories
pixelpost_comments
pixelpost_config
pixelpost_pixelpost
pixelpost_visitors
```

Observed failure:

```text
MySQL Error: Too big precision 14 specified for 'upgrade_date'. Maximum is 6.
```

Source location confirmed:

```text
includes/create_tables.php:126
`upgrade_date` TIMESTAMP(14) NOT NULL
```

Interpretation: MariaDB 10.3 behavior is identical to MariaDB 5.5 for this failure path. The installer runs further than a completely incompatible runtime would, but the schema halts at `{prefix}version`. The error message and source location match every other tested modern or near-modern runtime.

## Runtime Warnings

The PHP runtime produced compatibility warnings before the database blocker:

```text
mysql_connect(): The mysql extension is deprecated
Function eregi_replace() is deprecated
Function ereg_replace() is deprecated
```

These warnings did not stop execution in the PHP 5.6 lab image. They are PHP compatibility evidence, but they are not the current executable blocker for schema initialization.

One runner warning appeared because the non-browser schema harness emitted text before installer code attempted a header redirect:

```text
Cannot modify header information - headers already sent
```

This is a harness artifact and not treated as the database initialization blocker.

## Exact Execution Pattern

For each tested candidate, the lab created:

- one internal Docker network
- one disposable database container with no published ports
- one disposable Pixelpost workspace copied from the read-only archive specimen
- one PHP runner container attached only to the candidate internal network

Representative execution:

```text
docker network create --internal pp-dbcompat-net-mysql55
docker run -d --name pp-dbcompat-mysql55 --network pp-dbcompat-net-mysql55 --network-alias db mysql:5.5
cp -a /opt/pixelpost-restoration-lab/archive-readonly/pixelpost-1.7.3/. /opt/pixelpost-restoration-lab/workspaces/dbcompat-1.7.3-mysql55/
docker run --rm --network pp-dbcompat-net-mysql55 -v /opt/pixelpost-restoration-lab/workspaces/dbcompat-1.7.3-mysql55:/work -v /opt/pixelpost-restoration-lab/reports/dbcompat-1.7.3-20260531T000320Z:/reports pixelpost-restoration-lab-pixelpost-php php /reports/schema-finalize-runner.php /work db pixelpost pixelpost pixelpostpass pixelpost_
```

## Required Final Answers

1. Which database runtime got farthest?

MySQL 5.5.62 and MariaDB 5.5.64 reached the same functional point: database connection succeeded, early schema tables were created, and the installer stopped at `{prefix}version`. MySQL 5.5 is the farthest historically aligned runtime currently tested because it is official MySQL rather than the MariaDB fallback.

2. Did any runtime accept the unmodified schema?

No. Neither tested runtime accepted the unmodified `TIMESTAMP(14)` definition.

3. Did installer finalization reach version `1.73`?

No. `{prefix}version` was not created, so the version chain could not reach `1.73`.

4. Is the blocker database-related, PHP-related, filesystem-related, or installer-related?

The current executable blocker is database-related. PHP emits deprecation warnings, but execution reaches the schema statement. Filesystem setup was sufficient for the schema test. Installer code is functioning far enough to expose the database incompatibility.

5. What is the next executable blocker?

The next blocker is acquisition or construction of a runnable MySQL 4.1, 5.0, or 5.1 container candidate that can be tested against the same unmodified Pixelpost 1.7.3 installer chain. If those older runtimes accept `TIMESTAMP(14)`, the next test should continue to installer finalization and confirm whether `{prefix}version` reaches `1.73`.
