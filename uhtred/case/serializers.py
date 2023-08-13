from rest_framework import serializers

from django.utils.translation import gettext_lazy as _

from uhtred.case.models import Case
from uhtred.core.serializers import DynamicFieldsModelSerializer
from uhtred.core.exceptions import APIError

from uhtred.base.serializers import ImageDetail


class CaseDetail(DynamicFieldsModelSerializer):
    
    class Meta:
        model = Case
        exclude = ['is_active']
    
    cover = ImageDetail(read_only=True)
    banner = ImageDetail(read_only=True)
    banner_dark = ImageDetail(read_only=True)
    brand_logo = ImageDetail(read_only=True)
    brand_logo_dark = ImageDetail(read_only=True)
