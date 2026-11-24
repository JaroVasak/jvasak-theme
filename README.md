# jvasak block theme

Minimal block theme for [jvasak.com](https://jvasak.com), replacing Neve. Self-hosted fonts, no front-end JavaScript, no plugins required (Polylang free handles the languages).

## Layout

| Path | Purpose |
|---|---|
| `theme.json` | Palette, fonts, sizes, buttons, layout widths |
| `style.css` | Theme header and all design CSS (`jv-*` classes), moved out of Neve's Additional CSS |
| `functions.php` | Menu location, styles, font preload, shortcodes, Polylang query fix |
| `assets/fonts/` | Spectral 400 (+ italic) and DM Sans 400–700 variable (+ italic), latin and latin-ext woff2 |
| `parts/` | `header.html` (also used over the hero, via the `jv-overlay` class) and `footer.html` |
| `templates/` | `front-page`, `page`, `page-no-title`, `single`, `archive`, `home`, `search`, `404`, `index` |

Palette slugs keep Neve's names (`nv-site-bg`, `nv-dark-bg`, `neve-text-color`, …) so colours already saved in posts and pages keep working. Neve's `is-style-secondary` button style is registered too.

### Shortcodes used by the templates

Polylang free cannot translate template parts, so text that differs per language is rendered on the server:

- `[jv_menu]`: the classic menu at the **Primary menu** location. Polylang free assigns one menu per language. It's printed as a list on wide screens and inside a `<details>` toggle on small screens.
- `[jv_t en="…" cs="…"]`: short template strings (eyebrows, 404 text).
- `[year]`, `[jv_home_url]`, `[jv_page_title]`.

The footer tagline is the Site Tagline block, which Polylang translates in **Languages → Translations**.

### Polylang fix

Polylang free does not filter Query Loop blocks by language, so the "Stories" section on the English homepage was listing Czech posts. `functions.php` adds the current language to every Query Loop.

## Local development

Use the production-copy overlay in the [wordpress repo](https://github.com/JaroVasak/wordpress) (`local/docker-compose.prod-copy.yml`). It mounts this folder read-only as `wp-content/themes/jvasak`, so edits show on reload.

## Fonts

Spectral (Production Type) and DM Sans (Colophon Foundry) are licensed under the SIL Open Font License 1.1: https://openfontlicense.org
