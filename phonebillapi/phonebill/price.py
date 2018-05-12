from datetime import datetime, time
from decimal import Decimal


class CallPrice(object):
    '''Class to calculate call prices based on tariff ranges.
    '''

    START_REDUCED_TIME = time(hour=22)
    END_REDUCED_TIME = time(hour=6)
    CONN_PRICE = Decimal('0.36')
    MIN_PRICE = Decimal('0.09')

    def __init__(self, started_at, ended_at):
        invalid_types = not (
            isinstance(started_at, datetime) and isinstance(ended_at, datetime)
        )
        if invalid_types:
            raise TypeError
        start_is_in_future = started_at > ended_at
        if start_is_in_future:
            raise ValueError
        self.started_at, self.ended_at = started_at, ended_at

    def calculate(self):
        subtotal = Decimal('0.00')
        if self.started_at == self.ended_at:
            return subtotal
        subtotal += self.CONN_PRICE
        start_reduced = self.started_at.replace(
            hour=self.START_REDUCED_TIME.hour,
            minute=self.START_REDUCED_TIME.minute
        )
        end_reduced = self.started_at.replace(
            hour=self.END_REDUCED_TIME.hour,
            minute=self.END_REDUCED_TIME.minute
        )
        if self.started_at < self.ended_at < start_reduced:
            mins = int((self.ended_at - self.started_at).total_seconds() // 60)
            subtotal += self.MIN_PRICE * mins
        elif self.started_at < start_reduced < self.ended_at:
            mins = int((start_reduced - self.started_at).total_seconds() // 60)
            subtotal += self.MIN_PRICE * mins
        return subtotal
