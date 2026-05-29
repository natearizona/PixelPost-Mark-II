# Installer Analysis

## Entry Flow

If `admin/index.php` cannot find `../includes/pixelpost.php`, it redirects to `install.php`.

The installer checks environment requirements, collects database/admin/site settings, attempts to create `includes/pixelpost.php`, connects to MySQL, creates or upgrades tables, and updates site configuration.

## Requirements

The included README documents:

- Apache or Windows IIS.
- PHP 4.3.0 or higher.
- GD with JPG support.
- MySQL 3.24.58 or higher.
- Existing MySQL database credentials.

Installer checks include PHP version, GD support, MySQL connection, writable directories, and `register_globals` status.

## Config File Behavior

The installer writes `includes/pixelpost.php` containing database host, user, password, database name, and table prefix. If the directory is not writable, it attempts to chmod the config directory. It can also return config data for manual download.

## Upgrade Behavior

The installer uses a fall-through `switch($installed_version)` chain. A clean install starts at version `0`, creates v1.3 tables, then falls through each upgrade step until v1.73. Existing installs enter the chain from their detected version.

## Preservation Concerns

The install flow is historically important because Pixelpost targeted ordinary shared hosting. Its low ceremony is part of the product philosophy. However, the exact chmod/config-write behavior is not safe to carry forward unchanged.

