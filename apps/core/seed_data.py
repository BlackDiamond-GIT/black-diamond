"""Дані для seed_site — масажі, масажистки, мапінг спеціальностей."""

from apps.core.seed_data_branches import BRANCHES
from apps.core.seed_data_services import SERVICES as _SERVICES_1
from apps.core.seed_data_services2 import SERVICES_PART2
from apps.core.seed_data_therapists1 import THERAPISTS_PART1
from apps.core.seed_data_therapists2 import THERAPISTS_PART2

SERVICES = _SERVICES_1 + SERVICES_PART2
THERAPISTS = THERAPISTS_PART1 + THERAPISTS_PART2

BLOG_SLUGS = [
    'koristi-masazu-pro-zdorovi',
    'relaks-meditace-masaz',
    'spa-retreat-kompletni-pruvodce',
]

BLOG_DATES = {
    'koristi-masazu-pro-zdorovi': '2026-01-15T10:00:00+02:00',
    'relaks-meditace-masaz': '2026-01-22T10:00:00+02:00',
    'spa-retreat-kompletni-pruvodce': '2026-02-01T10:00:00+02:00',
}
