# Setup Hermes su ASUS TUF Gaming F15 per Università di Architettura

> **Target:** Windows 11, uso universitario individuale. La guida parte da zero: include l'installazione di Hermes Agent, la configurazione e i primi test.
>
> **Obiettivo:** un assistente locale e prudente per studio, revisione testi, organizzazione progetti, analisi di PDF/testi e supporto a tavole/concept. Nessun abbonamento obbligatorio.
>
> **Modello consigliato all'inizio:** OpenRouter Free Models Router (`openrouter/free`).
>
> **Importante:** OpenRouter può offrire modelli gratuiti, ma non è una risorsa illimitata né garantita: disponibilità, modello effettivo e rate limit cambiano. Per avere costo marginale zero e disponibilità offline, aggiungere in seguito il modello locale opzionale con llama.cpp.

---

## Come usare questa guida (leggi prima)

- **Incolla i comandi, non scriverli a mano**: seleziona il testo del comando (Ctrl+C), incollalo in PowerShell con il tasto destro del mouse (o Ctrl+V) e premi Invio. Un solo carattere sbagliato fa fallire il comando.
- **Un comando alla volta**: esegui, guarda il risultato, poi passa al successivo.
- **Non saltare passaggi**: ogni capitolo prepara quello dopo.
- **Se qualcosa dà errore o non torna, fermati**: non cancellare nulla e non riprovare all'infinito. Scrivi a Francesco cosa appare a schermo (o mandagli una foto).
- **PowerShell si apre così**: menu Start, cerca "PowerShell" o "Terminale", premi Invio. Non serve l'amministratore.
- **Aspettati testi lunghi**: i messaggi del computer sono normali. Conta solo che il comando finisca senza errori.

---

## Il modo più facile (consigliato): fai solo il minimo, Hermes completa il resto

Questa guida si può usare in due modi:

- **Percorso A — fai da te**: segui i capitoli uno alla volta, da qui in fondo. Adatto a chi vuole capire ogni passaggio.
- **Percorso B — lascia fare a Hermes (consigliato)**: fai a mano solo il setup minimo (capitolo 1), poi passi questo foglio a Hermes e lui completa tutto da solo, chiedendoti aiuto solo per i passaggi che richiedono i tuoi account (OpenRouter, GitHub, Telegram). Per un principiante è il modo più semplice e meno soggetto a errori.

### Percorso B, passo per passo

