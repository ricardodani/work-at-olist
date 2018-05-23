from datetime import datetime, date
from django.shortcuts import render
from django.urls import reverse
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework import status
from call_records.serializers import (
    CallStartSerializer, CallEndSerializer,CallSerializer, BillInputSerializer,
    BillSerializer
)


class CallRecordView(GenericAPIView):
    '''
    Post a call record API endpoint. Accept's start and end records types.
    '''

    http_method_names = ['post']
    serializers = {
        'start': CallStartSerializer,
        'end': CallEndSerializer,
    }
    default_serializer = 'start'

    def get_serializer_class(self):
        _type = self.request.data.get('type')
        return (
            self.serializers[_type] if _type in self.serializers.keys()
            else self.default_serializer
        )

    def post(self, request, format=None):
        '''
        Handle a post request to register a phone call, act`s as a serializer
        router depending on `type` attribute.
        '''
        serializer = self.get_serializer_class()(data=request.data)

        if not serializer.is_valid():
            return Response(
                dict(errors=serializer.errors),
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            call = serializer.save()
        except APIException as err:
            return Response(
                dict(detail=err.default), status=err.status_code
            )

        call_serializer = CallSerializer(call)
        return Response(
            call_serializer.data, status=status.HTTP_201_CREATED
        )
