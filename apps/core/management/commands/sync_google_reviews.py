"""
Sync home-page guest reviews from Google Places API (New).

Requires GOOGLE_PLACES_API_KEY; GOOGLE_PLACE_ID is optional (Text Search fallback).
Keeps up to six highest-rated reviews active on the home page (API returns max 5).
"""

from __future__ import annotations

from django.core.management.base import BaseCommand, CommandError

from apps.core.google_places import _api_key, fetch_place_reviews, get_place_id
from apps.core.models import GuestReview


class Command(BaseCommand):
    help = 'Sync GuestReview records from Google Places API (top reviews by rating).'

    def add_arguments(self, parser):
        parser.add_argument(
            '--limit',
            type=int,
            default=6,
            help='Number of reviews to activate on the home page (default: 6).',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Print changes without saving.',
        )

    def handle(self, *args, **options):
        api_key = _api_key()
        if not api_key:
            raise CommandError('Set GOOGLE_PLACES_API_KEY in the environment.')

        try:
            place_id = get_place_id(api_key)
        except RuntimeError as exc:
            raise CommandError(str(exc)) from exc

        self.stdout.write(f'Using place ID: {place_id}')

        limit = max(1, min(int(options['limit']), 6))
        dry_run = bool(options['dry_run'])

        try:
            reviews = fetch_place_reviews(place_id, api_key)
        except RuntimeError as exc:
            raise CommandError(str(exc)) from exc

        if not reviews:
            raise CommandError('No reviews returned for this place.')

        ranked = sorted(
            reviews,
            key=lambda r: (r.get('rating') or 0, len(r.get('text') or '')),
            reverse=True,
        )[:limit]

        if dry_run:
            for idx, row in enumerate(ranked):
                self.stdout.write(f"[{idx}] {row['author_label']} ({row.get('rating')}★)")
                snippet = row['text'][:200]
                self.stdout.write(snippet + ('…' if len(row['text']) > 200 else ''))
            return

        synced_ids: list[str] = []
        for order, row in enumerate(ranked):
            defaults = {
                'order': order,
                'author_label': row['author_label'],
                'city': '',
                'text_cs': row['text'],
                'rating': row.get('rating'),
                'is_active': True,
            }
            obj, created = GuestReview.objects.update_or_create(
                google_review_id=row['google_review_id'],
                defaults=defaults,
            )
            synced_ids.append(row['google_review_id'])
            verb = 'Created' if created else 'Updated'
            self.stdout.write(f'  {verb}: {obj.author_label}')

        GuestReview.objects.filter(google_review_id__isnull=False).exclude(
            google_review_id__in=synced_ids,
        ).update(is_active=False)

        self.stdout.write(self.style.SUCCESS(f'Synced {len(synced_ids)} Google review(s).'))
