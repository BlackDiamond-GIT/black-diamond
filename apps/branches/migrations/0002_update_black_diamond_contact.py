"""Keep existing branch records aligned with the Black Diamond contact details."""

from django.db import migrations


def update_branch_contact(apps, schema_editor):
    Branch = apps.get_model('branches', 'Branch')
    Branch.objects.filter(name='Black Diamond').update(
        address='Opletalova 1566/30, 110 00 Praha',
        phone='+420 778 622 334',
    )


class Migration(migrations.Migration):

    dependencies = [
        ('branches', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(update_branch_contact, migrations.RunPython.noop),
    ]
