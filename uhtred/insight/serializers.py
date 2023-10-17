from rest_framework import serializers

from uhtred.base.serializers import ImageDetail

from uhtred.core.serializers import DynamicFieldsModelSerializer
from uhtred.insight.models import (
    Insight,
    Topic,
    Serie,
    Author)


class AuthorDetail(DynamicFieldsModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

    avatar = ImageDetail(read_only=True)
    count_series = serializers.IntegerField(read_only=True)
    count_insights = serializers.IntegerField(read_only=True)


class TopicDetail(DynamicFieldsModelSerializer):
    class Meta:
        model = Topic
        fields = [
            'id',
            'name',
            'pt_name',
            'is_main',
            'is_category'
        ]


class InsightDetail(DynamicFieldsModelSerializer):
    class Meta:
        model = Insight
        exclude = ['is_active']

    cover = ImageDetail(read_only=True)
    author = AuthorDetail(read_only=True)
    topics = TopicDetail(read_only=True, many=True)


class SerieDetail(DynamicFieldsModelSerializer):

    class Meta:
        model = Serie
        exclude = ['is_active']

    author = AuthorDetail(read_only=True)
    topics = TopicDetail(read_only=True, many=True)
    count_insights = serializers.IntegerField(read_only=True)
    count_insights_views = serializers.IntegerField(read_only=True)
