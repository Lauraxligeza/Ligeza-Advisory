const year = document.getElementById('year');
if (year) year.textContent = new Date().getFullYear();

const menuButton = document.querySelector('.hamburger');
const menu = document.querySelector('.nav-links');
const navbar = document.getElementById('navbar');
if (navbar) {
  const updateNavbar = () => navbar.classList.toggle('is-scrolled', window.scrollY > 20);
  window.addEventListener('scroll', updateNavbar, { passive: true });
  updateNavbar();
}

if (menuButton && menu) {
  const setMenuOpen = (isOpen) => {
    menu.classList.toggle('open', isOpen);
    menuButton.setAttribute('aria-expanded', String(isOpen));
    menuButton.setAttribute('aria-label', isOpen ? 'Close menu' : 'Open menu');
  };
  menuButton.addEventListener('click', () => setMenuOpen(!menu.classList.contains('open')));
  menu.addEventListener('click', (event) => {
    if (event.target.closest('a')) setMenuOpen(false);
  });
  document.addEventListener('click', (event) => {
    if (!navbar.contains(event.target)) setMenuOpen(false);
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && menu.classList.contains('open')) {
      setMenuOpen(false);
      menuButton.focus();
    }
  });
  document.addEventListener('focusin', (event) => {
    if (!navbar.contains(event.target)) setMenuOpen(false);
  });
  window.matchMedia('(max-width: 1100px)').addEventListener('change', () => setMenuOpen(false));
}

const filters = document.querySelectorAll('[data-filter]');
const articles = document.querySelectorAll('[data-category]');

filters.forEach((filter) => {
  filter.addEventListener('click', () => {
    const selected = filter.dataset.filter;
    filters.forEach((button) => {
      button.setAttribute('aria-pressed', String(button === filter));
    });
    articles.forEach((article) => {
      article.hidden = selected !== 'all' && article.dataset.category !== selected;
    });
  });
});

const serviceParameter = new URLSearchParams(window.location.search).get('service');
const serviceAliases = {
  "market-entry-assessment": "market-entry-review",
  "market-entry-quick-check": "market-entry-review",
  "competitor-positioning-snapshot": "market-entry-review",
  "market-sales-adaptation": "market-entry-implementation",
  "localization-market-fit-review": "market-entry-implementation",
  "website-market-fit-review": "market-entry-implementation",
  "buyer-distributor-targeting": "market-development",
  "market-development-pilot": "market-development",
  "market-development-support": "market-development"
};
const requestedService = serviceAliases[serviceParameter] || serviceParameter;
if (requestedService) {
  document.querySelectorAll('[data-service-select]').forEach((select) => {
    if ([...select.options].some((option) => option.value === requestedService)) {
      select.value = requestedService;
    }
  });
}
