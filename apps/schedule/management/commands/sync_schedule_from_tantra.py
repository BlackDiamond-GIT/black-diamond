"""Sync schedule from tantra-prague.com Hub API (replaces HTML scraper)."""

from __future__ import annotations

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from apps.schedule.seed_schedule import seed_schedule_entries
from apps.schedule.tantra_sync import sync_schedule_from_hub
from apps.schedule.week import business_date, parse_anchor_param


class Command(BaseCommand):
    help = "Sync schedule from tantra-prague.com Hub API for therapists in the local DB."

    def add_arguments(self, parser):
        parser.add_argument(
            "--from",
            dest="from_date",
            default="",
            help="Start date YYYY-MM-DD (default: today)",
        )
        parser.add_argument(
            "--days",
            type=int,
            default=35,
            help="Number of days to fetch (default: 35)",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Count only — do not write to DB",
        )

    def _seed_fallback(self, days: int, dry_run: bool, reason: str) -> None:
        weeks = max(1, (days + 6) // 7)
        self.stdout.write(self.style.WARNING(f"{reason} Using local schedule seed ({weeks} weeks)."))
        if dry_run:
            self.stdout.write("[dry-run] Would seed local schedule template.")
            return
        stats = seed_schedule_entries(weeks=weeks)
        self.stdout.write(
            f"Seeded: created {stats['created']}, updated {stats['updated']}, "
            f"skipped {stats['skipped']}"
        )
        self.stdout.write(self.style.SUCCESS("Schedule filled from local seed."))

    def handle(self, *args, **options):
        days = options["days"]
        dry_run = options["dry_run"]

        if not settings.HUB_API_KEY:
            self._seed_fallback(
                days,
                dry_run,
                "HUB_API_KEY is not set on this service.",
            )
            return

        from_date = (
            parse_anchor_param(options["from_date"])
            if options["from_date"]
            else business_date()
        )
        stats = sync_schedule_from_hub(
            from_date=from_date,
            days=days,
            dry_run=dry_run,
        )

        if "error" in stats:
            error = stats["error"]
            if "401" in error:
                raise CommandError(
                    f"{error} Check HUB_API_KEY in Render (web + cron) — "
                    "copy the UUID from tantra-prague.com admin → SiteConfig → black-diamond."
                )
            raise CommandError(f"Hub API error: {error}")

        prefix = "[dry-run] " if dry_run else ""
        self.stdout.write(
            f"{prefix}Fetched: {stats['fetched']}, matched: {stats['matched']}, "
            f"created: {stats['created']}, updated: {stats['updated']}, "
            f"skipped (unknown slug): {stats['skipped']}"
        )
        if not dry_run:
            self.stdout.write(self.style.SUCCESS("Schedule synced from hub API."))
