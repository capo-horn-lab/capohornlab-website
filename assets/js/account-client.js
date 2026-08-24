/* Capo Horn Lab browser account client. Tokens stay in sessionStorage. */
(function (global) {
  'use strict';

  var API_BASE = global.CHL_API_BASE || 'https://capohornlab-website.onrender.com/api/v1';
  var ACCESS_KEY = 'chl_access_token';
    var USER_KEY = 'chl_user';
    var storage = (function() { try { global.localStorage.setItem('_test_', '1'); global.localStorage.removeItem('_test_'); return global.localStorage; } catch (_) { return global.sessionStorage; } })();

  function errorMessage(response, fallback) {
    return response.json().then(function (body) {
      return Promise.reject(new Error(body.detail || body.message || body.error || fallback));
    }).catch(function (error) {
      if (error instanceof Error) throw error;
      throw new Error(fallback);
    });
  }

  function request(path, options) {
    options = options || {};
    options.credentials = options.credentials || 'include';
    options.headers = Object.assign({'Content-Type': 'application/json'}, options.headers || {});
    return fetch(API_BASE + path, options).then(function (response) {
      if (!response.ok) return errorMessage(response, 'The service could not complete the request.');
      return response.status === 204 ? null : response.json();
    });
  }

  function remember(login) {
    storage.setItem(ACCESS_KEY, login.access_token);
        storage.setItem(USER_KEY, JSON.stringify(login.user));
    return login.user;
  }

  function signup(name, email, password) {
    return request('/auth/signup', {
      method: 'POST', body: JSON.stringify({name: name, email: email, password: password})
    });
  }

  function login(email, password) {
    return request('/auth/login', {
      method: 'POST', body: JSON.stringify({email: email, password: password})
    }).then(remember);
  }

  function token() { return storage.getItem(ACCESS_KEY); }

  function getMe() {
      if (!token()) return Promise.reject(new Error('Please log in to continue.'));
      return request('/auth/me', {headers: {Authorization: 'Bearer ' + token()}}).then(function (user) {
        storage.setItem(USER_KEY, JSON.stringify(user));
        return user;
      });
    }

    function currentUser() {
      try { return JSON.parse(storage.getItem(USER_KEY) || 'null'); }
      catch (_) { return null; }
    }

  function requireSession() {
    if (!token()) { global.location.replace('login.html?next=dashboard.html'); return false; }
    return true;
  }

  function logout() {
      storage.removeItem(ACCESS_KEY);
      storage.removeItem(USER_KEY);
      global.location.assign('index.html');
    }

  function listRequests() {
    if (!token()) return Promise.reject(new Error('Please log in to continue.'));
    return request('/requests', {headers: {Authorization: 'Bearer ' + token()}});
  }

  function createRequest(payload) {
    if (!token()) return Promise.reject(new Error('Please log in to continue.'));
    return request('/requests', {method: 'POST', headers: {Authorization: 'Bearer ' + token()}, body: JSON.stringify(payload)});
  }

  function uploadAttachment(requestId, file) {
    if (!token()) return Promise.reject(new Error('Please log in to continue.'));
    var form = new FormData(); form.append('file', file);
    return fetch(API_BASE + '/requests/' + encodeURIComponent(requestId) + '/attachments', {
      method: 'POST', headers: {Authorization: 'Bearer ' + token()}, body: form
    }).then(function (response) {
      if (!response.ok) return errorMessage(response, 'Attachment upload failed.');
      return response.json();
    });
  }

  function refresh() {
    return fetch(API_BASE + '/auth/refresh', {method: 'POST', credentials: 'include'})
          .then(function (response) { if (!response.ok) throw new Error('Session expired.'); return response.json(); })
          .then(function (data) { storage.setItem(ACCESS_KEY, data.access_token); return data.access_token; });
  }

  function changePassword(currentPassword, newPassword) {
    if (!token()) return Promise.reject(new Error('Please log in to continue.'));
    return request('/auth/change-password', {
      method: 'POST',
      headers: {Authorization: 'Bearer ' + token()},
      body: JSON.stringify({current_password: currentPassword, new_password: newPassword})
    });
  }

  global.CHLAccount = {signup: signup, login: login, getMe: getMe, listRequests: listRequests, createRequest: createRequest, uploadAttachment: uploadAttachment, refresh: refresh, changePassword: changePassword, currentUser: currentUser, requireSession: requireSession, logout: logout};
})(window);
