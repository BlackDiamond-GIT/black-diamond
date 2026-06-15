"""Parse massage detail pages from static HTML exports."""

from __future__ import annotations

import json
import re
from html import unescape
from pathlib import Path


def _strip_html(value: str) -> str:
    return unescape(re.sub(r'<[^>]+>', '', value)).strip()


def _section_text(content: str, heading_id: str) -> str:
    match = re.search(
        rf'id="{re.escape(heading_id)}"[^>]*>.*?</h2>\s*<p[^>]*>(.*?)</p>',
        content,
        re.DOTALL | re.IGNORECASE,
    )
    return _strip_html(match.group(1)) if match else ''


def _lead_description(content: str) -> str:
    match = re.search(
        r'itemprop="description"[^>]*>(.*?)</p>',
        content,
        re.DOTALL | re.IGNORECASE,
    )
    return _strip_html(match.group(1)) if match else ''


def _faq_items(content: str) -> list[dict[str, str]]:
    for block in re.findall(
        r'<script type="application/ld\+json">\s*(\{[\s\S]*?\})\s*</script>',
        content,
        re.IGNORECASE,
    ):
        try:
            data = json.loads(block)
        except json.JSONDecodeError:
            continue
        if data.get('@type') != 'FAQPage':
            continue
        items = []
        for entry in data.get('mainEntity', []):
            question = entry.get('name', '').strip()
            answer = entry.get('acceptedAnswer', {}).get('text', '').strip()
            if question and answer:
                items.append({'q': question, 'a': answer})
        return items
    return []


def read_service_page(root: Path, lang: str, slug: str) -> dict:
    path = root / lang / 'masaze' / slug / 'index.html'
    if not path.is_file():
        return {}

    content = path.read_text(encoding='utf-8')
    return {
        'description': _lead_description(content),
        'what': _section_text(content, 'what-heading'),
        'who': _section_text(content, 'who-heading'),
        'faq': _faq_items(content),
    }
