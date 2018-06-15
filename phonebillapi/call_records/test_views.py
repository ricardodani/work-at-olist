from unittest import mock
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIRequestFactory
from rest_framework import status
from rest_framework import exceptions
from call_records.views import CallRecordView, BillRetrieveView


class TestCallRecordCreateView(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.url = reverse('call_records:post-record')
        self.view = CallRecordView.as_view()

    def test_route(self):
        self.assertEqual(self.url, '/call-records/post-record/')

    def test_forbidden_methods(self):
        forbidden_methods = ['get', 'put', 'patch', 'options', 'delete']
        for fm in forbidden_methods:
            request = getattr(self.factory, fm)(self.url)
            response = self.view(request)
            self.assertEqual(
                response.status_code,
                status.HTTP_405_METHOD_NOT_ALLOWED
            )

    @mock.patch('call_records.views.CallRecordSerializer')
    def test_post_invalid_data_returns_bad_request(self, mocked_serializer):
        mocked_serializer.return_value = mock.Mock(
            is_valid=mock.Mock(side_effect=exceptions.ValidationError)
        )
        request = self.factory.post(self.url, {})
        response = self.view(request)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    @mock.patch('call_records.views.CallRecordSerializer')
    def test_save_error_return_api_exception(self, mocked_serializer):
        save_mock = mock.Mock(side_effect = exceptions.APIException)
        mocked_serializer.return_value = mock.Mock(
            is_valid=mock.Mock(return_value=True),
            save=save_mock
        )
        request = self.factory.post(self.url, {})
        response = self.view(request)
        self.assertEqual(
            response.status_code,
            status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        save_mock.assert_called_once()

    @mock.patch('call_records.views.CallRecordSerializer')
    def test_post_valid_data_return_saved_data(self, mocked_serializer):
        save_mock = mock.Mock(return_value={'call': 'data'})
        mocked_serializer.return_value = mock.Mock(
            is_valid=mock.Mock(return_value=True),
            save=save_mock
        )
        request = self.factory.post(self.url, {})
        response = self.view(request)
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            response.data, {'call': 'data'}
        )
        save_mock.assert_called_once()


class TestBillRetrieve(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.url = reverse('call_records:get-bill')
        self.view = BillRetrieveView.as_view()

    def test_route(self):
        self.assertEqual(self.url, '/call-records/get-bill/')

    def test_forbidden_methods(self):
        forbidden_methods = ['post', 'put', 'patch', 'options', 'delete']
        for fm in forbidden_methods:
            request = getattr(self.factory, fm)(self.url)
            response = self.view(request)
            self.assertEqual(
                response.status_code,
                status.HTTP_405_METHOD_NOT_ALLOWED
            )

    @mock.patch('call_records.views.BillInputSerializer')
    def test_get_invalid_params_returns_bad_request(self, mocked_serializer):
        mocked_serializer.return_value = mock.Mock(
            is_valid=mock.Mock(side_effect=exceptions.ValidationError)
        )
        request = self.factory.get(self.url)
        response = self.view(request)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    @mock.patch('call_records.views.BillInputSerializer')
    def test_get_bill_error_returns_api_exception(self, mocked_serializer):
        get_bill_data = mock.Mock(side_effect = exceptions.APIException)
        mocked_serializer.return_value = mock.Mock(
            is_valid=mock.Mock(return_value=True),
            get_bill_data=get_bill_data
        )
        request = self.factory.get(self.url, {})
        response = self.view(request)
        self.assertEqual(
            response.status_code,
            status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        get_bill_data.assert_called_once()

    @mock.patch('call_records.views.BillInputSerializer')
    def test_get_bill_returns_bill_data(self, mocked_serializer):
        get_bill_data = mock.Mock(return_value={'bill': 'data'})
        mocked_serializer.return_value = mock.Mock(
            is_valid=mock.Mock(return_value=True),
            get_bill_data=get_bill_data
        )
        request = self.factory.get(self.url, {})
        response = self.view(request)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.data, {'bill': 'data'}
        )
        get_bill_data.assert_called_once()
