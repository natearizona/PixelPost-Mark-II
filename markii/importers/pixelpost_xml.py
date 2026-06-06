from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse
import xml.etree.ElementTree as ET


@dataclass
class ParsedPost:
    legacy_id: str
    title: str
    slug: str
    publication_date: str
    status: str
    body: str
    guid: str
    source_file: str

    def to_dict(self):
        return asdict(self)


@dataclass
class ParsedAttachment:
    legacy_id: str
    attachment_url: str
    filename_candidate: str
    guid: str
    source_file: str

    def to_dict(self):
        return asdict(self)


@dataclass
class ParsedComment:
    legacy_id: str
    post_id: str
    author: str
    author_url: str
    author_email: str
    date: str
    approval_status: str
    body: str
    parent_id: str
    source_file: str

    def to_dict(self):
        return asdict(self)


@dataclass(frozen=True)
class ParsedTaxonomy:
    name: str
    slug: str

    def to_dict(self):
        return asdict(self)


@dataclass
class ParseSummary:
    posts_parsed: int = 0
    attachments_parsed: int = 0
    comments_parsed: int = 0
    categories_parsed: int = 0
    tags_parsed: int = 0
    date_range: dict[str, str | None] = field(default_factory=lambda: {"earliest": None, "latest": None})
    parser_warnings: list[str] = field(default_factory=list)
    malformed_records: list[str] = field(default_factory=list)
    duplicate_ids: dict[str, list[str]] = field(default_factory=dict)

    def to_dict(self):
        return asdict(self)


@dataclass
class PixelPostParseResult:
    source_files: list[str]
    posts: list[ParsedPost]
    attachments: list[ParsedAttachment]
    comments: list[ParsedComment]
    categories: list[ParsedTaxonomy]
    tags: list[ParsedTaxonomy]
    summary: ParseSummary
    status: str

    def to_dict(self):
        return {
            "source_files": self.source_files,
            "posts": [post.to_dict() for post in self.posts],
            "attachments": [attachment.to_dict() for attachment in self.attachments],
            "comments": [comment.to_dict() for comment in self.comments],
            "categories": [category.to_dict() for category in self.categories],
            "tags": [tag.to_dict() for tag in self.tags],
            "summary": self.summary.to_dict(),
            "status": self.status,
        }


def parse_pixelpost_exports(sources: list[Path]) -> PixelPostParseResult:
    files = _expand_sources(sources)
    posts: list[ParsedPost] = []
    attachments: list[ParsedAttachment] = []
    comments: list[ParsedComment] = []
    categories: dict[str, ParsedTaxonomy] = {}
    tags: dict[str, ParsedTaxonomy] = {}
    summary = ParseSummary()

    for file_path in files:
        try:
            root = ET.parse(file_path).getroot()
        except ET.ParseError as exc:
            summary.parser_warnings.append(f"{file_path}: XML parse error: {exc}")
            continue
        except OSError as exc:
            summary.parser_warnings.append(f"{file_path}: read error: {exc}")
            continue

        channel = _first_child(root, "channel")
        if channel is None:
            summary.parser_warnings.append(f"{file_path}: missing channel element")
            continue

        _collect_channel_taxonomies(channel, categories, tags)

        for item in _children(channel, "item"):
            post_type = _text(_first_child(item, "post_type")) or "post"
            if post_type == "attachment":
                attachment = _parse_attachment(item, file_path, summary)
                if attachment:
                    attachments.append(attachment)
                continue

            post = _parse_post(item, file_path, summary)
            if post:
                posts.append(post)
                _collect_item_taxonomies(item, categories, tags)
                comments.extend(_parse_comments(item, post.legacy_id, file_path))

    summary.posts_parsed = len(posts)
    summary.attachments_parsed = len(attachments)
    summary.comments_parsed = len(comments)
    summary.categories_parsed = len(categories)
    summary.tags_parsed = len(tags)
    summary.date_range = _date_range(posts)
    summary.duplicate_ids = _duplicate_ids(posts, attachments, comments)
    status = "completed" if not summary.parser_warnings else "completed_with_warnings"

    return PixelPostParseResult(
        source_files=[str(path) for path in files],
        posts=posts,
        attachments=attachments,
        comments=comments,
        categories=sorted(categories.values(), key=lambda item: (item.slug, item.name)),
        tags=sorted(tags.values(), key=lambda item: (item.slug, item.name)),
        summary=summary,
        status=status,
    )


def _expand_sources(sources: list[Path]) -> list[Path]:
    files: list[Path] = []
    for source in sources:
        if source.is_file():
            files.append(source)
        elif source.is_dir():
            files.extend(sorted(path for path in source.rglob("*.xml") if path.is_file()))
    return sorted(files)


def _parse_post(item: ET.Element, file_path: Path, summary: ParseSummary) -> ParsedPost | None:
    legacy_id = _text(_first_child(item, "post_id"))
    if not legacy_id:
        summary.malformed_records.append(f"{file_path}: post missing wp:post_id")
        return None

    return ParsedPost(
        legacy_id=legacy_id,
        title=_text(_first_child(item, "title")),
        slug=_text(_first_child(item, "post_name")),
        publication_date=_text(_first_child(item, "post_date")) or _text(_first_child(item, "pubDate")),
        status=_text(_first_child(item, "status")),
        body=_text(_first_child(item, "encoded")),
        guid=_text(_first_child(item, "guid")),
        source_file=str(file_path),
    )


