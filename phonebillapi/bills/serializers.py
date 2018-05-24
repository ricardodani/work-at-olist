from rest_framework.serializers import Serializer
from rest_framework.fields import DateField, RegexField
from call_records.serializers import PHONE_REGEX
from bills.models import Bill


PERIOD_FORMAT = '%Y-%m'

class BillInputSerializer(Serializer):
    '''
    Serializes, validate a bill request.
    '''
    source = RegexField(PHONE_REGEX)
    period = DateField(format=PERIOD_FORMAT, input_formats=[PERIOD_FORMAT])

    def validate_period(self):
        import ipdb; ipdb.set_trace()
        pass

    def is_valid(self):
        return self.validate_period() and super().is_valid()

    def get_bill(self):
        return Bill.objects.get(
            source=self.data.get('source'),
            period=self.data.get('period')
        )


class BillSerializer(Serializer):
    '''
    Serializes a bill queryset (`Call`s).
    '''
    class Meta:
        model = Bill
        fields = ['source', 'period', 'calls', 'total']
    # source = RegexField(PHONE_REGEX)
    # period = CharField(required=True)
    # total = DecimalField(max_digits=10, decimal_places=2, read_only=True)
    # calls = CompletedCallSerializer(many=True, read_only=True)
