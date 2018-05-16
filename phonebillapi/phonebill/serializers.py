from rest_framework.serializers import (
    Serializer, ModelSerializer
)
from rest_framework.fields import (
    CharField, DecimalField, RegexField, IntegerField,
    ValidationError, SerializerMethodField
)
from phonebill.models import Call, CallStart, CallEnd


PHONE_REGEX = r'^([0-9]){10,11}$'
PERIOD_REGEX = r'^([0-9]){4}-([0-9]){2}$'


class CallStartSerializer(ModelSerializer):
    '''
    Serializes a `CallStart` instance
    '''
    type = SerializerMethodField()

    def get_type(self, obj):
        return 'start'

    class Meta:
        model = CallStart
        fields = ['id', 'timestamp', 'source', 'destination', 'call', 'type']
        read_only_fields = fields


class CallEndSerializer(ModelSerializer):
    '''
    Serializes a CallEnd instance
    '''
    type = SerializerMethodField()

    def get_type(self, obj):
        return 'end'

    class Meta:
        model = CallEnd
        fields = ['id', 'timestamp', 'call', 'type']
        read_only_fields = fields

class CallStartCreateSerializer(Serializer):
    '''
    Serializes, validate and save a `CallStart` creation request.
    '''
    source = RegexField(PHONE_REGEX)
    destination = RegexField(PHONE_REGEX)
    call_id = IntegerField(required=True)
    type = CharField(required=True)

    def validate_type(self, value):
        if value not in ['start', 'end']:
            raise ValidationError(
                detail='Call record type must be `start` or `end`.'
            )
        return value

    def save(self):
        return CallStart.objects.create(
            call_id=self.data['call_id'],
            source=self.data['source'],
            destination=self.data['destination'],
        )


class CallEndCreateSerializer(Serializer):
    '''
    Serializes, validate and save a `CallEnd` creation request.
    '''
    call_id = IntegerField(required=True)
    type = CharField(required=True)

    def save(self):
        return CallEnd.objects.create(call_id=self.data['call_id'])


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
