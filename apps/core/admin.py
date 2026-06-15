from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Адреса салону'), {
            'fields': ('street_name', 'street_number', 'postal_code', 'city', 'country_code'),
        }),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
