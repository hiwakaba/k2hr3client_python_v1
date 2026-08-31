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

import json
import logging
import unittest
from unittest.mock import patch
import urllib.parse
from http.client import HTTPMessage

from k2hr3client import http as khttp
from k2hr3client import token as ktoken

LOG = logging.getLogger(__name__)


class TestK2hr3token(unittest.TestCase):
    """Tests the K2hr3token class.

    Simple usage(this class only):
    $ python -m unittest tests/test_token.py

    Simple usage(all):
    $ python -m unittest tests
    """
    def setUp(self):
        """Sets up a test case."""
        self.base_url = "http://127.0.0.1:18080"
        self.iaas_project = "my_project"
        self.iaas_token = "my_iaas_token"
        self.r3token = "my_r3_token"
        self.role = "my_role"
        self.expire = 0
        self.expand = True

    def tearDown(self):
        """Tears down a test case."""

    def test_k2hr3token_construct(self):
        """Creates a K2hr3Token instance."""
        mytoken = ktoken.K2hr3Token(self.iaas_project, self.iaas_token)
        self.assertIsInstance(mytoken, ktoken.K2hr3Token)

    def test_k2hr3token_repr(self):
        """Represent a K2hr3Token instance."""
        mytoken = ktoken.K2hr3Token(self.iaas_project, self.iaas_token)
        # Note: The order of _error and _code is unknown!
        self.assertRegex(repr(mytoken), '<K2hr3Token .*>')

    @patch('k2hr3client.http.K2hr3Http._HTTP_REQUEST_METHOD')
    def test_token_create_using_post(self, mock_HTTP_REQUEST_METHOD):
        """Get root path."""
        mytoken = ktoken.K2hr3Token(self.iaas_project, self.iaas_token)
        self.assertEqual(mytoken.iaas_project, self.iaas_project)
        self.assertEqual(mytoken.iaas_token, self.iaas_token)
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': f'U={self.iaas_token}'
        }
        self.assertEqual(mytoken.headers, headers)
        mytoken.create()
        httpreq = khttp.K2hr3Http(self.base_url)
        self.assertTrue(httpreq.POST(mytoken))

        # 1. assert URL
        self.assertEqual(httpreq.url, f"{self.base_url}/v1/user/tokens")
        # 2. assert URL params
        self.assertEqual(mytoken.urlparams, None)
        # 3. assert Request headers
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': f'U={self.iaas_token}'
        }
        self.assertEqual(mytoken.headers, headers)
        # 4. assert Request body
        python_data = json.loads(ktoken._TOKEN_API_CREATE_TOKEN_TYPE2)
        python_data['auth']['tenantName'] = self.iaas_project
        body = json.dumps(python_data)
        self.assertEqual(mytoken.body, body)

    @patch('k2hr3client.http.K2hr3Http._HTTP_REQUEST_METHOD')
    def test_token_create_using_put(self, mock_HTTP_REQUEST_METHOD):
        """Get root path."""
        mytoken = ktoken.K2hr3Token(self.iaas_project, self.iaas_token)
        self.assertEqual(mytoken.iaas_project, self.iaas_project)
        self.assertEqual(mytoken.iaas_token, self.iaas_token)
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': f'U={self.iaas_token}'
        }
        self.assertEqual(mytoken.headers, headers)
        mytoken.create()
        httpreq = khttp.K2hr3Http(self.base_url)
        self.assertTrue(httpreq.PUT(mytoken))

        # 1. assert URL
        self.assertEqual(httpreq.url, f"{self.base_url}/v1/user/tokens")
        # 2. assert URL params
        s_s_urlparams = {'tenantname': self.iaas_project}
        self.assertEqual(mytoken.urlparams, json.dumps(s_s_urlparams))
        s_urlparams = urllib.parse.urlencode(s_s_urlparams)
        self.assertEqual(httpreq.urlparams, f"{s_urlparams}")
        # 3. assert Request headers
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': f'U={self.iaas_token}'
        }
        self.assertEqual(mytoken.headers, headers)
        # 4. assert Request body
        self.assertEqual(mytoken.body, None)

    @patch('k2hr3client.http.K2hr3Http._HTTP_REQUEST_METHOD')
    def test_token_show_credential_details_using_get(
            self, mock_HTTP_REQUEST_METHOD):
        """Get root path."""
        mytoken = ktoken.K2hr3Token(self.iaas_project, self.iaas_token)
        self.assertEqual(mytoken.iaas_project, self.iaas_project)
        self.assertEqual(mytoken.iaas_token, self.iaas_token)
        mytoken.show()
        httpreq = khttp.K2hr3Http(self.base_url)
        self.assertTrue(httpreq.GET(mytoken))

        # 1. assert URL
        self.assertEqual(httpreq.url, f"{self.base_url}/v1/user/tokens")
        # 2. assert URL params
        self.assertEqual(httpreq.urlparams, None)
        # 3. assert Request headers
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': f'U={self.iaas_token}'
        }
        self.assertEqual(mytoken.headers, headers)
        # 4. assert Request body
        self.assertEqual(mytoken.body, None)

    @patch('k2hr3client.http.K2hr3Http._HTTP_REQUEST_METHOD')
    def test_validate(self, mock_HTTP_REQUEST_METHOD):
        mytoken = ktoken.K2hr3Token(self.iaas_project, self.iaas_token)
        """Get root path."""
        self.assertEqual(mytoken.iaas_project, self.iaas_project)
        self.assertEqual(mytoken.iaas_token, self.iaas_token)
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': f'U={self.iaas_token}'
        }
        self.assertEqual(mytoken.headers, headers)

        mytoken.validate()

        httpreq = khttp.K2hr3Http(self.base_url)
        self.assertTrue(httpreq.HEAD(mytoken))

        # 1. assert URL
        self.assertEqual(httpreq.url, f"{self.base_url}/v1/user/tokens")
        # 2. assert URL params
        self.assertEqual(httpreq.urlparams, None)
        # 3. assert Request headers
        self.assertEqual(mytoken.headers, headers)
        # 4. assert Request body
        self.assertEqual(mytoken.body, None)

    def test_token_credential_auth_type(self):
        """Test K2hr3Token with CREDENTIAL auth_type."""
        mytoken = ktoken.K2hr3Token(self.iaas_project, self.iaas_token,
                                    auth_type=ktoken.K2hr3AuthType.CREDENTIAL)
        self.assertEqual(mytoken.headers, {'Content-Type': 'application/json'})

    def test_token_property_from_response(self):
        """Test token property extracts token from response body."""
        mytoken = ktoken.K2hr3Token(self.iaas_project, self.iaas_token)
        hdrs = HTTPMessage()
        hdrs['content-type'] = 'application/json'
        mytoken.set_response(code=200, url=self.base_url, headers=hdrs,
                             body=json.dumps({'result': True, 'token': 'test_r3_token_123'}))
        self.assertEqual(mytoken.token, 'test_r3_token_123')

    @patch('k2hr3client.http.K2hr3Http._HTTP_REQUEST_METHOD')
    def test_token_create_with_user_password_post(self, mock_HTTP_REQUEST_METHOD):
        """Test K2hr3Token create with user and password via POST."""
        mytoken = ktoken.K2hr3Token(self.iaas_project, self.iaas_token)
        mytoken.create(user="test_user", password="test_password")
        httpreq = khttp.K2hr3Http(self.base_url)
        self.assertTrue(httpreq.POST(mytoken))
        body = json.loads(mytoken.body)
        self.assertEqual(body['auth']['user'], 'test_user')
        self.assertEqual(body['auth']['password'], 'test_password')
        self.assertEqual(body['auth']['tenantName'], self.iaas_project)

    @patch('k2hr3client.http.K2hr3Http._HTTP_REQUEST_METHOD')
    def test_token_create_with_user_password_put(self, mock_HTTP_REQUEST_METHOD):
        """Test K2hr3Token create with user and password via PUT."""
        mytoken = ktoken.K2hr3Token(self.iaas_project, self.iaas_token)
        mytoken.create(user="test_user", password="test_password")
        httpreq = khttp.K2hr3Http(self.base_url)
        self.assertTrue(httpreq.PUT(mytoken))
        urlparams = json.loads(mytoken.urlparams)
        self.assertEqual(urlparams['user'], 'test_user')
        self.assertEqual(urlparams['password'], 'test_password')
        self.assertEqual(urlparams['tenantname'], self.iaas_project)

    def test_token_api_path_unsupported_method(self):
        """Test _api_path returns None for unsupported methods."""
        mytoken = ktoken.K2hr3Token(self.iaas_project, self.iaas_token)
        mytoken.api_id = 999
        self.assertIsNone(mytoken._api_path(ktoken.K2hr3HTTPMethod.DELETE))

    @patch('urllib.request.urlopen')
    def test_get_openstack_token_success(self, mock_urlopen):
        """Test get_openstack_token successfully retrieves scoped token."""
        mock_unscoped_res = unittest.mock.MagicMock()
        mock_unscoped_res.info.return_value = {'X-Subject-Token': 'unscoped_token_val'}
        mock_unscoped_res.__enter__.return_value = mock_unscoped_res

        mock_scoped_res = unittest.mock.MagicMock()
        mock_scoped_res.info.return_value = {'X-Subject-Token': 'scoped_token_val'}
        mock_scoped_res.__enter__.return_value = mock_scoped_res

        mock_urlopen.side_effect = [mock_unscoped_res, mock_scoped_res]

        token = ktoken.K2hr3Token.get_openstack_token(
            "http://keystone:5000/v3/auth/tokens",
            "demo", "secret", "myproject"
        )
        self.assertEqual(token, 'scoped_token_val')
        self.assertEqual(mock_urlopen.call_count, 2)

    @patch('urllib.request.urlopen')
    def test_get_openstack_token_unscoped_fail(self, mock_urlopen):
        """Test get_openstack_token returns None when unscoped token is not found."""
        mock_unscoped_res = unittest.mock.MagicMock()
        mock_unscoped_res.info.return_value = {}
        mock_unscoped_res.__enter__.return_value = mock_unscoped_res

        mock_urlopen.return_value = mock_unscoped_res

        token = ktoken.K2hr3Token.get_openstack_token(
            "http://keystone:5000/v3/auth/tokens",
            "demo", "secret", "myproject"
        )
        self.assertIsNone(token)

    @patch('urllib.request.urlopen')
    def test_get_openstack_token_scoped_fail(self, mock_urlopen):
        """Test get_openstack_token returns None when scoped token is not found."""
        mock_unscoped_res = unittest.mock.MagicMock()
        mock_unscoped_res.info.return_value = {'X-Subject-Token': 'unscoped_token_val'}
        mock_unscoped_res.__enter__.return_value = mock_unscoped_res

        mock_scoped_res = unittest.mock.MagicMock()
        mock_scoped_res.info.return_value = {}
        mock_scoped_res.__enter__.return_value = mock_scoped_res

        mock_urlopen.side_effect = [mock_unscoped_res, mock_scoped_res]

        token = ktoken.K2hr3Token.get_openstack_token(
            "http://keystone:5000/v3/auth/tokens",
            "demo", "secret", "myproject"
        )
        self.assertIsNone(token)


