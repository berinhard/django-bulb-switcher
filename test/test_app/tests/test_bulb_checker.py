# coding:utf-8
from django.test import TestCase, RequestFactory
from django_bulb_switcher import bulb_checker


class RequestFlagCheckerTests(TestCase):

    def setUp(self):
        factory = RequestFactory()
        self.request = factory.get('/')
        self.request.VALID_BULB_SWITCHER_CONDITIONALS = []

    def test_check_flag_is_on(self):
        self.assertFalse(bulb_checker.is_on(self.request, 'flag'))
        self.request.VALID_BULB_SWITCHER_CONDITIONALS.append('flag')
        self.assertTrue(bulb_checker.is_on(self.request, 'flag'))

    def test_check_flag_is_off(self):
        self.assertTrue(bulb_checker.is_off(self.request, 'flag'))
        self.request.VALID_BULB_SWITCHER_CONDITIONALS.append('flag')
        self.assertFalse(bulb_checker.is_off(self.request, 'flag'))
