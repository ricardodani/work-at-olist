import pytz
from unittest import mock
from datetime import datetime
from django.test import TestCase
from call_records.models import Call, NotCompletedCall #, CompletedCall
from call_records import exceptions
from call_records.price import (
    CallPriceInvalidInputError #, CallPriceStartGtEndError,
    #CallPriceEndInFutureError
)


class TestCallManagers(TestCase):

    def setUp(self):
        self.completed_call_1 = Call.objects.create(
            call_id=1,
            source="21999000000",
            destination="11999000000",
            started_at=datetime(2000, 1, 2, 1, 1, 1, tzinfo=pytz.UTC),
            ended_at=datetime(2000, 1, 3, 1, 1, 1, tzinfo=pytz.UTC)
        )
        self.not_completed_call_2 = Call.objects.create(
            call_id=2,
            source="21999000000",
            destination="11999000000",
            started_at=datetime(2000, 1, 2, 1, 1, 1, tzinfo=pytz.UTC)
        )

    def test_get_queryset(self):
        call = NotCompletedCall.objects.get()
        self.assertEqual(call.call_id, 2)

    def test_create_call_exist_error(self):
        self.assertRaises(
            exceptions.CallExistsError, NotCompletedCall.objects.create,
            2, '21999090000', '31999099999',
            datetime(2000, 1, 2, 1, 1, 1, tzinfo=pytz.UTC)
        ) # same id
        self.assertRaises(
            exceptions.CallExistsError, NotCompletedCall.objects.create,
            1, '21999090000', '31999099999',
            datetime(2000, 1, 2, 1, 1, 1, tzinfo=pytz.UTC)
        ) # same id as completed call

    def test_create_call(self):
        not_completed_call = NotCompletedCall.objects.create(
            call_id=3, source="99999099999", destination="88888888888",
            started_at=datetime(2000, 1, 2, 1, 1, 1, tzinfo=pytz.UTC)
        )
        self.assertEqual(
            not_completed_call.call_id,
            NotCompletedCall.objects.get(call_id=3).call_id
        )

    def test_complete_no_call_to_end_error(self):
        self.assertRaises(
            exceptions.NoCallToEndError, NotCompletedCall.objects.complete,
            1, datetime(2000, 1, 3, 1, 1, 1, tzinfo=pytz.UTC)
        )

    @mock.patch('call_records.models.CallPrice')
    def test_raises_calculate_price_error(self, mocked_call_price):
        mocked_calculate = mock.Mock(
            side_effect=CallPriceInvalidInputError
        )
        mocked_call_price.return_value = mock.Mock(
            calculate=mocked_calculate
        )
        self.assertRaises(
            exceptions.CalculatePriceError,
            NotCompletedCall.objects.complete,
            call_id=self.not_completed_call_2.call_id,
            ended_at=datetime(2000, 1, 3, 1, 1, 1, tzinfo=pytz.UTC)
        )
        self.assertTrue(mocked_calculate.called)

    def test_complete_call(self):
        pass

    def test_get_bill_queryset(self):
        pass

