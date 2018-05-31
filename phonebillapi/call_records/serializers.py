from rest_framework.serializers import (
    Serializer, ModelSerializer, ValidationError
)
from rest_framework.fields import (
    RegexField, IntegerField, DateTimeField, ChoiceField
)
from call_records.models import Call, NotCompletedCall, CompletedCall


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

    def save(self):
        '''
        Saves the request.
        '''
        if self.validated_data['record_type'] == START:
            return Call.objects.create(
                call_id=self.validated_data['call_id'],
                source=self.validated_data['source'],
                destination=self.validated_data['destination'],
                started_at=self.validated_data['timestamp']
            )

        else:
            return NotCompletedCall.objects.complete(
                call_id=self.validated_data['call_id'],
                ended_at=self.validated_data['timestamp']
            )

    def get_return_serializer(self):
        return self.RETURN_SERIALIZERS[self.validated_data['record_type']]
