# coding:utf-8
from mock import Mock
from model_mommy import mommy

from django.test import TestCase, override_settings, RequestFactory
from django.contrib.auth import get_user_model

from django_bulb_switcher.exceptions import ImproperlyConfiguredBulbSwitcherConditions
from django_bulb_switcher.middlewares import ContionalBulbSwitcherMiddleware


class ContionalBulbSwitcherMiddlewareTests(TestCase):

    def setUp(self):
        self.middleware = ContionalBulbSwitcherMiddleware()
        factory = RequestFactory()
        self.user = mommy.make(get_user_model(), username='foo')
        self.request = factory.get('/')
        self.request.user = self.user

    def test_calls_conditions_given_user_and_request(self):
        mocks = [Mock() for i in range(4)]

        BULB_SWITCHER_CONDITIONALS = {
            'flag1': mocks[:2],
            'flag2': mocks[2:],
        }
        with override_settings(BULB_SWITCHER_CONDITIONALS=BULB_SWITCHER_CONDITIONALS):
            self.middleware.process_request(self.request)

        for mock in mocks:
            mock.assert_called_once_with(self.request, self.user)

    def test_populates_flag_result_on_request(self):
        BULB_SWITCHER_CONDITIONALS = {
            'flag1': [lambda request, user: True],
            'flag2': [lambda request, user: True, lambda  request, user: False],
        }
        with override_settings(BULB_SWITCHER_CONDITIONALS=BULB_SWITCHER_CONDITIONALS):
            self.middleware.process_request(self.request)

        valid_bulb_switcher_conditionals= self.request.VALID_BULB_SWITCHER_CONDITIONALS
        self.assertEqual(1, len(valid_bulb_switcher_conditionals))
        self.assertIn('flag1', valid_bulb_switcher_conditionals)

    def test_ensure_middleware_returns_none_to_continue_middleware_processing(self):
        with override_settings(BULB_SWITCHER_CONDITIONALS={}):
            result = self.middleware.process_request(self.request)

        self.assertIsNone(result)

    def test_raises_improperly_configured_if_not_var_on_settings(self):
        self.assertRaises(
            ImproperlyConfiguredBulbSwitcherConditions,
            self.middleware.process_request,
            self.request
        )

    def test_raises_improperly_configured_if_settings_is_not_a_dict(self):
        with override_settings(BULB_SWITCHER_CONDITIONALS=[]):
            self.assertRaises(
                ImproperlyConfiguredBulbSwitcherConditions,
                self.middleware.process_request,
                self.request
            )

    def test_raises_improperly_configured_if_conditionals_are_iterables(self):
        with override_settings(BULB_SWITCHER_CONDITIONALS={'flag1': 13}):
            self.assertRaises(
                ImproperlyConfiguredBulbSwitcherConditions,
                self.middleware.process_request,
                self.request
            )

    def test_raises_improperly_configured_if_conditionals_are_not_callable_iterables(self):
        with override_settings(BULB_SWITCHER_CONDITIONALS={'flag1': [13]}):
            self.assertRaises(
                ImproperlyConfiguredBulbSwitcherConditions,
                self.middleware.process_request,
                self.request
            )

    def test_allows_string_to_import_conditional(self):
        BULB_SWITCHER_CONDITIONALS = {
            'flag1': ['test.test_app.conditionals.valid_conditional'],
            'flag2': [u'test.test_app.conditionals.invalid_conditional'],
        }
        with override_settings(BULB_SWITCHER_CONDITIONALS=BULB_SWITCHER_CONDITIONALS):
            self.middleware.process_request(self.request)

        valid_bulb_switcher_conditionals= self.request.VALID_BULB_SWITCHER_CONDITIONALS
        self.assertEqual(1, len(valid_bulb_switcher_conditionals))
        self.assertIn('flag1', valid_bulb_switcher_conditionals)
