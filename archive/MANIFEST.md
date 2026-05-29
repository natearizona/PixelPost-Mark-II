# PixelPost Mark II Archive Manifest

This archive is the untouched source-material area for the PixelPost Mark II archaeology phase.

## Acquisition Log

| Local file | Source | Status | SHA-256 |
| --- | --- | --- | --- |
| `archive/original-pixelpost/raw/phpsources.net_Pixelpost-v1.7.3_435-3.zip` | `https://phpsources.net/script/php/blogs/435-3_pixelpost%2Cv1.7.3` download link | Preserved raw ZIP; extracted for inspection | `0553abce0a647ff226d117de0893f903697910761aabf680fad5ce3ed693d98a` |
| `archive/original-pixelpost/raw/sourceforge_pixelpost_1.3.zip` | `https://sourceforge.net/projects/pixelpost/files/pixelpost/Pixelpost%20v1.3/` | Preserved raw ZIP; extracted for lineage inspection | `62a06a4aca2a7472c24ae7ef15bd5bf305c48501cb723ed7c4b296f97515eef9` |
| `archive/original-pixelpost/raw/sourceforge_pixelpost_1.4.zip` | `https://sourceforge.net/projects/pixelpost/files/pixelpost/Pixelpost%20v1.4/` file `pixelpost_1-1.4.zip` | Preserved raw ZIP; extracted for lineage inspection | `0e36a4599bffe185ae93a08bb02c1038acbc252417af0ba4a47be820a9989475` |
| `archive/original-pixelpost/raw/sourceforge_pixelpost_1.4.1.zip` | `https://sourceforge.net/projects/pixelpost/files/pixelpost/Pixelpost%20v1.4.1/` | Preserved raw ZIP; extracted for lineage inspection | `373ed13d4e4362a8484b600098236ce63ef7fdba8dc0cf43400a81e4af5d96c4` |
| `archive/original-pixelpost/raw/sourceforge_pixelpost_1.4.2.zip` | `https://sourceforge.net/projects/pixelpost/files/pixelpost/Pixelpost%20v1.4.2/` | Preserved raw ZIP; extracted for lineage inspection | `a7d4d7b1ab6ea917a627cf2fd1dd09dabfdd1b821169b23b3f710db7cfde080b` |

## Source Notes

SourceForge still exposes early Pixelpost files and identifies the original project maintainers. It also notes that as of 2009-07-01 the project moved to `www.pixelpost.org`.

PHP Sources mirrors Pixelpost v1.7.3 and lists the release as 04 Sept 2009 with 182 files and approximately 0.62 MB compressed.

The official extension repository historically lived at `http://www.pixelpost.org/extend/`, with addon and template sections at `/extend/addons/` and `/extend/templates/`. The site was not directly acquired in this pass; secondary tutorial pages and search results confirm its historical role. Future work should attempt Wayback/CDX harvesting of those paths and named addons/templates.

OpenSourceCMS exposes two Pixelpost screenshot entries in its page markup, but direct image acquisition failed in this pass: guessed media URLs returned 404 documents and were not preserved as images. Future work should use browser-side inspection or archived copies to recover the actual screenshot assets.

Secondary references checked during this pass:

- OpenSourceCMS confirms Pixelpost as a PHP/MySQL photoblog, first released 2005-02-23, with final stable version 1.7.3 in September 2009.
- Wikipedia-style summaries and security advisories confirm common feature claims: chronological photo publishing, multilingual support, comments, EXIF, spam filtering, categories, tags, templates, and addons.
- TMDHosting tutorials confirm the historical module/template installation workflow: download archives from Pixelpost Extend, extract one addon PHP file into `addons/`, or extract one template folder into `templates/`.

## Repository Discipline

Raw archives under `archive/original-pixelpost/raw/` should remain byte-for-byte unchanged.

Extracted copies under `archive/original-pixelpost/extracted/` are inspection copies. Do not modernize or patch them in place during the archaeology phase.

Future recovered themes, addons, documentation, and screenshots should be placed under:

- `archive/themes/`
- `archive/plugins/`
- `archive/docs/`
- `archive/screenshots/`
