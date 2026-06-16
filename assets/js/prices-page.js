/**
 * Black Diamond Spa — Prices page tabs (duration + currency)
 */
(function () {
  'use strict';

  var root = document.querySelector('.prices-page');
  if (!root) return;

  root.setAttribute('data-currency', 'czk');

  var durationTabs = root.querySelectorAll('[data-duration-tab]');
  var durationPanels = root.querySelectorAll('[data-duration-panel]');
  var currencyBtns = root.querySelectorAll('.prices-currency');

  function activateDuration(duration) {
    durationTabs.forEach(function (tab) {
      var active = tab.getAttribute('data-duration-tab') === duration;
      tab.classList.toggle('is-active', active);
      tab.setAttribute('aria-selected', active ? 'true' : 'false');
    });
    durationPanels.forEach(function (panel) {
      var active = panel.getAttribute('data-duration-panel') === duration;
      panel.classList.toggle('is-active', active);
      if (active) {
        panel.removeAttribute('hidden');
      } else {
        panel.setAttribute('hidden', '');
      }
    });
  }

  function activateCurrency(code) {
    root.setAttribute('data-currency', code);
    currencyBtns.forEach(function (btn) {
      var active = btn.getAttribute('data-currency') === code;
      btn.classList.toggle('is-active', active);
      btn.setAttribute('aria-selected', active ? 'true' : 'false');
    });
  }

  durationTabs.forEach(function (tab) {
    tab.addEventListener('click', function () {
      activateDuration(tab.getAttribute('data-duration-tab'));
    });
  });

  currencyBtns.forEach(function (btn) {
    btn.addEventListener('click', function () {
      activateCurrency(btn.getAttribute('data-currency'));
    });
  });
})();
