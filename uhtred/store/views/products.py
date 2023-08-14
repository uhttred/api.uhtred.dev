from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404

from rest_framework.request import Request
from rest_framework.response import Response

from uhtred.core.views import ViewSet
from uhtred.core.paginator import Paginator
from uhtred.store.models import Product
from uhtred.store.serializers import ProductDetail

    
class ProductViewSet(ViewSet, Paginator):

    lookup_field = 'slug'
    lookup_value_regex = '[a-z0-9]+(?:-[a-z0-9]+)*'
    pg_name = _('products listing')
    serializer_class = ProductDetail
    pg_query_filter_choices = (
        'name__icontains',)

    def get(self, request: Request) -> Response:
        """"""
        queryset = Product.objects.default_list()
        return self.get_paginated_response(queryset)

    def retrieve(self, request: Request, slug: str) -> Response:
        """"""
        obj: Product = self.get_object(slug)
        return Response(self.serializer_class(obj).data)
    
    def get_object(self, product_slug: str) -> Product:
        obj = get_object_or_404(slug=product_slug, is_active=True)
        self.check_object_permissions(self.request, obj)
        return obj
