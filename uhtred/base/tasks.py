from uhtred.base.models import Image

from uhtred.core.images import (
    resize)


def task_create_image_thumbnail(image: Image) -> None:
    """Read function name hahah"""
    thumb = resize(
        file=image.file,
        rename=False,
        check_image_orientation=False,
        add_thumbnail_sufix=True)
    if thumb:
        image.thumbnail = thumb
        image.save()
