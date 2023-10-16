from rest_framework.viewsets import ViewSet as RestViewSet
from uhtred.core.validators import int_id_regex

class ViewSet(RestViewSet):
    lookup_value_regex = int_id_regex
