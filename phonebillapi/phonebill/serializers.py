from django.conf import settings
from rest_framework.serializers import (
    Serializer, ValidationError, ModelSerializer
)
from rest_framework.fields import (
    CharField, ListField, DecimalField, RegexField, IntegerField
)
from phonebill.models import Call, CallEnd, CallStart


PHONE_REGEX = getattr(settings, "PHONE_REGEX", r'([0-9]){10,11}')


class CallStartSerializer(ModelSerializer):
    source = RegexField(PHONE_REGEX)
    destination = RegexField(PHONE_REGEX)
    call_id = IntegerField(required=True)
    type = CharField(required=True)

    class Meta:
        model = CallStart
        fields = ['source', 'destination', 'call_id', 'type', 'timestamp']
        read_only_fields = ['call_id', 'type', 'timestamp']

    def save(self, *args, **kwargs):
        try:
            return CallStart.objects.create(
                call_id=self.validated_data['call_id'],
                source=self.validated_data['source'],
                destination=self.validated_data['destination'],
            )
        except Exception as e:
            raise ValidationError(e)


class CallEndSerializer(ModelSerializer):
    call_id = IntegerField(required=True)
    type = CharField(required=True)

    class Meta:
        model = CallEnd
        fields = ['call_id', 'timestamp', 'type']
        read_only_fields = ['call_id']

    def save(self, *args, **kwargs):
        try:
            return CallEnd.objects.create(
                call_id=self.validated_data['call_id']
            )
        except Exception as e:
            raise ValidationError(e)


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
