from uhtred.base.models import Image

from uhtred.core.images import (
    resize,
    rename,)


def task_rename_image_and_create_thumbnail(image_id: str) -> None:
    """Read function name hahah"""
    image: Image = Image.objects.get(id=image_id)
    rename(image.file)
    image.thumbnail = resize(
        file=image.file,
        rename=False,
        add_thumbnail_sufix=True)
    image.save()
