from rest_framework.exceptions import APIException
from rest_framework import status


class CallCreationError(APIException):
    default_detail = 'Failed to create call record.'
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


class CallCompletionError(APIException):
    default_detail = 'Failed to complete call record.'
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


class InvalidPeriodDateError(APIException):
    default_detail = 'Invalid period date.'
    status_code = status.HTTP_400_BAD_REQUEST
