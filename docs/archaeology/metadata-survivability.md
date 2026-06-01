# Metadata Survivability

Phase: PixelPost Archaeology Phase 8 - PixelPost Export Reconstruction Analysis

Mode: read-only analysis. No artifacts were modified, imported, restored, committed, or pushed.

## Survivability Matrix

Classification:

- FULL = enough data appears present to reconstruct the field directly.
- PARTIAL = useful data exists, but normalization or inference is required.
- ABSENT = no structured evidence found in the PixelPost export XML.

| Metadata field | Status | Evidence |
| --- | --- | --- |
| Post title | FULL | 731 post titles are present; attachment records also carry image filenames as titles. |
| Post body/caption | FULL | 731 post records contain `content:encoded`, generally with image HTML followed by caption/body text. |
| Post date | FULL | `pubDate`, `wp:post_date`, and `wp:post_date_gmt` are present. |
| Categories | FULL | 18 category definitions and 1,110 category assignments observed. |
| Tags | FULL | 441 tag definitions and 880 tag assignments observed. |
| Comment records | FULL/PARTIAL | 887 `wp:comment` records found across 408 exported records. Author/date/content/status fields are present in WXR form, but exact PixelPost comment table fidelity still requires mapping. |
| Image filename | FULL | 731 unique JPEG references in XML; all match surviving JPEG files. |
| EXIF references | ABSENT | No structured EXIF fields found in PixelPost export XML. Sidecar search found only incidental text mentions of EXIF. |
| Permalinks/slugs | FULL | `wp:post_name` is present for all 1,462 content items; WordPress comparison exports also preserve public links. |
| Post-to-attachment relationship | FULL | 731 post records and 731 attachment records; `wp:post_parent` and filename references support pairing. |
| Public archive chronology | FULL | Dates are present on every content item and cover 2006-10-16 through 2011-06-23. |

## Preserved Fields

The XML exports preserve enough information to reconstruct the user-facing content layer:

- title
- image filename
- caption/body
- publication date
- slug
- category assignments
- tag assignments
- comment records
- post/image pairing

## Fields Requiring Transformation

The XML exports are not PixelPost-native. A future derived reconstruction would need mapping from WXR fields into PixelPost-style concepts:

| WXR field | Likely reconstruction use |
| --- | --- |
| `title` | PixelPost headline |
| `content:encoded` | PixelPost body/caption after stripping image HTML |
| `wp:post_date` | PixelPost datetime |
| `wp:post_name` | Slug/permalink support if preserved in Mark II |
| `category domain="category"` | PixelPost category mapping |
| `category domain="post_tag"` | PixelPost tag mapping |
| `wp:comment` | PixelPost comment mapping |
| image filename in `content:encoded` | PixelPost `image` filename |

## Missing Native PixelPost Context

The XML exports do not preserve:

- original PixelPost MySQL table rows in native form
- original PixelPost image IDs as stored in `pixelpost_pixelpost`
- original `pixelpost.php` database config
- original template choice
- original addons
- structured EXIF storage

## Metadata Survivability Answer

The exported metadata is strong enough for a historically grounded derived reconstruction of the visible content layer. It is not enough for a byte-for-byte native PixelPost database restore.
