import os
import io
import base64
import secrets

from typing import Tuple, Union
from PIL import Image

from django.core.files.base import (
    ContentFile,
    File)


SIZE_1_THIN: tuple = 30, 30
SIZE_2_SMALL: tuple = 128, 128
SIZE_2_1_SMALL: tuple = 280, 280
SIZE_3_SMALL: tuple = 540, 540
SIZE_4_MEDIUM: tuple = 768, 768
SIZE_5_LARGE: tuple = 1080, 1080
SIZE_6_LARGE: tuple = 1200, 1200


def get_name_and_extension(filename: str, rename=True) -> Tuple[str, str]:
    """Get Filename and Extension from a file or Generates new"""
    name, ext = os.path.splitext(filename)
    name = (name.split('/')[-1] if not rename
        else secrets.token_hex(20))
    return name, ext


def rename(file: File) -> None:
    """Rename a file from ImageField by creating new one and delete the old one"""
    oldname = file.name
    name, ext = get_name_and_extension(file.name)
    file.save(f'{name}{ext}', file)
    file.storage.delete(oldname)


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
        size: tuple = SIZE_2_1_SMALL,
        rename: bool = False,
        add_thumbnail_sufix: bool = False,
        _format: str = None
    ) -> ContentFile:
    """
    Create a New Resized Image (Thumbnail).
    Uses inmemory with BytesIO
    """
    
    name, ext = get_name_and_extension(file.name,
        rename=rename)
    thumb: Image.Image = Image.open(file)
    thumb_io = io.BytesIO()

    thumb.thumbnail(size)
    thumb = check_image_orientation_and_rotate(thumb)
    thumb.save(thumb_io, format=_format or ext[1:], optimize=True, quality=85)

    filename = (f'{name}.thumbnail{ext}' if add_thumbnail_sufix
        else f'{name}{ext}')

    return ContentFile(thumb_io.getvalue(), name=filename)
