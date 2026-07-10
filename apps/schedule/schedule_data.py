"""Розклад і години роботи — синхронізовано з black-elixir."""

import math
from datetime import datetime

TIMES = ['09:00', '11:00', '18:30', '20:30', '02:00', '04:00', '06:00']

DAYS_SHORT = {
    'cs': ['Po', 'Út', 'St', 'Čt', 'Pá', 'So', 'Ne'],
    'en': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    'ru': ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'],
}

OPENING_HOURS_SCHEMA = [
    {
        'dayOfWeek': [
            'Monday', 'Tuesday', 'Wednesday', 'Thursday',
            'Friday', 'Saturday', 'Sunday',
        ],
        'opens': '09:00',
        'closes': '05:00',
    },
]


def today_weekday_index():
    return datetime.now().weekday()


def _srand(seed):
    x = math.sin(seed + 1) * 10000
    return x - math.floor(x)


def _slot_dict(slot_id, therapist, service, lang, is_booked):
    service_name = ''
    if service:
        service_name = service.get_title(lang)
    return {
        'id': slot_id,
        'therapist_id': therapist.id,
        'therapist_name': therapist.name,
        'service_name': service_name,
        'is_booked': is_booked,
    }


def build_demo_grid(therapists, lang='cs'):
    grid = {day: {time: [] for time in TIMES} for day in range(7)}
    seed = 77
    slot_id = 1

    for therapist in therapists:
        services = list(therapist.specialties.filter(is_active=True))
        if not services:
            continue

        for day in range(7):
            for time in TIMES:
                seed += 1
                if _srand(seed) <= 0.42:
                    continue

                seed += 1
                service = services[int(_srand(seed + 500) * len(services)) % len(services)]
                seed += 1
                is_booked = _srand(seed + 1000) > 0.52

                grid[day][time].append(
                    _slot_dict(slot_id, therapist, service, lang, is_booked)
                )
                slot_id += 1

    return grid


def build_db_grid(slots, lang='cs'):
    grid = {day: {time: [] for time in TIMES} for day in range(7)}

    for slot in slots:
        time_str = slot.time_start.strftime('%H:%M')
        if time_str not in TIMES:
            continue

        day = slot.date.weekday()
        is_booked = slot.status == 'busy'
        service = slot.service
        grid[day][time_str].append(
            _slot_dict(slot.pk, slot.therapist, service, lang, is_booked)
        )

    return grid


def build_schedule_rows(grid, today_idx):
    rows = []
    for time in TIMES:
        cells = []
        for day in range(7):
            cells.append({
                'day': day,
                'is_today': day == today_idx,
                'slots': grid[day][time],
            })
        rows.append({'time': time, 'cells': cells})
    return rows
