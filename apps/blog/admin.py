from django.contrib import admin
from django.db import models
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from tinymce.widgets import TinyMCE

from apps.core.unfold_admin import BDModelAdmin

from .models import Article


@admin.register(Article)
class ArticleAdmin(BDModelAdmin):
    list_display = ('title_cs', 'published_at', 'is_published', 'get_hero_preview')
    list_editable = ('is_published',)
    list_filter = ('is_published',)
    prepopulated_fields = {'slug': ('title_cs',)}
    search_fields = ('title_cs', 'title_en')
    date_hierarchy = 'published_at'
    readonly_fields = ('get_hero_preview',)

    fieldsets = (
        (None, {'fields': ('is_published', 'published_at', 'slug')}),
        (_('Images'), {'fields': ('get_hero_preview', 'image')}),
        (_('Czech'), {'fields': ('title_cs', 'body_cs', 'meta_description_cs')}),
        (_('English'), {'fields': ('title_en', 'body_en', 'meta_description_en')}),
        (_('Russian'), {'fields': ('title_ru', 'body_ru', 'meta_description_ru')}),
    )

    formfield_overrides = {models.TextField: {'widget': TinyMCE}}

    @admin.display(description=_('Preview'))
    def get_hero_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:60px;width:90px;object-fit:cover;border-radius:4px">',
                obj.image.url,
            )
        return '—'
