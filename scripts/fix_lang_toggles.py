#!/usr/bin/env python3
"""Fix language toggles: CS links must point to /cs/ paths; x-default → Czech."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOMAIN = "https://black-diamond.cz"
LANGS = ("cs", "en", "ru")
LABELS = {"cs": "CS", "en": "EN", "ru": "RU"}


def page_suffix(path: Path) -> str:
    parts = path.parts
    for i, part in enumerate(parts):
        if part in LANGS:
            rest = list(parts[i + 1:])
            if not rest or rest == ["index.html"]:
                return ""
            if rest[-1] == "index.html":
                rest = rest[:-1]
            return "/".join(rest)
    return ""


def lang_href(lang: str, suffix: str) -> str:
    if suffix:
        return f"/{lang}/{suffix}/"
    return f"/{lang}/"


def lang_abs(lang: str, suffix: str) -> str:
    return DOMAIN + lang_href(lang, suffix)


def lang_items(current_lang: str, suffix: str, indent: str) -> str:
    lines = []
    for lang in LANGS:
        href = lang_href(lang, suffix)
        active = lang == current_lang
        cls = "nav__lang-btn active" if active else "nav__lang-btn"
        aria = " aria-current=\"true\"" if active else ""
        lines.append(
            f"{indent}<li><a href=\"{href}\" class=\"{cls}\"{aria} "
            f"hreflang=\"{lang}\">{LABELS[lang]}</a></li>"
        )
    return "\n".join(lines)


def replace_lang_ul(html: str, ul_class: str, current_lang: str, suffix: str) -> str:
    pattern = re.compile(
        rf"(<ul class=\"{ul_class}\"[^>]*>)\s*(?:<li>.*?</li>\s*)+(</ul>)",
        re.DOTALL,
    )

    def repl(match: re.Match) -> str:
        open_tag = match.group(1)
        close_tag = match.group(2)
        indent_match = re.search(r"\n([ \t]*)<", open_tag)
        indent = indent_match.group(1) if indent_match else "          "
        close_indent = indent[:-2] if len(indent) >= 2 else indent
        inner = lang_items(current_lang, suffix, indent)
        return f"{open_tag}\n{inner}\n{close_indent}{close_tag}"

    return pattern.sub(repl, html)


def fix_hreflang_head(html: str, suffix: str) -> str:
    block_lines = [
        f'  <link rel="alternate" hreflang="{lang}" href="{lang_abs(lang, suffix)}">'
        for lang in LANGS
    ]
    block_lines.append(
        f'  <link rel="alternate" hreflang="x-default" href="{lang_abs("cs", suffix)}">'
    )
    block = "\n".join(block_lines)

    return re.sub(
        r"(?:  <link rel=\"alternate\" hreflang=\"[^\"]+\" href=\"[^\"]+\">\n?)+",
        block + "\n",
        html,
        count=1,
    )


def patch_file(path: Path) -> bool:
    current_lang = None
    for lang in LANGS:
        if f"/{lang}/" in str(path) or str(path).startswith(str(ROOT / lang)):
            parts = path.parts
            if lang in parts:
                current_lang = lang
                break
    if not current_lang:
        return False

    suffix = page_suffix(path)
    html = path.read_text(encoding="utf-8")
    original = html

    html = replace_lang_ul(html, "nav__lang", current_lang, suffix)
    html = replace_lang_ul(html, "nav__drawer-lang", current_lang, suffix)
    html = fix_hreflang_head(html, suffix)

    if html != original:
        path.write_text(html, encoding="utf-8")
        return True
    return False


def main() -> None:
    updated = 0
    for lang in LANGS:
        lang_dir = ROOT / lang
        if not lang_dir.is_dir():
            continue
        for path in sorted(lang_dir.rglob("*.html")):
            if patch_file(path):
                updated += 1
                print(f"fixed {path.relative_to(ROOT)}")

    print(f"Done: {updated} files updated")


if __name__ == "__main__":
    main()
