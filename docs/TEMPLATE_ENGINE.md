# Template Engine

## Scope

This document analyzes the original Pixelpost 1.7.3 template system. It does not propose a replacement.

Evidence files:

- `index.php`
- `templates/simple/*.html`
- `templates/horizon/*.html`
- `includes/functions_browse.php`
- `includes/functions_exif.php`
- `includes/functions_feeds.php`

## Subsystem Purpose

Pixelpost's template system lets a site owner control the public photoblog using plain HTML files with angle-bracket replacement tags. The template is not a PHP theme in the WordPress sense. It is mostly static HTML transformed by `index.php` through direct token replacement.

The purpose is photographer-level customization: edit HTML/CSS files, place image metadata tags where desired, and keep the publishing workflow independent from presentation.

## Major Files Involved

- `templates/{active_template}/image_template.html`: default image page.
- `templates/{active_template}/browse_template.html`: browse/archive/category/tag view.
- `templates/{active_template}/comment_template.html`: popup comment view.
- `templates/{active_template}/about_template.html`: example static page.
- Optional `header.html` and `footer.html`: wrapped around main template output when present.
- Language variants such as `image_en_template.html` or `comment_en_template.html`: selected when alternate language behavior is active.
- `index.php`: loads templates and performs most replacements.
- `includes/functions_browse.php`: replaces browse-specific tags.
- `includes/functions_exif.php`: replaces EXIF-specific tags.
- `includes/functions_feeds.php`: replaces feed tags and emits feed responses.

## Execution Flow

1. `index.php` loads the active template name from `{prefix}config.template`.
2. If `header.html` or `footer.html` exist, they are loaded unless rendering a comment popup.
3. If `x` is set and `templates/{template}/{x}_template.html` exists, that template is loaded.
4. If no matching `x` template exists and `x` is not a feed/comment action, Pixelpost returns a 404.
5. If no `x` template applies, `image_template.html` is loaded.
6. Alternate-language templates may override the default file name pattern.
7. Pixelpost computes image, navigation, category, comment, EXIF, browse, site, and feed values.
8. Tags are replaced with `ereg_replace()` and `str_replace()`.
9. Addons can run front-end workspaces and may modify global/template state.
10. The final string is output.

## Common Template Tags

Observed core tags include:

- Site tags: `<SITE_TITLE>`, `<SUB_TITLE>`, `<SITE_URL>`, `<SITE_BROWSELINK>`, `<SITE_RSS_LINK>`, `<SITE_ATOM_LINK>`, `<FEED_AUTO_DISCOVERY>`.
- Image tags: `<IMAGE_ID>`, `<IMAGE_NAME>`, `<IMAGE_TITLE>`, `<IMAGE_NOTES>`, `<IMAGE_NOTES_CLEAN>`, `<IMAGE_DATE>`, `<IMAGE_TIME>`, `<IMAGE_DATETIME>`, `<IMAGE_WIDTH>`, `<IMAGE_HEIGHT>`, `<IMAGE_PERMALINK>`.
- Navigation tags: `<IMAGE_PREVIOUS_LINK>`, `<IMAGE_NEXT_LINK>`, `<IMAGE_FIRST_LINK>`, `<IMAGE_LAST_LINK>`, plus thumbnail/id/title variants.
- Thumbnail tags: `<IMAGE_THUMBNAIL>`, `<IMAGE_THUMBNAIL_ROW>`, `<IMAGE_THUMBNAIL_ROW_REV>`, `<THUMBNAIL_WIDTH>`, `<THUMBNAIL_HEIGHT>`.
- Category/browse tags: `<IMAGE_CATEGORY>`, `<IMAGE_CATEGORY_PAGED>`, `<BROWSE_CATEGORIES>`, `<BROWSE_CHECKBOXLIST>`, `<THUMBNAILS>`.
- Comment tags: `<IMAGE_COMMENTS>`, `<IMAGE_COMMENTS_NUMBER>`, `<IMAGE_COMMENT_TEXT>`, `<COMMENT_POPUP>`, `<VINFO_NAME>`, `<VINFO_URL>`, `<VINFO_EMAIL>`, `<TOKEN>`.
- EXIF tags: `<EXIF_CAMERA_MODEL>`, `<EXIF_EXPOSURE_TIME>`, `<EXIF_APERTURE>`, `<EXIF_FLASH>`, and related EXIF/language labels.

## Database Interactions

The template engine itself does not isolate DB access. Instead, `index.php` and included helpers query the database before replacing template tags.

Important reads:

- `{prefix}config`: active template, site identity, paths, feed settings, display order, language, EXIF/comment settings.
- `{prefix}pixelpost`: selected image and neighboring images.
- `{prefix}categories` and `{prefix}catassoc`: category labels and browse filters.
- `{prefix}comments`: comments and counts.
- `{prefix}tags`: tag browse and tag feeds.
- `{prefix}visitors`: visitor count.

## Original Developer Assumptions

- Template authors can edit HTML and CSS files directly.
- Tags are unique enough that direct string replacement is sufficient.
- Public output is assembled in one request rather than through a compiled template cache.
- Template files are trusted filesystem artifacts.
- The active template directory is controlled by the site owner.
- XHTML/CSS validation and feed autodiscovery are visible markers of web craftsmanship.

## Strengths

- Extremely low conceptual barrier for customization.
- Templates are portable and inspectable.
- The photo remains the primary template object.
- The system supports static pages through `?x={name}` without adding a CMS page model.
- Language-specific template files allow design differences per language.
- Theme authors can create a complete visual identity with ordinary files.

## Weaknesses

- There is no formal syntax, parser, inheritance model, or escaping policy.
- Replacement order matters.
- `ereg_replace()` is obsolete and unavailable in modern PHP.
- Many replacements mix presentation HTML and data construction inside `index.php`.
- Addons can affect output indirectly through globals, making behavior harder to reason about.
- The template engine cannot clearly distinguish trusted HTML, escaped text, and raw user content.

## Historical Context

The template engine is a defining part of Pixelpost's feel. It invited photographers to own their visual space without becoming CMS developers. A photoblog could look handmade, quiet, experimental, gallery-like, diary-like, or starkly minimal because the template was just files.

This differs from WordPress themes, which increasingly became PHP applications in their own right. Pixelpost templates are closer to a field notebook cover: tangible, editable, and in service of the photographs.

## Preservation Notes

Future Mark II work should preserve:

- editable templates as first-class artifacts,
- image-centered template vocabulary,
- simple static-page affordances,
- clear feed/archive/comment tags,
- portability of visual identity.

Any future template modernization should be documented as a compatibility layer, not a replacement of the historical concept.
