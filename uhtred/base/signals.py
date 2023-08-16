from django.dispatch import receiver
from django.db.models.signals import post_save

from uhtred.base.models import Image
from uhtred.base.tasks import task_create_image_thumbnail

@receiver(post_save, sender=Image)
def on_image_created(instance: Image, created, **kwargs) -> None:
    if created:
        task_create_image_thumbnail(
            image_id=instance.id)