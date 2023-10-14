from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.functions import Lower
from django.db.models.constraints import UniqueConstraint
from django.utils.text import slugify

from uhtred.core.models.abstract import BaseFieldsAbstractModel


class SerieStatusChoice(models.TextChoices):
    IN_LAUNCH = 'in_lauch', _('in launch')
    COMPLETED = 'completed', _('completed')


class Serie(BaseFieldsAbstractModel):

    class Meta:
        verbose_name = _('serie')
        verbose_name_plural = _('series')
        constraints = (
            UniqueConstraint(
                Lower('title'),
                name='unique_serie_title'),
            UniqueConstraint(
                fields=['slug'],
                name='unique_serie_slug')
        )

    Status = SerieStatusChoice

    created_by = models.ForeignKey(
        'user.User',
        verbose_name=_('created by'),
        null=True,
        default=None,
        on_delete=models.SET_NULL,
        related_name='series')

    author = models.ForeignKey(
        'insight.Author',
        related_name='series',
        on_delete=models.SET_NULL,
        null=True)

    insights = models.ManyToManyField(
        'insight.Insight',
        through='insight.SerieItem',
        related_name='series')

    topics = models.ManyToManyField(
        'insight.Topic',
        related_name='series',
        blank=True)

    title = models.CharField(
        verbose_name=_('title'),
        max_length=230)

    pt_title = models.CharField(
        verbose_name=_('title (PT)'),
        max_length=230,
        blank=True,
        default=str)

    slug = models.SlugField(
        'slug',
        max_length=255,
        allow_unicode=True)

    description = models.TextField(
        verbose_name=_('description'))

    pt_description = models.TextField(
        verbose_name=_('description (PT)'),
        blank=True,
        default=str)

    status = models.TextField(
        default=Status.IN_LAUNCH,
        verbose_name=_('status'),
        max_length=9,
        choices=Status.choices)

    is_active = models.BooleanField(
        verbose_name=_('is active'),
        default=False)

    def __slugify(self):
        if not self.slug:
            self.slug = slugify(
                self.title,
                allow_unicode=False)

    def save(self, *args, **kwargs) -> None:
        self.__slugify()
        super(Serie, self).save(*args, **kwargs)
