# Evidence Directory

This directory holds primary evidence from Pixelpost restoration testing.

## What belongs here

- Raw test output: logs, installer responses, database errors, HTTP traces
- Image acquisition records: which images were pulled, which failed, and why
- Compatibility results: pass/fail outcomes from installer and schema tests
- Browser validation captures: screenshots and HTML captures from live installer sessions
- Schema dumps: database state after installer execution

## What does not belong here

- SSH commands targeting a specific server
- SCP commands or paths referencing a production or lab server
- Hostnames, IP addresses, or internal filesystem paths

The rule: evidence shows what Pixelpost did. It does not show where the test was executed or how files moved between machines.

Operational records — server sessions, deployment logs, infrastructure commands — belong in the private operational archive, not here.

## Evidence Subdirectories

| Directory | Contents |
| --- | --- |
| `1.7.3-database-compatibility/` | Schema compatibility test logs for MySQL 5.5 and MariaDB 5.5 |
| `1.7.3-historical-runtime/` | Historical MySQL runtime acquisition logs and installer-chain results |
| `1.7.3-browser-validation/` | Browser-level installer session screenshots and HTTP captures |
| `1.7.3-repeatability/` | Repeatability validation output and schema dump |
| `1.7.3-historical-import/` | Historical artifact search results |
