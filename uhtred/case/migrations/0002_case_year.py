# Generated by Django 4.2.4 on 2023-08-21 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('case', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='case',
            name='year',
            field=models.PositiveIntegerField(default=0, verbose_name='year'),
        ),
    ]