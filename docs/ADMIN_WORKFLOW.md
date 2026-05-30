# Admin Workflow

## Scope

This document describes the Pixelpost 1.7.3 administration workflow as observed in the recovered source.

Evidence files:

- `admin/index.php`
- `admin/new_image.php`
- `admin/images_edit.php`
- `admin/comments.php`
- `admin/categories.php`
- `admin/options.php`
- `admin/view_addons.php`
- `admin/view_info.php`
- `admin/pass_recovery.php`
- `includes/functions.php`

## Subsystem Purpose

The admin panel is a single-photographer control room. It supports logging in, publishing photos, editing the archive, managing comments, categories, templates/options, addons, and environment information.

It is not a multi-author editorial dashboard. Its center of gravity is the next photograph.

## Major Files Involved

- `admin/index.php`: session/login bootstrap, admin navigation, module inclusion.
- `admin/new_image.php`: default admin screen and upload form.
- `admin/images_edit.php`: post listing, editing, deletion, mass publish/delete/category tools.
- `admin/comments.php`: comment moderation, deletion, spam-list helpers.
- `admin/categories.php`: add/edit/delete categories and alternate names.
- `admin/options.php`: general, template, thumbnail, comment, feed, antispam, and display settings.
- `admin/view_addons.php`: addon discovery and activation controls.
- `admin/view_info.php`: installation/runtime information.
- `admin/pass_recovery.php`: password reminder/recovery path.

## Execution Flow

1. `admin/index.php` redirects to the installer when `../includes/pixelpost.php` is missing.
2. It starts a session and includes database config/shared functions.
3. It reads the installed Pixelpost version and redirects to installer if the DB version is too old.
4. It loads the configuration row and admin language file.
5. Login:
   - submitted username is compared to `{prefix}config.admin`;
   - submitted password is MD5-hashed and compared to `{prefix}config.password`;
   - successful login stores username and password hash in session;
   - optional remember cookie stores a SHA1 value derived from password hash and remote IP.
6. Enabled admin addons are included and register hooks.
7. The navigation bar is rendered.
8. The shell includes all primary admin module files.
9. Each module checks route state and renders/actions only when relevant.

## Main Admin Tasks

### Publish A New Image

Default admin view. The photographer uploads an image, assigns title/body/tags/categories/date/comment setting, and Pixelpost creates the post, EXIF, and thumbnail.

### Manage Images

`view=images` lists existing photographs with edit, preview, delete, paging, filters, and mass actions. Editing updates image metadata, date, categories, tags, comments setting, and may regenerate/adjust thumbnails.

### Manage Categories

`view=categories` adds, edits, and deletes category labels. Category associations live separately in `{prefix}catassoc`.

### Manage Comments

`view=comments` reviews published and masked comments, deletes comments, and can feed spam/referrer lists.

### Manage Options

`view=options` includes several submenus:

- general site identity and paths,
- template selection,
- thumbnail/crop/compression settings,
- date/category formatting,
- feed options,
- comments and anti-spam settings,
- language and admin settings.

### Manage Addons

`view=addons` refreshes addon metadata and lets the administrator turn registered addons on/off.

## Database Interactions

- `{prefix}config`: authentication, site options, template choice, paths, feed/comment/display settings.
- `{prefix}pixelpost`: create/update/delete image posts.
- `{prefix}catassoc`: assign categories to images.
- `{prefix}categories`: category definitions.
- `{prefix}tags`: create/edit/delete image tags.
- `{prefix}comments`: moderate/delete comments.
- `{prefix}addons`: track addon files, activation state, and type.
- `{prefix}banlist`: anti-spam lists.
- `{prefix}version`: version check.

## Addon Interactions

Admin addons are discovered from `addons/`, stored in `{prefix}addons`, included when enabled, and registered through `add_admin_functions(...)`. Hook workspaces include:

- `admin_html_head`
- `admin_main_menu`
- `admin_main_menu_contents`
- upload-related workspaces in `admin/new_image.php`
- other menu/submenu-specific workspaces exposed by addons.

## Original Developer Assumptions

- One trusted administrator.
- Shared-hosting session and cookie behavior.
- MD5 password storage was acceptable for the era.
- Admin actions happen inside a trusted browser session.
- The admin panel can be built as a single PHP page with included modules.
- Photographers want fast access to upload, edit, comments, and options rather than a broad CMS dashboard.

## Strengths

- The default admin landing page is the publishing action.
- Navigation is compact and task-oriented.
- Photo editing, categories, tags, comments, and thumbnail behavior are close to the upload workflow.
- The admin can preview public images directly.
- Addons can extend admin navigation without a large framework.

## Weaknesses

- Authentication and session handling are weak by modern standards.
- CSRF protections are not systematic.
- Modules are included every request, creating broad execution surfaces.
- Many actions are controlled by GET parameters.
- Inline SQL and direct output are mixed.
- Addons share the same trust boundary as core admin code.

## Historical Context

The admin workflow reflects a photographer's routine: upload today's image, write a caption, choose a category, maybe moderate comments, then leave. It does not try to be an editorial newsroom, page builder, store, or community platform.

This restraint is one reason Pixelpost felt different from WordPress. The admin panel optimized for recurring photographic practice rather than general publishing administration.

## Preservation Notes

Future Mark II work should preserve:

- publishing as the default admin task,
- low-friction image upload and captioning,
- chronological scheduling,
- quick edit/preview loops,
- simple category/tag assignment,
- quiet comment moderation,
- a compact admin surface.
