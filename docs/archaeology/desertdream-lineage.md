# DesertDream — Site Lineage and Archaeological Record

**Discovered:** 2026-06-07
**Source:** DesertDream-Archeology/DesertDream1 — recovered from LaCie portable drive
**Status:** Archaeological artifact — one iteration recovered, others likely copies

---

## Summary

DesertDream is the name Nathan Cowlishaw used for his photography web presence
before, during, and after TalkingTree. It bookends the TalkingTree era rather
than simply preceding it.

The recovered artifact is a customized WordPress theme (Photo-Biyori LT v3.0.3)
deployed as a live photoblog circa 2012. The copyright line in the footer
establishes 2003 as the origin of the photography web presence.

---

## Known Timeline

| Period | Site | Platform | Notes |
|--------|------|----------|-------|
| 2003–? | DesertDream (earliest) | Unknown | Copyright origin. Platform not yet determined. |
| 2006–2011 | TalkingTree | PixelPost 1.7.x | 731 posts recovered. Last export 2011-06-25. |
| ~2012 | DesertDream (returns) | WordPress + Photo-Biyori LT | Listed on three photoblog directories. Nominated for 2012 Photoblog Awards. |

TalkingTree was the middle chapter. DesertDream was the name that opened and
closed the era.

---

## Recovered Artifact — DesertDream1

**Base theme:** Photo-Biyori LT v3.0.3
**Author:** tomo (photomo.com) — a Japanese photoblog WordPress theme
**Designed for:** WordPress 3.0+ (released June 2010)

**File timestamps (filesystem):**
- Created on drive: September 27, 2012
- Last modified: July 8, 2014 (style.css)

**Custom templates beyond base theme:**
- `album.php` — thumbnail grid archive view
- `guestbook.php` / `guestcomments.php` — community guestbook, not standard WordPress
- `extra.php` — two-column sidebar page template
- `disqus-form.css` — Disqus comment integration

---

## Evidence of Live Deployment

The `header.php` contains an Alexa site verification ID:

```
<meta name="alexaVerifyID" content="J31ec9RrgSXaqqahJxq3OZLssc8" />
```

Alexa verification required ownership confirmation of a live domain.
This site was deployed and publicly accessible.

**Meta description (verbatim):**
> Featuring photography by Nathan Cowlishaw showcasing the beautiful desert
> landscapes of the American Southwest.

**Meta keywords:**
utah, arizona, new mexico, nevada, photography, photographer,
micro four thirds, m4/3, desert, rural, decay, ghosts, panasonic,
images, photos, landscapes, cloudscapes, trees, color, beauty

---

## Community Presence (from footer.php)

| Directory | Listing |
|-----------|---------|
| CoolPhotoblogs.com | Profile #436 |
| Photoblogs.org | Listed |
| PhotoBlogs.com | Site #2233 |
| Photoblog Awards | Nominated — 2012 |

**FeedBurner RSS:** `feeds.feedburner.com/desertdream`

Active RSS syndication confirms the site had subscribers and regular readers.
Photoblog Awards nomination confirms community recognition within the photoblog
ecosystem.

---

## Copyright Statement (verbatim from footer.php)

```
Nathan Cowlishaw © 2003-2012 / All rights reserved.
Powered by Photo-Biyori & WordPress
```

**2003** is the earliest documented year of Nathan's photography web presence.
This predates TalkingTree by three years and suggests at least one earlier
DesertDream iteration on an unidentified platform.

---

## Design Aesthetic (from screenshot.png)

Single large photograph centered, full width.
Thumbnail strip below — recent posts as small images.
White background, minimal navigation: Home / Archives / Tags / About / Links / RSS.
Prev / Random navigation — characteristic of photoblog, not blog.
No sidebar intrusion on the primary photograph.

The design reflects the photoblog doctrine: the image is the content.
Everything else is infrastructure.

---

## Subject Matter Continuity

DesertDream and TalkingTree share identical subject matter:
- Utah, Arizona, New Mexico, Nevada
- Desert landscapes, rural decay, ghost towns
- Cloudscapes, trees, water
- Micro four thirds / Panasonic camera system

The photography practice is continuous across all known iterations.
The domain name changed. The eye did not.

---

## Open Questions

1. **What platform powered DesertDream 2003–?** PixelPost, Movable Type,
   hand-coded HTML, or another early photoblogging system?

2. **Was there a DesertDream between 2003 and TalkingTree's 2006 launch?**
   The gap is three years. Images from that period may exist.

3. **What domain(s) did DesertDream use?** The footer references
   `desertdream` as a FeedBurner identifier. The actual domain is unknown.
   Wayback Machine archaeology recommended.

4. **Were other DesertDream iterations substantially different?**
   Nathan noted "several iterations" — DesertDream1 is the only recovered
   artifact. Others may be copies or minor variations.

5. **When did DesertDream (2012) go offline?** Last file modification
   is July 2014. The site may have remained active beyond that date.

---

## Archaeological Significance

DesertDream establishes that TalkingTree was not Nathan's first photoblog —
it was his most sustained one. The photography web presence spans at least
2003–2014, possibly longer.

The PixelPost-Mark-II restoration project is not recovering a single site.
It is recovering the most complete surviving chapter of a longer photographic
publishing history.

---

## Source Files Preserved

Location on recovery drive:
```
<local-recovery-volume>/DesertDream-Archeology/DesertDream1/
```

Copied to working archive:
```
<private-local-path>/DesertDream-Archeology/DesertDream1/
```

Files: 19 (PHP templates, CSS, JS, PNG assets)
Platform: WordPress theme — not a database backup, not a full site snapshot.
