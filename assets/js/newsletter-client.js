/* Shared newsletter client. It never claims success before the API confirms it. */
(function (global) {
  'use strict';
  function subscribe(event) {
    event.preventDefault();
    var form = event.currentTarget;
    var button = form.querySelector('button[type="submit"]');
    var email = form.querySelector('input[type="email"]');
    var status = form.nextElementSibling && form.nextElementSibling.classList.contains('newsletter-status')
      ? form.nextElementSibling : null;
    if (!status) {
      status = document.createElement('p');
      status.className = 'newsletter-status';
      status.style.cssText = 'margin-top:10px;font-size:0.875rem;';
      form.insertAdjacentElement('afterend', status);
    }
    if (!email || !email.value.trim()) {
      status.textContent = 'Please enter your email address.';
      status.style.color = '#ef4444';
      return;
    }
    var original = button ? button.textContent : '';
    if (button) { button.disabled = true; button.textContent = 'Subscribing…'; }
    fetch('/api/v1/newsletter/subscribe', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: email.value.trim() })
    }).then(async function (response) {
      var data = await response.json().catch(function () { return {}; });
      if (!response.ok) throw new Error(data.detail || 'Subscription could not be completed.');
      status.textContent = data.message || 'Check your inbox to confirm your subscription.';
      status.style.color = '#059669';
      form.reset();
    }).catch(function (error) {
      status.textContent = error.message;
      status.style.color = '#ef4444';
    }).finally(function () {
      if (button) { button.disabled = false; button.textContent = original; }
    });
  }
  global.CHLNewsletter = { subscribe: subscribe };
})(window);
