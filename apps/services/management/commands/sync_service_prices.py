"""Sync service price and duration from seed_data (safe for production)."""

from django.core.management.base import BaseCommand

from apps.core.seed_data import SERVICES
from apps.services.models import Service
from apps.services.pricing_catalog import CATALOG_DURATIONS, normalize_duration

LEGACY_SLUG = 'thajska-masaz'
CURRENT_SLUG = 'hlubokotkaninni-masaz'

_CONTENT_KEYS = (
    'description_cs', 'description_en', 'description_ru',
    'what_cs', 'what_en', 'what_ru',
    'who_cs', 'who_en', 'who_ru',
    'meta_title_cs', 'meta_title_en', 'meta_title_ru',
    'meta_description_cs', 'meta_description_en', 'meta_description_ru',
    'faq_cs', 'faq_en', 'faq_ru',
)


class Command(BaseCommand):
    help = 'Synchronize massage prices and durations from seed_data (45 / 60 / 90 min).'

    def handle(self, *args, **options):
        if Service.objects.filter(slug=LEGACY_SLUG).exists():
            Service.objects.filter(slug=LEGACY_SLUG).update(slug=CURRENT_SLUG)
            self.stdout.write(self.style.WARNING(f'  renamed {LEGACY_SLUG} → {CURRENT_SLUG}'))

        updated = 0
        for item in SERVICES:
            slug = item['slug']
            try:
                service = Service.objects.get(slug=slug)
            except Service.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'  skip {slug}: not in DB'))
                continue

            duration = normalize_duration(int(item['duration']))
            price = int(item['price'])
            fields = {
                'duration': duration,
                'price': price,
                'base_price_czk': price,
                'base_duration_min': duration,
                'title_cs': item.get('title_cs', ''),
                'title_en': item.get('title_en', ''),
                'title_ru': item.get('title_ru', ''),
                'short_cs': item.get('short_cs', ''),
                'short_en': item.get('short_en', ''),
                'short_ru': item.get('short_ru', ''),
            }
            for key in _CONTENT_KEYS:
                if key in item:
                    fields[key] = item[key]
            changed = False
            for field, value in fields.items():
                if getattr(service, field) != value:
                    setattr(service, field, value)
                    changed = True
            if changed:
                service.save(update_fields=list(fields.keys()))
                updated += 1
            self.stdout.write(f'  {slug}: {duration} min / {price} Kč — {fields["title_cs"]}')

        self.stdout.write(self.style.SUCCESS(
            f'Done. Updated {updated} services. Allowed durations: {", ".join(map(str, CATALOG_DURATIONS))} min.'
        ))
