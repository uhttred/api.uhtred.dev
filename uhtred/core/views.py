from rest_framework.viewsets import ViewSet as RestViewSet

class ViewSet(RestViewSet):
    lookup_value_regex = '[0-9]+'
