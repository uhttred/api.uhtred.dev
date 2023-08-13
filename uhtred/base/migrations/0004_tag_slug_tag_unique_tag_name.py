# Generated by Django 4.2.4 on 2023-08-13 15:26

from django.db import migrations, models
import django.db.models.functions.text
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='slug',
            field=models.SlugField(allow_unicode=True, default=django.utils.timezone.now, max_length=200, verbose_name='slug'),
            preserve_default=False,
        ),
        migrations.AddConstraint(
            model_name='tag',
            constraint=models.UniqueConstraint(django.db.models.functions.text.Lower('name'), name='unique_tag_name'),
        ),
    ]