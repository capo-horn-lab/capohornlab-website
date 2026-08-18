# Session handoff — Resend/DNS — 2026-08-17

## Stato verificato

- Dominio Resend: `capohornlab.com` aggiunto.
- Aruba DNS panel: accesso riuscito.
- DKIM TXT salvato su Aruba: `resend._domainkey`.
- SPF TXT salvato su Aruba: host `send`, valore `v=spf1 include:amazonses.com ~all`.
- MX subdomain salvato su Aruba advanced management: host `send`, target `feedback-smtp.eu-west-1.amazonses.com`, priority `10`.
- Aruba main MX `@` → `mx.capohornlab.com`, priority `10`: NON modificato.
- DMARC esistente: NON modificato.

## Verifiche reali

- Aruba ha mostrato `Operazione andata a buon fine` per SPF e MX.
- DNS autorevole `dns.technorail.com` restituisce DKIM TXT.
- DNS autorevole `dns.technorail.com` restituisce SPF TXT per `send`.
- Il record MX `send` non è ancora restituito dal nameserver autorevole/pubblico.
- Resend mostra evento `DNS verified`, ma dominio ancora `Pending / Verifying domain`.

## Blocco attuale

Attendere propagazione/aggiornamento DNS del record MX `send`. Non aggiungere duplicati e non usare `SOSTITUISCI RECORD` in Aruba.

## Prossima sessione

1. Ricontrollare:
   - `nslookup -type=MX send.capohornlab.com dns.technorail.com`
   - `nslookup -type=TXT send.capohornlab.com dns.technorail.com`
2. Ricontrollare Resend fino a `Verified`.
3. Solo dopo la verifica creare/configurare API key Resend.
4. La API key è un segreto: non leggerla, non riportarla in chat, non salvarla in Git o nei report.
5. Inserirla nel secret manager/ambiente backend con procedura sicura.
6. Eseguire test reale signup → verifica email → login → contact → newsletter.
7. Nessun deploy ancora eseguito.

## File di riferimento

- `D:/CapoHornLab/projects/capohornlab-website/reports/resend-dns-execution-20260817.md`
- `D:/CapoHornLab/projects/capohornlab-website/reports/RESEND_ARUBA_DNS_SETUP.txt`
- `D:/CapoHornLab/projects/capohornlab-website/reports/implementation-progress-20260817.md`
