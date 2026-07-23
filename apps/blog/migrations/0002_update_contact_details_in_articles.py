"""Update persisted contact details in imported article content."""

from django.db import migrations


REPLACEMENTS = (
    ('+420 797 669 633', '+420 778 622 334'),
    ('tel:+420797669633', 'tel:+420778622334'),
    ('wa.me/420797669633', 'wa.me/420778622334'),
    ('Opletalova 1566/30, 110 00 Nové Město', 'Opletalova 1566/30, 110 00 Praha'),
    ('Opletalova 1566/30, Nové Město', 'Opletalova 1566/30, Praha'),
)
FIELDS = (
    'body_cs', 'body_en', 'body_ru',
    'meta_description_cs', 'meta_description_en', 'meta_description_ru',
)


def update_article_contacts(apps, schema_editor):
    Article = apps.get_model('blog', 'Article')
    for article in Article.objects.all().iterator():
        changed = []
        for field in FIELDS:
            value = getattr(article, field, '') or ''
            updated = value
            for old, new in REPLACEMENTS:
                updated = updated.replace(old, new)
            if updated != value:
                setattr(article, field, updated)
                changed.append(field)
        if changed:
            article.save(update_fields=changed)


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(update_article_contacts, migrations.RunPython.noop),
    ]
