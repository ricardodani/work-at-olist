from datetime import datetime, date
from collections import namedtuple
from django.shortcuts import render
from django.urls import reverse
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework import status
from phonebill.serializers import (
    CallStartCreateSerializer, CallEndCreateSerializer, CallStartSerializer,
    CallEndSerializer, BillSerializer, BillInputSerializer
)
from phonebill.models import Call
from phonebill import exceptions


class CallRecordCreateView(GenericAPIView):
    '''
    Post a call record API endpoint. Accept's start and end records types.
    '''

    http_method_names = ['post']
    serializers = {
        'start': {
            'create': CallStartCreateSerializer,
            'retrieve': CallStartSerializer,
        },
        'end': {
            'create': CallEndCreateSerializer,
            'retrieve': CallEndSerializer,
        },
    }
    default_serializer = 'start'

    @property
    def record_type(self):
        _type = self.request.data.get('type')
        return (
            _type if _type in self.serializers.keys()
            else self.default_serializer
        )

    def get_serializer_class(self):
        return self.serializers[self.record_type]['create']

    def get_retrieve_serializer_class(self):
        return self.serializers[self.record_type]['retrieve']

    def post(self, request, format=None):
        input_serializer = self.get_serializer_class()(data=request.data)

        if not input_serializer.is_valid():
            return Response(
                dict(errors=input_serializer.errors),
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            instance = input_serializer.save()
        except APIException as e:
            return Response(
                dict(detail=e.default), status=e.status_code
            )

        retrieve_serializer = (
            self.get_retrieve_serializer_class()(instance=instance)
        )
        return Response(
            retrieve_serializer.data, status=status.HTTP_201_CREATED
        )


class BillRetrieveView(GenericAPIView):
    '''
    Get a bill API endpoint. Requires `source` and `period` GET parameters.
    If `period` is not given, then the actual period is used.
    '''

    http_method_names = ['get']
    serializer_class = BillInputSerializer

    @staticmethod
    def get_period(period):
        '''
        Return a `date` of the period or a `date` of today`s month if period is
        is None.
        Raises exception if period is invalid.
        '''
        if period:
            try:
                return datetime.strptime(period, '%Y-%m').date()
            except:
                raise exceptions.InvalidPeriodDateError
        return date.today().replace(day=1)

    def get(self, request):
        serializer = BillInputSerializer(data=self.request.GET)

        if not serializer.is_valid():
            return Response(
                dict(errors=serializer.errors),
                status=status.HTTP_400_BAD_REQUEST
            )

        source = serializer.data.get('source')
        try:
            period = self.get_period(serializer.data.get('period'))
            bill_queryset = Call.objects.get_bill(source, period)
        except APIException as e:
            return Response(
                dict(detail=e.default_detail), status=e.status_code
            )

        result_serializer = BillSerializer(dict(
            calls=bill_queryset,
            total=sum(
                call.price for call in bill_queryset if call.price
            ),
            period=period.strftime('%Y-%m'),
            source=source
        ))
        return Response(result_serializer.data)


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
