from django.contrib import admin
from .models import TimeSlot


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('therapist', 'date', 'time_start', 'time_end', 'status', 'service')
    list_filter = ('status', 'date', 'therapist')
    list_editable = ('status',)
    date_hierarchy = 'date'
