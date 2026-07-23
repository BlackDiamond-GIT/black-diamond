"""Update persisted schedule locations to the requested postal address."""

from django.db import migrations


def update_work_address(apps, schema_editor):
    ScheduleEntry = apps.get_model('schedule', 'ScheduleEntry')
    ScheduleEntry.objects.update(location_address='Opletalova 1566/30, 110 00 Praha')


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0004_update_work_address'),
    ]

    operations = [
        migrations.RunPython(update_work_address, migrations.RunPython.noop),
    ]
