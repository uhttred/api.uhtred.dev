from typing import Any

from django.db import models
from django.db.models.functions import Lower
from django.db.models.constraints import UniqueConstraint
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

from uhtred.core.models.abstract import BaseFieldsAbstractModel


class ProductManager(models.Manager):

    def default_list(self, *args: Any, **kwargs: Any):
        return super().filter(
            is_active=True).filter(*args, **kwargs)


class Product(BaseFieldsAbstractModel):

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')
        constraints = (
            UniqueConstraint(
                Lower('name'),
                name='unique_product_name'),
            UniqueConstraint(
                fields=['slug'],
                name='unique_product_slug')
        )

    slug = models.SlugField(
        'slug',
        max_length=250,
        allow_unicode=True)

    cover = models.ForeignKey(
        'base.Image',
        verbose_name=_('cover'),
        related_name='product_cover',
        on_delete=models.SET_NULL,
        null=True)

    name = models.CharField(
        verbose_name=_('name'),
        max_length=250)

    pt_name = models.CharField(
        verbose_name=_('(pt) name'),
        max_length=250,
        null=True,
        default=None,
        blank=True)

    buy_at = models.URLField(
        verbose_name=_('buy at'))

    price = models.DecimalField(
        _('price'),
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True,
        default=None)

    tags = models.ManyToManyField(
        'base.Tag',
        related_name='products',
        blank=True)

    topics = models.ManyToManyField(
        'insight.Topic',
        related_name='products',
        blank=True)

    see_prices = models.BooleanField(
        verbose_name=_('see prices'),
        default=False)

    is_featured = models.BooleanField(
        verbose_name=_('is featured'),
        default=False)

    is_active = models.BooleanField(
        verbose_name=_('is active'),
        default=True)

    objects = ProductManager()

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
        super(Product, self).save(*args, **kwargs)
