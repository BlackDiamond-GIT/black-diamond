#!/usr/bin/env python3
"""Sync footer hours + Telegram across static HTML exports."""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')

import django

django.setup()

from apps.core.models import SiteSettings
from apps.core.opening_hours import DEFAULT_HOURS

HOURS_NAP = """          <div class="footer__nap-item">
            <svg class="footer__nap-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true">
              <circle cx="12" cy="12" r="10"/>
              <polyline points="12 6 12 12 16 14"/>
            </svg>
            <span class="footer__hours-text" itemprop="openingHours">{hours}</span>
          </div>"""

TELEGRAM_LINK = """          <a href="{url}" class="footer__social-link" rel="noopener noreferrer" aria-label="Telegram" target="_blank">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
              <path d="M11.944 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0a12 12 0 0 0-.056 0zm4.962 7.224c.1-.002.321.023.465.14a.506.506 0 0 1 .171.325c.016.093.036.306.02.472-.18 1.898-.962 6.502-1.36 8.627-.168.9-.499 1.201-.82 1.23-.696.065-1.225-.46-1.9-.902-1.056-.693-1.653-1.124-2.678-1.8-1.185-.78-.417-1.21.258-1.91.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.14-5.061 3.345-.48.33-.913.49-1.302.48-.428-.008-1.252-.241-1.865-.44-.752-.245-1.349-.374-1.297-.789.027-.216.325-.437.893-.663 3.498-1.524 5.83-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635z"/>
            </svg>
          </a>"""

HOURS_COLUMN_RE = re.compile(
    r'\s*<div>\s*<h3 class="footer__col-title">[^<]*</h3>\s*<div class="footer__hours">.*?</div>\s*</div>',
    re.DOTALL,
)

SCHEMA_OLD = re.compile(
    r'"openingHoursSpecification"\s*:\s*\[\s*\{[\s\S]*?\}\s*,\s*\{[\s\S]*?\}\s*\]',
)

CONTACT_HOURS_OLD = re.compile(
    r'(<h2 style="font-family:var\(--font-display\);font-size:var\(--fs-xl\);margin-bottom:var\(--sp-xl\)">[^<]+</h2>\s*)'
    r'<div style="display:flex;flex-direction:column;gap:var\(--sp-md\)">[\s\S]*?</div>',
)


def contact_hours_block(hours: str) -> str:
    return f'''<div style="display:flex;align-items:center;gap:var(--sp-md)">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--tiffany)" stroke-width="1.5" style="flex-shrink:0" aria-hidden="true">
                  <circle cx="12" cy="12" r="10"/>
                  <polyline points="12 6 12 12 16 14"/>
                </svg>
                <p style="color:var(--tiffany);font-weight:600;font-size:var(--fs-md);margin:0" itemprop="openingHours">{hours}</p>
              </div>'''

SCHEMA_NEW = '''"openingHoursSpecification": [
      {
        "@type": "OpeningHoursSpecification",
        "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
        "opens": "09:00",
        "closes": "04:00"
      }
    ]'''

SCHEDULE_BAR_RE = re.compile(
    r'<div class="schedule__hours-bar"[^>]*>.*?</div>',
    re.DOTALL,
)


def detect_lang(path: Path) -> str:
    parts = path.parts
    for code in ('cs', 'en', 'ru'):
        if code in parts:
            return code
    return 'cs'


def build_schedule_bar(hours: str) -> str:
    return f'''<div class="schedule__hours-bar" role="complementary" aria-label="Opening hours">
      <svg class="schedule__hours-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true">
        <circle cx="12" cy="12" r="10"/>
        <polyline points="12 6 12 12 16 14"/>
      </svg>
      <span class="schedule__hours-text">{hours}</span>
      &nbsp;|&nbsp;
      <a href="tel:+420797669633" style="color:var(--tiffany)">+420 797 669 633</a>
    </div>'''


def patch_html(content: str, lang: str, telegram_url: str, instagram_url: str) -> str:
    hours = DEFAULT_HOURS.get(lang, DEFAULT_HOURS['cs'])
    try:
        site = SiteSettings.load()
        hours = site.get_hours_for_language(lang)
    except Exception:
        pass

    if 'footer__hours-text' not in content and 'itemprop="email"' in content:
        content = content.replace(
            '</address>',
            HOURS_NAP.format(hours=hours) + '\n          </address>',
            1,
        )
        content = re.sub(
            r'(itemprop="email">[^<]+</a>\s*</div>\s*)(</address>)',
            r'\1' + HOURS_NAP.format(hours=hours) + '\n          \2',
            content,
            count=1,
        )

    content = HOURS_COLUMN_RE.sub('', content)

    if telegram_url and 'aria-label="Telegram"' not in content:
        content = content.replace(
            '</div>\n\n        <div>\n          <h3 class="footer__col-title">Stránky',
            TELEGRAM_LINK.format(url=telegram_url) + '\n          </div>\n\n        <div>\n          <h3 class="footer__col-title">Stránky',
        )
        content = content.replace(
            '</svg>\n            </a>\n          </div>\n        </div>',
            '</svg>\n            </a>\n' + TELEGRAM_LINK.format(url=telegram_url) + '\n          </div>\n        </div>',
            1,
        )

    if instagram_url:
        content = content.replace(
            'https://instagram.com/blackdiamondspa',
            instagram_url,
        )

    content = SCHEMA_OLD.sub(SCHEMA_NEW, content)
    content = CONTACT_HOURS_OLD.sub(
        lambda m: m.group(1) + contact_hours_block(hours),
        content,
    )

    if 'schedule__hours-bar' in content:
        content = SCHEDULE_BAR_RE.sub(build_schedule_bar(hours), content, count=1)

    return content


def main() -> None:
    site = SiteSettings.load()
    if site.hours == 'Od 11 ráno do 4 ráno':
        site.hours = 'Od 9 ráno do 4 ráno'
        site.save(update_fields=['hours'])
    if not site.hours_en:
        site.hours_en = DEFAULT_HOURS['en']
        site.save(update_fields=['hours_en'])
    if not site.hours_ru:
        site.hours_ru = DEFAULT_HOURS['ru']
        site.save(update_fields=['hours_ru'])

    telegram_url = (site.telegram_url or '').strip()
    instagram_url = (site.instagram_url or '').strip() or 'https://instagram.com/blackdiamondspa'

    targets = list(ROOT.glob('cs/**/*.html'))
    targets += list(ROOT.glob('en/**/*.html'))
    targets += list(ROOT.glob('ru/**/*.html'))
    targets.append(ROOT / 'partials' / 'footer-cs.html')

    updated = 0
    for path in targets:
        if path.name.startswith('.'):
            continue
        text = path.read_text(encoding='utf-8')
        if 'footer__grid' not in text and 'schedule__hours-bar' not in text:
            continue
        lang = detect_lang(path)
        new_text = patch_html(text, lang, telegram_url, instagram_url)
        if new_text != text:
            path.write_text(new_text, encoding='utf-8')
            updated += 1
            print(f'updated: {path.relative_to(ROOT)}')

    print(f'done — {updated} files')


if __name__ == '__main__':
    main()
