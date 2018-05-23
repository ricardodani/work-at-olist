from rest_framework.serializers import Serializer, ModelSerializer
from rest_framework.fields import (
    RegexField, IntegerField, DateTimeField, ChoiceField
)
from call_records.models import Call, NotCompletedCall, CompletedCall
from call_records import exceptions


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

    record_type = ChoiceField(choices=RECORD_TYPE_CHOICES)
    call_id = IntegerField(required=True)
    source = RegexField(PHONE_REGEX)
    destination = RegexField(PHONE_REGEX)
    timestamp = DateTimeField(required=True)

    def validate_record_type(self, value):
        if value not in RECORD_TYPE_CHOICES:
            raise exceptions.InvalidRecordTypeRequestError
        return value

    def save(self):
        '''
        Saves the request.
        '''
        self._record_type = self.data['record_type']
        if self._record_type == START:
            self._object = Call.objects.create(
                call_id=self.data['call_id'],
                source=self.data['source'],
                destination=self.data['destination'],
                started_at=self.data['timestamp']
            )

        elif self._record_type == END:
            self._object = NotCompletedCall.objects.complete(
                call_id=self.data['call_id'],
                ended_at=self.data['timestamp']
            )

    def get_return_serializer(self):
        '''
        Return a Serializer class that intended to serialize the returned
        saved object.
        '''
        if self._record_type == START:
            return NotCompletedCallSerializer(self._object)

        elif self._record_type == END:
            return CompletedCallSerializer(self._object)
