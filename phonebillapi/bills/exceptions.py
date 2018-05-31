from rest_framework.exceptions import APIException
from rest_framework import status


class BillNotFound(APIException):
    default_detail = 'Bill for this source and period not found.'
    status_code = status.HTTP_404_NOT_FOUND


class BillUpdateOrCreateError(APIException):
    default_detail = 'Could not save bill.'
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
