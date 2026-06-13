#!/usr/bin/env python3
"""Remove all years-of-experience mentions from static HTML files."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Meta descriptions: remove "N let zkušeností" / "N years" / "N лет"
META_PATTERNS = [
    re.compile(r'\.\s*\d+\s+let zkušeností\.', re.I),
    re.compile(r'\.\s*\d+\s+let zkušeností', re.I),
    re.compile(r'\.\s*\d+\s+years of experience\.?', re.I),
    re.compile(r'\.\s*\d+\s+years\.?', re.I),
    re.compile(r'\.\s*\d+\s+лет[^.]*\.?', re.I),
    re.compile(r'\.\s*\d+\s+год[^.]*\.?', re.I),
]

# Badge overlay on masseuse photo
BADGE_RE = re.compile(
    r'\s*<div style="position:absolute;top:var\(--sp-md\);right:var\(--sp-md\);[^"]*">\s*\d+\s+let zkušeností\s*</div>',
    re.DOTALL,
)

# Tag spans with praxe / experience
TAG_RE = re.compile(
    r'\s*<span class="tag tag--duration">\d+\s+let praxe</span>',
    re.I,
)
TAG_EN_RE = re.compile(
    r'\s*<span class="tag tag--duration">\d+\s+years?</span>',
    re.I,
)
TAG_RU_RE = re.compile(
    r'\s*<span class="tag tag--duration">\d+\s+(?:лет|год(?:а|ов)?)\s+(?:практики|опыта)</span>',
    re.I,
)

# Masseuse card years on listing page
CARD_YEARS_RE = re.compile(
    r'\s*<span class="masseuse-card__years">[^<]+</span>',
    re.I,
)

# Bio text mentioning years (Czech)
BIO_YEARS_RE = re.compile(
    r'\b\d+\s+let(?:\s+praxe|\s+zkušeností)?\b',
    re.I,
)


def clean_html(text: str) -> str:
    for pat in META_PATTERNS:
        text = pat.sub('.', text)
    text = BADGE_RE.sub('', text)
    text = TAG_RE.sub('', text)
    text = TAG_EN_RE.sub('', text)
    text = TAG_RU_RE.sub('', text)
    text = CARD_YEARS_RE.sub('', text)
    return text


def fix_footer_html(html: str) -> str:
    if 'footer__disclaimer-text' not in html and 'footer__disclaimer' in html:
        html = re.sub(
            r'<div class="footer__disclaimer">\s*([^<]+?)\s*</div>',
            lambda m: (
                '<div class="footer__disclaimer">\n'
                f'    <p class="footer__disclaimer-text">{m.group(1).strip()}</p>\n'
                '  </div>'
            ),
            html,
            count=1,
        )

    match = re.search(
        r'(<footer[^>]*>.*?<div class="container">\s*'
        r'<div class="footer__grid">.*?</div>\s*)\s*'
        r'(<div class="footer__disclaimer">.*?</div>)\s*'
        r'(<div class="footer__bottom">.*?</div>)\s*'
        r'(</div>\s*</footer>)',
        html,
        flags=re.DOTALL,
    )
    if match:
        grid_part = match.group(1)
        disc = match.group(2)
        bottom = match.group(3)
        footer_end = match.group(4)
        replacement = (
            f'{grid_part}  </div>\n\n  {disc}\n\n  <div class="container">\n    {bottom}\n  </div>\n{footer_end}'
        )
        html = html[:match.start()] + replacement + html[match.end():]
    return html


def main() -> None:
    changed = 0
    for path in ROOT.rglob('*.html'):
        if '.venv' in path.parts:
            continue
        text = path.read_text(encoding='utf-8')
        cleaned = clean_html(text)
        if 'footer__disclaimer' in cleaned:
            cleaned = fix_footer_html(cleaned)
        if cleaned != text:
            path.write_text(cleaned, encoding='utf-8')
            print(f'Updated: {path.relative_to(ROOT)}')
            changed += 1

    print(f'Done. {changed} files updated.')


if __name__ == '__main__':
    main()
