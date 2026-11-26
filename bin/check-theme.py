#!/usr/bin/env python3
"""Static checks for the jvasak theme files. Standard library only.

- style.css header has the fields WordPress and the release process rely on
- theme.json is valid JSON and every font file it references exists
- block markup in templates/ and parts/ is balanced, with valid JSON attributes
- template parts referenced by templates exist in parts/
- every [jv_t] has both en and cs text
- fonts preloaded in functions.php exist
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
errors = []


def error(path, message):
    errors.append(f"{path.relative_to(ROOT)}: {message}")


def check_style_header():
    path = ROOT / "style.css"
    header = re.search(r"/\*(.*?)\*/", path.read_text(encoding="utf-8"), re.S)
    fields = dict(re.findall(r"^([A-Za-z ]+):[ \t]*(.+?)\s*$", header.group(1), re.M)) if header else {}
    for name in ("Theme Name", "Version", "Requires at least", "Requires PHP", "License", "Text Domain"):
        if not fields.get(name):
            error(path, f"header is missing '{name}'")
    if fields.get("Version") and not re.fullmatch(r"\d+\.\d+\.\d+", fields["Version"]):
        error(path, f"Version '{fields['Version']}' is not MAJOR.MINOR.PATCH")
    if fields.get("Text Domain", "jvasak") != "jvasak":
        error(path, "Text Domain must be 'jvasak'")


def check_theme_json():
    path = ROOT / "theme.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        error(path, f"invalid JSON: {exc}")
        return
    if data.get("version") != 3:
        error(path, "expected theme.json version 3")
    for family in data.get("settings", {}).get("typography", {}).get("fontFamilies", []):
        for face in family.get("fontFace", []):
            for src in face.get("src", []):
                if src.startswith("file:./") and not (ROOT / src[len("file:./"):]).is_file():
                    error(path, f"font file not found: {src}")


BLOCK = re.compile(r"<!--\s+(/?)wp:([a-z][a-z0-9_-]*(?:/[a-z][a-z0-9_-]*)?)\s*(\{.*?\})?\s*(/?)-->", re.S)


def check_block_markup():
    parts = {p.stem for p in (ROOT / "parts").glob("*.html")}
    for path in sorted([*ROOT.glob("templates/*.html"), *ROOT.glob("parts/*.html")]):
        text = path.read_text(encoding="utf-8")
        stack = []
        for match in BLOCK.finditer(text):
            closing, name, attrs, self_closing = match.groups()
            line = text.count("\n", 0, match.start()) + 1
            if attrs:
                try:
                    parsed = json.loads(attrs)
                except json.JSONDecodeError as exc:
                    error(path, f"line {line}: invalid attributes on wp:{name}: {exc}")
                    parsed = {}
                if name == "template-part" and parsed.get("slug") not in parts:
                    error(path, f"line {line}: template part '{parsed.get('slug')}' not found in parts/")
            if closing:
                if not stack:
                    error(path, f"line {line}: </wp:{name}> without an opening block")
                elif stack[-1][0] != name:
                    error(path, f"line {line}: </wp:{name}> closes wp:{stack[-1][0]} opened on line {stack[-1][1]}")
                    stack.pop()
                else:
                    stack.pop()
            elif not self_closing:
                stack.append((name, line))
        for name, line in stack:
            error(path, f"line {line}: wp:{name} is never closed")

        for match in re.finditer(r"\[jv_t\b([^\]]*)\]", text):
            attrs = dict(re.findall(r'(\w+)="([^"]*)"', match.group(1)))
            missing = [lang for lang in ("en", "cs") if not attrs.get(lang, "").strip()]
            if missing:
                line = text.count("\n", 0, match.start()) + 1
                error(path, f"line {line}: [jv_t] is missing {' and '.join(missing)} text")


def check_preloaded_fonts():
    path = ROOT / "functions.php"
    block = re.search(r"foreach\s*\(\s*array\(([^)]*)\)\s*as\s*\$font", path.read_text(encoding="utf-8"))
    for font in re.findall(r"'([^']+)'", block.group(1) if block else ""):
        if not (ROOT / "assets/fonts" / f"{font}.woff2").is_file():
            error(path, f"preloaded font not found: assets/fonts/{font}.woff2")


check_style_header()
check_theme_json()
check_block_markup()
check_preloaded_fonts()

for message in errors:
    print(f"error: {message}", file=sys.stderr)
if errors:
    sys.exit(1)
print("Theme file checks passed.")