class TestK2hr3RoleToken(unittest.TestCase):
    """Tests the K2hr3RoleToken class."""

    def setUp(self):
        """Sets up a test case."""
        self.base_url = "http://127.0.0.1:18080"
        self.r3token = "my_r3_token"
        self.role = "my_role"
        self.expire = 3600

    def test_role_token_construct(self):
        """Test K2hr3RoleToken construction."""
        role_token = ktoken.K2hr3RoleToken(self.r3token, self.role, self.expire)
        self.assertEqual(role_token.r3token, self.r3token)
        self.assertEqual(role_token.role, self.role)
        self.assertEqual(role_token.expire, self.expire)
        self.assertEqual(role_token.headers, {
            'Content-Type': 'application/json',
            'x-auth-token': f'U={self.r3token}'
        })
        self.assertIn('<K2hr3RoleToken', repr(role_token))

    def test_role_token_validation_error(self):
        """Test K2hr3RoleToken raises K2hr3Exception on invalid types."""
        from k2hr3client.exception import K2hr3Exception
        with self.assertRaises(K2hr3Exception):
            ktoken.K2hr3RoleToken(self.r3token, 123, self.expire)  # role not str
        with self.assertRaises(K2hr3Exception):
            ktoken.K2hr3RoleToken(self.r3token, self.role, "invalid_expire")  # expire not int

    def test_role_token_token_property(self):
        """Test K2hr3RoleToken token property."""
        role_token = ktoken.K2hr3RoleToken(self.r3token, self.role, self.expire)
        hdrs = HTTPMessage()
        hdrs['content-type'] = 'application/json'
        role_token.set_response(code=200, url=self.base_url, headers=hdrs,
                                body=json.dumps({'result': True, 'token': 'role_token_xyz'}))
        self.assertEqual(role_token.token, 'role_token_xyz')

    @patch('k2hr3client.http.K2hr3Http._HTTP_REQUEST_METHOD')
    def test_role_token_get(self, mock_HTTP_REQUEST_METHOD):
        """Test K2hr3RoleToken via GET."""
        role_token = ktoken.K2hr3RoleToken(self.r3token, self.role, self.expire)
        httpreq = khttp.K2hr3Http(self.base_url)
        self.assertTrue(httpreq.GET(role_token))
        self.assertEqual(httpreq.url, f"{self.base_url}/v1/role/token/{self.role}")
        self.assertEqual(role_token._api_path(ktoken.K2hr3HTTPMethod.POST), None)


