from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.constraints import UniqueConstraint

from uhtred.core.models.abstract import BaseFieldsAbstractModel


class SerieItem(BaseFieldsAbstractModel):

    class Meta:
        # ordering = ('-number', )
        verbose_name = _('serie item')
        verbose_name_plural = _('serie items')
        constraints = (
            UniqueConstraint(
                fields=['insight', 'serie'],
                name='unique_serie_insight'),
        )

    insight = models.ForeignKey(
        'insight.Insight',
        verbose_name=_('inisght'),
        on_delete=models.CASCADE)

    serie = models.ForeignKey(
        'insight.Serie',
        verbose_name=_('serie'),
        on_delete=models.CASCADE)

    number = models.PositiveIntegerField(
        verbose_name=_('order number'),
        null=True,
        blank=True,
        default=None)

    def __str__(self) -> str:
        return '%s > %s' % (self.insight.title, self.serie.title)

    def __set_next_number(self) -> None:
        if not self.number:
            self.number = self.serie.insights.count() + 1

    def save(self, *args, **kwargs) -> None:
        self.__set_next_number()
        super(SerieItem, self).save(*args, **kwargs)
