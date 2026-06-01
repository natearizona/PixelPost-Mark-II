# Prototype Estimate

Phase: Product Definition

Status: planning estimate. No implementation is performed by this document.

## Prototype Goal

Build the shortest useful PixelPost Mark II prototype:

```text
TalkingTree import -> image-first public site -> archive browsing -> preserved comments -> portable export
```

## Recommended Prototype Type

Start with a server-rendered or static-rendered prototype, not a full CMS.

Reason:

- the first proof is reconstruction and rendering, not live multi-user publishing
- TalkingTree gives a real dataset immediately
- static or server-rendered pages keep the scope close to PixelPost's original simplicity
- import correctness matters more than admin polish at this stage

## Shortest Path

1. Define Mark II schema.
2. Build PixelPost XML parser.
3. Build media matcher for JPEGs and thumbnails.
4. Import TalkingTree posts, comments, categories, tags.
5. Render home page.
6. Render image page.
7. Render browse/archive/category/tag pages.
8. Generate import report.
9. Generate portable export manifest.

## Estimated Work Breakdown

| Area | Estimate | Notes |
| --- | ---: | --- |
| Data schema | 1-2 days | Post, image, derivative, EXIF, comment, category, tag, provenance. |
| XML parser | 2-3 days | PixelPost WXR-style import, comments, attachments, categories, tags. |
| Media matcher | 1-2 days | Match 731 JPEGs and thumbnails; report missing/orphan files. |
| Public renderer | 3-5 days | Home, image, browse, archive, category, tag pages. |
| Import report | 1 day | Counts, warnings, hashes, unresolved files. |
| Minimal styling | 2-3 days | Mobile-first, image-centered, restrained default theme. |
| Export manifest | 1-2 days | JSON manifest with media checksums. |
| Verification pass | 2-3 days | Compare counts and sample pages against known evidence. |

Practical prototype estimate:

```text
2-3 focused weeks
```

This assumes no live admin upload interface in the first prototype.

## MVP Prototype Scope

Included:

- local import
- durable public URLs
- responsive pages
- image chronology
- comments display
- category/tag pages
- archive pages
- provenance-aware import report
- portable export manifest

Excluded:

- live browser admin
- new image upload
- comment submission
- anti-spam
- user roles
- theme editor
- installer
- Docker production deployment

## Technology Guidance

Do not choose technology because it is fashionable. Choose the smallest stack that supports:

- safe image handling
- good filesystem control
- stable routing
- boring deployment
- easy backup/export
- future admin UI

Good prototype shapes:

- PHP server-rendered app with SQLite or MySQL
- lightweight Python import tool plus generated static site
- small server-rendered Node app only if it keeps file/archive handling clean

Avoid in the first prototype:

- React-first architecture
- Laravel-scale scaffolding before schema is proven
- headless CMS architecture
- SaaS-oriented services
- object storage as a requirement

## Prototype Success Test

The prototype succeeds when a clean operator can:

1. Point Mark II at the recovered TalkingTree XML and media directories.
2. Run one import command.
3. See a report with expected counts.
4. Open a local/public-safe site.
5. Navigate from latest image to older images.
6. Browse by archive, category, and tag.
7. View imported comments on image pages.
8. Export the reconstructed site manifest.

Expected counts:

- 731 posts
- 731 linked images
- 731 linked thumbnails
- 887 comments
- 18 categories
- 441 tags

## Current Risks

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Original PixelPost SQL absent | Cannot claim native restore | Label import as derived reconstruction. |
| EXIF absent from XML | Cannot preserve original DB EXIF | Extract from JPEGs later and label source. |
| Original template absent | Cannot replicate exact presentation | Build spirit-faithful default theme; preserve theme gap. |
| WordPress exports contain malformed XML tokens | Parser may need recovery mode | Start with PixelPost exports; use WXR as secondary comparison. |
| Three extra JPEGs unresolved | Small content ambiguity | Keep as orphan candidates in report. |

## Short Answer

The shortest path to a working prototype is a read-only public renderer plus TalkingTree import pipeline. Live publishing can come after import correctness and archive rendering are proven.
