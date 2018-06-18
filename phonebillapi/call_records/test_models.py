import pytz
from datetime import date
from unittest.mock import patch
from django.utils.timezone import datetime
from django.test import TestCase
from call_records.models import Call


class TestCall(TestCase):

    def setUp(self):
        self.started_call = Call.objects.create(
            call_id=1,
            source="21999000000",
            destination="11999000000",
            started_at=datetime(2000, 1, 2, 1, 1, 1, tzinfo=pytz.UTC)
        )
        self.ended_call = Call.objects.create(
            call_id=2,
            source="21999000000",
            destination="11999000000",
            started_at=datetime(2000, 1, 2, 1, 1, 1, tzinfo=pytz.UTC),
            ended_at=datetime(2000, 1, 2, 1, 2, 1, tzinfo=pytz.UTC)
        )

    def test_call_is_completed_property(self):
        self.assertFalse(self.started_call.is_completed)
        self.assertTrue(self.ended_call.is_completed)

    @patch('call_records.models.CallPrice')
    def test_call_set_price_called(self, mocked_call_price):
        self.started_call.set_price()
        self.assertFalse(mocked_call_price.called)
        self.ended_call.set_price()
        self.assertTrue(mocked_call_price.called)

    def test_period_property(self):
        self.assertEqual(self.started_call.period, None)
        self.assertEqual(self.ended_call.period, date(2000, 1, 1))

    def test_duration_property(self):
        self.assertEqual(self.started_call.duration, None)
        self.assertEqual(self.ended_call.duration, '0h01m00s')
