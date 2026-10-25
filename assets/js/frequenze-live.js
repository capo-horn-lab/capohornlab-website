/* Live frequencies client (FREQ-SITO-1, phase 1): shows the engine JSON raw. Server data goes through textContent only. */
(function (global) {
  'use strict';
  var API_BASE = global.CHL_API_BASE || 'https://capohornlab-website.onrender.com/api/v1';
  var REFRESH_MS = 60000;
  var STALE_AFTER_S = 180;

  function el(id) { return document.getElementById(id); }
  function show(id, text) { el(id).textContent = text; }
  function txt(value) { return value == null ? '?' : String(value); }

  function render(r) {
    if (r === null || typeof r !== 'object' || Array.isArray(r)) {
      show('freq-stato', '');
      show('freq-dati', '');
      show('freq-avviso', 'Risposta inattesa dal backend.');
      return;
    }
    var dati = r.dati;
    if (dati == null) {
      show('freq-stato', '');
      show('freq-dati', '');
      show('freq-avviso', 'Il motore non ha ancora pubblicato.');
      return;
    }
    if (typeof dati !== 'object' || Array.isArray(dati)) {
      show('freq-stato', '');
      show('freq-dati', '');
      show('freq-avviso', 'Risposta inattesa dal backend.');
      return;
    }
    var p = dati.principale || {};
    show('freq-stato', 'Ultimo calcolo (ora di Roma): ' + txt(dati.ora_roma) +
      ' — ricevuto dal sito ' + txt(r.eta_s) + ' s fa' +
      ' — strumento principale ' + txt(p.strumento) +
      ' (' + txt(p.contratto) + ', barra ' + txt(p.ultima_barra) + ')');
    show('freq-dati', JSON.stringify(dati, null, 2));
    show('freq-avviso', typeof r.eta_s === 'number' && r.eta_s > STALE_AFTER_S
      ? 'Motore spento o scollegato da ' + Math.floor(r.eta_s / 60) + ' minuti.' : '');
  }

  function aggiornamentoFallito() {
    var ora = new Date().toLocaleTimeString('it-IT', { hour: '2-digit', minute: '2-digit' });
    show('freq-avviso', 'Aggiornamento fallito alle ' + ora + ', dati dell\'ultimo caricamento.');
  }

  function carica() {
    return fetch(API_BASE + '/frequenze', { cache: 'no-store' }).then(function (res) {
      if (!res.ok) { throw new Error('HTTP ' + res.status); }
      return res.json();
    }).then(render, aggiornamentoFallito);
  }

  global.CHLFrequenze = { carica: carica, render: render };
  carica();
  setInterval(carica, REFRESH_MS);
}(window));
