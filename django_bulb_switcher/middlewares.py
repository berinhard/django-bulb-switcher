# coding:utf-8
import importlib

from django.conf import settings

from .exceptions import ImproperlyConfiguredBulbSwitcherConditions


class ContionalBulbSwitcherMiddleware(object):

    error_messages = {
        'not_configured': 'You must define BULB_SWITCHER_CONDITIONALS on your settings file.',
        'bad_format': 'BULB_SWITCHER_CONDITIONALS setting must be a dictionary containg iterables with callables.',
    }

    def process_request(self, request):
        request.VALID_BULB_SWITCHER_CONDITIONALS = []

        conditionals_config = getattr(settings, 'BULB_SWITCHER_CONDITIONALS', None)
        if conditionals_config is None:
            raise ImproperlyConfiguredBulbSwitcherConditions(self.error_messages['not_configured'])

        try:
            for flag, conditionals in conditionals_config.items():
                for cond in conditionals:
                    if isinstance(cond, str) or isinstance(cond, unicode):
                        path, cond_name = cond.rsplit('.', 1)
                        cond = getattr(importlib.import_module(path), cond_name)
                    if not cond(request.user):
                        break
                else:
                    request.VALID_BULB_SWITCHER_CONDITIONALS.append(flag)

        except (TypeError, AttributeError):
            raise ImproperlyConfiguredBulbSwitcherConditions(self.error_messages['bad_format'])
