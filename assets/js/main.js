(() => {
  const root = document.documentElement;
  const body = document.body;
  const header = document.querySelector('.site-header');
  const nav = document.querySelector('.site-nav');
  const navToggle = document.querySelector('.nav-toggle');
  const themeToggle = document.querySelector('.theme-toggle');
  const yearEl = document.getElementById('year');
  const progress = document.querySelector('.page-progress span');
  const navLinks = [...document.querySelectorAll('.site-nav a')];

  if (yearEl) yearEl.textContent = new Date().getFullYear();

  // Theme preference persists across all pages.
  const storedTheme = localStorage.getItem('kai-fa-lu-theme');
  const prefersDark = window.matchMedia?.('(prefers-color-scheme: dark)').matches;
  root.dataset.theme = storedTheme || (prefersDark ? 'dark' : 'light');
  themeToggle?.addEventListener('click', () => {
    const next = root.dataset.theme === 'dark' ? 'light' : 'dark';
    root.dataset.theme = next;
    localStorage.setItem('kai-fa-lu-theme', next);
  });

  const closeNav = () => {
    nav?.classList.remove('open');
    navToggle?.setAttribute('aria-expanded', 'false');
    navToggle?.setAttribute('aria-label', 'Open navigation');
  };

  navToggle?.addEventListener('click', () => {
    const isOpen = nav?.classList.toggle('open');
    navToggle.setAttribute('aria-expanded', String(Boolean(isOpen)));
    navToggle.setAttribute('aria-label', isOpen ? 'Close navigation' : 'Open navigation');
  });
  navLinks.forEach((link) => link.addEventListener('click', closeNav));
  window.addEventListener('resize', () => { if (window.innerWidth > 1080) closeNav(); });

  const updateScrollState = () => {
    const y = window.scrollY;
    header?.classList.toggle('scrolled', y > 12);
    if (progress) {
      const max = document.documentElement.scrollHeight - window.innerHeight;
      progress.style.width = `${max > 0 ? Math.min(100, (y / max) * 100) : 0}%`;
    }
  };
  updateScrollState();
  window.addEventListener('scroll', updateScrollState, { passive: true });

  // Reveal-on-scroll enhancement. Content remains visible when JavaScript is unavailable.
  const revealEls = [...document.querySelectorAll('.reveal')];
  if ('IntersectionObserver' in window && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    const observer = new IntersectionObserver((entries, obs) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('revealed');
          obs.unobserve(entry.target);
        }
      });
    }, { threshold: 0.08, rootMargin: '0px 0px -34px 0px' });
    revealEls.forEach((el) => observer.observe(el));
  } else {
    revealEls.forEach((el) => el.classList.add('revealed'));
  }

  // Complete-publication directory: independent status/topic filters plus text search.
  const records = [...document.querySelectorAll('.publication-record')];
  const searchInput = document.getElementById('publication-search');
  const filterButtons = [...document.querySelectorAll('.directory-filter')];
  const visibleCount = document.getElementById('visible-count');
  const emptyState = document.getElementById('publication-empty');
  const filterState = { status: 'all', topic: 'all', query: '' };

  const normalize = (value) => (value || '').toLowerCase().trim();
  const applyPublicationFilters = () => {
    let shown = 0;
    records.forEach((record) => {
      const statusMatch = filterState.status === 'all' || record.dataset.status === filterState.status;
      const topicMatch = filterState.topic === 'all' || record.dataset.topic === filterState.topic;
      const searchText = normalize(record.dataset.search || record.textContent);
      const queryMatch = !filterState.query || searchText.includes(filterState.query);
      const show = statusMatch && topicMatch && queryMatch;
      record.classList.toggle('is-hidden', !show);
      if (show) shown += 1;
    });
    if (visibleCount) visibleCount.textContent = String(shown);
    if (emptyState) emptyState.hidden = shown !== 0;
  };

  filterButtons.forEach((button) => {
    button.addEventListener('click', () => {
      const group = button.dataset.filterGroup;
      const value = button.dataset.filter || 'all';
      if (!group || !(group in filterState)) return;
      filterState[group] = value;
      filterButtons
        .filter((candidate) => candidate.dataset.filterGroup === group)
        .forEach((candidate) => candidate.classList.toggle('active', candidate === button));
      applyPublicationFilters();
    });
  });

  searchInput?.addEventListener('input', () => {
    filterState.query = normalize(searchInput.value);
    applyPublicationFilters();
  });

  if (records.length) applyPublicationFilters();

  // Highlight the contact navigation item while the home-page contact section is visible.
  const contactSection = document.getElementById('contact');
  const contactLink = document.querySelector('.site-nav a[data-nav="contact"]');
  const homeLink = document.querySelector('.site-nav a[data-nav="home"]');
  if (body?.dataset.page === 'home' && contactSection && contactLink && 'IntersectionObserver' in window) {
    const contactObserver = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        contactLink.classList.toggle('active', entry.isIntersecting);
        homeLink?.classList.toggle('section-dimmed', entry.isIntersecting);
      });
    }, { threshold: 0.35 });
    contactObserver.observe(contactSection);
  }
})();
