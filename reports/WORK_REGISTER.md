# WORK REGISTER — God Mode Deploy + QA cycle · 2026-08-23

## ✅ DEPLOY ARUBA COMPLETATO

- **369 file** uploadati via FTP su `/www.capohornlab.com/` — zero errori
- **Meta anti-cache**: no-store/no-cache/must-revalidate live su login, signup, dashboard
- **Redirect stub**: `/pages/index.html` e `/pages/documentation.html` → 200, redirect canonico
- **Cache**: X-Aruba-Cache: MISS (cache pulita da Francesco prima del deploy)
- **8 key pages**: tutte 200 (login, signup, dashboard, pricing, research, about, faq, documentation)
- **index.php** / **ver.php** Aruba → rinominati in backup
- **QA file sparsi** rimossi dalla root (22 file temporanei)
- **GitHub**: push su master + main sincronizzati

## Verifica live

| Risorsa | HTTP | Contenuto |
|---------|------|-----------|
| https://www.capohornlab.com/ | 200 | Home, X-Aruba-Cache: MISS |
| /login.html | 200 | no-store, no-cache, must-revalidate ✅ |
| /dashboard.html | 200 | no-store, no-cache, must-revalidate ✅ |
| /signup.html | 200 | no-store, no-cache, must-revalidate ✅ |
| /pages/index.html | 200 | redirect → ../index.html ✅ |
| /pages/documentation.html | 200 | redirect → ../documentation.html ✅ |

## ⏳ DA FARE

- **Ricerca**: QA chart per entry (14 studi)
- **Backend**: migrare SQLite effimero → Postgres gestito (Neon/Supabase) prima di utenti reali
- **Browser automation**: CDP non disponibile per click/console sweep live
- **Email supporto**: app password Gmail ancora da creare (Francesco)
- **Aruba cache**: se il sito mostra vecchio contenuto, ripetere purge da PannelloAdmin → Velocità → Caching