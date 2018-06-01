from decimal import Decimal
from django.db import models
from bills import exceptions
from call_records.models import CompletedCall


class BillManager(models.Manager):

    def get_bill_serialized_metadata(self, source, period):
        '''
        Returns bill serialized metadata from fetched calls.
        '''
        from bills.serializers import BillMetadataSerializer
        bill_qs = CompletedCall.objects.get_bill_queryset(source, period)

        metadata = {'total': Decimal('0.00'), 'calls': list(bill_qs)}
        for call in metadata['calls']:
            metadata['total'] += call.price

        return BillMetadataSerializer(metadata).data

    def update_or_create(self, source, period, **kwargs):
        '''
        Create a bill if does not exist. Update it if exists.
        '''
        metadata = self.get_bill_serialized_metadata(source, period)
        return super().update_or_create(
            source=source, period=period, defaults={'metadata': metadata}
        )

    def get(self, *args, **kwargs):
        try:
            return super().get(*args, **kwargs)
        except:
            raise exceptions.BillNotFoundError
