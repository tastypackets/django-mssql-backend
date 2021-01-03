from unittest import skip
from django.test.runner import DiscoverRunner
from django.conf import settings


EXCLUDED_TESTS = getattr(settings, 'EXCLUDED_TESTS', [])


class ExcludeTestSuiteRunner(DiscoverRunner):
    def build_suite(self, *args, **kwargs):
        suite = super().build_suite(*args, **kwargs)
        for case in suite:
            cls = case.__class__
            for attr in dir(cls):
                if not attr.startswith('test_'):
                    continue
                fullname = f'{cls.__module__}.{cls.__name__}.{attr}'
                if len(list(filter(fullname.startswith, EXCLUDED_TESTS))):
                    setattr(cls, attr, skip('Does not work on MSSQL')(getattr(cls, attr)))

        return suite
