# Generated by Django 4.2.4 on 2023-08-21 14:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='person',
            field=models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user', to='base.person'),
        ),
    ]
