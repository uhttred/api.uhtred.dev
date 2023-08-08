from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import (
    PermissionDenied, NotFound, NotAcceptable, ValidationError,
    NotAuthenticated, MethodNotAllowed, APIException, AuthenticationFailed,
    _get_error_details)


class APIError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Invalid input.')
    default_code = 'invalid'

    def __init__(self, detail=None, code=None, status=None):
        self.status_code = status or self.status_code
        
        if code is None:
            code = self.default_code

        if not isinstance(detail, dict) or detail is None:
            detail = {'detail': detail or self.default_detail}

        # # For validation failures, we may collect many errors together,
        # # so the details should always be coerced to a list if not already.
        if isinstance(detail, tuple):
            detail = list(detail)
        elif not isinstance(detail, dict) and not isinstance(detail, list):
            detail = [detail]

        self.detail = _get_error_details(detail, code)
        