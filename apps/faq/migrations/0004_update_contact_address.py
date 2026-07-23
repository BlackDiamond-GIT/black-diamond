"""Update persisted FAQ location text to the requested postal address."""

from django.db import migrations


OLD = 'Opletalova 1566/30, 110 00 Nové Město'
NEW = 'Opletalova 1566/30, 110 00 Praha'


def update_faq_addresses(apps, schema_editor):
    FAQ = apps.get_model('faq', 'FAQ')
    for faq in FAQ.objects.all().iterator():
        changed = []
        for field in ('answer_cs', 'answer_en', 'answer_ru'):
            value = getattr(faq, field, '') or ''
            updated = value.replace(OLD, NEW)
            if updated != value:
                setattr(faq, field, updated)
                changed.append(field)
        if changed:
            faq.save(update_fields=changed)


class Migration(migrations.Migration):

    dependencies = [
        ('faq', '0003_update_faq_answers'),
    ]

    operations = [
        migrations.RunPython(update_faq_addresses, migrations.RunPython.noop),
    ]
