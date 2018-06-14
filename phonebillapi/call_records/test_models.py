from datetime import datetime, date
from unittest.mock import patch, Mock
from decimal import Decimal
from django.utils.timezone import datetime, timedelta
from django.test import TestCase
from call_records.models import Call


class TestCall(TestCase):

    def setUp(self):
        self.ended_call = Call.objects.create(
            call_id=1,
            source="21999000000",
            destination="11999000000",
            started_at=datetime(2000, 1, 2, 1, 1, 1, tzinfo=tz.UTC)
        )
