#!/usr/bin/env python

from os.path import dirname, join
import sys
from optparse import OptionParser
import warnings
import django


def configure_settings():
    from django.conf import settings

    # If DJANGO_SETTINGS_MODULE envvar exists the settings will be
    # configured by it. Otherwise it will use the parameters bellow.
    if not settings.configured:
        params = dict(
            DATABASES={
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': ':memory:',
                }
            },
            INSTALLED_APPS = (
                'django.contrib.contenttypes',
                'test.test_app'
            ),
            SITE_ID=1,
            TEST_RUNNER='django.test.simple.DjangoTestSuiteRunner',
        )

        if django.VERSION >= (1, 7):
            params.update(
                MIDDLEWARE_CLASSES=tuple()
            )

        # Configure Django's settings
        settings.configure(**params)

    return settings


def get_runner(settings):
    '''
    Asks Django for the TestRunner defined in settings or the default one.
    '''
    from django.test.utils import get_runner
    TestRunner = get_runner(settings)
    if django.VERSION >= (1, 7):
        #  I suspect this will not be necessary in next release after 1.7.0a1:
        #  See https://code.djangoproject.com/ticket/21831
        setattr(settings, 'INSTALLED_APPS',
                ['django.contrib.auth']
                + list(getattr(settings, 'INSTALLED_APPS')))
    return TestRunner(verbosity=1, interactive=True, failfast=False)


def runtests():
    settings = configure_settings()
    settings.TEST_RUNNER='django.test.runner.DiscoverRunner'
    django.setup()
    runner = get_runner(settings)
    sys.exit(runner.run_tests(['test.test_app']))


if __name__ == '__main__':
    runtests()
