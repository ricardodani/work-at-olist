from rest_framework.exceptions import APIException
from rest_framework import status


class InvalidPeriodDateError(APIException):
    default_detail = 'Invalid period date.'
    status_code = status.HTTP_400_BAD_REQUEST
