from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework import status
from call_records.serializers import CallRecordSerializer


class CallRecordView(APIView):
    '''
    Save start and end call records (POST). Examples:

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
    '''

    http_method_names = ['post']

    def post(self, request, format=None):
        try:
            serializer = CallRecordSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except APIException as err:
            raise err
        else:
            return_serializer = serializer.get_return_serializer()
            return Response(
                return_serializer.data, status=status.HTTP_201_CREATED
            )
