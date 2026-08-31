# -*- coding: utf-8 -*-
#
# k2hr3client - Python client for K2HR3 REST API
#
# Copyright 2020 Yahoo Japan Corporation
# Copyright 2024 LY Corporation
#
# K2HR3 is K2hdkc based Resource and Roles and policy Rules, gathers
# common management information for the cloud.
# K2HR3 can dynamically manage information as "who", "what", "operate".
# These are stored as roles, resources, policies in K2hdkc, and the
# client system can dynamically read and modify these information.
#
# For the full copyright and license information, please view
# the license file that was distributed with this source code.
#
# AUTHOR:   Hirotaka Wakabayashi
# CREATE:   Mon Sep 14 2020
# REVISION:
#
"""Test Package for K2hr3Http."""

import json
import logging
import socket
import ssl
import unittest
from unittest.mock import patch, MagicMock
import urllib.request
from urllib.error import HTTPError, URLError, ContentTooShortError
from http.client import HTTPMessage

from k2hr3client.http import K2hr3Http, _AgentError
from k2hr3client.api import K2hr3Api, K2hr3HTTPMethod
from k2hr3client.exception import K2hr3Exception

LOG = logging.getLogger(__name__)


class DummyApi(K2hr3Api):
    """Dummy K2hr3Api implementation for testing HTTP methods."""

    def __init__(self, basepath="dummy", headers=None, body=None, urlparams=None):
        super().__init__(basepath)
        self.headers = headers if headers is not None else {'Content-Type': 'application/json'}
        self.body = body
        self.urlparams = urlparams

    def _api_path(self, method: K2hr3HTTPMethod):
        return f"{self.version}/{self.basepath}"


