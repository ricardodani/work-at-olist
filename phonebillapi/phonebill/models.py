import datetime
from django.db import models
from phonebill.pricing import PricingRule


class CallRecordManager(models.Manager):
    pass


class CallRecord(models.Model):
    timestamp = models.DateTimeField(null=False)
    objects = CallRecordManager()
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


class CallPrice:

    STANDARD_TIME_RANGE = ()

class Call(models.Model):
    '''A call representation.
    '''

    start_record = models.OneToOneField(CallStart, on_delete=models.CASCADE)
    end_record = models.OneToOneField(CallEnd, on_delete=models.CASCADE)
    total = models.DecimalField(null=True, decimal_places=2, max_digits=10)

    @property
    def is_completed(self):
        return bool(self.start_record) and bool(self.end_record)

    @property
    def duration(self):
        if self.is_completed:
            return self.end_record.timestamp - self.start_record.timestamp

    @property
    def price(self):
        if self.is_completed:
            return CallPrice.calculate(
                started_at=self.start_record.timestamp,
                started_at=self.start_record.timestamp,
                started_at=self.start_record.timestamp,
            )

    def _set_total(self):
        '''Set the calculated total price of a the call if possible.
        '''
        should_calculate_total = not self.total and not self.is_completed
        if should_calculate_total:
            self.total = self.pricing.calculate(self)

    def save(self, *args, **kwargs):
        self._set_total()
        super().save(*args, **kwargs)
