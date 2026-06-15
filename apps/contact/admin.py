from django.contrib import admin

from apps.core.unfold_admin import BDModelAdmin

from .models import ContactRequest


@admin.register(ContactRequest)
class ContactRequestAdmin(BDModelAdmin):
    list_display = ('name', 'email', 'phone', 'service', 'created_at', 'is_processed')
    list_editable = ('is_processed',)
    list_filter = ('is_processed',)
    search_fields = ('name', 'email', 'phone')
    readonly_fields = ('name', 'email', 'phone', 'service', 'message', 'created_at')
    date_hierarchy = 'created_at'
