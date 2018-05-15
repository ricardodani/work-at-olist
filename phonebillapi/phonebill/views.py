from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.response import Response
from phonebill.serializers import (
    CallStartSerializer, CallEndSerializer, BillSerializer
)
from phonebill.models import Call


class CallRecordCreateView(CreateAPIView):

    http_method_names = ['post']
    serializers = {
        'start': CallStartSerializer,
        'end': CallEndSerializer
    }
    default_serializer = 'start'

    def get_serializer_class(self):
        try:
            record_type = self.request.data.get('type')
            return self.serializers[record_type]
        except KeyError:
            return self.serializers[self.default_serializer]


class BillRetrieveView(GenericAPIView):

    http_method_names = ['get']

    def get_params(self):
        pass

    def get_queryset(self, request):
        params = self.get_params(request)
        return Call.objects.get_bill(
            source=params['source'], period=params['period']
        )

    def get(self, request):
        serializer = BillSerializer(self.get_queryset())
        return Response(serializer.data)
