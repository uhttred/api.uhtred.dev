from rest_framework import serializers

from uhtred.base.serializers import ImageDetail

from uhtred.core.serializers import DynamicFieldsModelSerializer
from uhtred.insight.models import (
    Insight,
    Topic,
    Author)


class AuthorDetail(DynamicFieldsModelSerializer):
    class Meta:
        model = Author
        exclude = ['uid']

    avatar = ImageDetail(read_only=True)


class TopicDetail(DynamicFieldsModelSerializer):
    class Meta:
        model = Topic
        fields = [
            'id',
            'name',
            'pt_name'
        ]


class InsightDetail(DynamicFieldsModelSerializer):
    class Meta:
        model = Insight
        exclude = ['is_active']

    cover = ImageDetail(read_only=True)
    author = AuthorDetail(read_only=True)
    topics = TopicDetail(read_only=True, many=True)
