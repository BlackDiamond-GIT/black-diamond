(function () {
  'use strict';

  const modal = document.getElementById('th-modal');
  if (modal) {
    const photo = document.getElementById('modal-photo');
    const name = document.getElementById('modal-name');
    const tags = document.getElementById('modal-tags');
    const bio = document.getElementById('modal-bio');
    const svcsEl = document.getElementById('modal-svcs');
    const closes = modal.querySelectorAll('[data-close-modal]');
    let lastFocus = null;
    let bodyScrollY = 0;

    function lockBody() {
      if (document.body.style.position === 'fixed') {
        bodyScrollY = Math.abs(parseInt(document.body.style.top, 10)) || window.scrollY;
      } else {
        bodyScrollY = window.scrollY;
      }
      document.body.style.position = 'fixed';
      document.body.style.top = '-' + bodyScrollY + 'px';
      document.body.style.left = '0';
      document.body.style.right = '0';
      document.body.style.width = '100%';
      document.body.style.overflow = 'hidden';
    }

    function unlockBody() {
      const scrollY = bodyScrollY;
      const root = document.documentElement;
      const prevBehavior = root.style.scrollBehavior;

      root.style.scrollBehavior = 'auto';
      document.body.style.position = '';
      document.body.style.top = '';
      document.body.style.left = '';
      document.body.style.right = '';
      document.body.style.width = '';
      document.body.style.overflow = '';

      root.scrollTop = scrollY;
      document.body.scrollTop = scrollY;
      window.scrollTo(0, scrollY);

      requestAnimationFrame(() => {
        window.scrollTo(0, scrollY);
        root.style.scrollBehavior = prevBehavior;
      });
    }

    function restoreFocus() {
      if (!lastFocus) return;
      try {
        lastFocus.focus({ preventScroll: true });
      } catch (err) {
        lastFocus.focus();
      }
    }

    function openModal(trigger) {
      lastFocus = trigger;
      const d = trigger.dataset;
      if (photo) {
        photo.src = d.photo || '';
        photo.alt = d.name || '';
      }
      if (name) name.textContent = d.name || '';
      if (bio) bio.textContent = d.bio || '';

      if (tags) {
        tags.innerHTML = '';
        (d.spec || '').split('|').filter(Boolean).forEach((s) => {
          const sp = document.createElement('span');
          sp.className = 'tag tag--specialty';
          sp.textContent = s;
          tags.appendChild(sp);
        });
      }

      if (svcsEl) {
        svcsEl.innerHTML = '';
        (d.svcs || '').split('|').filter(Boolean).forEach((s) => {
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
      const panel = modal.querySelector('.th-modal__panel');
      let finished = false;
      const onEnd = () => {
        if (finished) return;
        finished = true;
        unlockBody();
        modal.hidden = true;
        restoreFocus();
      };
      if (panel) panel.addEventListener('transitionend', onEnd, { once: true });
      setTimeout(onEnd, 500);
    }

    document.querySelectorAll('[data-modal-trigger]').forEach((btn) => {
      btn.addEventListener('click', () => openModal(btn));
    });
    closes.forEach((el) => el.addEventListener('click', closeModal));
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && modal.classList.contains('is-open')) closeModal();
    });
  }

  function bindAccordion(root, itemSel, triggerSel, panelSel) {
    if (!root) return;
    root.querySelectorAll(itemSel).forEach((item) => {
      const trigger = item.querySelector(triggerSel);
      const panel = item.querySelector(panelSel);
      if (!trigger || !panel || trigger.dataset.accordionBound) return;
      trigger.dataset.accordionBound = '1';
      trigger.addEventListener('click', () => {
        const open = trigger.getAttribute('aria-expanded') === 'true';
        root.querySelectorAll(triggerSel).forEach((t) => {
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

  document.querySelectorAll('.faq').forEach((el) => {
    bindAccordion(el, '.faq__item', '.faq__question', '.faq__answer');
  });
  document.querySelectorAll('.proc-acc').forEach((el) => {
    bindAccordion(el, '.proc-acc__item', '.proc-acc__trigger', '.proc-acc__panel');
  });

  if ('IntersectionObserver' in window) {
    const obs = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
            obs.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.1 }
    );
    document.querySelectorAll('[data-reveal]').forEach((el) => obs.observe(el));
  } else {
    document.querySelectorAll('[data-reveal]').forEach((el) => el.classList.add('is-visible'));
  }
})();
