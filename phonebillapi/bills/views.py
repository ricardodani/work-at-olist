from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework.views import APIView
from bills.serializers import BillInputSerializer


class BillRetrieveView(APIView):
    '''
    Get a bill API endpoint. Requires `source` and `period` GET parameters.
    If `period` is not given, then the actual period is used.
    '''

    http_method_names = ['get']

    def get(self, request):
        serializer = BillInputSerializer(data=self.request.GET)
        serializer.is_valid(raise_exception=True)

        try:
            bill_data = serializer.get_serialized_bill()
        except APIException as e:
            return Response(
                dict(detail=e.default_detail), status=e.status_code
            )
        else:
            return Response(bill_data)


