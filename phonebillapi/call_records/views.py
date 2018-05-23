from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework import status
from call_records.serializers import CallRecordSerializer


class CallRecordView(APIView):
    '''
    View to add call record requests, can create or complete a `Call`.
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
