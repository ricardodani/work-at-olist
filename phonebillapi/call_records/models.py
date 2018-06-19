from django.db import models
from call_records.price import CallPrice
from call_records.managers import (
    CompletedCallManager, NotCompletedCallManager
)


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

    def _date_range(self):
        return (self.started_at, self.ended_at)

    @property
    def is_completed(self):
        '''Return if the `Call` instance is complete, in other words, has
        start and end records.
        '''
        return all(self._date_range())

    def set_price(self):
        '''Set's the call price when completed.
        '''
        if self.is_completed:
            call_price = CallPrice(*self._date_range())
            self.price = call_price.calculate()

    @property
    def period(self):
        if self.is_completed:
            return self.ended_at.date().replace(day=1)

    @property
    def duration(self):
        '''Return duration of a call in a human format.
        '''
        if self.is_completed:
            delta = (self.ended_at - self.started_at)
            hours, minutes, seconds = str(delta).split(':')
            return '{}h{}m{}s'.format(hours, minutes, seconds)


class NotCompletedCall(Call):
    '''
    A call proxy model class for not completed calls.
    '''
    objects = NotCompletedCallManager()
    class Meta:
        proxy = True


class CompletedCall(Call):
    '''
    A call proxy model class for completed calls.
    '''
    objects = CompletedCallManager()
    class Meta:
        proxy = True
