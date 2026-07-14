# -*- coding: utf-8 -*-
"""Sjednotit všechna telefonní/WhatsApp čísla na +420 797 669 633 + odkaz na mapu.

Rotace telefonů (rotation_phone_1/2/3) napájela WhatsApp přes get_active_whatsapp_number,
takže wa.me odkazy cyklovaly přes 797/777/778. Nastavíme všechny na jediné číslo.
Model default byl změněn, ale existující produkční řádek si držel stará čísla.
"""
from django.db import migrations

PHONE = '+420 797 669 633'
WA = '420797669633'
MAPS_URL = (
    'https://www.google.com/maps/place/Black+Diamond+-+massage+saloon+%26+private+tantric+club/'
    '@50.082366,14.4315265,17z/data=!3m1!4b1!4m6!3m5!1s0x470b95f3d3849a1f:0xa55ddc497485ffc6'
    '!8m2!3d50.082366!4d14.4315265!16s%2Fg%2F11v6y56n1w?hl=cs&entry=ttu'
    '&g_ep=EgoyMDI2MDcxMi4wIKXMDSoASAFQAw%3D%3D'
)


def set_numbers(apps, schema_editor):
    SiteSettings = apps.get_model('core', 'SiteSettings')
    SiteSettings.objects.all().update(
        phone_primary=PHONE,
        rotation_phone_1=PHONE,
        rotation_phone_2=PHONE,
        rotation_phone_3=PHONE,
        location_phone_1=PHONE,
        whatsapp_number=WA,
        map_url=MAPS_URL,
    )


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_hours_remove_rano'),
    ]

    operations = [
        migrations.RunPython(set_numbers, migrations.RunPython.noop),
    ]
