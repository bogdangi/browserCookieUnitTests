#!/usr/bin/env python
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import subprocess
import browserCookieUnitTests
import urllib

SHEME = 'http'
HOST = 'localhost'
PORT = 36521
URL = "%s://%s:%s"%(SHEME, HOST, PORT)


class ChromeCookie(unittest.TestCase):

    def setUp(self):
        self.server = subprocess.Popen([browserCookieUnitTests.browserCookieUnitTests.__file__[:-12] + 'cookieserver.py', str(PORT)])
        self.driver = webdriver.Chrome()

    def test_set_cookie(self):
        driver = self.driver
        params = urllib.urlencode({
            'cookie': 'Customer=WILE_E_COYOTE; Version=1; Path=/'})
        driver.get(URL + '/set/header/set-cookie?'+params)
        self.assertEqual(
            u'WILE_E_COYOTE',
            driver.get_cookie('Customer').get('value',None))

    def test_cookies_limits(self):
        driver = self.driver

        # * at least 4096 bytes per cookie (as measured by the size of the
        #   characters that comprise the cookie non-terminal in the syntax
        #   description of the Set-Cookie header)

        max_cookie_size = 4096
        params = urllib.urlencode({
            'cookie': 'Cookie4096=%s' % ('A'*(max_cookie_size-11))})
        driver.get(URL + '/set/header/set-cookie?'+params)

        self.assertEqual(
            'A'*(max_cookie_size-11),
            driver.get_cookie('Cookie4096').get('value',None))

        params = urllib.urlencode({
            'cookie': 'Cookie4097=%s' % ('A'*(max_cookie_size-10))})
        driver.get(URL + '/set/header/set-cookie?'+params)

        self.assertIsNone(driver.get_cookie('Cookie4097'))

        # * at least 20 cookies per unique host or domain name

        for i in xrange(21):
            params = urllib.urlencode({
                'cookie': 'Cookie%s=Cookie data; Version=1; Path=/' % i})
            driver.get(URL + '/set/header/set-cookie?'+params)
        self.assertTrue(20 <= len(driver.get_cookies()))

    def test_rejecting_cookies(self):
        driver = self.driver

        # * The value for the Path attribute is not a prefix of the request-
        #   URI.

        params = urllib.urlencode({
            'cookie': 'BadPath=Data; Path=/BadPath'})
        driver.get(URL + '/set/header/set-cookie?'+params)
        self.assertIsNone(driver.get_cookie('BadPath'))

        # * The value for the Domain attribute contains no embedded dots or
        #   does not start with a dot.

        params = urllib.urlencode({
            'cookie': 'BadDomain=Data; Domain=localhost'})
        driver.get(URL + '/set/header/set-cookie?'+params)
        self.assertIsNone(driver.get_cookie('BadDomain'))

        # * The value for the request-host does not domain-match the Domain
        #   attribute.

        params = urllib.urlencode({
            'cookie': 'BadDomain=Data; Domain=.com'})
        driver.get(URL + '/set/header/set-cookie?'+params)
        self.assertIsNone(driver.get_cookie('BadDomain'))

    def tearDown(self):
        self.server.kill()
        self.driver.close()

suite = unittest.TestLoader().loadTestsFromTestCase(ChromeCookie)


def run():
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    run()
