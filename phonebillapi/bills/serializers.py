from datetime import datetime, date
from rest_framework.serializers import Serializer
from rest_framework.fields import CharField, DecimalField, RegexField
from call_records.models import CompletedCall
from call_records.serializers import CompletedCallSerializer, PHONE_REGEX
from bills import exceptions


PERIOD_FORMAT = '%Y-%m'

class BillInputSerializer(Serializer):
    '''
    Serializes, validate a bill request.
    '''
    source = RegexField(PHONE_REGEX)
    period = CharField(required=False)

    def is_valid(self):
        import ipdb; ipdb.set_trace()
        if value:
            try:
                return datetime.strptime(value, PERIOD_FORMAT).date()
            except:
                raise exceptions.InvalidPeriodDateError
        return date.today().replace(day=1)

    def get_bill(self):
        return CompletedCall.objects.get_bill_queryset(
            source=self.data.get('source'),
            period=self.data.get('period')
        )

    def get_period(self):
        return self.data['period'].strftime(PERIOD_FORMAT)


class BillSerializer(Serializer):
    '''
    Serializes a bill queryset (`Call`s).
    '''
    source = RegexField(PHONE_REGEX)
    period = CharField(required=True)
    total = DecimalField(max_digits=10, decimal_places=2, read_only=True)
    calls = CompletedCallSerializer(many=True, read_only=True)
