import pytz
from datetime import timedelta
from decimal import Decimal
from django.test import TestCase
from django.utils import timezone
from django.utils.timezone import datetime
from call_records.price import (
    CallPrice, CallPriceInvalidInputError, CallPriceStartGtEndError,
    CallPriceEndInFutureError
)


class TestCallPrice(TestCase):

    def test_invalid_types_raises_type_error(self):
        test_cases = (
            {'started_at': None, 'ended_at': None},
            {'started_at': datetime(2010, 10, 10, 1, 1, 1, tzinfo=pytz.UTC),
             'ended_at': None},
            {'started_at': None,
             'ended_at': datetime(2010, 10, 10, 1, 1, 1, tzinfo=pytz.UTC)},
            {'started_at': 2, 'ended_at': 1},
            {'started_at': "1", 'ended_at': "2"},
        )
        for tc in test_cases:
            self.assertRaises(CallPriceInvalidInputError, CallPrice, **tc)

    def test_start_grater_than_end_raises_value_error(self):
        test_cases = (
            {
                'started_at': datetime(2011, 11, 11, 2, 2, 2, tzinfo=pytz.UTC),
                'ended_at': datetime(2010, 10, 10, 1, 1, 1, tzinfo=pytz.UTC)
            },
            {
                'started_at': datetime(2010, 10, 10, 1, 1, 2, tzinfo=pytz.UTC),
                'ended_at': datetime(2010, 10, 10, 1, 1, 1, tzinfo=pytz.UTC)
            },
        )
        for tc in test_cases:
            self.assertRaises(CallPriceStartGtEndError, CallPrice, **tc)

    def test_start_in_future_raises_value_error(self):
        start = timezone.now() + timedelta(seconds=1)
        end = timezone.now() + timedelta(seconds=10)
        self.assertRaises(
            CallPriceEndInFutureError, CallPrice, started_at=start,
            ended_at=end
        )

    def test_calculate_equal_values_return_zero(self):
        ds = de = datetime(2011, 11, 11, 2, 2, 2, tzinfo=pytz.UTC)
        cp = CallPrice(started_at=ds, ended_at=de)
        self.assertEqual(cp.calculate(), Decimal('0.00'))

    def test_calculate_reduced_short_call(self):
        ds = datetime(2010, 1, 1, 22, 30, 0, tzinfo=pytz.UTC)
        de = datetime(2010, 1, 1, 22, 33, 0, tzinfo=pytz.UTC)
        cp = CallPrice(started_at=ds, ended_at=de)
        expected = Decimal('0.36')
        self.assertEqual(cp.calculate(), expected)

    def test_calculate_standard_short_call(self):
        ds = datetime(2010, 1, 1, 20, 30, 0, tzinfo=pytz.UTC)
        de = datetime(2010, 1, 1, 20, 33, 0, tzinfo=pytz.UTC)
        cp = CallPrice(started_at=ds, ended_at=de)
        expected = Decimal('0.36') + (3 * Decimal('0.09'))
        self.assertEqual(cp.calculate(), expected)

    def test_calculate_mixed_short_call(self):
        ds = datetime(2010, 1, 1, 21, 30, 0, tzinfo=pytz.UTC)
        de = datetime(2010, 1, 1, 22, 3, 0, tzinfo=pytz.UTC)
        cp = CallPrice(started_at=ds, ended_at=de)
        expected = Decimal('0.36') + (30 * Decimal('0.09'))
        self.assertEqual(cp.calculate(), expected)

    def test_calculate_mixed_long_call_pass_midnight(self):
        ds = datetime(2010, 1, 1, 21, 30, 0, tzinfo=pytz.UTC)
        de = datetime(2010, 1, 2, 2, 30, 0, tzinfo=pytz.UTC)
        cp = CallPrice(started_at=ds, ended_at=de)
        expected = Decimal('0.36') + (30 * Decimal('0.09'))
        self.assertEqual(cp.calculate(), expected)

    def test_calculate_mixed_long_call_ending_day_after_as_standard(self):
        ds = datetime(2010, 1, 1, 21, 30, 0, tzinfo=pytz.UTC)
        de = datetime(2010, 1, 2, 6, 30, 0, tzinfo=pytz.UTC)
        cp = CallPrice(started_at=ds, ended_at=de)
        expected = Decimal('0.36') + (2 * (30 * Decimal('0.09')))
        self.assertEqual(cp.calculate(), expected)

    def test_calculate_mixed_long_call_end_two_day_after(self):
        ds = datetime(2010, 1, 1, 21, 30, 0, tzinfo=pytz.UTC)
        de = datetime(2010, 1, 3, 6, 30, 0, tzinfo=pytz.UTC)
        cp = CallPrice(started_at=ds, ended_at=de)
        expected = (
            Decimal('0.36')  # call
            + (60 * Decimal('0.09'))  # first and last day
            + (16 * 60 * Decimal('0.09'))  # middle day
        )
        self.assertEqual(cp.calculate(), expected)

    def test_calculate_mixed_long_call_end_two_year_after(self):
        ds = datetime(2010, 1, 1, 21, 30, 0, tzinfo=pytz.UTC)
        de = datetime(2012, 1, 2, 6, 30, 0, tzinfo=pytz.UTC)
        cp = CallPrice(started_at=ds, ended_at=de)
        expected = (
            Decimal('0.36')  # call
            + (60 * Decimal('0.09'))  # first and last day
            + (2 * 365 * 16 * 60 * Decimal('0.09'))  # two years
        )
        self.assertEqual(cp.calculate(), expected)
