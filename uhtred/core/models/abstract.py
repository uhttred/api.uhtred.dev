import uuid
from datetime import timedelta

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now

from uhtred.core.strings import get_random_string_code


class BaseDateTimeFieldsAbstractModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(_('created at'), auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)


class BaseFieldsAbstractModel(BaseDateTimeFieldsAbstractModel):
    """
    Abstract Model with UUID field and base date time fields: created_at and updated_at
    """
    class Meta:
        abstract = True

    # id = models.UUIDField(_('id'), primary_key=True, default=uuid.uuid4, editable=False)
    uid = models.UUIDField(_('unique id'), default=uuid.uuid4, editable=False)


class AbstractTokenCode(BaseDateTimeFieldsAbstractModel):
    class Meta:
        abstract = True
    
    code = models.CharField(max_length=6)
    life_time = models.DateTimeField()

    def validate (self, code: str) -> bool:
        if code == self.code and self.life_time > now():
            self.delete()
            return True
        return False
    
    def update(self, seconds: int = 1800):
        self.code = get_random_string_code(6, '0123456789')
        self.life_time = timedelta(seconds=seconds) + now()
        self.save()