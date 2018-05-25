from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework.views import APIView
from rest_framework import status
from bills.serializers import BillInputSerializer, BillSerializer


class BillRetrieveView(APIView):
    '''
    Get a bill API endpoint. Requires `source` and `period` GET parameters.
    If `period` is not given, then the actual period is used.
    '''

    http_method_names = ['get']

    def get(self, request):
        serializer = BillInputSerializer(data=self.request.GET)

        if not serializer.is_valid():
            return Response(
                dict(errors=serializer.errors),
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            bill = serializer.get_bill()
        except APIException as e:
            return Response(
                dict(detail=e.default_detail), status=e.status_code
            )

        bill_serializer = BillSerializer(bill)
        return Response(bill_serializer.data)


