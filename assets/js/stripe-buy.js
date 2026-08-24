/* Capo Horn Lab — Stripe buy flow + card management
   Requires Stripe.js loaded from CDN in the page head. */
(function () {
  var API_BASE = 'https://capohornlab-website.onrender.com/api/v1';
  var STRIPE_KEY = null;  // fetched from /api/v1/config

  function token() {
    return localStorage.getItem('chl_access_token');
  }

  function authHeaders() {
    return { 'Authorization': 'Bearer ' + token(), 'Content-Type': 'application/json' };
  }

  /* ── fetch stripe publishable key ── */
  function init() {
    return fetch(API_BASE + '/config', { credentials: 'include' })
      .then(function (r) { return r.json(); })
      .then(function (cfg) {
        STRIPE_KEY = cfg.stripe_publishable_key;
        if (STRIPE_KEY) {
          window.Stripe(STRIPE_KEY);  // load Stripe.js
        }
      })
      .catch(function () {
        console.warn('CHL: Stripe not configured — payments unavailable');
      });
  }

  /* ── Buy a product ── */
  function buy(productSlug, productName, productType, amount) {
    if (!token()) {
      alert('Log in first to purchase.');
      window.location.href = 'login.html?next=' + encodeURIComponent(window.location.pathname);
      return Promise.reject('not logged in');
    }

    var body = {
      product_slug: productSlug,
      product_name: productName,
      product_type: productType,
      amount: amount
    };

    return fetch(API_BASE + '/payments/buy', {
      method: 'POST',
      headers: authHeaders(),
      body: JSON.stringify(body),
      credentials: 'include'
    }).then(function (r) {
      if (r.status === 409) {
        alert('You already own this product.');
        return null;
      }
      if (r.status === 402) {
        return r.json().then(function (e) { throw new Error(e.detail || 'Payment failed — is your card set up?'); });
      }
      if (!r.ok) {
        return r.json().then(function (e) { throw new Error(e.detail || 'Purchase failed.'); });
      }
      return r.json();
    });
  }

  /* ── Setup card ── */
  function setupCard(paymentMethodId) {
    if (!token()) {
      alert('Log in first.');
      return Promise.reject('not logged in');
    }
    return fetch(API_BASE + '/payments/setup-card', {
      method: 'POST',
      headers: authHeaders(),
      body: JSON.stringify({ payment_method_id: paymentMethodId }),
      credentials: 'include'
    }).then(function (r) {
      if (!r.ok) return r.json().then(function (e) { throw new Error(e.detail || 'Card setup failed.'); });
      return r.json();
    });
  }

  /* ── Load purchases + cards ── */
  function getDashboard() {
    if (!token()) return Promise.reject('not logged in');
    return fetch(API_BASE + '/payments/dashboard', {
      headers: authHeaders(),
      credentials: 'include'
    }).then(function (r) { return r.json(); });
  }

  /* ── Expose ── */
  window.CHLPay = {
    init: init,
    buy: buy,
    setupCard: setupCard,
    getDashboard: getDashboard,
    hasToken: function () { return !!token(); }
  };

  // Auto-init
  if (token()) { init(); }
})();