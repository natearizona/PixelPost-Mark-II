# TIMESTAMP(14) Forensics

## Finding

Pixelpost 1.7.3 database initialization fails at:

```text
includes/create_tables.php:126
`upgrade_date` TIMESTAMP(14) NOT NULL
```

This is not evidence of source corruption. It is evidence that the current database runtime is newer or behaviorally different from the MySQL runtime assumptions embedded in Pixelpost.

## Local Source Evidence

Pixelpost 1.7.3 creates the version table during the installer finalize step:

```text
CREATE TABLE IF NOT EXISTS `{$prefix}version` (
  `id` INT(10) unsigned NOT NULL auto_increment,
  `upgrade_date` TIMESTAMP(14) NOT NULL,
  `version` FLOAT NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `version` (`version`)
)
```

The same syntax appears in the recovered Pixelpost 1.4.2 tree:

```text
pixelpost_1.4.2/includes/create_tables.php:188
`upgrade_date` timestamp(14) NOT NULL
```

That means `TIMESTAMP(14)` is not an accidental 1.7.3-only artifact. It belongs to Pixelpost's historical upgrade lineage.

## MySQL Historical Context

MySQL 5.0 documentation says `TIMESTAMP` behavior varies by MySQL version and SQL mode. It also explicitly notes that pre-4.1 `TIMESTAMP` behavior differed significantly and points readers to the MySQL 3.23/4.0/4.1 manuals for old behavior.

The same MySQL 5.0 documentation states that, as of MySQL 4.1-style behavior, `TIMESTAMP` display width is fixed at 19 characters in `YYYY-MM-DD HH:MM:SS` format.

The important inference:

- `TIMESTAMP(14)` likely originated as an old MySQL display-width form, where `14` represented compact `YYYYMMDDHHMMSS` behavior.
- Pixelpost retained that schema syntax into later releases.
- Newer engines may reinterpret the number as fractional-second precision or reject it entirely.

MySQL 5.6 introduced fractional-second precision for temporal types up to 6 digits. Oracle's later MySQL notes describe old temporal types as a legacy format from MySQL 5.5 and below, deprecated since MySQL 5.6 and removed as an in-place-upgrade path in MySQL 8.0.

## Runtime Evidence From PixelPost Restoration Lab

All tests were run inside the isolated PixelPost Restoration Lab:

```text
/opt/pixelpost-restoration-lab
```

Security controls remained in place:

```text
127.0.0.1:18080 only
traefik.enable=false
no public DNS
no firewall change
archive-readonly untouched
```

### MariaDB 10.3

Result:

```text
MySQL Error: Too big precision 14 specified for 'upgrade_date'. Maximum is 6
```

### MySQL 5.5

Result:

```text
MySQL Error: You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near '(14) NOT NULL,
                 `version` FLOAT NOT NULL DEFAULT '0',
```

### MariaDB 5.5

Result:

```text
MySQL Error: Too big precision 14 specified for 'upgrade_date'. Maximum is 6.
```

### MariaDB 5.5 With MAXDB SQL Mode

The server was confirmed running with `MAXDB` in `@@sql_mode`:

```text
PIPES_AS_CONCAT,ANSI_QUOTES,IGNORE_SPACE,MAXDB,NO_KEY_OPTIONS,NO_TABLE_OPTIONS,NO_FIELD_OPTIONS,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION
```

Result:

```text
MySQL Error: Too big precision 14 specified for 'upgrade_date'. Maximum is 6.
```

This means MariaDB 5.5's MAXDB mode did not provide a sufficient compatibility bridge for Pixelpost's `TIMESTAMP(14)` schema.

## Container Availability Findings

The following official or vendor image references were not available:

```text
mysql:4
mysql:4.1
mysql:5.0
mysql:5.1
mysql/mysql-server:5.0
mysql/mysql-server:5.1
```

The following images were available and tested:

```text
mysql:5.5
mariadb:5.5
mariadb:10.3
```

## Conclusion

`TIMESTAMP(14)` is a historical MySQL compatibility artifact. Pixelpost appears to rely on behavior from MySQL 3.23/4.0/early-4.x lineage, or at least from a MySQL family version that tolerated old timestamp display-width syntax.

Modern MariaDB/MySQL containers tested so far do not accept it during fresh schema creation.

## Preservation Recommendation

Do not patch `includes/create_tables.php` yet.

Next steps should be:

1. Locate or build a provenance-recorded MySQL 4.0 or Oracle MySQL 5.0 container.
2. Rerun the installer without source changes.
3. Only if historical runtime reconstruction fails, define a minimal restoration shim in a cloned workspace and document it as compatibility work, not preservation.

## Sources

- Local: `archive/original-pixelpost/extracted/pixelpost-1.7.3/includes/create_tables.php`
- Local: `archive/original-pixelpost/extracted/pixelpost-1.4.2/pixelpost_1.4.2/includes/create_tables.php`
- MySQL 5.0 documentation: `https://documentation.help/MySQL-5.0/ch11s03.html`
- MySQL old temporal datatype note: `https://dev.mysql.com/blog-archive/mysql-8-0-removing-support-for-old-temporal-datatypes/`
