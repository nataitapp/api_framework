__author__ = 'nata'

from api_utils import Calls
from unittest import TestCase
import httplib

# defining TestClass class using inheritance from TestCase class od module
class TestClass(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.calls = Calls()



    def test_create_folder_positive(self):
        folder = self.calls.gen_random_name()
        resp = self.calls.create_folder(folder)
        assert resp.http_code == httplib.CREATED # or 201

    def test_delete_folder(self):
        folder = self.calls.gen_random_name()
        resp = self.calls.create_folder(folder)
        assert resp.http_code == httplib.CREATED # or 201
        resp = self.calls.delete_folder(folder)
        assert resp.http_code == httplib.OK # or 200

    def test_create_folder_negative(self):
        folder = self.calls.gen_random_name()
        resp = self.calls.create_folder(folder, password = 'asdas')
        assert resp.http_code == httplib.UNAUTHORIZED
        assert resp.json_body['inputErrors']['credentials'][0]['code'] == 'INVALID_CREDENTIALS'
        assert resp.json_body['inputErrors']['credentials'][0]['msg'] == 'This request is unauthenticated. ' \
                                                                    'Please provide credentials and try again.'
    def test_non_existing_folder(self):
        folder_name = self.calls.gen_random_name()
        resp = self.calls.delete_folder(folder_name)
        assert self.http_code == httplib.NOT_FOUND
        assert resp.json_body['errorMessage'] == 'Item does not exist'

    def test_delete_folder_wrong_accept_header(self):
        folder_name = self.calls.gen_random_name()
        resp = self.calls.delete_folder(folder_name, accept = 'application/xml')
        assert self.http_code == httplib.NOT_ACCEPTABLE #or 406
        assert resp.json_body['errorMessage'] == 'Not Acceptablet'

    def test_method_not_allowed(self):
        folder_name = self.calls.gen_random_name()
        resp = self.calls.delete_folder(folder_name)
        resp = self.http_code == httplib.METHOD_NOT_ALLOWED #or 405





    # @classmethod
    # def tearDown(cls):