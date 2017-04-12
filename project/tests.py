from django.test import TestCase, RequestFactory
from django.test.utils import override_settings

from .context_processors import settings_values, SETTINGS_VARS

class CtxProcessor(TestCase):

    def test_default_settings_variables(self):
        """We get all default variables for presence
        """
        request = RequestFactory()
        values = settings_values(request)
        for varname in SETTINGS_VARS:
            self.assertIn(varname, values['dj_settings'].keys())

    @override_settings(MY_WAMP_URL='stupid_url')
    def test_one_variable(self):
        """Just checking one settings variable
        """
        request = RequestFactory()
        values = settings_values(request)
        self.assertEqual(values['dj_settings']['MY_WAMP_URL'], 'stupid_url')
