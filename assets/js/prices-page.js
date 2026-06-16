/**
 * Black Diamond Spa — Prices page currency toggle
 */
(function () {
  'use strict';

  var root = document.querySelector('.prices-page');
  if (!root) return;

  root.setAttribute('data-currency', 'czk');

  root.querySelectorAll('.prices-currency').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var code = btn.getAttribute('data-currency');
      root.setAttribute('data-currency', code);
      root.querySelectorAll('.prices-currency').forEach(function (item) {
        var active = item.getAttribute('data-currency') === code;
        item.classList.toggle('is-active', active);
        item.setAttribute('aria-selected', active ? 'true' : 'false');
      });
    });
  });
})();
