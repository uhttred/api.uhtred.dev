from django.dispatch import receiver
from django.db.models.signals import post_save

from uhtred.base.models import Image
from uhtred.base.tasks import task_rename_image_and_create_thumbnail

@receiver(post_save, sender=Image)
def on_image_created(instance: Image, created, **kwargs) -> None:
    print(kwargs)
    if created:
        task_rename_image_and_create_thumbnail(
            image_id=instance.id)