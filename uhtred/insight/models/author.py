from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.functions import Lower
from django.db.models.constraints import UniqueConstraint

from uhtred.core.models.abstract import BaseFieldsAbstractModel
from uhtred.core.validators import (
    UsernameValidator,
    NoPoitSequenceValidator)


class Author(BaseFieldsAbstractModel):

    class Meta:
        verbose_name = _('author')
        verbose_name_plural = _('authors')
        constraints: tuple = (
            UniqueConstraint(
                Lower('username'),
                name='unique_author_username'),
        )

    avatar = models.ForeignKey(
        'base.Image',
        verbose_name='avatar',
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        blank=True)

    name = models.CharField(
        verbose_name=_('name'),
        max_length=45)

    username = models.CharField(
        _('username'),
        max_length=25,
        unique=True,
        null=True,
        default=None,
        validators=[UsernameValidator(), NoPoitSequenceValidator()],
        error_messages={
            'unique': _('An author with that username already exists'),
        })

    pt_name = models.CharField(
        verbose_name=_('name (pt)'),
        blank=True,
        default='',
        max_length=60)

    headline = models.CharField(
        verbose_name=_('headline'),
        blank=True,
        default='',
        max_length=100)

    website = models.URLField(
        verbose_name='website',
        blank=True,
        default='')

    instagram = models.URLField(
        verbose_name='instagram',
        blank=True,
        default='')

    linkedin = models.URLField(
        verbose_name='instagram',
        blank=True,
        default='')

    def __str__(self) -> str:
        return self.name

    @property
    def count_insights(self) -> int:
        return self.insights.filter(is_active=True).count()

    @property
    def count_series(self) -> int:
        return self.series.filter(is_active=True).count()
