# Wayback Correlation

Phase: PixelPost Archaeology Phase 9 - Public Reality Verification

Mode: read-only. No artifacts were modified, imported, restored, committed, or pushed.

## Operating Question

Did the recovered artifacts preserve the public TalkingTree Photoblog with historical fidelity?

## Evidence Sources

Recovered local artifacts:

- PixelPost export XML files: `pixelpost-export-2011-06-25_*.xml`
- Recovered JPEG image directories
- Recovered thumbnail directory
- 2012 WordPress WXR comparison exports

Public captures checked:

- `https://web.archive.org/web/20070210091949/https://talkingtree.org/`
- `https://web.archive.org/web/20070222124836/http://talkingtree.org/photoblog/`
- `https://web.archive.org/web/20100412124322/http://talkingtree.org/index.php?x=about`
- `https://web.archive.org/web/20100412124631/http://talkingtree.org/index.php?x=browse`
- `https://web.archive.org/web/20110106010751/http://talkingtree.org/`
- `https://web.archive.org/web/20110913170636/http://talkingtree.org/2006/10/journey-to-the-spirit-world/`
- `https://web.archive.org/web/20110920063430/http://talkingtree.org/2007/09/sidewall-in-calf-creek-canyon/`
- `https://web.archive.org/web/20070701043639/http://talkingtree.org/native_issues.htm`
- `https://web.archive.org/web/20060618133338/http://talkingtree.org/chief_joseph.htm`

## Correlation Matrix

| Wayback URL | Public evidence observed | Local artifact evidence | Classification |
| --- | --- | --- | --- |
| 2007 home page | Static site title `Home - The Talking Tree`; navigation images and pre-photoblog static pages. | Not expected in PixelPost XML; outside photoblog content layer. | Not enough data |
| 2007 `/photoblog/` | PixelPost page title `Desert Dream`; image `photoblog/images/20070214173921_parashantcanyon.jpg`; visible title `Parashant Canyon Overlook`; comments UI. | PixelPost export chronology includes 2007 photoblog posts and matching image naming style. Specific record not yet spot-checked in local XML. | Partial match |
| 2010 about page | PixelPost page title `About - Desert Dream`; headings for about/equipment/software. | About/static PixelPost page not present in post export set. Confirms public PixelPost theme/site context. | Partial match |
| 2010 browse page | PixelPost page title `Browse - Desert Dream`; public thumbnail grid; 588 images in capture parse; thumbnails such as `thumb_20100411081444_pine_cones.jpg`; categories/tags headings. | Recovered thumbnail directory contains PixelPost-style `thumb_*.jpg` files; XML preserves categories/tags. | Match |
| 2011 home page | PixelPost page title `Cedar City in Winter - Desert Dream`; image `images/20110103091640_cedar_city_main_street.jpg`; tags shown; EXIF display visible; zero comments visible. | XML contains 2011 posts, images, tags, comments. Structured EXIF is absent from XML. | Partial match |
| 2011 WordPress post: Journey to the Spirit World | Public title `Journey to the Spirit World`; visible date `10.17.2006`; categories `Abstract`, `Rock Art`, `Southern Utah`; comments count `0`; caption text matches local XML opening. | XML record: title `Journey to the Spirit World`; date `2006-10-17 16:31:06`; slug `journey-to-the-spirit-world`; image `20061017163106_headless.jpg`; same categories; zero comments. | Match |
| 2011 WordPress post: Sidewall in Calf Creek Canyon | Public title `Sidewall in Calf Creek Canyon`; visible date `9.20.2007`; categories `Clouds`, `Southern Utah`; comments count `0`; caption text matches local XML opening. | XML record: title `Sidewall in Calf Creek Canyon`; date `2007-09-20 06:28:59`; slug `sidewall-in-calf-creek-canyon`; image `20070920062859_calfcreek2.jpg`; same categories; zero comments. | Match |
| 2007 `native_issues.htm` | Static pre/parallel TalkingTree page title `Native Issues`; navigation images and static site structure. | Not part of PixelPost export. Useful for broader site context only. | Not enough data |
| 2006 `chief_joseph.htm` | Static pre/parallel TalkingTree page title `Chief Joseph`; navigation images and static site structure. | Not part of PixelPost export. Useful for broader site context only. | Not enough data |

## Public Reality Findings

The strongest direct matches are the two known WordPress-era public post captures:

- `Journey to the Spirit World`
- `Sidewall in Calf Creek Canyon`

Both match recovered XML records on:

- title
- slug
- publication date
- category list
- zero public comments
- body/caption text

The 2010 browse capture also strongly supports the recovered thumbnail and category/tag model. It shows a public PixelPost browse page with hundreds of thumbnail images using the same `thumb_*.jpg` convention found in the recovered thumbnail directory.

## Correlation Answer

Public Wayback evidence confirms the recovered XML/image reconstruction for known photoblog pages and the broader PixelPost public structure. The static 2006-2007 non-photoblog pages are contextual TalkingTree material, but they are outside the PixelPost export scope.
