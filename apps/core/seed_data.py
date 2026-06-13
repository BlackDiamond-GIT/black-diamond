"""Дані для seed_site — масажі, масажистки, мапінг спеціальностей."""

SERVICES = [
    {
        'slug': 'klasicka-masaz',
        'order': 1,
        'duration': 60,
        'price': 1200,
        'title_cs': 'Klasická masáž',
        'title_en': 'Classic massage',
        'title_ru': 'Классический массаж',
        'short_cs': 'Tradiční švédská masáž pro uvolnění svalového napětí a celkovou relaxaci celého těla.',
        'short_en': 'Traditional Swedish massage to release muscle tension and relax the whole body.',
        'short_ru': 'Традиционный шведский массаж для снятия мышечного напряжения и общего расслабления.',
        'description_cs': (
            'Tradiční švédská masáž pro uvolnění svalového napětí a celkovou relaxaci celého těla '
            'pomocí hladivých a hnětacích hmatů. Klasická masáž je základem péče o pohybový aparát.'
        ),
        'description_en': (
            'Traditional Swedish massage to release muscle tension and relax the whole body '
            'with flowing and kneading strokes. A foundation of musculoskeletal care.'
        ),
        'description_ru': (
            'Традиционный шведский массаж для снятия мышечного напряжения и общего расслабления '
            'плавными и разминательными движениями.'
        ),
    },
    {
        'slug': 'cbd-relaxacni-masaz',
        'order': 2,
        'duration': 75,
        'price': 1700,
        'title_cs': 'Relax masáž',
        'title_en': 'Relax massage',
        'title_ru': 'Релакс массаж',
        'short_cs': 'Jemná relaxační masáž s prémiálními oleji pro hluboké uvolnění těla i mysli.',
        'short_en': 'Gentle relaxation massage with premium oils for deep release of body and mind.',
        'short_ru': 'Мягкий релакс-массаж с премиальными маслами для глубокого расслабления.',
        'description_cs': (
            'Jemná relaxační masáž s prémiálními oleji pro hluboké uvolnění těla i mysli. '
            'Pomalé, plynulé tahy navozují hluboký klid v privátní atmosféře salonu.'
        ),
        'description_en': (
            'Gentle relaxation massage with premium oils for deep release of body and mind '
            'in a calm and private setting.'
        ),
        'description_ru': (
            'Мягкий релакс-массаж с премиальными маслами для глубокого расслабления тела и разума.'
        ),
    },
    {
        'slug': 'thajska-masaz',
        'order': 3,
        'duration': 90,
        'price': 1600,
        'title_cs': 'Uvolňující masáž',
        'title_en': 'Relaxing massage',
        'title_ru': 'Расслабляющий массаж',
        'short_cs': 'Hluboká relaxace s pomalými technikami pro uvolnění celého těla a mysli.',
        'short_en': 'Deep relaxation with slow techniques to release tension throughout body and mind.',
        'short_ru': 'Глубокое расслабление медленными техниками для снятия напряжения.',
        'description_cs': (
            'Uvolňující masáž s pomalými technikami pro hluboké uvolnění svalů i mysli. '
            'Ideální pro ty, kdo hledají klid a regeneraci po náročném období.'
        ),
        'description_en': (
            'Relaxing massage with slow techniques for deep muscle and mental release. '
            'Ideal after stressful periods.'
        ),
        'description_ru': (
            'Расслабляющий массаж медленными техниками для глубокого снятия напряжения.'
        ),
    },
    {
        'slug': 'sportovni-masaz',
        'order': 4,
        'duration': 60,
        'price': 1500,
        'title_cs': 'Sportovní masáž',
        'title_en': 'Sports massage',
        'title_ru': 'Спортивный массаж',
        'short_cs': 'Intenzivní masáž pro sportovce a aktivní lidi — regenerace svalů a prevence zranění.',
        'short_en': 'Intensive massage for athletes — muscle recovery and injury prevention.',
        'short_ru': 'Интенсивный массаж для спортсменов — восстановление мышц и профилактика травм.',
        'description_cs': (
            'Sportovní masáž zaměřená na regeneraci svalů, uvolnění napětí a podporu výkonu. '
            'Vhodná po tréninku i pro prevenci zranění.'
        ),
        'description_en': (
            'Sports massage focused on muscle recovery, tension release and performance support.'
        ),
        'description_ru': (
            'Спортивный массаж для восстановления мышц, снятия напряжения и поддержки формы.'
        ),
    },
    {
        'slug': 'lymfaticka-masaz',
        'order': 5,
        'duration': 75,
        'price': 1600,
        'title_cs': 'Lymfatická masáž',
        'title_en': 'Lymphatic massage',
        'title_ru': 'Лимфатический массаж',
        'short_cs': 'Jemná technika podporující lymfatický systém, detoxikaci a redukci otoků.',
        'short_en': 'Gentle technique supporting the lymphatic system, detox and reducing swelling.',
        'short_ru': 'Мягкая техника для лимфатической системы, детокса и уменьшения отёков.',
        'description_cs': (
            'Lymfatická masáž jemnými hmaty podporuje lymfatický systém, detoxikaci těla '
            'a redukci otoků. Vhodná pro regeneraci a celkovou pohodu.'
        ),
        'description_en': (
            'Lymphatic massage with gentle strokes supports detox and reduces swelling.'
        ),
        'description_ru': (
            'Лимфатический массаж мягкими движениями поддерживает детокс и уменьшает отёки.'
        ),
    },
    {
        'slug': 'aromaterapie',
        'order': 6,
        'duration': 75,
        'price': 1400,
        'title_cs': 'Aromamasáž',
        'title_en': 'Aroma massage',
        'title_ru': 'Аромамассаж',
        'short_cs': 'Aromamasáž s prémiálními éterickými oleji pro hlubokou relaxaci těla i mysli.',
        'short_en': 'Aroma massage with premium essential oils for deep body and mind relaxation.',
        'short_ru': 'Аромамассаж с премиальными эфирными маслами для глубокого расслабления.',
        'description_cs': (
            'Aromamasáž s prémiálními éterickými oleji pro harmonii těla a mysli. '
            'Vůně a dotek jako jeden celek pro hlubokou relaxaci.'
        ),
        'description_en': (
            'Aroma massage with premium essential oils for body and mind harmony.'
        ),
        'description_ru': (
            'Аромамассаж с премиальными эфирными маслами для гармонии тела и разума.'
        ),
    },
]

