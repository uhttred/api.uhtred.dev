# Generated by Django 4.2.6 on 2023-10-15 15:23

from django.db import migrations, models
import django.db.models.functions.text
import uhtred.core.validators
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('insight', '0005_author_serie_serieitem_topic_remove_insight_tags_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='unique id')),
                ('name', models.CharField(blank=True, default=str, max_length=45, validators=[uhtred.core.validators.NameValidator(), uhtred.core.validators.NoPoitSequenceValidator()], verbose_name='name')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email')),
                ('verified', models.BooleanField(default=False, verbose_name='verifeid')),
                ('subscribe_to_all', models.BooleanField(default=False, verbose_name='subscribe to all topics')),
                ('subscribed_topics', models.ManyToManyField(blank=True, related_name='subscribed_emails', to='insight.topic')),
            ],
            options={
                'verbose_name': 'email list',
                'verbose_name_plural': 'email list',
            },
        ),
        migrations.AddConstraint(
            model_name='email',
            constraint=models.UniqueConstraint(django.db.models.functions.text.Lower('email'), name='unique_email_email'),
        ),
    ]