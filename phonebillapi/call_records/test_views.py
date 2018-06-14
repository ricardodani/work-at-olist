from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIRequestFactory
from rest_framework import status
from call_records.views import CallRecordView


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

    def test_post_data_(self):
        pass

    def test_save_a_call_record_returns_201(self):
        pass


class TestBillRetrieve(TestCase):

    def test_route(self):
        url = reverse('call_records:get-bill')
        self.assertEqual(url, '/call-records/get-bill/')

    def test_forbidden_methods(self):
        # TODO, post, put, patch, delete, options
        pass

    def test_not_found(self):
        pass

    def test_get_returns_200(self):
        pass
