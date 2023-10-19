from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from uhtred.core.views import ViewSet
from uhtred.core.exceptions import APIError
from uhtred.notify.serializers import EmailDetail
from uhtred.notify.models import Email
from uhtred.core.validators import uuid_regex

from uhtred.notify.tasks import send_newsletter_confirmation_email


class EmailViewSet(ViewSet):

    lookup_field = 'uuid'
    lookup_value_regex = uuid_regex
    serializer_class = EmailDetail

    def create(self, request: Request) -> Response:

        seriaizer = self.serializer_class(
            data=request.data,
            fields=[
                'subscribe_to_all',
                'subscribed_topics',
                'email',
                'name'])
        try:
            email = Email.objects.get(
                email=request.data.get('email', '').lower(),
                verified=False)
        except Email.DoesNotExist:
            pass
        else:
            send_newsletter_confirmation_email(email)
            return Response(status=status.HTTP_204_NO_CONTENT)

        if seriaizer.is_valid(raise_exception=True):
            seriaizer.save()
            return Response(seriaizer.data, status=status.HTTP_201_CREATED)
        raise APIError(_('Some error occurred, try later'))

    @action(
        methods=['PATCH'],
        url_path='verified',
        detail=True)
    def email_verification(self, request: Request, uuid: str) -> Response:
        """"""
        email: Email = self.get_object(uuid)
        if email.email == request.GET.get('email'):
            if not email.verified:
                email.verified = True
                email.save()
                # TODO: send email notification welcome
                return Response(status=status.HTTP_202_ACCEPTED)
            return Response(status=status.HTTP_204_NO_CONTENT)
        raise APIError()

    def delete(self, request: Request, uuid: str) -> Response:
        """"""
        email: Email = self.get_object(uuid)
        if email.email == request.GET.get('email'):
            email.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        raise APIError()

    def get_object(self, uuid: str) -> Email:
        obj = get_object_or_404(Email, uid=uuid)
        self.check_object_permissions(self.request, obj)
        return obj
