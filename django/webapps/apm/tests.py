# This file is part of the research.fi API service
#
# Copyright 2019 Ministry of Education and Culture, Finland
#
# :author: CSC - IT Center for Science Ltd., Espoo Finland servicedesk@csc.fi
# :license: MIT
from django.test import SimpleTestCase
from django.conf import settings
from http import HTTPStatus
from unittest.mock import patch
from mock import MagicMock, Mock
import urllib3
from common import utils

class ApmProxyViewTests(SimpleTestCase):
    base_url = '/apm/'

    def setUp(self):
        # Get mock for testing http request.
        def get_urlopen_mock(body=u'Hello world'.encode('utf-8'), headers=None, status=200):
            mockHttpResponse = Mock(name='httplib.HTTPResponse')
            headers = urllib3.response.HTTPHeaderDict(headers)
            urllib3_response = urllib3.HTTPResponse(body, headers, status, preload_content=False, original_response=mockHttpResponse)
            return MagicMock(return_value=urllib3_response)

        self.urlopen_mock = get_urlopen_mock()
        self.urlopen_patcher = patch('urllib3.PoolManager.urlopen', self.urlopen_mock)
        self.urlopen = self.urlopen_patcher.start()

    def tearDown(self):
        self.urlopen_patcher.stop()

    def test_http_basic_authentication_header_is_added_when_username_and_password_are_defined(self):
        """HTTP basic authentication header should be added when settings.HTTP_AUTH_USERNAME and settings.HTTP_AUTH_PASSWORD are defined."""
        with self.settings(HTTP_AUTH_USERNAME='foo'):
            with self.settings(HTTP_AUTH_PASSWORD='bar'):
                response = self.client.post(self.base_url)
                headers = self.urlopen_mock.call_args.kwargs['headers']
                self.assertTrue('Authorization' in headers, 'Authorization header is not present')
                expected_header_value = utils.get_basic_authentication_header_value(settings.HTTP_AUTH_USERNAME, settings.HTTP_AUTH_PASSWORD)
                self.assertEquals(headers['Authorization'], expected_header_value, 'Authorization header value is incorrect')

    def test_http_basic_authentication_header_is_not_added_when_username_or_password_is_not_defined(self):
        """HTTP basic authentication header should not be added when settings.HTTP_AUTH_USERNAME and/or settings.HTTP_AUTH_PASSWORD is None."""
        with self.settings(HTTP_AUTH_USERNAME=None):
            with self.settings(HTTP_AUTH_PASSWORD=None):
                response = self.client.post(self.base_url)
                headers = self.urlopen_mock.call_args.kwargs['headers']
                self.assertFalse('Authorization' in headers, 'Authorization header is present when both password and username are None')
        with self.settings(HTTP_AUTH_USERNAME=None):
            with self.settings(HTTP_AUTH_PASSWORD='bar'):
                response = self.client.post(self.base_url)
                headers = self.urlopen_mock.call_args.kwargs['headers']
                self.assertFalse('Authorization' in headers, 'Authorization header is present when username is None')
        with self.settings(HTTP_AUTH_USERNAME='foo'):
            with self.settings(HTTP_AUTH_PASSWORD=None):
                response = self.client.post(self.base_url)
                headers = self.urlopen_mock.call_args.kwargs['headers']
                self.assertFalse('Authorization' in headers, 'Authorization header is present when password is None')

    def test_post_request_is_allowed(self):
        """When request HTTP method is POST it is forwarded to Application Performance Monitoring."""
        # In unit test, instead of APM, forward request to internal view "ping", which responds with HTTP status 200.
        response = self.client.post(self.base_url)
        self.assertEquals(response.status_code, HTTPStatus.OK.value, 'POST request is not allowed')

    def test_get_request_not_allowed(self):
        """When request HTTP method is GET it is rejected with status code 405 Method Not Allowed"""
        response = self.client.get(self.base_url)
        self.assertEquals(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED.value, 'GET request is allowed')

    def test_put_request_not_allowed(self):
        """When request HTTP method is PUT, it is rejected with status code 405 Method Not Allowed"""
        response = self.client.put(self.base_url)
        self.assertEquals(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED.value, 'PUT request is allowed')

    def test_delete_request_not_allowed(self):
        """When request HTTP method is DELETE, it is rejected with status code 405 Method Not Allowed"""
        response = self.client.delete(self.base_url)
        self.assertEquals(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED.value, 'DELETE request is allowed')

    def test_patch_request_not_allowed(self):
        """When request HTTP method is PATCH, it is rejected with status code 405 Method Not Allowed"""
        response = self.client.patch(self.base_url)
        self.assertEquals(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED.value, 'PATCH request is allowed')