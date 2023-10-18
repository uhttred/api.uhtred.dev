from rest_framework.request import Request
from rest_framework.response import Response

from uhtred.core.views import ViewSet
from uhtred.core.paginator import Paginator
from uhtred.core.exceptions import APIError

from uhtred.insight.serializers import SerieItemDetail
from uhtred.insight.models import SerieItem


class SerieItemViewSet(ViewSet, Paginator):

    pg_limit = 100
    serializer_class = SerieItemDetail
    pg_order_by: str = 'number'
    pg_order_choices: tuple = (
        'number',
        '-number')

    def get(self, request: Request) -> Response:
        """"""
        if serie_id := request.query_params.get('serie'):
            queryset = SerieItem.objects.filter(
                insight__is_active=True,
                serie=serie_id)
            return self.get_paginated_response(queryset)
        raise APIError()
