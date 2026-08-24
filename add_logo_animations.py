# -*- coding: utf-8 -*-
"""Add logo (orbit mark SVG) + rich animations to all pages."""
import os, re

BASE = "D:/CapoHornLab/projects/capohornlab-website"

# Pages using the old PNG logo in <img>
PNG_PAGES = ["about.html", "contact.html", "dashboard.html", "documentation.html",
             "faq.html", "login.html", "method.html", "pricing.html", "research.html",
             "signup.html", "test-strategy.html"]

# research-detail uses text "CH" and no favicon
RD_PAGE = "research-detail.html"

# ---- Shared animation CSS (injected before </style>) ----
ANIM_CSS = """
    /* ── Scroll progress bar ── */
    .ch-scroll-progress {
      position: fixed; top: 0; left: 0; height: 2px; width: 0%;
      background: var(--ch-signal, #e33b2f);
      box-shadow: 0 0 8px rgba(227,59,47,.5);
      z-index: 9999; transition: width .08s linear;
    }
    /* ── Scroll reveal ── */
    .ch-reveal {
      opacity: 0; transform: translateY(26px);
      transition: opacity .7s cubic-bezier(.16,1,.3,1),
                  transform .7s cubic-bezier(.16,1,.3,1);
      will-change: opacity, transform;
    }
    .ch-reveal.is-visible { opacity: 1; transform: translateY(0); }
    @media (prefers-reduced-motion: reduce) {
      .ch-reveal { opacity: 1; transform: none; transition: none; }
    }
    /* ── Logo mark animation ── */
    .brand-icon img, .ch-nav-brand .brand-icon img {
      animation: chLogoFloat 7s ease-in-out infinite;
      filter: drop-shadow(0 0 10px rgba(227,59,47,.35));
    }
    .ch-nav-brand:hover .brand-icon img {
      transform: rotate(14deg) scale(1.1);
      transition: transform .4s cubic-bezier(.34,1.56,.64,1);
    }
    @keyframes chLogoFloat {
      0%, 100% { transform: rotate(0deg) scale(1); }
      50% { transform: rotate(3deg) scale(1.06); }
    }
"""

# ---- Shared animation JS (injected before </body>) ----
ANIM_JS = """
<script>
  (function() {
    // Scroll progress bar
    var bar = document.createElement('div');
    bar.className = 'ch-scroll-progress';
    document.body.appendChild(bar);
    function updateProgress() {
      var h = document.documentElement;
      var scrolled = h.scrollTop / Math.max(1, h.scrollHeight - h.clientHeight);
      bar.style.width = (scrolled * 100) + '%';
    }
    document.addEventListener('scroll', updateProgress, { passive: true });
    window.addEventListener('resize', updateProgress);
    updateProgress();

    // Scroll reveal via IntersectionObserver
    var revealSel = 'section, .ch-section, .page-hero, .ch-card, .step-card, ' +
                    '.research-card, .data-panel, .principle-card, .status-card, .feature-card';
    var targets = document.querySelectorAll(revealSel);
    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function(entries) {
        entries.forEach(function(e) {
          if (e.isIntersecting) {
            e.target.classList.add('is-visible');
            io.unobserve(e.target);
          }
        });
      }, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });
      targets.forEach(function(t, i) {
        t.classList.add('ch-reveal');
        t.style.transitionDelay = (i % 7) * 0.04 + 's';
        io.observe(t);
      });
    } else {
      targets.forEach(function(t) { t.classList.add('is-visible'); });
    }
  })();
</script>
"""

def inject_anim(path):
    with open(path, "r", encoding="utf-8") as f:
        c = f.read()
    orig = c
    if "ch-scroll-progress" not in c and "</style>" in c:
        c = c.replace("</style>", ANIM_CSS + "\n  </style>", 1)
    if "ch-scroll-progress" not in c and "</body>" in c:
        c = c.replace("</body>", ANIM_JS + "\n</body>", 1)
    if c != orig:
        with open(path, "w", encoding="utf-8") as f:
            f.write(c)
        return True
    return False

# 1. PNG pages: swap logo + object-fit + background
for p in PNG_PAGES:
    path = os.path.join(BASE, p)
    with open(path, "r", encoding="utf-8") as f:
        c = f.read()
    orig = c
    changes = []

    # Swap PNG -> orbit SVG
    n1 = c.count("assets/logo/capo-horn-lab-logo.png")
    c = c.replace("assets/logo/capo-horn-lab-logo.png", "assets/capo-horn-lab-orbit-mark.svg")
    if n1:
        changes.append(f"logo x{n1}")

    # object-fit cover -> contain (SVG needs contain, not crop)
    if "object-fit: cover" in c:
        c = c.replace("object-fit: cover", "object-fit: contain")
        changes.append("object-fit")

    # Remove old blue gradient background on brand-icon
    c = re.sub(
        r'background: linear-gradient\(135deg,\s*var\(--ch-blue-500\),\s*var\(--ch-amber-500\)\);',
        'background: transparent;',
        c
    )
    if "background: transparent" in c and "gradient" not in c.split("brand-icon")[0]:
        changes.append("bg-clean")

    if c != orig:
        with open(path, "w", encoding="utf-8") as f:
            f.write(c)
    print(f"{p}: {', '.join(changes) if changes else 'no logo change'}")

# 2. research-detail: add favicon + orbit SVG instead of text CH
path = os.path.join(BASE, RD_PAGE)
with open(path, "r", encoding="utf-8") as f:
    c = f.read()
orig = c
rd_changes = []

if 'rel="icon"' not in c and "<title>" in c:
    c = c.replace(
        "<title>Capo Horn Lab — Research Detail</title>",
        '<title>Capo Horn Lab — Research Detail</title>\n  <link rel="icon" type="image/svg+xml" href="assets/capo-horn-lab-orbit-mark.svg">',
        1
    )
    rd_changes.append("favicon")

c = c.replace('<div class="brand-icon">CH</div>',
              '<div class="brand-icon"><img src="assets/capo-horn-lab-orbit-mark.svg" alt="Capo Horn Lab"></div>')
if "brand-icon\"><img" in c:
    rd_changes.append("logo")

if c != orig:
    with open(path, "w", encoding="utf-8") as f:
        f.write(c)
print(f"{RD_PAGE}: {', '.join(rd_changes) if rd_changes else 'no change'}")

# 3. Inject animations on ALL pages (incl index)
all_pages = PNG_PAGES + [RD_PAGE]  # index already has its own canvas/orbit
for p in all_pages:
    path = os.path.join(BASE, p)
    if inject_anim(path):
        print(f"{p}: animations injected")

print("\nDone")
