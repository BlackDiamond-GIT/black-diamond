#!/usr/bin/env python3
"""Sync static index.html files with the onsen home redesign."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MODAL_CSS = '<link rel="stylesheet" href="/assets/css/components/modal.css">\n'

def inject_modal_css(html: str) -> str:
    if 'components/modal.css' in html:
        return html
    return html.replace(
        '<link rel="stylesheet" href="/assets/css/pages/home.css">',
        '<link rel="stylesheet" href="/assets/css/pages/home.css">\n  ' + MODAL_CSS.strip(),
    )


def build_main(lang: str) -> str:
    prefix = f'/{lang}'
    texts = LANG_TEXTS[lang]
    services = SERVICES[lang]
    therapists = THERAPISTS[lang]
    faqs = FAQS[lang]

    services_html = []
    layouts = ['left', 'right', 'left']
    for i, svc in enumerate(services):
        layout = layouts[i % 3]
        overlay = ''
        name_in_body = True
        if i == 0:
            overlay = f'''
            <div class="service-editorial__overlay">
              <h3 class="service-editorial__name">{svc["title"]}</h3>
            </div>'''
            name_in_body = False
        name_block = ''
        if name_in_body:
            name_block = f'<h3 class="service-editorial__name">{svc["title"]}</h3>'

        services_html.append(f'''
        <article class="service-editorial service-editorial--{layout}" role="listitem" data-ink>
          <div class="service-editorial__visual">
            <img src="{svc["img"]}" alt="{svc["alt"]}" width="800" height="600" loading="lazy" decoding="async">
            {overlay}
          </div>
          <div class="service-editorial__body">
            {name_block}
            <p class="service-editorial__description">{svc["desc"]}</p>
            <div class="service-editorial__meta">
              <span class="tag tag--duration">{svc["duration"]}</span>
              <span class="tag tag--price">{svc["price"]}</span>
            </div>
            <a href="{prefix}/masaze/{svc["slug"]}/" class="btn btn--ghost">{texts["service_detail"]}</a>
          </div>
        </article>''')

    therapists_html = []
    for t in therapists:
        therapists_html.append(f'''
        <button type="button"
          class="masseuse-portrait"
          role="listitem"
          data-therapist-trigger
          data-therapist-name="{t["name"]}"
          data-therapist-slug="{t["slug"]}"
          data-therapist-years="{t["years"]}"
          data-therapist-photo="{t["photo"]}"
          data-therapist-bio="{t["bio"]}"
          data-therapist-services="{t["services"]}"
          data-therapist-cta="{t["cta"]}"
          aria-label="{t["aria"]}">
          <img class="masseuse-portrait__image" src="{t["photo"]}" alt="{t["alt"]}"
            width="300" height="400" loading="lazy" decoding="async">
          <div class="masseuse-portrait__overlay">
            <span class="masseuse-portrait__name">{t["name"]}</span>
            <span class="masseuse-portrait__spec">{t["spec"]}</span>
          </div>
        </button>''')

    faqs_html = []
    for i, faq in enumerate(faqs, 1):
        faqs_html.append(f'''
          <div class="faq__item" role="listitem">
            <button class="faq__question" aria-expanded="false" aria-controls="faq-{i}">
              {faq["q"]}
              <span class="faq__icon" aria-hidden="true">
                <span class="faq__icon-line"></span>
              </span>
            </button>
            <div id="faq-{i}" class="faq__answer" role="region">
              <div class="faq__answer-inner">{faq["a"]}</div>
            </div>
          </div>''')

    process_html = []
    for step in PROCESS[lang]:
        process_html.append(f'''
        <li class="process-timeline__item" data-ink>
          <div class="process-timeline__marker" aria-hidden="true">{step["num"]}</div>
          <div class="process-timeline__content">
            <h3>{step["title"]}</h3>
            <p>{step["text"]}</p>
          </div>
        </li>''')

    return f'''
    <!-- Hero — split screen -->
    <section class="hero hero--split" aria-label="{texts["hero_aria"]}">
      <div class="hero__visual" aria-hidden="true">
        <div class="hero__bg">
          <img src="/assets/img/hero.webp" alt="" width="1920" height="1080" fetchpriority="high" decoding="async" data-parallax>
        </div>
        <div class="hero__noise"></div>
      </div>

      <div class="hero__layout">
        <div class="hero__content">
          <div class="hero__eyebrow" aria-hidden="true">{texts["eyebrow"]}</div>

          <h1 class="hero__title" data-ink>
            {texts["hero_title"]}
          </h1>

          <p class="hero__subtitle" data-ink>
            {texts["hero_subtitle"]}
          </p>

          <div class="hero__actions">
            <a href="{prefix}/rozvrh/" class="btn btn--primary btn--lg" aria-label="{texts["hero_cta_aria"]}">
              {texts["hero_cta"]}
            </a>
            <a href="{prefix}/masaze/" class="btn btn--secondary btn--lg">
              {texts["hero_secondary"]}
            </a>
          </div>
        </div>

        <aside class="hero__stats-col" aria-label="{texts["stats_aria"]}">
          <div class="hero__stat">
            <span class="hero__stat-value">6</span>
            <span class="hero__stat-label">{texts["stat_massages"]}</span>
          </div>
          <div class="hero__stat">
            <span class="hero__stat-value">6</span>
            <span class="hero__stat-label">{texts["stat_masseuses"]}</span>
          </div>
          <div class="hero__stat">
            <span class="hero__stat-value">4.9★</span>
            <span class="hero__stat-label">{texts["stat_rating"]}</span>
          </div>
        </aside>
      </div>

      <div class="hero__scroll" aria-hidden="true">
        <div class="hero__scroll-line"></div>
        <span>Scroll</span>
      </div>
    </section>

    <!-- Atmosphere -->
    <section class="atmosphere" aria-label="{texts["atmosphere_aria"]}">
      <div class="atmosphere__bg" aria-hidden="true">
        <img src="/assets/img/atmosphere.webp" alt="" width="1920" height="1080" loading="lazy" decoding="async">
      </div>
      <div class="atmosphere__mist mist-breath" aria-hidden="true"></div>
      <blockquote class="atmosphere__quote" data-ink>
        {texts["atmosphere_quote"]}
        <span class="atmosphere__quote-sub">{texts["atmosphere_sub"]}</span>
      </blockquote>
    </section>

    <!-- Services — editorial -->
    <section class="section-services" aria-labelledby="services-heading">
      <div class="container">
        <header class="section-header section-header--center">
          <span class="section-label" aria-hidden="true">{texts["services_label"]}</span>
          <h2 class="section-title" id="services-heading" data-line>{texts["services_title"]}</h2>
          <span class="section-line" aria-hidden="true"></span>
          <p class="section-subtitle">{texts["services_subtitle"]}</p>
        </header>

        <div class="services-editorial" role="list">
          {''.join(services_html)}
        </div>

        <div style="text-align:center;margin-top:var(--sp-3xl)">
          <a href="{prefix}/masaze/" class="btn btn--secondary btn--lg">{texts["all_massages"]}</a>
        </div>
      </div>
    </section>

    <!-- Masseuses — portrait gallery -->
    <section class="section-masseuses" aria-labelledby="masseuses-heading" style="background:var(--bg-tertiary)">
      <div class="container">
        <header class="section-header section-header--center">
          <span class="section-label" aria-hidden="true">{texts["team_label"]}</span>
          <h2 class="section-title" id="masseuses-heading" data-line>{texts["team_title"]}</h2>
          <span class="section-line" aria-hidden="true"></span>
          <p class="section-subtitle">{texts["team_subtitle"]}</p>
        </header>

        <div class="masseuse-gallery" role="list">
          {''.join(therapists_html)}
        </div>

        <div style="text-align:center;margin-top:var(--sp-3xl)">
          <a href="{prefix}/masazistky/" class="btn btn--secondary btn--lg">{texts["all_masseuses"]}</a>
        </div>
      </div>
    </section>

    <!-- Process timeline -->
    <section class="section-process" aria-labelledby="process-heading">
      <div class="container">
        <header class="section-header section-header--center">
          <span class="section-label" aria-hidden="true">{texts["process_label"]}</span>
          <h2 class="section-title" id="process-heading" data-line>{texts["process_title"]}</h2>
          <span class="section-line" aria-hidden="true"></span>
        </header>

        <ol class="process-timeline" aria-label="{texts["process_aria"]}">
          {''.join(process_html)}
        </ol>
      </div>
    </section>

    <!-- FAQ -->
    <section class="section-faq" aria-labelledby="faq-heading" style="background:var(--bg-tertiary)">
      <div class="container">
        <header class="section-header section-header--center">
          <span class="section-label" aria-hidden="true">FAQ</span>
          <h2 class="section-title" id="faq-heading" data-line>{texts["faq_title"]}</h2>
          <span class="section-line" aria-hidden="true"></span>
        </header>

        <div class="faq" role="list">
          {''.join(faqs_html)}
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section class="section-cta" aria-labelledby="cta-heading">
      <div class="container">
        <span class="section-label" aria-hidden="true">{texts["cta_label"]}</span>
        <h2 class="section-title" id="cta-heading" style="font-size:var(--fs-h1);max-width:16ch;margin-inline:auto">
          {texts["cta_title"]}
        </h2>
        <p class="section-subtitle" style="margin-inline:auto;margin-top:var(--sp-lg);margin-bottom:var(--sp-3xl)">
          {texts["cta_subtitle"]}
        </p>
        <div style="display:flex;flex-wrap:wrap;gap:var(--sp-md);justify-content:center">
          <a href="{prefix}/rozvrh/" class="btn btn--primary btn--lg">{texts["cta_primary"]}</a>
          <a href="{prefix}/kontakty/" class="btn btn--secondary btn--lg">{texts["cta_secondary"]}</a>
        </div>
      </div>
    </section>

    <!-- Therapist modal -->
    <div class="therapist-modal" id="therapist-modal" role="dialog" aria-modal="true" aria-hidden="true" hidden>
      <div class="therapist-modal__backdrop" data-therapist-close></div>
      <div class="therapist-modal__panel">
        <button type="button" class="therapist-modal__close" data-therapist-close aria-label="{texts["modal_close"]}">×</button>
        <div class="therapist-modal__photo-wrap">
          <img class="therapist-modal__photo" src="" alt="" width="480" height="600" decoding="async">
          <span class="therapist-modal__years" hidden></span>
        </div>
        <div class="therapist-modal__info">
          <h2 class="therapist-modal__name"></h2>
          <div class="therapist-modal__tags"></div>
          <p class="therapist-modal__bio"></p>
          <p class="therapist-modal__services-title">{texts["modal_services"]}</p>
          <ul class="therapist-modal__services"></ul>
          <a href="{prefix}/rozvrh/" class="btn btn--primary btn--lg therapist-modal__cta" data-default-label="{texts["modal_reserve"]}">{texts["modal_reserve"]}</a>
        </div>
      </div>
    </div>
'''


LANG_TEXTS = {
    'cs': {
        'hero_aria': 'Uvítací sekce',
        'eyebrow': 'Nové Město · Prémiový salon',
        'hero_title': 'Umění<br><em>relaxace</em><br>ve vašich<br>rukou',
        'hero_subtitle': 'Zkušené masérky, privátní kabinety a luxusní atmosféra v srdci Prahy. Dopřejte si klid a regeneraci, které si zasloužíte.',
        'hero_cta': 'Rezervovat masáž',
        'hero_cta_aria': 'Rezervovat masáž online',
        'hero_secondary': 'Naše masáže',
        'stats_aria': 'Statistiky salonu',
        'stat_massages': 'Masáží',
        'stat_masseuses': 'Masérky',
        'stat_rating': 'Hodnocení',
        'atmosphere_aria': 'Atmosféra salonu',
        'atmosphere_quote': 'Čas zastavit čas.',
        'atmosphere_sub': 'Ticho, voda, péče',
        'services_label': 'Naše služby',
        'services_title': 'Masáže pro každou potřebu',
        'services_subtitle': 'VIP, relaxační, pro ženy nebo pro páry — vyberte masáž, která vám přinese úlevu.',
        'service_detail': 'Detail masáže',
        'all_massages': 'Všechny masáže',
        'team_label': 'Náš tým',
        'team_title': 'Zkušené masérky',
        'team_subtitle': 'Šest zkušených specialistek, každá s vlastním přístupem a hlubokými znalostmi masážních technik.',
        'all_masseuses': 'Všechny masérky',
        'process_label': 'Jak to funguje',
        'process_title': '4 kroky k dokonalé relaxaci',
        'process_aria': 'Kroky rezervace a masáže',
        'faq_title': 'Časté otázky',
        'cta_label': 'Dopřejte si',
        'cta_title': 'Vaše cesta k dokonalé relaxaci začíná zde',
        'cta_subtitle': 'Rezervujte si masáž ještě dnes a nechte se unést péčí, která obnoví vaše tělo i mysl.',
        'cta_primary': 'Rezervovat nyní',
        'cta_secondary': 'Kontaktovat nás',
        'modal_close': 'Zavřít',
        'modal_services': 'Nabízené masáže',
        'modal_reserve': 'Rezervovat',
    },
    'en': {
        'hero_aria': 'Welcome section',
        'eyebrow': 'Prague 1 · Premium salon',
        'hero_title': 'The art<br>of <em>relaxation</em><br>in your<br>hands',
        'hero_subtitle': 'Experienced masseuses, private cabins and a luxurious atmosphere in the heart of Prague. Give yourself the peace and regeneration you deserve.',
        'hero_cta': 'Book a massage',
        'hero_cta_aria': 'Book massage online',
        'hero_secondary': 'Our massages',
        'stats_aria': 'Salon statistics',
        'stat_massages': 'Massages',
        'stat_masseuses': 'Masseuses',
        'stat_rating': 'Rating',
        'atmosphere_aria': 'Salon atmosphere',
        'atmosphere_quote': 'Time to stop time.',
        'atmosphere_sub': 'Silence, water, care',
        'services_label': 'Our services',
        'services_title': 'Massages for every need',
        'services_subtitle': 'VIP, relaxation, for women or for couples — choose the massage that brings you relief.',
        'service_detail': 'Massage details',
        'all_massages': 'All massages',
        'team_label': 'Our team',
        'team_title': 'Experienced masseuses',
        'team_subtitle': 'Six experienced specialists, each with a unique approach and deep knowledge of massage techniques.',
        'all_masseuses': 'All masseuses',
        'process_label': 'How it works',
        'process_title': '4 steps to perfect relaxation',
        'process_aria': 'Booking and massage steps',
        'faq_title': 'Frequently asked questions',
        'cta_label': 'Treat yourself',
        'cta_title': 'Your journey to perfect relaxation starts here',
        'cta_subtitle': 'Book your massage today and let care restore your body and mind.',
        'cta_primary': 'Book now',
        'cta_secondary': 'Contact us',
        'modal_close': 'Close',
        'modal_services': 'Offered massages',
        'modal_reserve': 'Book',
    },
    'ru': {
        'hero_aria': 'Главная секция',
        'eyebrow': 'Прага 1 · Премиальный салон',
        'hero_title': 'Искусство<br><em>расслабления</em><br>в ваших<br>руках',
        'hero_subtitle': 'Опытные массажистки, приватные кабинеты и роскошная атмосфера в сердце Праги. Подарите себе покой и восстановление, которое вы заслуживаете.',
        'hero_cta': 'Записаться на массаж',
        'hero_cta_aria': 'Записаться на массаж онлайн',
        'hero_secondary': 'Наши массажи',
        'stats_aria': 'Статистика салона',
        'stat_massages': 'Массажей',
        'stat_masseuses': 'Массажистки',
        'stat_rating': 'Оценка',
        'atmosphere_aria': 'Атмосфера салона',
        'atmosphere_quote': 'Время остановить время.',
        'atmosphere_sub': 'Тишина, вода, уход',
        'services_label': 'Наши услуги',
        'services_title': 'Массаж для любой потребности',
        'services_subtitle': 'VIP, расслабляющий, для женщин или для пар — выберите массаж, который принесёт вам облегчение.',
        'service_detail': 'Подробнее о массаже',
        'all_massages': 'Все массажи',
        'team_label': 'Наша команда',
        'team_title': 'Опытные массажистки',
        'team_subtitle': 'Шесть опытных специалисток с уникальным подходом и глубокими знаниями массажных техник.',
        'all_masseuses': 'Все массажистки',
        'process_label': 'Как это работает',
        'process_title': '4 шага к идеальному расслаблению',
        'process_aria': 'Шаги бронирования и массажа',
        'faq_title': 'Частые вопросы',
        'cta_label': 'Подарите себе',
        'cta_title': 'Ваш путь к идеальному расслаблению начинается здесь',
        'cta_subtitle': 'Забронируйте массаж сегодня и позвольте уходу восстановить ваше тело и разум.',
        'cta_primary': 'Забронировать',
        'cta_secondary': 'Связаться с нами',
        'modal_close': 'Закрыть',
        'modal_services': 'Предлагаемые массажи',
        'modal_reserve': 'Забронировать',
    },
}

SERVICES = {
    'cs': [
        {
            'slug': 'vip-masaz', 'title': 'VIP masáž',
            'desc': 'Luxusní VIP masáž s plnou pozorností masérky, prémiálními oleji a individuálním přístupem od začátku do konce.',
            'duration': 'od 30 min', 'price': 'od 1&nbsp;800 Kč',
            'img': '/assets/img/services/vip-masaz.webp',
            'alt': 'VIP masáž Praha — Black Diamond Spa',
        },
        {
            'slug': 'relaxacni-masaz', 'title': 'Relaxační masáž',
            'desc': 'Jemná relaxační masáž s prémiálními oleji pro hluboké uvolnění těla i mysli v klidné privátní atmosféře.',
            'duration': 'od 30 min', 'price': 'od 1&nbsp;600 Kč',
            'img': '/assets/img/services/relaxacni-masaz.webp',
            'alt': 'Relaxační masáž Praha — Black Diamond Spa',
        },
        {
            'slug': 'masaz-pro-zeny', 'title': 'Masáž pro ženy',
            'desc': 'Masáž navržená speciálně pro potřeby ženského těla — jemná, bezpečná a zcela privátní.',
            'duration': 'od 45 min', 'price': 'od 3&nbsp;200 Kč',
            'img': '/assets/img/services/masaz-pro-zeny.webp',
            'alt': 'Masáž pro ženy Praha — Black Diamond Spa',
        },
        {
            'slug': 'masaz-pro-pary', 'title': 'Masáž pro páry',
            'desc': 'Párová masáž pro dvě osoby ve společném prostoru — sdílená relaxace a společný zážitek.',
            'duration': 'od 30 min', 'price': 'od 1&nbsp;400 Kč',
            'img': '/assets/img/services/masaz-pro-pary.webp',
            'alt': 'Masáž pro páry Praha — Black Diamond Spa',
        },
    ],
    'en': [
        {
            'slug': 'vip-masaz', 'title': 'VIP Massage',
            'desc': 'Luxury VIP massage with full masseuse attention, premium oils and individual care from start to finish.',
            'duration': 'from 30 min', 'price': 'from 1,800&nbsp;CZK',
            'img': '/assets/img/services/vip-masaz.webp',
            'alt': 'VIP Massage Prague — Black Diamond Spa',
        },
        {
            'slug': 'relaxacni-masaz', 'title': 'Relaxation Massage',
            'desc': 'Gentle relaxation massage with premium oils for deep release of body and mind in a calm private atmosphere.',
            'duration': 'from 30 min', 'price': 'from 1,600&nbsp;CZK',
            'img': '/assets/img/services/relaxacni-masaz.webp',
            'alt': 'Relaxation Massage Prague — Black Diamond Spa',
        },
        {
            'slug': 'masaz-pro-zeny', 'title': 'Massage for Women',
            'desc': 'Massage designed specifically for women\'s needs — gentle, safe and fully private.',
            'duration': 'from 45 min', 'price': 'from 3,200&nbsp;CZK',
            'img': '/assets/img/services/masaz-pro-zeny.webp',
            'alt': 'Massage for Women Prague — Black Diamond Spa',
        },
        {
            'slug': 'masaz-pro-pary', 'title': 'Couples Massage',
            'desc': 'Couples massage for two in a shared space — shared relaxation and a joint experience.',
            'duration': 'from 30 min', 'price': 'from 1,400&nbsp;CZK',
            'img': '/assets/img/services/masaz-pro-pary.webp',
            'alt': 'Couples Massage Prague — Black Diamond Spa',
        },
    ],
    'ru': [
        {
            'slug': 'vip-masaz', 'title': 'VIP-массаж',
            'desc': 'Роскошный VIP-массаж с полным вниманием массажистки, премиальными маслами и индивидуальным подходом.',
            'duration': 'от 30 мин', 'price': 'от 1&nbsp;800 Kč',
            'img': '/assets/img/services/vip-masaz.webp',
            'alt': 'VIP-массаж Прага — Black Diamond Spa',
        },
        {
            'slug': 'relaxacni-masaz', 'title': 'Расслабляющий массаж',
            'desc': 'Мягкий расслабляющий массаж с премиальными маслами для глубокого снятия напряжения в приватной атмосфере.',
            'duration': 'от 30 мин', 'price': 'от 1&nbsp;600 Kč',
            'img': '/assets/img/services/relaxacni-masaz.webp',
            'alt': 'Расслабляющий массаж Прага — Black Diamond Spa',
        },
        {
            'slug': 'masaz-pro-zeny', 'title': 'Массаж для женщин',
            'desc': 'Массаж, разработанный специально для потребностей женского тела — мягкий, безопасный и полностью приватный.',
            'duration': 'от 45 мин', 'price': 'от 3&nbsp;200 Kč',
            'img': '/assets/img/services/masaz-pro-zeny.webp',
            'alt': 'Массаж для женщин Прага — Black Diamond Spa',
        },
        {
            'slug': 'masaz-pro-pary', 'title': 'Массаж для пар',
            'desc': 'Массаж для двоих в общем пространстве — совместная релаксация и общий опыт.',
            'duration': 'от 30 мин', 'price': 'от 1&nbsp;400 Kč',
            'img': '/assets/img/services/masaz-pro-pary.webp',
            'alt': 'Массаж для пар Прага — Black Diamond Spa',
        },
    ],
}

THERAPISTS = {
    'cs': [
        {
            'slug': 'julia', 'name': 'Julia', 'years': '8 let', 'spec': 'Klasická & Relax masáž',
            'photo': '/assets/img/masseuses/julia.webp',
            'alt': 'Julia — masérka Black Diamond Spa Praha',
            'bio': 'Julia je zkušená masérka specializující se na klasickou a relax masáž. Přizpůsobuje každé sezení potřebám klienta a navozuje hlubokou relaxaci.',
            'services': 'Klasická masáž|Relax masáž|Uvolňující masáž',
            'cta': 'Rezervovat s Julia', 'aria': 'Zobrazit profil Julia',
        },
        {
            'slug': 'diana', 'name': 'Diana', 'years': '5 let', 'spec': 'Uvolňující & Aromamasáž',
            'photo': '/assets/img/masseuses/diana.webp',
            'alt': 'Diana — masérka Black Diamond Spa Praha',
            'bio': 'Diana se zaměřuje na uvolňující a aromamasáže. Její přístup je klidný a citlivý, ideální pro ty, kdo hledají hluboký odpočinek.',
            'services': 'Uvolňující masáž|Aromamasáž',
            'cta': 'Rezervovat s Diana', 'aria': 'Zobrazit profil Diana',
        },
        {
            'slug': 'laura', 'name': 'Laura', 'years': '6 let', 'spec': 'Aromamasáž & Relax masáž',
            'photo': '/assets/img/masseuses/laura.webp',
            'alt': 'Laura — masérka Black Diamond Spa Praha',
            'bio': 'Laura kombinuje aromamasáž a relax masáž s důrazem na harmonii těla a mysli prostřednictvím éterických olejů.',
            'services': 'Aromamasáž|Relax masáž',
            'cta': 'Rezervovat s Laura', 'aria': 'Zobrazit profil Laura',
        },
        {
            'slug': 'vanessa', 'name': 'Vanessa', 'years': '10 let', 'spec': 'Klasická & Sportovní masáž',
            'photo': '/assets/img/masseuses/vanessa.webp',
            'alt': 'Vanessa — masérka Black Diamond Spa Praha',
            'bio': 'Vanessa má deset let praxe v klasické a sportovní masáži. Pomáhá uvolnit napětí po sportu i v každodenním životě.',
            'services': 'Klasická masáž|Sportovní masáž',
            'cta': 'Rezervovat s Vanessa', 'aria': 'Zobrazit profil Vanessa',
        },
        {
            'slug': 'ella', 'name': 'Ella', 'years': '7 let', 'spec': 'Sportovní & Regenerační masáž',
            'photo': '/assets/img/masseuses/ella.webp',
            'alt': 'Ella — masérka Black Diamond Spa Praha',
            'bio': 'Ella se specializuje na sportovní a regenerační masáže. Její techniky podporují zotavení svalů a celkovou regeneraci.',
            'services': 'Sportovní masáž|Regenerační masáž',
            'cta': 'Rezervovat s Ella', 'aria': 'Zobrazit profil Ella',
        },
        {
            'slug': 'mira', 'name': 'Mira', 'years': '4 let', 'spec': 'Lymfatická & Aromamasáž',
            'photo': '/assets/img/masseuses/mira.webp',
            'alt': 'Mira — masérka Black Diamond Spa Praha',
            'bio': 'Mira nabízí lymfatickou a aromamasáž s jemným přístupem, který podporuje detoxikaci a relaxaci.',
            'services': 'Lymfatická masáž|Aromamasáž',
            'cta': 'Rezervovat s Mira', 'aria': 'Zobrazit profil Mira',
        },
    ],
    'en': [
        {
            'slug': 'julia', 'name': 'Julia', 'years': '8 years', 'spec': 'Classic & Relax massage',
            'photo': '/assets/img/masseuses/julia.webp',
            'alt': 'Julia — masseuse Black Diamond Spa Prague',
            'bio': 'Julia is an experienced masseuse specializing in classic and relax massage, tailoring each session to client needs.',
            'services': 'Classic massage|Relax massage|Relaxing massage',
            'cta': 'Book with Julia', 'aria': 'View Julia profile',
        },
        {
            'slug': 'diana', 'name': 'Diana', 'years': '5 years', 'spec': 'Relaxing & Aroma massage',
            'photo': '/assets/img/masseuses/diana.webp',
            'alt': 'Diana — masseuse Black Diamond Spa Prague',
            'bio': 'Diana focuses on relaxing and aroma massages with a calm, sensitive approach for deep rest.',
            'services': 'Relaxing massage|Aroma massage',
            'cta': 'Book with Diana', 'aria': 'View Diana profile',
        },
        {
            'slug': 'laura', 'name': 'Laura', 'years': '6 years', 'spec': 'Aroma & Relax massage',
            'photo': '/assets/img/masseuses/laura.webp',
            'alt': 'Laura — masseuse Black Diamond Spa Prague',
            'bio': 'Laura combines aroma and relax massage with essential oils for body and mind harmony.',
            'services': 'Aroma massage|Relax massage',
            'cta': 'Book with Laura', 'aria': 'View Laura profile',
        },
        {
            'slug': 'vanessa', 'name': 'Vanessa', 'years': '10 years', 'spec': 'Classic & Sports massage',
            'photo': '/assets/img/masseuses/vanessa.webp',
            'alt': 'Vanessa — masseuse Black Diamond Spa Prague',
            'bio': 'Vanessa has ten years of experience in classic and sports massage, helping release tension after sport and daily life.',
            'services': 'Classic massage|Sports massage',
            'cta': 'Book with Vanessa', 'aria': 'View Vanessa profile',
        },
        {
            'slug': 'ella', 'name': 'Ella', 'years': '7 years', 'spec': 'Sports & Recovery massage',
            'photo': '/assets/img/masseuses/ella.webp',
            'alt': 'Ella — masseuse Black Diamond Spa Prague',
            'bio': 'Ella specializes in sports and recovery massage to support muscle recovery and regeneration.',
            'services': 'Sports massage|Recovery massage',
            'cta': 'Book with Ella', 'aria': 'View Ella profile',
        },
        {
            'slug': 'mira', 'name': 'Mira', 'years': '4 years', 'spec': 'Lymphatic & Aroma massage',
            'photo': '/assets/img/masseuses/mira.webp',
            'alt': 'Mira — masseuse Black Diamond Spa Prague',
            'bio': 'Mira offers lymphatic and aroma massage with a gentle approach supporting detox and relaxation.',
            'services': 'Lymphatic massage|Aroma massage',
            'cta': 'Book with Mira', 'aria': 'View Mira profile',
        },
    ],
    'ru': [
        {
            'slug': 'julia', 'name': 'Julia', 'years': '8 лет', 'spec': 'Классический & Релакс массаж',
            'photo': '/assets/img/masseuses/julia.webp',
            'alt': 'Julia — массажистка Black Diamond Spa Прага',
            'bio': 'Julia — опытная массажистка, специализирующаяся на классическом и релакс-массаже.',
            'services': 'Классический массаж|Релакс массаж|Расслабляющий массаж',
            'cta': 'Забронировать с Julia', 'aria': 'Профиль Julia',
        },
        {
            'slug': 'diana', 'name': 'Diana', 'years': '5 лет', 'spec': 'Расслабляющий & Аромамассаж',
            'photo': '/assets/img/masseuses/diana.webp',
            'alt': 'Diana — массажистка Black Diamond Spa Прага',
            'bio': 'Diana специализируется на расслабляющем и аромамассаже с мягким и внимательным подходом.',
            'services': 'Расслабляющий массаж|Аромамассаж',
            'cta': 'Забронировать с Diana', 'aria': 'Профиль Diana',
        },
        {
            'slug': 'laura', 'name': 'Laura', 'years': '6 лет', 'spec': 'Арома & Релакс массаж',
            'photo': '/assets/img/masseuses/laura.webp',
            'alt': 'Laura — массажистка Black Diamond Spa Прага',
            'bio': 'Laura сочетает арома и релакс-массаж с эфирными маслами для гармонии тела и разума.',
            'services': 'Аромамассаж|Релакс массаж',
            'cta': 'Забронировать с Laura', 'aria': 'Профиль Laura',
        },
        {
            'slug': 'vanessa', 'name': 'Vanessa', 'years': '10 лет', 'spec': 'Классический & Спортивный массаж',
            'photo': '/assets/img/masseuses/vanessa.webp',
            'alt': 'Vanessa — массажистка Black Diamond Spa Прага',
            'bio': 'Vanessa имеет десять лет опыта в классическом и спортивном массаже.',
            'services': 'Классический массаж|Спортивный массаж',
            'cta': 'Забронировать с Vanessa', 'aria': 'Профиль Vanessa',
        },
        {
            'slug': 'ella', 'name': 'Ella', 'years': '7 лет', 'spec': 'Спортивный & Регенерационный массаж',
            'photo': '/assets/img/masseuses/ella.webp',
            'alt': 'Ella — массажистка Black Diamond Spa Прага',
            'bio': 'Ella специализируется на спортивном и регенерационном массаже для восстановления мышц.',
            'services': 'Спортивный массаж|Регенерационный массаж',
            'cta': 'Забронировать с Ella', 'aria': 'Профиль Ella',
        },
        {
            'slug': 'mira', 'name': 'Mira', 'years': '4 лет', 'spec': 'Лимфодренажный & Аромамассаж',
            'photo': '/assets/img/masseuses/mira.webp',
            'alt': 'Mira — массажистка Black Diamond Spa Прага',
            'bio': 'Mira предлагает лимфодренажный и аромамассаж с мягким подходом для детокса и расслабления.',
            'services': 'Лимфодренажный массаж|Аромамассаж',
            'cta': 'Забронировать с Mira', 'aria': 'Профиль Mira',
        },
    ],
}

PROCESS = {
    'cs': [
        {'num': '01', 'title': 'Vyberte masáž', 'text': 'Prozkoumejte náš katalog masáží a vyberte typ, který nejlépe odpovídá vašim potřebám.'},
        {'num': '02', 'title': 'Zvolte masérku', 'text': 'Každá z našich šesti masérky má jedinečnou specializaci. Vyberte tu, která vám vyhovuje.'},
        {'num': '03', 'title': 'Rezervujte termín', 'text': 'V rozvrhu vyberte volný termín a potvrďte rezervaci. Potvrzení obdržíte e-mailem.'},
        {'num': '04', 'title': 'Relaxujte', 'text': 'Přijďte 10 minut předem. Vše ostatní necháme na nás — váš čas je jen pro vás.'},
    ],
    'en': [
        {'num': '01', 'title': 'Choose a massage', 'text': 'Browse our massage catalog and pick the type that best fits your needs.'},
        {'num': '02', 'title': 'Pick a masseuse', 'text': 'Each of our six masseuses has a unique specialty. Choose the one you prefer.'},
        {'num': '03', 'title': 'Book a time', 'text': 'Select an available slot in the schedule and confirm. You will receive email confirmation.'},
        {'num': '04', 'title': 'Relax', 'text': 'Arrive 10 minutes early. We take care of everything else — your time is yours alone.'},
    ],
    'ru': [
        {'num': '01', 'title': 'Выберите массаж', 'text': 'Изучите каталог массажей и выберите тип, который лучше всего подходит вашим потребностям.'},
        {'num': '02', 'title': 'Выберите массажистку', 'text': 'Каждая из шести массажисток имеет уникальную специализацию. Выберите подходящую.'},
        {'num': '03', 'title': 'Забронируйте время', 'text': 'Выберите свободный слот в расписании и подтвердите. Подтверждение придёт по email.'},
        {'num': '04', 'title': 'Расслабьтесь', 'text': 'Приходите за 10 минут. Всё остальное — на нас. Ваше время только для вас.'},
    ],
}

FAQS = {
    'cs': [
        {'q': 'Jak se připravit na masáž?', 'a': 'Před masáží doporučujeme přijít 10 minut předem, přijít čistí a hydratovaní. Vyhněte se jídlu hodinu před masáží.'},
        {'q': 'Jak rezervovat masáž?', 'a': 'Rezervaci provedete online v sekci <a href="/cs/rozvrh/">Rozvrh</a> — vyberte masáž, zvolte masérku a volný termín.'},
        {'q': 'Jak dlouho masáž trvá?', 'a': 'Délka masáže závisí na vybraném typu: od 60 minut (klasická, sportovní) do 90 minut (uvolňující).'},
        {'q': 'Jak probíhá platba?', 'a': 'Přijímáme hotovost i platební karty. Platba probíhá na místě po skončení masáže.'},
        {'q': 'Nabízíte párovou masáž?', 'a': 'Ano, párová masáž je možná po domluvě. Kontaktujte nás pro rezervaci pro dvě osoby.'},
        {'q': 'Co je zahrnuto v ceně?', 'a': 'V ceně jsou masážní oleje, prostěradla a přístup do relaxační zóny.'},
    ],
    'en': [
        {'q': 'How to prepare for a massage?', 'a': 'Arrive 10 minutes early, clean and hydrated. Avoid eating one hour before your massage.'},
        {'q': 'How to book a massage?', 'a': 'Book online in the <a href="/en/rozvrh/">Schedule</a> section — choose massage, masseuse and available slot.'},
        {'q': 'How long does a massage last?', 'a': 'Duration depends on type: from 60 minutes (classic, sports) up to 90 minutes (relaxing).'},
        {'q': 'How does payment work?', 'a': 'We accept cash and cards. Payment is made on site after the massage.'},
        {'q': 'Do you offer couples massage?', 'a': 'Yes, couples massage is available upon request. Contact us to book for two people.'},
        {'q': 'What is included in the price?', 'a': 'Massage oils, linens and access to the relaxation zone are included.'},
    ],
    'ru': [
        {'q': 'Как подготовиться к массажу?', 'a': 'Приходите за 10 минут, чистым и гидратированным. Избегайте еды за час до массажа.'},
        {'q': 'Как забронировать массаж?', 'a': 'Бронирование онлайн в разделе <a href="/ru/rozvrh/">Расписание</a> — выберите массаж, массажистку и время.'},
        {'q': 'Как долго длится массаж?', 'a': 'От 60 минут (классический, спортивный) до 90 минут (расслабляющий).'},
        {'q': 'Как происходит оплата?', 'a': 'Принимаем наличные и карты. Оплата на месте после массажа.'},
        {'q': 'Предлагаете парный массаж?', 'a': 'Да, парный массаж возможен по запросу. Свяжитесь с нами для бронирования для двух людей.'},
        {'q': 'Что включено в цену?', 'a': 'Масляные составы, простыни и доступ к зоне отдыха.'},
    ],
}


def replace_main(html: str, new_main_inner: str) -> str:
    start = html.find('<main id="main-content">')
    end = html.find('</main>', start)
    if start == -1 or end == -1:
        raise ValueError('main block not found')
    return html[:start + len('<main id="main-content">')] + new_main_inner + html[end:]


def remove_legacy_styles(html: str) -> str:
    marker = '<!-- Process steps grid → responsive -->'
    if marker in html:
        html = html.split(marker)[0].rstrip() + '\n</body>\n</html>\n'
    return html


def sync_lang(lang: str) -> None:
    path = ROOT / lang / 'index.html'
    html = path.read_text(encoding='utf-8')
    html = inject_modal_css(html)
    html = replace_main(html, build_main(lang))
    html = remove_legacy_styles(html)
    path.write_text(html, encoding='utf-8')
    print(f'Updated {path}')


def main() -> None:
    for lang in ('cs', 'en', 'ru'):
        sync_lang(lang)


if __name__ == '__main__':
    main()
