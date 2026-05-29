# Template System

## Model

Templates are plain HTML files under `templates/<template-name>/`.

The default image view uses `image_template.html`. Comment popups use `comment_template.html`. Browse pages use `browse_template.html`. Additional pages are created by adding `<name>_template.html` and linking to `index.php?x=<name>`.

Optional `header.html` and `footer.html` files wrap normal pages but are skipped for comment popups.

## Language Variants

For non-default languages, Pixelpost looks for language-specific template files such as:

- `image_<language-abbreviation>_template.html`
- `<x>_<language-abbreviation>_template.html`
- `comment_<language-abbreviation>_template.html`

If a selected language template is missing, Pixelpost emits an explicit template error.

## Tags

The renderer performs direct string and regex replacements for tags such as:

- `<SITE_TITLE>`
- `<SUB_TITLE>`
- `<SITE_URL>`
- `<IMAGE_TITLE>`
- `<IMAGE_NOTES>`
- `<IMAGE_ID>`
- `<IMAGE_PERMALINK>`
- `<IMAGE_PREVIOUS_LINK>`
- `<IMAGE_NEXT_LINK>`
- `<IMAGE_FIRST_LINK>`
- `<IMAGE_LAST_LINK>`
- `<IMAGE_THUMBNAIL>`
- `<IMAGE_THUMBNAIL_ROW>`
- `<IMAGE_COMMENTS>`
- `<BROWSE_CATEGORIES>`
- `<TOKEN>`

EXIF tags are replaced separately when EXIF display is enabled and the image has stored EXIF data.

## Preservation Notes

This template system is central to Pixelpost's identity. It allowed non-programmers to edit HTML and sprinkle in semantic photo tags without learning a theme framework. Future work should preserve this editable-template contract even if the implementation changes internally.

