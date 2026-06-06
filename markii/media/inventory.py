from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Iterable

from .checksums import sha256_file
from .images import inspect_jpeg_dimensions


@dataclass
class Artifact:
    source_path: str
    filename: str
    extension: str
    artifact_type: str
    file_size: int | None
    sha256: str | None
    modified_time: float | None
    image_width: int | None = None
    image_height: int | None = None
    detection_rule: str = ""
    warnings: list[str] = field(default_factory=list)

    def to_dict(self):
        return asdict(self)


@dataclass
class InventorySummary:
    total_files_scanned: int = 0
    xml_count: int = 0
    pixelpost_xml_count: int = 0
    wordpress_wxr_count: int = 0
    jpeg_count: int = 0
    thumbnail_count: int = 0
    unknown_count: int = 0
    unsupported_count: int = 0
    unreadable_files: int = 0
    duplicate_filename_count: int = 0
    duplicate_hash_count: int = 0
    warnings: list[str] = field(default_factory=list)

    def to_dict(self):
        return asdict(self)


@dataclass
class InventoryResult:
    profile: str | None
    sources: list[str]
    summary: InventorySummary
    artifacts: list[Artifact]
    duplicate_filenames: dict[str, list[str]]
    duplicate_hashes: dict[str, list[str]]

    def to_dict(self):
        return {
            "profile": self.profile,
            "sources": self.sources,
            "summary": self.summary.to_dict(),
            "artifacts": [artifact.to_dict() for artifact in self.artifacts],
            "duplicate_filenames": self.duplicate_filenames,
            "duplicate_hashes": self.duplicate_hashes,
        }


def inventory_sources(sources: Iterable[Path], profile: str | None = None) -> InventoryResult:
    source_list = [source.expanduser() for source in sources]
    artifacts = [_inspect_path(path) for source in source_list for path in _iter_files(source)]
    summary = _summarize(artifacts)
    duplicate_filenames = _duplicates_by(lambda artifact: artifact.filename, artifacts)
    duplicate_hashes = _duplicates_by(lambda artifact: artifact.sha256 or "", artifacts)
    duplicate_hashes.pop("", None)
    summary.duplicate_filename_count = len(duplicate_filenames)
    summary.duplicate_hash_count = len(duplicate_hashes)

    return InventoryResult(
        profile=profile,
        sources=[str(source) for source in source_list],
        summary=summary,
        artifacts=artifacts,
        duplicate_filenames=duplicate_filenames,
        duplicate_hashes=duplicate_hashes,
    )


def _iter_files(source: Path):
    if source.is_file():
        yield source
        return
    if source.is_dir():
        for path in sorted(source.rglob("*")):
            if path.is_file():
                yield path
        return
    yield source


def _inspect_path(path: Path) -> Artifact:
    warnings: list[str] = []
    try:
        stat = path.stat()
        file_size = stat.st_size
        modified_time = stat.st_mtime
        digest = sha256_file(path)
    except OSError as exc:
        return Artifact(
            source_path=str(path),
            filename=path.name,
            extension=path.suffix.lower(),
            artifact_type="unreadable",
            file_size=None,
            sha256=None,
            modified_time=None,
            detection_rule="stat/read failure",
            warnings=[str(exc)],
        )

    artifact_type, detection_rule = classify_artifact(path)
    width = None
    height = None

    if artifact_type in {"jpeg", "thumbnail"}:
        width, height, warning = inspect_jpeg_dimensions(path)
        if warning:
            warnings.append(warning)

    return Artifact(
        source_path=str(path),
        filename=path.name,
        extension=path.suffix.lower(),
        artifact_type=artifact_type,
        file_size=file_size,
        sha256=digest,
        modified_time=modified_time,
        image_width=width,
        image_height=height,
        detection_rule=detection_rule,
        warnings=warnings,
    )


def classify_artifact(path: Path) -> tuple[str, str]:
    suffix = path.suffix.lower()
    name = path.name.lower()
    parts = {part.lower() for part in path.parts}

    if suffix == ".xml":
        if name.startswith("pixelpost-export-"):
            return "pixelpost_xml", "filename starts with pixelpost-export-"
        if "wordpress" in name or "wxr" in name:
            return "wordpress_wxr", "xml filename contains wordpress or wxr"
        return "xml", "xml extension"

    if suffix in {".jpg", ".jpeg"}:
        if name.startswith("thumb_") or "thumbnail" in parts or "thumbnails" in parts:
            return "thumbnail", "jpeg thumbnail naming/path rule"
        return "jpeg", "jpeg extension"

    if suffix:
        return "unsupported", "unsupported extension"
    return "unknown", "no extension"


def _summarize(artifacts: list[Artifact]) -> InventorySummary:
    summary = InventorySummary(total_files_scanned=len(artifacts))
    for artifact in artifacts:
        if artifact.artifact_type in {"xml", "pixelpost_xml", "wordpress_wxr"}:
            summary.xml_count += 1
        if artifact.artifact_type == "pixelpost_xml":
            summary.pixelpost_xml_count += 1
        elif artifact.artifact_type == "wordpress_wxr":
            summary.wordpress_wxr_count += 1
        elif artifact.artifact_type == "jpeg":
            summary.jpeg_count += 1
        elif artifact.artifact_type == "thumbnail":
            summary.thumbnail_count += 1
        elif artifact.artifact_type == "unknown":
            summary.unknown_count += 1
        elif artifact.artifact_type == "unsupported":
            summary.unsupported_count += 1
        elif artifact.artifact_type == "unreadable":
            summary.unreadable_files += 1

        for warning in artifact.warnings:
            summary.warnings.append(f"{artifact.source_path}: {warning}")
    return summary


def _duplicates_by(key_func, artifacts: list[Artifact]) -> dict[str, list[str]]:
    grouped: dict[str, list[str]] = {}
    for artifact in artifacts:
        key = key_func(artifact)
        if not key:
            continue
        grouped.setdefault(key, []).append(artifact.source_path)
    return {key: paths for key, paths in grouped.items() if len(paths) > 1}

