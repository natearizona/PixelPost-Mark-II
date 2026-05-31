# Pixelpost 1.7.3 Core Workflow Validation

Question: Can Pixelpost 1.7.3 perform its core photoblogging workflow on the verified historical runtime without source modification?

Answer: yes. A realistic JPEG upload completed end to end: admin login, image storage, database row creation, thumbnail generation, EXIF extraction, theme rendering, archive rendering, and category rendering.

## Runtime

- Database: MySQL `5.1.73` from `ggmartinez/mysql:5.1`
- PHP: `5.6.40`
- Template: `simple`
- Thumbnail settings: `100x75`
- EXIF enabled: `T`
- Test URL: `http://127.0.0.1:18082/` over SSH tunnel
- Workspace: disposable copy under `/opt/pixelpost-restoration-lab/workspaces/browser-validation-1.7.3-20260531T021851Z`

## Results

| Workflow Area | Result | Evidence |
| --- | --- | --- |
| Admin login page loads | Pass | `screenshots/13-admin-login.png` |
| Administrator login succeeds | Pass | `screenshots/14-admin-dashboard.png` |
| Session persists | Pass | `screenshots/20-admin-images-session-persisted.png` |
| Upload form loads | Pass | `screenshots/14-admin-dashboard.png` |
| JPEG upload succeeds | Pass | `upload-response-320x240.html` |
| Database row created | Pass | `runtime-evidence-final.txt` |
| Image file stored | Pass | `runtime-evidence-final.txt` |
| Thumbnail generated | Pass | `runtime-evidence-final.txt` |
| EXIF extracted | Pass | `runtime-evidence-final.txt` |
| EXIF rendered by template | Pass | `screenshots/17-public-image-page.png` |
| Default image page renders | Pass | `screenshots/17-public-image-page.png` |
| Archive page renders | Pass | `screenshots/18-archive-page.png` |
| Category page renders | Pass | `screenshots/19-category-page.png` |

## Test Images

Two controlled JPEGs were used:

| File | Dimensions | Purpose | Result |
| --- | --- | --- | --- |
| `test-image-exif.jpg` | `1x1` | EXIF parser smoke test | Image and EXIF stored; thumbnail file was zero bytes. |
| `test-image-exif-320x240.jpg` | `320x240` | Realistic workflow validation | Full pass, including `100x75` thumbnail. |

The 1x1 image is retained as evidence because it exposed a thumbnail edge case. It is not treated as the core workflow result.

## Successful Upload Evidence

The successful upload response contains:

```text
POSTED: Phase 4 EXIF Workflow Pass
```

Database row:

```text
id: 2
datetime: 2026-05-31 02:35:47
headline: Phase 4 EXIF Workflow Pass
image: 20260531170747_test-image-exif-320x240.jpg
exif_len: 740
```

Stored files:

```text
images/20260531170747_test-image-exif-320x240.jpg 5970 bytes
thumbnails/thumb_20260531170747_test-image-exif-320x240.jpg 1195 bytes
```

Dimensions:

```text
images/20260531170747_test-image-exif-320x240.jpg 320x240
thumbnails/thumb_20260531170747_test-image-exif-320x240.jpg 100x75
```

## EXIF Evidence

The EXIF serializer stored known values from the controlled JPEG:

```text
MakeIFD0=PixelPost Lab
ModelIFD0=RestorationCam 173
ExposureTimeSubIFD=1/125 sec
FNumberSubIFD=f 5.6
DateTimeOriginalSubIFD=2008:01:16 19:24:38
FlashSubIFD=No Flash
FocalLengthSubIFD=35 mm
ISOSpeedRatingsSubIFD=200
```

The public image page rendered:

```text
RestorationCam 173
1/125 sec
f/5.6
Flash: Not Fired
```

## Theme Rendering Evidence

The public image page rendered the default `simple` theme with:

```text
Pixelpost Restoration Lab - Phase 4 Browser Validation
Home | Browse | About
Phase 4 EXIF Workflow Pass - 2026-05-31 02:35:47
Pixelpost Restoration Lab end-to-end workflow test.
RestorationCam 173
1/125 sec
f/5.6
Flash: Not Fired
```

The archive and category pages rendered and contained thumbnails. Browser DOM inspection confirmed the successful image thumbnail:

```text
src=http://127.0.0.1:18082/thumbnails/thumb_20260531170747_test-image-exif-320x240.jpg
naturalWidth=100
naturalHeight=75
alt=Phase 4 EXIF Workflow Pass
```

## Known Warnings And Edge Cases

PHP compatibility warnings remain:

```text
mysql_connect(): The mysql extension is deprecated
Function ereg_replace() is deprecated
Function eregi_replace() is deprecated
```

These warnings did not block the workflow.

The 1x1 EXIF JPEG produced a zero-byte thumbnail:

```text
thumbnails/thumb_20260531170520_test-image-exif.jpg 0 bytes
```

The realistic 320x240 image generated a valid thumbnail, so the next blocker is not general thumbnail generation. The 1x1 behavior should be tracked later as an image-size edge case.

## Final Questions

1. Does the browser installer function correctly?

Yes. It completed configuration generation and schema finalization through version `1.73`.

2. Can an administrator log in?

Yes. The administrator `archivist` logged in successfully, and the session persisted across the Images view.

3. Can an image be uploaded?

Yes. Pixelpost accepted the 320x240 JPEG upload and inserted a database row.

4. Are thumbnails generated?

Yes for the realistic workflow image. Pixelpost generated a `100x75` thumbnail. The separate 1x1 image produced a zero-byte thumbnail edge case.

5. Does EXIF extraction function?

Yes. EXIF values were serialized into `pixelpost_pixelpost.exif_info` and rendered on the public image page.

6. Does the default theme render correctly?

Yes. The default `simple` theme rendered the public image page, archive page, and category page.

7. Can Pixelpost perform its original photoblogging workflow without source modification?

Yes. The recovered Pixelpost 1.7.3 release completed the end-to-end workflow without source modification: upload image, store image, generate thumbnail, extract EXIF, render through theme, and display publicly.

8. What is the next executable blocker, if any?

No blocker prevents the core photoblogging workflow on this verified runtime. Next executable work should validate repeatability from a clean container runbook, then test comments, RSS/Atom feeds, addon loading, and restoration from an imported historical database.
