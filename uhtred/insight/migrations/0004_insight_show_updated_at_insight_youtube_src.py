# Generated by Django 4.2.4 on 2023-09-10 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insight', '0003_alter_insight_cover_alter_insight_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='insight',
            name='show_updated_at',
            field=models.BooleanField(default=False, verbose_name='show updated at'),
        ),
        migrations.AddField(
            model_name='insight',
            name='youtube_src',
            field=models.URLField(blank=True, default=None, null=True, verbose_name='youtube src'),
        ),
    ]
