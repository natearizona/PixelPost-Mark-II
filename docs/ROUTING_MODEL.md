# Routing Model

## Scope

This document maps Pixelpost 1.7.3 routing behavior. Pixelpost does not use a router class or framework; routing is emergent behavior inside entrypoint scripts and query parameters.

Evidence files:

- `index.php`
- `admin/index.php`
- `admin/install.php`
- `includes/functions_browse.php`
- `includes/functions_comments.php`
- `includes/functions_feeds.php`

## Subsystem Purpose

The routing model directs browser requests to the correct photoblog mode:

- current image,
- specific image,
- browse/archive/category/tag view,
- feed output,
- comment posting or popup,
- admin workflow,
- installer/upgrade workflow.

## Major Files Involved

- `index.php`: public routing hub.
- `admin/index.php`: admin routing hub.
- `admin/install.php`: installer routing hub.
- `includes/functions_browse.php`: `x=browse` behavior.
- `includes/functions_comments.php`: `x=save_comment` behavior.
- `includes/functions_feeds.php`: `x=rss`, `x=atom`, `x=comment_rss`, `x=comment_atom` behavior.

## Public Execution Flow

### Current Image

Request:

```text
index.php
```

Behavior:

1. Loads `image_template.html`.
2. Selects the current photograph from `{prefix}pixelpost`.
3. Public visitors receive only rows with `datetime <= current site datetime`.
4. Selection respects configured `display_sort_by` and `display_order`.

### Specific Image

Request:

```text
index.php?showimage={id}
```

Behavior:

1. `showimage` is cast to integer.
2. Pixelpost selects that row from `{prefix}pixelpost`.
3. It builds previous/next/first/latest navigation based on chronology.

### Template Page

Request:

```text
index.php?x=about
```

Behavior:

1. Pixelpost looks for `templates/{template}/about_template.html`.
2. If found, it loads that template.
3. If not found and the `x` value is not a known feed/comment action, it returns a 404.

### Browse

Request examples:

```text
index.php?x=browse
index.php?x=browse&category=3
index.php?x=browse&archivedate=2008-01
index.php?x=browse&tag=portrait
```

Behavior:

1. Loads `browse_template.html`.
2. `includes/functions_browse.php` builds thumbnail lists and category controls.
3. Category, archive month, tag, and multi-category POST filters alter the image query.

### Feeds

Request examples:

```text
index.php?x=rss
index.php?x=atom
index.php?x=comment_rss
index.php?x=comment_atom
index.php?x=rss&tag=portrait
```

Behavior:

1. `includes/functions_feeds.php` detects feed requests.
2. It emits RSS or Atom XML and exits through normal PHP output.
3. It uses public-only chronological queries.

### Comments

Request examples:

```text
index.php?popup=comment&showimage={id}
index.php?x=save_comment
```

Behavior:

1. Comment popup loads `comment_template.html`.
2. Comment submission is handled by `includes/functions_comments.php`.
3. Anti-spam checks may return Apache-style 404 responses.
4. Accepted comments are inserted into `{prefix}comments` and redirect back to the image.

## Admin Execution Flow

Admin routes are query-parameter driven through `admin/index.php`.

Common routes:

- `admin/index.php`: new image/upload form.
- `admin/index.php?view=images`: image listing and edit tools.
- `admin/index.php?view=images&id={id}`: edit one image.
- `admin/index.php?view=categories`: category manager.
- `admin/index.php?view=comments`: comment moderation.
- `admin/index.php?view=options`: site/template/feed/comment/spam/thumbnail settings.
- `admin/index.php?view=info`: environment/info page.
- `admin/index.php?view=addons`: addon manager.
- `admin/index.php?x=logout`: logout.

The admin shell includes all major admin modules every request. Modules self-select based on `view`, `x`, `action`, and `id`.

## Installer Execution Flow

Installer routes use `view` and `cat`:

- `install.php?view=overview&cat=introduction`
- `install.php?view=overview&cat=license`
- `install.php?view=install&cat=requirements`
- `install.php?view=install&cat=database`
- `install.php?view=install&cat=administrator`
- `install.php?view=install&cat=settings`
- `install.php?view=install&cat=configuration`
- `install.php?view=install&cat=finalize`
- `install.php?view=db_fix`

## mod_rewrite Assumption

Pixelpost has a `$mod_rewrite` flag that changes permalink prefix behavior. In the recovered 1.7.3 front controller, this primarily affects whether generated image links use `./index.php?showimage=` or a shorter rewritten path. Routing still fundamentally depends on `index.php` and image IDs.

## Database Interactions

Routing modes trigger different query families:

- image routes query `{prefix}pixelpost`;
- browse routes query `{prefix}pixelpost`, `{prefix}catassoc`, `{prefix}categories`, and `{prefix}tags`;
- comments routes query/write `{prefix}comments` and read `{prefix}banlist`;
- feeds query `{prefix}pixelpost`, `{prefix}comments`, and `{prefix}tags`;
- admin routes write nearly every core table depending on selected view;
- installer routes create/alter all schema tables.

## Original Developer Assumptions

- Query-string routing is acceptable and visible.
- Apache-style 404 headers are enough for invalid public actions.
- Public page types can be represented by template filenames.
- Admin pages can be included every request and self-filter.
- Optional URL rewriting is cosmetic, not architectural.

## Strengths

- Simple URLs are easy to inspect and recreate.
- Adding a static public page is as simple as adding `{name}_template.html` and linking `?x={name}`.
- The current-photo route is frictionless.
- The model is resilient on simple shared hosting.

## Weaknesses

- Routing logic is distributed across entrypoints and included files.
- Query parameters are overloaded: `x`, `view`, `cat`, `action`, `popup`, `id`, `showimage`.
- The admin include-all pattern makes module boundaries soft.
- Optional rewrite behavior is underdocumented in code.
- Route authorization is mostly implicit in admin bootstrap rather than per action.

## Historical Context

Pixelpost routing reflects a web before framework routing became standard. Its URLs are pragmatic and artifact-like: `showimage=123`, `x=browse`, `x=rss`. That plainness also suited the photoblog era, where permalinks, RSS, and archives mattered more than app-like navigation.

## Preservation Notes

Future work should preserve:

- stable image permalinks,
- simple browse/category/archive/tag URLs,
- feed URLs,
- a clear current-photo route,
- the ability for templates to define small public pages without becoming a CMS.
