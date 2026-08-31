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
"""Test Package for K2hr3 Python Client."""

import logging
import unittest
from http.client import HTTPMessage

from k2hr3client.api import K2hr3ApiResponse, K2hr3Api

LOG = logging.getLogger(__name__)


class TestK2hr3ApiResponse(unittest.TestCase):
    """Tests the K2hr3ApiResponse class.

    Simple usage(this class only):
    $ python -m unittest tests/test_r3token.py

    Simple usage(all):
    $ python -m unittest tests
    """
    def setUp(self):
        """Sets up a test case."""

    def tearDown(self):
        """Tears down a test case."""

    def test_k2hr3apiresponse_construct(self):
        """Creates a K2hr3ApiResponse instance."""
        hdrs = HTTPMessage()
        hdrs['mime-version'] = '1.0'
        response = K2hr3ApiResponse(code=200, url="http://localhost:18080", hdrs=hdrs, body=None)
        self.assertIsInstance(response, K2hr3ApiResponse)

    def test_k2hr3apiresponse_repr(self):
        """Represent a K2hr3ApiResponse instance."""
        hdrs = HTTPMessage()
        hdrs['mime-version'] = '1.0'
        response = K2hr3ApiResponse(code=200, url="http://localhost:18080", hdrs=hdrs, body=None)
        # Note: The order of _error and _code is unknown!
        self.assertRegex(repr(response), '<K2hr3ApiResponse .*>')

    def test_k2hr3apiresponse_validation_errors(self):
        """Test K2hr3ApiResponse property validation."""
        from k2hr3client.exception import K2hr3Exception
        hdrs = HTTPMessage()
        hdrs['mime-version'] = '1.0'
        resp = K2hr3ApiResponse(code=200, url="http://localhost:18080", hdrs=hdrs, body="OK")
        self.assertEqual(resp.body, "OK")
        self.assertEqual(resp.code, 200)
        self.assertEqual(resp.url, "http://localhost:18080")
        self.assertEqual(resp.hdrs, hdrs)

        # Invalid body type
        with self.assertRaises(K2hr3Exception):
            K2hr3ApiResponse(code=200, url="http://localhost:18080", hdrs=hdrs, body=123)  # type: ignore

        # Invalid hdrs type
        with self.assertRaises(K2hr3Exception):
            K2hr3ApiResponse(code=200, url="http://localhost:18080", hdrs="not_hdrs", body=None)  # type: ignore

        # Empty hdrs
        with self.assertRaises(K2hr3Exception):
            K2hr3ApiResponse(code=200, url="http://localhost:18080", hdrs=HTTPMessage(), body=None)

        # Invalid code type
        with self.assertRaises(K2hr3Exception):
            K2hr3ApiResponse(code="200", url="http://localhost:18080", hdrs=hdrs, body=None)  # type: ignore

        # Zero code
        with self.assertRaises(K2hr3Exception):
            K2hr3ApiResponse(code=0, url="http://localhost:18080", hdrs=hdrs, body=None)

        # Invalid url type
        with self.assertRaises(K2hr3Exception):
            K2hr3ApiResponse(code=200, url=123, hdrs=hdrs, body=None)  # type: ignore

        # Empty url
        with self.assertRaises(K2hr3Exception):
            K2hr3ApiResponse(code=200, url="", hdrs=hdrs, body=None)


class DummyK2hr3Api(K2hr3Api):
    """Concrete subclass of K2hr3Api for testing."""

    def _api_path(self, method):
        return f"{self.version}/{self.basepath}"


class TestK2hr3Api(unittest.TestCase):
    """Tests the K2hr3Api abstract base class through a concrete subclass."""

    def test_k2hr3api_construct_and_repr(self):
        """Test K2hr3Api construction and __repr__."""
        api = DummyK2hr3Api("test_basepath", params="a=1", hdrs={'H': 'V'}, body="body_data")
        self.assertEqual(api.basepath, "test_basepath")
        self.assertEqual(api.urlparams, "a=1")
        self.assertEqual(api.headers, {'H': 'V'})
        self.assertEqual(api.body, "body_data")
        self.assertEqual(api.version, "v1")
        self.assertIn('<K2hr3Api', repr(api))

    def test_basepath_property(self):
        """Test basepath property setter, re-assignment, and type validation."""
        from k2hr3client.exception import K2hr3Exception
        api = DummyK2hr3Api("path1")
        with self.assertRaises(K2hr3Exception):
            api.basepath = 12345  # type: ignore
        api.basepath = "path2"
        self.assertEqual(api.basepath, "path2")

    def test_set_response(self):
        """Test set_response correctly creates K2hr3ApiResponse."""
        api = DummyK2hr3Api("test")
        hdrs = HTTPMessage()
        hdrs['content-type'] = 'text/plain'
        api.set_response(code=200, url="http://localhost:18080/v1/test", headers=hdrs, body="response_body")
        self.assertIsNotNone(api.resp)
        self.assertEqual(api.resp.code, 200)
        self.assertEqual(api.resp.body, "response_body")

    def test_get_version(self):
        """Test package level get_version function."""
        import k2hr3client
        ver = k2hr3client.get_version()
        self.assertIsInstance(ver, str)
        self.assertTrue(len(ver) > 0)


#
# Local variables:
# tab-width: 4
# c-basic-offset: 4
# End:
# vim600: expandtab sw=4 ts=4 fdm=marker
# vim<600: expandtab sw=4 ts=4
#
