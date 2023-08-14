from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404

from rest_framework.request import Request
from rest_framework.response import Response

from uhtred.core.views import ViewSet
from uhtred.core.paginator import Paginator

from uhtred.base.serializers import QuoteDetail
from uhtred.base.models import Quote

    
class QuoteViewSet(ViewSet, Paginator):

    lookup_field = 'quote_id'
    pg_limit = 10
    serializer_class = QuoteDetail

    def get(self, request: Request) -> Response:
        """"""
        return self.get_paginated_response(
            Quote.objects.default_list())

    def retrieve(self, request: Request, quote_id: str) -> Response:
        """"""
        obj: Quote = self.get_object(quote_id)
        return Response(self.serializer_class(obj).data)
    
    def get_object(self, quote_id: str) -> Quote:
        obj = get_object_or_404(Quote, id=quote_id, is_active=True)
        self.check_object_permissions(self.request, obj)
        return obj
