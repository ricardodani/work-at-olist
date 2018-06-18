from unittest import mock
from datetime import datetime
from django.test import TestCase
from call_records.serializers import CallStartSerializer, CallEndSerializer
from call_records.models import Call


class TestCallStartSerializer(TestCase):
    def test_validation_of_empty_data(self):
        data = {}
        serializer = CallStartSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertTrue('call_id' in serializer.errors)
        self.assertTrue('timestamp' in serializer.errors)
        self.assertTrue('destination' in serializer.errors)
        self.assertTrue('source' in serializer.errors)

    def test_validation_of_invalid_data(self):
        data = {
            'call_id': 'a',
            'timestamp': 'b',
            'source': 'c',
            'destination': 'd'
        }
        serializer = CallStartSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertTrue('call_id' in serializer.errors)
        self.assertTrue('timestamp' in serializer.errors)
        self.assertTrue('destination' in serializer.errors)
        self.assertTrue('source' in serializer.errors)

    def test_valid_data(self):
        data = {
            'record_type': 'start',
            'call_id': 1,
            'source': '99999999999',
            'destination': '88888888888',
            'timestamp': '2018-01-01T20:30',
        }
        serializer = CallStartSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    @mock.patch('call_records.serializers.NotCompletedCall')
    def test_save_valid_data_return_serialized_obj(self, mocked_call_class):
        mocked_call_class.return_value = mock.Mock(
            objects=mock.Mock(
                create=Call(
                    call_id=1,
                    source='99999999999',
                    destination='88888888888',
                    started_at=datetime(2010, 10, 10, 1, 1, 1),
                )
            )
        )
        data = {
            'call_id': 1,
            'source': '99999999999',
            'destination': '88888888888',
            'timestamp': '2018-01-01T20:30',
        }
        serializer = CallStartSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        self.assertEqual(instance['call_id'], data['call_id'])


class TestCallEndSerializer(TestCase):
    def test_validation_of_empty_data(self):
        data = {}
        serializer = CallEndSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertTrue('call_id' in serializer.errors)
        self.assertTrue('timestamp' in serializer.errors)

    def test_validation_of_invalid_data(self):
        data = {
            'call_id': 'a',
            'timestamp': 'b',
        }
        serializer = CallEndSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertTrue('call_id' in serializer.errors)
        self.assertTrue('timestamp' in serializer.errors)

    def test_valid_data(self):
        data = {
            'call_id': 1,
            'timestamp': '2018-01-01T20:30',
        }
        serializer = CallEndSerializer(data=data)
        self.assertTrue(serializer.is_valid())
