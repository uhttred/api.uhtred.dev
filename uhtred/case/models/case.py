from django.db import models
from django.db.models.constraints import UniqueConstraint
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

from martor.models import MartorField

from uhtred.core.models.abstract import BaseFieldsAbstractModel
from uhtred.core.text import get_random_string_code


def case_images_upload_to(instance, filename):
    return f"cases/{instance.article.uid}/{filename}"


class Case(BaseFieldsAbstractModel):
    
    class Meta:
        verbose_name = _('case')
        verbose_name_plural = _('cases')
    
    slug = models.SlugField(
        verbose_name='slug',
        max_length=250,
        allow_unicode=False)
    
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
        verbose_name=_('content'))
    pt_content = MartorField(
        verbose_name=_('pt content'))
    
    cover = models.ForeignKey(
        'base.Image',
        verbose_name=_('cover'),
        related_name='case_cover',
        on_delete=models.CASCADE)
    banner_light = models.ForeignKey(
        'base.Image',
        verbose_name=_('banner light'),
        related_name='case_banner_light',
        on_delete=models.CASCADE)
    banner_dark = models.ForeignKey(
        'base.Image',
        verbose_name=_('banner dark'),
        related_name='case_banner_dark',
        on_delete=models.CASCADE)

    def __slugify(self):
        self.slug = slugify(
            f'{self.title} {get_random_string_code(4)}',
            allow_unicode=False)
    
    def save(self, *args, **kwargs) -> None:
        """"""
        if not self.slug:
            self.__slugify()
        super(Case, self).save(*args, **kwargs)
