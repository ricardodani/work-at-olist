from dateutil.relativedelta import relativedelta
from django.db import models
from call_records.price import CallPrice


class Call(models.Model):
    '''
    A call record metadada.
    '''

    call_id = models.AutoField(primary_key=True)
    started_at = models.DateTimeField(null=False)
    ended_at = models.DateTimeField(null=True, blank=True)
    source = models.CharField(max_length=11, null=False, db_index=True)
    destination = models.CharField(max_length=11, null=True, blank=True)
    price = models.DecimalField(
        null=True, decimal_places=2, max_digits=10, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_completed(self):
        '''Return if the `Call` instance is complete, in other words, has
        start and end records.
        '''
        return all([self.start_record, self.end_record])


class NotCompletedManager(models.Manager):
    '''
    Manager that filters only not completed calls.
    '''
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(
            ended_at__isnull=True
        )


class NotCompletedCall(Call):
    '''
    A call proxy model class for not completed calls.
    '''
    objects = NotCompletedManager()

    def _set_price(self):
        '''Set's the call price when completed.
        '''
        assert self.is_completed, "Call must be completed to set price."
        call_price = CallPrice(
            started_at=self.started_at,
            ended_at=self.ended_at
        )
        self.price = call_price.calculate()

    def complete_call(self, ended_at):
        self.ended_at = ended_at
        self._set_price()
        self.save(update_fields=['ended_at', 'price', 'updated_at'])

    class Meta:
        proxy = True


class CompletedManager(models.Manager):
    '''
    Manager that filters only completed calls.
    '''

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(
            ended_at__isnull=False,
            price__isnull=False
        )

    def _filter_period(self, period):
        period_lookup = {
            'ended_at__lt': period + relativedelta(months=1),
            'ended_at__gte': period,
        }
        return self.get_queryset().filter(**period_lookup)

    def get_bill_queryset(self, source, period):
        return (
            self._filter_period(period).filter(source=source)
            .order_by('-ended_at')
        )


class CompletedCall(Call):
    '''
    A call proxy model class for completed calls.
    '''
    objects = CompletedManager()

    @property
    def duration(self):
        '''Return duration of a call in a human format.
        '''
        total_seconds = (self.ended_at - self.started_at).total_seconds()
        hours = int(total_seconds // 60 // 60)
        minutes = int(total_seconds // 60)
        seconds = int(total_seconds % 60)
        return '{}h{}m{}s'.format(hours, minutes, seconds)

    class Meta:
        proxy = True
