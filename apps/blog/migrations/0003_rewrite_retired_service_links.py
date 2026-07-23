from django.db import migrations


RETIRED_SERVICE_SLUGS = (
    'aromaterapie',
    'cbd-relaxacni-masaz',
    'klasicka-masaz',
    'lymfaticka-masaz',
)


def rewrite_retired_service_links(apps, schema_editor):
    Article = apps.get_model('blog', 'Article')

    for article in Article.objects.all().iterator():
        changed_fields = []
        for field in ('body_cs', 'body_en', 'body_ru'):
            original = getattr(article, field, '') or ''
            rewritten = original
            for retired_slug in RETIRED_SERVICE_SLUGS:
                rewritten = rewritten.replace(
                    f'/masaze/{retired_slug}/',
                    '/masaze/relaxacni-masaz/',
                )
            if rewritten != original:
                setattr(article, field, rewritten)
                changed_fields.append(field)
        if changed_fields:
            article.save(update_fields=changed_fields)


class Migration(migrations.Migration):
    dependencies = [
        ('blog', '0002_update_contact_details_in_articles'),
    ]

    operations = [
        migrations.RunPython(
            rewrite_retired_service_links,
            migrations.RunPython.noop,
        ),
    ]
