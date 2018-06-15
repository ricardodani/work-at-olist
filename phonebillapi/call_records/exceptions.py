from rest_framework.exceptions import APIException
from rest_framework import status


class CallCreationError(APIException):
    default_detail = 'Failed to create call record.'
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


class CallCompletionError(APIException):
    default_detail = 'Failed to complete call record.'
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


class NoCallToEndError(APIException):
    default_detail = 'There is no call to end'
    status_code = status.HTTP_400_BAD_REQUEST


class CallExistsError(APIException):
    default_detail = 'The call already exists'
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


class CalculatePriceError(APIException):
    default_detail = 'Calculation of the price call failed.'
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


class BillNotFoundError(APIException):
    default_detail = 'No bill found.'
    status_code = status.HTTP_404_NOT_FOUND


class InvalidCallRecordType(APIException):
    default_detail = 'Invalid call record type, choices are "start" and "end"'
    status_code = status.HTTP_400_BAD_REQUEST
