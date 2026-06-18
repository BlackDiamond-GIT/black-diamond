"""Update schedule work address to Opletalova 1566/30, Nové Město."""

from django.db import migrations

NEW_ADDRESS = 'Opletalova 1566/30, 110 00 Nové Město'
OLD_ADDRESSES = (
    'Soukenická, 110 00 Praha 1',
    'Opletalova 1566/30, 110 00 Praha 1',
)


def update_work_address(apps, schema_editor):
    ScheduleEntry = apps.get_model('schedule', 'ScheduleEntry')
    ScheduleEntry.objects.filter(location_address__in=OLD_ADDRESSES).update(
        location_address=NEW_ADDRESS,
    )


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0003_schedule_single_work_address'),
    ]

    operations = [
        migrations.RunPython(update_work_address, migrations.RunPython.noop),
    ]