class TestK2hr3RoleTokenList(unittest.TestCase):
    """Tests the K2hr3RoleTokenList class."""

    def setUp(self):
        """Sets up a test case."""
        self.base_url = "http://127.0.0.1:18080"
        self.r3token = "my_r3_token"
        self.role = "my_role"
        self.expand = True

    def test_role_token_list_construct(self):
        """Test K2hr3RoleTokenList construction."""
        token_list = ktoken.K2hr3RoleTokenList(self.r3token, self.role, self.expand)
        self.assertEqual(token_list.r3token, self.r3token)
        self.assertEqual(token_list.role, self.role)
        self.assertEqual(token_list.expand, self.expand)
        self.assertEqual(token_list.headers, {
            'Content-Type': 'application/json',
            'x-auth-token': f'U={self.r3token}'
        })
        self.assertIn('<K2hr3RoleTokenList', repr(token_list))

    def test_role_token_list_validation_error(self):
        """Test K2hr3RoleTokenList raises K2hr3Exception on invalid types."""
        from k2hr3client.exception import K2hr3Exception
        with self.assertRaises(K2hr3Exception):
            ktoken.K2hr3RoleTokenList(self.r3token, 123, self.expand)  # role not str
        with self.assertRaises(K2hr3Exception):
            ktoken.K2hr3RoleTokenList(self.r3token, self.role, "not_a_bool")  # expand not bool

    def test_role_token_list_registerpath(self):
        """Test K2hr3RoleTokenList registerpath method."""
        token_list = ktoken.K2hr3RoleTokenList(self.r3token, self.role, self.expand)
        hdrs = HTTPMessage()
        hdrs['content-type'] = 'application/json'
        token_list.set_response(code=200, url=self.base_url, headers=hdrs,
                                body=json.dumps({
                                    'result': True,
                                    'tokens': {
                                        'tok_123': {'registerpath': '/path/to/register'}
                                    }
                                }))
        self.assertEqual(token_list.registerpath('tok_123'), '/path/to/register')

    @patch('k2hr3client.http.K2hr3Http._HTTP_REQUEST_METHOD')
    def test_role_token_list_get(self, mock_HTTP_REQUEST_METHOD):
        """Test K2hr3RoleTokenList via GET."""
        token_list = ktoken.K2hr3RoleTokenList(self.r3token, self.role, self.expand)
        httpreq = khttp.K2hr3Http(self.base_url)
        self.assertTrue(httpreq.GET(token_list))
        self.assertEqual(httpreq.url, f"{self.base_url}/v1/role/token/list/{self.role}")
        self.assertEqual(token_list._api_path(ktoken.K2hr3HTTPMethod.POST), None)


#
# Local variables:
# tab-width: 4
# c-basic-offset: 4
# End:
# vim600: expandtab sw=4 ts=4 fdm=marker
# vim<600: expandtab sw=4 ts=4
#
#
