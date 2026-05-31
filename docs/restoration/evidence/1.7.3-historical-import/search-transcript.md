# Phase 6 Historical Artifact Search Transcript

Date: 2026-05-31 America/Phoenix

## Local Repository Search

```text
find . -maxdepth 5 \( -iname '*talkingtree*' -o -iname '*pixelpost*' -o -iname '*.sql' -o -iname '*.sql.gz' -o -iname '*.mysql' -o -iname '*.zip' -o -iname '*.tar' -o -iname '*.tar.gz' -o -iname '*.tgz' -o -iname '*.gz' -o -iname '*backup*' -o -iname 'pixelpost.php' -o -iname 'images' -o -iname 'thumbnails' -o -iname 'templates' -o -iname 'addons' \) -print
```

Result summary:

- Original Pixelpost release archives and extracted trees were found.
- Generated restoration workspace copies were found.
- No historical TalkingTree SQL dump or site backup was found.

## Adjacent Local TalkingTree Lead

```text
find /Users/nathanarizona/Documents/Codex/2026-05-28/howdy-ready-for-my-public-ssh/turquoise-ai-infra/wordpress/talkingtree -maxdepth 5 -print
```

Result:

```text
/Users/nathanarizona/Documents/Codex/2026-05-28/howdy-ready-for-my-public-ssh/turquoise-ai-infra/wordpress/talkingtree
/Users/nathanarizona/Documents/Codex/2026-05-28/howdy-ready-for-my-public-ssh/turquoise-ai-infra/wordpress/talkingtree/.gitkeep
```

## VPS Restoration Lab Search

```text
find /opt/pixelpost-restoration-lab -maxdepth 7 \( -iname '*talkingtree*' -o -iname '*.sql' -o -iname '*.sql.gz' -o -iname '*.zip' -o -iname '*.tar' -o -iname '*.tar.gz' -o -iname '*.tgz' -o -iname '*backup*' -o -iname 'pixelpost.php' -o -iname 'images' -o -iname 'thumbnails' -o -iname 'templates' -o -iname 'addons' \) -print
```

Result summary:

- Read-only Pixelpost 1.7.3 source specimen was found.
- Disposable lab workspaces were found.
- Phase 5 generated test dump was found at `/opt/pixelpost-restoration-lab/reports/repeat-173-20260531T172345Z/pixelpost-repeatability.sql`.
- No historical TalkingTree site backup was found.

## VPS Broader Read-Only Search

```text
find /opt /root /home -maxdepth 8 \( -iname '*talkingtree*' -o -iname '*.sql' -o -iname '*.sql.gz' -o -iname '*pixelpost*.zip' -o -iname '*pixelpost*.tar*' -o -iname '*backup*.zip' -o -iname '*backup*.tar*' -o -iname '*dreamhost*' -o -iname '*cpanel*' \) -print
```

Result:

```text
/opt/pixelpost-restoration-lab/reports/repeat-173-20260531T172345Z/pixelpost-repeatability.sql
```

Conclusion:

No real historical Pixelpost/TalkingTree import artifact is currently present in the searched locations.
