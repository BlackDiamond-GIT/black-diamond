"""Data migration — unify schedule entries to Soukenická."""

from django.db import migrations

WORK_ADDRESS = 'Soukenická, 110 00 Praha 1'


def set_single_work_address(apps, schema_editor):
    ScheduleEntry = apps.get_model('schedule', 'ScheduleEntry')
    ScheduleEntry.objects.all().update(
        location_address=WORK_ADDRESS,
        branch_id=None,
    )


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0002_scheduleentry'),
    ]

    operations = [
        migrations.RunPython(set_single_work_address, migrations.RunPython.noop),
    ]
