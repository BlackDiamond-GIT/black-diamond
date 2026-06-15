from django.contrib import admin
from django.db import models
from django.utils.translation import gettext_lazy as _
from tinymce.widgets import TinyMCE

from apps.core.unfold_admin import BDModelAdmin

from .models import FAQ


@admin.register(FAQ)
class FAQAdmin(BDModelAdmin):
    list_display = ('question_cs', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('question_cs', 'question_en')

    formfield_overrides = {
        models.TextField: {'widget': TinyMCE},
    }

    fieldsets = (
        (None, {'fields': ('order', 'is_active', 'include_in_schema')}),
        (_('Czech'), {'fields': ('question_cs', 'answer_cs')}),
        (_('English'), {'fields': ('question_en', 'answer_en')}),
        (_('Russian'), {'fields': ('question_ru', 'answer_ru')}),
    )