THERAPISTS = [
    {
        'slug': 'julia', 'name': 'Julia', 'order': 1,
        'specialties': ['klasicka-masaz', 'cbd-relaxacni-masaz', 'thajska-masaz'],
        'bio_cs': (
            'Julia je certifikovaná masérka specializující se na klasickou a relax masáž. '
            'Přizpůsobuje každé sezení potřebám klienta a navozuje hlubokou relaxaci.'
        ),
        'bio_en': (
            'Julia is a certified masseuse specializing in classic and relax massage, '
            'tailoring each session to client needs.'
        ),
        'bio_ru': (
            'Julia — сертифицированная массажистка, специализирующаяся на классическом и релакс-массаже.'
        ),
    },
    {
        'slug': 'diana', 'name': 'Diana', 'order': 2,
        'specialties': ['thajska-masaz', 'aromaterapie'],
        'bio_cs': (
            'Diana se zaměřuje na uvolňující a aromamasáže. Její přístup je klidný a citlivý, '
            'ideální pro ty, kdo hledají hluboký odpočinek.'
        ),
        'bio_en': (
            'Diana focuses on relaxing and aroma massages with a calm, sensitive approach for deep rest.'
        ),
        'bio_ru': (
            'Diana специализируется на расслабляющем и аромамассаже с мягким и внимательным подходом.'
        ),
    },
    {
        'slug': 'laura', 'name': 'Laura', 'order': 3,
        'specialties': ['aromaterapie', 'cbd-relaxacni-masaz'],
        'bio_cs': (
            'Laura kombinuje aromamasáž a relax masáž s důrazem na harmonii těla a mysli '
            'prostřednictvím éterických olejů.'
        ),
        'bio_en': (
            'Laura combines aroma and relax massage with essential oils for body and mind harmony.'
        ),
        'bio_ru': (
            'Laura сочетает арома и релакс-массаж с эфирными маслами для гармонии тела и разума.'
        ),
    },
    {
        'slug': 'vanessa', 'name': 'Vanessa', 'order': 4,
        'specialties': ['klasicka-masaz', 'sportovni-masaz'],
        'bio_cs': (
            'Vanessa má deset let praxe v klasické a sportovní masáži. '
            'Pomáhá uvolnit napětí po sportu i v každodenním životě.'
        ),
        'bio_en': (
            'Vanessa has ten years of experience in classic and sports massage.'
        ),
        'bio_ru': (
            'Vanessa имеет десять лет опыта в классическом и спортивном массаже.'
        ),
    },
    {
        'slug': 'ella', 'name': 'Ella', 'order': 5,
        'specialties': ['sportovni-masaz', 'klasicka-masaz'],
        'bio_cs': (
            'Ella se specializuje na sportovní a regenerační masáže. '
            'Její techniky podporují zotavení svalů a celkovou regeneraci.'
        ),
        'bio_en': (
            'Ella specializes in sports and recovery massage to support muscle regeneration.'
        ),
        'bio_ru': (
            'Ella специализируется на спортивном и восстановительном массаже.'
        ),
    },
    {
        'slug': 'mira', 'name': 'Mira', 'order': 6,
        'specialties': ['lymfaticka-masaz', 'aromaterapie'],
        'bio_cs': (
            'Mira nabízí lymfatickou a aromamasáž s jemným přístupem, '
            'který podporuje detoxikaci a relaxaci.'
        ),
        'bio_en': (
            'Mira offers lymphatic and aroma massage with a gentle approach supporting detox.'
        ),
        'bio_ru': (
            'Mira предлагает лимфатический и аромамассаж с мягким подходом для детокса.'
        ),
    },
]

BLOG_SLUGS = [
    'koristi-masazu-pro-zdorovi',
    'relaks-meditace-masaz',
    'spa-retreat-kompletni-pruvodce',
]

BLOG_DATES = {
    'koristi-masazu-pro-zdorovi': '2026-01-15T10:00:00+02:00',
    'relaks-meditace-masaz': '2026-01-22T10:00:00+02:00',
    'spa-retreat-kompletni-pruvodce': '2026-02-01T10:00:00+02:00',
}
