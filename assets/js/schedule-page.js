/**
 * Black Diamond Spa — Schedule page (tabs + live clock)
 */
(function () {
  'use strict';

  var tablist = document.querySelector('.masseuse-tabs');
  if (!tablist) return;

  var tabs = tablist.querySelectorAll('.masseuse-tabs__btn[role="tab"]');
  var panels = document.querySelectorAll('.masseuse-panel[role="tabpanel"]');

  function activateTab(tab) {
    var targetId = tab.getAttribute('aria-controls');
    if (!targetId) return;

    tabs.forEach(function (btn) {
      var isActive = btn === tab;
      btn.classList.toggle('is-active', isActive);
      btn.setAttribute('aria-selected', isActive ? 'true' : 'false');
    });

    panels.forEach(function (panel) {
      var isActive = panel.id === targetId;
      panel.classList.toggle('is-active', isActive);
      if (isActive) {
        panel.removeAttribute('hidden');
      } else {
        panel.setAttribute('hidden', '');
      }
    });
  }

  tablist.addEventListener('click', function (event) {
    var tab = event.target.closest('.masseuse-tabs__btn[role="tab"]');
    if (!tab || !tablist.contains(tab)) return;
    activateTab(tab);
  });

  tablist.addEventListener('keydown', function (event) {
    var current = document.activeElement;
    if (!current || !current.classList.contains('masseuse-tabs__btn')) return;

    var index = Array.prototype.indexOf.call(tabs, current);
    if (index < 0) return;

    var nextIndex = index;
    if (event.key === 'ArrowRight') {
      nextIndex = (index + 1) % tabs.length;
    } else if (event.key === 'ArrowLeft') {
      nextIndex = (index - 1 + tabs.length) % tabs.length;
    } else if (event.key === 'Home') {
      nextIndex = 0;
    } else if (event.key === 'End') {
      nextIndex = tabs.length - 1;
    } else {
      return;
    }

    event.preventDefault();
    tabs[nextIndex].focus();
    activateTab(tabs[nextIndex]);
  });

  var clockEl = document.querySelector('[data-schedule-clock]');
  if (!clockEl) return;

  function updateClock() {
    var now = new Date();
    clockEl.textContent = now.toLocaleTimeString([], {
      hour: '2-digit',
      minute: '2-digit',
    });
  }

  updateClock();
  setInterval(updateClock, 60000);
})();
