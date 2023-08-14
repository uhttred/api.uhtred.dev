from typing import Any

from django.db import models
from django.utils.translation import gettext_lazy as _

from uhtred.core.models.abstract import BaseFieldsAbstractModel


class QuoteManager(models.Manager):
    
    def default_list(self, *args: Any, **kwargs: Any):
        return super().filter(
            is_active=True).filter(*args, **kwargs)
    

class Quote(BaseFieldsAbstractModel):
    
    class Meta:
        verbose_name = _('quote')
        verbose_name_plural = _('quotes')
    
    author = models.ForeignKey(
        'base.Person',
        related_name='quotes',
        on_delete=models.CASCADE)
    
    text = models.TextField(
        verbose_name=_('text'))
    
    pt_text = models.TextField(
        verbose_name=_('text (PT)'),
        blank=True,
        default=str)
    
    brand_logo = models.ForeignKey(
        'base.Image',
        verbose_name=_('brand logo'),
        related_name='quote_brand_logo',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None)
    
    brand_logo_dark = models.ForeignKey(
        'base.Image',
        verbose_name=_('brand logo dark'),
        related_name='quote_brand_logo_dark',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None)
    
    is_active = models.BooleanField(
        verbose_name='is active',
        default=True)
    
    objects = QuoteManager()

    def __str__(self) -> str:
        return 'Quote from %s' % self.author.name
    
    def author_name(self) -> str:
        return self.author.name
