/**
 * Black Diamond Spa — Diamond Schedule
 * Day strip + therapist filter + HTMX slot loading
 */

(function () {
  'use strict';

  const TIMES = ['10:00', '11:30', '13:00', '14:30', '16:00', '17:30', '19:00'];
  const DAYS_CS = ['Po', 'Út', 'St', 'Čt', 'Pá', 'So', 'Ne'];
  const DAYS_EN = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
  const DAYS_RU = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'];

  const THERAPISTS = [
    { slug: 'julia',   name: 'Julia',   spec: 'Klasická & Relax' },
    { slug: 'diana',   name: 'Diana',   spec: 'Uvolňující & Aroma' },
    { slug: 'laura',   name: 'Laura',   spec: 'Aromamasáž & Relax' },
    { slug: 'vanessa', name: 'Vanessa', spec: 'Klasická & Sportovní' },
    { slug: 'ella',    name: 'Ella',    spec: 'Sportovní & Regen.' },
    { slug: 'mira',    name: 'Mira',    spec: 'Lymfatická & Aroma' },
  ];

  // deterministic slot generator: free / busy / soon
  function getSlotStatus(dayIdx, timeIdx, therapistIdx) {
    const seed = (dayIdx * 7 + timeIdx + therapistIdx * 3) % 10;
    if (seed < 5) return 'free';
    if (seed < 8) return 'busy';
    return 'soon';
  }

  function getStatusLabel(status, lang) {
    const labels = {
      cs: { free: 'Volno', busy: 'Obsazeno', soon: 'Brzy volno' },
      en: { free: 'Available', busy: 'Booked', soon: 'Almost free' },
      ru: { free: 'Свободно', busy: 'Занято',  soon: 'Скоро свободно' },
    };
    return (labels[lang] || labels.cs)[status];
  }

  const scheduleEl = document.querySelector('[data-schedule]');
  if (!scheduleEl) return;

  const lang = document.documentElement.lang || 'cs';
  const slotsTarget = scheduleEl.querySelector('[data-schedule-slots]');
  if (!slotsTarget) return;

  let activeDay = new Date().getDay(); // 0=Sun → normalize to Mon=0
  activeDay = activeDay === 0 ? 6 : activeDay - 1;
  let activeTherapist = null; // null = all

  function renderSlots() {
    const therapists = activeTherapist
      ? THERAPISTS.filter(t => t.slug === activeTherapist)
      : THERAPISTS;

    const slots = [];
    TIMES.forEach((time, tIdx) => {
      therapists.forEach((th, thIdx) => {
        const status = getSlotStatus(activeDay, tIdx, THERAPISTS.indexOf(th));
        slots.push({ time, therapist: th, status, tIdx, thIdx });
      });
    });

    // Sort: free first, soon, busy
    const order = { free: 0, soon: 1, busy: 2 };
    slots.sort((a, b) => {
      if (order[a.status] !== order[b.status]) return order[a.status] - order[b.status];
      return a.time.localeCompare(b.time);
    });

    const serviceNames = {
      julia:   'Klasická masáž',
      diana:   'Aromamasáž',
      laura:   'Relax masáž',
      vanessa: 'Sportovní masáž',
      ella:    'Uvolňující masáž',
      mira:    'Lymfatická masáž',
    };

    const bookLabel = { cs: 'Rezervovat', en: 'Book', ru: 'Забронировать' };

    slotsTarget.innerHTML = slots.map(s => `
      <article class="schedule__slot schedule__slot--${s.status}" aria-label="${s.time} — ${s.therapist.name}">
        <div class="schedule__slot-time">${s.time}</div>
        <div class="schedule__slot-therapist">${s.therapist.name}</div>
        <div class="schedule__slot-service">${serviceNames[s.therapist.slug] || ''}</div>
        <div class="schedule__slot-status schedule__slot-status--${s.status}">
          <span class="schedule__slot-status-dot" aria-hidden="true"></span>
          ${getStatusLabel(s.status, lang)}
        </div>
        ${s.status !== 'busy' ? `<a href="/cs/kontakty/" class="btn btn--sm btn--${s.status === 'free' ? 'primary' : 'secondary'} schedule__slot-cta" style="margin-top:var(--sp-sm)">${bookLabel[lang] || bookLabel.cs}</a>` : ''}
      </article>
    `).join('');

    // Update URL for SEO-friendliness (no page reload)
    const days = { cs: DAYS_CS, en: DAYS_EN, ru: DAYS_RU };
    const dayKey = (days[lang] || days.cs)[activeDay].toLowerCase();
    const thKey  = activeTherapist || '';
    const params = new URLSearchParams();
    params.set('den', dayKey);
    if (thKey) params.set('maserka', thKey);
    const canonical = window.location.pathname;
    history.replaceState(null, '', canonical + '?' + params.toString());
  }

  function renderDayStrip() {
    const strip = scheduleEl.querySelector('[data-schedule-days]');
    if (!strip) return;
    const days = { cs: DAYS_CS, en: DAYS_EN, ru: DAYS_RU };
    const dayLabels = days[lang] || days.cs;

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
        </button>
      `;
    }).join('');

    strip.querySelectorAll('.schedule__day-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        activeDay = parseInt(btn.dataset.day);
        strip.querySelectorAll('.schedule__day-btn').forEach(b => {
          b.classList.toggle('is-active', b.dataset.day === String(activeDay));
          b.setAttribute('aria-pressed', b.dataset.day === String(activeDay));
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
      ...THERAPISTS.map(t => `
        <button class="schedule__therapist-chip${activeTherapist === t.slug ? ' is-active' : ''}"
          data-therapist="${t.slug}">
          <span class="schedule__therapist-avatar">${t.name[0]}</span>
          ${t.name}
        </button>
      `),
    ].join('');

    filterEl.querySelectorAll('.schedule__therapist-chip').forEach(chip => {
      chip.addEventListener('click', () => {
        activeTherapist = chip.dataset.therapist || null;
        filterEl.querySelectorAll('.schedule__therapist-chip').forEach(c => {
          c.classList.toggle('is-active', c.dataset.therapist === (chip.dataset.therapist));
        });
        renderSlots();
      });
    });
  }

  // Initial render
  renderDayStrip();
  renderTherapistFilter();
  renderSlots();

})();
