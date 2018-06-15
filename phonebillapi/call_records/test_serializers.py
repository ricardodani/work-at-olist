from django.test import TestCase
from call_records.serializers import CallRecordSerializer


class TestCallRecordSerializer(TestCase):

    def test_validation_of_empty_data(self):
        data = {}
        serializer = CallRecordSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertTrue('record_type' in serializer.errors)
        self.assertTrue('call_id' in serializer.errors)
        self.assertTrue('timestamp' in serializer.errors)

    def test_invalid_start(self):
        data = {
            'record_type': 'start',
            'call_id': 2,
            'timestamp': '2018-01-01T20:30',
        }
        serializer = CallRecordSerializer(data=data)
        import ipdb; ipdb.set_trace()
        serializer.is_valid()
        pass

    def test_invalid_record_type(self):
        data = {
            'record_type': 'something',
            'call_id': 2,
            'timestamp': '2018-01-01T20:30',
        }
        serializer = CallRecordSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertTrue('record_type' in serializer.errors)

    def test_valid_start_data(self):
        data = {
            'record_type': 'start',
            'call_id': 1,
            'source': '999999999999',
            'destination': '88888888888',
            'timestamp': '2018-01-01T20:30',
        }
        serializer = CallRecordSerializer(data=data)
        self.assertTrue(serializer.is_valid())
