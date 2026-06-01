# Historical Fidelity Score

Phase: PixelPost Archaeology Phase 9 - Public Reality Verification

Mode: read-only. No artifacts were modified, imported, restored, committed, or pushed.

## Score Matrix

| Category | Score | Rationale |
| --- | ---: | --- |
| Image fidelity | 98 / 100 | All 731 XML-referenced JPEGs are present; public pages confirm image naming conventions. Three extra JPEGs remain unresolved. |
| Thumbnail fidelity | 96 / 100 | All 731 XML-referenced images have matching thumbnails; 2010 browse page confirms `thumb_*.jpg` public usage. |
| Post metadata fidelity | 94 / 100 | Titles, dates, slugs, captions/body, post status, and image references survive; native PixelPost IDs/table context absent. |
| Chronology fidelity | 97 / 100 | XML date range is coherent and public spot checks match known Wayback post dates. |
| Category/tag fidelity | 92 / 100 | XML preserves categories and tags; public post categories match spot checks; tag visibility varies by page. |
| Comment fidelity | 90 / 100 | 887 comments preserve author/date/content/status; public spot checks confirm zero-comment pages; no threaded relationships. |
| Public page fidelity | 88 / 100 | Known public posts match title/date/slug/category/caption/comment count; image extraction from migrated Wayback post pages was incomplete. |
| Presentation/theme fidelity | 55 / 100 | Wayback confirms public appearance, but original PixelPost template files have not been recovered. |

## Historical Fidelity Score

Calculated as an evidence-weighted practical score:

```text
89 / 100
```

## Final Questions

### 1. Does public Wayback evidence confirm the recovered XML/image reconstruction?

Yes. Wayback evidence confirms:

- public PixelPost site title and browse/about structure
- public thumbnail grid using `thumb_*.jpg`
- public image naming conventions
- known post titles, dates, slugs, categories, captions, and comment counts
- later WordPress migration continuity

### 2. Do known public TalkingTree posts match recovered XML records?

Yes. The two named public posts match recovered XML records:

- `Journey to the Spirit World`
- `Sidewall in Calf Creek Canyon`

They match on title, date, slug, category, caption/body, and zero-comment count.

### 3. What evidence contradicts the reconstruction, if any?

No direct contradiction was found in Phase 9.

Known limitations:

- native PixelPost SQL is still missing
- original PixelPost template is still missing
- structured EXIF is not present in the XML
- three extra JPEGs are not tied to XML records yet
- some Wayback pages are static site material outside the PixelPost export scope

### 4. What percentage of the public TalkingTree Photoblog appears recoverable?

Estimated recoverability:

```text
90%
```

This is higher than the Phase 8 reconstruction percentage because public Wayback evidence now corroborates the recovered content layer. It remains below 100% because exact native database, template, addon, config, and structured EXIF artifacts are missing.

### 5. Is the project now best described as software restoration, content reconstruction, or historical publication recovery?

For TalkingTree specifically, the project is now best described as:

```text
historical publication recovery
```

The broader PixelPost Mark II project still includes software restoration, but the TalkingTree evidence has crossed into recovering a historically published photoblog from surviving exports, media files, thumbnails, and public captures.
