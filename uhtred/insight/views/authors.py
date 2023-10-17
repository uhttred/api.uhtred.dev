from django.shortcuts import get_object_or_404

from rest_framework.request import Request
from rest_framework.response import Response

from uhtred.core.views import ViewSet
from uhtred.core.paginator import Paginator
from uhtred.core.validators import uuid_regex

from uhtred.insight.serializers import AuthorDetail
from uhtred.insight.models import Author


class AuthorViewSet(ViewSet, Paginator):

    lookup_field = 'uid'
    lookup_value_regex = uuid_regex
    pg_limit = 6
    serializer_class = AuthorDetail

    def get(self, request: Request) -> Response:
        """"""
        return self.get_paginated_response(Author.objects.all())

    def retrieve(self, request: Request, uid: str) -> Response:
        """"""
        obj: Author = self.get_object(uid)
        return Response(self.serializer_class(obj).data)

    def get_object(self, uid: str) -> Author:
        obj = get_object_or_404(Author, uid=uid)
        self.check_object_permissions(self.request, obj)
        return obj
