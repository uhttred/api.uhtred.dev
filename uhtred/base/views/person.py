from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404

from rest_framework.request import Request
from rest_framework.response import Response

from uhtred.core.views import ViewSet

from uhtred.base.serializers import PersonDetail
from uhtred.base.models import Person

    
class PersonViewSet(ViewSet):

    lookup_field = 'person_id'
    serializer_class = PersonDetail

    def retrieve(self, request: Request, person_id: int) -> Response:
        obj: Person = self.get_object(person_id)
        return Response(self.serializer_class(obj).data)
    
    def get_object(self, person_id: int) -> Person:
        obj = get_object_or_404(Person, id=person_id)
        self.check_object_permissions(self.request, obj)
        return obj
