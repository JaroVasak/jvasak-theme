# jvasak block theme

Minimal block theme for [jvasak.com](https://jvasak.com), replacing Neve. Self-hosted fonts, no front-end JavaScript, no plugins required (Polylang free handles the languages).

## Layout

| Path | Purpose |
|---|---|
| `theme.json` | Palette, fonts, sizes, buttons, layout widths |
| `style.css` | Theme header and all design CSS (`jv-*` classes), moved out of Neve's Additional CSS |
| `functions.php` | Menu location, styles, font preload, shortcodes, Polylang query fix |
| `assets/fonts/` | Spectral 400 (+ italic) and DM Sans 400–700 variable (+ italic), latin and latin-ext woff2 |
| `parts/` | `header.html` (also used over the homepage hero and the post banner, via the `jv-overlay` class) and `footer.html` |
| `templates/` | `front-page`, `page`, `page-no-title`, `single`, `archive`, `home`, `search`, `404`, `index` |
| `bin/build-zip.sh` | Builds the installable ZIP (not part of the theme itself) |
| `bin/check.sh` | Lints the theme; CI runs it on every pull request (see [Checks](#checks)) |

Palette slugs keep Neve's names (`nv-site-bg`, `nv-dark-bg`, `neve-text-color`, …) so colours already saved in posts and pages keep working. Neve's `is-style-secondary` button style is registered too.

### Shortcodes used by the templates

Polylang free cannot translate template parts, so text that differs per language is rendered on the server:

- `[jv_menu]`: the classic menu at the **Primary menu** location. Polylang free assigns one menu per language. It's printed as a list on wide screens and inside a `<details>` toggle on small screens.
- `[jv_t en="…" cs="…"]`: short template strings (eyebrows, 404 text).
- `[year]`, `[jv_home_url]`, `[jv_page_title]`.

The footer tagline is the Site Tagline block, which Polylang translates in **Languages → Translations**.

### Polylang fix

Polylang free does not filter Query Loop blocks by language, so the "Stories" section on the English homepage was listing Czech posts. `functions.php` adds the current language to every Query Loop.

## Checks

`bin/check.sh` runs the same checks as the **Theme checks** GitHub Action, which must pass before a pull request can merge into `main`. It needs Docker (Docker Desktop on WSL) and Python 3:

- PHP syntax with PHP 8.1 (the theme's minimum, `Requires PHP` in `style.css`) and PHP 8.5, deprecation warnings included.
- `bin/check-theme.py`: the `style.css` header fields and `MAJOR.MINOR.PATCH` version, valid `theme.json` and existing font files, balanced block markup with valid attributes in `templates/` and `parts/`, existing template parts, both `en` and `cs` text in every `[jv_t]`, and existing preloaded fonts.
- ShellCheck on the `bin/` scripts.

CI also lints the workflow files with actionlint.

## Building the theme ZIP

WordPress installs and updates the theme from a ZIP file. To build one:

1. Raise `Version:` in `style.css` (for example `1.0.0` → `1.0.1`). The stylesheet URL includes the version, so browsers and the cache load the new CSS only after a version change.
2. Commit your changes. The ZIP is built from the last commit, so uncommitted changes are left out. The script warns you about them.
3. Run the script:

   ```bash
   bin/build-zip.sh                                  # writes dist/jvasak-<version>.zip
   bin/build-zip.sh /mnt/c/Users/<you>/Downloads     # or into another folder, e.g. Windows Downloads from WSL
   ```

4. In wp-admin, go to **Appearance → Themes → Add New Theme → Upload Theme**, choose the ZIP and confirm **Replace current with uploaded**.
5. Clear the site cache.

`bin/`, `.github/`, `.gitattributes`, `.gitignore` and `CLAUDE.md` are left out of the ZIP (`export-ignore` in `.gitattributes`).

## Fonts

Spectral (Production Type) and DM Sans (Colophon Foundry) are licensed under the SIL Open Font License 1.1: https://openfontlicense.org
