from django.db.models import Manager
from django.db import transaction


class CallStartManager(Manager):

    @transaction.atomic
    def create(self, call_id, source, destination):
        '''
        Creates a `CallStart` record and a associated `Call` record.
        Raises Exception if call exists.

        :param call_id: Unique call id
        :param source: Source phone number
        :param call_id: Destination phone number

        :returns: `CallStart` instance
        '''
        from phonebill.models import Call
        if Call.objects.exists(call_id):
            raise Exception('Invalid call id.')
        instance = super().create(
            source=source,
            destination=destination,
        )
        Call.objects.create(
            id=call_id, start_record=instance
        )
        return instance


class CallEndManager(Manager):

    @transaction.atomic
    def create(self, call_id):
        '''
        Creates a `CallEnd` if there's a not completed call with the given id,
        then updates that call with the created object also allowing the save
        method to update the calculated `price`.

        :param call_id: Unique call id

        :returns: `CallEnd` instance
        '''
        from phonebill.models import Call
        try:
            not_completed_call = Call.objects.not_completed(call_id).get()
        except:
            raise Exception('There`s no call to end')
        instance = super().create()
        not_completed_call.end_record = instance
        not_completed_call.save(update_fields=['end_record', 'price'])
        return instance


class CallManager(Manager):

    def _get_period_lookup(self, period):
        period_dt = None
        one_month = None  # TODO: use relativedelta package from dateutil
        return {
            'end_record__timestamp__lt': period_dt + one_month,
            'end_record__timestamp__gte': period_dt,
        } if period_dt else {}

    def get_bill(self, source, period=None):
        '''
        Return a telephone bill of the given `source` at `period`.
        That is, a `Call` queryset with a `total` aggregated field.

        :param source: Source telephone number (subscriber)
        :param period: Year and month of the period (YYYY-MM format)

        :returns: `CallEnd` instance
        '''

        queryset = self.get_queryset()

        # TODO: annotate total bill price
        return queryset.filter(
            start_record__source=source,
            **self.get_period_lookup(period)
        )

    def exists(self, call_id):
        '''
        Returns if `Call` exists.

        :param call_id: Id of the `Call`
        :returns: bool
        '''

        return self.get_queryset().filter(id=call_id).exists()

    def not_completed(self, call_id):
        '''
        Returns a `Call` queryset filtering not completed calls for the
        given id.

        :param call_id: Id of the `Call`
        :returns: A `Call` queryset
        '''
        return self.get_queryset().filter(
            id=call_id, end_record__isnull=True
        )
