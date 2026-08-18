# Capo Horn Lab — Implementazione autorizzata

Data: 2026-08-17
Stato: sviluppo locale autorizzato; azioni esterne autorizzate ma subordinate a payload congelato e verifica.

## Caselle Aruba

- Supporto umano: support@capohornlab.com
- Contatti sito: contact@capohornlab.com
- Invii automatici: noreply@capohornlab.com
- Amministrazione: admin@capohornlab.com
- Privacy/DPO: privacy@capohornlab.com
- Test deliverability: tester@capohornlab.com
- Postmaster: postmaster@capohornlab.com

## Scelte applicative

- Frontend: Aruba.
- DNS: Aruba.
- Backend iniziale: PC locale; nessun dato market data originale sul frontend/server pubblico.
- Email transazionali: Resend, da verificare sul dominio capohornlab.com.
- Reply-To contatti: email del visitatore; destinazione: contact@capohornlab.com.
- Mittente automatico: noreply@capohornlab.com.
- Newsletter: double opt-in, unsubscribe, consenso separato dall'account.
- Pagamenti iniziali: Stripe Checkout come integrazione primaria; PayPal solo dopo specifica approvazione tecnica e test separato. POS Intesa resta una fase successiva.
- Motore backtest: PC locale, worker isolato, report controllati; Hermes non esposto direttamente al pubblico.
- Plausible analytics; niente marketing cookie.
- Account: verifica email richiesta, access token 15 minuti, refresh 7 giorni.
- Allegati: PDF, CSV, XLSX, PNG/JPG, ZIP, codice solo dopo validazione; nessun file eseguibile; limite iniziale raccomandato 25 MB/file, 5 file/richiesta.
- Dati: portfolio dati aziendale non pubblico; accessi cliente limitati ai dataset/entitlement acquistati.
- Stadi richiesta: Inviata, Info mancanti, In valutazione, Accettata, In lavorazione, Completata, Rifiutata.

## Autorizzazioni esterne ricevute

Francesco ha autorizzato: DNS Aruba per Resend, configurazione segreta Resend tramite canale sicuro, test email verso tester@capohornlab.com, configurazione Stripe/PayPal e pubblicazione frontend Aruba.

## Gate obbligatori prima dell'esecuzione esterna

1. Resend deve fornire record DNS esatti; non inventare SPF/DKIM/MX/CNAME.
2. Francesco completa login/2FA/passkey e inserimento segreti senza registrarli nei file o prompt.
3. Il test email deve essere verificato nella casella originale tester@capohornlab.com.
4. Stripe/PayPal devono usare prodotti e importi server-side; nessun prezzo proveniente dalla query string può autorizzare un pagamento.
5. Deploy Aruba deve usare un payload statico pulito, senza .env, dati raw, database, credenziali o artefatti non destinati al frontend.
6. Prima del deploy: test completo, diff finale e anteprima dei file inclusi.
