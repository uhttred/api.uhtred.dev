from django.db import models
from django.db.models.functions import Lower
from django.db.models.constraints import UniqueConstraint
from django.utils.translation import gettext_lazy as _

from uhtred.core.models.abstract import BaseFieldsAbstractModel
from uhtred.core.validators import (
    NoPoitSequenceValidator,
    NameValidator)


class Email(BaseFieldsAbstractModel):

    class Meta:

        verbose_name = _('email list')
        verbose_name_plural = _('email list')
        constraints = (
            UniqueConstraint(
                Lower('email'),
                name='unique_email_email'),
        )

    subscribed_topics = models.ManyToManyField(
        'insight.Topic',
        related_name='subscribed_emails',
        blank=True)

    name = models.CharField(
        _('name'),
        max_length=45,
        blank=True,
        validators=[
            NameValidator(),
            NoPoitSequenceValidator()],
        default=str)

    email = models.EmailField(
        unique=True,
        verbose_name=_('email'))

    verified = models.BooleanField(
        verbose_name=_('verifeid'),
        default=False)

    subscribe_to_all = models.BooleanField(
        verbose_name=_('subscribe to all topics'),
        default=False)

    def __str__(self):
        return f'{self.name} ({self.email})' if self.name else self.email
