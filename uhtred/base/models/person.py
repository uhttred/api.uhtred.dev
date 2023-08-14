from django.db import models
from django.utils.translation import gettext_lazy as _

from uhtred.core.models.abstract import BaseFieldsAbstractModel


class Person(BaseFieldsAbstractModel):
    
    class Meta:
        verbose_name = _('person')
        verbose_name_plural = _('person')
    
    name = models.CharField(
        verbose_name=_('name'),
        max_length=60)
    
    headline = models.CharField(
        verbose_name=_('headline'),
        max_length=100)
    
    job_title = models.CharField(
        verbose_name=_('job title'),
        max_length=100)

    website = models.URLField(
        verbose_name='website',
        blank=True,
        default='')    

    avatar = models.ForeignKey(
        'base.Image',
        verbose_name='avatar',
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        blank=True)

    def __str__(self) -> str:
        return self.name
