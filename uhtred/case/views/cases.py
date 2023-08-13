from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404

from rest_framework.request import Request
from rest_framework.response import Response

from uhtred.core.views import ViewSet
from uhtred.core.paginator import Paginator
from uhtred.case.models import Case
from uhtred.case.serializers import CaseDetail

    
class CaseViewSet(ViewSet, Paginator):

    lookup_field = 'slug'
    lookup_value_regex = '[a-z0-9]+(?:-[a-z0-9]+)*'
    pg_name = _('cases listing')
    serializer_class = CaseDetail
    # pg_query_filter_choices = (
    #     'title__icontains',)

    def get(self, request: Request) -> Response:
        """"""
        if search := request.GET.get('search'):
            queryset = Case.objects.search(search)
        else:
            queryset = Case.objects.filter()
        return self.get_paginated_response(queryset)

    def retrieve(self, request: Request, slug: str) -> Response:
        """"""
        obj: Case = self.get_object(slug)
        return Response(self.serializer_class(obj).data)
    
    def get_object(self, case_slug: str) -> Case:
        obj = get_object_or_404(Case, slug=case_slug)
        self.check_object_permissions(self.request, obj)
        return obj
