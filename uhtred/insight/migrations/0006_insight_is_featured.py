# Generated by Django 4.2.6 on 2023-10-16 01:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insight', '0005_author_serie_serieitem_topic_remove_insight_tags_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='insight',
            name='is_featured',
            field=models.BooleanField(default=False, verbose_name='is featured'),
        ),
    ]