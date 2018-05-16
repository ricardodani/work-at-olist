from rest_framework.exceptions import APIException
from rest_framework import status


class CallExistsError(APIException):
    default_detail = 'Call with this `id` already exists.'
    status_code = status.HTTP_400_BAD_REQUEST


class CallStartCreateError(APIException):
    default_detail = 'Failed to create Call start record.'
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


class NoCallToEndError(APIException):
    default_detail = 'There is no call to end.'
    status_code = status.HTTP_400_BAD_REQUEST


class CallEndCreateError(APIException):
    default_detail = 'Failed to create Call end record.'
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


class InvalidPeriodDateError(APIException):
    default_detail = 'Invalid period date.'
    status_code = status.HTTP_400_BAD_REQUEST
