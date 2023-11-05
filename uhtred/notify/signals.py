from django.dispatch import receiver
from django.db.models.signals import post_save

from uhtred.insight.signals import insight_published
from uhtred.insight.models import Insight

from .models import Email
from .tasks import (
    send_newsletter_article_published,
    send_newsletter_confirmation_email)


@receiver(post_save, sender=Email)
def on_newsletter_subscription(sender, instance: Email, created: bool, **kwargs):
    if created and not instance.verified:
        send_newsletter_confirmation_email(
            email=instance)


@receiver(insight_published)
def on_insight_published(sender, insight: Insight, **kwargs):
    if insight.notify_newsletter:
        send_newsletter_article_published(insight)
