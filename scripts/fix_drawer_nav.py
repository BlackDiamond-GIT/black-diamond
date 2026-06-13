#!/usr/bin/env python3
"""Update mobile drawer: remove lang toggle, add info pages."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANGS = ("cs", "en", "ru")

EXTRA = {
    "cs": [
        ("o-nas", "O nás"),
        ("pravidla-salonu", "Pravidla salonu"),
        ("soukromi", "Soukromí & GDPR"),
    ],
    "en": [
        ("o-nas", "About Us"),
        ("pravidla-salonu", "Salon Rules"),
        ("soukromi", "Privacy & GDPR"),
    ],
    "ru": [
        ("o-nas", "О нас"),
        ("pravidla-salonu", "Правила салона"),
        ("soukromi", "Конфиденциальность"),
    ],
}


def detect_lang(path: Path) -> str | None:
    for lang in LANGS:
        if lang in path.parts:
            return lang
    return None


def is_current_slug(rel: str, slug: str) -> bool:
    if slug == "o-nas":
        return "/o-nas/" in rel
    if slug == "pravidla-salonu":
        return "/pravidla-salonu/" in rel
    if slug == "soukromi":
        return "/soukromi/" in rel
    return False


def extra_lines(lang: str, rel: str, indent: str) -> str:
    lines = []
    for slug, label in EXTRA[lang]:
        href = f"/{lang}/{slug}/"
        aria = " aria-current=\"page\"" if is_current_slug(rel, slug) else ""
        lines.append(f"{indent}<li><a href=\"{href}\"{aria}>{label}</a></li>")
    return "\n".join(lines)


def patch_html(html: str, lang: str, rel: str) -> str:
    html = re.sub(
        r"\s*<ul class=\"nav__drawer-lang\"[^>]*>.*?</ul>",
        "",
        html,
        flags=re.DOTALL,
    )

    if "nav__drawer-links" not in html:
        return html

    drawer_chunk = html.split("nav__drawer-links", 1)[1].split("</ul>", 1)[0]
    if "/o-nas/" in drawer_chunk:
        return html

    pattern = re.compile(
        r"(<ul class=\"nav__drawer-links\"[^>]*>)(.*?)(</ul>)",
        re.DOTALL,
    )

    def repl(match: re.Match) -> str:
        inner = match.group(2)
        indent_match = re.search(r"\n([ \t]*)<li>", inner)
        indent = indent_match.group(1) if indent_match else "      "
        extra = extra_lines(lang, rel, indent)
        return f"{match.group(1)}{inner.rstrip()}\n{extra}\n{indent[:-2]}{match.group(3)}"

    return pattern.sub(repl, html, count=1)


def main() -> None:
    updated = 0
    for lang in LANGS:
        lang_dir = ROOT / lang
        if not lang_dir.is_dir():
            continue
        for path in sorted(lang_dir.rglob("*.html")):
            rel = str(path.relative_to(ROOT)).replace("\\", "/")
            html = path.read_text(encoding="utf-8")
            new_html = patch_html(html, lang, rel)
            if new_html != html:
                path.write_text(new_html, encoding="utf-8")
                updated += 1
                print(f"fixed {rel}")

    print(f"Done: {updated} files updated")


if __name__ == "__main__":
    main()
