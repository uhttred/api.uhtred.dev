# Generated by Django 4.2.4 on 2023-08-13 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_tag_slug_tag_unique_tag_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.SlugField(allow_unicode=True, editable=False, max_length=200, verbose_name='slug'),
        ),
        migrations.AddConstraint(
            model_name='tag',
            constraint=models.UniqueConstraint(fields=('slug',), name='unique_tag_slug'),
        ),
    ]