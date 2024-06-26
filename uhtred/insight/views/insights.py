from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action

from uhtred.core.views import ViewSet
from uhtred.core.paginator import Paginator
from uhtred.core.models.queryset import get_queryset_random_entries
from uhtred.insight.models import Insight
from uhtred.insight.serializers import InsightDetail


class InsightViewSet(ViewSet, Paginator):

    lookup_field = 'slug'
    lookup_value_regex = '[a-z0-9]+(?:-[a-z0-9]+)*'
    serializer_class = InsightDetail
    pg_fields = ('id', 'uid', 'slug', 'title', 'cover', 'author', 'topics',
                 'pt_title', 'description', 'pt_description', 'created_at',
                 'published_at')

    pg_order_by: str = '-published_at'
    pg_order_choices: tuple = (
        'visualisations',
        '-visualisations',
        'published_at',
        '-published_at',
        '-created_at',
        'created_at',
        '-updated_at',
        'updated_at',
        '-serieitem__number',
        'serieitem__number')
    pg_query_filter_choices = (
        'author',
        'topics__in',
        'series__in',
        'is_featured')

    def get(self, request: Request) -> Response:
        """"""

        if request.query_params.get('minimal-fields') == 'yes':
            self.pg_fields = ['id', 'title', 'pt_title', 'slug']

        if search := request.query_params.get('search'):
            queryset = Insight.objects.search(search)
        else:
            queryset = Insight.objects.default_list()
        return self.get_paginated_response(queryset)

    def retrieve(self, request: Request, slug: str) -> Response:
        """"""
        obj: Insight = self.get_object(slug)
        return Response(self.serializer_class(obj).data)

    @action(
        detail=False,
        methods=['GET'],
        url_path='random')
    def get_random_insights(self, request: Request) -> Response:
        self.set_pg_limit()
        qs = get_queryset_random_entries(Insight.objects.default_list(), self.pg_limit)
        return self.get_list_paginated_response(qs)

    @action(
        detail=False,
        methods=['GET'],
        url_path='featured')
    def get_random_featured_insights(self, request: Request) -> Response:
        if request.GET.get('minimal-fields') == 'yes':
            self.pg_fields = ['id', 'title', 'pt_title', 'slug']
        self.set_pg_limit()
        qs = get_queryset_random_entries(
            Insight.objects.default_list(is_featured=True), self.pg_limit)
        return self.get_list_paginated_response(qs)

    @action(
        detail=True,
        methods=['PATCH'],
        url_path='visualisations')
    def up_visualisations(self, request: Request, slug: str) -> Response:
        obj: Insight = self.get_object(slug)
        obj.up_visualisations()
        return Response(self.serializer_class(obj).data)

    def get_object(self, slug: str) -> Insight:
        obj = get_object_or_404(Insight, slug=slug, is_active=True)
        self.check_object_permissions(self.request, obj)
        return obj
