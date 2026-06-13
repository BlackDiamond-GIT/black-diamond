import os

from .base import *

DEBUG = False

_render_host = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
for _host in ('127.0.0.1', _render_host):
    if _host and _host not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(_host)

MIDDLEWARE = ['apps.core.middleware.RenderHostMiddleware', *MIDDLEWARE]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', default=True)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS', default=[])
