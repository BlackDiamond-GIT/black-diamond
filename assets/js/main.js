/**
 * Black Diamond Spa — Main JS
 * nav scroll, mobile drawer, FAQ accordion, ink reveal, modal, parallax
 */

(function () {
  'use strict';

  // Fix malformed internal links (//masaze/... or masaze/... without lang prefix).
  const SITE_SECTIONS = /^(masaze|masazistky|rozvrh|blog|kontakty|o-nas|pravidla-salonu|soukromi)(\/|$)/;
  const pageLang = (document.documentElement.lang || 'cs').split('-')[0];

  function normalizeInternalHref(href) {
    if (!href || /^(https?:|mailto:|tel:|#|\/static\/|\/media\/|\/admin\/|\/api\/)/.test(href)) {
      return href;
    }
    if (href.startsWith('//') && SITE_SECTIONS.test(href.slice(2))) {
      return `/${pageLang}/${href.slice(2)}`.replace(/\/{2,}/g, '/');
    }
    if (!href.startsWith('/') && SITE_SECTIONS.test(href)) {
      return `/${pageLang}/${href}`.replace(/\/{2,}/g, '/');
    }
    return href;
  }

  document.querySelectorAll('a[href]').forEach((link) => {
    const fixed = normalizeInternalHref(link.getAttribute('href'));
    if (fixed && fixed !== link.getAttribute('href')) {
      link.setAttribute('href', fixed);
    }
  });

  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent) ||
    (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);

  // ── Nav scroll state ───────────────────────────
  const nav = document.querySelector('.nav');
  if (nav) {
    const onScroll = () => {
      if (window.scrollY > 20) {
        nav.classList.add('nav--scrolled');
      } else {
        nav.classList.remove('nav--scrolled');
      }
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  // ── Body lock (shared) ─────────────────────────
  let bodyLocked = false;
  let savedScrollY = 0;

  function lockBody() {
    if (bodyLocked) return;
    savedScrollY = window.scrollY;
    document.body.style.position = 'fixed';
    document.body.style.top = `-${savedScrollY}px`;
    document.body.style.width = '100%';
    bodyLocked = true;
  }

  function unlockBody() {
    if (!bodyLocked) return;
    document.body.style.position = '';
    document.body.style.top = '';
    document.body.style.width = '';
    window.scrollTo(0, savedScrollY);
    bodyLocked = false;
  }

  // ── Mobile drawer ──────────────────────────────
  const burger  = document.querySelector('.nav__burger');
  const drawer  = document.querySelector('.nav__drawer');
  const overlay = document.querySelector('.nav__overlay');

  function openDrawer() {
    if (!drawer) return;
    burger.setAttribute('aria-expanded', 'true');
    drawer.classList.add('is-open');
    if (overlay) overlay.classList.add('is-visible');
    lockBody();
  }

  function closeDrawer() {
    if (!drawer) return;
    if (burger) burger.setAttribute('aria-expanded', 'false');
    drawer.classList.remove('is-open');
    if (overlay) overlay.classList.remove('is-visible');
    unlockBody();
  }

  if (burger && drawer) {
    burger.addEventListener('click', () => {
      const isOpen = drawer.classList.contains('is-open');
      isOpen ? closeDrawer() : openDrawer();
    });

    if (overlay) overlay.addEventListener('click', closeDrawer);

    const drawerClose = drawer.querySelector('.nav__drawer-close');
    if (drawerClose) drawerClose.addEventListener('click', closeDrawer);

    drawer.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', closeDrawer);
    });
  }

  // ── FAQ Accordion ──────────────────────────────
  const faqItems = document.querySelectorAll('.faq__item');

  faqItems.forEach(item => {
    const question = item.querySelector('.faq__question');
    const answer   = item.querySelector('.faq__answer');
    if (!question || !answer) return;

    question.addEventListener('click', () => {
      const isExpanded = question.getAttribute('aria-expanded') === 'true';

      faqItems.forEach(other => {
        if (other === item) return;
        const otherQ = other.querySelector('.faq__question');
        const otherA = other.querySelector('.faq__answer');
        if (otherQ) otherQ.setAttribute('aria-expanded', 'false');
        if (otherA) otherA.classList.remove('is-open');
      });

      question.setAttribute('aria-expanded', String(!isExpanded));
      answer.classList.toggle('is-open', !isExpanded);
    });
  });

  // ── Ink reveal + line draw ─────────────────────
  function revealInkElement(el) {
    el.classList.add('is-visible');
  }

  function isInViewport(el) {
    const rect = el.getBoundingClientRect();
    return rect.bottom > 0 && rect.top < window.innerHeight;
  }

  if ('IntersectionObserver' in window && !prefersReducedMotion) {
    const inkObserver = new IntersectionObserver(
      entries => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            revealInkElement(entry.target);
            inkObserver.unobserve(entry.target);
          }
        });
      },
      { threshold: 0, rootMargin: '0px 0px -5% 0px' }
    );

    document.querySelectorAll('[data-ink]').forEach((el, i) => {
      el.style.transitionDelay = `${(i % 5) * 60}ms`;
      if (isInViewport(el)) {
        revealInkElement(el);
      } else {
        inkObserver.observe(el);
      }
    });

    document.querySelectorAll('[data-line]').forEach(title => {
      const line = title.parentElement.querySelector('.section-line');
      if (!line) return;
      const lineObserver = new IntersectionObserver(
        entries => {
          entries.forEach(entry => {
            if (entry.isIntersecting) {
              line.classList.add('is-visible');
              lineObserver.unobserve(entry.target);
            }
          });
        },
        { threshold: 0.2 }
      );
      lineObserver.observe(title);
    });
  } else {
    document.querySelectorAll('[data-ink]').forEach(el => el.classList.add('is-visible'));
    document.querySelectorAll('.section-line').forEach(el => el.classList.add('is-visible'));
  }

  // ── Hero parallax (non-iOS) ────────────────────
  const parallaxImg = document.querySelector('[data-parallax]');
  if (parallaxImg && !prefersReducedMotion && !isIOS) {
    const hero = document.querySelector('.hero');
    if (hero) {
      const onParallax = () => {
        const rect = hero.getBoundingClientRect();
        if (rect.bottom < 0 || rect.top > window.innerHeight) return;
        const offset = rect.top * 0.3;
        parallaxImg.style.transform = `translate3d(0, ${offset}px, 0) scale(1.05)`;
      };
      window.addEventListener('scroll', onParallax, { passive: true });
      onParallax();
    }
  }

  // ── Therapist modal ────────────────────────────
  const modal = document.getElementById('therapist-modal');
  if (modal) {
    const panel      = modal.querySelector('.therapist-modal__panel');
    const photoEl    = modal.querySelector('.therapist-modal__photo');
    const nameEl     = modal.querySelector('.therapist-modal__name');
    const tagsEl     = modal.querySelector('.therapist-modal__tags');
    const bioEl      = modal.querySelector('.therapist-modal__bio');
    const servicesEl = modal.querySelector('.therapist-modal__services');
    const ctaEl      = modal.querySelector('.therapist-modal__cta');
    const closeEls   = modal.querySelectorAll('[data-therapist-close]');
    let lastFocus = null;

    function openModal(trigger) {
      const name     = trigger.dataset.therapistName || '';
      const slug       = trigger.dataset.therapistSlug || '';
      const photo      = trigger.dataset.therapistPhoto || '';
      const bio        = trigger.dataset.therapistBio || '';
      const services   = trigger.dataset.therapistServices || '';

      lastFocus = trigger;

      if (photoEl) {
        if (photo) {
          photoEl.src = photo;
          photoEl.alt = `${name} — Black Diamond Spa`;
          photoEl.hidden = false;
        } else {
          photoEl.removeAttribute('src');
          photoEl.alt = '';
          photoEl.hidden = true;
        }
      }

      if (nameEl) nameEl.textContent = name;
      if (bioEl) bioEl.textContent = bio;

      if (tagsEl) {
        tagsEl.innerHTML = '';
        const serviceList = services.split('|').filter(Boolean);
        serviceList.forEach(spec => {
          const tag = document.createElement('span');
          tag.className = 'tag tag--specialty';
          tag.textContent = spec;
          tagsEl.appendChild(tag);
        });
      }

      if (servicesEl) {
        servicesEl.innerHTML = '';
        const serviceList = services.split('|').filter(Boolean);
        serviceList.forEach(spec => {
          const li = document.createElement('li');
          const tag = document.createElement('span');
          tag.className = 'tag tag--duration';
          tag.textContent = spec;
          li.appendChild(tag);
          servicesEl.appendChild(li);
        });
      }

      if (ctaEl) {
        const lang = document.documentElement.lang || 'cs';
        ctaEl.href = `/${lang}/rozvrh/`;
        const reserveLabel = trigger.dataset.therapistCta || '';
        ctaEl.textContent = reserveLabel || ctaEl.dataset.defaultLabel || 'Rezervovat';
      }

      modal.hidden = false;
      modal.setAttribute('aria-hidden', 'false');
      requestAnimationFrame(() => modal.classList.add('is-open'));
      lockBody();

      const closeBtn = modal.querySelector('.therapist-modal__close');
      if (closeBtn) closeBtn.focus();
    }

    function closeModal() {
      modal.classList.remove('is-open');
      modal.setAttribute('aria-hidden', 'true');
      unlockBody();

      const onEnd = () => {
        modal.hidden = true;
        panel.removeEventListener('transitionend', onEnd);
        if (lastFocus) lastFocus.focus();
      };

      if (prefersReducedMotion) {
        onEnd();
      } else {
        panel.addEventListener('transitionend', onEnd, { once: true });
        setTimeout(onEnd, 500);
      }
    }

    document.querySelectorAll('[data-therapist-trigger]').forEach(trigger => {
      trigger.addEventListener('click', () => openModal(trigger));
    });

    closeEls.forEach(el => el.addEventListener('click', closeModal));

    document.addEventListener('keydown', e => {
      if (e.key === 'Escape' && modal.classList.contains('is-open')) {
        if (drawer && drawer.classList.contains('is-open')) {
          closeDrawer();
        } else {
          closeModal();
        }
      }
    });
  }

})();
