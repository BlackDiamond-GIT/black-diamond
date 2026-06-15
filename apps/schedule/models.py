from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.services.models import Service
from apps.therapists.models import Therapist


class ScheduleEntry(models.Model):
    class ShiftType(models.TextChoices):
        DAY = 'day', _('Day')
        NIGHT = 'night', _('Night')

    therapist = models.ForeignKey(
        Therapist, on_delete=models.CASCADE,
        related_name='schedule_entries', verbose_name=_('Therapist'),
    )
    date = models.DateField(_('Date'), db_index=True)
    time_from = models.TimeField(_('From'))
    time_to = models.TimeField(_('To'))
    location_address = models.CharField(_('Work address'), max_length=200, blank=True)
    shift_type = models.CharField(
        _('Shift'), max_length=10, choices=ShiftType.choices, default=ShiftType.DAY,
    )
    branch = models.ForeignKey(
        'branches.Branch', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='schedule_entries', verbose_name=_('Branch'),
    )
    note_cs = models.CharField(_('Note (CS)'), max_length=100, blank=True)
    note_en = models.CharField(_('Note (EN)'), max_length=100, blank=True)

    class Meta:
        verbose_name = _('Schedule Entry')
        verbose_name_plural = _('Schedule Entries')
        ordering = ['date', 'time_from']
        unique_together = [('therapist', 'date', 'time_from')]

    def __str__(self):
        return f'{self.therapist.name} — {self.date} {self.time_from}–{self.time_to}'


class TimeSlot(models.Model):
    STATUS_FREE = 'free'
    STATUS_BUSY = 'busy'
    STATUS_SOON = 'soon'
    STATUS_CHOICES = [
        (STATUS_FREE, _('Вільно')),
        (STATUS_BUSY, _('Зайнято')),
        (STATUS_SOON, _('Скоро')),
    ]

    therapist = models.ForeignKey(
        Therapist, on_delete=models.CASCADE, related_name='slots',
    )
    service = models.ForeignKey(
        Service, on_delete=models.SET_NULL, null=True, blank=True,
    )
    date = models.DateField()
    time_start = models.TimeField()
    time_end = models.TimeField()
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default=STATUS_FREE,
    )

    class Meta:
        ordering = ['date', 'time_start']
        unique_together = [('therapist', 'date', 'time_start')]
        verbose_name = _('Слот')
        verbose_name_plural = _('Слоти розкладу')

    def __str__(self):
        return f'{self.therapist.name} — {self.date} {self.time_start}'
