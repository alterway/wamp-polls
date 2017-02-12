# See https://docs.djangoproject.com/en/1.10/ref/templates/api/#writing-your-own-context-processors
from django.conf import settings

SETTINGS_VARS = ('MY_WAMP_URL', 'MY_WAMP_REALM')


def settings_values(request):
    """Exposes some settings values to the templates context"""
    return {'dj_settings': {k: getattr(settings, k, None) for k in SETTINGS_VARS}}
