# Generated by Django 4.2.6 on 2023-10-16 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insight', '0006_insight_is_featured'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serie',
            name='status',
            field=models.TextField(choices=[('in_launch', 'in launch'), ('completed', 'completed')], default='in_launch', max_length=9, verbose_name='status'),
        ),
    ]