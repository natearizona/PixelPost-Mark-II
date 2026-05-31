# Pixelpost 1.7.3 Browser First Boot

Question: Does the Pixelpost 1.7.3 browser installer function correctly on the verified MySQL 5.1 runtime?

Answer: yes. The installer loads in a browser, validates requirements, connects to MySQL 5.1.73, generates `includes/pixelpost.php` inside the disposable workspace, creates the schema, reaches version `1.73`, and redirects to the admin login page after completion.

## Runtime

- Pixelpost release: 1.7.3
- Database image: `ggmartinez/mysql:5.1`
- Database runtime: MySQL `5.1.73`
- PHP runtime: PHP `5.6.40`
- PHP extensions observed earlier and required here: `mysql`, `gd`, `exif`
- Access path: local browser to `127.0.0.1:18082` through SSH tunnel
- Docker exposure: no published public HTTP port, no Traefik

## Installer Results

| Step | Result | Evidence |
| --- | --- | --- |
| Introduction page loads | Pass | `screenshots/01-installer-introduction.png` |
| Requirements page loads | Pass | `screenshots/02-installer-requirements.png` |
| `images/` writable | Pass | Requirements page reports `Found, Writable` |
| `thumbnails/` writable | Pass | Requirements page reports `Found, Writable` |
| Database form loads | Pass | `screenshots/03-installer-database-empty.png` |
| Database connection succeeds | Pass | `screenshots/04-installer-database-ok.png` |
| Administrator form loads | Pass | `screenshots/05-installer-admin-empty.png` |
| Administrator validation succeeds | Pass | `screenshots/06-installer-admin-ok.png` |
| Settings form loads | Pass | `screenshots/07-installer-settings-empty.png` |
| Settings validation succeeds | Pass | `screenshots/08-installer-settings-ok.png` |
| Configuration generation succeeds | Pass | `screenshots/09-installer-configuration.png` |
| Schema finalization succeeds | Pass | `screenshots/10-installer-finalize.png` |
| Redirect to admin login after finish | Pass | `screenshots/11-after-finish.png` |
| Empty public front page renders | Pass | `screenshots/12-front-page-empty.png` |

## Configuration Evidence

The installer reported:

```text
Your configuration has been successfully created and saved. All tests have passed!
Open file: Passed
Write file: Passed
CHMOD file: Passed
Configuration exists: Found
Test connection: Connection Successful!
```

The finalizer reported:

```text
Create version table: Created
Update to 1.73: Updated
Finished
```

The database later confirmed:

```text
version
1.4
1.41
1.49995
1.59
1.6
1.7
1.71
1.72
1.73
```

## Warnings

PHP displayed historical compatibility warnings during browser installation:

```text
Function ereg_replace() is deprecated
Function eregi_replace() is deprecated
```

These warnings did not block the installer.

The finalizer also displayed:

```text
Notice: Undefined variable: admin_user in admin/install/install_functions.php on line 1017
```

This affected display of the username on the final credentials page only. Database evidence confirmed the administrator account was stored as `archivist`, and admin login succeeded.

## Result

Browser first boot passes. Pixelpost 1.7.3 can be installed through the original browser installer on the verified historical database runtime without modifying the recovered release.
