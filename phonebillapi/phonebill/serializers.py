from django.conf import settings
from rest_framework.serializers import (
    Serializer, ValidationError, ModelSerializer
)
from rest_framework.fields import (
    CharField, ListField, DecimalField, RegexField, IntegerField
)
from phonebill.models import Call, CallEnd, CallStart


PERIOD_FORMAT = getattr(settings, "PERIOD_FORMAT", "%Y-%m")
PHONE_REGEX = getattr(settings, "PHONE_REGEX", r'([0-9]){10,11}')


class CallStartSerializer(ModelSerializer):
    source = RegexField(PHONE_REGEX)
    destination = RegexField(PHONE_REGEX)
    call_id = IntegerField(required=True)
    type = CharField(default='start')

    class Meta:
        model = CallStart
        fields = ['source', 'destination', 'call_id', 'type', 'timestamp']
        read_only_fields = ['call_id', 'type', 'timestamp']

    def validate_call_id(self, value):
        if Call.objects.exists(value):
            raise ValidationError('Call already exists.')
        return value

    def save(self, *args, **kwargs):
        start = CallStart.objects.create(
            source=self.validated_data['source'],
            destination=self.validated_data['destination'],
        )
        self.call = Call.objects.create(
            id=self.validated_data['call_id'], start_record=start
        )
        start.refresh_from_db()
        return start


class CallEndSerializer(ModelSerializer):
    call_id = IntegerField(required=True)
    type = CharField(default='end')
    class Meta:
        model = CallEnd
        fields = ['call_id', 'timestamp', 'type']
        read_only_fields = ['call_id']

    def validate_call_id(self, value):
        if not Call.objects.not_completed(value):
            raise ValidationError('Theres no call to end.')
        return value

    def save(self, *args, **kwargs):
        end = CallEnd.objects.create()
        Call.objects.update(end_record=end)
        return end


class CallSerializer(ModelSerializer):
    class Meta:
        model = Call
        fields = [
            'destination', 'started_at', 'ended_at', 'duration', 'price'
        ]


class BillSerializer(Serializer):

    source = RegexField(PHONE_REGEX)
    period = CharField(required=False)
    calls = ListField(CallSerializer)
    total = DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        fields = ['source', 'period', 'calls', 'total']
        read_only_fields = ['calls', 'total']
