from typing import Any

from django.db import models
from django.db.models.functions import Lower
from django.db.models.constraints import UniqueConstraint
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.utils.timezone import now

from martor.models import MartorField

from uhtred.insight.signals import insight_published
from uhtred.core.models.abstract import BaseFieldsAbstractModel
from uhtred.core.text import get_random_string_code


class InsightManager(models.Manager):

    def default_list(self, *args: Any, **kwargs: Any):
        return super().filter(
            is_active=True,
            published_at__isnull=False).filter(*args, **kwargs)

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

    created_by = models.ForeignKey(
        'user.User',
        verbose_name=_('created by'),
        null=True,
        default=None,
        on_delete=models.SET_NULL,
        related_name='insights')

    author = models.ForeignKey(
        'insight.Author',
        related_name='insights',
        on_delete=models.SET_NULL,
        null=True,
        default=None)

    cover = models.ForeignKey(
        'base.Image',
        verbose_name=_('cover'),
        related_name='insight_cover',
        on_delete=models.SET_NULL,
        null=True,
        blank=True)

    topics = models.ManyToManyField(
        'insight.Topic',
        related_name='insights',
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
        max_length=250,
        allow_unicode=True)

    description = models.TextField(
        verbose_name=_('description'))

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

    youtube_src = models.URLField(
        verbose_name=_('youtube src'),
        default=None,
        blank=True,
        null=True)

    visualisations = models.PositiveIntegerField(
        verbose_name=_('visualisations'),
        default=0)

    is_active = models.BooleanField(
        verbose_name=_('is active'),
        default=False)

    is_completed = models.BooleanField(
        verbose_name=_('is completed'),
        default=False)

    is_featured = models.BooleanField(
        verbose_name=_('is featured'),
        default=False)

    notify_newsletter = models.BooleanField(
        _('notify newsletter'),
        default=True)

    show_updated_at = models.BooleanField(
        _('show updated at'),
        default=False)

    published_at = models.DateTimeField(
        verbose_name=_('published at'),
        null=True,
        default=None)

    objects = InsightManager()

    def __str__(self) -> str:
        return self.title

    def __slugify(self):
        if not self.slug:
            self.slug = slugify(
                '%s %s' % (self.title, get_random_string_code(4)),
                allow_unicode=False)

    @property
    def serie(self):
        """primary insight serie"""
        return self.series.first()


    def up_visualisations(self):
        self.visualisations = self.visualisations + 1
        self.save()

    def publish(self) -> bool:
        if self.is_completed and not self.published_at:
            self.published_at = now()
            self.save()
            insight_published.send(
                self.__class__,
                insight=self)
            return True
        return False

    def save(self, *args, **kwargs) -> None:
        self.__slugify()
        super(Insight, self).save(*args, **kwargs)
