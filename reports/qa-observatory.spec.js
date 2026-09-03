const { test, chromium } = require('@playwright/test');
const path = require('path');

const root = 'D:/CapoHornLab/projects/capohornlab-website';
const pages = [
  ['home', 'index.html'],
  ['about', 'about.html'],
  ['method', 'method.html'],
  ['pricing', 'pricing.html'],
  ['admin', 'admin.html'],
  ['checkout', 'checkout.html'],
  ['privacy-policy', 'privacy-policy.html'],
];

test('Observatory visual screenshots', async () => {
  const browser = await chromium.launch({ headless: true });
  const results = [];
  for (const [name, rel] of pages) {
    const page = await browser.newPage({ viewport: { width: 1440, height: 1200 } });
    page.on('dialog', async dialog => {
      await dialog.accept('capohorn2026!');
    });
    await page.goto('file:///' + path.join(root, rel).replace(/\\/g, '/'), { waitUntil: 'load' });
    await page.waitForTimeout(700);
    const metrics = await page.evaluate(() => {
      const body = getComputedStyle(document.body);
      const h = document.querySelector('h1, .hero-title, .page-title, .admin-title');
      const hs = h ? getComputedStyle(h) : null;
      return {
        title: document.title,
        bodyBg: body.backgroundColor,
        bodyColor: body.color,
        bodyFont: body.fontFamily,
        hText: h ? h.textContent.trim().slice(0, 120) : '',
        hFont: hs ? hs.fontFamily : '',
        hasObservatory: document.documentElement.innerHTML.includes('observatory-tokens.css') || document.documentElement.innerHTML.includes('--ch-ink'),
        hasSidebar: !!document.querySelector('.site-sidebar, .ch-sidebar, aside') || document.body.innerText.includes('01 Home'),
      };
    });
    const shot = path.join(root, 'reports', `qa-observatory-${name}-pw.png`);
    await page.screenshot({ path: shot, fullPage: false });
    results.push({ name, rel, shot, metrics });
    await page.close();
  }
  await browser.close();
  console.log(JSON.stringify(results, null, 2));
});
