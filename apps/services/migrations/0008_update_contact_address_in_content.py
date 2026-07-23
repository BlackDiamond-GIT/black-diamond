"""Replace the former locality in existing service content and FAQ JSON."""

from django.db import migrations


REPLACEMENTS = (
    ('Opletalova 1566/30, 110 00 Nové Město', 'Opletalova 1566/30, 110 00 Praha'),
    ('Opletalova 1566/30, Nové Město', 'Opletalova 1566/30, Praha'),
)
TEXT_FIELDS = (
    'description_cs', 'description_en', 'description_ru',
    'what_cs', 'what_en', 'what_ru',
    'who_cs', 'who_en', 'who_ru',
    'meta_description_cs', 'meta_description_en', 'meta_description_ru',
)
FAQ_FIELDS = ('faq_cs', 'faq_en', 'faq_ru')


def replace_text(value):
    for old, new in REPLACEMENTS:
        value = value.replace(old, new)
    value = value.replace('110 00 Praha, Praha.', '110 00 Praha.')
    value = value.replace('110 00 Praha, Prague.', '110 00 Praha.')
    value = value.replace('110 00 Praha, Прага.', '110 00 Praha.')
    return value


def update_service_addresses(apps, schema_editor):
    Service = apps.get_model('services', 'Service')
    for service in Service.objects.all().iterator():
        changed = []
        for field in TEXT_FIELDS:
            value = getattr(service, field, '') or ''
            updated = replace_text(value)
            if updated != value:
                setattr(service, field, updated)
                changed.append(field)
        for field in FAQ_FIELDS:
            items = getattr(service, field, None) or []
            updated = [
                {
                    **item,
                    'a': replace_text(item.get('a', '')),
                }
                for item in items
            ]
            if updated != items:
                setattr(service, field, updated)
                changed.append(field)
        if changed:
            service.save(update_fields=changed)


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0007_update_requested_service_copy'),
    ]

    operations = [
        migrations.RunPython(update_service_addresses, migrations.RunPython.noop),
    ]
