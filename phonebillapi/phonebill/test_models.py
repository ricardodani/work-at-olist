import pytz
from unittest.mock import patch, Mock
from decimal import Decimal
from django.utils.timezone import datetime, timedelta
from django.test import TestCase
from phonebill.models import Call, CallStart, CallEnd


class TestCall(TestCase):

    def setUp(self):
        self.call_start = CallStart.objects.create(
            timestamp=datetime(2000, 1, 1, 1, 1, 1, tzinfo=pytz.UTC)
        )
        self.call_end = CallEnd.objects.create(
            timestamp=datetime(2000, 1, 2, 1, 1, 1, tzinfo=pytz.UTC)
        )
        self.call = Call.objects.create(start_record=self.call_start)

    def test_is_completed_property(self):
        self.assertEqual(self.call.is_completed, False)
        self.call.end_record = self.call_end
        self.assertEqual(self.call.is_completed, True)

    def test_duration_property(self):
        self.assertEqual(self.call.duration, None)
        self.call.end_record = self.call_end
        self.assertEqual(self.call.duration, timedelta(days=1))

    @patch('phonebill.models.CallPrice')
    def test_save_sets_price(self, call_price_mock):
        call_price_mock.return_value = Mock(calculate=Mock(
            return_value=Decimal('1.00')
        ))
        self.assertEqual(self.call.price, None)
        self.call.end_record = self.call_end
        self.call.save()
        self.assertEqual(call_price_mock.called, True)
        self.call.save()
        self.assertEqual(call_price_mock.call_count, 1)
        self.assertEqual(self.call.price, Decimal('1.00'))
