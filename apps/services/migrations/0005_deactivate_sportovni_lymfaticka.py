"""Deactivate sportovni-masaz and lymfaticka-masaz services."""

from django.db import migrations

SLUGS = ['sportovni-masaz', 'lymfaticka-masaz']


def deactivate_services(apps, schema_editor):
    Service = apps.get_model('services', 'Service')
    Service.objects.filter(slug__in=SLUGS).update(is_active=False)


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0004_rename_thajska_to_hlubokotkaninni'),
    ]

    operations = [
        migrations.RunPython(deactivate_services, migrations.RunPython.noop),
    ]
