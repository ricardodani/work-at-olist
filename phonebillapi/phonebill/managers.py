from django.db.models import Manager


class CallStartManager(Manager):
    def create(self, call_id, source, destination):
        from phonebill.models import Call
        instance = super().create(
            source=source,
            destination=destination,
        )
        Call.objects.create(
            id=call_id, start_record=instance
        )
        return instance


class CallEndManager(Manager):
    pass


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
        Return a telephone bill queryset, that is,
        a `Call` queryset from a `source` telephone in 
        deterined `period` (or the last).
        The queryset`s also agreggate the total price of the bill on the
        query field `total`
        '''
        queryset = self.get_queryset()

        return queryset.filter(
            start_record__source=source,
            **self.get_period_lookup(period)
        )
        # TODO: annotate total bill price

    def exists(self, call_id):
        return self.get_queryset().filter(id=call_id).exists()

    def not_completed(self, call_id):
        return self.get_queryset().filter(
            id=call_id, end_record__isnull=True
        ).exists()
