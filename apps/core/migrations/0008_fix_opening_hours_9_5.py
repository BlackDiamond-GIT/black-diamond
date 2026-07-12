"""Srovnat zastaralou provozní dobu na singletonu SiteSettings (9:00–5:00 ráno).

Migrace 0003 změnila jen DEFAULT pole `hours`, ale existující řádek v produkční
DB si držel starou hodnotu ("Od 11 ráno do 4 ráno"), která se zobrazovala na
Kontaktu. Tahle data-migrace ji při deployi přepíše na jednotné 9:00–5:00.
"""

from django.db import migrations

NEW_CS = 'Denně od 9:00 do 5:00 ráno'
NEW_EN = 'Daily from 9 AM to 5 AM'
NEW_RU = 'Ежедневно с 9:00 до 5:00 утра'


def fix_hours(apps, schema_editor):
    SiteSettings = apps.get_model('core', 'SiteSettings')
    for site in SiteSettings.objects.all():
        changed = []
        cs = site.hours or ''
        # staré varianty: "Od 11 ráno do 4 ráno", "Od 9 ráno do 4 ráno", prázdné
        if not cs.strip() or 'do 4' in cs or '11' in cs:
            site.hours = NEW_CS
            changed.append('hours')
        en = site.hours_en or ''
        if not en.strip() or 'to 4' in en or '4 AM' in en:
            site.hours_en = NEW_EN
            changed.append('hours_en')
        ru = site.hours_ru or ''
        if not ru.strip() or 'до 4' in ru:
            site.hours_ru = NEW_RU
            changed.append('hours_ru')
        if changed:
            site.save(update_fields=changed)


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_guest_review_ru_translations'),
    ]

    operations = [
        migrations.RunPython(fix_hours, migrations.RunPython.noop),
    ]
