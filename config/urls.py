from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.urls import path, include
from django.views.generic import RedirectView

from apps.core.views_favicon import favicon

urlpatterns = [
    path('favicon.ico', favicon, name='favicon'),
    path('admin/favicon.ico', favicon, name='admin_favicon'),
    path('admin/media-library/', include('apps.media_library.urls')),
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('rosetta/', include('rosetta.urls')),
    path('api/contact/', include('apps.contact.urls')),
    path('', RedirectView.as_view(url='/cs/', permanent=False)),
] + i18n_patterns(
    path('', include('apps.pages.urls', namespace='pages')),
    path('masaze/', include('apps.services.urls', namespace='services')),
    path('masazistky/', include('apps.therapists.urls', namespace='therapists')),
    path('rozvrh/', include('apps.schedule.urls', namespace='schedule')),
    path('blog/', include('apps.blog.urls', namespace='blog')),
    path('booking/', include('apps.booking.urls', namespace='booking')),
    prefix_default_language=True,
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
