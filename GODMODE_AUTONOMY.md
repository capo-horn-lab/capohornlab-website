# God Mode — Autonomy Toggle

Francesco: this file documents how to turn OFF the authorization requests in
the God Mode autonomous loop.

## Status

**Autonomy flag: OFF** (default). God Mode freezes L3 payloads and asks you.

## Commands

| Azione | Comando |
|---|---|
| ATTIVA autonomia (il loop non chiede più per deploy/pubblicazioni sul sito) | `touch D:/CapoHornLab/projects/capohornlab-website/.godmode_autonomy` |
| DISATTIVA (torna a chiedere conferma) | `rm D:/CapoHornLab/projects/capohornlab-website/.godmode_autonomy` |
| Verifica stato | `ls D:/CapoHornLab/projects/capohornlab-website/.godmode_autonomy` |

Oppure da PowerShell:
```powershell
New-Item -ItemType File D:\CapoHornLab\projects\capohornlab-website\.godmode_autonomy
Remove-Item D:\CapoHornLab\projects\capohornlab-website\.godmode_autonomy
```

## Cosa cambia col flag ATTIVO

Il loop God Mode può procedere SENZA chiederti per:
- Deploy su Aruba (upload frontend)
- Pubblicazione ricerche/contenuti sul sito
- Push su GitHub

Ma deve comunque verificare ogni azione con un read-back reale (HTTP status,
file sul server, contenuto pagina live) prima di dichiarare successo.

## Cosa resta SEMPRE BLOCCATO (anche col flag attivo)

- Segreti e credenziali (mai letti/esposti)
- Pagamenti e configurazione pagamenti
- Ordini (trading)
- DNS / impostazioni Aruba / provider
- Messaggi esterni (email/Slack/Telegram non autorizzati)
- Cancellazione dati

## Opzionale: approvazioni runtime dei comandi in cron

Il runtime Hermes ha un secondo livello: i comandi shell "pericolosi" nei job
cron vengono NEGATI (approvals.cron_mode: deny). Per farli auto-approvare:

```
hermes config set approvals.cron_mode approve
```

Attenzione: vale per TUTTI i cron job (Task Observer, Startup, God Mode), non
solo per God Mode. Il floor di sicurezza (chmod -R 777, curl|sh, ecc.) resta
attivo comunque. Per tornare indietro: `hermes config set approvals.cron_mode deny`.
