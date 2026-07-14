# -*- coding: utf-8 -*-
"""Aktualizace FAQ na produkci: pryč odkazy na rozvrh/masérku a staré typy masáží.

Seed migrace 0002 vložila odpovědi odkazující na /rozvrh/ a výběr masérky a
vyjmenovávala odstraněné masáže (aromamasáž, klasická, sportovní, hlubokotkaninní).
Rezervace nyní probíhá přes WhatsApp; tahle data-migrace přepíše existující řádky.
"""
from django.db import migrations

UPDATES = [
    {
        'match': 'Jak rezervovat masáž?',
        'answer_cs': 'Napište nám na WhatsApp nebo zavolejte — domluvíme termín, který vám vyhovuje, a obratem ho potvrdíme.',
        'answer_en': 'Message us on WhatsApp or give us a call — we will arrange a time that suits you and confirm it right away.',
        'answer_ru': 'Напишите нам в WhatsApp или позвоните — подберём удобное время и сразу подтвердим запись.',
    },
    {
        'match': 'Jak dlouho masáž trvá?',
        'answer_cs': 'Standardní masáž trvá 60 minut, prodloužené varianty 90 minut. Délku si vyberete při rezervaci.',
        'answer_en': 'A standard massage lasts 60 minutes, extended options 90 minutes. You choose the length when booking.',
        'answer_ru': 'Стандартный массаж длится 60 минут, продлённые варианты — 90 минут. Продолжительность выбираете при записи.',
    },
    {
        'match': 'Jaká je otevírací doba?',
        'answer_cs': 'Salon je otevřen každý den od 9:00 do 5:00. Rezervace přijímáme přes WhatsApp i telefonicky.',
        'answer_en': 'The salon is open daily from 9:00 to 5:00. Bookings are accepted via WhatsApp or by phone.',
        'answer_ru': 'Салон открыт ежедневно с 9:00 до 5:00. Запись — через WhatsApp или по телефону.',
    },
]


def update_faq(apps, schema_editor):
    FAQ = apps.get_model('faq', 'FAQ')
    for row in UPDATES:
        FAQ.objects.filter(question_cs=row['match']).update(
            answer_cs=row['answer_cs'],
            answer_en=row['answer_en'],
            answer_ru=row['answer_ru'],
        )


class Migration(migrations.Migration):

    dependencies = [
        ('faq', '0002_seed_faq'),
    ]

    operations = [
        migrations.RunPython(update_faq, migrations.RunPython.noop),
    ]
