from typing import Any
from django.db import models
from django.db.models.constraints import UniqueConstraint
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

from martor.models import MartorField

from uhtred.core.models.abstract import BaseFieldsAbstractModel
from uhtred.core.text import get_random_string_code


def case_images_upload_to(instance, filename):
    return f"cases/{instance.article.uid}/{filename}"


class CaseManager(models.Manager):
    
    def default_list(self, *args: Any, **kwargs: Any):
        return super().filter(
            is_active=True).filter(*args, **kwargs)

    def search(self, lookup: str):
        return self.filter(
            models.Q(title__icontains=lookup) |
            models.Q(pt_title__icontains=lookup)
        ).distinct()


class Case(BaseFieldsAbstractModel):
    
    class Meta:
        verbose_name = _('case')
        verbose_name_plural = _('cases')
        constraints = (
            UniqueConstraint(
                fields=['title'],
                name='unique_case_title'),
            UniqueConstraint(
                fields=['slug'],
                name='unique_case_slug')
        )
    
    slug = models.SlugField(
        verbose_name='slug',
        max_length=250,
        allow_unicode=True)
    
    title = models.CharField(
        verbose_name=_('title'),
        max_length=200)
    pt_title = models.CharField(
        verbose_name=_('pt title'),
        max_length=200)
    
    description = models.CharField(
        verbose_name=_('description'),
        max_length=240,
        blank=True,
        default=str)
    pt_description = models.CharField(
        verbose_name=_('pt description'),
        max_length=240,
        blank=True,
        default=str)
    
    content = MartorField(
        verbose_name=_('content'),
        blank=True,
        default=str)
    pt_content = MartorField(
        verbose_name=_('content'),
        blank=True,
        default=str)
    
    cover = models.ForeignKey(
        'base.Image',
        verbose_name=_('cover'),
        related_name='case_cover',
        on_delete=models.SET_NULL,
        null=True)
    
    banner = models.ForeignKey(
        'base.Image',
        verbose_name=_('banner'),
        related_name='case_banner',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None)
    banner_dark = models.ForeignKey(
        'base.Image',
        verbose_name=_('banner dark'),
        related_name='case_banner_dark',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None)
    
    brand_logo = models.ForeignKey(
        'base.Image',
        verbose_name=_('brand logo'),
        related_name='case_brand_logo',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None)
    brand_logo_dark = models.ForeignKey(
        'base.Image',
        verbose_name=_('brand logo dark'),
        related_name='case_brand_logo_dark',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None)
    
    data = models.JSONField(
        verbose_name=_('additional data'),
        blank=True,
        default=dict)

    is_active = models.BooleanField(
        verbose_name=_('is active'),
        default=False)
    
    objects = CaseManager()

    def __slugify(self):
        self.slug = slugify(
            f'{self.title} {get_random_string_code(4)}',
            allow_unicode=False)
    
    def save(self, *args, **kwargs) -> None:
        """"""
        if not self.slug:
            self.__slugify()
        super(Case, self).save(*args, **kwargs)
