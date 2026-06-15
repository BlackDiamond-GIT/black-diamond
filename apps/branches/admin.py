from django.contrib import admin

from apps.core.unfold_admin import BDModelAdmin

from .models import Branch


@admin.register(Branch)
class BranchAdmin(BDModelAdmin):
    list_display = ('name', 'address', 'phone', 'is_active', 'order')
    list_filter = ('is_active',)
    search_fields = ('name', 'address', 'phone')
    ordering = ('order', 'name')
