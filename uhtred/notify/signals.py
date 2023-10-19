from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import Email
from .tasks import send_newsletter_confirmation_email


@receiver(post_save, sender=Email)
def on_newsletter_subscription(sender, instance: Email, created: bool, **kwargs):
    if created and not instance.verified:
        send_newsletter_confirmation_email(
            email=instance)
