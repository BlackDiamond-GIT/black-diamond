"""Синхронізує розклад з tantra-prague.com/cs/rozvrh/."""

from __future__ import annotations

from django.core.management.base import BaseCommand

from apps.branches.models import Branch
from apps.schedule.tantra_sync import sync_schedule_from_tantra
from apps.schedule.week import business_date, parse_anchor_param


class Command(BaseCommand):
    help = 'Імпортує розклад з tantra-prague.com для масажисток, що є в БД.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--from',
            dest='from_date',
            default='',
            help='Початкова дата (YYYY-MM-DD), за замовчуванням — сьогодні',
        )
        parser.add_argument(
            '--weeks',
            type=int,
            default=5,
            help='Скільки тижнів (по 7 днів) завантажити',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Лише підрахунок без запису в БД',
        )

    def handle(self, *args, **options):
        if not Branch.objects.filter(is_active=True).exists():
            self.stderr.write(
                self.style.ERROR(
                    'Немає філій у БД. Спочатку запустіть: python manage.py seed_site --force'
                )
            )
            return

        anchor = (
            parse_anchor_param(options['from_date'])
            if options['from_date']
            else business_date()
        )
        stats = sync_schedule_from_tantra(
            weeks=options['weeks'],
            anchor=anchor,
            dry_run=options['dry_run'],
        )

        prefix = '[dry-run] ' if options['dry_run'] else ''
        self.stdout.write(
            f'{prefix}Завантажено: {stats["fetched"]}, '
            f'зіставлено: {stats["matched"]}, '
            f'створено: {stats["created"]}, '
            f'оновлено: {stats["updated"]}, '
            f'пропущено: {stats["skipped"]}'
        )
        if stats['fetch_errors']:
            self.stdout.write(
                self.style.WARNING(f'Помилки завантаження тижнів: {stats["fetch_errors"]}')
            )
        if not options['dry_run']:
            self.stdout.write(self.style.SUCCESS('Розклад синхронізовано.'))
