from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404

from rest_framework.request import Request
from rest_framework.response import Response

from uhtred.core.views import ViewSet
from uhtred.core.paginator import Paginator
from uhtred.insight.models import Serie
from uhtred.insight.serializers import SerieDetail


class SerieViewSet(ViewSet, Paginator):

    lookup_field = 'slug'
    lookup_value_regex = '[a-z0-9]+(?:-[a-z0-9]+)*'
    pg_name = _('serie listing')
    serializer_class = SerieDetail
    pg_fields = ('id', 'uid', 'slug', 'title', 'topics', 'status', 'count_insights', 'count_insights_views',
                 'pt_title', 'description', 'pt_description', 'created_at')

    pg_order_by: str = '-created_at'
    pg_order_choices: tuple = (
        '-created_at',
        'created_at',
        '-updated_at',
        'updated_at')

    pg_query_filter_choices = (
        'topics__in',
        'insights__in',
        'status')

    def get(self, request: Request) -> Response:
        """"""
        if search := request.query_params.get('search'):
            queryset = Serie.objects.search(search)
        else:
            queryset = Serie.objects.default_list()
        return self.get_paginated_response(queryset)

    def retrieve(self, request: Request, slug: str) -> Response:
        """"""
        obj: Serie = self.get_object(slug)
        return Response(self.serializer_class(obj).data)

    def get_object(self, slug: str) -> Serie:
        obj: Serie = get_object_or_404(Serie, slug=slug, is_active=True)
        self.check_object_permissions(self.request, obj)
        return obj
