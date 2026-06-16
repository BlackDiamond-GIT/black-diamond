/**
 * Gallery carousel + lightbox for therapist detail pages.
 */
(function () {
  'use strict';

  let lightboxEl = null;
  let bodyScrollY = 0;

  function lockBody() {
    bodyScrollY = window.scrollY;
    document.body.style.position = 'fixed';
    document.body.style.top = '-' + bodyScrollY + 'px';
    document.body.style.width = '100%';
  }

  function unlockBody() {
    document.body.style.position = '';
    document.body.style.top = '';
    document.body.style.width = '';
    window.scrollTo(0, bodyScrollY);
  }

  function closeLightbox() {
    if (!lightboxEl) return;
    lightboxEl.hidden = true;
    unlockBody();
  }

  function openLightbox(src, alt) {
    if (!lightboxEl) {
      lightboxEl = document.createElement('div');
      lightboxEl.className = 'lightbox';
      lightboxEl.setAttribute('role', 'dialog');
      lightboxEl.setAttribute('aria-modal', 'true');
      lightboxEl.setAttribute('aria-label', 'Image viewer');

      const img = document.createElement('img');
      img.className = 'lightbox__img';

      const closeBtn = document.createElement('button');
      closeBtn.type = 'button';
      closeBtn.className = 'lightbox__close';
      closeBtn.setAttribute('aria-label', 'Close');
      closeBtn.textContent = '×';
      closeBtn.addEventListener('click', closeLightbox);

      lightboxEl.addEventListener('click', (e) => {
        if (e.target === lightboxEl) closeLightbox();
      });

      lightboxEl.appendChild(img);
      lightboxEl.appendChild(closeBtn);
      document.body.appendChild(lightboxEl);

      document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && !lightboxEl.hidden) closeLightbox();
      });
    }

    const img = lightboxEl.querySelector('.lightbox__img');
    img.src = src;
    img.alt = alt || '';
    lightboxEl.hidden = false;
    lockBody();
    lightboxEl.querySelector('.lightbox__close').focus();
  }

  function initGallery(gallery) {
    const slides = gallery.querySelectorAll('.gallery-carousel__slide');
    if (!slides.length) return;

    let track = gallery.querySelector('.gallery-carousel__track');
    if (!track) {
      track = document.createElement('div');
      track.className = 'gallery-carousel__track';
      slides.forEach((slide) => track.appendChild(slide));
      gallery.insertBefore(track, gallery.firstChild);
    }

    let current = 0;

    function goTo(idx) {
      if (slides.length < 2) return;
      current = ((idx % slides.length) + slides.length) % slides.length;
      track.style.transform = 'translateX(-' + (current * gallery.offsetWidth) + 'px)';
      updateDots();
    }

    gallery.querySelector('[data-gallery-prev]')?.addEventListener('click', () => goTo(current - 1));
    gallery.querySelector('[data-gallery-next]')?.addEventListener('click', () => goTo(current + 1));

    let dotsWrap = gallery.querySelector('.gallery-carousel__dots');
    if (slides.length > 1 && !dotsWrap) {
      dotsWrap = document.createElement('div');
      dotsWrap.className = 'gallery-carousel__dots';
      slides.forEach((_, i) => {
        const dot = document.createElement('button');
        dot.type = 'button';
        dot.className = 'gallery-carousel__dot' + (i === 0 ? ' gallery-carousel__dot--active' : '');
        dot.setAttribute('aria-label', 'Slide ' + (i + 1));
        dot.addEventListener('click', () => goTo(i));
        dotsWrap.appendChild(dot);
      });
      gallery.appendChild(dotsWrap);
    }

    function updateDots() {
      if (!dotsWrap) return;
      dotsWrap.querySelectorAll('.gallery-carousel__dot').forEach((dot, i) => {
        dot.classList.toggle('gallery-carousel__dot--active', i === current);
      });
    }

    if (slides.length > 1) {
      let startX = 0;
      gallery.addEventListener('touchstart', (e) => {
        startX = e.touches[0].clientX;
      }, { passive: true });

      gallery.addEventListener('touchend', (e) => {
        const dx = e.changedTouches[0].clientX - startX;
        if (Math.abs(dx) > 40) goTo(current + (dx < 0 ? 1 : -1));
      }, { passive: true });

      window.addEventListener('resize', () => goTo(current), { passive: true });
    }

    slides.forEach((slide) => {
      const img = slide.querySelector('.gallery-carousel__img');
      if (!img) return;
      img.style.cursor = 'zoom-in';
      img.addEventListener('click', () => openLightbox(img.currentSrc || img.src, img.alt));
    });
  }

  document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.gallery-carousel').forEach(initGallery);
  });
})();
