"""Заповнює БД масажистками, масажами та статтями блогу."""

from __future__ import annotations

import re
from datetime import datetime
from html import unescape
from pathlib import Path

from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_datetime

from apps.blog.models import Article
from apps.branches.models import Branch
from apps.services.models import Service
from apps.therapists.models import Therapist

from apps.core.seed_data import BLOG_DATES, BLOG_SLUGS, BRANCHES, SERVICES, THERAPISTS

ROOT = Path(__file__).resolve().parents[4]


def _meta(content: str, name: str) -> str:
    match = re.search(
        rf'<meta\s+name="{re.escape(name)}"\s+content="([^"]*)"',
        content,
        re.IGNORECASE,
    )
    return unescape(match.group(1)).strip() if match else ''


def _blog_body(content: str) -> str:
    match = re.search(
        r'<div class="blog-post__content"[^>]*>(.*?)</div>\s*(?:<!-- CTA -->|<div class="glass")',
        content,
        re.DOTALL | re.IGNORECASE,
    )
    if not match:
        return ''
    body = match.group(1).strip()
    body = re.sub(r'\s*\n\s*', '\n', body)
    return body


def _blog_title(content: str) -> str:
    match = re.search(
        r'<h1[^>]*itemprop="headline"[^>]*>(.*?)</h1>',
        content,
        re.DOTALL | re.IGNORECASE,
    )
    if match:
        return re.sub(r'<[^>]+>', '', match.group(1)).strip()
    title = _meta(content, 'description')
    if '|' in content:
        head = re.search(r'<title>([^<|]+)', content)
        if head:
            return head.group(1).strip()
    return title


def _read_blog(lang: str, slug: str) -> dict[str, str]:
    path = ROOT / lang / 'blog' / slug / 'index.html'
    if not path.is_file():
        return {'title': '', 'meta_description': '', 'body': ''}
    text = path.read_text(encoding='utf-8')
    return {
        'title': _blog_title(text),
        'meta_description': _meta(text, 'description').split('|')[0].strip(),
        'body': _blog_body(text),
    }


class Command(BaseCommand):
    help = 'Заповнює БД масажистками, масажами та статтями блогу z seed_data (blog z HTML).'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Оновити існуючі записи',
        )

    def handle(self, *args, **options):
        force = options['force']
        services_by_slug: dict[str, Service] = {}

        branches_by_name: dict[str, Branch] = {}
        for item in BRANCHES:
            defaults = {k: v for k, v in item.items() if k != 'name'}
            if force:
                obj, created = Branch.objects.update_or_create(
                    name=item['name'],
                    defaults=defaults,
                )
            else:
                obj, created = Branch.objects.get_or_create(
                    name=item['name'],
                    defaults=defaults,
                )
            branches_by_name[obj.name] = obj
            self.stdout.write(f'  branch {obj.name}: {"created" if created else "exists"}')

        for item in SERVICES:
            slug = item['slug']
            defaults = {k: v for k, v in item.items() if k != 'slug'}
            defaults['base_price_czk'] = defaults.get('price', 0)
            defaults['base_duration_min'] = defaults.get('duration', 60)

            if force:
                obj, created = Service.objects.update_or_create(
                    slug=slug,
                    defaults=defaults,
                )
            else:
                obj, created = Service.objects.get_or_create(
                    slug=slug,
                    defaults=defaults,
                )
            services_by_slug[slug] = obj
            self.stdout.write(f'  service {obj.slug}: {"created" if created else "exists"}')

        for item in THERAPISTS:
            spec_slugs = item['specialties']
            offer_slugs = item.get('offers', spec_slugs)
            defaults = {
                k: v for k, v in item.items()
                if k not in ('slug', 'specialties', 'offers')
            }
            if force:
                obj, created = Therapist.objects.update_or_create(
                    slug=item['slug'],
                    defaults=defaults,
                )
            else:
                obj, created = Therapist.objects.get_or_create(
                    slug=item['slug'],
                    defaults=defaults,
                )
            obj.specialties.set([services_by_slug[s] for s in spec_slugs if s in services_by_slug])
            obj.offers.set([services_by_slug[s] for s in offer_slugs if s in services_by_slug])
            if branches_by_name:
                obj.branches.set(branches_by_name.values())
            self.stdout.write(f'  therapist {obj.name}: {"created" if created else "exists"}')

        for slug in BLOG_SLUGS:
            cs = _read_blog('cs', slug)
            en = _read_blog('en', slug)
            ru = _read_blog('ru', slug)
            published = parse_datetime(BLOG_DATES[slug]) or datetime(2026, 1, 15, 10, 0)

            defaults = {
                'title_cs': cs['title'],
                'title_en': en['title'] or cs['title'],
                'title_ru': ru['title'] or cs['title'],
                'body_cs': cs['body'],
                'body_en': en['body'] or cs['body'],
                'body_ru': ru['body'] or cs['body'],
                'meta_description_cs': cs['meta_description'][:160],
                'meta_description_en': (en['meta_description'] or cs['meta_description'])[:160],
                'meta_description_ru': (ru['meta_description'] or cs['meta_description'])[:160],
                'published_at': published,
                'is_published': True,
            }
            if force:
                obj, created = Article.objects.update_or_create(slug=slug, defaults=defaults)
            else:
                obj, created = Article.objects.get_or_create(slug=slug, defaults=defaults)
            self.stdout.write(f'  article {slug}: {"created" if created else "exists"}')

        if Therapist.objects.filter(is_active=True).exists():
            from apps.schedule.seed_schedule import seed_schedule_entries
            sched = seed_schedule_entries()
            self.stdout.write(
                f'  schedule: created {sched["created"]}, updated {sched["updated"]}'
            )

        from apps.core.models import SiteSettings
        from apps.core.opening_hours import ensure_hours_i18n

        site = SiteSettings.load()
        if ensure_hours_i18n(site):
            self.stdout.write('  site hours: filled EN/RU defaults')

        self.stdout.write(self.style.SUCCESS(
            f'Done: {Branch.objects.count()} branches, '
            f'{Service.objects.count()} services, '
            f'{Therapist.objects.count()} therapists, '
            f'{Article.objects.count()} articles'
        ))
