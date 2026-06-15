#!/usr/bin/env python3
"""Generate favicon PNG/ICO assets from vector facet data."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets' / 'img' / 'icons'

BG = '#14171b'
CANVAS = 32
CORNER_RADIUS = 7

FACETS = [
    ([(9, 7), (5, 13), (16, 13)], '#00827F'),
    ([(23, 7), (27, 13), (16, 13)], '#81D8D0'),
    ([(9, 7), (23, 7), (16, 13)], '#0ABAB5'),
    ([(5, 13), (12, 13), (16, 27)], '#006B68'),
    ([(12, 13), (20, 13), (16, 27)], '#0ABAB5'),
    ([(20, 13), (27, 13), (16, 27)], '#81D8D0'),
    ([(11, 8.5), (16, 11.5), (21, 8.5), (16, 7.5)], '#B8F0EC'),
]


def _scale_point(x: float, y: float, size: int) -> tuple[float, float]:
    factor = size / CANVAS
    return x * factor, y * factor


def render(size: int) -> Image.Image:
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img, 'RGBA')
    radius = CORNER_RADIUS * size / CANVAS
    draw.rounded_rectangle((0, 0, size - 1, size - 1), radius=radius, fill=BG)

    for points, color in FACETS:
        scaled = [_scale_point(x, y, size) for x, y in points]
        if color == '#B8F0EC':
            draw.polygon(scaled, fill=(184, 240, 236, 153))
        else:
            draw.polygon(scaled, fill=color)

    return img


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    outputs = {
        32: OUT / 'favicon-32.png',
        48: OUT / 'favicon-48.png',
        512: OUT / 'favicon-512.png',
        180: OUT / 'apple-touch-icon.png',
    }

    images: dict[int, Image.Image] = {}
    for size, path in outputs.items():
        image = render(size)
        images[size] = image
        image.save(path, format='PNG', optimize=True)
        print(f'wrote {path.relative_to(ROOT)}')

    ico_path = OUT / 'favicon.ico'
    ico_sizes = [16, 32, 48]
    ico_images = [render(size) for size in ico_sizes]
    ico_images[0].save(
        ico_path,
        format='ICO',
        sizes=[(size, size) for size in ico_sizes],
        append_images=ico_images[1:],
    )
    print(f'wrote {ico_path.relative_to(ROOT)}')


if __name__ == '__main__':
    main()
