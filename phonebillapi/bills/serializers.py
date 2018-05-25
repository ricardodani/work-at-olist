from rest_framework.serializers import Serializer, ModelSerializer
from rest_framework.serializers import ValidationError
from rest_framework.fields import DateField, RegexField
from call_records.serializers import PHONE_REGEX
from bills.models import Bill
from bills import exceptions


PERIOD_FORMAT = '%Y-%m'

class BillInputSerializer(Serializer):
    '''
    Serializes, validate a bill request.
    '''
    source = RegexField(PHONE_REGEX)
    period = DateField(
        required=False, format=PERIOD_FORMAT, input_formats=[PERIOD_FORMAT]
    )

    def validate_period(self, value):
        if value.day != 1:
            raise ValidationError('Period day should be 1.')
        return value

    def get_bill(self):
        try:
            return Bill.objects.get(
                source=self.validated_data['source'],
                period=self.validated_data['period']
            )
        except Bill.DoesNotExist:
            raise exceptions.BillNotFound


class BillSerializer(ModelSerializer):
    '''
    Serializes a bill queryset (`Call`s).
    '''
    class Meta:
        model = Bill
        fields = ['source', 'period', 'calls', 'total']
