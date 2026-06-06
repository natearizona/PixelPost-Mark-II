from __future__ import annotations

from pathlib import Path


SOF_MARKERS = {
    0xC0,
    0xC1,
    0xC2,
    0xC3,
    0xC5,
    0xC6,
    0xC7,
    0xC9,
    0xCA,
    0xCB,
    0xCD,
    0xCE,
    0xCF,
}


def inspect_jpeg_dimensions(path: Path) -> tuple[int | None, int | None, str | None]:
    try:
        data = path.read_bytes()
    except OSError as exc:
        return None, None, str(exc)

    if len(data) < 4 or data[:2] != b"\xff\xd8":
        return None, None, "missing JPEG SOI marker"

    offset = 2
    while offset < len(data):
        while offset < len(data) and data[offset] != 0xFF:
            offset += 1
        while offset < len(data) and data[offset] == 0xFF:
            offset += 1
        if offset >= len(data):
            break

        marker = data[offset]
        offset += 1

        if marker in {0xD8, 0xD9, 0x01} or 0xD0 <= marker <= 0xD7:
            continue
        if offset + 2 > len(data):
            return None, None, "truncated JPEG segment length"

        segment_length = int.from_bytes(data[offset : offset + 2], "big")
        if segment_length < 2:
            return None, None, "invalid JPEG segment length"

        segment_start = offset + 2
        segment_end = offset + segment_length
        if segment_end > len(data):
            return None, None, "truncated JPEG segment"

        if marker in SOF_MARKERS:
            if segment_start + 5 > segment_end:
                return None, None, "truncated JPEG SOF segment"
            height = int.from_bytes(data[segment_start + 1 : segment_start + 3], "big")
            width = int.from_bytes(data[segment_start + 3 : segment_start + 5], "big")
            return width, height, None

        offset = segment_end

    return None, None, "JPEG dimensions not found"