class TestK2hr3Http(unittest.TestCase):
    """Tests the K2hr3Http class."""

    def setUp(self):
        """Sets up test fixtures."""
        self.base_url = "http://127.0.0.1:18080"
        self.https_url = "https://127.0.0.1:18443"

    def test_http_construct_and_repr(self):
        """Test K2hr3Http construction and repr."""
        http = K2hr3Http(self.base_url)
        self.assertEqual(http.baseurl, self.base_url)
        self.assertIn('<K2hr3Http', repr(http))

    def test_http_construct_invalid_url(self):
        """Test invalid baseurl inputs raise K2hr3Exception."""
        # Non-string
        with self.assertRaises(K2hr3Exception):
            K2hr3Http(12345)  # type: ignore
        # No scheme separator
        with self.assertRaises(K2hr3Exception):
            K2hr3Http("invalid_url_without_scheme")
        # Unsupported scheme
        with self.assertRaises(K2hr3Exception):
            K2hr3Http("ftp://127.0.0.1:21")
        # Unresolvable domain
        with self.assertRaises(K2hr3Exception):
            K2hr3Http("http://this-domain-does-not-exist-at-all-12345.example:18080")

    def test_headers_property(self):
        """Test headers getter, setter, and deleter."""
        http = K2hr3Http(self.base_url)
        http.headers = {'Custom-Header': 'value'}
        self.assertEqual(http.headers, {'Custom-Header': 'value'})
        del http.headers
        self.assertIsNone(http.headers)

    def test_url_property(self):
        """Test url getter, setter, deleter, and error cases."""
        http = K2hr3Http(self.base_url)
        with self.assertRaises(K2hr3Exception):
            http.url = 12345  # type: ignore
        http.url = "http://127.0.0.1:18080/v1/test"
        self.assertEqual(http.url, "http://127.0.0.1:18080/v1/test")
        # Setting again logs info
        http.url = "http://127.0.0.1:18080/v1/test2"
        self.assertEqual(http.url, "http://127.0.0.1:18080/v1/test2")
        del http.url
        self.assertIsNone(http.url)

    def test_urlparams_property(self):
        """Test urlparams getter, setter, and deleter."""
        http = K2hr3Http(self.base_url)
        http.urlparams = "foo=bar"
        self.assertEqual(http.urlparams, "foo=bar")
        del http.urlparams
        self.assertIsNone(http.urlparams)

    @patch('urllib.request.urlopen')
    def test_http_request_method_success(self, mock_urlopen):
        """Test _HTTP_REQUEST_METHOD success path."""
        http = K2hr3Http(self.base_url)
        dummy_api = DummyApi()

        mock_resp = MagicMock()
        mock_resp.getcode.return_value = 200
        mock_resp.geturl.return_value = f"{self.base_url}/v1/dummy"
        mock_hdrs = HTTPMessage()
        mock_hdrs['content-type'] = 'application/json'
        mock_resp.info.return_value = mock_hdrs
        mock_resp.read.return_value = b'{"result": true}'
        mock_resp.__enter__.return_value = mock_resp
        mock_urlopen.return_value = mock_resp

        req = urllib.request.Request(f"{self.base_url}/v1/dummy")
        result = http._HTTP_REQUEST_METHOD(dummy_api, req)
        self.assertTrue(result)
        self.assertEqual(dummy_api.resp.code, 200)

    @patch('ssl.create_default_context')
    @patch('urllib.request.urlopen')
    def test_http_request_method_https_self_signed(self, mock_urlopen, mock_ssl_context):
        """Test _HTTP_REQUEST_METHOD with HTTPS and self-signed certificate enabled."""
        http = K2hr3Http(self.https_url)
        http._allow_self_signed_cert = True
        dummy_api = DummyApi()

        mock_ctx = MagicMock()
        mock_ssl_context.return_value = mock_ctx

        mock_resp = MagicMock()
        mock_resp.getcode.return_value = 200
        mock_resp.geturl.return_value = f"{self.https_url}/v1/dummy"
        mock_hdrs = HTTPMessage()
        mock_hdrs['content-type'] = 'application/json'
        mock_resp.info.return_value = mock_hdrs
        mock_resp.read.return_value = b'{"result": true}'
        mock_resp.__enter__.return_value = mock_resp
        mock_urlopen.return_value = mock_resp

        req = urllib.request.Request(f"{self.https_url}/v1/dummy")
        result = http._HTTP_REQUEST_METHOD(dummy_api, req)
        self.assertTrue(result)
        self.assertFalse(mock_ctx.check_hostname)
        self.assertEqual(mock_ctx.verify_mode, ssl.CERT_NONE)

    @patch('urllib.request.urlopen')
    def test_http_request_method_http_error(self, mock_urlopen):
        """Test _HTTP_REQUEST_METHOD handling HTTPError."""
        http = K2hr3Http(self.base_url)
        dummy_api = DummyApi()

        mock_urlopen.side_effect = HTTPError("url", 404, "Not Found", HTTPMessage(), None)
        req = urllib.request.Request(f"{self.base_url}/v1/dummy")
        result = http._HTTP_REQUEST_METHOD(dummy_api, req)
        self.assertFalse(result)

    @patch('urllib.request.urlopen')
    def test_http_request_method_url_error(self, mock_urlopen):
        """Test _HTTP_REQUEST_METHOD handling URLError and ContentTooShortError."""
        http = K2hr3Http(self.base_url)
        dummy_api = DummyApi()

        mock_urlopen.side_effect = URLError("Connection refused")
        req = urllib.request.Request(f"{self.base_url}/v1/dummy")
        result = http._HTTP_REQUEST_METHOD(dummy_api, req)
        self.assertFalse(result)

        mock_urlopen.side_effect = ContentTooShortError("Too short", "content")
        result = http._HTTP_REQUEST_METHOD(dummy_api, req)
        self.assertFalse(result)

    @patch('time.sleep')
    @patch('urllib.request.urlopen')
    def test_http_request_method_retry_and_exhaustion(self, mock_urlopen, mock_sleep):
        """Test _HTTP_REQUEST_METHOD retry on socket.timeout and eventual exhaustion."""
        http = K2hr3Http(self.base_url)
        http._retries = 1
        http._retry_interval_seconds = 0
        dummy_api = DummyApi()

        mock_urlopen.side_effect = socket.timeout("timed out")
        req = urllib.request.Request(f"{self.base_url}/v1/dummy")
        result = http._HTTP_REQUEST_METHOD(dummy_api, req)
        self.assertFalse(result)

    @patch('k2hr3client.http.K2hr3Http._HTTP_REQUEST_METHOD')
    def test_post_with_non_json_content_type_with_urlparams(self, mock_HTTP_REQUEST_METHOD):
        """Test POST with non-json content type and non-empty urlparams."""
        http = K2hr3Http(self.base_url)
        dummy_api = DummyApi(headers={'Content-Type': 'text/plain'}, urlparams={'name': 'test'})
        mock_HTTP_REQUEST_METHOD.return_value = True

        res = http.POST(dummy_api)
        self.assertTrue(res)
        self.assertEqual(http.urlparams, b'name=test')

    @patch('k2hr3client.http.K2hr3Http._HTTP_REQUEST_METHOD')
    def test_post_with_non_json_content_type(self, mock_HTTP_REQUEST_METHOD):
        """Test POST with non-json content type."""
        http = K2hr3Http(self.base_url)
        dummy_api = DummyApi(headers={'Content-Type': 'application/x-www-form-urlencoded'}, urlparams={'key': 'val'})
        mock_HTTP_REQUEST_METHOD.return_value = True

        res = http.POST(dummy_api)
        self.assertTrue(res)

    @patch('k2hr3client.http.K2hr3Http._HTTP_REQUEST_METHOD')
    def test_put_method(self, mock_HTTP_REQUEST_METHOD):
        """Test PUT method execution."""
        http = K2hr3Http(self.base_url)
        dummy_api = DummyApi()
        dummy_api.urlparams = json.dumps({'param1': 'value1'})
        mock_HTTP_REQUEST_METHOD.return_value = True

        res = http.PUT(dummy_api)
        self.assertTrue(res)

    @patch('k2hr3client.http.K2hr3Http._HTTP_REQUEST_METHOD')
    def test_get_with_dict_urlparams(self, mock_HTTP_REQUEST_METHOD):
        """Test GET method with dict urlparams."""
        http = K2hr3Http(self.base_url)
        dummy_api = DummyApi()
        mock_HTTP_REQUEST_METHOD.return_value = True

        dummy_api.urlparams = {'foo': 'bar'}
        res = http.GET(dummy_api)
        self.assertTrue(res)
        self.assertIn("foo=bar", http.urlparams)

    @patch('k2hr3client.http.K2hr3Http._HTTP_REQUEST_METHOD')
    def test_get_with_string_urlparams(self, mock_HTTP_REQUEST_METHOD):
        """Test GET method with json string urlparams."""
        http = K2hr3Http(self.base_url)
        dummy_api = DummyApi()
        mock_HTTP_REQUEST_METHOD.return_value = True

        dummy_api.urlparams = json.dumps({'baz': 'qux'})
        res = http.GET(dummy_api)
        self.assertTrue(res)
        self.assertIn("baz=qux", http.urlparams)

    @patch('k2hr3client.http.K2hr3Http._HTTP_REQUEST_METHOD')
    def test_head_and_delete_methods(self, mock_HTTP_REQUEST_METHOD):
        """Test HEAD and DELETE methods."""
        http = K2hr3Http(self.base_url)
        dummy_api = DummyApi()
        mock_HTTP_REQUEST_METHOD.return_value = True

        # HEAD with dict params
        dummy_api.urlparams = {'head_param': '1'}
        res = http.HEAD(dummy_api)
        self.assertTrue(res)

        # HEAD with string params
        dummy_api.urlparams = json.dumps({'head_param': '2'})
        res = http.HEAD(dummy_api)
        self.assertTrue(res)

        # DELETE with dict params
        dummy_api.urlparams = {'del_param': '1'}
        res = http.DELETE(dummy_api)
        self.assertTrue(res)

        # DELETE with string params
        dummy_api.urlparams = json.dumps({'del_param': '2'})
        res = http.DELETE(dummy_api)
        self.assertTrue(res)


#
# Local variables:
# tab-width: 4
# c-basic-offset: 4
# End:
# vim600: expandtab sw=4 ts=4 fdm=marker
# vim<600: expandtab sw=4 ts=4
#
