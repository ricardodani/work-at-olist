from datetime import datetime, time, timedelta
from decimal import Decimal


class CallPriceBaseError(Exception):
    pass


class CallPriceInvalidInputError(CallPriceBaseError):
    message = 'Input types are not valid types.'


class CallPriceStartGtEndError(CallPriceBaseError):
    message = 'End should be greater or equal than start.'


class CallPriceEndInFutureError(CallPriceBaseError):
    message = 'Impossible to calculate calls that end at future.'


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
            raise CallPriceInvalidInputError
        if started_at > ended_at:
            raise CallPriceStartGtEndError
        if ended_at > datetime.now():
            raise CallPriceEndInFutureError
        self.started_at, self.ended_at = started_at, ended_at

    def _calculate_range_price(self, start, end):
        mins = int((end - start).total_seconds() // 60)
        return self.MIN_PRICE * mins

    def _calculate(self, starting_at, subtotal):
        start_reduced = starting_at.replace(
            hour=self.START_REDUCED_TIME.hour,
            minute=self.START_REDUCED_TIME.minute
        )
        end_reduced = starting_at.replace(
            hour=self.END_REDUCED_TIME.hour,
            minute=self.END_REDUCED_TIME.minute
        )
        end_of_day = starting_at.replace(hour=23, minute=59, second=59)

        if starting_at == self.ended_at or self.ended_at < end_reduced:
            return subtotal
        if starting_at < end_reduced < self.ended_at < start_reduced:
            subtotal += self._calculate_range_price(end_reduced, self.ended_at)
        elif starting_at < end_reduced < start_reduced < self.ended_at:
            subtotal += self._calculate_range_price(end_reduced, start_reduced)
        elif end_reduced < starting_at < self.ended_at < start_reduced:
            subtotal += self._calculate_range_price(starting_at, self.ended_at)
        elif end_reduced < starting_at < start_reduced < self.ended_at:
            subtotal += self._calculate_range_price(starting_at, start_reduced)
        if self.ended_at > end_of_day:
            midnight = end_of_day + timedelta(seconds=1)
            days_til_last = (self.ended_at - midnight).days
            if days_til_last:
                subtotal += (
                    days_til_last * self._calculate_range_price(
                        end_reduced, start_reduced
                    )
                )
                last_day_start = self.ended_at.replace(
                    hour=0, minute=0, second=0
                )
                subtotal = self._calculate(last_day_start, subtotal)
            else:
                subtotal = self._calculate(midnight, subtotal)

        return subtotal

    def calculate(self):
        '''Calculate price recursively.
        '''
        if self.started_at == self.ended_at:
            return Decimal('0.00')
        return self._calculate(
            starting_at=self.started_at, subtotal=self.CONN_PRICE
        )
