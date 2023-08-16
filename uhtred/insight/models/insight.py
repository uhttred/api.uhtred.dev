from typing import Any

from django.db import models
from django.db.models.functions import Lower
from django.db.models.constraints import UniqueConstraint
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

from martor.models import MartorField

from uhtred.core.models.abstract import BaseFieldsAbstractModel


class InsightManager(models.Manager):
    
    def default_list(self, *args: Any, **kwargs: Any):
        return super().filter(
            is_active=True).filter(*args, **kwargs)
    
    def search(self, lookup: str):
        return self.default_list(
            models.Q(title__icontains=lookup) |
            models.Q(pt_title__icontains=lookup)
        ).distinct()
    

class Insight(BaseFieldsAbstractModel):
    
    class Meta:
        verbose_name = _('insight')
        verbose_name_plural = _('insights')
        constraints = (
            UniqueConstraint(
                Lower('title'),
                name='unique_insight_title'),
            UniqueConstraint(
                fields=['slug'],
                name='unique_insight_slug')
        )
    
    slug = models.SlugField(
        'slug',
        max_length=250,
        allow_unicode=True)
    
    author = models.ForeignKey(
        'base.Person',
        related_name='insights',
        on_delete=models.SET_NULL,
        null=True)

    cover = models.ForeignKey(
        'base.Image',
        verbose_name=_('cover'),
        related_name='insight_cover',
        on_delete=models.SET_NULL,
        null=True)
    
    title = models.CharField(
        verbose_name=_('title'),
        max_length=230)

    description = models.TextField(
        verbose_name=_('description'))
    
    pt_title = models.CharField(
        verbose_name=_('title (PT)'),
        max_length=230,
        blank=True,
        default=str)
    
    pt_description = models.TextField(
        verbose_name=_('description (PT)'),
        blank=True,
        default=str)
    
    content = MartorField(
        verbose_name=_('content'))
    
    pt_content = MartorField(
        verbose_name=_('content (PT)'),
        blank=True,
        default=str)
    
    tags = models.ManyToManyField(
        'base.Tag',
        related_name='insights')
    
    visualisations = models.PositiveIntegerField(
        verbose_name=_('visualisations'),
        default=0)
    
    is_active = models.BooleanField(
        verbose_name=_('is active'),
        default=False)
    
    published_at = models.DateTimeField(
        verbose_name=_('published at'),
        null=True,
        default=None)
    
    objects = InsightManager()

    def __str__(self) -> str:
        return self.title

    def __slugify(self):
        self.slug = slugify(
            self.title,
            allow_unicode=False)
    
    def save(self, *args, **kwargs) -> None:
        """"""
        if not self.slug:
            self.__slugify()
        super(Insight, self).save(*args, **kwargs)