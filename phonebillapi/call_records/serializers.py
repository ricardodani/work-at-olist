from datetime import date
from rest_framework.fields import DateField
from rest_framework.serializers import (
    Serializer, ModelSerializer, ValidationError, SerializerMethodField
)
from rest_framework.fields import (
    RegexField, IntegerField, DateTimeField
)
from call_records.models import NotCompletedCall, CompletedCall



_todays_period = date.today().replace(day=1)
PERIOD_FORMAT = '%Y-%m'
PHONE_REGEX = r'^([0-9]){10,11}$'
START, END = 'start', 'end'
RECORD_TYPE_CHOICES = (START, END)


class NotCompletedCallSerializer(ModelSerializer):
    '''
    Serialize a not completed `Call`.
    '''
    class Meta:
        model = NotCompletedCall
        fields = [
            'call_id', 'source', 'destination', 'started_at', 'is_completed'
        ]


class CompletedCallSerializer(ModelSerializer):
    '''
    Serialize a completed `Call`.
    '''
    class Meta:
        model = CompletedCall
        fields = [
            'call_id', 'source', 'destination', 'started_at', 'ended_at',
            'duration', 'price', 'is_completed'
        ]


class CallStartSerializer(Serializer):
    '''
    Serializes a call start payload and returns a new serialized
    `NotCompletedCall`
    if valid input.
    '''

    call_id = IntegerField(required=True)
    source = RegexField(PHONE_REGEX, required=True)
    destination = RegexField(PHONE_REGEX, required=True)
    timestamp = DateTimeField(required=True)

    def save(self):
        '''
        Create with validated data and returns a serialized `NotCompletedCall`.
        '''
        call = NotCompletedCall.objects.create(
            call_id=self.validated_data['call_id'],
            source=self.validated_data['source'],
            destination=self.validated_data['destination'],
            started_at=self.validated_data['timestamp']
        )
        return NotCompletedCallSerializer(call).data


class CallEndSerializer(Serializer):
    '''
    Serializes a call end payload and returns a updated serialized
    `CompletedCall`
    if valid input.
    '''

    call_id = IntegerField(required=True)
    timestamp = DateTimeField(required=True)

    def save(self):
        '''
        Complete with validated data and returns a serialized `CompletedCall`.
        '''
        call = NotCompletedCall.objects.complete(
            call_id=self.validated_data['call_id'],
            ended_at=self.validated_data['timestamp']
        )
        return CompletedCallSerializer(call).data


class BillCompletedCallSerializer(ModelSerializer):
    '''
    Serialize a completed `Call` for the bill serializer.
    '''
    class Meta:
        model = CompletedCall
        fields = [
            'call_id', 'destination', 'started_at', 'ended_at',
            'duration', 'price'
        ]


class BillSerializer(Serializer):
    '''
    Serializes a `CompletedCall` queryset into as a bill.
    '''
    calls = BillCompletedCallSerializer(many=True)
    total = SerializerMethodField()
    period = DateField(format=PERIOD_FORMAT)
    source = RegexField(PHONE_REGEX)

    def get_total(self, obj):
        if obj['calls']:
            return sum(call.price for call in obj['calls'])


class BillInputSerializer(Serializer):
    '''
    Serializes and validate a `Bill` get request.
    '''
    source = RegexField(PHONE_REGEX)
    period = DateField(
        required=False, format=PERIOD_FORMAT, input_formats=[PERIOD_FORMAT],
        default=_todays_period
    )

    def validate_period(self, value):
        if value.day != 1:
            raise ValidationError('Period day should be 1.')
        return value

    def get_bill_data(self):
        calls_queryset = CompletedCall.objects.get_bill_queryset(
            **self.validated_data
        )
        serializer = BillSerializer({
            'calls': calls_queryset,
            'period': self.validated_data['period'],
            'source': self.validated_data['source']
        })
        return serializer.data
