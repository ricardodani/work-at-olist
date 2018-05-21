from rest_framework.serializers import (
    Serializer, ModelSerializer
)
from rest_framework.fields import (
    CharField, DecimalField, RegexField, IntegerField,
    ValidationError, DateTimeField
)
from call_records.models import Call, NotCompletedCall


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

    def validate_call_id(self, value):
        if Call.objects.get(call_id=value).exists():
            raise ValidationError('Call already exists.')
        return value

    def save(self):
        return Call.objects.create(
            call_id=self.data['call_id'],
            source=self.data['source'],
            destination=self.data['destination'],
            started_at=self.data['timestamp']
        )


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
        self.call.complete_call(self.data['timestamp'])
        return self.call


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
