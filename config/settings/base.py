from pathlib import Path
import environ
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env(
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, ['localhost', '127.0.0.1']),
)
environ.Env.read_env(BASE_DIR / '.env')

SECRET_KEY = env('SECRET_KEY')
ALLOWED_HOSTS = env('ALLOWED_HOSTS')

INSTALLED_APPS = [
    'unfold',
    'unfold.contrib.filters',
    'unfold.contrib.inlines',
    'tinymce',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'rosetta',
    'apps.core',
    'apps.pages',
    'apps.branches',
    'apps.services',
    'apps.therapists',
    'apps.schedule',
    'apps.blog',
    'apps.contact',
    'apps.faq',
    'apps.media_library',
    'apps.booking',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'apps.core.middleware.AdminUkrainianMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'apps.core.context_processors.site_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': env.db(default='sqlite:///db.sqlite3')
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'cs'
LANGUAGES = [
    ('cs', 'Čeština'),
    ('en', 'English'),
    ('ru', 'Русский'),
]
TIME_ZONE = 'Europe/Prague'
USE_I18N = True
USE_L10N = True
USE_TZ = True
LOCALE_PATHS = [BASE_DIR / 'locale']

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / env('STATIC_ROOT', default='staticfiles/')
STATICFILES_DIRS = [BASE_DIR / 'assets']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/uploads/'
MEDIA_ROOT = BASE_DIR / env('MEDIA_ROOT', default='uploads/')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = env('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = env('EMAIL_HOST', default='localhost')
EMAIL_PORT = env.int('EMAIL_PORT', default=587)
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='info@blackdiamond.cz')
CONTACT_RECIPIENT_EMAIL = env('CONTACT_RECIPIENT_EMAIL', default='info@blackdiamond.cz')

SITE_NAME = 'Black Diamond Spa'
SITE_URL = 'https://blackdiamond.cz'
SITE_PHONE = '+420 797 669 633'
SITE_EMAIL = 'info@blackdiamond.cz'
SITE_ADDRESS = 'Soukenická, 110 00 Praha 1'

CLOUDINARY_URL = env('CLOUDINARY_URL', default='')

if CLOUDINARY_URL:
    import cloudinary
    cloudinary.config(secure=True)

TIFFANY = {
    '50': '240 253 252',
    '100': '204 251 250',
    '200': '153 246 244',
    '300': '94 234 229',
    '400': '45 212 207',
    '500': '10 186 181',
    '600': '8 145 142',
    '700': '0 130 127',
    '800': '6 95 92',
    '900': '8 78 76',
    '950': '4 47 46',
}

UNFOLD = {
    'SITE_TITLE': 'Black Diamond Spa',
    'SITE_HEADER': 'Black Diamond Spa',
    'SITE_URL': '/',
    'SITE_SYMBOL': 'diamond',
    'SHOW_HISTORY': True,
    'THEME': 'dark',
    'COLORS': {
        'primary': TIFFANY,
    },
    'SIDEBAR': {
        'show_search': True,
        'show_all_applications': False,
        'navigation': [
            {
                'title': _('Settings'),
                'separator': True,
                'items': [
                    {
                        'title': _('Site Settings'),
                        'icon': 'settings',
                        'link': reverse_lazy('admin:core_sitesettings_changelist'),
                    },
                    {
                        'title': _('Branches'),
                        'icon': 'location_on',
                        'link': reverse_lazy('admin:branches_branch_changelist'),
                    },
                    {
                        'title': _('Legacy Redirects'),
                        'icon': 'link',
                        'link': reverse_lazy('admin:core_legacyredirect_changelist'),
                    },
                ],
            },
            {
                'title': _('Therapists'),
                'items': [
                    {
                        'title': _('Therapists'),
                        'icon': 'person',
                        'link': reverse_lazy('admin:therapists_therapist_changelist'),
                    },
                    {
                        'title': _('Schedule'),
                        'icon': 'calendar_today',
                        'link': reverse_lazy('admin:schedule_scheduleentry_changelist'),
                    },
                    {
                        'title': _('Photo Library'),
                        'icon': 'photo_library',
                        'link': reverse_lazy('admin:media_library_cloudinaryimage_changelist'),
                    },
                ],
            },
            {
                'title': _('Services'),
                'items': [
                    {
                        'title': _('Massage Types'),
                        'icon': 'spa',
                        'link': reverse_lazy('admin:services_service_changelist'),
                    },
                    {
                        'title': _('Prices'),
                        'icon': 'payments',
                        'link': reverse_lazy('admin:services_price_changelist'),
                    },
                    {
                        'title': _('Extras'),
                        'icon': 'add_circle',
                        'link': reverse_lazy('admin:services_extra_changelist'),
                    },
                    {
                        'title': _('HashTags'),
                        'icon': 'tag',
                        'link': reverse_lazy('admin:services_hashtag_changelist'),
                    },
                    {
                        'title': _('Languages'),
                        'icon': 'language',
                        'link': reverse_lazy('admin:services_language_changelist'),
                    },
                ],
            },
            {
                'title': _('Content'),
                'items': [
                    {
                        'title': _('Page Content'),
                        'icon': 'description',
                        'link': reverse_lazy('admin:core_contentpage_changelist'),
                    },
                    {
                        'title': _('Interior Photos'),
                        'icon': 'photo_camera',
                        'link': reverse_lazy('admin:core_interiorimage_changelist'),
                    },
                    {
                        'title': _('Blog Posts'),
                        'icon': 'article',
                        'link': reverse_lazy('admin:blog_article_changelist'),
                    },
                    {
                        'title': _('FAQ'),
                        'icon': 'quiz',
                        'link': reverse_lazy('admin:faq_faq_changelist'),
                    },
                ],
            },
            {
                'title': _('Booking'),
                'items': [
                    {
                        'title': _('Availability'),
                        'icon': 'grid_view',
                        'link': reverse_lazy('admin:booking_appointment_availability'),
                    },
                    {
                        'title': _('Appointments'),
                        'icon': 'event_available',
                        'link': reverse_lazy('admin:booking_appointment_changelist'),
                    },
                    {
                        'title': _('Booking stats'),
                        'icon': 'insights',
                        'link': reverse_lazy('admin:booking_appointment_stats'),
                    },
                    {
                        'title': _('Booking clicks'),
                        'icon': 'analytics',
                        'link': reverse_lazy('admin:booking_bookingclick_changelist'),
                    },
                    {
                        'title': _('WhatsApp Templates'),
                        'icon': 'chat',
                        'link': reverse_lazy('admin:booking_whatsapptemplate_changelist'),
                    },
                ],
            },
        ],
    },
}

TINYMCE_DEFAULT_CONFIG = {
    'height': 400,
    'menubar': False,
    'plugins': 'lists link paste',
    'toolbar': 'undo redo | bold italic | bullist numlist | link | removeformat',
    'language': 'uk',
    'skin': 'oxide-dark',
    'content_css': 'dark',
}
