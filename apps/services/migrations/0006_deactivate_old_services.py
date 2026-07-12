"""Deactivate services replaced by the 4-service offering (VIP, Relaxační, pro ženy, pro páry)."""

from django.db import migrations

SLUGS = ['klasicka-masaz', 'cbd-relaxacni-masaz', 'hlubokotkaninni-masaz', 'aromaterapie']


def deactivate_services(apps, schema_editor):
    Service = apps.get_model('services', 'Service')
    Service.objects.filter(slug__in=SLUGS).update(is_active=False)


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0005_deactivate_sportovni_lymfaticka'),
    ]

    operations = [
        migrations.RunPython(deactivate_services, migrations.RunPython.noop),
    ]
