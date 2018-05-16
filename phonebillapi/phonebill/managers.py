from dateutil.relativedelta import relativedelta
from django.db.models import Manager
from django.db import transaction
from phonebill import exceptions


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
            raise exceptions.CallExistsError

        try:
            instance = super().create(
                source=source,
                destination=destination,
            )
            Call.objects.create(
                id=call_id, start_record=instance
            )
            return instance

        except:
            raise exceptions.CallStartCreateError


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
        except Call.DoesNotExists:
            raise exceptions.NoCallToEndError

        try:
            instance = super().create()
            not_completed_call.end_record = instance
            not_completed_call.save(update_fields=['end_record', 'price'])
            return instance
        except:
            raise exceptions.CallEndCreateError


class CallManager(Manager):

    def _get_period_lookup(self, period):
        return {
            'end_record__timestamp__lt': period + relativedelta(months=1),
            'end_record__timestamp__gte': period,
        }

    def get_bill(self, source, period):
        '''
        Return a telephone bill of the given `source` at `period`.
        That is, a `Call` queryset with a `total` aggregated field.

        :param source: Source telephone number (subscriber)
        :param period: a validated `date` object

        :returns: A `Call` queryset
        '''

        queryset = self.get_queryset()

        return queryset.filter(
            end_record__isnull=False,
            price__isnull=False,
            start_record__source=source,
            **self._get_period_lookup(period)
        ).select_related(
            'start_record', 'end_record'
        ).order_by(
            'end_record__timestamp'
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
        Filter's for a not completed call.

        :param call_id: Id of the `Call`
        :returns: A `Call` queryset.
        '''
        return self.get_queryset().filter(
            id=call_id, end_record__isnull=True
        )
