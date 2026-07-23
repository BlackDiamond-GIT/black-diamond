"""Replace the former locality in existing therapist content and FAQ JSON."""

from django.db import migrations


REPLACEMENTS = (
    ('Opletalova 1566/30, 110 00 Nové Město', 'Opletalova 1566/30, 110 00 Praha'),
    ('Opletalova 1566/30, Nové Město', 'Opletalova 1566/30, Praha'),
)
TEXT_FIELDS = (
    'bio_cs', 'bio_en', 'bio_ru',
    'meta_description',
    'meta_description_cs', 'meta_description_en', 'meta_description_ru',
)
FAQ_FIELDS = ('faq_cs', 'faq_en', 'faq_ru')


def replace_text(value):
    for old, new in REPLACEMENTS:
        value = value.replace(old, new)
    return value


def update_therapist_addresses(apps, schema_editor):
    Therapist = apps.get_model('therapists', 'Therapist')
    for therapist in Therapist.objects.all().iterator():
        changed = []
        for field in TEXT_FIELDS:
            value = getattr(therapist, field, '') or ''
            updated = replace_text(value)
            if updated != value:
                setattr(therapist, field, updated)
                changed.append(field)
        for field in FAQ_FIELDS:
            items = getattr(therapist, field, None) or []
            updated = [
                {
                    **item,
                    'a': replace_text(item.get('a', '')),
                }
                for item in items
            ]
            if updated != items:
                setattr(therapist, field, updated)
                changed.append(field)
        if changed:
            therapist.save(update_fields=changed)


class Migration(migrations.Migration):

    dependencies = [
        ('therapists', '0004_therapist_hub_slug'),
    ]

    operations = [
        migrations.RunPython(update_therapist_addresses, migrations.RunPython.noop),
    ]
