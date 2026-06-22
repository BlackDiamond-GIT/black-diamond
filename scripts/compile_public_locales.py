#!/usr/bin/env python3
"""Compile public site locales (en, ru) from Czech msgid dictionaries."""

from __future__ import annotations

import re
import sys
from pathlib import Path

import polib

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE / 'scripts'))

from public_locales_data import PUBLIC_EN, PUBLIC_RU  # noqa: E402

LOCALES = {
    'en': PUBLIC_EN,
    'ru': PUBLIC_RU,
}

TRANS_PATTERN = re.compile(r'\{%\s*trans\s+["\'](.+?)["\']\s*%\}')
BLOCKTRANS_PATTERN = re.compile(
    r'\{%\s*blocktrans\s*%\}(.+?)\{%\s*endblocktrans\s*%\}',
    re.S,
)

EXTRA_MSGIDS = (
    'Denní',
    'Noční',
    'Day',
    'Night',
    'Therapist',
    'Date',
    'From',
    'To',
    'Shift',
    'Work address',
)


def collect_template_msgids() -> set[str]:
    msgids: set[str] = set(EXTRA_MSGIDS)
    templates_dir = BASE / 'templates'
    for path in templates_dir.rglob('*.html'):
        text = path.read_text(encoding='utf-8', errors='ignore')
        msgids.update(TRANS_PATTERN.findall(text))
        msgids.update(BLOCKTRANS_PATTERN.findall(text))
    return msgids


def build_po(lang: str, translations: dict[str, str], msgids: set[str]) -> polib.POFile:
    missing = sorted(msgids - translations.keys())
    if missing:
        print(f'Warning [{lang}]: {len(missing)} untranslated msgids', file=sys.stderr)
        for item in missing[:10]:
            print(f'  - {item}', file=sys.stderr)
        if len(missing) > 10:
            print(f'  ... and {len(missing) - 10} more', file=sys.stderr)

    po = polib.POFile()
    po.metadata = {
        'Project-Id-Version': 'Black Diamond Spa',
        'Language': lang,
        'Content-Type': 'text/plain; charset=UTF-8',
    }

    for msgid in sorted(msgids):
        msgstr = translations.get(msgid, '')
        po.append(polib.POEntry(msgid=msgid, msgstr=msgstr))

    return po


def main() -> None:
    msgids = collect_template_msgids()

    for lang, translations in LOCALES.items():
        po_path = BASE / 'locale' / lang / 'LC_MESSAGES' / 'django.po'
        mo_path = po_path.with_suffix('.mo')
        po_path.parent.mkdir(parents=True, exist_ok=True)

        po = build_po(lang, translations, msgids)
        po.save(str(po_path))
        po.save_as_mofile(str(mo_path))
        translated = sum(1 for e in po if e.msgstr)
        print(f'[{lang}] {translated}/{len(po)} strings -> {mo_path}')


if __name__ == '__main__':
    main()
