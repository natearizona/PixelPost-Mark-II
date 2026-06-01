# Missing Artifact Impact

Phase: PixelPost Archaeology Phase 9 - Public Reality Verification

Mode: read-only. No artifacts were modified, imported, restored, committed, or pushed.

## Impact Scale

- Critical = blocks exact/native restoration or direct provenance.
- Useful = improves fidelity or reduces inference, but does not block derived reconstruction.
- Cosmetic = affects presentation polish or peripheral context.

## Missing Artifact Matrix

| Missing artifact | Impact | Reason |
| --- | --- | --- |
| Native PixelPost SQL dump | Critical | Blocks direct restoration of the exact original PixelPost database tables, IDs, option rows, EXIF table state, and installation settings. |
| `includes/pixelpost.php` | Critical | Blocks verification of original database credentials, table prefix, site path, and exact runtime configuration. |
| Original PixelPost template/theme directory | Useful | Blocks exact visual restoration of the PixelPost-era presentation, but public Wayback captures and recovered content still allow derived presentation reconstruction. |
| Original addon directory | Useful | Blocks exact behavior of any active plugins/addons; may affect comments, tags, feeds, spam controls, or display features. |
| Structured EXIF table data | Useful | Public pages show EXIF/camera-style display, but the PixelPost XML does not preserve structured EXIF fields. Image files may still contain EXIF, but that was not verified in this phase. |
| Original server config | Useful | Helps reproduce hosting behavior, paths, rewrites, and PHP settings, but runtime restoration has already succeeded in earlier lab phases. |
| Original static TalkingTree site source | Cosmetic/Useful | Static pages such as `chief_joseph.htm` and `native_issues.htm` are outside the PixelPost content layer, but they help reconstruct the broader public site context. |

## Highest-Impact Missing Item

The native PixelPost SQL dump remains the most important missing artifact.

Without it, the project cannot claim direct database restoration. With the current XML/image evidence, it can claim historically grounded content reconstruction.

## Missing Artifact Answer

Missing artifacts reduce exactness, not viability. The recovered XML, images, thumbnails, WordPress exports, and Wayback evidence are enough for a high-confidence public content reconstruction, but not enough for exact native PixelPost database restoration.
