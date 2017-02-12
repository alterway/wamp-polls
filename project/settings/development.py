from .common import *  # noqa

DEBUG = True
USE_DEBUG_TOOLBAR = False

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]']

# debug_toolbar
# -------------
# http://django-debug-toolbar.readthedocs.io/en/stable/installation.html
if USE_DEBUG_TOOLBAR:
    INTERNAL_IPS = ('127.0.0.1', '::1')
    INSTALLED_APPS.append('debug_toolbar')
    MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')
    DEBUG_TOOLBAR_CONFIG = {
        # We already got a jQuery, don't load it twice
        # see http://django-debug-toolbar.readthedocs.io/en/stable/configuration.html#debug-toolbar-config
        'JQUERY_URL': ''
    }
