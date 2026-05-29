# Routing Analysis

## Public Routing

Pixelpost uses one public entry point, `index.php`.

Observed routing inputs:

- `showimage`: integer image id for permalink-style image selection.
- `x`: page/action selector, sanitized to lowercase-ish alphanumeric, underscore, and dash characters.
- `popup=comment`: switches rendering to `comment_template.html`.
- `lang`: two-letter language cookie override.
- feed actions through `x`: `atom`, `comment_atom`, `rss`, `comment_rss`.
- comment submission through `x=save_comment`.
- browse through `x=browse`, implemented with `includes/functions_browse.php`.

Template routing is file-based. If `?x=about` is requested and `templates/<active-template>/about_template.html` exists, that file is rendered. If it does not exist and `x` is not a reserved feed/comment action, the public entry point emits a 404.

The historical `?x=ref` route is mapped to `referer`, but the referer route intentionally returns a fake 404. This appears to be an anti-log-spam or anti-probing behavior rather than ordinary content routing.

## Admin Routing

The admin area also uses a single entry point, `admin/index.php`.

Observed routing inputs:

- `x=login`, `x=logout`, `x=save`, `x=update`, and related action values.
- `view`: major admin section selector such as images, addons, options, categories, comments.
- section-specific parameters such as `id`, `imageid`, `selectfcat`, `selectfmon`, `selectftag`, and search/filter values.

Admin routing is not a controller layer. It is procedural dispatch with included files and conditionals.

## Continuity Notes

Future Mark II work should preserve the feeling of simple, linkable image chronology and editable template pages. Any modern router should first emulate the observed URL surface and only then add compatibility shims.

