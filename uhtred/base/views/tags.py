from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404

from rest_framework.request import Request
from rest_framework.response import Response

from uhtred.core.views import ViewSet
from uhtred.core.paginator import Paginator

from uhtred.base.serializers import TagDetail
from uhtred.base.models import Tag

    
class TagViewSet(ViewSet, Paginator):

    lookup_field = 'slug'
    pg_name = _('global tags listing')
    pg_limit = 60
    serializer_class = TagDetail
    # pg_query_filter_choices = (
    #     'title__icontains',)

    def get(self, request: Request) -> Response:
        """"""
        return self.get_paginated_response(Tag.objects.all())

    def retrieve(self, request: Request, tag_slug: str) -> Response:
        """"""
        obj: Tag = self.get_object(tag_slug)
        return Response(self.serializer_class(obj).data)
    
    def get_object(self, tag_slug: str) -> Tag:
        obj = get_object_or_404(Tag, slug=tag_slug)
        self.check_object_permissions(self.request, obj)
        return obj
