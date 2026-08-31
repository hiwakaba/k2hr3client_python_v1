# -*- Coding: utf-8 -*-
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
import urllib

from k2hr3client import http as khttp
from k2hr3client import role as krole

LOG = logging.getLogger(__name__)


class TestK2hr3Role(unittest.TestCase):
    """Tests the K2hr3Role class.

    Simple usage(this class only):
    $ python -m unittest tests/test_role.py

    Simple usage(all):
    $ python -m unittest tests
    """
    def setUp(self):
        """Sets up a test case."""
        self.base_url = "http://127.0.0.1:18080"
        self.token = "testtoken"
        self.name = "testrole"
        POLICY_PATH = "yrn:yahoo:::demo:policy:my_policy"
        self.policies = [POLICY_PATH]
        self.alias = []
        self.host = krole.K2hr3RoleHost(
            'localhost', '1024', 'testcuk', 'testextra',
            'testtag', '10.0.0.1', '172.24.4.1'
        )
        self.clear_hostname = False
        self.clear_ips = False
        self.role_token_string = "teststring"

    def tearDown(self):
        """Tears down a test case."""

    def test_k2hr3role_construct(self):
        """Creates a K2hr3Resoiurce  instance."""
        myrole = krole.K2hr3Role(self.token)
        self.assertIsInstance(myrole, krole.K2hr3Role)

    def test_k2hr3role_repr(self):
        """Represent a K2hr3Role instance."""
        myrole = krole.K2hr3Role(self.token)
        # Note: The order of _error and _code is unknown!
        self.assertRegex(repr(myrole), '<K2hr3Role .*>')

    @patch('k2hr3client.http.K2hr3Http._HTTP_REQUEST_METHOD')
    def test_role_create_role_using_post(self, mock_HTTP_REQUEST_METHOD):
        myrole = krole.K2hr3Role(self.token)
        """Get root path."""
        self.assertEqual(myrole.r3token, self.token)
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': 'U=testtoken'
        }
        self.assertEqual(myrole.headers, headers)
        myrole.create(self.name, self.policies, self.alias)

        httpreq = khttp.K2hr3Http(self.base_url)
        self.assertTrue(httpreq.POST(myrole))

        # 1. assert URL
        self.assertEqual(httpreq.url, f"{self.base_url}/v1/role")
        # 2. assert URL params
        self.assertEqual(myrole.urlparams, None)
        # 3. assert Request headers
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': f'U={self.token}'
        }
        self.assertEqual(myrole.headers, headers)
        # 4. assert Request body
        import json
        python_data = json.loads(krole._ROLE_API_CREATE_ROLE)
        python_data['role']['name'] = self.name
        python_data['role']['policies'] = self.policies
        python_data['role']['alias'] = self.alias
        body = json.dumps(python_data)
        self.assertEqual(myrole.body, body)

    @patch('k2hr3client.http.K2hr3Http._HTTP_REQUEST_METHOD')
    def test_role_create_role_using_put(self, mock_HTTP_REQUEST_METHOD):
        myrole = krole.K2hr3Role(self.token)
        """Get root path."""
        self.assertEqual(myrole.r3token, self.token)
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': 'U=testtoken'
        }
        self.assertEqual(myrole.headers, headers)
        myrole.create(self.name, self.policies, self.alias)

        httpreq = khttp.K2hr3Http(self.base_url)
        self.assertTrue(httpreq.PUT(myrole))

        # 1. assert URL
        self.assertEqual(httpreq.url, f"{self.base_url}/v1/role")
        # 2. assert URL params
        s_s_urlparams = {
            'name': self.name,
            'policies': self.policies,
            'alias': self.alias
        }
        self.assertEqual(myrole.urlparams, json.dumps(s_s_urlparams))
        s_urlparams = urllib.parse.urlencode(s_s_urlparams)
        self.assertEqual(httpreq.urlparams, f"{s_urlparams}")
        # 3. assert Request headers
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': f'U={self.token}'
        }
        self.assertEqual(myrole.headers, headers)
        # 4. assert Request body
        self.assertEqual(myrole.body, None)

    @patch('k2hr3client.http.K2hr3Http._HTTP_REQUEST_METHOD')
    def test_role_add_member_using_post(self, mock_HTTP_REQUEST_METHOD):
        myrole = krole.K2hr3Role(self.token)
        """Get root path."""
        self.assertEqual(myrole.r3token, self.token)
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': 'U=testtoken'
        }
        self.assertEqual(myrole.headers, headers)
        myrole.add_member(self.name, self.host, self.clear_hostname,
                          self.clear_ips)

        httpreq = khttp.K2hr3Http(self.base_url)
        self.assertTrue(httpreq.POST(myrole))

        # 1. assert URL
        self.assertEqual(httpreq.url, f"{self.base_url}/v1/role/{self.name}")
        # 2. assert URL params
        self.assertEqual(myrole.urlparams, None)
        # 3. assert Request headers
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': f'U={self.token}'
        }
        self.assertEqual(myrole.headers, headers)
        # 4. assert Request body
        import json
        python_data = json.loads(krole._ROLE_API_ADD_MEMBER)
        python_data['host']['host'] = self.host.host
        python_data['host']['port'] = self.host.port
        python_data['host']['cuk'] = self.host.cuk
        python_data['host']['extra'] = self.host.extra
        python_data['host']['tag'] = self.host.tag
        python_data['host']['inboundip'] = self.host.inboundip
        python_data['host']['outboundip'] = self.host.outboundip
        body = json.dumps(python_data)
        self.assertEqual(myrole.body, body)

    @patch('k2hr3client.http.K2hr3Http._HTTP_REQUEST_METHOD')
    def test_role_add_member_using_put(self, mock_HTTP_REQUEST_METHOD):
        myrole = krole.K2hr3Role(self.token)
        """Get root path."""
        self.assertEqual(myrole.r3token, self.token)
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': f'U={self.token}'
        }
        self.assertEqual(myrole.headers, headers)
        myrole.add_member(self.name, self.host, self.policies, self.alias)

        httpreq = khttp.K2hr3Http(self.base_url)
        self.assertTrue(httpreq.PUT(myrole))

        # 1. assert URL
        self.assertEqual(httpreq.url, f"{self.base_url}/v1/role/{self.name}")
        # 2. assert URL params
        s_s_urlparams = {
            'host': self.host.host,
            'port': self.host.port,
            'cuk': self.host.cuk,
            'extra': self.host.extra,
            'tag': self.host.tag,
            'inboundip': self.host.inboundip,
            'outboundip': self.host.outboundip
        }
        self.assertEqual(myrole.urlparams, json.dumps(s_s_urlparams))
        s_urlparams = urllib.parse.urlencode(s_s_urlparams)
        self.assertEqual(httpreq.urlparams, f"{s_urlparams}")
        # 3. assert Request headers
        self.assertEqual(myrole.headers, headers)
        # 4. assert Request body
        self.assertEqual(myrole.body, None)

    @patch('k2hr3client.http.K2hr3Http._HTTP_REQUEST_METHOD')
    def test_role_add_member_with_roletoken_using_put(
            self, mock_HTTP_REQUEST_METHOD):
        myrole = krole.K2hr3Role(self.token, krole.K2hr3TokenType.ROLE_TOKEN)
        """Get root path."""
        self.assertEqual(myrole.r3token, self.token)
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': f'R={self.token}'
        }
        self.assertEqual(myrole.headers, headers)

        myrole.add_member_with_roletoken(
            self.name, self.host.port, self.host.cuk, self.host.extra,
            self.host.tag, self.host.inboundip, self.host.outboundip)

        httpreq = khttp.K2hr3Http(self.base_url)
        self.assertTrue(httpreq.PUT(myrole))

        # 1. assert URL
        self.assertEqual(httpreq.url, f"{self.base_url}/v1/role/{self.name}")
        # 2. assert URL params
        s_s_urlparams = {
            'port': self.host.port,
            'cuk': self.host.cuk,
            'extra': self.host.extra,
            'tag': self.host.tag,
            'inboundip': self.host.inboundip,
            'outboundip': self.host.outboundip
        }
        self.assertEqual(myrole.urlparams, json.dumps(s_s_urlparams))
        s_urlparams = urllib.parse.urlencode(s_s_urlparams)
        self.assertEqual(httpreq.urlparams, f"{s_urlparams}")
        # 3. assert Request headers
        self.assertEqual(myrole.headers, headers)
        # 4. assert Request body
        self.assertEqual(myrole.body, None)

    @patch('k2hr3client.http.K2hr3Http._HTTP_REQUEST_METHOD')
    def test_role_get(self, mock_HTTP_REQUEST_METHOD):
        myrole = krole.K2hr3Role(self.token)
        """Get root path."""
        self.assertEqual(myrole.r3token, self.token)
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': f'U={self.token}'
        }
        self.assertEqual(myrole.headers, headers)

        myrole.get(self.name)

        httpreq = khttp.K2hr3Http(self.base_url)
        self.assertTrue(httpreq.GET(myrole))

        # 1. assert URL
        self.assertEqual(httpreq.url, f"{self.base_url}/v1/role/{self.name}")
        # 2. assert URL params
        s_s_urlparams = {
            'expand': True
        }
        self.assertEqual(myrole.urlparams, json.dumps(s_s_urlparams))
        s_urlparams = urllib.parse.urlencode(s_s_urlparams)
        self.assertEqual(httpreq.urlparams, f"{s_urlparams}")
        # 3. assert Request headers
        self.assertEqual(myrole.headers, headers)
        # 4. assert Request body
        self.assertEqual(myrole.body, None)

    @patch('k2hr3client.http.K2hr3Http._HTTP_REQUEST_METHOD')
    def test_get_token_list(self, mock_HTTP_REQUEST_METHOD):
        myrole = krole.K2hr3Role(self.token)
        """Get root path."""
        self.assertEqual(myrole.r3token, self.token)
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': f'U={self.token}'
        }
        self.assertEqual(myrole.headers, headers)

        myrole.get_token_list(self.name)

        httpreq = khttp.K2hr3Http(self.base_url)
        self.assertTrue(httpreq.GET(myrole))

        # 1. assert URL
        self.assertEqual(httpreq.url, f"{self.base_url}/v1/role/token/list/{self.name}") # noqa
        # 2. assert URL params
        s_s_urlparams = {
            'expand': True
        }
        self.assertEqual(myrole.urlparams, json.dumps(s_s_urlparams))
        s_urlparams = urllib.parse.urlencode(s_s_urlparams)
        self.assertEqual(httpreq.urlparams, f"{s_urlparams}")
        # 3. assert Request headers
        self.assertEqual(myrole.headers, headers)
        # 4. assert Request body
        self.assertEqual(myrole.body, None)

    @patch('k2hr3client.http.K2hr3Http._HTTP_REQUEST_METHOD')
    def test_validate(self, mock_HTTP_REQUEST_METHOD):
        myrole = krole.K2hr3Role(self.token)
        """Get root path."""
        self.assertEqual(myrole.r3token, self.token)
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': f'U={self.token}'
        }
        self.assertEqual(myrole.headers, headers)

        myrole.validate_role(self.name)

        httpreq = khttp.K2hr3Http(self.base_url)
        self.assertTrue(httpreq.HEAD(myrole))

        # 1. assert URL
        self.assertEqual(httpreq.url, f"{self.base_url}/v1/role/{self.name}")
        # 2. assert URL params
        self.assertEqual(httpreq.urlparams, None)
        # 3. assert Request headers
        self.assertEqual(myrole.headers, headers)
        # 4. assert Request body
        self.assertEqual(myrole.body, None)

    @patch('k2hr3client.http.K2hr3Http._HTTP_REQUEST_METHOD')
    def test_delete_role(self, mock_HTTP_REQUEST_METHOD):
        myrole = krole.K2hr3Role(self.token)
        """Get root path."""
        self.assertEqual(myrole.r3token, self.token)
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': f'U={self.token}'
        }
        self.assertEqual(myrole.headers, headers)

        myrole.delete(self.name)

        httpreq = khttp.K2hr3Http(self.base_url)
        self.assertTrue(httpreq.DELETE(myrole))

        # 1. assert URL
        self.assertEqual(httpreq.url, f"{self.base_url}/v1/role/{self.name}")
        # 2. assert URL params
        self.assertEqual(httpreq.urlparams, None)
        # 3. assert Request headers
        self.assertEqual(myrole.headers, headers)
        # 4. assert Request body
        self.assertEqual(myrole.body, None)

    @patch('k2hr3client.http.K2hr3Http._HTTP_REQUEST_METHOD')
    def test_role_delete_member(self, mock_HTTP_REQUEST_METHOD):
        myrole = krole.K2hr3Role(self.token)
        """Get root path."""
        self.assertEqual(myrole.r3token, self.token)
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': f'U={self.token}'
        }
        self.assertEqual(myrole.headers, headers)
        myrole.delete_member(self.name, self.host.host, self.host.port,
                             self.host.cuk)

        httpreq = khttp.K2hr3Http(self.base_url)
        self.assertTrue(httpreq.DELETE(myrole))

        # 1. assert URL
        self.assertEqual(httpreq.url, f"{self.base_url}/v1/role/{self.name}")
        # 2. assert URL params
        s_s_urlparams = {
            'host': self.host.host,
            'port': self.host.port,
            'cuk': self.host.cuk,
        }
        self.assertEqual(myrole.urlparams, json.dumps(s_s_urlparams))
        s_urlparams = urllib.parse.urlencode(s_s_urlparams)
        self.assertEqual(httpreq.urlparams, f"{s_urlparams}")
        # 3. assert Request headers
        self.assertEqual(myrole.headers, headers)
        # 4. assert Request body
        self.assertEqual(myrole.body, None)

    @patch('k2hr3client.http.K2hr3Http._HTTP_REQUEST_METHOD')
    def test_role_delete_member_with_roletoken(self, mock_HTTP_REQUEST_METHOD):
        myrole = krole.K2hr3Role(self.token, krole.K2hr3TokenType.NO_TOKEN)
        """Get root path."""
        self.assertEqual(myrole.r3token, self.token)
        headers = {
            'Content-Type': 'application/json'
        }
        self.assertEqual(myrole.headers, headers)

        myrole.delete_member_wo_roletoken(self.host.cuk)

        httpreq = khttp.K2hr3Http(self.base_url)
        self.assertTrue(httpreq.DELETE(myrole))

        # 1. assert URL
        self.assertEqual(httpreq.url, f"{self.base_url}/v1/role")
        # 2. assert URL params
        s_s_urlparams = {
            'cuk': self.host.cuk,
        }
        self.assertEqual(myrole.urlparams, json.dumps(s_s_urlparams))
        s_urlparams = urllib.parse.urlencode(s_s_urlparams)
        self.assertEqual(httpreq.urlparams, f"{s_urlparams}")
        # 3. assert Request headers
        self.assertEqual(myrole.headers, headers)
        # 4. assert Request body
        self.assertEqual(myrole.body, None)

    @patch('k2hr3client.http.K2hr3Http._HTTP_REQUEST_METHOD')
    def test_role_delete_roletoken(self, mock_HTTP_REQUEST_METHOD):
        myrole = krole.K2hr3Role(self.token, krole.K2hr3TokenType.ROLE_TOKEN)
        """Get root path."""
        self.assertEqual(myrole.r3token, self.token)
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': f'R={self.token}'
        }
        self.assertEqual(myrole.headers, headers)

        myrole.delete_roletoken(self.name, self.host.port, self.host.cuk)

        httpreq = khttp.K2hr3Http(self.base_url)
        self.assertTrue(httpreq.DELETE(myrole))

        # 1. assert URL
        self.assertEqual(httpreq.url, f"{self.base_url}/v1/role/{self.name}")
        # 2. assert URL params
        s_s_urlparams = {
            'port': self.host.port,
            'cuk': self.host.cuk,
        }
        self.assertEqual(myrole.urlparams, json.dumps(s_s_urlparams))
        s_urlparams = urllib.parse.urlencode(s_s_urlparams)
        self.assertEqual(httpreq.urlparams, f"{s_urlparams}")
        # 3. assert Request headers
        self.assertEqual(myrole.headers, headers)
        # 4. assert Request body
        self.assertEqual(myrole.body, None)

    @patch('k2hr3client.http.K2hr3Http._HTTP_REQUEST_METHOD')
    def test_role_delete_roletoken_with_usertoken(self,
                                                  mock_HTTP_REQUEST_METHOD):
        myrole = krole.K2hr3Role(self.token)
        """Get root path."""
        self.assertEqual(myrole.r3token, self.token)
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': f'U={self.token}'
        }
        self.assertEqual(myrole.headers, headers)

        myrole.delete_roletoken_with_string(self.role_token_string)

        httpreq = khttp.K2hr3Http(self.base_url)
        self.assertTrue(httpreq.DELETE(myrole))

        # 1. assert URL
        self.assertEqual(httpreq.url, f"{self.base_url}/v1/role/token/{self.role_token_string}") # noqa
        # 2. assert URL params
        s_s_urlparams = None
        self.assertEqual(httpreq.urlparams, s_s_urlparams)
        # 3. assert Request headers
        self.assertEqual(myrole.headers, headers)
        # 4. assert Request body
        self.assertEqual(myrole.body, None)

    def test_role_deprecated_role_name_arguments(self):
        """Test deprecated role_name argument generates warning."""
        myrole = krole.K2hr3Role(self.token)
        with self.assertWarns(DeprecationWarning):
            myrole.create(None, self.policies, self.alias, role_name="legacy_role")
        self.assertEqual(myrole.name, "legacy_role")

        with self.assertWarns(DeprecationWarning):
            myrole.add_member(None, "myhost", True, "1.1.1.1", role_name="legacy_role2")
        self.assertEqual(myrole.name, "legacy_role2")

        with self.assertWarns(DeprecationWarning):
            myrole.add_members(None, "myhosts", True, "1.1.1.1", role_name="legacy_role3")
        self.assertEqual(myrole.name, "legacy_role3")

        with self.assertWarns(DeprecationWarning):
            myrole.add_member_with_roletoken(None, "80", "cuk", "extra", "tag",
                                            "10.0.0.1", "10.0.0.2", role_name="legacy_role4")
        self.assertEqual(myrole.name, "legacy_role4")

        with self.assertWarns(DeprecationWarning):
            myrole.get(None, True, role_name="legacy_role5")
        self.assertEqual(myrole.name, "legacy_role5")

        with self.assertWarns(DeprecationWarning):
            myrole.get_token_list(None, True, role_name="legacy_role6")
        self.assertEqual(myrole.name, "legacy_role6")

        with self.assertWarns(DeprecationWarning):
            myrole.validate_role(None, role_name="legacy_role7")
        self.assertEqual(myrole.name, "legacy_role7")

        with self.assertWarns(DeprecationWarning):
            myrole.delete(None, role_name="legacy_role8")
        self.assertEqual(myrole.name, "legacy_role8")

        with self.assertWarns(DeprecationWarning):
            myrole.delete_member(None, "host", "80", "cuk", role_name="legacy_role9")
        self.assertEqual(myrole.name, "legacy_role9")

        with self.assertWarns(DeprecationWarning):
            myrole.delete_roletoken(None, "80", "cuk", role_name="legacy_role10")
        self.assertEqual(myrole.name, "legacy_role10")

    @patch('k2hr3client.http.K2hr3Http._HTTP_REQUEST_METHOD')
    def test_role_add_member_using_roletoken_post(self, mock_HTTP_REQUEST_METHOD):
        """Test POST add_member_with_roletoken using role_token."""
        myrole = krole.K2hr3Role("my_role_token", token_type=krole.K2hr3TokenType.ROLE_TOKEN)
        myrole.name = self.name
        myrole.host = self.host
        myrole.api_id = 5
        httpreq = khttp.K2hr3Http(self.base_url)
        self.assertTrue(httpreq.POST(myrole))
        self.assertEqual(httpreq.url, f"{self.base_url}/v1/role/{self.name}")

    def test_role_no_token_type(self):
        """Test K2hr3Role with NO_TOKEN type."""
        myrole = krole.K2hr3Role(None, token_type=krole.K2hr3TokenType.NO_TOKEN)
        self.assertEqual(myrole.headers, {'Content-Type': 'application/json'})

    @patch('k2hr3client.http.K2hr3Http._HTTP_REQUEST_METHOD')
    def test_role_add_members_put(self, mock_HTTP_REQUEST_METHOD):
        """Test PUT add_members."""
        myrole = krole.K2hr3Role(self.token)
        myrole.add_members(self.name, "hosts", True, "1.1.1.1")
        httpreq = khttp.K2hr3Http(self.base_url)
        self.assertTrue(httpreq.PUT(myrole))
        self.assertEqual(httpreq.url, f"{self.base_url}/v1/role/{self.name}")

    def test_role_api_path_unsupported(self):
        """Test _api_path returns None on unsupported method."""
        myrole = krole.K2hr3Role(self.token)
        myrole.api_id = 999
        self.assertIsNone(myrole._api_path(krole.K2hr3HTTPMethod.DELETE))

    def test_role_host_properties(self):
        """Test K2hr3RoleHost constructor and properties."""
        host = krole.K2hr3RoleHost('host1', '8080', 'cuk1', 'extra1', 'tag1', '1.1.1.1', '2.2.2.2')
        self.assertEqual(host.host, 'host1')
        self.assertEqual(host.port, '8080')
        self.assertEqual(host.cuk, 'cuk1')
        self.assertEqual(host.extra, 'extra1')
        self.assertEqual(host.tag, 'tag1')
        self.assertEqual(host.inboundip, '1.1.1.1')
        self.assertEqual(host.outboundip, '2.2.2.2')


#
# Local variables:
# tab-width: 4
# c-basic-offset: 4
# End:
# vim600: expandtab sw=4 ts=4 fdm=marker
# vim<600: expandtab sw=4 ts=4
#
