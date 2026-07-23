"""Set the verified Prague relax operator details and Black Diamond contacts."""

from django.db import migrations, models


PHONE = '+420 778 622 334'
WHATSAPP = '420778622334'
ADDRESS = 'Opletalova 1566/30, 110 00 Praha'
META_TITLE = 'Black Diamond Spa | Luxusní relaxační masáže Praha'
META_DESCRIPTION = (
    'Prémiový masážní salon v centru Prahy na adrese Opletalova 30. '
    'Nabízíme exkluzivní relaxační rituály a masáže pro páry v luxusním '
    'privátním prostředí.'
)


def update_company_contact_details(apps, schema_editor):
    SiteSettings = apps.get_model('core', 'SiteSettings')
    site, _ = SiteSettings.objects.get_or_create(pk=1)
    site.phone_primary = PHONE
    site.whatsapp_number = WHATSAPP
    site.rotation_phone_1 = PHONE
    site.rotation_phone_2 = PHONE
    site.rotation_phone_3 = PHONE
    site.address = ADDRESS
    site.location_phone_1 = PHONE
    site.default_meta_title = META_TITLE
    site.default_meta_description = META_DESCRIPTION
    site.save(update_fields=[
        'phone_primary',
        'whatsapp_number',
        'rotation_phone_1',
        'rotation_phone_2',
        'rotation_phone_3',
        'address',
        'location_phone_1',
        'default_meta_title',
        'default_meta_description',
    ])


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_whatsapp_number_797'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitesettings',
            name='address',
            field=models.CharField(default=ADDRESS, max_length=200, verbose_name='Address (studio 1)'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='location_phone_1',
            field=models.CharField(default=PHONE, max_length=30, verbose_name='Phone (studio 1)'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='phone_primary',
            field=models.CharField(default=PHONE, max_length=30, verbose_name='Primary phone'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='rotation_phone_1',
            field=models.CharField(default=PHONE, max_length=30, verbose_name='Rotating phone 1'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='rotation_phone_2',
            field=models.CharField(default=PHONE, max_length=30, verbose_name='Rotating phone 2'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='rotation_phone_3',
            field=models.CharField(default=PHONE, max_length=30, verbose_name='Rotating phone 3'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='whatsapp_number',
            field=models.CharField(
                default=WHATSAPP,
                help_text='e.g. 420778622334 — used in wa.me/ links',
                max_length=20,
                verbose_name='WhatsApp number (no +, no spaces)',
            ),
        ),
        migrations.RunPython(update_company_contact_details, migrations.RunPython.noop),
    ]
