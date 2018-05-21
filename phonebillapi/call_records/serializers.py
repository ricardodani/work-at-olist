from rest_framework.serializers import (
    Serializer, ModelSerializer
)
from rest_framework.fields import (
    CharField, DecimalField, RegexField, IntegerField, DateTimeField
)
from call_records.models import Call, NotCompletedCall, CompletedCall


PHONE_REGEX = r'^([0-9]){10,11}$'
PERIOD_REGEX = r'^([0-9]){4}-([0-9]){2}$'


class CallStartSerializer(Serializer):
    '''
    Serializes, validate and save a call start record.
    '''

    source = RegexField(PHONE_REGEX)
    destination = RegexField(PHONE_REGEX)
    call_id = IntegerField(required=True)
    timestamp = DateTimeField(required=True)

    def save(self):
        return Call.objects.create(**self.data)


class CallEndSerializer(Serializer):
    '''
    Serializes, validate and save a call end record.
    '''

    call_id = IntegerField(required=True)
    timestamp = DateTimeField(required=True)

    def save(self):
        return NotCompletedCall.objects.complete(**self.data)


class CallSerializer(ModelSerializer):
    '''
    Serializes a call post record.
    '''
    class Meta:
        model = Call
        fields = [
            'call_id', 'started_at', 'ended_at', 'source', 'destination'
        ]


class BillInputSerializer(Serializer):
    '''
    Serializes, validate a bill request.
    '''
    source = RegexField(PHONE_REGEX)
    period = RegexField(PERIOD_REGEX, required=False)


class BillCallSerializer(ModelSerializer):
    '''
    Serialize a completed `Call` for a bill.
    '''
    class Meta:
        model = CompletedCall
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
    calls = BillCallSerializer(many=True, read_only=True)
