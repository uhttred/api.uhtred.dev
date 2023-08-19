import os
import io
import secrets

from typing import Tuple, Union

from PIL import Image

from django.db.models import ImageField
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.timezone import now
from django.core.files.base import (
    ContentFile,
    File)


def get_name_and_extension(filename: str, rename=True) -> Tuple[str, str]:
    """Get Filename and Extension from a file or Generates new"""
    name, ext = os.path.splitext(filename)
    name = (name.split('/')[-1] if not rename
        else secrets.token_hex(20))
    return name, ext


def image_upload_to(instance, filename):
    name, ext = get_name_and_extension(filename)
    date = now()
    return f"images/{date.year}/{date.month}/{date.day}/{name}{ext}"


def image_thumbnail_upload_to(instance, filename):
    date = now()
    return f"images/{date.year}/{date.month}/{date.day}/{filename}"


def check_image_orientation_and_rotate(image: Image) -> Image:
    
    exif = image._getexif()
    orientation_key = 274
    
    if exif and orientation_key in exif:
        orientation = exif[orientation_key]
        rotate_values = {
            3: Image.ROTATE_180,
            6: Image.ROTATE_270,
            8: Image.ROTATE_90}

        if orientation in rotate_values:
            image = image.transpose(rotate_values[orientation])

    return image


def resize(
        file: File,
        size: tuple = (280, 280),
        rename: bool = False,
        add_thumbnail_sufix: bool = False,
        _format: Union[str,None] = None,
        check_image_orientation: bool = True
    ) -> Union[ContentFile,None]:
    """
    Create a New Resized Image (Thumbnail).
    Uses inmemory with BytesIO
    """
    
    name, ext = get_name_and_extension(file.name,
        rename=rename)
    
    if ext.lower() == '.svg':
        return None

    thumb: Image.Image = Image.open(file)
    thumb_io = io.BytesIO()

    thumb.thumbnail(size)
    if check_image_orientation:
        thumb = check_image_orientation_and_rotate(thumb)
    thumb.save(thumb_io, format=_format or ext[1:], optimize=True, quality=85)

    filename = (f'{name}.thumbnail{ext}' if add_thumbnail_sufix
        else f'{name}{ext}')
    
    return ContentFile(thumb_io.getvalue(), name=filename)
