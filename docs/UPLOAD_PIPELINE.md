# Upload Pipeline

## Scope

This document follows a photograph through Pixelpost 1.7.3 from admin upload to public display. It documents observed behavior only.

Evidence files:

- `admin/new_image.php`
- `admin/images_edit.php`
- `includes/functions.php`
- `includes/functions_exif.php`
- `index.php`

## Subsystem Purpose

The upload pipeline turns a photographer-selected image file into a photoblog entry. It stores the original image in the filesystem, extracts EXIF into the database, creates a thumbnail, records categories and tags, and makes the photograph available to the chronology-based front end.

## Major Files Involved

- `admin/index.php`: includes `new_image.php` after authentication.
- `admin/new_image.php`: upload form, validation, file move, EXIF serialization, insert into post/category/tag tables, thumbnail creation.
- `includes/functions.php`: `check_upload()`, `createthumbnail()`, `save_tags_new()`, category helpers.
- `includes/functions_exif.php`: `serialize_exif()` and EXIF formatting helpers.
- `includes/exifer1_5/exif.php`: bundled EXIF parser.
- `index.php`: reads the post, image file name, dimensions, thumbnail path, categories, comments, EXIF, and template tags for public output.

## Execution Flow

1. A logged-in administrator visits the default admin screen or `admin/index.php`.
2. `admin/new_image.php` renders the new image form unless `x=save` is present.
3. On submit, Pixelpost reads title, body, alternate-language fields, tags, categories, comments setting, and date settings from `$_POST`.
4. Date selection can use:
   - manual date/time fields,
   - one day after the latest existing image,
   - the current server-adjusted time,
   - or EXIF `DateTimeOriginalSubIFD` if requested and present.
5. The uploaded filename is normalized:
   - lowercased,
   - spaces become underscores,
   - unsupported characters are stripped,
   - an optional timestamp prefix is prepended when configured.
6. The file is moved from PHP's upload temp location into the configured image directory, usually `../images/`.
7. File permissions are set to `0644`.
8. EXIF is read from the stored file and serialized into a database-safe string.
9. A row is inserted into `{prefix}pixelpost`.
10. Category associations are inserted into `{prefix}catassoc`.
11. Tags are normalized and inserted into `{prefix}tags`.
12. Addon workspaces fire around the upload and thumbnail stages.
13. `createthumbnail()` reads the stored image, computes the thumbnail dimensions/crop, and writes a JPEG thumbnail named `thumb_{filename}` to the configured thumbnail directory.
14. The public front end later selects this row by chronology or `showimage`, reads the stored filename, calculates image dimensions, and emits template replacements such as `<IMAGE_NAME>`, `<IMAGE_WIDTH>`, `<IMAGE_HEIGHT>`, `<IMAGE_THUMBNAIL>`, and EXIF tags.

## Database Interactions

### Writes During Upload

- `{prefix}pixelpost`
  - `datetime`
  - `headline`
  - `body`
  - `image`
  - `alt_headline`
  - `alt_body`
  - `comments`
  - `exif_info`
- `{prefix}catassoc`
  - one row per selected category.
- `{prefix}tags`
  - one row per normalized tag.

### Reads During Upload

- `{prefix}config` for upload path, thumbnail path, crop mode, dimensions, compression, timestamp setting, EXIF setting, and language settings.
- `{prefix}pixelpost` when scheduling one day after the latest post.
- `{prefix}categories` for the category checklist.

### Reads During Public Display

- `{prefix}pixelpost` for current image, previous/next/first/latest images.
- `{prefix}catassoc` and `{prefix}categories` for category labels and links.
- `{prefix}comments` for comment counts and comment output.
- `{prefix}tags` for tag browse/feed behavior.

## Filesystem Interactions

- Original image: usually `images/{filename}`.
- Thumbnail: usually `thumbnails/thumb_{filename}`.
- Upload and thumbnail paths are configurable in `{prefix}config`.
- The installer checks or attempts to create/chmod `images/` and `thumbnails/`.

## EXIF Movement

1. `admin/new_image.php` includes `includes/functions_exif.php`.
2. `serialize_exif($uploadfile)` calls the bundled EXIF reader.
3. The returned EXIF tree is flattened, noisy fields such as MakerNote/unknown fields are removed, and the result is serialized.
4. The serialized string is inserted into `{prefix}pixelpost.exif_info`.
5. On public render, `index.php` calls `replace_exif_tags(...)` when EXIF is enabled and data exists.
6. Template tokens such as `<EXIF_CAMERA_MODEL>`, `<EXIF_EXPOSURE_TIME>`, `<EXIF_APERTURE>`, and `<EXIF_FLASH>` are replaced.

## Original Developer Assumptions

- PHP file uploads are enabled and the administrator can change filesystem permissions.
- GD functions are available for thumbnails.
- JPEG is the primary image format; PNG/GIF are partially handled but thumbnails are written as JPEG.
- The filesystem is trustworthy once admin authentication has happened.
- EXIF parsing can happen synchronously during upload.
- A single image maps to a single public post.
- Future-dated publishing is useful for photographers who want a paced photoblog.

## Strengths

- The pipeline is direct and understandable.
- Original files remain normal files in a visible directory.
- EXIF is captured at upload time, preserving camera context even if the file later changes.
- Thumbnail generation is built in, not delegated to the template.
- Categories, tags, scheduling, comments, and alternate-language fields are part of the upload workflow.

## Weaknesses

- File validation is filename/extension oriented and era-specific.
- Image and thumbnail operations assume GD and local writable paths.
- Failed thumbnail creation does not undo the already-created post.
- The pipeline stores serialized PHP EXIF structures in SQL, which is hard to query and fragile across runtimes.
- SQL escaping and filesystem handling are scattered inline.
- Upload handling predates modern MIME verification, content scanning, CSRF protection, and hardened session expectations.

## Historical Context

The upload workflow is photographer-centered. It asks for a photograph, a title, notes, categories/tags, comment behavior, and date. It does not ask the user to assemble blocks, pick engagement settings, or manage a page layout.

This pipeline reflects Pixelpost's identity: publish a photo into a chronological archive with just enough supporting context to make it meaningful.

## Preservation Notes

Future Mark II work should preserve:

- an image-first upload path,
- explicit chronology and future scheduling,
- original image file ownership,
- EXIF dignity,
- thumbnail generation as a supporting service,
- categories/tags as archival aids rather than engagement machinery.
