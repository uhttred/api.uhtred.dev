from django.shortcuts import get_object_or_404

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action

from uhtred.core.views import ViewSet
from uhtred.core.paginator import Paginator
from uhtred.core.models.queryset import get_queryset_random_entries

from uhtred.insight.serializers import TopicDetail
from uhtred.insight.models import Topic


class TopicViewSet(ViewSet, Paginator):

    lookup_field = 'slug'
    lookup_value_regex = '[a-z0-9]+(?:-[a-z0-9]+)*'
    pg_limit = 100
    serializer_class = TopicDetail
    pg_order_choices = (
        'is_category',
        '-is_category',
        'name',
        '-name',
        'created_at',
        '-created_at'
    )

    # pg_query_filter_choices = (
    #     'title__icontains',)

    def get(self, request: Request) -> Response:
        """"""
        return self.get_paginated_response(Topic.objects.all())

    def retrieve(self, request: Request, slug: str) -> Response:
        """"""
        obj: Topic = self.get_object(slug)
        return Response(self.serializer_class(obj).data)

    @action(
        detail=False,
        methods=['GET'],
        url_path='random')
    def get_random_tapics(self, request: Request) -> Response:
        self.set_pg_limit()
        qs = get_queryset_random_entries(Topic.objects.all(), self.pg_limit)
        return self.get_list_paginated_response(qs)

    def get_object(self, slug: str) -> Topic:
        obj = get_object_or_404(Topic, slug=slug)
        self.check_object_permissions(self.request, obj)
        return obj
