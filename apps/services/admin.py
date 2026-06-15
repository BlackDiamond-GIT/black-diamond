from django.contrib import admin
from django.db import models
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from tinymce.widgets import TinyMCE
from unfold.contrib.inlines.admin import TabularInline

from apps.core.unfold_admin import BDModelAdmin

from .models import Extra, HashTag, Language, Price, Service


class PriceInline(TabularInline):
    model = Price
    extra = 1
    fields = ('duration_min', 'price_czk', 'is_highlighted', 'note_cs', 'note_en')
    min_num = 0
    show_change_link = False


@admin.register(Service)
class ServiceAdmin(BDModelAdmin):
    list_display = (
        'slug', 'get_hero_preview', 'base_price_czk', 'base_duration_min',
        'order', 'is_active', 'is_extra',
    )
    list_filter = ('is_active', 'is_extra')
    list_editable = ('order', 'is_active')
    search_fields = ('slug', 'title_cs', 'title_en')
    prepopulated_fields = {'slug': ('title_cs',)}
    inlines = [PriceInline]
    readonly_fields = ('get_hero_preview',)

    fieldsets = (
        (None, {'fields': ('slug', 'icon', 'order', 'is_active', 'is_extra')}),
        (_('Images'), {'fields': ('get_hero_preview', 'hero_image', 'hero_image_url', 'image')}),
        (_('Defaults'), {'fields': ('base_price_czk', 'base_duration_min', 'price', 'duration')}),
        (_('Czech'), {
            'fields': (
                'title_cs', 'short_cs', 'description_cs', 'what_cs', 'who_cs', 'faq_cs',
                'meta_title_cs', 'meta_description_cs',
            ),
        }),
        (_('English'), {
            'fields': (
                'title_en', 'short_en', 'description_en', 'what_en', 'who_en', 'faq_en',
                'meta_title_en', 'meta_description_en',
            ),
        }),
        (_('Russian'), {
            'fields': (
                'title_ru', 'short_ru', 'description_ru', 'what_ru', 'who_ru', 'faq_ru',
                'meta_title_ru', 'meta_description_ru',
            ),
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        for field in ('description_cs', 'description_en', 'description_ru'):
            if field in form.base_fields:
                form.base_fields[field].widget = TinyMCE()
        return form

    @admin.display(description=_('Preview'))
    def get_hero_preview(self, obj):
        url = obj.hero_image.url if obj.hero_image else (obj.hero_image_url or (obj.image.url if obj.image else ''))
        if url:
            return format_html(
                '<img src="{}" style="height:60px;width:90px;object-fit:cover;border-radius:4px">',
                url,
            )
        return '—'


@admin.register(Price)
class PriceAdmin(BDModelAdmin):
    list_display = ('service', 'duration_min', 'price_czk', 'is_highlighted')
    list_filter = ('service', 'is_highlighted')
    search_fields = ('service__title_cs',)


@admin.register(Extra)
class ExtraAdmin(BDModelAdmin):
    list_display = ('slug', 'name_cs', 'name_en', 'name_ru', 'price_czk', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('slug', 'name_cs', 'name_en', 'name_ru')

    fieldsets = (
        (None, {'fields': ('slug', 'price_czk', 'order', 'is_active')}),
        (_('Names'), {'fields': ('name_cs', 'name_en', 'name_ru')}),
        (_('Price notes'), {'fields': ('price_note_cs', 'price_note_en')}),
    )


@admin.register(HashTag)
class HashTagAdmin(BDModelAdmin):
    list_display = ('slug', 'label_cs', 'label_en', 'label_ru', 'order')
    list_editable = ('order',)
    search_fields = ('slug', 'label_cs', 'label_en', 'label_ru')

    fieldsets = (
        (None, {'fields': ('slug', 'order')}),
        (_('Labels'), {'fields': ('label_cs', 'label_en', 'label_ru')}),
    )


@admin.register(Language)
class LanguageAdmin(BDModelAdmin):
    list_display = ('code', 'name', 'flag_emoji', 'order')
    list_editable = ('order',)
    search_fields = ('code', 'name')
