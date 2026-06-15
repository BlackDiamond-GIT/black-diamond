/**
 * Black Diamond Spa — Schedule (дані з black-elixir schedule_data)
 */

(function () {
  'use strict';

  const TIMES = ['09:00', '11:00', '18:30', '20:30', '02:00', '04:00', '06:00'];
  const DAYS_CS = ['Po', 'Út', 'St', 'Čt', 'Pá', 'So', 'Ne'];
  const DAYS_EN = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
  const DAYS_RU = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'];

  const OPENING_HOURS = {
    cs: { weekdays: 'Po – Pá', weekend: 'So – Ne', weekdays_hours: '10:00 – 21:00', weekend_hours: '10:00 – 19:00' },
    en: { weekdays: 'Mon – Fri', weekend: 'Sat – Sun', weekdays_hours: '10:00 – 21:00', weekend_hours: '10:00 – 19:00' },
    ru: { weekdays: 'Пн – Пт', weekend: 'Сб – Вс', weekdays_hours: '10:00 – 21:00', weekend_hours: '10:00 – 19:00' },
  };

  const THERAPISTS = [
    { id: 1, slug: 'julia',   name: 'Julia',   services: { cs: ['Klasická masáž', 'Relax masáž', 'Uvolňující masáž'], en: ['Classic massage', 'Relax massage', 'Relaxing massage'], ru: ['Классический массаж', 'Релакс массаж', 'Расслабляющий массаж'] } },
    { id: 2, slug: 'diana',   name: 'Diana',   services: { cs: ['Uvolňující masáž', 'Aromamasáž'], en: ['Relaxing massage', 'Aroma massage'], ru: ['Расслабляющий массаж', 'Аромамассаж'] } },
    { id: 3, slug: 'laura',   name: 'Laura',   services: { cs: ['Aromamasáž', 'Relax masáž'], en: ['Aroma massage', 'Relax massage'], ru: ['Аромамассаж', 'Релакс массаж'] } },
    { id: 4, slug: 'vanessa', name: 'Vanessa', services: { cs: ['Klasická masáž', 'Sportovní masáž'], en: ['Classic massage', 'Sports massage'], ru: ['Классический массаж', 'Спортивный массаж'] } },
    { id: 5, slug: 'ella',    name: 'Ella',    services: { cs: ['Sportovní masáž', 'Klasická masáž'], en: ['Sports massage', 'Classic massage'], ru: ['Спортивный массаж', 'Классический массаж'] } },
    { id: 6, slug: 'mira',    name: 'Mira',    services: { cs: ['Lymfatická masáž', 'Aromamasáž'], en: ['Lymphatic massage', 'Aroma massage'], ru: ['Лимфатический массаж', 'Аромамассаж'] } },
  ];

  function srand(seed) {
    const x = Math.sin(seed + 1) * 10000;
    return x - Math.floor(x);
  }

  function buildScheduleGrid() {
    const grid = {};
    for (let day = 0; day < 7; day++) {
      grid[day] = {};
      TIMES.forEach((t) => { grid[day][t] = []; });
    }

    let seed = 77;
    let slotId = 1;

    THERAPISTS.forEach((th) => {
      for (let day = 0; day < 7; day++) {
        TIMES.forEach((time) => {
          seed += 1;
          if (srand(seed) <= 0.42) return;

          seed += 1;
          const lang = document.documentElement.lang || 'cs';
          const services = th.services[lang] || th.services.cs;
          const svc = services[Math.floor(srand(seed + 500) * services.length) % services.length];
          seed += 1;
          const isBooked = srand(seed + 1000) > 0.52;

          grid[day][time].push({
            id: slotId++,
            therapist: th,
            service: svc,
            isBooked,
          });
        });
      }
    });

    return grid;
  }

  const SCHEDULE_GRID = buildScheduleGrid();

  const scheduleEl = document.querySelector('[data-schedule]');
  if (!scheduleEl) return;

  const lang = document.documentElement.lang || 'cs';
  const langPrefix = '/' + lang + '/';
  const slotsTarget = scheduleEl.querySelector('[data-schedule-slots]');
  if (!slotsTarget) return;

  const hours = OPENING_HOURS[lang] || OPENING_HOURS.cs;
  const hoursBar = document.querySelector('.schedule__hours-bar');
  if (hoursBar) {
    hoursBar.innerHTML = `
      ${hours.weekdays}: <span>${hours.weekdays_hours}</span>
      &nbsp;|&nbsp;
      ${hours.weekend}: <span>${hours.weekend_hours}</span>
      &nbsp;|&nbsp;
      <a href="tel:+420797669633" style="color:var(--tiffany)">+420 797 669 633</a>
    `;
  }

  let activeDay = new Date().getDay();
  activeDay = activeDay === 0 ? 6 : activeDay - 1;
  let activeTherapist = null;

  const bookLabel = { cs: 'Rezervovat', en: 'Book', ru: 'Забронировать' };
  const bookedLabel = { cs: 'Obsazeno', en: 'Booked', ru: 'Занято' };

  function renderSlots() {
    const therapists = activeTherapist
      ? THERAPISTS.filter((t) => t.slug === activeTherapist)
      : THERAPISTS;

    const slots = [];
    TIMES.forEach((time) => {
      const cellSlots = SCHEDULE_GRID[activeDay][time] || [];
      cellSlots.forEach((slot) => {
        if (activeTherapist && slot.therapist.slug !== activeTherapist) return;
        slots.push({ time, ...slot });
      });
    });

    slots.sort((a, b) => {
      if (a.isBooked !== b.isBooked) return a.isBooked ? 1 : -1;
      return a.time.localeCompare(b.time);
    });

    if (!slots.length) {
      slotsTarget.innerHTML = `
        <div style="grid-column:1/-1;text-align:center;padding:var(--sp-3xl);color:var(--text-muted)">
          ${lang === 'ru' ? 'Нет доступных слотов' : lang === 'en' ? 'No available slots' : 'Žádné dostupné termíny'}
        </div>`;
      return;
    }

    slotsTarget.innerHTML = slots.map((s) => {
      const status = s.isBooked ? 'busy' : 'free';
      return `
      <article class="schedule__slot schedule__slot--${status}" aria-label="${s.time} — ${s.therapist.name}">
        <div class="schedule__slot-time">${s.time}</div>
        <div class="schedule__slot-therapist">${s.therapist.name}</div>
        <div class="schedule__slot-service">${s.service}</div>
        <div class="schedule__slot-status schedule__slot-status--${status}">
          <span class="schedule__slot-status-dot" aria-hidden="true"></span>
          ${s.isBooked ? (bookedLabel[lang] || bookedLabel.cs) : (lang === 'ru' ? 'Свободно' : lang === 'en' ? 'Available' : 'Volno')}
        </div>
        ${!s.isBooked ? `<a href="${langPrefix}kontakty/" class="btn btn--sm btn--primary schedule__slot-cta" style="margin-top:var(--sp-sm)">${bookLabel[lang] || bookLabel.cs}</a>` : ''}
      </article>`;
    }).join('');

    const days = { cs: DAYS_CS, en: DAYS_EN, ru: DAYS_RU };
    const dayKey = (days[lang] || days.cs)[activeDay].toLowerCase();
    const params = new URLSearchParams();
    params.set('den', dayKey);
    if (activeTherapist) params.set('maserka', activeTherapist);
    history.replaceState(null, '', window.location.pathname + '?' + params.toString());
  }

  function renderDayStrip() {
    const strip = scheduleEl.querySelector('[data-schedule-days]');
    if (!strip) return;
    const dayLabels = { cs: DAYS_CS, en: DAYS_EN, ru: DAYS_RU }[lang] || DAYS_CS;
    const today = new Date();

    strip.innerHTML = dayLabels.map((day, i) => {
      const d = new Date(today);
      d.setDate(today.getDate() - today.getDay() + 1 + i);
      const dateStr = d.getDate() + '.' + (d.getMonth() + 1) + '.';
      return `
        <button class="schedule__day-btn${i === activeDay ? ' is-active' : ''}"
          aria-pressed="${i === activeDay}"
          data-day="${i}">
          <span class="schedule__day-name">${day}</span>
          <span class="schedule__day-date">${dateStr}</span>
        </button>`;
    }).join('');

    strip.querySelectorAll('.schedule__day-btn').forEach((btn) => {
      btn.addEventListener('click', () => {
        activeDay = parseInt(btn.dataset.day, 10);
        strip.querySelectorAll('.schedule__day-btn').forEach((b) => {
          const on = b.dataset.day === String(activeDay);
          b.classList.toggle('is-active', on);
          b.setAttribute('aria-pressed', on);
        });
        renderSlots();
      });
    });
  }

  function renderTherapistFilter() {
    const filterEl = scheduleEl.querySelector('[data-schedule-therapists]');
    if (!filterEl) return;
    const allLabel = { cs: 'Všechny', en: 'All', ru: 'Все' };

    filterEl.innerHTML = [
      `<button class="schedule__therapist-chip${activeTherapist === null ? ' is-active' : ''}" data-therapist="">
        <span class="schedule__therapist-avatar">✦</span>
        ${allLabel[lang] || allLabel.cs}
      </button>`,
      ...THERAPISTS.map((t) => `
        <button class="schedule__therapist-chip${activeTherapist === t.slug ? ' is-active' : ''}"
          data-therapist="${t.slug}">
          <span class="schedule__therapist-avatar">${t.name[0]}</span>
          ${t.name}
        </button>`),
    ].join('');

    filterEl.querySelectorAll('.schedule__therapist-chip').forEach((chip) => {
      chip.addEventListener('click', () => {
        activeTherapist = chip.dataset.therapist || null;
        filterEl.querySelectorAll('.schedule__therapist-chip').forEach((c) => {
          c.classList.toggle('is-active', c.dataset.therapist === chip.dataset.therapist);
        });
        renderSlots();
      });
    });
  }

  renderDayStrip();
  renderTherapistFilter();
  renderSlots();
})();
