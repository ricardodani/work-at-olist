from decimal import Decimal
from django.db import models
from bills.serializers import BillMetadataSerializer
from call_records.models import CompletedCall


class BillManager(models.Manager):

    def get_bill_serialized_metadata(self, source, period):
        '''
        Returns bill serialized metadata from fetched calls.
        '''
        bill_qs = CompletedCall.objects.get_bill_queryset(source, period)

        metadata = {'total': Decimal('0.00'), 'calls': list(bill_qs)}
        for call in metadata['calls']:
            metadata['total'] += call

        return BillMetadataSerializer(metadata).data

    def update_or_create(self, source, period, **kwargs):
        '''
        Create a bill if does not exist. Update it if exists.
        '''
        return super().update_or_create(
            source=source,
            period=period,
            defaults={
                'metadata': self.get_bill_serialized_metadata(
                    source, period
                )
            },
            **kwargs
        )
