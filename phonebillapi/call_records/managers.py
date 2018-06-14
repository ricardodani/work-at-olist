from dateutil.relativedelta import relativedelta
from django.db import models
from call_records import exceptions


class NotCompletedCallManager(models.Manager):
    '''
    Manager that filters only not completed calls.
    '''
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(
            ended_at__isnull=True
        )

    def create(self, call_id, source, destination, started_at):
        '''
        Create a call if does not exists.
        '''
        if super().get_queryset().filter(call_id=call_id).exists():
            raise exceptions.CallExistsError

        try:
            return super().create(
                call_id=call_id, source=source, destination=destination,
                started_at=started_at
            )
        except:
            raise exceptions.CallCreationError

    def complete(self, call_id, ended_at):
        '''
        Complete a not completed call calculating it`s price and return it.
        '''
        try:
            call = self.get_queryset().get(call_id=call_id)
        except:
            raise exceptions.NoCallToEndError

        call.ended_at = ended_at
        try:
            call.set_price()
        except:
            raise exceptions.CalculatePriceError

        try:
            call.save(update_fields=['ended_at', 'price', 'updated_at'])
        except:
            raise exceptions.CallCompletionError

        return call


class CompletedCallManager(models.Manager):
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
        '''
        Returns a bill queryset, in other words, completed calls from a source
        filtered by a period.
        '''
        calls = (
            self._filter_period(period).filter(source=source)
            .order_by('-ended_at')
        )
        if not calls.exists():
            raise exceptions.BillNotFoundError
        return calls

    def create(self, *args, **kwargs):
        raise NotImplementedError
