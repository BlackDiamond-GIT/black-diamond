from django.conf import settings
from django.http import HttpResponse


def robots_txt(request):
    sitemap_url = f"{settings.SITE_URL.rstrip('/')}/sitemap.xml"
    content = '\n'.join((
        'User-agent: *',
        'Allow: /',
        'Disallow: /admin/',
        'Disallow: /api/',
        'Disallow: /i18n/',
        'Disallow: /rosetta/',
        '',
        f'Sitemap: {sitemap_url}',
        '',
    ))
    return HttpResponse(content, content_type='text/plain; charset=utf-8')
