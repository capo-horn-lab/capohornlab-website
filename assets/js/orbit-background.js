/* Capo Horn Lab — Orbit Background (fixed, site-wide, autonomous)
   Draws a self-orbiting particle field behind every page.
   No mouse interaction, no small box — full-viewport fixed canvas. */
(function () {
  'use strict';

  // ── Inject positioning CSS ──
  var css = [
    '#orbit-bg { position: fixed; inset: 0; z-index: 0; pointer-events: none; width: 100vw; height: 100vh; display: block; }',
    '#orbit-veil { position: fixed; inset: 0; z-index: 1; pointer-events: none; ',
    '  background: radial-gradient(ellipse at 50% 42%, rgba(7,11,18,0.10) 0%, rgba(7,11,18,0.42) 55%, rgba(7,11,18,0.70) 100%); }',
    'body > *:not(#orbit-bg):not(#orbit-veil):not(script) { position: relative; z-index: 2; }'
  ].join('\n');
  var st = document.createElement('style');
  st.id = 'orbit-bg-style';
  st.textContent = css;
  document.head.appendChild(st);

  // ── Create canvas + veil ──
  var canvas = document.createElement('canvas');
  canvas.id = 'orbit-bg';
  var veil = document.createElement('div');
  veil.id = 'orbit-veil';
  document.body.insertBefore(veil, document.body.firstChild);
  document.body.insertBefore(canvas, document.body.firstChild);

  var ctx = canvas.getContext('2d');
  var w = 0, h = 0, dpr = 1, frame = 0;

  // ── Particles (deterministic seed) ──
  var seed = 1847;
  var rnd = function () { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; };
  var particles = [];
  var N = window.innerWidth < 700 ? 70 : 130;
  for (var i = 0; i < N; i++) {
    var a = rnd() * Math.PI * 2;
    var lat = (rnd() - 0.5) * 1.5;
    var r = 0.45 + rnd() * 0.75;
    particles.push({
      a: a, lat: lat, r: r,
      rate: 0.10 + rnd() * 0.38,
      size: 0.4 + rnd() * 1.7,
      phase: rnd() * 7
    });
  }
  // Warm "research nodes" that orbit like planets
  var nodes = [];
  for (var n = 0; n < 6; n++) {
    nodes.push({
      a: rnd() * Math.PI * 2,
      r: 0.6 + rnd() * 0.5,
      rate: 0.06 + rnd() * 0.14,
      size: 2.5 + rnd() * 3.5
    });
  }

  function hexToRgb(hex) {
    var n = parseInt(hex.replace('#', ''), 16);
    return [(n >> 16) & 255, (n >> 8) & 255, n & 255];
  }

  function resize() {
    dpr = Math.min(window.devicePixelRatio || 1, 1.5);
    w = window.innerWidth;
    h = window.innerHeight;
    canvas.width = Math.max(1, Math.round(w * dpr));
    canvas.height = Math.max(1, Math.round(h * dpr));
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }

  function project(x, y, z, tilt) {
    var cy = Math.cos(tilt), sy = Math.sin(tilt);
    var rx = x * cy - z * sy, rz = x * sy + z * cy;
    var px = rx / (2.6 - rz), py = y / (2.6 - rz);
    return { x: w * 0.5 + px * w * 0.8, y: h * 0.5 + py * h * 0.85, z: rz };
  }

  function draw(t) {
    frame = t * 0.00030;
    ctx.clearRect(0, 0, w, h);

    var signal = '#e33b2f', warm = '#ff9b64';
    try {
      var cs = getComputedStyle(document.body);
      signal = cs.getPropertyValue('--ch-signal').trim() || signal;
      warm = cs.getPropertyValue('--ch-warm').trim() || warm;
    } catch (e) {}
    var rgb = hexToRgb(signal);
    var wrgb = hexToRgb(warm);

    // Slow autonomous drift — NOT tied to the mouse
    var tilt = 0.46 + Math.sin(t * 0.00008) * 0.07;
    var lift = Math.sin(t * 0.00011) * 0.05;

    // Ambient fog
    var fog = ctx.createRadialGradient(w * 0.5, h * 0.5, 0, w * 0.5, h * 0.5, Math.max(w, h) * 0.75);
    fog.addColorStop(0, 'rgba(' + rgb[0] + ',' + rgb[1] + ',' + rgb[2] + ',0.18)');
    fog.addColorStop(0.5, 'rgba(' + rgb[0] + ',' + rgb[1] + ',' + rgb[2] + ',0.04)');
    fog.addColorStop(1, 'rgba(0,0,0,0)');
    ctx.fillStyle = fog;
    ctx.fillRect(0, 0, w, h);

    // Orbital rings
    ctx.save();
    ctx.lineWidth = 0.5;
    for (var ring = 0; ring < 8; ring++) {
      ctx.beginPath();
      for (var j = 0; j <= 96; j++) {
        var q = j / 96 * Math.PI * 2;
        var rad = 0.36 + ring * 0.14;
        var p = project(Math.cos(q) * rad, Math.sin(q) * rad * 0.5 + lift, Math.sin(q) * rad * 0.32, tilt);
        if (j) ctx.lineTo(p.x, p.y); else ctx.moveTo(p.x, p.y);
      }
      ctx.strokeStyle = 'rgba(' + rgb[0] + ',' + rgb[1] + ',' + rgb[2] + ',' + (0.014 + ring * 0.006) + ')';
      ctx.stroke();
    }
    ctx.restore();

    // Particles
    var draws = particles.map(function (p) {
      var a = p.a + frame * p.rate;
      var x = Math.cos(a) * p.r;
      var y = Math.sin(p.lat + Math.sin(a * 1.7 + p.phase) * 0.16) * p.r;
      var z = Math.sin(a) * p.r * 0.64;
      return { p: project(x, y + lift, z, tilt), size: p.size };
    }).sort(function (a, b) { return a.p.z - b.p.z; });

    for (var k = 0; k < draws.length; k++) {
      var d = draws[k];
      var alpha = 0.14 + (d.p.z + 1) * 0.30;
      ctx.beginPath();
      ctx.arc(d.p.x, d.p.y, d.size * (0.7 + (d.p.z + 1) * 0.5), 0, Math.PI * 2);
      ctx.fillStyle = 'rgba(' + rgb[0] + ',' + rgb[1] + ',' + rgb[2] + ',' + Math.max(0.06, alpha) + ')';
      ctx.fill();
    }

    // Warm nodes
    for (var m = 0; m < nodes.length; m++) {
      var nd = nodes[m];
      var na = nd.a + frame * nd.rate;
      var nx = Math.cos(na) * nd.r;
      var ny = Math.sin(na) * nd.r * 0.5 + lift;
      var nz = Math.sin(na) * nd.r * 0.6;
      var np = project(nx, ny, nz, tilt);
      var ns = nd.size * (0.8 + (np.z + 1) * 0.5);
      ctx.beginPath();
      ctx.arc(np.x, np.y, ns, 0, Math.PI * 2);
      ctx.fillStyle = 'rgba(' + wrgb[0] + ',' + wrgb[1] + ',' + wrgb[2] + ',' + (0.35 + (np.z + 1) * 0.2) + ')';
      ctx.fill();
      ctx.beginPath();
      ctx.arc(np.x, np.y, ns * 2.4, 0, Math.PI * 2);
      ctx.fillStyle = 'rgba(' + wrgb[0] + ',' + wrgb[1] + ',' + wrgb[2] + ',0.05)';
      ctx.fill();
    }

    // Central core
    var core = project(0, lift, 0, tilt);
    var glow = ctx.createRadialGradient(core.x, core.y, 0, core.x, core.y, Math.min(w, h) * 0.3);
    glow.addColorStop(0, 'rgba(' + rgb[0] + ',' + rgb[1] + ',' + rgb[2] + ',0.32)');
    glow.addColorStop(0.4, 'rgba(' + rgb[0] + ',' + rgb[1] + ',' + rgb[2] + ',0.08)');
    glow.addColorStop(1, 'rgba(' + rgb[0] + ',' + rgb[1] + ',' + rgb[2] + ',0)');
    ctx.fillStyle = glow;
    ctx.beginPath();
    ctx.arc(core.x, core.y, Math.min(w, h) * 0.3, 0, Math.PI * 2);
    ctx.fill();

    requestAnimationFrame(draw);
  }

  window.addEventListener('resize', resize);
  resize();
  requestAnimationFrame(draw);
})();
