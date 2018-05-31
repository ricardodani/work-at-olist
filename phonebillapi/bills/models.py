from django.db import models
from django.contrib.postgres.fields import JSONField


class Bill(models.Model):
    '''
    Store complete call details and total of a subscriber`s bill from
    a period.
    '''
    source = models.CharField(max_length=11)
    period = models.DateField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    metadata = JSONField(verbose_name='bill metadata')

    class Meta:
        indexes = [
            models.Index(fields=['source', 'period']),
        ]
