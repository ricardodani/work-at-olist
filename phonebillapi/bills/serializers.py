from datetime import date
from rest_framework.serializers import Serializer, ModelSerializer
from rest_framework.serializers import ValidationError
from rest_framework.fields import DateField, RegexField, DecimalField
from call_records.serializers import PHONE_REGEX
from call_records.serializers import CompletedCallSerializer
from bills.models import Bill


_todays_period = date.today().replace(day=1)
PERIOD_FORMAT = '%Y-%m'


class BillSerializer(ModelSerializer):
    '''
    Serializes a `Bill` model instance.
    '''
    class Meta:
        model = Bill
        fields = ['source', 'period', 'metadata']


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

    def get_serialized_bill(self):
        bill = Bill.objects.get(**self.validated_data)
        return BillSerializer(bill)


class BillMetadataSerializer(Serializer):
    calls = CompletedCallSerializer(many=True)
    total = DecimalField(max_digits=10, decimal_places=2)

