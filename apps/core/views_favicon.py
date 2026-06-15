from django.conf import settings
from django.http import FileResponse, Http404


def favicon(request):
    """Serve favicon from assets (works before collectstatic)."""
    path = settings.BASE_DIR / 'assets' / 'img' / 'icons' / 'favicon.ico'
    if not path.is_file():
        raise Http404
    return FileResponse(path.open('rb'), content_type='image/vnd.microsoft.icon')
