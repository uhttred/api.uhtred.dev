from rest_framework import serializers

from django.utils.translation import gettext_lazy as _

from uhtred.insight.models import Insight
from uhtred.core.serializers import DynamicFieldsModelSerializer

from uhtred.base.serializers import ImageDetail, TagDetail, PersonDetail


class InsightDetail(DynamicFieldsModelSerializer):
    
    class Meta:
        model = Insight
        exclude = ['is_active']
    
    cover = ImageDetail(read_only=True)
    author = PersonDetail(read_only=True)
    tags = TagDetail(read_only=True, many=True)
    published_at = serializers.DateTimeField(
        format="%d %B %Y at %H:%M",
        required=False,
        read_only=True)
