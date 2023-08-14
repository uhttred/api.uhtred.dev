# Generated by Django 4.2.4 on 2023-08-14 13:27

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.functions.text
import martor.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base', '0006_person'),
    ]

    operations = [
        migrations.CreateModel(
            name='Insight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='unique id')),
                ('slug', models.SlugField(allow_unicode=True, max_length=250, verbose_name='slug')),
                ('title', models.CharField(max_length=230, verbose_name='title')),
                ('description', models.TextField(verbose_name='description')),
                ('pt_title', models.CharField(blank=True, default=str, max_length=230, verbose_name='title (PT)')),
                ('pt_description', models.TextField(blank=True, default=str, verbose_name='description (PT)')),
                ('content', martor.models.MartorField(verbose_name='content')),
                ('pt_content', martor.models.MartorField(blank=True, default=str, verbose_name='content (PT)')),
                ('visualisations', models.PositiveIntegerField(default=0, verbose_name='visualisations')),
                ('is_active', models.BooleanField(default=False, verbose_name='is active')),
                ('published_at', models.DateTimeField(default=None, null=True, verbose_name='published at')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='insights', to='base.person')),
                ('cover', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='insight_cover', to='base.image', verbose_name='cover')),
                ('tags', models.ManyToManyField(related_name='insights', to='base.tag')),
            ],
            options={
                'verbose_name': 'insight',
                'verbose_name_plural': 'insights',
            },
        ),
        migrations.AddConstraint(
            model_name='insight',
            constraint=models.UniqueConstraint(django.db.models.functions.text.Lower('title'), name='unique_insight_title'),
        ),
        migrations.AddConstraint(
            model_name='insight',
            constraint=models.UniqueConstraint(fields=('slug',), name='unique_insight_slug'),
        ),
    ]
