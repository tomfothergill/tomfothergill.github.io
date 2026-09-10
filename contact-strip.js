(() => {
  const strip = document.querySelector('.contact-strip');
  if (!strip) return;
  const windowEl = strip.querySelector('.contact-strip__window');
  const track = strip.querySelector('.contact-strip__track');
  const group = strip.querySelector('.contact-strip__group');
  const toggle = strip.querySelector('.contact-strip__toggle');
  const copy = group.cloneNode(true);
  copy.setAttribute('aria-hidden', 'true');
  copy.querySelectorAll('a').forEach(link => link.tabIndex = -1);
  track.append(copy);
  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');

  function measure() {
    strip.classList.toggle('is-static', reducedMotion.matches);
    toggle.hidden = reducedMotion.matches;
    if (reducedMotion.matches) return;
    strip.style.setProperty('--contact-width', `${windowEl.clientWidth}px`);
    const width = group.getBoundingClientRect().width;
    strip.style.setProperty('--contact-distance', `${width}px`);
    strip.style.setProperty('--contact-duration', `${width / 28}s`);
    strip.classList.add('is-ready');
  }

  toggle.addEventListener('click', () => {
    const paused = strip.classList.toggle('is-paused');
    toggle.setAttribute('aria-pressed', String(paused));
    toggle.setAttribute('aria-label', `${paused ? 'Resume' : 'Pause'} contact carousel`);
    toggle.textContent = paused ? 'Play' : 'Pause';
  });
  reducedMotion.addEventListener('change', measure);
  new ResizeObserver(measure).observe(windowEl);
  document.fonts.ready.then(measure);
  measure();
})();
