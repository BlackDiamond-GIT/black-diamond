(function () {
  'use strict';

  function bindAccordion(root, itemSel, triggerSel, panelSel) {
    if (!root) return;
    root.querySelectorAll(itemSel).forEach((item) => {
      const trigger = item.querySelector(triggerSel);
      const panel = item.querySelector(panelSel);
      if (!trigger || !panel) return;
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
})();
