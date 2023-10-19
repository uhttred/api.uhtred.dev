from rest_framework import serializers

from uhtred.base.serializers import ImageDetail

from uhtred.core.serializers import DynamicFieldsModelSerializer
from uhtred.insight.models import (
    Insight,
    Topic,
    Serie,
    SerieItem,
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
            'slug',
            'name',
            'pt_name',
            'is_main',
            'is_category'
        ]


class SerieDetail(DynamicFieldsModelSerializer):

    class Meta:
        model = Serie
        exclude = ['is_active']

    author = AuthorDetail(read_only=True)
    topics = TopicDetail(read_only=True, many=True)
    count_insights = serializers.IntegerField(read_only=True)
    count_insights_views = serializers.IntegerField(read_only=True)


class InsightDetail(DynamicFieldsModelSerializer):

    class Meta:
        model = Insight
        exclude = ['is_active', 'is_featured', 'is_completed', 'created_by']

    cover = ImageDetail(read_only=True)
    # serie_number = serializers.SerializerMethodField()
    author = AuthorDetail(read_only=True, fields=[
        'uid', 'name', 'pt_name', 'avatar', 'headline'])
    topics = TopicDetail(read_only=True, many=True)
    serie = SerieDetail(read_only=True, fields=[
        'id', 'slug', 'title', 'pt_title', 'status'])

    # def get_serie_number(self, obj) -> int | None:
    #     if ((request := self.context.get('request'))
    #             and (serie_id := request.query_params.get('serie-number'))):
    #         if serieitem := obj.serieitem_set.filter(serie=serie_id).first():
    #             return serieitem.number
    #     return None


class SerieItemDetail(DynamicFieldsModelSerializer):
    class Meta:
        model = SerieItem
        fields = ['id', 'insight', 'serie', 'number']

    insight = InsightDetail(read_only=True, fields=[
        'id', 'slug'])
