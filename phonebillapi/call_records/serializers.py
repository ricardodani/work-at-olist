from datetime import date
from rest_framework.fields import DateField
from rest_framework.serializers import (
    Serializer, ModelSerializer, ValidationError, SerializerMethodField
)
from rest_framework.fields import (
    RegexField, IntegerField, DateTimeField, ChoiceField
)
from call_records.models import Call, NotCompletedCall, CompletedCall



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
            'call_id', 'source', 'destination', 'started_at',
        ]


class CompletedCallSerializer(ModelSerializer):
    '''
    Serialize a completed `Call`.
    '''
    class Meta:
        model = CompletedCall
        fields = [
            'call_id', 'source', 'destination', 'started_at', 'ended_at',
            'duration', 'price'
        ]


class CallRecordSerializer(Serializer):
    '''
    Serializes, validate and save a `Call` record.
    '''

    RETURN_SERIALIZERS = {
        START: NotCompletedCallSerializer,
        END: CompletedCallSerializer
    }

    record_type = ChoiceField(choices=RECORD_TYPE_CHOICES)
    call_id = IntegerField(required=True)
    source = RegexField(PHONE_REGEX, required=False)
    destination = RegexField(PHONE_REGEX, required=False)
    timestamp = DateTimeField(required=True)

    def validate_start(self):
        '''
        In the case of start record, source and destinations are required.
        '''
        if self.validated_data['record_type'] == START and not all([
                self.validated_data['source'],
                self.validated_data['destination']
        ]):
            raise ValidationError(
                'Source and destination are required on start record.'
            )

    def is_valid(self, *args, **kwargs):
        return super().is_valid(*args, **kwargs) and self.validate_start()

    def _get_return_serializer(self):
        return self.RETURN_SERIALIZERS[self.validated_data['record_type']]

    def save(self):
        '''
        Saves the request.
        '''
        if self.validated_data['record_type'] == START:
            instance = Call.objects.create(
                call_id=self.validated_data['call_id'],
                source=self.validated_data['source'],
                destination=self.validated_data['destination'],
                started_at=self.validated_data['timestamp']
            )

        else:
            instance = NotCompletedCall.objects.complete(
                call_id=self.validated_data['call_id'],
                ended_at=self.validated_data['timestamp']
            )
        return_serializer = self._get_return_serializer()(instance)
        return return_serializer.data


class BillSerializer(Serializer):
    '''
    Serializes a `CompletedCall` queryset into as a bill.
    '''
    calls = CompletedCallSerializer(many=True)
    total = SerializerMethodField()

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
        queryset = CompletedCall.objects.get_bill_queryset(
            **self.validated_data
        )
        serializer = BillSerializer({'calls': queryset})
        return serializer.data
