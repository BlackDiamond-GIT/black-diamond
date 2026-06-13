#!/usr/bin/env python3
"""Mobile nav fixes: WhatsApp, mob-bar, remove hero eyebrow, body class."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

WHATSAPP = (
    '<a href="https://wa.me/420797669633" class="nav__whatsapp" '
    'target="_blank" rel="noopener noreferrer" aria-label="WhatsApp">\n'
    '          <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
    '<path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15'
    '-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463'
    '-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134'
    '-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52'
    '-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371'
    '-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462'
    ' 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694'
    '.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248'
    '-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 '
    '01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51'
    '-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 '
    '9.825 0 012.893 6.994c-.003 5.45-4.435 9.884-9.885 9.884m8.413-18.297A11.815 '
    '11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945'
    'L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 '
    '11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>\n'
    '        </a>'
)

MOB = {
    'cs': [
        ('masaze', 'Masáže', False),
        ('masazistky', 'Masérky', False),
        ('masaze', 'Ceny', False),
        ('rozvrh', 'Rezervovat', True),
    ],
    'en': [
        ('masaze', 'Massages', False),
        ('masazistky', 'Masseuses', False),
        ('masaze', 'Prices', False),
        ('rozvrh', 'Book', True),
    ],
    'ru': [
        ('masaze', 'Массажи', False),
        ('masazistky', 'Массажистки', False),
        ('masaze', 'Цены', False),
        ('rozvrh', 'Забронировать', True),
    ],
}


def detect_lang(path: Path) -> str:
    parts = path.parts
    for lang in ('cs', 'en', 'ru'):
        if lang in parts:
            return lang
    return 'cs'


def mob_bar_html(lang: str, path: Path) -> str:
    rel = str(path).replace(str(ROOT), '')
    items = []
    for slug, label, cta in MOB[lang]:
        href = f'/{lang}/{slug}/'
        extra = ' mob-bar__item--cta' if cta else ''
        current = ''
        if slug == 'masaze' and label in ('Ceny', 'Prices', 'Цены'):
            if '/masaze/' in rel and 'masazistky' not in rel:
                current = ' aria-current="page"'
        elif f'/{slug}/' in rel or rel.endswith(f'/{slug}/index.html'):
            current = ' aria-current="page"'
        items.append(
            f'  <a href="{href}" class="mob-bar__item{extra}"{current}>{label}</a>'
        )
    inner = '\n'.join(items)
    return (
        f'<nav class="mob-bar" aria-label="Navigation">\n{inner}\n</nav>'
    )


def patch_html(html: str, path: Path) -> str:
    lang = detect_lang(path)

    html = re.sub(r'\s*<p class="hero2__eyebrow">[^<]*</p>\s*', '\n        ', html)

    if 'class="has-mob-bar"' not in html:
        html = html.replace('<body>', '<body class="has-mob-bar">')
        html = html.replace('<body\n', '<body class="has-mob-bar"\n')

    if 'mob-bar.css' not in html and 'nav.css' in html:
        html = html.replace(
            'href="/assets/css/components/nav.css">',
            'href="/assets/css/components/nav.css">\n'
            '  <link rel="stylesheet" href="/assets/css/components/mob-bar.css">',
        )

    if 'nav__whatsapp' not in html and 'nav__lang' in html:
        html = re.sub(
            r'(<div class="nav__right">\s*)<ul class="nav__lang"',
            r'\1' + WHATSAPP + '\n        <ul class="nav__lang"',
            html,
            count=1,
        )
        html = re.sub(
            r'(<div class="nav__right">\s*)<button class="nav__burger"',
            r'\1' + WHATSAPP + '\n        <button class="nav__burger"',
            html,
            count=1,
        )

    if '<nav class="mob-bar"' not in html:
        bar = mob_bar_html(lang, path)
        html = re.sub(
            r'(</footer>\s*)',
            f'</footer>\n\n  {bar}\n\n  ',
            html,
            count=1,
        )
        if '<nav class="mob-bar"' not in html:
            html = html.replace('</body>', f'{bar}\n</body>')

    return html


def main() -> None:
    count = 0
    for path in ROOT.rglob('*.html'):
        if '.venv' in path.parts:
            continue
        text = path.read_text(encoding='utf-8')
        if '<header class="nav"' not in text:
            continue
        patched = patch_html(text, path)
        if patched != text:
            path.write_text(patched, encoding='utf-8')
            print(f'Updated {path.relative_to(ROOT)}')
            count += 1
    print(f'Done. {count} files.')


if __name__ == '__main__':
    main()
