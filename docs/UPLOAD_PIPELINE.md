# Upload Pipeline

## New Image Flow

Primary file: `admin/new_image.php`.

Observed sequence:

1. The uploaded filename is lowercased, spaces become underscores, and most non-alphanumeric filename characters are stripped.
2. If timestamping is enabled, a timezone-adjusted `YmdHis_` prefix is added.
3. The upload target is `config.imagepath` plus the timestamped filename.
4. `image_upload_start` addon workspace runs.
5. `move_uploaded_file()` writes the uploaded image.
6. File mode is set to `0644`.
7. EXIF data is serialized and stored.
8. If selected, post datetime is taken from EXIF `DateTimeOriginalSubIFD`.
9. `image_upload_succesful` or `image_upload_failed` addon workspace runs.
10. A row is inserted into `pixelpost`.
11. Category associations are inserted into `catassoc`.
12. Tags are saved in `tags`.
13. `image_uploaded` and `upload_finished` addon workspaces run.
14. Thumbnail generation occurs using GD helpers.

## Thumbnail Flow

`includes/functions.php` creates thumbnails with GD:

- JPEG, PNG, and GIF inputs are detected by extension.
- Images are resized/cropped according to configured thumbnail width and height.
- Output thumbnails are JPEG files named `thumb_<original-filename>`.
- Optional unsharp mask sharpening can be applied.

## EXIF Flow

EXIF handling is implemented in `includes/functions_exif.php` with bundled `includes/exifer1_5/`. Stored EXIF is serialized into the `pixelpost.exif_info` text field and later rendered by template-tag replacement.

## Risks

- Upload validation trusts filename extension and PHP-provided upload data more than modern systems should.
- MIME/content sniffing is not sufficient for hostile uploads.
- Filename normalization differs between `$uploadfile` and the later `$filnamn` assignment, which deserves careful regression testing before any compatibility wrapper.
- Direct filesystem writes are assumed.
- Thumbnail generation may consume large memory for modern camera files.

