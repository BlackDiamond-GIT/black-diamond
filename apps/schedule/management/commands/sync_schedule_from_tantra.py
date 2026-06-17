"""Sync schedule from tantra-prague.com Hub API (replaces HTML scraper)."""

from __future__ import annotations

from django.core.management.base import BaseCommand

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

    def handle(self, *args, **options):
        from_date = (
            parse_anchor_param(options["from_date"])
            if options["from_date"]
            else business_date()
        )
        stats = sync_schedule_from_hub(
            from_date=from_date,
            days=options["days"],
            dry_run=options["dry_run"],
        )

        if "error" in stats:
            self.stderr.write(self.style.ERROR(f"Hub API error: {stats['error']}"))
            return

        prefix = "[dry-run] " if options["dry_run"] else ""
        self.stdout.write(
            f"{prefix}Fetched: {stats['fetched']}, matched: {stats['matched']}, "
            f"created: {stats['created']}, updated: {stats['updated']}, "
            f"skipped (unknown slug): {stats['skipped']}"
        )
        if not options["dry_run"]:
            self.stdout.write(self.style.SUCCESS("Schedule synced from hub API."))
