import datetime
from django.db import models
from phonebill.price import CallPrice


class CallRecord(models.Model):
    timestamp = models.DateTimeField(null=False)
    class Meta:
        abstract = True


class CallStart(CallRecord):
    '''A call start record information.
    '''
    source = models.CharField(max_length=9, null=False, db_index=True)
    destination = models.CharField(max_length=9, null=False)


class CallEnd(CallRecord):
    '''A call ending record information.
    '''
    pass


class Call(models.Model):
    '''A call representation.
    '''

    start_record = models.OneToOneField(
        CallStart, on_delete=models.CASCADE, null=False
    )
    end_record = models.OneToOneField(
        CallEnd, on_delete=models.CASCADE, null=True
    )
    price = models.DecimalField(null=True, decimal_places=2, max_digits=10)

    @property
    def is_completed(self):
        '''Return if the `Call` instance is complete, in other words, has
        start and end records.
        '''
        return all([self.start_record, self.end_record])

    @property
    def duration(self):
        '''Return the timedelta between end and start records if the call is
        completed.
        '''
        if self.is_completed:
            return self.end_record.timestamp - self.start_record.timestamp

    def _set_price(self):
        '''Set's the call price if it's null and the call is completed.
        '''
        if self.is_completed and not self.price:
            call_price = CallPrice(
                started_at=self.start_record.timestamp,
                ended_at=self.end_record.timestamp
            )
            self.price = call_price.calculate()

    def save(self, *args, **kwargs):
        self._set_price()
        super().save(*args, **kwargs)
