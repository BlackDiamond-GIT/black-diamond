"""Rename thajska-masaz → hlubokotkaninni-masaz and add legacy redirects."""

from django.db import migrations

OLD_SLUG = 'thajska-masaz'
NEW_SLUG = 'hlubokotkaninni-masaz'

REDIRECTS = [
    f'/cs/masaze/{OLD_SLUG}/',
    f'/en/masaze/{OLD_SLUG}/',
    f'/ru/masaze/{OLD_SLUG}/',
]


def rename_service(apps, schema_editor):
    Service = apps.get_model('services', 'Service')
    LegacyRedirect = apps.get_model('core', 'LegacyRedirect')
    Service.objects.filter(slug=OLD_SLUG).update(slug=NEW_SLUG)
    for old_path in REDIRECTS:
        lang = old_path.split('/')[1]
        new_path = f'/{lang}/masaze/{NEW_SLUG}/'
        LegacyRedirect.objects.update_or_create(
            old_path=old_path,
            defaults={'new_path': new_path, 'is_active': True},
        )


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0003_service_detail_content'),
        ('core', '0003_currency_defaults_show_usd'),
    ]

    operations = [
        migrations.RunPython(rename_service, migrations.RunPython.noop),
    ]
