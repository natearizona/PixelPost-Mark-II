# PixelPost Mark II

## A Preservation, Restoration, and Continuation Initiative

PixelPost Mark II is a long-term digital archaeology, preservation, restoration, and continuation project dedicated to the historic Pixelpost photoblogging platform.

## About Pixelpost

Pixelpost was a free, open-source photoblogging platform built with PHP and MySQL during the early 2000s. It allowed photographers to publish images, captions, categories, archives, and EXIF metadata on independently owned websites during a period when personal publishing was still decentralized.

Thousands of photographers used Pixelpost to create personal photoblogs focused on images rather than social engagement metrics. Development eventually ceased, leaving a large body of websites, templates, addons, and community knowledge scattered across the web.

PixelPost Mark II exists to preserve, document, and better understand that history.

## Current Status

PixelPost Mark II has completed its first archaeology and restoration cycle.

To date, the project has:

- Recovered and cataloged multiple historical PixelPost releases
- Established provenance, checksum, and preservation procedures
- Documented source architecture and runtime requirements
- Reconstructed historically appropriate runtime environments
- Restored PixelPost 1.7.3 to operational status
- Validated browser-based installation and configuration
- Confirmed image upload, thumbnail generation, and EXIF extraction
- Verified public theme rendering, archive rendering, and category rendering
- Demonstrated repeatable restoration from a clean environment

### Key Finding

PixelPost 1.7.3 successfully completes its original photoblogging workflow without source modification when operated on a verified historical runtime consisting of PHP 5.6.40 and MySQL 5.1.73.

### Current Focus

The project is now moving beyond initial restoration and into deeper historical validation, including:

- Earlier PixelPost release testing
- Historical database import workflows
- Comment system validation
- RSS and feed validation
- Addon and template preservation
- Recovery of surviving PixelPost community artifacts
- Reconstruction of historical photoblogs where archival evidence survives

Archaeology remains the priority. Modernization has not yet begun.

## Key Documents

Start here if you want to understand the restoration effort:

| Document | Purpose |
| --- | --- |
| [docs/README.md](docs/README.md) | Documentation index |
| [docs/restoration/historical-runtime-evaluation.md](docs/restoration/historical-runtime-evaluation.md) | Historical runtime findings |
| [docs/restoration/database-compatibility-1.7.3.md](docs/restoration/database-compatibility-1.7.3.md) | Compatibility matrix and failures |
| [docs/restoration/core-workflow-validation-1.7.3.md](docs/restoration/core-workflow-validation-1.7.3.md) | End-to-end workflow proof |
| [docs/restoration/repeatability-validation-1.7.3.md](docs/restoration/repeatability-validation-1.7.3.md) | Independent repeatability validation |

## Project Vision

PixelPost Mark II seeks to:

- Recover original Pixelpost releases
- Preserve source code and historical artifacts
- Document provenance and release history
- Reconstruct authentic runtime environments
- Restore operational versions of historical releases
- Preserve templates, addons, documentation, and community knowledge
- Study the evolution of photoblogging culture
- Build a sustainable continuation path for future generations

The objective is not merely to fork old code.

The objective is to understand Pixelpost completely before deciding how it should evolve.

## The Four Phases

### Phase I: Archaeology

Recover and catalog:

- Source releases
- Documentation
- Templates
- Addons
- Screenshots
- Forum archives
- Historical references
- Community contributions

### Phase II: Preservation

Establish:

- Provenance records
- Checksums
- Release lineage
- Chain-of-custody documentation
- Archival storage practices

Original artifacts are treated as preservation specimens and remain untouched whenever possible.

### Phase III: Restoration

Reconstruct historically accurate environments.

Questions include:

- Would these releases run on the hosting environments of their era?
- What assumptions did Pixelpost make about PHP, MySQL, Apache, GD, and EXIF?
- Can authentic historical installations be recreated today?

The goal is restoration before modification.

### Phase IV: Continuation

Only after archaeology and restoration are complete will modernization begin.

Future efforts may include:

- Modern PHP compatibility
- Contemporary database support
- Enhanced EXIF workflows
- Improved image handling
- Containerized deployments
- Security improvements
- New photographer-focused capabilities

Any continuation work should preserve the spirit and philosophy that made Pixelpost significant.

## Core Principles

### Preservation Before Modification

Understand first. Change later.

### Provenance Matters

Every recovered artifact should be traceable to its source whenever possible.

### Restoration Before Modernization

Historical behavior should be documented before compatibility work begins.

### Photographer First

Pixelpost was created for photographers.

PixelPost Mark II remains committed to that heritage.

## Repository Structure

This repository contains documentation, preservation records, restoration tooling, research materials, and future development work associated with PixelPost Mark II.

The project is currently focused on archaeology, preservation, and runtime restoration.

- `archive/original-pixelpost/`: preserved source archives and extracted inspection copies.
- `archive/provenance/`: chain-of-custody records and source verification notes.
- `docs/`: architecture, archaeology, preservation, audit, and restoration documentation.
- `docker/historical/`: historical runtime definitions used during restoration testing.
- `docker/restoration-workspaces/`: disposable first-boot workspaces.
- `runtime-testing/`: runtime test plans, fixtures, and logs.
- `tools/`: preservation and audit helper tools.

PixelPost Mark II is not an attempt to recreate the past exactly as it was.

It is an effort to preserve its lineage, understand its history, and carry its best ideas forward.

