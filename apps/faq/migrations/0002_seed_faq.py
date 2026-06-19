"""Seed FAQ entries from home page copy."""

from django.db import migrations

FAQ_ROWS = [
    {
        'order': 1,
        'question_cs': 'Jak se připravit na masáž?',
        'question_en': 'How to prepare for a massage?',
        'question_ru': 'Как подготовиться к массажу?',
        'answer_cs': 'Doporučujeme přijít 10 minut předem, čistí a hydratovaní. Vyhněte se jídlu hodinu před masáží.',
        'answer_en': 'Arrive 10 minutes early, clean and hydrated. Avoid eating one hour before your massage.',
        'answer_ru': 'Приходите за 10 минут, чистым и гидратированным. Избегайте еды за час до массажа.',
    },
    {
        'order': 2,
        'question_cs': 'Jak rezervovat masáž?',
        'question_en': 'How to book a massage?',
        'question_ru': 'Как забронировать массаж?',
        'answer_cs': 'Online v sekci <a href="/cs/rozvrh/">Rozvrh</a> — vyberte masáž, masérku a volný termín. Potvrzení obdržíte e-mailem.',
        'answer_en': 'Online in the <a href="/en/rozvrh/">Schedule</a> section — choose massage, masseuse and slot. Email confirmation follows.',
        'answer_ru': 'Онлайн в разделе <a href="/ru/rozvrh/">Расписание</a> — выберите массаж, массажистку и время.',
    },
    {
        'order': 3,
        'question_cs': 'Jak dlouho masáž trvá?',
        'question_en': 'How long does a massage last?',
        'question_ru': 'Сколько длится массаж?',
        'answer_cs': 'Závisí na zvoleném typu: od 45 minut (aromamasáž) přes 60 minut (klasická, relax, sportovní) do 90 minut (hlubokotkaninní masáž).',
        'answer_en': 'Duration depends on type: from 60 minutes (classic, sports) to 90 minutes (relaxing).',
        'answer_ru': 'Зависит от вида: от 60 минут (классический, спортивный) до 90 минут (расслабляющий).',
    },
    {
        'order': 4,
        'question_cs': 'Jak probíhá platba?',
        'question_en': 'How does payment work?',
        'question_ru': 'Как происходит оплата?',
        'answer_cs': 'Přijímáme hotovost i platební karty. Platba probíhá na místě po skončení masáže.',
        'answer_en': 'We accept cash and cards. Payment is made on site after the massage.',
        'answer_ru': 'Принимаем наличные и карты. Оплата на месте после сеанса.',
    },
    {
        'order': 5,
        'question_cs': 'Nabízíte párovou masáž?',
        'question_en': 'Do you offer couples massage?',
        'question_ru': 'Есть ли парный массаж?',
        'answer_cs': 'Ano, párová masáž je možná po domluvě. Kontaktujte nás pro rezervaci pro dvě osoby.',
        'answer_en': 'Yes, couples massage is available upon request. Contact us to book for two.',
        'answer_ru': 'Да, парный массаж возможен по договорённости. Свяжитесь с нами для записи на двоих.',
    },
    {
        'order': 6,
        'question_cs': 'Co je zahrnuto v ceně?',
        'question_en': 'What is included in the price?',
        'question_ru': 'Что входит в стоимость?',
        'answer_cs': 'Masážní oleje, prostěradla a přístup do relaxační zóny jsou součástí každé masáže.',
        'answer_en': 'Massage oils, linens and access to the relaxation zone are included in every massage.',
        'answer_ru': 'Массажные масла, бельё и доступ в зону релакса входят в каждый сеанс.',
    },
    {
        'order': 7,
        'question_cs': 'Kde salon najdu?',
        'question_en': 'Where is the salon?',
        'question_ru': 'Где находится салон?',
        'answer_cs': 'Black Diamond Spa, Opletalova 1566/30, 110 00 Nové Město — snadno dostupné MHD i pěšky z centra Prahy.',
        'answer_en': 'Black Diamond Spa, Opletalova 1566/30, 110 00 Nové Město — easy to reach by public transport in central Prague.',
        'answer_ru': 'Black Diamond Spa, Opletalova 1566/30, 110 00 Nové Město — удобно добраться на общественном транспорте в центре Праги.',
    },
    {
        'order': 8,
        'question_cs': 'Jaká je otevírací doba?',
        'question_en': 'What are the opening hours?',
        'question_ru': 'Какой режим работы?',
        'answer_cs': 'Salon je otevřen denně. Aktuální otevírací dobu a volné termíny najdete v sekci <a href="/cs/rozvrh/">Rozvrh</a>.',
        'answer_en': 'The salon is open daily. See current hours and available slots in the <a href="/en/rozvrh/">Schedule</a> section.',
        'answer_ru': 'Салон открыт ежедневно. Актуальные часы и свободные слоты — в разделе <a href="/ru/rozvrh/">Расписание</a>.',
    },
]


def seed_faq(apps, schema_editor):
    FAQ = apps.get_model('faq', 'FAQ')
    if FAQ.objects.exists():
        return
    for row in FAQ_ROWS:
        FAQ.objects.create(**row)


class Migration(migrations.Migration):

    dependencies = [
        ('faq', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_faq, migrations.RunPython.noop),
    ]
