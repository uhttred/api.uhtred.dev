from typing import Sequence, Union, Tuple
from rest_framework.response import Response

from django.utils.translation import gettext_lazy as _
from django.db.models.query import QuerySet

from core.exceptions import APIError


class InitLimitPaginatorMixin(object):
    """
    Init Limit Paginator Class
    serializer_class DynamicFieldsModelSerializer expected
    """

    pg_response_class = Response
    pg_exception_class = APIError

    pg_min_limit: int = 1
    pg_max_limit: int = 100
    pg_limit_query_param: str = 'limit'
    pg_init_query_param: str = 'init'
    pg_order_query_param: str = 'order_by'
    pg_entries_key: str = 'entries'

    pg_name: str = ''  # Pagination name
    pg_fields: Sequence[str] = []  # serializer fields
    pg_exclude: Sequence[str] = []  # serializer fields to exlude

    pg_init: int = 0
    pg_limit: int = 20
    pg_query_filter_choices: Sequence[str] = []

    pg_order_by: str = '-created_at'
    pg_order_choices: tuple = (
        '-created_at',
        'created_at',
        '-updated_at',
        'updated_at')

    def get_paginated_response(self,
                               queryset,
                               serializer_class=None,
                               fields: Sequence[str] = [],
                               exclude: Sequence[str] = [],
                               status_code=200) -> Response:
        """
        Paginate a Queryset and Returns a rest_framework.response.Response
        (by default) with queryset data serialize and total objects count
        """

        data = self.get_paginated_data(
            queryset,
            serializer_class,
            fields, exclude)

        return self.pg_response_class(data, status=status_code)

    def get_paginated_data(self,
                           queryset,
                           serializer_class=None,
                           fields: Sequence[str] = [],
                           exclude: Sequence[str] = []) -> dict:

        queryset = self.__get_paginated_queryset(queryset)
        data: dict = self.__get_data(
            queryset=queryset,
            serializer_class=serializer_class,
            fields=fields,
            exclude=exclude)

        return data

    def set_pg_limit(self, max_limit: Union[int, None] = None) -> None:
        if max_limit:
            self.pg_max_limit = max_limit
        self.__set_pg_limit()

    def __get_paginated_queryset(self, queryset: QuerySet) -> QuerySet:
        self.__set_defaults()

        if self.pg_query_filter_choices and self.request.GET:  # type: ignore
            queryset = queryset.filter(
                **self.__get_query_filters())

        self.pg_count = queryset.count()

        if self.pg_count == 0 or self.pg_init > self.pg_count:
            return list()

        return queryset.order_by(
            self.pg_order_by)[self.pg_init:self.pg_init + self.pg_limit]

    def __get_next(self) -> Union[None, dict]:
        init = None
        if (next_pg := self.pg_limit + self.pg_init) < self.pg_count:
            init = next_pg

        if init is not None:
            return {
                self.pg_init_query_param: init,
                self.pg_limit_query_param: self.pg_limit}
        return None

    def __get_previous(self) -> Union[None, dict]:
        init = None

        if (previous := self.pg_init - self.pg_limit) >= 0:
            init = previous

        if init is not None:
            return {
                self.pg_init_query_param: init,
                self.pg_limit_query_param: self.pg_limit}
        return None

    def __get_query_filters(self) -> dict:
        filters: dict = {}
        for key, val in self.request.GET.items():  # type: ignore
            if key in self.pg_query_filter_choices:
                filters[key] = val
        return filters

    def __get_data(self,
                   queryset: QuerySet,
                   serializer_class=None,
                   fields: Sequence[str] = [],
                   exclude: Sequence[str] = [], ) -> dict:
        """"""

        fields = fields or self.pg_fields
        exclude = exclude or self.pg_exclude
        serializer_class = serializer_class or self.serializer_class  # type: ignore
        assert serializer_class is not None

        data = serializer_class(queryset,
                                many=True,
                                fields=fields,
                                exclude=exclude,
                                context={'request': self.request}).data  # type: ignore

        context: dict = {
            'total': self.pg_count,  # total entries
            'name': self.pg_name,
            'page_size': self.pg_limit,
            'init': self.pg_init,
            'count': len(data),  # total current page entries
            'is_empty': True if not data else False,
            'next': self.__get_next(),
            'previous': self.__get_previous(),
            'order': self.__get__order(),
            self.pg_entries_key: data}
        # if not context.get('name'):
        #     context.pop('name')
        return context

    def __get__order(self):
        return {
            'by': self.pg_order_by,
            'direction': 'desc' if '-' in self.pg_order_by else 'asc'}
        # 'parameter': self.pg_order_query_param}
        # 'choices': self.pg_order_choices}

    def __set_defaults(self) -> None:
        """
        set dafaults pagination 
        values from query paramenters
        """
        self.__set_pg_init()
        self.__set_pg_limit()
        self.__set_pg_order()

    def __set_pg_order(self) -> None:
        self.pg_order_by = self.request.GET.get(  # type: ignore
            self.pg_order_query_param,
            self.pg_order_by)

        if self.pg_order_by not in self.pg_order_choices:
            raise self.pg_exception_class(
                _("the value '{}' of '{}' parameter not in order choices").format(
                    self.pg_order_by, self.pg_order_query_param))

    def __set_pg_limit(self) -> None:
        try:
            self.pg_limit = int(self.request.GET.get(  # type: ignore
                self.pg_limit_query_param,
                self.pg_limit))
        except:
            pass

        if self.pg_limit < self.pg_min_limit or self.pg_limit > self.pg_max_limit:
            raise self.pg_exception_class(
                _("'{}' parameter must be an integer between {} and {}").format(
                    self.pg_limit_query_param, self.pg_min_limit, self.pg_max_limit))

    def __set_pg_init(self) -> None:
        try:
            self.pg_init = int(self.request.GET.get(  # type: ignore
                self.pg_init_query_param,
                self.pg_init))
        except:
            self.pg_init = 0

        if self.pg_init < 0:
            raise self.pg_exception_class(
                _("'%s' parameter must be an integer starting form 0").format(
                    self.pg_init_query_param))


Paginator = InitLimitPaginatorMixin
