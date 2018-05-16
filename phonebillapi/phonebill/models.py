import datetime
from django.db import models
from phonebill.price import CallPrice
from phonebill.managers import CallManager, CallStartManager, CallEndManager


class CallStart(models.Model):
    '''A call start record information.
    '''
    timestamp = models.DateTimeField(
        null=False, verbose_name='Started at', auto_now_add=True
    )
    source = models.CharField(max_length=11, null=False, db_index=True)
    destination = models.CharField(max_length=11, null=False)

    objects = CallStartManager()


class CallEnd(models.Model):
    '''A call ending record information.
    '''
    timestamp = models.DateTimeField(
        null=False, verbose_name='Ended at', auto_now_add=True
    )
    objects = CallEndManager()


class Call(models.Model):
    '''A call representation.
    '''

    start_record = models.OneToOneField(
        CallStart, on_delete=models.CASCADE, null=False, blank=False
    )
    end_record = models.OneToOneField(
        CallEnd, on_delete=models.CASCADE, null=True, blank=True
    )
    price = models.DecimalField(
        null=True, decimal_places=2, max_digits=10, blank=True
    )
    objects = CallManager()

    @property
    def source(self):
        return self.start_record.source

    @property
    def destination(self):
        return self.start_record.destination

    @property
    def started_at(self):
        return self.start_record.timestamp

    @property
    def ended_at(self):
        if self.is_completed:
            return self.end_record.timestamp

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
            total_seconds = (self.ended_at - self.started_at).total_seconds()
            hours = int(total_seconds // 60 // 60)
            minutes = int(total_seconds // 60)
            seconds = int(total_seconds % 60)
            return '{}h{}m{}s'.format(hours, minutes, seconds)

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

    class Meta:
        indexes = [
            models.Index(
                fields=['start_record', 'end_record']
            ),
        ]
