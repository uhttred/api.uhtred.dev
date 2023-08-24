from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from uhtred.core.views import ViewSet
from uhtred.core.exceptions import APIError

from uhtred.newsletter.serializers import EmailListDetail
from uhtred.newsletter.models import EmailList

    
class EmailListViewSet(ViewSet):

    lookup_field = 'email_id'
    serializer_class = EmailListDetail
    
    def create(self, request: Request) -> Response:

        seriaizer = self.serializer_class(data=request.data)

        if seriaizer.is_valid(raise_exception=True):
            seriaizer.save()
            return Response({
                'detail': _('E-mail %s registered successfully!') % seriaizer.data.get('email')},
                status=status.HTTP_201_CREATED)
        raise APIError(_('Some error occurred, try later'))
    
    def delete(self, request: Request, email_id: int) -> Response:
        obj: EmailList = self.get_object(email_id)
        if (email := request.GET.get('email', '').lower()) and obj.email == email:
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        raise APIError()
    
    def get_object(self, email_id: int) -> EmailList:
        obj = get_object_or_404(EmailList, id=email_id)
        self.check_object_permissions(self.request, obj)
        return obj
