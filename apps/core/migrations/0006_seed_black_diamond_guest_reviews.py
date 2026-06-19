"""Add Black Diamond Google Maps guest reviews (Opletalova 30, Praha 1)."""

from __future__ import annotations

from django.db import migrations

BLACK_DIAMOND_REVIEWS = [
    {
        'order': 0,
        'google_review_id': 'google-bd-elias-schmelzer',
        'rating': 5,
        'author_label': 'Elias S.',
        'city': '',
        'text_cs': (
            'I visited the place at Opletalova 30 recently and was really impressed. '
            'The interior looked newly renovated and very luxurious. Everything felt '
            'clean, modern, and calm. You could tell a lot of care went into the '
            'design and details.'
        ),
        'text_en': '',
        'text_ru': '',
    },
    {
        'order': 1,
        'google_review_id': 'google-bd-leon-koch',
        'rating': 5,
        'author_label': 'Leon K.',
        'city': '',
        'text_cs': (
            'I came by Opletalova 30 recently and loved the new decor. The space felt '
            'fresh, quiet, and very upscale. You could relax easily because the '
            'environment looked clean and professionally designed.'
        ),
        'text_en': '',
        'text_ru': '',
    },
    {
        'order': 2,
        'google_review_id': 'google-bd-roland-schulte',
        'rating': 5,
        'author_label': 'Roland S.',
        'city': '',
        'text_cs': (
            'Last time I went to Opletalova 30, the interior really impressed me. The '
            'new decoration gave the place a luxury feel, very clean and modern. It '
            'felt comfortable and premium at the same time.'
        ),
        'text_en': '',
        'text_ru': '',
    },
    {
        'order': 3,
        'google_review_id': 'google-tantra-david-s',
        'rating': 5,
        'author_label': 'David S.',
        'city': '',
        'text_cs': (
            "I've read many reviews about this salon before visiting, and now I "
            'completely understand the praise. From the moment I entered, '
            'everything felt calm, elegant, and sincere. Liana welcomed me with '
            'a soft smile and instantly made me feel relaxed. The room was '
            'beautifully prepared — warm light, quiet music, and the scent of '
            'essential oils filling the air. Her massage was more than just '
            'professional; it felt intuitive, as if she could sense exactly what '
            'I needed. Each touch carried care and warmth. I left lighter, '
            'peaceful, and grateful for such a genuine experience.'
        ),
        'text_en': '',
        'text_ru': '',
    },
    {
        'order': 4,
        'google_review_id': 'google-tantra-finn-g',
        'rating': 5,
        'author_label': 'Finn G.',
        'city': '',
        'text_cs': (
            'She welcomed me with a calm smile and gentle eyes. Liza really knows '
            'how to make you feel comfortable. Her touch was slow, soft, yet '
            'confident. The lighting, music, and scent in the room blended '
            'perfectly. Every movement felt natural and caring, creating a '
            'genuine sense of relaxation and connection.'
        ),
        'text_en': '',
        'text_ru': '',
    },
    {
        'order': 5,
        'google_review_id': 'google-tantra-jano-h',
        'rating': 5,
        'author_label': 'Jano H.',
        'city': '',
        'text_cs': (
            'From the first moment, I noticed how clean the towels were. The '
            'decoration was beautiful in its simplicity—no extra clutter. They '
            'gave me a welcome drink before starting. It was refreshing and set '
            'a calm mood. During my massage, the therapist used just the right '
            'amount of pressure. My shoulders and back felt much better. The '
            'light in the room was dim and warm, making it easy to relax. At '
            'the end, I lay quietly for a moment, then rose feeling calm. I '
            'left feeling happy and refreshed.'
        ),
        'text_en': '',
        'text_ru': '',
    },
]

GOOGLE_MAPS_URL = (
    'https://www.google.com/maps/place/Black+Diamond/'
    '@50.082366,14.4289516,17z/data=!3m1!4b1!4m6!3m5!1s0x470b95f3d3849a1f:0xa55ddc497485ffc6'
    '!8m2!3d50.082366!4d14.4289516'
)


def apply_reviews(apps, schema_editor):
    GuestReview = apps.get_model('core', 'GuestReview')
    SiteSettings = apps.get_model('core', 'SiteSettings')
    synced_ids = []

    for row in BLACK_DIAMOND_REVIEWS:
        GuestReview.objects.update_or_create(
            google_review_id=row['google_review_id'],
            defaults={
                'order': row['order'],
                'author_label': row['author_label'],
                'city': row['city'],
                'text_cs': row['text_cs'],
                'text_en': row['text_en'],
                'text_ru': row['text_ru'],
                'rating': row['rating'],
                'is_active': True,
            },
        )
        synced_ids.append(row['google_review_id'])

    GuestReview.objects.filter(google_review_id__isnull=False).exclude(
        google_review_id__in=synced_ids,
    ).update(is_active=False)

    site = SiteSettings.objects.filter(pk=1).first()
    if site and not (site.google_maps_reviews_url or '').strip():
        SiteSettings.objects.filter(pk=1).update(google_maps_reviews_url=GOOGLE_MAPS_URL)
    if site and not (site.map_url or '').strip():
        SiteSettings.objects.filter(pk=1).update(map_url=GOOGLE_MAPS_URL)


def revert_reviews(apps, schema_editor):
    GuestReview = apps.get_model('core', 'GuestReview')
    ids = [r['google_review_id'] for r in BLACK_DIAMOND_REVIEWS[:3]]
    GuestReview.objects.filter(google_review_id__in=ids).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_google_reviews_fields'),
    ]

    operations = [
        migrations.RunPython(apply_reviews, revert_reviews),
    ]
