# Generated by Django 4.2.4 on 2023-08-13 15:18

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_alter_image_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='unique id')),
                ('name', models.CharField(max_length=60, verbose_name='name')),
                ('pt_name', models.CharField(blank=True, default='', max_length=60, verbose_name='name (PT)')),
                ('description', models.CharField(blank=True, default='', max_length=250, verbose_name='description')),
            ],
            options={
                'verbose_name': 'tag',
                'verbose_name_plural': 'tags',
            },
        ),
    ]