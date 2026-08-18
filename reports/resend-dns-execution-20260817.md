# Resend DNS execution log — 2026-08-17

## Applied in Aruba DNS panel

- DKIM TXT: `resend._domainkey` — Aruba reported operation successful.
- SPF TXT: `send` → `v=spf1 include:amazonses.com ~all` — Aruba panel shows saved.
- MX subdomain: `send` → `feedback-smtp.eu-west-1.amazonses.com`, priority 10 — Aruba reported `Operazione andata a buon fine` and displays the row.
- Main Aruba MX `@` → `mx.capohornlab.com`, priority 10 — not modified.
- Existing DMARC — not modified.

## Verification

- Authoritative DNS `dns.technorail.com`: DKIM TXT present.
- Authoritative DNS `dns.technorail.com`: SPF TXT for `send` present.
- Public Google/Cloudflare resolvers: SPF TXT present after propagation.
- Authoritative/public MX query for `send.capohornlab.com`: not returning the MX yet.
- Resend: `DNS verified` event reached, domain remains `Pending` while verifying.

## Remaining blocker

The MX row is visible in Aruba but not yet returned by the authoritative DNS response. Do not create a duplicate MX or replace the main Aruba MX. Allow DNS/provider propagation and recheck. Resend API key has not been created or handled by Camilla; secret values must not be read, typed, or placed in logs/chat.
