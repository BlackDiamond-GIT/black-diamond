import os

from django.conf import settings
from django.http.request import validate_host


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
