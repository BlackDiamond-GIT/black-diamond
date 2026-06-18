"""Update site address to Opletalova 1566/30, Nové Město."""

from django.db import migrations

NEW_ADDRESS = 'Opletalova 1566/30, 110 00 Nové Město'
OLD_ADDRESSES = (
    'Soukenická, 110 00 Praha 1',
    'Opletalova 1566/30, 110 00 Praha 1',
)


def update_site_address(apps, schema_editor):
    SiteSettings = apps.get_model('core', 'SiteSettings')
    SiteSettings.objects.filter(address__in=OLD_ADDRESSES).update(address=NEW_ADDRESS)


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_currency_defaults_show_usd'),
    ]

    operations = [
        migrations.RunPython(update_site_address, migrations.RunPython.noop),
    ]