def _parse_attachment(item: ET.Element, file_path: Path, summary: ParseSummary) -> ParsedAttachment | None:
    legacy_id = _text(_first_child(item, "post_id"))
    if not legacy_id:
        legacy_id = _text(_first_child(item, "post_name")) or _text(_first_child(item, "guid"))
        summary.malformed_records.append(f"{file_path}: attachment missing wp:post_id; using fallback legacy ID")

    attachment_url = _text(_first_child(item, "attachment_url")) or _text(_first_child(item, "guid"))
    return ParsedAttachment(
        legacy_id=legacy_id,
        attachment_url=attachment_url,
        filename_candidate=_filename_from_url(attachment_url),
        guid=_text(_first_child(item, "guid")),
        source_file=str(file_path),
    )


def _parse_comments(item: ET.Element, post_id: str, file_path: Path) -> list[ParsedComment]:
    parsed: list[ParsedComment] = []
    for comment in _children(item, "comment"):
        parsed.append(
            ParsedComment(
                legacy_id=_text(_first_child(comment, "comment_id")),
                post_id=post_id,
                author=_text(_first_child(comment, "comment_author")),
                author_url=_text(_first_child(comment, "comment_author_url")),
                author_email=_text(_first_child(comment, "comment_author_email")),
                date=_text(_first_child(comment, "comment_date")),
                approval_status=_text(_first_child(comment, "comment_approved")),
                body=_text(_first_child(comment, "comment_content")),
                parent_id=_text(_first_child(comment, "comment_parent")),
                source_file=str(file_path),
            )
        )
    return parsed


def _collect_channel_taxonomies(channel: ET.Element, categories: dict[str, ParsedTaxonomy], tags: dict[str, ParsedTaxonomy]) -> None:
    for category in _children(channel, "category"):
        slug = _text(_first_child(category, "category_nicename"))
        name = _text(_first_child(category, "cat_name"))
        _add_taxonomy(categories, name, slug)
    for tag in _children(channel, "tag"):
        slug = _text(_first_child(tag, "tag_slug")) or _text(_first_child(tag, "tag_wp_slug"))
        name = _text(_first_child(tag, "tag_name"))
        _add_taxonomy(tags, name, slug)


def _collect_item_taxonomies(item: ET.Element, categories: dict[str, ParsedTaxonomy], tags: dict[str, ParsedTaxonomy]) -> None:
    for element in _children(item, "category"):
        domain = element.attrib.get("domain", "")
        name = _text(element)
        slug = element.attrib.get("nicename", "")
        if domain == "post_tag":
            _add_taxonomy(tags, name, slug)
        else:
            _add_taxonomy(categories, name, slug)


def _add_taxonomy(target: dict[str, ParsedTaxonomy], name: str, slug: str) -> None:
    if not name and not slug:
        return
    key = slug or name
    target[key] = ParsedTaxonomy(name=name, slug=slug)


def _duplicate_ids(posts: list[ParsedPost], attachments: list[ParsedAttachment], comments: list[ParsedComment]) -> dict[str, list[str]]:
    duplicates = {}
    for label, values in {
        "posts": [post.legacy_id for post in posts],
        "attachments": [attachment.legacy_id for attachment in attachments],
        "comments": [comment.legacy_id for comment in comments],
    }.items():
        seen = set()
        repeated = sorted({value for value in values if value in seen or seen.add(value)})
        if repeated:
            duplicates[label] = repeated
    return duplicates


def _date_range(posts: list[ParsedPost]) -> dict[str, str | None]:
    dates = []
    for post in posts:
        parsed = _parse_date(post.publication_date)
        if parsed:
            dates.append(parsed)
    if not dates:
        return {"earliest": None, "latest": None}
    return {
        "earliest": min(dates).isoformat(sep=" "),
        "latest": max(dates).isoformat(sep=" "),
    }


def _parse_date(value: str) -> datetime | None:
    value = value.strip()
    if not value:
        return None
    for fmt in ("%Y-%m-%d %H:%M:%S", "%a, %d %b %Y %H:%M:%S %z", "%a, %d %b %Y %H:%M %z"):
        try:
            parsed = datetime.strptime(value, fmt)
            return parsed.replace(tzinfo=None)
        except ValueError:
            pass
    return None


def _filename_from_url(value: str) -> str:
    path = urlparse(value).path
    return Path(path).name


def _first_child(element: ET.Element, local_name: str) -> ET.Element | None:
    for child in list(element):
        if _local_name(child.tag) == local_name:
            return child
    return None


def _children(element: ET.Element, local_name: str) -> list[ET.Element]:
    return [child for child in list(element) if _local_name(child.tag) == local_name]


def _local_name(tag: str) -> str:
    if "}" in tag:
        return tag.rsplit("}", 1)[1]
    return tag


def _text(element: ET.Element | None) -> str:
    if element is None:
        return ""
    return "".join(element.itertext()).strip()
