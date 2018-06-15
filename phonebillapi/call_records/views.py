from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework import status
from call_records.serializers import (
    CallStartSerializer, CallEndSerializer, BillInputSerializer
)
from call_records import exceptions


class CallRecordView(APIView):
    '''
    Record start and end call events of a call.

    Method accepted: POST

    There is two types of payloads, start and end:

    Start: \
    {\
        "record_type": "start", \
        "call_id": 42, \
        "source": "11999887766", \
        "destination": "11888221100", \
        "timestamp": "2010-10-01T12:00"\
    }

    End: \
    {\
        "record_type": "end", \
        "call_id": 42, \
        "timestamp": "2010-10-02T02:40"\
    }

    Returns on success:
        Status: 201 Created
        Response body: Call's JSON object
    '''

    http_method_names = ['post']
    record_serializers = {
        'start': CallStartSerializer,
        'end': CallEndSerializer,
    }

    def get_serializer_class(self, request):
        '''
        Return a serializer class depending on the `record_type` attibute
        from posted data.
        '''
        # Note: The reason I don't treat the record types as two different
        # endpoints is just because it's a requirement for the challange,
        # as written in README
        record_type = request.data.get('record_type')
        if record_type not in self.record_serializers:
            raise exceptions.InvalidCallRecordType
        return self.record_serializers[record_type]

    def post(self, request, format=None):
        '''
        Handles post record request.
        '''
        try:
            serializer_class = self.get_serializer_class(request)
            serializer = serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            call_data = serializer.save()
        except APIException as api_exception:
            raise api_exception
        else:
            return Response(
                call_data, status=status.HTTP_201_CREATED
            )


class BillRetrieveView(APIView):
    '''
    Get a phone bill.

    Returns a set of call records of a given `source` at given `period`.
    If `period` is not given, then the actual period is used.

    Method accepted: GET

    GET Params:
        `source`: A telphone in the format 9999999999
        `period`: A year-month representation in the format YYYY-MM

    Returns on success:
        Status: 200 Ok
        Response body: JSON object representing a bill.
    '''

    http_method_names = ['get']

    def get(self, request):
        '''
        Handles get bill request.
        '''
        try:
            serializer = BillInputSerializer(data=self.request.GET)
            serializer.is_valid(raise_exception=True)
            bill_data = serializer.get_bill_data()
        except APIException as api_exception:
            raise api_exception
        else:
            return Response(bill_data)
