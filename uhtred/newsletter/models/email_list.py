from django.db import models
from django.db.models.functions import Lower
from django.db.models.constraints import UniqueConstraint
from django.utils.translation import gettext_lazy as _

from uhtred.core.models.abstract import BaseFieldsAbstractModel
from uhtred.core.validators import (
    NameValidator,
    NoPoitSequenceValidator)


class EmailList(BaseFieldsAbstractModel):
    class Meta:
        verbose_name = _('email list')
        verbose_name_plural = _('emails list')
        constraints: tuple = (
            UniqueConstraint(
                fields=['email', 'verified'],
                condition=models.Q(verified=True),
                name='unique_verified_email'),
            )
    
    name = models.CharField(
        _('name'),
        max_length=60,
        blank=True,
        validators=[NameValidator(),
                    NoPoitSequenceValidator()],
        default=str)
    
    email = models.EmailField(
        verbose_name=_('email'))
    
    verified = models.BooleanField(
        verbose_name=_('verifeid'),
        default=False)
    
    is_active = models.BooleanField(
        verbose_name=_('is active'),
        default=True)
    
    tags = models.ManyToManyField(
        'base.Tag',
        related_name='emails_list',
        blank=True)
