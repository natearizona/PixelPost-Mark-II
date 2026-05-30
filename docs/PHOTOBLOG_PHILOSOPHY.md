# Photoblog Philosophy

## Scope

This document records the publishing philosophy embedded in Pixelpost 1.7.3. It is intentionally broader than code structure because Pixelpost's historical value is partly cultural.

Evidence sources:

- public front controller behavior in `index.php`,
- upload workflow in `admin/new_image.php`,
- editable templates in `templates/`,
- archive/tag/category behavior in `includes/functions_browse.php`,
- EXIF handling in `includes/functions_exif.php`,
- feed handling in `includes/functions_feeds.php`,
- admin workflow in `admin/index.php` and related admin modules.

## Subsystem Purpose

Pixelpost is a photoblog engine. Its purpose is to help a photographer publish a sequence of photographs on an independent website.

It is not a general blog engine with image support added later. It is image-first at the root.

## What Made Pixelpost Different From WordPress

WordPress begins from posts, pages, themes, taxonomies, comments, and plugins. Images can be inserted into posts, but the basic unit is a text post in a general publishing system.

Pixelpost begins from the photograph. The homepage is the current image. The upload form is the default admin task. The template language is filled with image tags: image title, image notes, image date, image dimensions, image navigation, image thumbnail row, image EXIF, image comments.

That difference matters. Pixelpost does not ask "what kind of content are you publishing today?" It assumes: a photograph.

## Workflows Pixelpost Optimized For

- Publish one image at a time.
- Attach a title, caption/notes, date, categories, tags, and comments setting.
- Preserve camera metadata through EXIF.
- Generate a thumbnail automatically.
- Let the newest eligible image become the public center of the site.
- Let visitors move previous/next through the photographic chronology.
- Let archives, categories, tags, feeds, and comments support the image sequence.
- Let the photographer alter visual presentation through editable template files.

This is a quiet routine, closer to developing and placing prints in an ordered notebook than managing a media platform.

## Publishing Assumptions

Pixelpost assumes:

- the site is owned by the photographer,
- the archive lives on a personal domain or shared host,
- publishing pace can be slow and deliberate,
- chronological order has meaning,
- a photograph deserves a page of its own,
- metadata helps preserve context,
- comments are optional conversation around a photograph,
- feeds are a way to let interested readers follow without locking them into a platform,
- templates should be editable by the owner.

## Image-First Behavior

The central public route selects an image, not a page. If no specific `showimage` is requested, Pixelpost finds the current image according to configured sort and chronology. It builds the page around:

- original image filename,
- dimensions,
- title,
- notes,
- date/time,
- category links,
- previous/next navigation,
- thumbnail navigation,
- comments,
- EXIF.

This creates a strong viewing rhythm: one photograph, then the next, then the archive.

## Chronology-First Behavior

Chronology is not just sorting. It is the public narrative.

Pixelpost uses `datetime` to determine:

- current image,
- public eligibility,
- future-dated scheduled posts,
- previous/next links,
- first/latest links,
- browse/archive ordering,
- feed ordering,
- month archive filters.

The date attached to a photograph is a publishing decision and an archival fact.

## Metadata And EXIF

Pixelpost treats EXIF as part of the photograph's story. It extracts metadata during upload, stores it with the post, and exposes camera model, exposure, aperture, flash, focal length, ISO, and capture date through template tags.

This is photographer-centric. The camera context is not decorative; it is part of how photographers understand images and learn from one another.

## Templates As Ownership

Editable templates gave Pixelpost sites a handmade quality. A photographer could shape the presentation without surrendering to a platform's feed design. The template system encouraged:

- minimal galleries,
- daily photo journals,
- experimental layouts,
- personal visual identity,
- valid XHTML/CSS pride of the era,
- portable site files.

The template files are not merely implementation detail. They are part of the culture Pixelpost served.

## Categories, Tags, Archives

Categories and tags support discovery inside a personal archive. They are not engagement funnels. Browse views, month filters, and tag feeds help visitors revisit bodies of work, locations, subjects, and periods.

This archive behavior should be preserved because it turns a sequence of posts into a durable photographic record.

## Comments And Feeds

Comments are per-image conversation. Feeds are outward-facing syndication. Both fit the independent web:

- the image remains on the photographer's site,
- interested readers can subscribe,
- comments attach to the artifact rather than becoming a social graph,
- public interaction is present but not dominant.

## Strengths

- Strong sense of ownership.
- Clear, repeatable publishing ritual.
- Low conceptual overhead.
- Photograph-centered public experience.
- Built-in archive and feed culture.
- Templates encourage personal visual identity.
- EXIF and chronology respect photography as a practice.

## Weaknesses

- Narrow scope can feel limiting for non-photoblog use.
- Manual template editing assumes some comfort with HTML/CSS.
- Single-admin assumptions do not fit collaborative publishing.
- Historical comment/spam/security expectations are outdated.
- Chronological presentation can under-serve large portfolio-style collections.

## Historical Context

Pixelpost emerged before algorithmic image feeds and social platforms became the default home for photographs. It belongs to an internet where a photographer's website was a primary place of publication, RSS was a social contract, and the archive was owned by the person who made it.

Its restraint now feels important. Pixelpost did not try to maximize time-on-site. It made a place for photographs.

## What PixelPost Mark II Should Preserve

- The photograph as the primary unit.
- The current/latest image as a meaningful homepage concept.
- Previous/next chronological navigation.
- Future-dated calm publishing.
- Owned image files and portable archives.
- Editable templates or an equally owner-respecting presentation layer.
- EXIF as first-class photographic context.
- Categories, tags, and archives as preservation tools.
- Feeds and exportable public records.
- A compact, photographer-first admin workflow.
- Independence from engagement-engine incentives.

## Doctrine

PixelPost Mark II should feel like a durable camera body and a field notebook:

- reliable,
- quiet,
- owned,
- portable,
- repairable,
- focused on photographs.

It should not become a social network, creator platform, analytics product, framework showcase, or dopamine machine.
