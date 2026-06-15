from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from apps.core.unfold_admin import BDModelAdmin

from .models import Therapist
from .widgets import CloudinaryFKWidget, CloudinaryM2MWidget


@admin.register(Therapist)
class TherapistAdmin(BDModelAdmin):
    list_display = (
        'photo_preview', 'name', 'age', 'is_active', 'is_busy',
        'has_location', 'col_schedule', 'col_new', 'sort_order',
    )
    list_filter = ('is_active', 'is_busy', 'has_location', 'is_new', 'offers', 'languages', 'hashtags')
    list_editable = ('is_active', 'is_busy', 'has_location', 'sort_order')
    search_fields = ('name', 'slug', 'bio_cs')
    prepopulated_fields = {'slug': ('name',)}
    autocomplete_fields = ('offers', 'loves', 'extras', 'hashtags', 'languages', 'branches')
    readonly_fields = ('photo_preview',)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if 'main_cloudinary_photo' in form.base_fields:
            form.base_fields['main_cloudinary_photo'].widget = CloudinaryFKWidget(
                choices=form.base_fields['main_cloudinary_photo'].widget.choices,
            )
        if 'gallery_cloudinary' in form.base_fields:
            form.base_fields['gallery_cloudinary'].widget = CloudinaryM2MWidget(
                choices=form.base_fields['gallery_cloudinary'].widget.choices,
            )
        return form

    fieldsets = (
        (_('Identity'), {'fields': ('name', 'slug', 'sort_order', 'is_active', 'is_new')}),
        (_('Status'), {'fields': ('is_busy', 'has_location', 'has_schedule')}),
        (_('Physical'), {'fields': ('age', 'height_cm', 'weight_kg', 'bust')}),
        (_('Photos — Cloudinary Library'), {
            'fields': ('photo_preview', 'main_cloudinary_photo', 'gallery_cloudinary'),
        }),
        (_('Photos — Legacy (file / URL)'), {
            'fields': ('photo', 'main_photo_url', 'gallery_urls'),
            'classes': ('collapse',),
        }),
        (_('Czech'), {'fields': ('bio_cs', 'loves_text_cs')}),
        (_('English'), {'fields': ('bio_en', 'loves_text_en')}),
        (_('Russian'), {'fields': ('bio_ru', 'loves_text_ru')}),
        (None, {'fields': ('use_default',)}),
        (_('Services & Attributes'), {
            'fields': ('offers', 'loves', 'extras', 'hashtags', 'languages', 'branches', 'specialties'),
        }),
        (_('SEO'), {'fields': ('meta_title', 'meta_description')}),
    )

    @admin.display(description=_('Photo'))
    def photo_preview(self, obj):
        url = obj.photo_url
        if url:
            return format_html(
                '<img src="{}" style="height:60px;width:48px;object-fit:cover;border-radius:4px">',
                url,
            )
        return '—'

    @admin.display(description=_('Sched.'), boolean=True)
    def col_schedule(self, obj):
        return obj.has_schedule

    @admin.display(description=_('New'), boolean=True)
    def col_new(self, obj):
        return obj.is_new
