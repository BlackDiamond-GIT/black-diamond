from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_update_site_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='guestreview',
            name='published_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Published at'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='google_rating',
            field=models.DecimalField(
                blank=True, decimal_places=1, max_digits=2, null=True,
                verbose_name='Google rating',
            ),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='google_review_count',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Google review count'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='google_maps_reviews_url',
            field=models.URLField(blank=True, max_length=500, verbose_name='Google Maps reviews URL'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='google_reviews_synced_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Google reviews synced at'),
        ),
        migrations.AlterModelOptions(
            name='guestreview',
            options={
                'ordering': ['order', '-published_at', 'pk'],
                'verbose_name': 'Guest review',
                'verbose_name_plural': 'Guest reviews',
            },
        ),
    ]
