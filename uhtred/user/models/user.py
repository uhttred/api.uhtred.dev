from django.db import models
from django.db.models.functions import Lower
from django.db.models.constraints import UniqueConstraint
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, UserManager as UM

from uhtred.core.models.abstract import BaseFieldsAbstractModel
from uhtred.core.validators import (
    UsernameValidator,
    NameValidator,
    NoPoitSequenceValidator,
    EmailValidator)


class UserRole(models.TextChoices):
    COLLABORATOR = 'collaborator', _('collaborator')
    MEMBER = 'member', _('member')


class UserManager(UM):
    
    def is_username_registered(self, username: str, ignore_owner_id: str = None) -> bool:
        """"""
        queryset = ( self.filter(username__iexact=username) if not ignore_owner_id
            else self.filter(
                ~models.Q(id=ignore_owner_id),
                models.Q(username__iexact=username))
            )
        return queryset.exists()


class User(AbstractUser, BaseFieldsAbstractModel):

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        constraints: tuple = (
            UniqueConstraint(
                Lower('username'),
                name='unique_user_username'),
            )
    
    Role = UserRole

    name = models.CharField(_('name'), max_length=40, blank=True,
        validators=[NameValidator(), NoPoitSequenceValidator()], default=str)
    role = models.CharField(_('role'), max_length=12, choices=Role.choices, default=Role.MEMBER)
    email = models.EmailField(_('email address'), null=True, blank=True,
        validators=[EmailValidator()], default=None)
    username = models.CharField(
        _('username'),
        max_length=25,
        unique=True,
        # help_text=_('Required. 25 characters or fewer. Letters, digits and ./-/_ only.'),
        validators=[UsernameValidator(), NoPoitSequenceValidator()],
        error_messages={
            'unique': _('A user with that username already exists'),
        })
    
    first_name = None
    last_name =  None
    date_joined = None
    last_login = None

    objects = UserManager()


class MemberManager(UserManager):

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(role=UserRole.MEMBER)


class Member(User):

    class Meta:
        proxy = True
        verbose_name = _('member')
        verbose_name_plural = _('members')

    Role = UserRole
    objects = MemberManager()

    def save(self, *args, **kwargs) -> None:
        if not self.pk:
            self.role = UserRole.MEMBER
        return super().save(*args, **kwargs)


class CollaboratorManager(UserManager):

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(role=UserRole.COLLABORATOR)


class Collaborator(User):

    class Meta:
        proxy = True
        verbose_name = _('collaborator')
        verbose_name_plural = _('collaborators')

    Role = UserRole
    objects = MemberManager()

    def save(self, *args, **kwargs) -> None:
        if not self.pk:
            self.role = UserRole.COLLABORATOR
        return super().save(*args, **kwargs)
