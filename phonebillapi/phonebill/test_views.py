from django.test import TestCase


class TestCallRecordCreateView(TestCase):


    def test_route(self):
        # TODO: just test /v1/api/add-record/
        pass

    def test_forbidden_methods(self):
        # TODO: get, put, patch, delete, options
        pass

    def test_invalid_form_data_returns_bad_request(self):
        pass

    def test_save_a_call_record_returns_201(self):
        pass


class TestBillRetrieve(TestCase):
    def test_route(self):
        # TODO: test /v1/api/get-bill/
        pass

    def test_forbidden_methods(self):
        # TODO, post, put, patch, delete, options
        pass

    def test_not_found(self):
        pass

    def test_get_returns_200(self):
        pass
