# -*- coding: utf-8 -*-
"""Odebrat slovo „ráno"/„утра" z otevírací doby na existujících řádcích.

Migrace 0008 sjednotila dobu na „Denně od 9:00 do 5:00 ráno"; nové znění je
bez „ráno" (viz defaulty v models.py a opening_hours.py).
"""
from django.db import migrations


def strip_rano(apps, schema_editor):
    SiteSettings = apps.get_model('core', 'SiteSettings')
    for site in SiteSettings.objects.all():
        fields = []
        if site.hours and ' ráno' in site.hours:
            site.hours = site.hours.replace(' ráno', '')
            fields.append('hours')
        if site.hours_ru and ' утра' in site.hours_ru:
            site.hours_ru = site.hours_ru.replace(' утра', '')
            fields.append('hours_ru')
        if fields:
            site.save(update_fields=fields)


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_fix_opening_hours_9_5'),
    ]

    operations = [
        migrations.RunPython(strip_rano, migrations.RunPython.noop),
    ]
