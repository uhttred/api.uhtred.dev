from typing import Tuple, Dict

from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _

from uhtred.core.models.abstract import BaseFieldsAbstractModel


def images_upload_to(instance, filename):
    return f"images/{instance.uid}/{filename}"


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
        upload_to=images_upload_to,
        validators=[
            FileExtensionValidator(['svg', 'png', 'gif', 'jpg', 'jpeg'])])

    thumbnail = models.ImageField(
        verbose_name=_('image thumbnail'),
        upload_to=images_upload_to,
        null=True,
        default=None,
        editable=False)
    
    def __str__(self) -> str:
        return self.name or f'image ({self.id})'
    
    @property
    def url(self):
        return None if not self.file else f'http://localhost:8000{self.file.url}'
    
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
        