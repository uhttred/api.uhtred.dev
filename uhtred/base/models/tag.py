from django.db import models
from django.db.models.functions import Lower
from django.utils.translation import gettext_lazy as _
from django.db.models.constraints import UniqueConstraint
from django.utils.text import slugify

from uhtred.core.models.abstract import BaseFieldsAbstractModel


class Tag(BaseFieldsAbstractModel):
    
    class Meta:
        verbose_name = _('tag')
        verbose_name_plural = _('tags')
        constraints = (
            UniqueConstraint(
                Lower('name'),
                name='unique_tag_name'),
            UniqueConstraint(
                fields=['slug'],
                name='unique_tag_slug')
        )
    
    name = models.CharField(
        verbose_name=_('name'),
        max_length=60)
    
    slug = models.SlugField(
        verbose_name='slug',
        max_length=200,
        editable=False,
        allow_unicode=True)

    pt_name = models.CharField(
        verbose_name=_('name (PT)'),
        max_length=60,
        blank=True,
        default='')
    
    description = models.CharField(
        verbose_name=_('description'),
        max_length=250,
        blank=True,
        default='')

    def __str__(self) -> str:
        return self.name
    
    def __slugify(self):
        self.slug = slugify(
            self.name,
            allow_unicode=False)
    
    def save(self, *args, **kwargs) -> None:
        """"""
        if not self.slug:
            self.__slugify()
        super(Tag, self).save(*args, **kwargs)
