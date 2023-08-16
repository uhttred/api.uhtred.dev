from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404

from rest_framework.request import Request
from rest_framework.response import Response

from uhtred.core.views import ViewSet
from uhtred.core.paginator import Paginator
from uhtred.insight.models import Insight
from uhtred.insight.serializers import InsightDetail

    
class InsightViewSet(ViewSet, Paginator):

    lookup_field = 'slug'
    lookup_value_regex = '[a-z0-9]+(?:-[a-z0-9]+)*'
    pg_name = _('cases listing')
    serializer_class = InsightDetail

    # pg_query_filter_choices = (
    #     'title__icontains',)

    def get(self, request: Request) -> Response:
        """"""
        if search := request.GET.get('search'):
            queryset = Insight.objects.search(search)
        else:
            queryset = Insight.objects.default_list()
        return self.get_paginated_response(
            queryset,
            fields=('id', 'uid', 'slug', 'title', 'cover', 'author', 'tags',
                    'pt_title', 'description', 'pt_description', 'created_at',
                    'published_at'))

    def retrieve(self, request: Request, slug: str) -> Response:
        """"""
        obj: Insight = self.get_object(slug)
        return Response(self.serializer_class(obj).data)
    
    def get_object(self, slug: str) -> Insight:
        obj = get_object_or_404(Insight, slug=slug, is_active=True)
        self.check_object_permissions(self.request, obj)
        return obj