from django.db import models


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
    source = models.CharField(max_length=9, null=True)
    destination = models.CharField(max_length=9, null=True)


class CallEnd(CallRecord):
    '''A call ending record information.
    '''
    pass


class Call(models.Model):
    '''A call representation.
    '''

    start_record = models.OneToOneField(CallStart, on_delete=models.CASCADE)
    end_record = models.OneToOneField(CallEnd, on_delete=models.CASCADE)
    total = models.DecimalField(null=True, decimal_places=2, max_digits=10)

    @property
    def is_completed(self):
        return bool(self.start_record) and bool(self.end_record)
