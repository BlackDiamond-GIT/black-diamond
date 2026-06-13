from django.contrib import admin
from .models import Therapist


@admin.register(Therapist)
class TherapistAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('specialties',)
    search_fields = ('name',)
