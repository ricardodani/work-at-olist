from rest_framework.serializers import (
    Serializer, ModelSerializer
)
from rest_framework.fields import (
    CharField, DecimalField, RegexField, IntegerField,
    ValidationError, DateTimeField
)
from call_records.models import Call, NotCompletedCall
from call_records.exceptions import CallCreationError


PHONE_REGEX = r'^([0-9]){10,11}$'
PERIOD_REGEX = r'^([0-9]){4}-([0-9]){2}$'


class CallStartCreateSerializer(Serializer):
    '''
    Serializes, validate and save a call start record.
    '''

    source = RegexField(PHONE_REGEX)
    destination = RegexField(PHONE_REGEX)
    call_id = IntegerField(required=True)
    timestamp = DateTimeField(required=True)

    def save(self):
        return Call.objects.create(**self.data)


class CallEndCreateSerializer(Serializer):
    '''
    Serializes, validate and save a call end record.
    '''

    call_id = IntegerField(required=True)
    timestamp = DateTimeField(required=True)

    def validate_call_id(self, value):
        try:
            self.call = NotCompletedCall.objects.get(call_id=value)
            return value
        except NotCompletedCall.DoesNotExists:
            raise ValidationError('There is no call to end.')

    def save(self):
        return NotCompletedCall.objects.complete(
            call_id, ended_atself.data['timestamp']
        )


class BillInputSerializer(Serializer):
    '''
    Serializes, validate a bill request.
    '''
    source = RegexField(PHONE_REGEX)
    period = RegexField(PERIOD_REGEX, required=False)


class CallSerializer(ModelSerializer):
    '''
    Serialize a `Call`.
    '''
    class Meta:
        model = Call
        fields = [
            'destination', 'started_at', 'ended_at', 'duration', 'price'
        ]


class BillSerializer(Serializer):
    '''
    Serializes a bill queryset (`Call`s).
    '''
    source = RegexField(PHONE_REGEX)
    period = CharField(required=True)
    total = DecimalField(max_digits=10, decimal_places=2, read_only=True)
    calls = CallSerializer(many=True, read_only=True)
