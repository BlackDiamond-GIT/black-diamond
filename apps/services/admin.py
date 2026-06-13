from django.contrib import admin
from .models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title_cs', 'duration', 'price', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    list_filter = ('is_active',)
    prepopulated_fields = {'slug': ('title_cs',)}
    search_fields = ('title_cs', 'title_en')
