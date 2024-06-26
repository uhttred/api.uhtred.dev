from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action

from uhtred.core.views import ViewSet
from uhtred.core.paginator import Paginator
from uhtred.core.models.queryset import get_queryset_random_entries

from uhtred.base.serializers import TagDetail
from uhtred.base.models import Tag

    
class TagViewSet(ViewSet, Paginator):

    lookup_field = 'slug'
    lookup_value_regex = '[a-z0-9]+(?:-[a-z0-9]+)*'
    pg_name = _('global tags listing')
    pg_limit = 60
    serializer_class = TagDetail
    # pg_query_filter_choices = (
    #     'title__icontains',)

    def get(self, request: Request) -> Response:
        """"""
        return self.get_paginated_response(Tag.objects.all())
    
    @action(
        detail=False,
        methods=['GET'],
        url_path='random')
    def get_random_tags(self, request: Request) -> Response:
        self.set_pg_limit()
        qs =  get_queryset_random_entries(Tag.objects.all(), self.pg_limit)
        return self.get_list_paginated_response(qs)

    def retrieve(self, request: Request, slug: str) -> Response:
        """"""
        obj: Tag = self.get_object(slug)
        return Response(self.serializer_class(obj).data)
    
    def get_object(self, slug: str) -> Tag:
        obj = get_object_or_404(Tag, slug=slug)
        self.check_object_permissions(self.request, obj)
        return obj
