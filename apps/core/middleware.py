import os

from django.conf import settings
from django.http.request import validate_host
from django.utils import translation

from .admin_locale import ADMIN_LOCALE, ADMIN_PATH_PREFIXES


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
