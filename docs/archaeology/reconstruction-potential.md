# Reconstruction Potential

Phase: PixelPost Archaeology Phase 8 - PixelPost Export Reconstruction Analysis

Mode: read-only analysis. No artifacts were modified, imported, restored, committed, or pushed.

## Operating Question

Can the surviving PixelPost export XML files reconstruct the original TalkingTree PixelPost content layer?

Answer: yes, for a historically grounded derived reconstruction of the content layer. No, for a native unmodified PixelPost MySQL database restore.

## Reconstruction Capabilities

| Question | Answer | Evidence |
| --- | --- | --- |
| Can a derived PixelPost reconstruction dataset be built from the XML exports? | Yes | 731 post records, 731 attachment records, titles, dates, captions, categories, tags, comments, slugs, and image references survive. |
| Can a TalkingTree timeline be reconstructed? | Yes | Every exported item has `pubDate` and `wp:post_date`; range is 2006-10-16 through 2011-06-23. |
| Can image-to-post relationships be reconstructed? | Yes | 731 unique XML image references match 731 surviving JPEGs and 731 thumbnails. |
| Can category relationships be reconstructed? | Yes | 18 category definitions and 1,110 category assignments survive. |
| Can tag relationships be reconstructed? | Yes | 441 tag definitions and 880 tag assignments survive. |
| Can comments be reconstructed? | Mostly yes | 887 comment records survive in WXR form; exact PixelPost table mapping still needs a later transform design. |
| Can public archive chronology be reconstructed? | Yes | Dates, slugs, image filenames, titles, and categories are present. |
| Can EXIF be reconstructed from XML? | No | Structured EXIF fields were not found in the PixelPost XML exports. |
| Can native PixelPost DB state be restored directly? | No | No original PixelPost SQL dump or `includes/pixelpost.php` was found. |

## Surviving Content Layer

The recoverable PixelPost-era content layer includes:

- 731 photoblog posts
- 731 image attachment records
- 731 matched JPEG image references
- 731 matched thumbnails
- 887 comments
- 18 categories
- 441 tags
- captions/body text for post records
- slugs/permalink names
- full publication chronology

The surviving image directories contain 734 JPEGs, so there are three additional JPEG files beyond the XML-referenced set. Those should be treated as supplemental candidates until a later read-only inspection determines whether they are duplicates, alternates, or orphaned posts.

## Reconstruction Scores

These scores estimate practical recoverability of the historical TalkingTree PixelPost content layer from currently discovered artifacts.

| Score | Value | Rationale |
| --- | ---: | --- |
| Content Recovery Score | 90 / 100 | 731 posts, captions, comments, categories, tags, and slugs survive, but native SQL and templates are absent. |
| Metadata Recovery Score | 86 / 100 | Most visible metadata survives; EXIF and native PixelPost table context are absent. |
| Chronology Recovery Score | 97 / 100 | Dates are present for every record and the archive sequence is recoverable. |
| Image Recovery Score | 99 / 100 | All 731 XML-referenced images and thumbnails are present; 734 total JPEGs suggest extra variants. |
| Overall TalkingTree Reconstruction Score | 90 / 100 | A strong derived reconstruction is feasible, but exact native PixelPost restoration remains blocked without the original database. |

## New Estimated Reconstruction Percentage

Previous historical reconstruction status was 25% because the runtime was operational but no real historical content had been located.

After Phase 8:

```text
85%
```

Rationale:

- Runtime restoration already works from earlier phases.
- Historical content artifacts now exist.
- XML reconstructs the content layer.
- JPEGs and thumbnails correlate strongly.
- WordPress exports corroborate migration continuity.
- Native PixelPost SQL/config/templates are still missing.

This is not 100% because the original PixelPost MySQL database, original config, original templates, original addons, and structured EXIF table content have not been recovered.

## Final Questions

### How much of TalkingTree survives inside the PixelPost exports?

A substantial majority of the visible content layer survives:

- 731 posts
- 731 attachments
- 887 comments
- 18 categories
- 441 tags
- titles, captions, dates, slugs, and image filenames

Structured EXIF and native database layout do not survive in these XML files.

### How much of TalkingTree survives when combining exports + JPEGs + thumbnails?

Enough survives to reconstruct the historical photoblog presentation at high confidence:

- all 731 XML-referenced images are present
- all 731 XML-referenced thumbnails are present
- captions/body text and chronology are present
- categories/tags/comments are present

### Can a historically grounded reconstruction be created without the original PixelPost MySQL database?

Yes. A historically grounded derived reconstruction can be created without the original database.

It should be documented as derived reconstruction, not direct database restoration. The source of truth would be:

```text
PixelPost export XML + surviving JPEGs + surviving thumbnails + WordPress comparison exports
```

### What is the new estimated reconstruction percentage?

```text
85%
```

The project has moved from runtime-only restoration into viable historical content reconstruction. The next phase should remain read-only until a reconstruction mapping is designed and reviewed.
