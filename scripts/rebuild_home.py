#!/usr/bin/env python3
"""Rebuild static homepage — v4 Okura / Bliss Spa inspired."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# ─── Texts ────────────────────────────────────────────────────────────────────
T = {
    'cs': {
        'hero_title':     'Místo<br><em>odpočinku</em><br>a klidu',
        'hero_sub':       'Nechte stres za dveřmi. Privátní kabinety, vědomá masáž a atmosféra, kde si tělo i mysl konečně oddychnou.',
        'hero_cta1': 'Rezervovat masáž', 'hero_cta1_href': '/cs/rozvrh/',
        'hero_cta2': 'Naše masáže',      'hero_cta2_href': '/cs/masaze/',
        'svc_label': 'Naše masáže', 'svc_title': 'Relaxace pro každý moment',
        'svc_sub': 'Čtyři druhy masáže přizpůsobených vašemu tělu i mysli — VIP, relaxační, pro ženy nebo pro páry.',
        'svc_btn': 'Zjistit více', 'all_svc': 'Všechny masáže',
        'team_label': 'Náš tým', 'team_title': 'Masérky',
        'team_sub': 'Zkušené specialistky s individuálním přístupem a hlubokými znalostmi masážních technik.',
        'all_team': 'Seznámit se s týmem',
        'proc_label': 'Vaše cesta k relaxaci',
        'proc_title': 'Každý detail<br>myslíme za vás',
        'faq_label': 'FAQ', 'faq_title': 'Odpovědi na vaše otázky',
        'cta_label': 'Dopřejte si',
        'cta_title': 'Vaše tělo si<br>zaslouží péči',
        'cta_sub': 'Rezervujte si masáž online a nechte se unést luxusní atmosférou Black Diamond Spa.',
        'cta_btn1': 'Rezervovat nyní', 'cta_btn1_href': '/cs/rozvrh/',
        'cta_btn2': 'Kontakt',          'cta_btn2_href': '/cs/kontakty/',
        'modal_close': 'Zavřít',
        'modal_svc_title': 'Nabízené masáže',
        'modal_reserve': 'Rezervovat termín',
        'steps': [
            ('Vyberte masáž',    'Prozkoumejte katalog a vyberte masáž, která nejlépe odpovídá vašim potřebám a přáním.'),
            ('Zvolte masérku',   'Každá z našich masérky má jedinečnou specializaci. Vyberte tu, jejíž styl vám vyhovuje.'),
            ('Potvrďte termín',  'Zvolte volný termín v online rozvrhu a potvrďte rezervaci. Potvrzení přijde e-mailem.'),
            ('Relaxujte',        'Přijďte 10 minut předem. Vše ostatní necháme na nás — váš čas je jen pro vás.'),
        ],
        'faqs': [
            ('Jak se připravit na masáž?', 'Doporučujeme přijít 10 minut předem, čistí a hydratovaní. Vyhněte se jídlu hodinu před masáží.'),
            ('Jak rezervovat masáž?',       'Online v sekci <a href="/cs/rozvrh/">Rozvrh</a> — vyberte masáž, masérku a volný termín. Potvrzení obdržíte e-mailem.'),
            ('Jak dlouho masáž trvá?',      'Závisí na zvoleném typu: od 60 minut (klasická, sportovní) do 90 minut (uvolňující masáž).'),
            ('Jak probíhá platba?',         'Přijímáme hotovost i platební karty. Platba probíhá na místě po skončení masáže.'),
            ('Nabízíte párovou masáž?',     'Ano, párová masáž je možná po domluvě. Kontaktujte nás pro rezervaci pro dvě osoby.'),
            ('Co je zahrnuto v ceně?',      'Masážní oleje, prostěradla a přístup do relaxační zóny jsou součástí každé masáže.'),
        ],
    },
    'en': {
        'hero_title':     'A place for<br><em>rest</em><br>and calm',
        'hero_sub':       'Leave stress at the door. Private cabins, mindful massage and an atmosphere where body and mind truly recover.',
        'hero_cta1': 'Book a massage', 'hero_cta1_href': '/en/rozvrh/',
        'hero_cta2': 'Our massages',   'hero_cta2_href': '/en/masaze/',
        'svc_label': 'Our massages', 'svc_title': 'Relaxation for every moment',
        'svc_sub': 'Four types of massage tailored to your body and mind — VIP, relaxation, for women or for couples.',
        'svc_btn': 'Learn more', 'all_svc': 'All massages',
        'team_label': 'Our team', 'team_title': 'Masseuses',
        'team_sub': 'Experienced specialists with an individual approach and deep knowledge of massage techniques.',
        'all_team': 'Meet our team',
        'proc_label': 'Your path to relaxation',
        'proc_title': 'Every detail<br>thought through for you',
        'faq_label': 'FAQ', 'faq_title': 'Answers to your questions',
        'cta_label': 'Treat yourself',
        'cta_title': 'Your body<br>deserves care',
        'cta_sub': 'Book your massage online and immerse yourself in the luxurious atmosphere of Black Diamond Spa.',
        'cta_btn1': 'Book now',     'cta_btn1_href': '/en/rozvrh/',
        'cta_btn2': 'Contact us',   'cta_btn2_href': '/en/kontakty/',
        'modal_close': 'Close',
        'modal_svc_title': 'Offered massages',
        'modal_reserve': 'Book appointment',
        'steps': [
            ('Choose a massage',  'Browse our catalog and pick the massage that best fits your needs and wishes.'),
            ('Pick a masseuse',   'Each of our masseuses has a unique specialty. Choose the one whose style suits you.'),
            ('Confirm your slot', 'Select an available slot in the online schedule and confirm. Email confirmation follows.'),
            ('Relax',             'Arrive 10 minutes early. We take care of everything else — your time is yours alone.'),
        ],
        'faqs': [
            ('How to prepare for a massage?', 'Arrive 10 minutes early, clean and hydrated. Avoid eating one hour before your massage.'),
            ('How to book a massage?',         'Online in the <a href="/en/rozvrh/">Schedule</a> section — choose massage, masseuse and slot. Email confirmation follows.'),
            ('How long does a massage last?',  'Duration depends on type: from 60 minutes (classic, sports) to 90 minutes (relaxing).'),
            ('How does payment work?',         'We accept cash and cards. Payment is made on site after the massage.'),
            ('Do you offer couples massage?',  'Yes, couples massage is available upon request. Contact us to book for two.'),
            ('What is included in the price?', 'Massage oils, linens and access to the relaxation zone are included in every massage.'),
        ],
    },
    'ru': {
        'hero_title':     'Место<br><em>отдыха</em><br>и покоя',
        'hero_sub':       'Оставьте стресс за дверью. Приватные кабинеты, сознательный массаж и атмосфера, где тело и разум наконец отдохнут.',
        'hero_cta1': 'Записаться на массаж', 'hero_cta1_href': '/ru/rozvrh/',
        'hero_cta2': 'Наши массажи',          'hero_cta2_href': '/ru/masaze/',
        'svc_label': 'Наши массажи', 'svc_title': 'Расслабление для каждого момента',
        'svc_sub': 'Четыре вида массажа для вашего тела и разума — VIP, расслабляющий, для женщин или для пар.',
        'svc_btn': 'Подробнее', 'all_svc': 'Все массажи',
        'team_label': 'Наша команда', 'team_title': 'Массажистки',
        'team_sub': 'Сертифицированные специалистки с индивидуальным подходом и глубокими знаниями массажных техник.',
        'all_team': 'Познакомиться с командой',
        'proc_label': 'Ваш путь к расслаблению',
        'proc_title': 'Каждая деталь<br>продумана за вас',
        'faq_label': 'FAQ', 'faq_title': 'Ответы на ваши вопросы',
        'cta_label': 'Подарите себе',
        'cta_title': 'Ваше тело<br>заслуживает ухода',
        'cta_sub': 'Забронируйте массаж онлайн и погрузитесь в роскошную атмосферу Black Diamond Spa.',
        'cta_btn1': 'Забронировать', 'cta_btn1_href': '/ru/rozvrh/',
        'cta_btn2': 'Контакты',       'cta_btn2_href': '/ru/kontakty/',
        'modal_close': 'Закрыть',
        'modal_svc_title': 'Предлагаемые массажи',
        'modal_reserve': 'Забронировать',
        'steps': [
            ('Выберите массаж',        'Изучите каталог и выберите массаж, который лучше всего отвечает вашим потребностям.'),
            ('Выберите массажистку',   'У каждой массажистки уникальная специализация. Выберите ту, чей стиль вам подходит.'),
            ('Подтвердите время',      'Выберите свободный слот в онлайн-расписании и подтвердите. Подтверждение придёт по email.'),
            ('Расслабьтесь',           'Приходите за 10 минут. Всё остальное — на нас. Ваше время только для вас.'),
        ],
        'faqs': [
            ('Как подготовиться к массажу?', 'Приходите за 10 минут, чистым и гидратированным. Избегайте еды за час до массажа.'),
            ('Как забронировать массаж?',     'Онлайн в разделе <a href="/ru/rozvrh/">Расписание</a> — выберите массаж, массажистку и время.'),
            ('Как долго длится массаж?',      'От 60 минут (классический, спортивный) до 90 минут (расслабляющий).'),
            ('Как происходит оплата?',        'Принимаем наличные и карты. Оплата на месте после массажа.'),
            ('Предлагаете парный массаж?',    'Да, парный массаж возможен по запросу. Свяжитесь с нами для бронирования.'),
            ('Что включено в цену?',          'Масляные составы, простыни и доступ к зоне отдыха включены в каждый массаж.'),
        ],
    },
}

SERVICES = {
    'cs': [
        {'slug': 'vip-masaz',      'title': 'VIP masáž',        'short': 'Luxusní VIP masáž s plnou pozorností masérky, prémiálními oleji a individuálním přístupem od začátku do konce.', 'duration': 'od 30 min', 'price': 'od 1 800 Kč', 'img': '/assets/img/services/vip-masaz.webp'},
        {'slug': 'relaxacni-masaz','title': 'Relaxační masáž',  'short': 'Jemná relaxační masáž s prémiálními oleji pro hluboké uvolnění těla i mysli v klidné privátní atmosféře.', 'duration': 'od 30 min', 'price': 'od 1 600 Kč', 'img': '/assets/img/services/relaxacni-masaz.webp'},
        {'slug': 'masaz-pro-zeny', 'title': 'Masáž pro ženy',   'short': 'Masáž navržená speciálně pro potřeby ženského těla — jemná, bezpečná a zcela privátní.', 'duration': 'od 45 min', 'price': 'od 3 200 Kč', 'img': '/assets/img/services/masaz-pro-zeny.webp'},
        {'slug': 'masaz-pro-pary', 'title': 'Masáž pro páry',   'short': 'Párová masáž pro dvě osoby ve společném prostoru — sdílená relaxace a společný zážitek.', 'duration': 'od 30 min', 'price': 'od 1 400 Kč', 'img': '/assets/img/services/masaz-pro-pary.webp'},
    ],
    'en': [
        {'slug': 'vip-masaz',      'title': 'VIP Massage',          'short': 'Luxury VIP massage with full masseuse attention, premium oils and individual care from start to finish.', 'duration': 'from 30 min', 'price': 'from 1,800 CZK', 'img': '/assets/img/services/vip-masaz.webp'},
        {'slug': 'relaxacni-masaz','title': 'Relaxation Massage',   'short': 'Gentle relaxation massage with premium oils for deep release of body and mind in a calm private atmosphere.', 'duration': 'from 30 min', 'price': 'from 1,600 CZK', 'img': '/assets/img/services/relaxacni-masaz.webp'},
        {'slug': 'masaz-pro-zeny', 'title': 'Massage for Women',    'short': 'Massage designed specifically for women\'s needs — gentle, safe and fully private.', 'duration': 'from 45 min', 'price': 'from 3,200 CZK', 'img': '/assets/img/services/masaz-pro-zeny.webp'},
        {'slug': 'masaz-pro-pary', 'title': 'Couples Massage',      'short': 'Couples massage for two in a shared space — shared relaxation and a joint experience.', 'duration': 'from 30 min', 'price': 'from 1,400 CZK', 'img': '/assets/img/services/masaz-pro-pary.webp'},
    ],
    'ru': [
        {'slug': 'vip-masaz',      'title': 'VIP-массаж',              'short': 'Роскошный VIP-массаж с полным вниманием массажистки, премиальными маслами и индивидуальным подходом.', 'duration': 'от 30 мин', 'price': 'от 1 800 Kč', 'img': '/assets/img/services/vip-masaz.webp'},
        {'slug': 'relaxacni-masaz','title': 'Расслабляющий массаж',   'short': 'Мягкий расслабляющий массаж с премиальными маслами для глубокого снятия напряжения в приватной атмосфере.', 'duration': 'от 30 мин', 'price': 'от 1 600 Kč', 'img': '/assets/img/services/relaxacni-masaz.webp'},
        {'slug': 'masaz-pro-zeny', 'title': 'Массаж для женщин',       'short': 'Массаж, разработанный специально для потребностей женского тела — мягкий, безопасный и полностью приватный.', 'duration': 'от 45 мин', 'price': 'от 3 200 Kč', 'img': '/assets/img/services/masaz-pro-zeny.webp'},
        {'slug': 'masaz-pro-pary', 'title': 'Массаж для пар',          'short': 'Массаж для двоих в общем пространстве — совместная релаксация и общий опыт.', 'duration': 'от 30 мин', 'price': 'от 1 400 Kč', 'img': '/assets/img/services/masaz-pro-pary.webp'},
    ],
}

THERAPISTS = {
    'cs': [
        {'slug': 'julia',   'name': 'Julia',   'spec': 'Klasická & Relax masáž',       'svcs': 'Klasická masáž|Relax masáž|Uvolňující masáž', 'bio': 'Julia je zkušená masérka specializující se na klasickou a relax masáž. Každé sezení přizpůsobuje potřebám klienta a vytváří prostor pro skutečné uvolnění.'},
        {'slug': 'diana',   'name': 'Diana',   'spec': 'Uvolňující & Aromamasáž',       'svcs': 'Uvolňující masáž|Aromamasáž', 'bio': 'Diana se zaměřuje na uvolňující a aromaterapeutické masáže. Její klidný přístup je ideální pro hluboký odpočinek a celkovou regeneraci.'},
        {'slug': 'laura',   'name': 'Laura',   'spec': 'Aromaterapie & Relax',           'svcs': 'Aromamasáž|Relax masáž', 'bio': 'Laura kombinuje aromamasáž a relaxační techniky s prémiálními éterickými oleji pro harmonii těla a mysli.'},
        {'slug': 'vanessa', 'name': 'Vanessa', 'spec': 'Klasická & Sportovní masáž',    'svcs': 'Klasická masáž|Sportovní masáž', 'bio': 'Vanessa se specializuje na klasickou a sportovní masáž. Pomáhá uvolnit napětí po sportu i v každodenním životě.'},
        {'slug': 'ella',    'name': 'Ella',    'spec': 'Sportovní & Regenerace',         'svcs': 'Sportovní masáž|Regenerační masáž', 'bio': 'Ella specialuje sportovní a regenerační masáže, které efektivně podporují zotavení svalů a celkovou regeneraci těla.'},
        {'slug': 'mira',    'name': 'Mira',    'spec': 'Lymfatická & Aromaterapie',      'svcs': 'Lymfatická masáž|Aromamasáž', 'bio': 'Mira nabízí lymfatickou a aromamasáž s jemným a uvědomělým přístupem, který podporuje detoxikaci a hlubokou relaxaci.'},
    ],
    'en': [
        {'slug': 'julia',   'name': 'Julia',   'spec': 'Classic & Relax Massage',       'svcs': 'Classic massage|Relax massage|Relaxing massage', 'bio': 'Julia is an experienced masseuse specializing in classic and relax massage, tailoring each session to the client\'s individual needs.'},
        {'slug': 'diana',   'name': 'Diana',   'spec': 'Relaxing & Aroma Massage',       'svcs': 'Relaxing massage|Aroma massage', 'bio': 'Diana focuses on relaxing and aromatherapy massages with a calm, sensitive approach for deep rest and regeneration.'},
        {'slug': 'laura',   'name': 'Laura',   'spec': 'Aromatherapy & Relax',           'svcs': 'Aroma massage|Relax massage', 'bio': 'Laura combines aroma and relax massage with premium essential oils for body and mind harmony.'},
        {'slug': 'vanessa', 'name': 'Vanessa', 'spec': 'Classic & Sports Massage',      'svcs': 'Classic massage|Sports massage', 'bio': 'Vanessa specializes in classic and sports massage, helping release tension after sport and in daily life.'},
        {'slug': 'ella',    'name': 'Ella',    'spec': 'Sports & Recovery',              'svcs': 'Sports massage|Recovery massage', 'bio': 'Ella specializes in sports and recovery massage to effectively support muscle recovery and regeneration.'},
        {'slug': 'mira',    'name': 'Mira',    'spec': 'Lymphatic & Aromatherapy',      'svcs': 'Lymphatic massage|Aroma massage', 'bio': 'Mira offers lymphatic and aroma massage with a gentle, mindful approach that supports detox and deep relaxation.'},
    ],
    'ru': [
        {'slug': 'julia',   'name': 'Julia',   'spec': 'Классический & Релакс',          'svcs': 'Классический массаж|Релакс массаж', 'bio': 'Julia — опытная массажистка, специализирующаяся на классическом и релакс-массаже с индивидуальным подходом.'},
        {'slug': 'diana',   'name': 'Diana',   'spec': 'Расслабляющий & Арома',           'svcs': 'Расслабляющий массаж|Аромамассаж', 'bio': 'Diana специализируется на расслабляющем и аромамассаже с чутким подходом для глубокого отдыха.'},
        {'slug': 'laura',   'name': 'Laura',   'spec': 'Ароматерапия & Релакс',           'svcs': 'Аромамассаж|Релакс массаж', 'bio': 'Laura сочетает арома и релакс-массаж с эфирными маслами для гармонии тела и разума.'},
        {'slug': 'vanessa', 'name': 'Vanessa', 'spec': 'Классический & Спортивный',       'svcs': 'Классический массаж|Спортивный массаж', 'bio': 'Vanessa специализируется на классическом и спортивном массаже, снимая напряжение после спорта и в повседневной жизни.'},
        {'slug': 'ella',    'name': 'Ella',    'spec': 'Спортивный & Регенерация',        'svcs': 'Спортивный массаж|Регенерационный массаж', 'bio': 'Ella специализируется на спортивном и регенерационном массаже для восстановления мышц и общей регенерации.'},
        {'slug': 'mira',    'name': 'Mira',    'spec': 'Лимфодренажный & Ароматерапия',   'svcs': 'Лимфодренажный массаж|Аромамассаж', 'bio': 'Mira предлагает лимфодренажный и аромамассаж с мягким подходом для детокса и глубокого расслабления.'},
    ],
}


def service_cards_html(lang):
    t = T[lang]
    cards = []
    for svc in SERVICES[lang]:
        href = f'/{lang}/masaze/{svc["slug"]}/'
        cards.append(f'''
          <article class="svc-card" data-reveal>
            <div class="svc-card__img">
              <img src="{svc['img']}" alt="{svc['title']} Praha — Black Diamond Spa" width="120" height="90" loading="lazy" decoding="async">
            </div>
            <div class="svc-card__body">
              <h3 class="svc-card__name">{svc['title']}</h3>
              <p class="svc-card__desc">{svc['short']}</p>
              <div class="svc-card__tags">
                <span class="tag tag--duration">{svc['duration']}</span>
                <span class="tag tag--price">{svc['price']}</span>
              </div>
              <a href="{href}" class="btn btn--ghost">{t['svc_btn']}</a>
            </div>
          </article>''')
    return '\n'.join(cards)


def therapist_cards_html(lang):
    cards = []
    for th in THERAPISTS[lang]:
        photo = f'/assets/img/masseuses/{th["slug"]}.webp'
        cards.append(f'''
          <button type="button" class="th-card" data-modal-trigger
            data-name="{th['name']}"
            data-spec="{th['spec']}" data-bio="{th['bio']}"
            data-svcs="{th['svcs']}" data-photo="{photo}"
            aria-label="Profil {th['name']}">
            <div class="th-card__img">
              <img src="{photo}" alt="{th['name']} — Black Diamond Spa" width="80" height="80" loading="lazy" decoding="async">
            </div>
            <div class="th-card__info">
              <span class="th-card__name">{th['name']}</span>
              <span class="th-card__spec">{th['spec']}</span>
            </div>
            <span class="th-card__hint" aria-hidden="true">+</span>
          </button>''')
    return '\n'.join(cards)


def steps_html(lang):
    rows = []
    for i, (title, text) in enumerate(T[lang]['steps'], 1):
        expanded = 'true' if i == 1 else 'false'
        open_cls = ' is-open' if i == 1 else ''
        rows.append(f'''
          <div class="proc-acc__item">
            <button type="button" class="proc-acc__trigger" aria-expanded="{expanded}" aria-controls="proc-{i}">
              <span class="proc-acc__title">{title}</span>
              <span class="proc-acc__mark" aria-hidden="true"></span>
            </button>
            <div id="proc-{i}" class="proc-acc__panel{open_cls}">
              <p class="proc-acc__text">{text}</p>
            </div>
          </div>''')
    return '\n'.join(rows)


def faqs_html(lang):
    items = []
    for i, (q, a) in enumerate(T[lang]['faqs'], 1):
        items.append(f'''
          <div class="faq__item">
            <button class="faq__question" aria-expanded="false" aria-controls="faq-{i}">
              {q}
              <span class="faq__mark" aria-hidden="true"></span>
            </button>
            <div id="faq-{i}" class="faq__answer">
              <div class="faq__answer-inner">{a}</div>
            </div>
          </div>''')
    return '\n'.join(items)


def build_main(lang):
    t = T[lang]
    return f'''  <main id="main-content">

    <!-- ── HERO ────────────────────────────────── -->
    <section class="hero2" aria-label="Úvodní sekce">
      <div class="hero2__bg" aria-hidden="true">
        <img src="/assets/img/hero.webp" alt="" width="1920" height="1080" fetchpriority="high" decoding="async">
      </div>
      <div class="hero2__overlay" aria-hidden="true"></div>
      <div class="hero2__inner">
        <h1 class="hero2__title">{t['hero_title']}</h1>
        <p class="hero2__sub">{t['hero_sub']}</p>
        <div class="hero2__actions">
          <a href="{t['hero_cta1_href']}" class="btn btn--primary btn--lg">{t['hero_cta1']}</a>
          <a href="{t['hero_cta2_href']}" class="btn btn--ghost btn--lg">{t['hero_cta2']}</a>
        </div>
      </div>
    </section>

    <!-- ── SERVICES ─────────────────────────────── -->
    <section class="sec sec--dark" aria-labelledby="svc-hd">
      <div class="container">
        <header class="sec__hd sec__hd--center">
          <span class="sec__label">{t['svc_label']}</span>
          <h2 class="sec__title" id="svc-hd">{t['svc_title']}</h2>
          <p class="sec__sub">{t['svc_sub']}</p>
        </header>
        <div class="svc-grid">
          {service_cards_html(lang)}
        </div>
        <p class="sec__more">
          <a href="/{lang}/masaze/" class="btn btn--secondary btn--lg">{t['all_svc']}</a>
        </p>
      </div>
    </section>

    <!-- ── MASSEUSES ─────────────────────────────── -->
    <section class="sec sec--alt" aria-labelledby="team-hd">
      <div class="container">
        <header class="sec__hd sec__hd--center">
          <span class="sec__label">{t['team_label']}</span>
          <h2 class="sec__title" id="team-hd">{t['team_title']}</h2>
          <p class="sec__sub">{t['team_sub']}</p>
        </header>
        <div class="th-grid" role="list">
          {therapist_cards_html(lang)}
        </div>
        <p class="sec__more">
          <a href="/{lang}/masazistky/" class="btn btn--secondary btn--lg">{t['all_team']}</a>
        </p>
      </div>
    </section>

    <!-- ── HOW IT WORKS ───────────────────────────── -->
    <section class="sec sec--dark sec--how" aria-labelledby="proc-hd">
      <div class="container">
        <div class="proc-layout">
          <div class="proc-intro">
            <span class="sec__label">{t['proc_label']}</span>
            <h2 class="sec__title sec__title--large" id="proc-hd">{t['proc_title']}</h2>
          </div>
          <div class="proc-acc" role="list">
            {steps_html(lang)}
          </div>
        </div>
      </div>
    </section>

    <!-- ── FAQ ───────────────────────────────────── -->
    <section class="sec sec--alt" aria-labelledby="faq-hd">
      <div class="container container--md">
        <header class="sec__hd sec__hd--center">
          <span class="sec__label">{t['faq_label']}</span>
          <h2 class="sec__title" id="faq-hd">{t['faq_title']}</h2>
        </header>
        <div class="faq" role="list">
          {faqs_html(lang)}
        </div>
      </div>
    </section>

    <!-- ── CTA ───────────────────────────────────── -->
    <section class="cta-sec" aria-labelledby="cta-hd">
      <div class="cta-sec__bg" aria-hidden="true">
        <img src="/assets/img/services/lymfaticka-masaz.webp" alt="" width="1920" height="900" loading="lazy" decoding="async">
      </div>
      <div class="cta-sec__overlay" aria-hidden="true"></div>
      <div class="container cta-sec__inner">
        <span class="sec__label">{t['cta_label']}</span>
        <h2 class="sec__title cta-sec__title" id="cta-hd">{t['cta_title']}</h2>
        <p class="sec__sub cta-sec__sub">{t['cta_sub']}</p>
        <div class="cta-sec__actions">
          <a href="{t['cta_btn1_href']}" class="btn btn--primary btn--lg">{t['cta_btn1']}</a>
          <a href="{t['cta_btn2_href']}" class="btn btn--ghost btn--lg">{t['cta_btn2']}</a>
        </div>
      </div>
    </section>

    <!-- ── MODAL ─────────────────────────────────── -->
    <div id="th-modal" class="th-modal" role="dialog" aria-modal="true" aria-hidden="true" hidden>
      <div class="th-modal__bd" data-close-modal></div>
      <div class="th-modal__panel">
        <button type="button" class="th-modal__close" data-close-modal aria-label="{t['modal_close']}">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
        </button>
        <div class="th-modal__photo-wrap">
          <img id="modal-photo" class="th-modal__photo" src="" alt="" width="480" height="600" decoding="async">
        </div>
        <div class="th-modal__info">
          <h2 id="modal-name" class="th-modal__name"></h2>
          <div id="modal-tags" class="th-modal__tags"></div>
          <p id="modal-bio" class="th-modal__bio"></p>
          <p class="th-modal__svcs-title">{t['modal_svc_title']}</p>
          <ul id="modal-svcs" class="th-modal__svcs"></ul>
          <a id="modal-cta" href="/{lang}/rozvrh/" class="btn btn--primary btn--lg">{t['modal_reserve']}</a>
        </div>
      </div>
    </div>

  </main>
'''


HOME_CSS = r'''/* ─────────────────────────────────────────────────────────────────
   Black Diamond Spa — Home v4
   Fonts: DM Serif Display (headings) + Jost (body)
   Inspired by Okura Spa & Bliss Spa aesthetic
───────────────────────────────────────────────────────────────── */

/* ── CSS overrides for new fonts ─────────────────── */
:root {
  --font-display: 'DM Serif Display', Georgia, serif;
  --font-body:    'Jost', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* ── Section shell ───────────────────────────────── */
.sec { padding-block: clamp(4.5rem, 10vw, 7rem); }
.sec--dark { background: var(--bg-primary); }
.sec--alt  { background: var(--bg-tertiary); }
.sec--how  { background: var(--bg-secondary); }

.sec__hd {
  margin-bottom: clamp(3rem, 6vw, 4.5rem);
}
.sec__hd--center { text-align: center; }
.sec__hd--split {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
  margin-bottom: clamp(2.5rem, 5vw, 3.5rem);
}

@media (min-width: 768px) {
  .sec__hd--split {
    grid-template-columns: 1fr 1fr;
    align-items: end;
  }
}

.sec__label {
  display: inline-block;
  font-family: var(--font-body);
  font-size: .68rem;
  font-weight: 400;
  letter-spacing: .2em;
  text-transform: uppercase;
  color: var(--tiffany);
  margin-bottom: .875rem;
}

.sec__title {
  font-family: var(--font-display);
  font-size: clamp(2rem, 4.5vw, 2.75rem);
  font-weight: 400;
  color: var(--text-primary);
  line-height: 1.2;
  margin-bottom: 1.25rem;
}

.sec__title--large {
  font-size: clamp(2.25rem, 5vw, 3.25rem);
  line-height: 1.15;
  margin-bottom: 0;
}

.sec__sub {
  font-family: var(--font-body);
  font-size: 1rem;
  font-weight: 300;
  color: var(--text-secondary);
  max-width: 54ch;
  line-height: 1.85;
  margin: 0;
}
.sec__hd--center .sec__sub { margin-inline: auto; }

.sec__more {
  text-align: center;
  margin-top: clamp(2.5rem, 5vw, 3.5rem);
}

/* ── Hero ────────────────────────────────────────── */
.hero2 {
  position: relative;
  min-height: 100vh;
  min-height: 100svh;
  display: flex;
  align-items: flex-end;
  overflow: hidden;
  background: var(--bg-deep);
}

.hero2__bg {
  position: absolute;
  inset: 0;
  z-index: 0;
}
.hero2__bg img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center 15%;
}

.hero2__overlay {
  position: absolute;
  inset: 0;
  z-index: 1;
  background:
    linear-gradient(to right,
      rgba(14,17,21,.90) 0%,
      rgba(14,17,21,.60) 50%,
      rgba(14,17,21,.18) 100%),
    linear-gradient(to top,
      rgba(14,17,21,.60) 0%,
      transparent 55%);
}

.hero2__inner {
  position: relative;
  z-index: 2;
  width: 100%;
  max-width: var(--container-xl);
  margin-inline: auto;
  padding: calc(var(--nav-height) + 4rem) var(--container-pad) clamp(4rem, 8vw, 6rem);
}

.hero2__eyebrow {
  font-family: var(--font-body);
  font-size: clamp(0.65rem, 1.5vw, 0.75rem);
  font-weight: 500;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: rgba(255, 255, 255, 0.88);
  margin-bottom: clamp(1.25rem, 3vw, 2rem);
  animation: heroFadeUp 1.1s ease 0.5s both;
}

.hero2__title {
  font-family: var(--font-display);
  font-size: clamp(3rem, 8.5vw, 5.5rem);
  font-weight: 400;
  line-height: 1.08;
  letter-spacing: -.01em;
  color: var(--text-primary);
  max-width: 13ch;
  margin-bottom: 1.75rem;
}
.hero2__title em {
  font-style: italic;
  color: var(--tiffany-light);
}

.hero2__sub {
  font-family: var(--font-body);
  font-size: 1.05rem;
  font-weight: 300;
  color: var(--text-secondary);
  max-width: 42ch;
  line-height: 1.85;
  margin-bottom: 2.5rem;
}

.hero2__actions { display: flex; flex-wrap: wrap; gap: 1rem; align-items: center; }

/* ── Service cards ───────────────────────────────── */
.svc-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.75rem;
}

@media (min-width: 640px)  { .svc-grid { grid-template-columns: repeat(2, 1fr); } }
@media (min-width: 1024px) { .svc-grid { grid-template-columns: repeat(3, 1fr); } }

.svc-card {
  background: var(--glass-bg);
  -webkit-backdrop-filter: blur(20px);
  backdrop-filter: blur(20px);
  border: 1px solid var(--glass-border);
  border-radius: 20px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  transition: transform .35s ease, border-color .35s ease, box-shadow .35s ease;
}
.svc-card:hover {
  transform: translateY(-7px);
  border-color: rgba(10,186,181,.3);
  box-shadow: 0 20px 50px rgba(0,0,0,.45);
}

.svc-card__img {
  aspect-ratio: 16/9;
  overflow: hidden;
  background: var(--bg-secondary);
  flex-shrink: 0;
}
.svc-card__img img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform .6s ease;
}
.svc-card:hover .svc-card__img img { transform: scale(1.07); }

.svc-card__body {
  padding: 1.75rem;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: .875rem;
}

.svc-card__name {
  font-family: var(--font-display);
  font-size: 1.5rem;
  font-weight: 400;
  color: var(--text-primary);
  line-height: 1.25;
}

.svc-card__desc {
  font-family: var(--font-body);
  font-size: .9rem;
  font-weight: 300;
  color: var(--text-secondary);
  line-height: 1.75;
  flex: 1;
  max-width: none;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.svc-card__tags { display: flex; flex-wrap: wrap; gap: .5rem; }

/* ── Therapist grid ──────────────────────────────── */
.th-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

@media (min-width: 640px) {
  .th-grid { grid-template-columns: repeat(3, 1fr); gap: 1.25rem; }
}
@media (min-width: 1100px) {
  .th-grid { grid-template-columns: repeat(6, 1fr); gap: 1rem; }
}

.th-card {
  background: var(--bg-secondary);
  border: 1px solid transparent;
  border-radius: 16px;
  overflow: hidden;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  text-align: left;
  padding: 0;
  transition: transform .35s ease, border-color .35s ease, box-shadow .35s ease;
  -webkit-tap-highlight-color: transparent;
}
.th-card:hover {
  transform: translateY(-5px);
  border-color: rgba(10,186,181,.3);
  box-shadow: 0 14px 36px rgba(10,186,181,.1);
}

.th-card__img {
  position: relative;
  aspect-ratio: 2/3;
  overflow: hidden;
  background: var(--bg-deep);
  flex-shrink: 0;
}
.th-card__img img {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: top center;
  display: block;
  transition: transform .55s ease;
}
.th-card:hover .th-card__img img { transform: scale(1.04); }

.th-card__info {
  padding: 1rem 1rem .875rem;
  display: flex;
  flex-direction: column;
  gap: .25rem;
  background: var(--bg-secondary);
}

.th-card__name {
  font-family: var(--font-display);
  font-size: 1.15rem;
  font-weight: 400;
  color: var(--text-primary);
  line-height: 1.2;
}
.th-card__spec {
  font-family: var(--font-body);
  font-size: .65rem;
  font-weight: 500;
  letter-spacing: .1em;
  text-transform: uppercase;
  color: var(--tiffany);
  line-height: 1.4;
}

/* ── Steps (no numbers) ──────────────────────────── */
.steps-list {
  display: grid;
  grid-template-columns: 1fr;
  gap: 0;
  list-style: none;
}

@media (min-width: 768px) {
  .steps-list {
    grid-template-columns: repeat(4, 1fr);
  }
}

.step {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  padding: 2rem;
  border-top: 1px solid var(--divider);
  position: relative;
}

@media (min-width: 768px) {
  .step {
    border-top: none;
    border-left: 1px solid var(--divider);
    padding: 0 2.5rem 0 2rem;
  }
  .step:first-child { padding-left: 0; border-left: none; }
}

.step__line {
  width: 32px;
  height: 1px;
  background: var(--tiffany);
  opacity: .6;
}

.step__title {
  font-family: var(--font-display);
  font-size: 1.3rem;
  font-weight: 400;
  color: var(--text-primary);
  line-height: 1.3;
}
.step__text {
  font-family: var(--font-body);
  font-size: .875rem;
  font-weight: 300;
  color: var(--text-secondary);
  line-height: 1.75;
  max-width: none;
}

/* ── FAQ ─────────────────────────────────────────── */
.faq { max-width: 760px; margin-inline: auto; }
.faq__item { border-bottom: 1px solid var(--divider); }

.faq__question {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1.25rem;
  padding: 1.4rem 0;
  background: transparent;
  border: none;
  cursor: pointer;
  text-align: left;
  font-family: var(--font-body);
  font-size: .975rem;
  font-weight: 400;
  color: var(--text-primary);
  transition: color .25s;
  min-height: 44px;
  -webkit-tap-highlight-color: transparent;
}
.faq__question:hover,
.faq__question[aria-expanded="true"] { color: var(--tiffany); }

.faq__icon {
  flex-shrink: 0;
  width: 28px;
  display: flex;
  align-items: center;
  justify-content: flex-end;
}
.faq__icon-dash {
  display: block;
  height: 1px;
  background: var(--tiffany);
  width: 16px;
  transition: width .25s ease;
}
.faq__question[aria-expanded="true"] .faq__icon-dash { width: 28px; }

.faq__answer {
  overflow: hidden;
  max-height: 0;
  transition: max-height .4s cubic-bezier(.4,0,.2,1);
}
.faq__answer.is-open { max-height: 600px; }
.faq__answer-inner {
  padding-bottom: 1.4rem;
  font-family: var(--font-body);
  font-size: .9rem;
  font-weight: 300;
  color: var(--text-secondary);
  line-height: 1.85;
  max-width: none;
}

/* ── CTA section ─────────────────────────────────── */
.cta-sec {
  position: relative;
  overflow: hidden;
  text-align: center;
  padding-block: clamp(6rem, 14vw, 9rem);
  background: var(--bg-deep);
}
.cta-sec__bg {
  position: absolute;
  inset: 0;
}
.cta-sec__bg img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
}
.cta-sec__overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    160deg,
    rgba(14,17,21,.92) 0%,
    rgba(14,17,21,.8) 100%
  );
  border-top: 1px solid rgba(10,186,181,.25);
}
.cta-sec__inner {
  position: relative;
  z-index: 1;
}
.cta-sec__title {
  font-size: clamp(2rem, 5.5vw, 3.5rem);
  max-width: 14ch;
  margin-inline: auto;
  margin-bottom: 1.25rem;
}
.cta-sec__sub {
  max-width: 46ch;
  margin-inline: auto;
  margin-bottom: 2.75rem;
  font-size: 1rem;
  font-weight: 300;
}
.cta-sec__actions {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  justify-content: center;
}

/* ── Therapist modal ─────────────────────────────── */
.th-modal {
  position: fixed;
  inset: 0;
  z-index: 500;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1.25rem;
  padding-top: calc(1.25rem + env(safe-area-inset-top));
  padding-bottom: calc(1.25rem + env(safe-area-inset-bottom));
  opacity: 0;
  visibility: hidden;
  pointer-events: none;
  transition: opacity .3s ease, visibility .3s ease;
}
.th-modal.is-open {
  opacity: 1;
  visibility: visible;
  pointer-events: auto;
}
.th-modal__bd {
  position: absolute;
  inset: 0;
  background: rgba(14,17,21,.78);
  -webkit-backdrop-filter: blur(22px);
  backdrop-filter: blur(22px);
}

.th-modal__panel {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 840px;
  max-height: calc(100dvh - 2.5rem);
  max-height: calc(100svh - 2.5rem);
  display: grid;
  grid-template-columns: 1fr;
  background: var(--bg-secondary);
  border: 1px solid rgba(10,186,181,.18);
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 32px 72px rgba(0,0,0,.65);
  transform: translateY(36px) scale(.97);
  opacity: 0;
  transition: transform .45s cubic-bezier(.22,1,.36,1), opacity .4s ease;
  -webkit-overflow-scrolling: touch;
}
.th-modal.is-open .th-modal__panel {
  transform: translateY(0) scale(1);
  opacity: 1;
}

@media (min-width: 680px) {
  .th-modal__panel { grid-template-columns: 44% 56%; }
}

.th-modal__close {
  position: absolute;
  top: 1rem;
  right: 1rem;
  z-index: 2;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(20,23,27,.9);
  border: 1px solid var(--glass-border);
  border-radius: 50%;
  color: var(--text-secondary);
  cursor: pointer;
  transition: border-color .25s, color .25s;
  -webkit-tap-highlight-color: transparent;
}
.th-modal__close:hover { border-color: rgba(10,186,181,.5); color: var(--tiffany); }

.th-modal__photo-wrap {
  position: relative;
  overflow: hidden;
  background: var(--bg-deep);
  aspect-ratio: 3/4;
}
@media (min-width: 680px) {
  .th-modal__photo-wrap { aspect-ratio: auto; }
}
.th-modal__photo {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: top center;
  display: block;
}

.th-modal__info {
  padding: 2.25rem 2rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
}

.th-modal__name {
  font-family: var(--font-display);
  font-size: 2.25rem;
  font-weight: 400;
  color: var(--text-primary);
  line-height: 1.1;
}

.th-modal__tags { display: flex; flex-wrap: wrap; gap: .5rem; }

.th-modal__bio {
  font-family: var(--font-body);
  font-size: .9rem;
  font-weight: 300;
  color: var(--text-secondary);
  line-height: 1.85;
  max-width: none;
}

.th-modal__svcs-title {
  font-family: var(--font-body);
  font-size: .65rem;
  font-weight: 500;
  letter-spacing: .15em;
  text-transform: uppercase;
  color: var(--text-muted);
  max-width: none;
}

.th-modal__svcs {
  display: flex;
  flex-wrap: wrap;
  gap: .5rem;
  list-style: none;
  margin-top: -.25rem;
}

/* ── Tags (override) ─────────────────────────────── */
.tag {
  font-family: var(--font-body);
  font-weight: 400;
}

/* ── Scroll reveal ───────────────────────────────── */
[data-reveal] {
  opacity: 0;
  transform: translateY(18px);
  transition: opacity .6s cubic-bezier(.4,0,.2,1), transform .6s cubic-bezier(.4,0,.2,1);
}
[data-reveal].is-visible { opacity: 1; transform: none; }

/* ── Mobile modal fullscreen ─────────────────────── */
@media (max-width: 599px) {
  .th-modal { padding: 0; align-items: stretch; }
  .th-modal__panel {
    max-width: none;
    max-height: 100dvh;
    max-height: 100svh;
    border-radius: 0;
    border: none;
  }
  .th-modal__close {
    top: calc(1rem + env(safe-area-inset-top));
    right: calc(1rem + env(safe-area-inset-right));
  }
}

@media (prefers-reduced-motion: reduce) {
  .th-modal, .th-modal__panel, [data-reveal] { transition: none; }
  [data-reveal] { opacity: 1; transform: none; }
}
'''


MODAL_JS = r'''
(function () {
  'use strict';

  // ── Modal ───────────────────────────────────────
  const modal = document.getElementById('th-modal');
  if (modal) {
    const photo   = document.getElementById('modal-photo');
    const name    = document.getElementById('modal-name');
    const tags    = document.getElementById('modal-tags');
    const bio     = document.getElementById('modal-bio');
    const svcsEl  = document.getElementById('modal-svcs');
    const ctaEl   = document.getElementById('modal-cta');
    const closes  = modal.querySelectorAll('[data-close-modal]');
    let lastFocus = null;
    let bodyScrollY = 0;

    function lockBody() {
      bodyScrollY = window.scrollY;
      document.body.style.position = 'fixed';
      document.body.style.top = '-' + bodyScrollY + 'px';
      document.body.style.width = '100%';
    }
    function unlockBody() {
      document.body.style.position = '';
      document.body.style.top = '';
      document.body.style.width = '';
      window.scrollTo(0, bodyScrollY);
    }

    function openModal(trigger) {
      lastFocus = trigger;
      const d = trigger.dataset;
      if (photo) { photo.src = d.photo || ''; photo.alt = d.name || ''; }
      if (name)  name.textContent = d.name || '';
      if (bio)   bio.textContent  = d.bio  || '';

      if (tags) {
        tags.innerHTML = '';
        (d.spec || '').split('|').filter(Boolean).forEach(s => {
          const sp = document.createElement('span');
          sp.className = 'tag tag--specialty';
          sp.textContent = s;
          tags.appendChild(sp);
        });
      }
      if (svcsEl) {
        svcsEl.innerHTML = '';
        (d.svcs || '').split('|').filter(Boolean).forEach(s => {
          const li = document.createElement('li');
          const sp = document.createElement('span');
          sp.className = 'tag tag--duration';
          sp.textContent = s;
          li.appendChild(sp);
          svcsEl.appendChild(li);
        });
      }

      modal.hidden = false;
      modal.setAttribute('aria-hidden', 'false');
      requestAnimationFrame(() => modal.classList.add('is-open'));
      lockBody();
      const closeBtn = modal.querySelector('.th-modal__close');
      if (closeBtn) closeBtn.focus();
    }

    function closeModal() {
      modal.classList.remove('is-open');
      modal.setAttribute('aria-hidden', 'true');
      unlockBody();
      const panel = modal.querySelector('.th-modal__panel');
      const onEnd = () => { modal.hidden = true; if (lastFocus) lastFocus.focus(); };
      if (panel) panel.addEventListener('transitionend', onEnd, { once: true });
      setTimeout(onEnd, 500);
    }

    document.querySelectorAll('[data-modal-trigger]').forEach(btn =>
      btn.addEventListener('click', () => openModal(btn))
    );
    closes.forEach(el => el.addEventListener('click', closeModal));
    document.addEventListener('keydown', e => {
      if (e.key === 'Escape' && modal.classList.contains('is-open')) closeModal();
    });
  }

  // ── Accordions (FAQ + process) ──────────────────
  function bindAccordion(root, itemSel, triggerSel, panelSel) {
    if (!root) return;
    root.querySelectorAll(itemSel).forEach(item => {
      const trigger = item.querySelector(triggerSel);
      const panel = item.querySelector(panelSel);
      if (!trigger || !panel) return;
      trigger.addEventListener('click', () => {
        const open = trigger.getAttribute('aria-expanded') === 'true';
        root.querySelectorAll(triggerSel).forEach(t => {
          t.setAttribute('aria-expanded', 'false');
          const p = t.closest(itemSel).querySelector(panelSel);
          if (p) p.classList.remove('is-open');
        });
        if (!open) {
          trigger.setAttribute('aria-expanded', 'true');
          panel.classList.add('is-open');
        }
      });
    });
  }

  document.querySelectorAll('.faq').forEach(el =>
    bindAccordion(el, '.faq__item', '.faq__question', '.faq__answer')
  );
  document.querySelectorAll('.proc-acc').forEach(el =>
    bindAccordion(el, '.proc-acc__item', '.proc-acc__trigger', '.proc-acc__panel')
  );

  // ── Scroll reveal ────────────────────────────────
  if ('IntersectionObserver' in window) {
    const obs = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          obs.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1 });
    document.querySelectorAll('[data-reveal]').forEach(el => obs.observe(el));
  } else {
    document.querySelectorAll('[data-reveal]').forEach(el => el.classList.add('is-visible'));
  }

})();
'''


# ─── Font injection string ─────────────────────────────────────────────────────
FONT_LINK = (
    '  <link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
    'family=DM+Serif+Display:ital@0;1'
    '&family=Jost:wght@300;400;500;600'
    '&family=Pinyon+Script'
    '&display=swap">\n'
)

CSS_BLOCK = (
    '  <link rel="stylesheet" href="/assets/css/tokens.css">\n'
    '  <link rel="stylesheet" href="/assets/css/base.css">\n'
    '  <link rel="stylesheet" href="/assets/css/components/glass.css">\n'
    '  <link rel="stylesheet" href="/assets/css/components/buttons.css">\n'
    '  <link rel="stylesheet" href="/assets/css/components/nav.css">\n'
    '  <link rel="stylesheet" href="/assets/css/components/footer.css">\n'
    '  <link rel="stylesheet" href="/assets/css/pages/home-v4.css">\n'
)


def fix_footer_structure(html: str) -> str:
    """Disclaimer full-width outside container; disclaimer before bottom bar."""
    # Wrap disclaimer text in <p class="footer__disclaimer-text">
    html = re.sub(
        r'<div class="footer__disclaimer">\s*([^<]+?)\s*</div>',
        lambda m: (
            '<div class="footer__disclaimer">\n'
            f'    <p class="footer__disclaimer-text">{m.group(1).strip()}</p>\n'
            '  </div>'
        ),
        html,
        count=1,
    )

    # Move disclaimer + bottom outside inner container if nested
    pattern = (
        r'(<div class="footer__grid">.*?</div>\s*)\s*'
        r'<div class="footer__disclaimer">.*?</div>\s*'
        r'<div class="footer__bottom">.*?</div>\s*'
        r'(</div>\s*</footer>)'
    )
    match = re.search(pattern, html, flags=re.DOTALL)
    if not match:
        return html

    grid_block = match.group(1)
    footer_close = match.group(2)

    disc_match = re.search(
        r'<div class="footer__disclaimer">.*?</div>',
        html,
        flags=re.DOTALL,
    )
    bottom_match = re.search(
        r'<div class="footer__bottom">.*?</div>',
        html,
        flags=re.DOTALL,
    )
    if not disc_match or not bottom_match:
        return html

    disc_block = disc_match.group(0)
    bottom_block = bottom_match.group(0)

    replacement = (
        f'{grid_block}  </div>\n\n  {disc_block}\n\n  <div class="container">\n    {bottom_block}\n  </div>\n{footer_close}'
    )
    return html[:match.start()] + replacement + html[match.end():]


def fix_logo_symbol(html: str) -> str:
    """Remove decorative logo symbols."""
    html = html.replace(
        '<span class="nav__logo-diamond" aria-hidden="true">◆</span>',
        '',
    )
    html = html.replace(
        '<span class="nav__logo-diamond" aria-hidden="true">✦</span>',
        '',
    )
    html = html.replace(
        '<span class="footer__logo-diamond" aria-hidden="true">◆</span>',
        '',
    )
    return html


def rebuild(lang: str) -> None:
    path = ROOT / lang / 'index.html'
    html = path.read_text(encoding='utf-8')

    # Remove all existing link stylesheet tags and preconnects
    html = re.sub(r' {2}<link rel="preconnect"[^\n]+\n', '', html)
    html = re.sub(r' {2}<link rel="stylesheet"[^\n]+\n', '', html)

    # Inject fonts + new CSS block after theme-color meta
    html = html.replace(
        '  <meta name="theme-color" content="#1a1d21">\n',
        '  <meta name="theme-color" content="#1a1d21">\n' + FONT_LINK + CSS_BLOCK,
    )

    # Replace main block
    start = html.find('<main id="main-content">')
    end   = html.find('</main>', start) + len('</main>')
    if start == -1 or end <= len('</main>'):
        print(f'WARNING: <main> not found in {lang}')
        return
    html = html[:start] + build_main(lang) + html[end:]

    # Remove legacy inline style block
    html = re.sub(r'\n  <!-- Process steps.*?</style>\n', '', html, flags=re.DOTALL)

    # Fix footer order
    html = fix_footer_structure(html)

    # Fix logo symbol
    html = fix_logo_symbol(html)

    # Replace scripts block
    new_scripts = (
        '  <script src="/assets/js/main.js" defer></script>\n'
        '  <script>\n' + MODAL_JS + '\n  </script>\n'
        '  <script>document.getElementById(\'footer-year\').textContent = new Date().getFullYear();</script>\n'
    )
    # Remove any old script block
    html = re.sub(
        r'  <script src="/assets/js/main\.js"[^\n]+\n.*?</script>\n',
        '',
        html,
        flags=re.DOTALL,
    )
    html = html.replace('</body>', new_scripts + '</body>')

    path.write_text(html, encoding='utf-8')
    print(f'Rebuilt {path}')


def main() -> None:
    css_path = ROOT / 'assets' / 'css' / 'pages' / 'home-v4.css'
    if not css_path.exists():
        css_path.write_text(HOME_CSS, encoding='utf-8')
        print(f'Wrote {css_path}')
    for lang in ('cs', 'en', 'ru'):
        rebuild(lang)


if __name__ == '__main__':
    main()
