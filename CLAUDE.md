# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

The `jvasak` WordPress block theme for jvasak.com (replaced Neve). Plain theme files: `theme.json`, `style.css`, `functions.php`, HTML block templates in `templates/` and `parts/`, self-hosted woff2 fonts. No build step, no npm or composer. [README.md](README.md) documents the layout, shortcodes, and release steps.

## Checks and release

```bash
bin/check.sh                                   # PHP lint (8.1 + 8.5), theme file checks, ShellCheck; needs Docker + python3
bin/build-zip.sh                               # dist/jvasak-<version>.zip, via git archive of HEAD
bin/build-zip.sh /mnt/c/Users/<you>/Downloads  # write elsewhere (WSL → Windows)
```

- `bin/check.sh` is the required **Theme checks** CI job on `main`; run it before committing. Extend `bin/check-theme.py` (standard library only) for new theme invariants.
- The ZIP is built from the **last commit**; uncommitted changes are left out.
- **Raise `Version:` in the `style.css` header for every release.** The stylesheet is enqueued with that version as its cache-busting query string, so without a bump browsers and the site cache keep the old CSS.
- `--prefix=jvasak/` sets the installed theme folder name; don't change it. Repo tooling is kept out of the ZIP with `export-ignore` in [.gitattributes](.gitattributes). Add new non-theme files there too.
- The owner installs it on the live site by uploading the ZIP in wp-admin (no SSH). Changing the live site is the owner's call.

## Architecture constraints

- **No front-end JavaScript and no plugin dependencies.** Solve UI with CSS or server-side PHP (e.g. the mobile menu is a `<details>` element, not a JS toggle). Performance is a priority.
- **Bilingual via Polylang free**, which can't translate template parts or filter Query Loops. So:
  - Per-language strings in templates use the `[jv_t en="…" cs="…"]` shortcode inside `wp:html` blocks. Every new template string needs both languages. Czech copy addresses the reader informally ("ty", never "vy").
  - Navigation is `[jv_menu]`, which renders the classic `primary` menu location. Polylang assigns a different menu per language. The menu is printed twice (wide and narrow screens), so `nav_menu_item_id` is blanked to avoid duplicate ids.
  - `functions.php` adds the current language to every Query Loop (`query_loop_block_query_vars`). Without it, the English homepage lists Czech posts.
  - `pll_*` calls are always guarded by `function_exists`, so the theme still works without Polylang.
- **Palette slugs in `theme.json` keep Neve's names** (`nv-site-bg`, `neve-text-color`, …), and the `is-style-secondary` button style is registered for the same reason: existing post content references them. Don't rename them.
- Design tokens (colours, fonts, sizes, layout widths) live in `theme.json`; everything else is in `style.css` under `jv-*` class names. Non-token colours are tints of the forest green `#17372b`.
- Headings use Spectral and body text uses DM Sans. Both are OFL-licensed and served from `assets/fonts/`; the four "normal" files (latin and latin-ext) are preloaded in `functions.php`. If you rename those font files, update the preload list too.
- `parts/header.html` is also used over the homepage hero and the single-post banner with the `jv-overlay` class (see `templates/front-page.html` and `templates/single.html`).
- `page-no-title` is a custom template that existing pages are assigned to; keep its slug.

## Conventions

- Commits use Conventional Commits with no scope (`feat: …`, `docs: …`, `build: …`).
- Branch names use the type as a prefix: `<type>/<short-kebab-description>`, branched from `main`.
- Keep [README.md](README.md) in sync when adding shortcodes, templates, or changing the release steps.
