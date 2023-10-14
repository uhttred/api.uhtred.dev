from django.db import models
from django.db.models.functions import Lower
from django.utils.translation import gettext_lazy as _
from django.db.models.constraints import UniqueConstraint
from django.utils.text import slugify

from uhtred.core.models.abstract import BaseFieldsAbstractModel


class Topic(BaseFieldsAbstractModel):

    class Meta:
        verbose_name = _('topic')
        verbose_name_plural = _('topics')
        constraints = (
            UniqueConstraint(
                Lower('name'),
                name='unique_topic_name'),
            UniqueConstraint(
                fields=['slug'],
                name='unique_topic_slug')
        )

    name = models.CharField(
        verbose_name=_('name'),
        max_length=60)

    pt_name = models.CharField(
        verbose_name=_('name (PT)'),
        max_length=60,
        blank=True,
        default='')

    slug = models.SlugField(
        verbose_name='slug',
        max_length=120,
        editable=False,
        allow_unicode=True)

    is_category = models.BooleanField(
        verbose_name=_('is category'),
        default=False)

    is_main = models.BooleanField(
        verbose_name=_('is main topic'),
        default=False)

    def __str__(self) -> str:
        return self.name

    def __slugify(self):
        if not self.slug:
            self.slug = slugify(
                self.name,
                allow_unicode=False)

    def save(self, *args, **kwargs) -> None:
        self.__slugify()
        super(Topic, self).save(*args, **kwargs)
