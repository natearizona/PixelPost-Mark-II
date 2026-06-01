# PixelPost Mark II Roadmap

Phase: Product Definition

Status: design only. No code is introduced by this document.

## Roadmap Principle

The shortest credible path is not to clone all of Pixelpost. It is to prove the core photoblog loop:

```text
import or upload image -> preserve metadata -> render image page -> render chronology -> export archive
```

## MVP

Goal: working image-first photoblog prototype with TalkingTree import capability.

Required features:

- Post, image, category, tag, comment, and EXIF data models.
- Import from PixelPost export XML.
- Import local JPEG and thumbnail directories by filename.
- Home page showing latest published image.
- Image page with title, date, caption, image, categories, tags, previous/next.
- Browse page with responsive thumbnail grid.
- Archive page grouped by year/month.
- Category and tag pages.
- Comment display for imported comments.
- Admin-free import command or script for initial prototype.
- Read-only public rendering.
- Exportable JSON manifest.

Not required for MVP:

- live admin upload interface
- comment submission
- theme marketplace
- multi-user roles
- full WordPress import parity
- EXIF editing
- public installer

Success criteria:

- TalkingTree-derived content imports into Mark II.
- Public pages render with stable URLs.
- Chronology survives intact.
- Image relationships survive intact.
- Comments display on the correct image pages.
- Missing media and unresolved images are reported.

## Version 0.2

Goal: make Mark II usable for a new photoblog.

Features:

- Admin login.
- Image upload.
- Thumbnail and responsive derivative generation.
- EXIF extraction from uploaded JPEGs.
- Caption/category/tag editing.
- Draft, scheduled, and published states.
- Basic settings.
- RSS/Atom feeds.
- Backup/export command.
- Import report UI.

Success criteria:

- A photographer can start a new photoblog without using command-line import tools.
- The original PixelPost publishing loop exists in modern form.

## Version 0.3

Goal: improve restoration, portability, and theme control.

Features:

- WordPress WXR import.
- TalkingTree reconstruction import profile.
- Conflict resolution for duplicate posts/media.
- Static HTML export.
- Theme/template system.
- Theme preview.
- Comment moderation.
- Spam protection.
- Search.
- Alt text workflow.
- Image privacy controls for GPS EXIF.

Success criteria:

- Historical sites can be reconstructed with transparent import reports.
- Owners can shape presentation without changing application code.

## Version 1.0

Goal: stable public release for independent photographers and preservation projects.

Features:

- Hardened install/update workflow.
- Full backup and restore documentation.
- Database migrations.
- Security review.
- Accessibility pass.
- Responsive default theme.
- Import/export test fixtures.
- Checksummed media archive format.
- Plugin or extension boundary only where justified.
- Public documentation.

Success criteria:

- A new user can deploy Mark II, import historical content or start fresh, publish safely, and export the whole site later.

## Explicit Non-Goals Through 1.0

- hosted SaaS product
- social graph
- algorithmic feed
- native mobile app
- creator monetization platform
- engagement analytics
- AI image generation features
- large plugin marketplace

## Dependency Order

1. Data model.
2. Import parser.
3. Media library with checksums.
4. Public renderer.
5. Archive/category/tag routing.
6. Comment preservation.
7. Export manifest.
8. Admin upload workflow.
9. EXIF extraction.
10. Theme system.

## Recommended First Prototype Slice

Use the TalkingTree reconstruction as the prototype fixture:

- 731 posts
- 731 matched JPEGs
- 731 matched thumbnails
- 887 comments
- 18 categories
- 441 tags
- chronology from 2006-10-16 through 2011-06-23

This gives Mark II a real-world archive immediately and prevents a toy prototype from looking successful while failing preservation realities.
