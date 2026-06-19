/**
 * reviews-carousel.js — horizontal guest reviews on the home page
 */
(function () {
  'use strict';

  const DESKTOP_MQ = '(min-width: 769px)';

  function readGapPx(track) {
    const styles = getComputedStyle(track);
    const raw = styles.columnGap || styles.gap || '0';
    const parsed = parseFloat(raw);
    return Number.isFinite(parsed) ? parsed : 0;
  }

  function getSlides(track) {
    return Array.from(track.querySelectorAll('.reviews-carousel__slide'));
  }

  function visibleColumns() {
    return window.matchMedia(DESKTOP_MQ).matches ? 3 : 1;
  }

  function syncSlideWidths(viewport, track) {
    const cols = visibleColumns();
    const gap = readGapPx(track);
    const inner = viewport.clientWidth;
    const slideW = cols > 1 ? (inner - gap * (cols - 1)) / cols : inner;
    const px = `${Math.max(0, Math.floor(slideW * 100) / 100)}px`;
    track.style.setProperty('--reviews-slide-w', px);
    return parseFloat(px);
  }

  function slideScrollLeft(slide, track) {
    return slide.offsetLeft - track.offsetLeft;
  }

  function currentSlideIndex(viewport, track, slides) {
    const scrollLeft = viewport.scrollLeft;
    let index = 0;
    for (let i = 0; i < slides.length; i += 1) {
      if (slideScrollLeft(slides[i], track) <= scrollLeft + 6) {
        index = i;
      }
    }
    return index;
  }

  function lastScrollIndex(slides, visible) {
    return Math.max(0, slides.length - visible);
  }

  function isScrollable(viewport, track) {
    return track.scrollWidth > viewport.clientWidth + 2;
  }

  function updateButtons(viewport, track, prev, next) {
    if (!prev || !next) {
      return;
    }

    const slides = getSlides(track);
    if (!slides.length) {
      prev.disabled = true;
      next.disabled = true;
      return;
    }

    const visible = visibleColumns();
    const index = currentSlideIndex(viewport, track, slides);
    const maxIndex = lastScrollIndex(slides, visible);
    const atStart = index <= 0;
    const atEnd = index >= maxIndex;

    prev.disabled = atStart;
    prev.setAttribute('aria-disabled', atStart ? 'true' : 'false');
    next.disabled = atEnd;
    next.setAttribute('aria-disabled', atEnd ? 'true' : 'false');
  }

  function initCarousel(root) {
    if (root.dataset.reviewsReady === '1') {
      return;
    }

    const viewport = root.querySelector('[data-reviews-viewport]');
    const track = root.querySelector('.reviews-carousel__track');
    const prev = root.querySelector('[data-reviews-prev]');
    const next = root.querySelector('[data-reviews-next]');

    if (!viewport || !track) {
      return;
    }

    root.dataset.reviewsReady = '1';

    function refresh() {
      syncSlideWidths(viewport, track);
      const scrollable = isScrollable(viewport, track);
      root.classList.toggle('is-static', !scrollable);

      if (!scrollable) {
        if (prev) {
          prev.disabled = true;
          prev.setAttribute('aria-disabled', 'true');
        }
        if (next) {
          next.disabled = true;
          next.setAttribute('aria-disabled', 'true');
        }
        return;
      }

      updateButtons(viewport, track, prev, next);
    }

    function scrollBySlide(direction) {
      const slides = getSlides(track);
      if (!slides.length || !isScrollable(viewport, track)) {
        return;
      }

      const index = currentSlideIndex(viewport, track, slides);
      const maxIndex = lastScrollIndex(slides, visibleColumns());
      const targetIndex = Math.min(Math.max(index + direction, 0), maxIndex);
      const targetLeft = slideScrollLeft(slides[targetIndex], track);

      viewport.scrollTo({ left: targetLeft, behavior: 'smooth' });
    }

    prev?.addEventListener('click', () => {
      if (prev.disabled) {
        return;
      }
      scrollBySlide(-1);
    });

    next?.addEventListener('click', () => {
      if (next.disabled) {
        return;
      }
      scrollBySlide(1);
    });

    viewport.addEventListener(
      'scroll',
      () => {
        window.requestAnimationFrame(() => updateButtons(viewport, track, prev, next));
      },
      { passive: true }
    );

    let resizeTimer;
    window.addEventListener('resize', () => {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(refresh, 120);
    });

    if (window.visualViewport) {
      window.visualViewport.addEventListener('resize', () => {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(refresh, 120);
      });
    }

    if (document.fonts?.ready) {
      document.fonts.ready.then(refresh).catch(refresh);
    }

    window.requestAnimationFrame(() => {
      window.requestAnimationFrame(refresh);
    });
  }

  function initReviewsCarousel() {
    document.querySelectorAll('[data-reviews-carousel]').forEach(initCarousel);
  }

  window.initReviewsCarousel = initReviewsCarousel;

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initReviewsCarousel);
  } else {
    initReviewsCarousel();
  }
})();
