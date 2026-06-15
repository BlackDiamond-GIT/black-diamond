"""Admin registration for core models."""

from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from apps.core.unfold_admin import BDModelAdmin

from . import admin_pages  # noqa: F401
from .models import LegacyRedirect, SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(BDModelAdmin):
    readonly_fields = ('rotation_status_display',)

    fieldsets = (
        (_('Rotating phones'), {
            'fields': (
                'rotation_phone_1', 'rotation_phone_2', 'rotation_phone_3',
                'phone_rotation_hours', 'rotation_status_display',
            ),
        }),
        (_('Contact'), {
            'fields': (
                'email', 'address', 'location_phone_1', 'map_url', 'maps_embed_url',
                'address_2', 'location_phone_2', 'map_url_2', 'maps_embed_url_2',
            ),
        }),
        (_('Opening Hours'), {'fields': ('hours', 'hours_en', 'hours_ru')}),
        (_('Social'), {'fields': ('instagram_url', 'telegram_url')}),
        (_('SEO defaults'), {
            'fields': ('default_meta_title', 'default_meta_description', 'og_image_url'),
        }),
        (_('Currency display'), {
            'fields': ('eur_rate', 'usd_rate', 'show_eur', 'show_usd'),
        }),
        (_('Settings'), {'fields': ('require_age_confirmation',)}),
    )

    @admin.display(description=_('Rotation status (Europe/Prague)'))
    def rotation_status_display(self, obj: SiteSettings) -> str:
        preview = obj.get_rotation_preview()
        return format_html(
            '<strong>{}</strong><br>{}: {}/{}<br>{}: {}<br>{}: {}',
            preview['active'],
            _('Slot'), preview['slot'], preview['total'],
            _('Prague time now'), preview['prague_now'],
            _('Next switch at'), preview['next_switch'],
        )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj, _ = SiteSettings.objects.get_or_create(pk=1)
        return HttpResponseRedirect(
            reverse('admin:core_sitesettings_change', args=[obj.pk])
        )


@admin.register(LegacyRedirect)
class LegacyRedirectAdmin(BDModelAdmin):
    list_display = ('old_path', 'new_path', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('old_path', 'new_path')
    list_editable = ('is_active',)
