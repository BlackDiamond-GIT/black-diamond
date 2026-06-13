#!/usr/bin/env python3
"""Завантажує зображення з GitHub і генерує відсутні blog/og через Pillow."""

from __future__ import annotations

import re
import sys
import urllib.error
import urllib.request
from io import BytesIO
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMG_ROOT = ROOT / 'assets' / 'img'
GITHUB_RAW = (
    'https://raw.githubusercontent.com/BlackDiamond-GIT/black-diamond/main/assets/img'
)

BLOG_SOURCES = {
    'koristi-masazu-pro-zdorovi': 'services/klasicka-masaz.webp',
    'relaks-meditace-masaz': 'services/cbd-relaxacni-masaz.webp',
    'spa-retreat-kompletni-pruvodce': 'services/aromaterapie.webp',
}

OG_SOURCES = {
    'home.jpg': ('hero-spa.webp', (1200, 630)),
    'blog.jpg': ('atmosphere.webp', (1200, 630)),
    'masaze.jpg': ('services/klasicka-masaz.webp', (1200, 630)),
    'masazistky.jpg': ('masseuses/julia.webp', (1200, 630)),
    'rozvrh.jpg': ('hero.webp', (1200, 630)),
}


def collect_paths() -> set[str]:
    paths: set[str] = set()
    pattern = re.compile(r'/assets/img/([^"\s>]+)')
    for html in ROOT.rglob('*.html'):
        if '.git' in html.parts:
            continue
        for match in pattern.findall(html.read_text(errors='ignore')):
            if match.endswith('{%'):
                continue
            paths.add(match)
    return paths


def download(url: str, dest: Path) -> bool:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={'User-Agent': 'black-diamond-assets/1.0'})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
    except (urllib.error.URLError, TimeoutError) as exc:
        print(f'  skip download {dest.name}: {exc}')
        return False
    if len(data) < 200:
        print(f'  skip download {dest.name}: too small ({len(data)} B)')
        return False
    dest.write_bytes(data)
    print(f'  downloaded {dest.relative_to(ROOT)} ({len(data) // 1024} KB)')
    return True


def crop_cover(img, size: tuple[int, int]):
    from PIL import Image

    target_w, target_h = size
    src_w, src_h = img.size
    scale = max(target_w / src_w, target_h / src_h)
    resized = img.resize(
        (int(src_w * scale), int(src_h * scale)),
        Image.Resampling.LANCZOS,
    )
    left = (resized.width - target_w) // 2
    top = (resized.height - target_h) // 2
    return resized.crop((left, top, left + target_w, top + target_h))


def generate_webp(source_rel: str, dest: Path, size: tuple[int, int]) -> bool:
    from PIL import Image

    source = IMG_ROOT / source_rel
    if not source.is_file():
        print(f'  skip generate {dest.name}: missing source {source_rel}')
        return False
    img = Image.open(source).convert('RGB')
    cropped = crop_cover(img, size)
    dest.parent.mkdir(parents=True, exist_ok=True)
    cropped.save(dest, 'WEBP', quality=82, method=6)
    print(f'  generated {dest.relative_to(ROOT)}')
    return True


def generate_jpg(source_rel: str, dest: Path, size: tuple[int, int]) -> bool:
    from PIL import Image

    source = IMG_ROOT / source_rel
    if not source.is_file():
        print(f'  skip generate {dest.name}: missing source {source_rel}')
        return False
    img = Image.open(source).convert('RGB')
    cropped = crop_cover(img, size)
    dest.parent.mkdir(parents=True, exist_ok=True)
    cropped.save(dest, 'JPEG', quality=85, optimize=True)
    print(f'  generated {dest.relative_to(ROOT)}')
    return True


def main() -> int:
    print('Collecting image paths from HTML…')
    paths = collect_paths()
    print(f'Found {len(paths)} unique paths')

    for rel in sorted(paths):
        dest = IMG_ROOT / rel
        if dest.is_file() and dest.stat().st_size > 500:
            continue
        url = f'{GITHUB_RAW}/{rel}'
        if not download(url, dest):
            pass

    print('Generating blog images…')
    for slug, source in BLOG_SOURCES.items():
        dest = IMG_ROOT / 'blog' / f'{slug}.webp'
        if dest.is_file() and dest.stat().st_size > 500:
            continue
        generate_webp(source, dest, (1200, 675))

    print('Generating OG images…')
    for filename, (source, size) in OG_SOURCES.items():
        dest = IMG_ROOT / 'og' / filename
        if dest.is_file() and dest.stat().st_size > 500:
            continue
        generate_jpg(source, dest, size)

    missing = [
        p for p in sorted(paths)
        if not (IMG_ROOT / p).is_file()
    ]
    if missing:
        print('Still missing:')
        for item in missing:
            print(f'  - {item}')
        return 1

    print('All images ready.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
