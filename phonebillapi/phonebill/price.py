from datetime import datetime
from phonebill.utils import in_range


class CallPrice:
    '''Class to calculate call prices based on tariff ranges.
    '''

    STANDARD = 'Standard'
    REDUCED = 'Reduced'
    _START_STANDARD_TIME = datetime.time(hour=6)
    _START_REDUCED_TIME = datetime.time(hour=22)
    _CONN_PRICE_STANDARD = Decimal('0.36')
    _CONN_PRICE_REDUCED = CONN_PRICE_STANDARD
    _MIN_PRICE_STANDARD = Decimal('0.09')
    _MIN_PRICE_REDUCED = None
    TARIFFS = {
        STANDARD: {
            'range': (_START_TIME_STANDARD, _START_REDUCED_TIME),
            'conn_price': _CONN_PRICE_STANDARD,
            'min_price': _MIN_PRICE_STANDARD,
        },
        REDUCED: {
            'range': (_START_TIME_REDUCED, _START_STANDARD_TIME_,
            'conn_price': _CONN_PRICE_REDUCED,
            'min_price': _MIN_PRICE_REDUCED,
        }
    }

    def __init__(self, started_at, ended_at):
        self.started_at, self.ended_at = started_at, ended_at

    def get_tariff(self, time):
        return self.TARIFFS[self.STANDARD] if in_range(
            self.TARIFFS[self.STANDARD]['range'], time
        ) else self.TARIFFS[self.REDUCED]

    def calculate(self, starting_at=None):
        starting_at = self.started_at if not starting_at else starting_at
        tariff = self.get_tariff(starting_at)
        subtotal = tariff['conn_price']
        _, end = tariff['range']
        if tariff['min_price']:
            delta_mins = (end - starting_at).total_minutes()
            subtotal += delta_mins * tariff['min_price']
        subtotal += self.calculate(starting_at=end)
        return subtotal



'''
# get date ranges
>>> split_period(date_1, date_2)
[FirstDay(reduced_mins=X, standard_minutes=Y), MiddleDays(reduced_mins=), ]
