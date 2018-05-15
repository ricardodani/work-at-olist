from collections import namedtuple
from django.conf import settings
from django.shortcuts import render
from django.urls import reverse
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.response import Response
from phonebill.serializers import (
    CallStartSerializer, CallEndSerializer, BillSerializer
)
from phonebill.models import Call


class CallRecordCreateView(CreateAPIView):
    '''
    Post a call record API endpoint. Accept's start and end records payloads.
    '''

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
    '''
    Get a bill API endpoint.
    '''

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


def index(request):
    '''
    Show`s project sitemap.
    '''
    Link = namedtuple('Link', ['url', 'name', 'staff_only'])
    return render(request, 'index.html', {
        'links': (
            Link(reverse('admin:index'), 'Admin', True),
            Link("/docs", 'Documentation', False),
            Link(reverse('get-bill'), 'Get a Bill API', False),
            Link(reverse('add-record'), 'Post a Call Record API', False),
        )
    })
