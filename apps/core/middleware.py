import os
import re

from django.conf import settings
from django.http import HttpResponsePermanentRedirect
from django.http.request import validate_host
from django.utils import translation

from .admin_locale import ADMIN_LOCALE, ADMIN_PATH_PREFIXES

SUPPORTED_LANGS = frozenset({'cs', 'en', 'ru'})
PUBLIC_SECTIONS = frozenset({
    'masaze', 'masazistky', 'rozvrh', 'blog', 'kontakty',
    'o-nas', 'pravidla-salonu', 'soukromi', 'booking',
})
SKIP_PREFIX_PATHS = (
    '/static/', '/media/', '/admin/', '/api/', '/i18n/', '/rosetta/',
    '/favicon.ico', '/admin/favicon.ico',
)


class MissingLanguagePrefixMiddleware:
    """Redirect /masaze/... → /cs/masaze/... when language prefix is missing."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        if any(path.startswith(prefix) for prefix in SKIP_PREFIX_PATHS):
            return self.get_response(request)

        parts = [part for part in path.split('/') if part]
        if parts and parts[0] not in SUPPORTED_LANGS and parts[0] in PUBLIC_SECTIONS:
            lang = _preferred_lang(request)
            tail = '/'.join(parts)
            target = f'/{lang}/{tail}/'
            query = request.META.get('QUERY_STRING', '')
            if query:
                target = f'{target}?{query}'
            return HttpResponsePermanentRedirect(target)

        return self.get_response(request)


def _preferred_lang(request) -> str:
    cookie = request.COOKIES.get(getattr(settings, 'LANGUAGE_COOKIE_NAME', 'django_language'), '')
    code = (cookie or '')[:2].lower()
    if code in SUPPORTED_LANGS:
        return code

    accept = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
    for chunk in accept.split(','):
        token = chunk.strip().split(';')[0].lower()
        match = re.match(r'([a-z]{2})', token)
        if match and match.group(1) in SUPPORTED_LANGS:
            return match.group(1)
    return 'cs'


class AdminUkrainianMiddleware:
    """Force Ukrainian only inside Django admin routes.

    Public site keeps cs / en / ru via LocaleMiddleware and i18n URL prefixes.
    ``uk`` is intentionally absent from ``LANGUAGES`` so visitors cannot switch to it.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith(ADMIN_PATH_PREFIXES):
            with translation.override(ADMIN_LOCALE):
                response = self.get_response(request)
                return response
        return self.get_response(request)


class RenderHostMiddleware:
    """Normalize Host for Render probes that send an internal IP instead of the service hostname."""

    def __init__(self, get_response):
        self.get_response = get_response
        self.render_hostname = os.environ.get('RENDER_EXTERNAL_HOSTNAME', '')

    def __call__(self, request):
        if self.render_hostname:
            host = request.META.get('HTTP_HOST', '').split(':')[0]
            user_agent = request.META.get('HTTP_USER_AGENT', '')
            is_render_probe = user_agent in ('Render/1.0', 'Go-http-client/1.1')
            if host and is_render_probe and not validate_host(host, settings.ALLOWED_HOSTS):
                request.META['HTTP_HOST'] = self.render_hostname
        return self.get_response(request)
