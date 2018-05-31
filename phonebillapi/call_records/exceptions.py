from rest_framework.exceptions import APIException
from rest_framework import status


class BillSaveError(APIException):
    default_detail = 'Could not save bill.'
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


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


class CouldNotSaveCallIntoBill(APIException):
    default_detail = (
        'Could not save call into bill.'
    )
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
