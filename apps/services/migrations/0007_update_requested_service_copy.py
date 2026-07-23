"""Update the two client-requested service summaries in the production database."""

from django.db import migrations


COPY = {
    'vip-masaz': {
        'short_cs': 'Exkluzivní a individuální celotělová péče s plnou pozorností certifikovaného terapeuta za využití prémiových bio olejů.',
        'short_en': 'Exclusive and individual full-body care with the undivided attention of a certified therapist, using premium organic oils.',
        'short_ru': 'Эксклюзивный индивидуальный уход за всем телом с полным вниманием сертифицированного терапевта и использованием премиальных био-масел.',
    },
    'masaz-pro-zeny': {
        'short_cs': 'Zklidňující regenerační rituál v harmonickém a plně soukromém prostředí, zaměřený na odbourání stresu a hluboké uvolnění svalů.',
        'short_en': 'A soothing regenerative ritual in a harmonious and fully private setting, focused on relieving stress and deeply relaxing the muscles.',
        'short_ru': 'Успокаивающий восстанавливающий ритуал в гармоничной и полностью приватной обстановке, направленный на снятие стресса и глубокое расслабление мышц.',
    },
}


def update_service_copy(apps, schema_editor):
    Service = apps.get_model('services', 'Service')
    for slug, values in COPY.items():
        Service.objects.filter(slug=slug).update(**values)


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0006_deactivate_old_services'),
    ]

    operations = [
        migrations.RunPython(update_service_copy, migrations.RunPython.noop),
    ]
