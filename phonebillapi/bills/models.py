from decimal import Decimal
from django.db import models
from django.contrib.postgres import fields as pgfields
from call_records.models import CompletedCall
from call_records.serializers import CompletedCallSerializer


class Bill(models.Model):
    '''
    Store complete call details and total of a subscriber`s bill from
    a period.
    '''
    source = models.CharField(max_length=11)
    period = models.DateField()  # TODO: Validate if is day 1
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # metadata
    calls = pgfields.ArrayField(
        pgfields.JSONField(verbose_name='call')
    )
    total = models.DecimalField(decimal_places=2, max_digits=10)

    def set_bill_metadata(self):
        '''
        Set's the value of calls and total fetched from call records.
        Invoked on every Bill save.
        '''
        bill_qs = CompletedCall.objects.get_bill_queryset(
            self.source, self.period
        )
        self.total, self.calls = Decimal('0.00'), []
        for call in bill_qs:
            self.calls.append(CompletedCallSerializer(call))
            self.total += call.price  # TODO aggragate total

    class Meta:
        indexes = [
            models.Index(fields=['source', 'period']),
        ]

    def save(self, *args, **kwargs):
        self.set_bill_metadata()
        super().save(*args, **kwargs)
