/* Capo Horn Lab — unified left sidebar builder.
   Injects a site-wide sidebar ordered by importance.
   Relies on assets/css/sidebar.css (link it in <head>). */
(function () {
  if (document.getElementById('chl-sidebar')) return;

  // ── Menu, ordered by importance ──
  var MENU = [
    { href: 'index.html',         label: 'Home',         idx: '01' },
    { href: 'research.html',      label: 'Research',     idx: '02' },
    { href: 'method.html',        label: 'Method',       idx: '03' },
    { href: 'test-strategy.html', label: 'Enter the Lab', idx: '04', cta: true },
    { href: 'about.html',         label: 'About',        idx: '05' },
    { href: 'pricing.html',       label: 'Pricing',      idx: '06' },
    { href: 'contact.html',       label: 'Contact',      idx: '07' }
  ];

  // ── Resolve current page for active state ──
  var path = (location.pathname || '').split('/').pop() || 'index.html';
  if (!path || path === '') path = 'index.html';

  function isActive(href) {
    var h = href.split('/').pop();
    return h === path;
  }

  // ── Build DOM ──
  var aside = document.createElement('aside');
  aside.id = 'chl-sidebar';
  aside.setAttribute('aria-label', 'Primary navigation');

  var html = '';
  html += '<div class="sb-brand">';
  html += '  <img src="assets/capo-horn-lab-orbit-mark.svg" alt="Capo Horn Lab" width="34" height="34">';
  html += '  <div class="sb-name"><strong>Capo Horn Lab</strong><small>Research observatory</small></div>';
  html += '</div>';
  html += '<div class="sb-group-label">Navigate</div>';
  html += '<nav>';
  for (var i = 0; i < MENU.length; i++) {
    var item = MENU[i];
    var cls = item.cta ? 'sb-cta' : '';
    if (isActive(item.href)) cls += ' active';
    html += '<a class="' + cls + '" href="' + item.href + '">';
    html += '<span>' + item.label + '</span>';
    html += '<span class="sb-idx">' + item.idx + '</span>';
    html += '</a>';
  }
  html += '</nav>';

  // ── Auth section: user avatar + name (logged in) or login/signup links ──
  var user = null;
  try { user = JSON.parse(localStorage.getItem('chl_user') || 'null'); } catch (_) {}

  html += '<div class="sb-foot">';
  if (user && user.email) {
    // Avatar from first letters of name or first email letter
    var initials = (user.name || user.email).split(/\s+/).slice(0,2).map(function(w){return (w[0]||'').toUpperCase();}).join('');
    if (!initials || initials.length < 2) initials = (user.email[0] || '').toUpperCase();
    html += '<a href="dashboard.html" class="sb-user">';
    html += '<span class="sb-avatar">' + initials + '</span>';
    html += '<span class="sb-user-name">' + (user.name || user.email.split('@')[0]) + '</span>';
    html += '</a>';
    html += '<a href="#" class="sb-logout" onclick="window.CHLAccount.logout();return false">Log out</a>';
  } else {
    html += '<a href="login.html">Log in</a>';
    html += '<a href="signup.html">Sign up</a>';
  }
  html += '</div>';

  aside.innerHTML = html;
  document.body.insertBefore(aside, document.body.firstChild);
  document.body.classList.add('chl-has-sidebar');

  // ── Mobile toggle ──
  var toggle = document.createElement('button');
  toggle.id = 'chl-sidebar-toggle';
  toggle.setAttribute('aria-label', 'Toggle menu');
  toggle.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">' +
    '<line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/>' +
    '<line x1="3" y1="18" x2="21" y2="18"/></svg>';
  toggle.addEventListener('click', function () {
    aside.classList.toggle('chl-open');
  });
  document.body.appendChild(toggle);
})();
