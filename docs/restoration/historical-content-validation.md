# Historical Content Validation

Question: How much historical Pixelpost content survives in currently available artifacts?

Answer: no original historical site content is currently available for validation. The project can validate runtime restoration and generated test content, but it cannot yet validate TalkingTree content survival.

## Validation Status

| Validation Area | Status | Reason |
| --- | --- | --- |
| Image count | Not tested | No historical `images/` directory found |
| Category count | Not tested | No historical SQL dump found |
| Comment count | Not tested | No historical SQL dump found |
| EXIF preservation | Not tested | No historical SQL dump/images found |
| Archive pages | Not tested | No historical content imported |
| Category pages | Not tested | No historical content imported |
| Public image pages | Not tested | No historical content imported |
| Historical comparison | Not tested | No historical screenshots/Wayback captures paired with content found |

## Available Non-Historical Validation

Prior phases have validated generated test content:

- Phase 4: browser workflow with controlled EXIF JPEG.
- Phase 5: repeatability workflow with controlled EXIF JPEG.

Those results prove the restoration runtime works. They do not prove historical content survival.

## Reconstruction Percentage

Current historical site reconstruction percentage:

```text
25%
```

Rationale:

- 0% would mean runtime only.
- 25% means an empty installation is reproducibly operational.
- 50% requires importing a historical database.
- 75% requires imported historical database plus images.
- 100% requires historically accurate site reconstruction.

The lab has exceeded empty-install runtime capability in generated tests, but for historical-content reconstruction specifically it remains at 25% until a real historical SQL dump is imported.

## Next Evidence Needed

To advance beyond 25%, the project needs:

1. A real historical Pixelpost SQL dump.
2. The corresponding `images/` directory.
3. Preferably `thumbnails/`, `templates/`, `addons/`, and `includes/pixelpost.php`.
4. Any historical screenshots or archived public pages for comparison.

## Result

Historical content validation is blocked by absence of historical artifacts, not by runtime failure.
