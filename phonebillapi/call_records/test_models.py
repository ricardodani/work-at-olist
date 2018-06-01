from datetime import datetime, date
from unittest.mock import patch, Mock
from decimal import Decimal
from django.utils.timezone import datetime, timedelta
from django.test import TestCase
from phonebill.models import Call, CallStart, CallEnd


class TestCall(TestCase):

    def setUp(self):
        self.call = Call.objects.create(
            call_id=1,
            source="21999000000",
            destination="11999000000",
            started_at=datetime(2000, 1, 2, 1, 1, 1, tzinfo=tz.UTC)
        )

    def test_can_create_inexistent_call(self):
        self.assertEqual(self.call.pk, 1)

    def test_cannot_create_existent_call(self):
        with self.assertRaises(exceptions.CallExistsError):
            Call.objects.create(
                call_id=self.call.pk,
                source="21999000000",
                destination="11999000000",
                started_at=datetime(2000, 1, 2, 1, 1, 1, tzinfo=tz.UTC)
            )
    def test_can_complete_a_incomplete_call(self):
        call = IncompleteCall.objects.complete(
            self.call.pk, datetime(2000, 1, 3, 1, 1, 1, tzinfo=tz.UTC)
        )
        self.assertEqual(call.is_completed, True)
        self.assertEqual(call.period, date(2000, 1, 1))