1. **Installa Hermes** seguendo il capitolo 1 (installer desktop + primo avvio minimale). Fermati lì: non serve configurare niente a mano.
2. **Salva questo foglio** in una cartella facile da trovare, per esempio `Documenti\Uni-Architettura\`. Va bene sia il PDF sia il file .md: Hermes sa leggere entrambi.
3. **Apri Hermes** (doppio clic sull'app desktop, oppure il comando `hermes` in PowerShell) e scrivi questo messaggio:

   > Leggi il file `SETUP_HERMES_ASUS_TUF_F15_ARCHITETTURA` che ho salvato in `Documenti\Uni-Architettura` e completa da solo il setup del profilo `architettura` seguendo la guida: profilo, OpenRouter, configurazione, workspace, test e GitHub Desktop. Fai tu tutte le operazioni che puoi fare da terminale; se un passaggio prevede un wizard interattivo che non puoi usare, applica lo stesso risultato con i comandi `config set` indicati nella guida. Chiedimi aiuto solo quando serve qualcosa che posso fare solo io (creare account, API key, login, collegamento Telegram) e in quel caso dammi istruzioni passo-passo.

4. **Rispondi alle sue domande** quando ti chiede account o chiavi: sarà solo per OpenRouter (capitolo 4), GitHub (capitolo 7) e Telegram (qui sotto). Per il resto guarda mentre lavora.

### Il collegamento Telegram (l'unica parte "umana")

Hermes può avvisarti su Telegram. Per collegarlo serve creare un "bot", e solo tu puoi farlo (serve il tuo account Telegram):

1. Apri Telegram e cerca **@BotFather** (è il bot ufficiale di Telegram, con la spunta blu).
2. Scrivi `/newbot` e segui le domande: scegli un nome (es. "Assistente Architettura") e uno username che finisce in `bot` (es. `assistente_architettura_bot`).
3. BotFather ti risponde con un **token** (una stringa lunga tipo `123456:ABC-DEF...`). È la "chiave" del bot: **non va mai incollata in chat**.
4. Quando Hermes ti chiede il token per Telegram, digli: "il token è pronto, dimmi dove incollarlo". Hermes ti indica il file `.env` del profilo da aprire (comando `notepad (hermes -p architettura config env-path)`): incolli lì il token, salvi, chiudi e dici a Hermes "fatto".
5. Hermes completa la configurazione e ti manda un messaggio di prova su Telegram.

> Se in qualsiasi momento una richiesta di Hermes ti sembra strana o vuoi fermarti, rispondi "no" o "fermati": con le approvazioni su smart (capitolo 0) Hermes chiede conferma prima delle azioni delicate. In caso di dubbi, chiama Francesco.

---

## 0. Regole di sicurezza e aspettative

1. Creare un profilo Hermes separato chiamato `architettura`: non mescolare i file o la memoria con altri progetti/personaggi.
2. Non incollare mai API key, password, token o codici 2FA in una chat, in documenti condivisi o nel prompt dell'agente.
3. Per i primi giorni mantenere le approvazioni su `smart`: Hermes deve chiedere quando un'azione è ambigua o rischiosa.
4. Non attivare gateway Telegram/Discord, automazioni cron, browser automation o strumenti di controllo desktop fino a quando la chat base non è verificata.
5. Per i lavori universitari verificare sempre fonti, norme, citazioni, dimensioni e calcoli: Hermes è un assistente, non una fonte finale né un progettista abilitato.

---

## 1. Installare Hermes Agent

La guida parte da zero: il PC deve avere solo Windows 11 aggiornato, connessione Internet e circa 3 GB di spazio libero.

### 1.1 Installazione (metodo consigliato: installer desktop)

1. Aprire il sito ufficiale https://hermes-agent.nousresearch.com/ e cliccare il pulsante di download per Windows (installer **Hermes Desktop**). Se il browser chiede dove salvare, scegliere "Download".
2. Aprire il file scaricato (nella cartella Download) e seguire la procedura: nella pratica basta cliccare **Avanti / Installa** fino alla fine. L'installer installa sia l'app desktop sia il comando `hermes` nel terminale.
3. Al termine, chiudere e riaprire PowerShell: serve a far riconoscere il nuovo comando.

### 1.2 Alternativa solo terminale

Se non si vuole l'app desktop, da PowerShell:

```powershell
iex (irm https://hermes-agent.nousresearch.com/install.ps1)
```

Poi chiudere e riaprire PowerShell.

### 1.3 Verificare l'installazione

```powershell
hermes --version
hermes doctor
```

`--version` deve mostrare una versione; `doctor` segnala eventuali problemi di base (Python, configurazione, spazio su disco). Se `doctor` mostra errori critici, risolverli prima di proseguire.

### 1.4 Primo avvio

```powershell
hermes setup
```

Il programma fa alcune domande. Scegliere sempre **l'opzione più semplice e minimale**: se compare **Blank Slate**, sceglierla (parte con tutto spento tranne l'essenziale). Non serve inserire nessuna API key: provider e modello si configurano nel profilo dedicato al capitolo 3, e la chiave OpenRouter si aggiunge nel capitolo 4. Se una domanda non è chiara, scegliere l'opzione più prudente e proseguire, oppure chiedere a Francesco. Al termine chiudere e riaprire PowerShell.

> In questa fase non serve inserire nessuna API key: se il wizard la chiede, si può saltare.

---

## 2. Verificare il PC e Hermes

Aprire **PowerShell** (non serve amministratore) e copiare questi comandi uno alla volta.

```powershell
# Versione Hermes e diagnostica non distruttiva
hermes --version
hermes doctor

# Versione Windows, RAM, CPU e GPU
Get-ComputerInfo | Select-Object WindowsProductName, WindowsVersion, OsBuildNumber, CsSystemType
Get-CimInstance Win32_ComputerSystem | Select-Object TotalPhysicalMemory
Get-CimInstance Win32_Processor | Select-Object Name, NumberOfCores, NumberOfLogicalProcessors
Get-CimInstance Win32_VideoController | Select-Object Name, AdapterRAM, DriverVersion

# Spazio libero sui dischi
Get-PSDrive -PSProvider FileSystem
```

### Cosa annotare

- modello GPU NVIDIA (ad esempio GTX 1650, RTX 3050, RTX 3060, RTX 4050/4060);
- VRAM disponibile;
- RAM totale;
- spazio libero su SSD (per un modello locale lasciare almeno 15–25 GB liberi);
- output di `hermes doctor` se ci sono errori.

> La serie ASUS TUF F15 esiste con molte GPU diverse. Non scegliere un modello locale “a caso”: la scelta dipende soprattutto da VRAM e RAM rilevate qui.

---

## 3. Creare un profilo Hermes isolato

```powershell
# Crea/configura il profilo universitario separato.
hermes -p architettura setup
```

Nel wizard:

1. scegliere una configurazione controllata/minimale se disponibile;
2. selezionare **OpenRouter** come provider;
3. non abilitare ancora Telegram, Discord, cron, email, browser automation o desktop control;
4. abilitare solo gli strumenti necessari per iniziare: file, terminale e skills.

Al termine, controllare il percorso della configurazione:

```powershell
hermes -p architettura config path
hermes -p architettura config env-path
hermes -p architettura config check
```

---

## 4. Configurare OpenRouter senza abbonamento

### 4.1 Creare l'account e la chiave

1. Aprire [OpenRouter](https://openrouter.ai/).
2. Creare un account e verificare l'email.
3. Nella sezione **Keys**, creare una chiave con nome, ad esempio `hermes-architettura`.
4. Se OpenRouter offre limiti/budget per la chiave, impostare il limite più restrittivo disponibile.
5. Copiare la chiave **solo nel computer dell'amico**.

### 4.2 Salvare la chiave in modo locale

Aprire il file `.env` del profilo:

```powershell
notepad (hermes -p architettura config env-path)
```

Aggiungere una sola riga, sostituendo il valore **sul PC**, senza mai inviarlo in chat:

```dotenv
OPENROUTER_API_KEY=incolla-la-chiave-solo-qui
```

Salvare e chiudere Notepad.

### 4.3 Selezionare il router gratuito

Impostare il provider e il modello gratuito:

```powershell
hermes -p architettura config set model.provider openrouter
hermes -p architettura config set model.default openrouter/free
hermes -p architettura config set approvals.mode smart
hermes -p architettura config set security.redact_secrets true
```

Il modello `openrouter/free` lascia a OpenRouter la scelta tra i modelli attualmente disponibili a prezzo zero. Questo è comodo per iniziare, ma significa che il modello può cambiare e che esistono limiti di frequenza.

### 4.4 Verificare una chat reale

Chiudere e riaprire PowerShell, poi eseguire:

```powershell
hermes -p architettura chat -q "Rispondi con una frase: configurazione Hermes per architettura verificata."
hermes -p architettura status
```

**Risultato atteso:** la prima riga restituisce una frase sensata; `status` indica il profilo e il provider configurati.

Se ricevi `401`:
- controlla che la chiave sia completa nel file `.env` corretto;
- genera una nuova chiave OpenRouter;
- riapri PowerShell e riprova.

Se ricevi `429` o un messaggio di rate limit:
- attendi il reset del limite;
- riprova più tardi;
- oppure passa al modello locale opzionale nel capitolo 11.

---

## 5. Configurazione consigliata per studio di architettura

Per iniziare serve un assistente utile ma con pochi privilegi.

```powershell
# Interfaccia testuale leggibile e costi visibili, se supportati dalla versione installata.
hermes -p architettura config set display.interface tui
hermes -p architettura config set display.language it
hermes -p architettura config set display.show_cost true

# Mantieni le conferme di sicurezza e la redazione dei segreti.
hermes -p architettura config set approvals.mode smart
hermes -p architettura config set security.redact_secrets true
```

Poi avvia la chat interattiva:

```powershell
hermes -p architettura
```

Esempi di richieste sicure e utili:

```text
- Trasforma questi appunti in una checklist per la revisione di progetto.
- Dammi tre concept alternativi per una biblioteca di quartiere, indicando vincoli, utenti e flussi.
- Rivedi questo testo in inglese accademico senza inventare fonti.
- Crea una struttura di indice per una relazione di laboratorio di progettazione.
- Dammi domande critiche da fare prima di definire una pianta.
- Riassumi questo PDF che ho caricato, separando fatti, tesi e fonti da verificare.
```

Prompt da evitare o da trattare con prudenza:

```text
- Firma o presenta un progetto al posto mio.
- Inventa norme urbanistiche, misure antincendio o citazioni bibliografiche.
- Modifica/cancella file senza mostrarmi cosa farà.
- Invia email o messaggi a docenti senza una bozza e una mia conferma.
```

---

## 6. Creare un workspace universitario ordinato

```powershell
# Adatta il percorso se OneDrive o il disco dati sono preferiti.
New-Item -ItemType Directory -Force "$HOME\Documents\Uni-Architettura\Progetti" | Out-Null
New-Item -ItemType Directory -Force "$HOME\Documents\Uni-Architettura\Fonti" | Out-Null
New-Item -ItemType Directory -Force "$HOME\Documents\Uni-Architettura\Consegne" | Out-Null
New-Item -ItemType Directory -Force "$HOME\Documents\Uni-Architettura\Appunti" | Out-Null

# Imposta la cartella di lavoro predefinita del profilo.
hermes -p architettura config set terminal.cwd "$HOME\Documents\Uni-Architettura"
```

Struttura suggerita:

```text
Documenti\Uni-Architettura\
├── Appunti\        # lezioni, brief, appunti personali
├── Fonti\          # PDF, paper, norme scaricate, bibliografia
├── Progetti\       # un sottocartella per ciascun corso/progetto
└── Consegne\       # PDF finali, tavole, testi definitivi
```

Per ogni progetto creare un file `PROJECT_BRIEF.md` con:

```markdown
# Nome progetto

## Obiettivo

## Sito e vincoli noti

## Utenti

## Programma funzionale

## Norme/fonti da verificare

## Scadenze

## Decisioni prese

## Questioni aperte
```

Questo evita che l'assistente confonda ipotesi, vincoli e fatti verificati.

---

## 7. Backup e versionamento con GitHub

### 7.1 Cosa sono Git e GitHub (spiegazione semplice)

- **Git** è un programma che tiene traccia della storia di una cartella di lavoro. Ogni volta che salvi una versione (si chiama **commit**), Git ricorda cosa è cambiato: se sbagli qualcosa o perdi un file, puoi tornare indietro.
- **GitHub** è un sito gratuito dove tieni la copia online dei tuoi progetti. Serve come **backup** e come **portfolio** mostrabile.

Per l'università serve a:

- evitare file come `progetto_finale_v2_definitivo_OK.docx` (con Git ogni versione ha un nome e una data);
- recuperare versioni precedenti se sbagli o cancelli qualcosa per errore;
- avere una copia in cloud dei lavori importanti (se il PC si rompe, i file restano su GitHub);
- mostrare i progetti in modo ordinato a professori e futuri studi (portfolio).

> GitHub è perfetto per documenti, testi, brief, script e PDF leggeri. I file pesanti di CAD/rendering (file Revit, DWG, render ad alta risoluzione) vanno tenuti su OneDrive/Google Drive: GitHub accetta file fino a 100 MB e non è fatto per i "progetti pesanti".

### 7.2 Installare GitHub Desktop (niente terminale)

1. Scaricare **GitHub Desktop** da https://desktop.github.com/ (gratuito, per Windows).
2. Installarlo: **Avanti / Installa** fino alla fine.
3. Aprire GitHub Desktop e accedere. Se non hai un account GitHub, crearlo su https://github.com/ (gratuito).

### 7.3 Il giro base: repository, commit e push

- **Repository (repo)** = una cartella di cui Git tiene la storia. In GitHub Desktop: **File → New repository**, scegli il nome e la cartella del progetto (per esempio `Uni-Architettura`).
- **Commit** = salva una versione. Quando hai fatto un pezzo di lavoro, in GitHub Desktop scrivi un messaggio breve ("tavola 2 completata") e clicca **Commit to main**.
- **Push** = carica la versione su GitHub (il backup online). Clicca **Push origin**.
- **Pull** = scarica da GitHub le modifiche (serve quando lavori da un altro PC).

**Regola semplice per iniziare**: un repository per progetto; un commit a ogni punto di arrivo; un push a fine giornata (backup fatto).

### 7.4 Il regalo per studenti: GitHub Student Developer Pack

Con l'email dell'università puoi attivare il **GitHub Student Developer Pack** (https://education.github.com/pack): strumenti professionali gratuiti finché sei studente, tra cui assistente di codice AI, crediti per modelli AI, hosting e software di design. Conviene attivarlo al primo anno.

### 7.5 Regole di sicurezza

- Mai caricare file con password, chiavi o dati personali sensibili.
- Attenzione a **public** vs **private**: un repository public è visibile a tutti. Per i lavori universitari va bene, ma se qualcosa non deve essere visto, crea un repository **private** (gratis anche quello).

---

## 8. Add-ons e strumenti utili per l'università (ricerca agosto 2026)

> Ricerca fatta il 18/08/2026: thread Reddit (r/architecture, r/archviz, r/Architects), guida ArchDaily sulle estensioni Chrome, elenco open-source Awesome-AECO su GitHub e sito GitHub Education. Prima di installare qualsiasi cosa, verifica che sia ancora disponibile e leggi i permessi richiesti.

### 8.1 Estensioni del browser (Chrome o Edge)

Selezionate dalla guida ArchDaily "14 Chrome Extensions to Make Your Architecture Browsing More Efficient" (2017, i classici del settore) più le estensioni studentesche più consigliate:

| Estensione | Cosa fa |
|---|---|
| Page Ruler | misura gli elementi di una pagina web in pixel (utile per layout e presentazioni) |
| ColorPick Eyedropper | prende il colore esatto di un punto qualsiasi della pagina (per palette e render) |
| Palette Creator | crea una palette di colori coerente da un'immagine |
| WhatFont | riconosce font e dimensione del testo di un sito |
| Power Thesaurus | sinonimi per descrizioni di progetto in inglese |
| Nimbus Screenshot | screenshot e registrazione dello schermo (tutorial e presentazioni) |
| StayFocusd | blocca i siti che distraggono mentre studi |
| Dark Reader | modalità scura su qualsiasi sito (schermo meno aggressivo la sera) |
| Grammarly | correzione dell'inglese scritto (abstract, relazioni) |
| Zotero Connector | salva citazioni e bibliografia dai siti (fondamentale per relazioni e tesi) |

Installazione: aprire il **Chrome Web Store** (chrome.google.com/webstore) o i **Componenti aggiuntivi di Edge**, cercare il nome e cliccare **Aggiungi**. Installa solo estensioni con molti utenti e recensioni: alcune chiedono permessi eccessivi, e quelle vanno evitate.

### 8.2 Strumenti open source da GitHub (gratis, con file aperti)

| Strumento | Cosa fa | Sito |
|---|---|---|
| FreeCAD | CAD 3D parametrico gratuito, con modulo Arch per il BIM | github.com/FreeCAD/FreeCAD |
| Blender + Bonsai BIM | modellazione 3D + plugin BIM gratuito (muri, porte, IFC) | github.com/blenderbim/blenderbim |
| LibreCAD | disegno 2D gratuito, stile AutoCAD base | github.com/LibreCAD/LibreCAD |
| Speckle | "Git per il BIM": condivide modelli tra software e persone | github.com/specklesystems/speckle-server |
| IfcOpenShell | legge e modifica file BIM (formato IFC), per chi programma | github.com/IfcOpenShell/IfcOpenShell |
| Dynamo | programmazione visuale per Revit (solo se usi Revit) | github.com/DynamoDS/Dynamo |

Open source vuol dire: gratis, aggiornato dalla comunità, e file in formato aperto (IFC) che non ti "sequestrano" il lavoro. Ottimo per iniziare senza abbonamenti.

### 8.3 Il pacchetto standard consigliato dalla community (Reddit)

Dai thread di r/architecture, r/Architects e r/archviz (2026) emerge un percorso comune per i primi anni:

- **SketchUp** — il punto di partenza per il 3D: semplice, adatto ai primi progetti;
- **AutoCAD** — disegno 2D tecnico, standard del settore (l'università di solito dà la licenza gratuita);
- **Adobe (Photoshop, InDesign, Illustrator)** — tavole, presentazioni e portfolio (licenza studente a prezzo ridotto);
- **Rhino + Grasshopper** — modellazione parametrica (più avanti nel percorso);
- **Enscape / Lumion** — rendering veloci (dai secondi anni in poi).

Regola d'oro dai thread: **non installare tutto subito**. Primo anno: SketchUp + AutoCAD + Adobe coprono la stragrande maggioranza del lavoro.

### 8.4 Bonus: la "God Mode" di Windows

**Cos'è**: un trucco notissimo e innocuo di Windows. Creando una cartella con un nome speciale, Windows la trasforma in un unico pannello che raccoglie **tutti** i settaggi del sistema (schermo, rete, suono, privacy, dischi, ecc.) in una sola lista ordinata. Niente di più: **non** sblocca funzioni nascoste, non modifica il sistema e non è un hack. È una scorciatoia che usa impostazioni già esistenti di Windows.

**Come si crea (Windows 11):**

1. Tasto destro sul desktop → **Nuovo → Cartella**.
2. Rinomina la cartella esattamente così (punto e graffe inclusi):
   ```
   GodMode.{ED7BA470-8E54-465E-825C-99712043E01C}
   ```
3. Premi Invio: l'icona diventa quella del Pannello di controllo.
4. Doppio clic per aprirla: tutte le impostazioni in un posto solo.

A cosa serve davvero: ritrovare impostazioni nascoste (per esempio gestione avanzata del mouse o opzioni di risparmio energia) senza cercarle una per una. Se non ti serve, la cancelli come una cartella normale: nessun effetto sul sistema.

---

## 9. Primo test funzionale con un file reale

Creare un piccolo brief di prova:

```powershell
@'
# Studio test

## Obiettivo
Proporre una piccola area di studio per studenti universitari.

## Vincoli
Superficie circa 60 m². Luce naturale da nord. Accessibilità da verificare.

## Richiesta
Tre alternative di organizzazione spaziale con pro e contro.
'@ | Set-Content "$HOME\Documents\Uni-Architettura\Appunti\brief-test.md"
```

Poi chiedere a Hermes:

```powershell
hermes -p architettura chat -q "Leggi il file Appunti/brief-test.md. Produci una tabella con: opzione, distribuzione spazi, vantaggi, rischi, dati mancanti. Non inventare norme o misure non presenti."
```

**Verifica manuale:** controllare che l'output distingua i vincoli presenti dalle informazioni mancanti. Se inventa valori, correggerlo esplicitamente: “non assumere dimensioni o norme senza fonte”.

---

## 10. Tool consigliati e tool da lasciare spenti all'inizio

### Attivare gradualmente, solo quando serve

- **File:** per leggere e organizzare brief, appunti e bozze.
- **Skills:** per procedure ripetibili, ad esempio revisione portfolio o bibliografia.
- **Web/Search:** solo per trovare fonti pubbliche, sempre verificando URL e data.
- **Vision:** utile per commentare immagini, planimetrie e PDF renderizzati; attenzione a non caricare materiale sensibile o protetto senza autorizzazione.

Per gestire toolset dalla UI/CLI usare:

```powershell
hermes -p architettura tools
```

Le modifiche agli strumenti diventano effettive dalla nuova sessione successiva. Dopo le modifiche, chiudere la chat e riaprire `hermes -p architettura`.

### Lasciare disattivati inizialmente

- `computer_use` / controllo desktop;
- browser automation;
- cron/automazioni schedulate;
- gateway Telegram/Discord/WhatsApp;
- email;
- delegazione multi-agente;
- MCP di terze parti non verificati.

Sono potenti ma non necessari per studiare. Attivarli solo dopo una necessità precisa e una verifica separata.

---

## 11. Opzione veramente gratuita: modello locale con llama.cpp

Questa parte è **opzionale**. Usarla se OpenRouter Free è troppo limitato, lento o non disponibile. Il costo API è zero, ma il PC consuma più batteria/energia e i modelli locali saranno in genere meno capaci di modelli cloud forti.

### 11.1 Scegliere dimensione modello in base alla GPU

| Hardware rilevato | Scelta iniziale prudente | Nota |
|---|---|---|
| GPU con 4 GB VRAM / 16 GB RAM | Qwen3 4B quantizzato Q4 | può usare CPU + GPU parziale; chiudere software pesante |
| GPU con 6 GB VRAM / 16–32 GB RAM | Qwen3 4B Q5 oppure Qwen3 8B Q4 | 8B più capace ma più lento/affamato |
| GPU con 8 GB VRAM / 32 GB RAM | Qwen3 8B Q4/Q5 | buon compromesso per testi e studio |
| Solo CPU o GPU non compatibile | Qwen3 4B Q4 | funziona, ma con risposta più lenta |

Non eseguire rendering pesanti (Enscape, Lumion, Twinmotion, Rhino, Revit) nello stesso momento del modello locale: possono contendersi VRAM e rendere entrambi instabili.

### 11.2 Installare llama.cpp

Aprire PowerShell **come amministratore** solo se `winget` lo richiede:

```powershell
winget install llama.cpp
```

Chiudere e riaprire PowerShell, quindi verificare:

```powershell
llama-server --help
```

### 11.3 Avviare una prova locale Qwen3 4B

Creare una cartella per i modelli:

```powershell
New-Item -ItemType Directory -Force "D:\AI-Models" | Out-Null
```

Eseguire il server. Il comando scarica il GGUF da Hugging Face la prima volta; occorre Internet solo per il download iniziale.

```powershell
llama-server -hf Qwen/Qwen3-4B-GGUF:Q4_K_M --host 127.0.0.1 --port 8080 -c 8192 -ngl 99
```

Se il PC va in errore VRAM/CUDA, fermare con `Ctrl+C` e riprovare riducendo i layer GPU:

```powershell
llama-server -hf Qwen/Qwen3-4B-GGUF:Q4_K_M --host 127.0.0.1 --port 8080 -c 4096 -ngl 20
```

Controllare la disponibilità del server in una seconda PowerShell:

```powershell
curl http://127.0.0.1:8080/v1/models
```

### 11.4 Collegare Hermes al server locale

Prima controllare il nome restituito da `/v1/models`. Poi impostare Hermes con quel nome (nell'esempio è `Qwen3-4B-Q4_K_M.gguf`; sostituirlo se l'output differisce):

```powershell
hermes -p architettura config set model.provider custom
hermes -p architettura config set model.base_url http://127.0.0.1:8080/v1
hermes -p architettura config set model.api_key local-offline
hermes -p architettura config set model.default Qwen3-4B-Q4_K_M.gguf
hermes -p architettura config set model.context_length 4096
```

Verificare:

```powershell
hermes -p architettura chat -q "Rispondi in italiano: modello locale Hermes verificato."
```

Per tornare a OpenRouter Free:

```powershell
hermes -p architettura config set model.provider openrouter
hermes -p architettura config set model.default openrouter/free
hermes -p architettura config unset model.base_url
hermes -p architettura config unset model.api_key
```

> Non esporre mai `llama-server` su `0.0.0.0` o su Internet. Mantenerlo su `127.0.0.1` come nei comandi sopra.

---

## 12. Aggiornamenti e diagnostica

Una volta al mese, oppure quando qualcosa non funziona:

```powershell
hermes doctor
hermes -p architettura config check
hermes -p architettura status
```

Prima di aggiornare, leggere le note di rilascio e fare un backup dei file del profilo e dei progetti. Non copiare file `.env` in cartelle cloud condivise.

---

## 13. Checklist finale

- [ ] Hermes è installato: `hermes --version` mostra una versione.
- [ ] `hermes doctor` non mostra blocchi critici.
- [ ] GitHub Desktop installato, primo commit e push fatti (capitolo 7).
- [ ] Il profilo `architettura` è separato e si avvia.
- [ ] `hermes -p architettura chat -q "..."` risponde.
- [ ] La chiave OpenRouter è solo nel `.env` locale e mai nel prompt/chat.
- [ ] Le approvazioni sono `smart`.
- [ ] Redazione segreti attiva.
- [ ] Un file di prova è stato letto senza inventare dati.
- [ ] Gateway/messaggistica/cron/browser control restano disattivati finché non servono.
- [ ] Se usato, il modello locale ascolta solo su `127.0.0.1`.

---

## Fonti ufficiali

- Hermes Agent — installazione e quickstart: https://hermes-agent.nousresearch.com/docs/getting-started/quickstart
- Hermes Agent — guida all'installazione (prerequisiti e risoluzione problemi): https://hermes-agent.nousresearch.com/docs/getting-started/installation
- GitHub Desktop: https://desktop.github.com/
- GitHub Student Developer Pack: https://education.github.com/pack
- ArchDaily — 14 Chrome Extensions to Make Your Architecture Browsing More Efficient: https://www.archdaily.com/870408/14-chrome-extensions-to-make-your-architecture-browsing-more-efficient
- Awesome-AECO (strumenti open source per architettura/ingegneria/edilizia): https://github.com/osama-ata/Awesome-AECO
- Reddit r/archviz — "If you were an architecture student again in 2026": https://www.reddit.com/r/archviz/comments/1rp0etk/
- Reddit r/Windows11 — thread sulla cartella God Mode: https://www.reddit.com/r/Windows11/comments/ueuvzk/
- Hermes Agent — provider: https://hermes-agent.nousresearch.com/docs/integrations/providers
- Hermes Agent — configurazione: https://hermes-agent.nousresearch.com/docs/user-guide/configuration
- OpenRouter — free models router: https://openrouter.ai/docs/cookbook/get-started/free-models-router-playground
- OpenRouter — modelli gratuiti correnti: https://openrouter.ai/models?max_price=0
- llama.cpp: https://github.com/ggml-org/llama.cpp
- Qwen3 GGUF: https://huggingface.co/Qwen/Qwen3-4B-GGUF
