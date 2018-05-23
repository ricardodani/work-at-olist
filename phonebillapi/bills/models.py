from django.db import models
from django.contrib.postgres import fields as pgfields


class Bill(models.Model):
    '''
    Store complete call details and total of a subscriber`s bill from
    a period.
    '''
    source = models.CharField(max_length=11)
    period = models.CharField(max_length=7)
    calls = pgfields.ArrayField(
        pgfields.JSONField(verbose_name='call')
    )
    total = models.DecimalField(decimal_places=2, max_digits=10)

    class Meta:
        indexes = [
            models.Index(fields=['source', 'period']),
        ]
