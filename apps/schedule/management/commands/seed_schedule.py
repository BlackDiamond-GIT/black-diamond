"""Заповнює розклад шаблонними змінами (як black-velvet)."""

from django.core.management.base import BaseCommand

from apps.schedule.seed_schedule import seed_schedule_entries
from apps.schedule.week import MAX_WEEKS
from apps.therapists.models import Therapist


class Command(BaseCommand):
    help = 'Seed weekly schedule entries for active therapists (velvet-style pattern).'

    def add_arguments(self, parser):
        parser.add_argument(
            '--weeks',
            type=int,
            default=MAX_WEEKS,
            help='How many ISO weeks to fill from the current week',
        )

    def handle(self, *args, **options):
        if not Therapist.objects.filter(is_active=True).exists():
            self.stderr.write(
                self.style.ERROR('No therapists in DB. Run: python3 manage.py seed_site --force')
            )
            return

        stats = seed_schedule_entries(weeks=options['weeks'])
        self.stdout.write(
            self.style.SUCCESS(
                f'Done: created {stats["created"]}, updated {stats["updated"]}, '
                f'skipped {stats["skipped"]} (unknown therapist).'
            )
        )
