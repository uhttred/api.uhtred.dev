from typing import Tuple, Dict

from django.db import models
from django.utils.html import mark_safe
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _

from uhtred.core.models.abstract import BaseFieldsAbstractModel
from uhtred.core.images import (
    image_thumbnail_upload_to,
    image_upload_to)


class Image(BaseFieldsAbstractModel):
    
    class Meta:
        verbose_name = _('image')
        verbose_name_plural = _('images')
    
    name = models.CharField(
        verbose_name=_('name'),
        help_text=_('describe what image is for'),
        max_length=250,
        blank=True,
        default='')

    file = models.ImageField(
        upload_to=image_upload_to,
        validators=[
            FileExtensionValidator(['svg', 'png', 'gif', 'jpg', 'jpeg'])])

    thumbnail = models.ImageField(
        verbose_name=_('image thumbnail'),
        upload_to=image_thumbnail_upload_to,
        null=True,
        default=None,
        editable=False)
    
    def __str__(self) -> str:
        return self.name or f'image ({self.id})'
    
    @property
    def url(self):
        return None if not self.file else self.file.url
    
    @property
    def thumbnail_url(self):
        return None if not self.thumbnail else self.thumbnail.url

    def delete(self, **kwargs) -> Tuple[int, Dict[str, int]]:
        """delete the instance and related files"""
        for file in (self.file, self.thumbnail):
            if file.name:
                try:
                    file.storage.delete(file.file.name)
                    file.delete()
                except: continue
        return super().delete(**kwargs)
    
    def admin_thumbnail_preview(self, max_width: int = 300):
        if self.thumbnail_url:
            return mark_safe(f'<img src="{self.thumbnail_url}" style="max-width:{max_width}px;"/>')
        return '-'
    
    def admin_image_preview(self, max_width: int = 300):
        if self.url:
            return mark_safe(f'<img src="{self.url}" style="max-width:{max_width}px;"/>')
        return '-'
        