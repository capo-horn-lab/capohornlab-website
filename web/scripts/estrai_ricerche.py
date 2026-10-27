#!/usr/bin/env python3
"""Genera le pagine delle ricerche del sito dall'inventario del motore (FREQ-SITO-3, Task 4).

Legge `inventario-ricerche.md` (sorgente unica) e per ogni scheda classificata OK o
"OK con avvertenza" scrive `<id>.md` (+ `<id>.dati.json` quando esiste una tabella strutturata)
in `web/src/content/ricerche/`, piu' `indice.json`. Schede NO / da verificare: nessun file.

Regole (vincolanti; "nulla di inventato": meno contenuto e' sempre accettabile, mai contenuto in piu'):
- i numeri sono COPIATI dal testo dell'inventario: lo script non calcola, non arrotonda, non parafrasa;
- ogni riga della tabella "Esito" ha una colonna Fonte (ledger `docs/EXECUTION_LEDGER.md#La-Lb` e/o prova);
  una riga con un numero che non si ritrova nella fonte citata NON si pubblica: la pagina dice soltanto
  quante righe non sono riportate. Si ammette solo il recupero entro 3 righe dall'intervallo citato dal
  registro (stesso numero e stesse parole), con la Fonte alla riga vera. Lato fonte i numeri si leggono come
  in tabella (un orario e' un token, numeri a confine di parola, k/n sono due numeri) e la Fonte e' la riga
  dove numero e parole stanno insieme, la migliore tra i candidati (non la prima con le stesse cifre);
- l'etichetta di verdetto e' la parola del registro (lista chiusa) trovata, in una frase di verdetto ancorata,
  nelle righe di ledger citate dalla pagina (con l'ID davanti nelle schede con piu' studi); se non c'e',
  "senza verdetto nel registro". Ritiro/correzione dell'audit: campo `audit`, a parte;
- niente istruzioni di lavoro dell'inventario ("pubblicare solo...", "citare..."): si tengono le clausole fattuali;
- pagine ritirate: banner e motivo dal registro, senza i numeri ritirati;
- LIMALL-1 e OPT-COND-1 (senza esito chiuso) non compaiono da nessuna parte;
- prova citata e assente su disco: "prova non trovata su disco: <percorso>";
- deterministico: stesso input, stessi byte (LF).

Solo libreria standard. Uso:
  .venv\\Scripts\\python.exe web/scripts/estrai_ricerche.py [--inventario P] [--root R] [--out D] [--limit N]
"""
import argparse
import json
import re
import sys
import unicodedata
from functools import lru_cache
from math import ceil
from pathlib import Path

INVENTARIO = r"C:\Users\farne\TradingAgent-NinjaTrader\runtime\proofs\freqsito3\inventario-ricerche.md"
RADICE = r"C:\Users\farne\TradingAgent-NinjaTrader"
USCITA = Path(__file__).resolve().parent.parent / "src" / "content" / "ricerche"
LEDGER = "docs/EXECUTION_LEDGER.md"
SUMMARY = "runtime/research/sa-report/summary.json"
MAX_RIGHE_DATI = 150
MAX_BYTE_PROVA = 12_000_000
MARGINE_LEDGER = 3  # righe oltre l'intervallo citato in cui si accetta ancora un numero (con le parole sulla stessa riga)
SEZIONE_DOC = 12  # in un documento: righe sopra il numero in cui cercare l'intestazione della sezione/tabella con le parole
SENZA_VERDETTO = "senza verdetto nel registro"

FRONTMATTER = ("id", "titolo", "data", "strumenti", "finestra", "verdetto",
               "pubblicabilita", "avvertenza", "fonte_ledger", "prove")

# Studi elencati nelle schede ma senza esito chiuso nel ledger: non compaiono da nessuna parte
# (valore: pezzi di percorso delle loro prove, anch'esse escluse).
SENZA_ESITO = {
    "LIMALL-1": ("optfull_lim025", "optfull_lim05", "optfull_barra"),
    "OPT-COND-1": ("optcond",),
}

STRUMENTI = ("MES", "MNQ", "M2K", "MYM", "MCL", "MGC", "M6E", "MBT", "ES", "NQ", "RTY", "CL", "ZN",
             "SPY", "QQQ", "IWM", "DIA", "TLT", "IEF", "GLD", "SLV", "USO", "UNG", "UUP", "FXE", "FXY",
             "SPX", "NDX", "VIX", "VX", "BTC", "ETH", "FESX", "FDXM", "FDXS", "FSXE")

# Parole di verdetto/esito scritte nel registro (docs/EXECUTION_LEDGER.md); lista chiusa. Ognuna compare nel
# registro (PASS, FAIL, CONFERMATA/O/I/E, NON CONFERMATA/O, RITIRATA, PARZIALE, BLOCKED_ENV, NOT_RUN, ADOTTATA/I/E,
# NON ADOTTATA, DESCRITTIVO); RITIRATO e' nella lista del controllore anche se oggi il registro scrive RITIRATA.
_PAROLA = (r"(?:NON\s+(?:CONFERMAT[AO]|ADOTTATA|[Cc]onfermat[ao]|[Aa]dottata)"
           r"|CONFERMAT[AOIE]|ADOTTAT[AIE]|PARZIALE|RITIRAT[AO]|DESCRITTIVO|PASS|FAIL|BLOCKED_ENV|NOT_RUN)")
PAROLE = re.compile(r"(?<![A-Za-z_])" + _PAROLA + r"(?![A-Za-z_])")

# Una parola e' un verdetto solo se ANCORATA a una frase di verdetto che il registro usa davvero (docs/EXECUTION_LEDGER.md):
#   "Esito X (runtime/proofs/x/x.json, run.log): NON confermato" (L8058, L8481, L8782), "Esito: BLOCKED_ENV" (L1653),
#   "Esito PASS, verdetto NON CONFERMATA ..." (L9721; "esito PAROLA" solo a inizio riga o di punto elenco: a meta' riga
#   sono frasi ipotetiche, L9282), "Verdetto: NON CONFERMATA" (L9247), "verdetto NON CONFERMATA" (L9309).
#   Famiglia A: "Esito ID (provenienza lunga come si vuole): PAROLA", con i due punti subito dopo la parentesi chiusa
#   (L8628, L9766). Famiglia B: "<ID della scheda> = PAROLA" (la forma dell'audit, L8968, L8969).
# Mai una parola preceduta da un conteggio ("3643 PASS", "0 FAIL", "0 CONFERMATE"), mai seguita da "se"/"quando"/"dopo"
# (definizione di rubrica), mai fuori da queste frasi. In dubbio: senza verdetto.
_FINE = r"(?![A-Za-z_])(?!\s+(?:solo\s+)?(?:se|quando|dopo)\b)"
_ID = r"[A-Z][A-Za-z0-9]*(?:-[A-Za-z0-9]+)+"
ANCORE = [re.compile(rx, fl) for rx, fl in (
    (r"(?i:\besito\b)(?:\s+(?P<id>" + _ID + r"))?[^\n;]{0,100}?:\s*\**\s*(?P<w>" + _PAROLA + r")" + _FINE, 0),
    (r"^[ \t]*(?:[-*>][ \t]*)*\**[ \t]*(?i:esito)\s+\**(?P<w>" + _PAROLA + r")" + _FINE, re.M),
    (r"(?i:\bverdetto\b)[^:\n;]{0,40}?:\s*\**\s*(?P<w>" + _PAROLA + r")" + _FINE, 0),
    (r"(?i:\bverdetto)\s+\**(?P<w>" + _PAROLA + r")" + _FINE, 0),
    (r"(?i:\boutcome\b)[^\n;]{0,40}?:\s*\**\s*(?P<w>" + _PAROLA + r")" + _FINE, 0),
)]
_A_INIZIO = re.compile(r"(?i:\besito\b)(?:\s+(?P<id>" + _ID + r"))?[^():;\n]{0,60}\(")
_A_FINE = re.compile(r"\s*:\s*\**\s*(?P<w>" + _PAROLA + r")" + _FINE)
# "PASS, NON CONFERMATA" (L9863): dopo un PASS/FAIL ancorato la catena con la virgola porta anche il verdetto di ricerca,
# mai un conteggio ("PASS, 2 CONFERMATE"), mai una definizione ("PASS, CONFERMATA se ..."), mai BLOCKED_ENV/NOT_RUN.
_A_CATENA = re.compile(r"\s*,\s*\**\s*(?P<w>NON\s+(?:CONFERMAT[AO]|ADOTTATA)|CONFERMAT[AOIE]|ADOTTAT[AIE]|PARZIALE)" + _FINE)


def _famiglia_a(testo):
    """(posizione, ID|None, parola) di "Esito [ID] (provenienza): PAROLA" con la parentesi lunga quanto serve."""
    for m in _A_INIZIO.finditer(testo):
        profondita, i = 1, m.end()
        while i < len(testo) and profondita and i - m.end() < 1500:
            profondita += (testo[i] == "(") - (testo[i] == ")")
            i += 1
        if profondita == 0 and (f := _A_FINE.match(testo, i)):
            yield f.start("w"), m.group("id"), f.group("w")
            if f.group("w") in ("PASS", "FAIL") and (c := _A_CATENA.match(testo, f.end("w"))):
                yield c.start("w"), m.group("id"), c.group("w")


def _famiglia_b(testo, ids):
    """(posizione, ID, parola) di "<ID> = PAROLA", solo per gli ID della scheda."""
    for i_d in ids:
        for m in re.finditer(r"(?<![\w-])" + re.escape(i_d) + r"\s*=\s*\**\s*(?P<w>" + _PAROLA + r")" + _FINE, testo):
            yield m.start("w"), i_d, m.group("w")


# Istruzioni di lavoro dell'inventario (non sono fatti sullo studio): le clausole che le contengono non si pubblicano.
ISTRUZIONI = re.compile("|".join([
    r"\bpubblicar\w*", r"\bpubblicabil\w*", r"\bripubblic\w*", r"\bridistribu\w*", r"\bcitar[ei]\b",
    r"\bdichiarar\w*", r"\briportar[ei]\b", r"\bincluder\w*", r"\bpresentar[ei]\b", r"\bchiarir\w*",
    r"\bserve prima\b", r"\bverificar[ei] (?:termini|diritti|la licenza)\b", r"\bvalutar[ei]\b", r"\bdescriver[ei]\b",
    r"\bda omettere\b", r"\brimandar[ei]\b", r"\brispettar[ei]\b", r"\bnon riprodurre\b",
    r"\bnon va(?:nno)? (?:pubblicat|ridistribuit|presentat|riprodott|usat)\w*",
    r"\bva pubblicat\w*", r"\bgli esiti numerici s[iì]\b", r"\bnulla da mostrare\b", r"\bcontiene riferimenti\b",
    r"\bNO per\b", r"\bsolo per gli indicatori\b", r"\bper il sito\b", r"\bstudio centrale\b",
    r"\badatt\w+ al sito\b", r"\bmolto utile\b", r"\bsenza clausole\b",
]), re.I)

ID_RE = re.compile(r"\b[A-Z][A-Za-z0-9]*(?:-[A-Za-z0-9]+)+\b|\b[A-Z]+\d+[A-Za-z]*\b")
RIF = r"L\d{3,5}(?:\s*-\s*L?\d{3,5})?"
RIF_SOLO = re.compile(rf"^(?:docs/EXECUTION_LEDGER\.md:)?({RIF})$")
RIF_NUDO = re.compile(rf"(?<![\w-])({RIF})(?![\w])")
PAREN = re.compile(r"\(([^()]*)\)")

# --- numeri: stesse regole di verifica_numeri.py (segno compreso): un numero e' verificato se compare come cifre ---
MENO = "\N{MINUS SIGN}"
OPERANDO = r"A-Za-z0-9_)\]}%"
OP = re.compile("[" + OPERANDO + "]")
NUMERO = re.compile(
    r"(?P<v>\d{4}-\d{2}-\d{2}|\d{1,2}:\d{2}(?::\d{2})?)"
    # un numero comincia a confine di parola ("p95" non da' "5", "DSR1000" non da' "000"); "2.1.0" e' un token solo
    r"|(?:(?<![" + OPERANDO + r"])(?P<s>[-" + MENO + r"]))?(?<![A-Za-z_])(?<![A-Za-z]-)(?<!\d)"
    r"(?P<n>\d{1,3}(?:[.,]\d{3})+(?:[.,]\d+)?(?!\d)|\d+(?:\.\d+){2,}(?!\d)|\d+(?:[.,]\d+)?)"
)


def numeri(testo):
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", testo).replace("`", "").replace("*", "")
    return [m.group("v") or ("-" if m.group("s") else "") + m.group("n") for m in NUMERO.finditer(t)]


def varianti(tok):
    v = {tok, tok.replace(",", ".")}
    if re.fullmatch(r"[1-9]\d{0,2}(?:[.,]\d{3})+", tok):
        v.add(re.sub(r"[.,]", "", tok))
    if re.fullmatch(r"[1-9]\d{0,2}(?:\.\d{3})+,\d+", tok):
        v.add(tok.replace(".", "").replace(",", "."))
    return v


@lru_cache(maxsize=8192)
def _numeri_fonte(testo):
    """I numeri di un testo di fonte come (negativo, cifre), con la stessa tokenizzazione delle righe di tabella:
    un orario (20:47) e' un token solo, i numeri cominciano a confine di parola, k/n (30/69) sono due numeri."""
    return frozenset((t.startswith("-"), t.lstrip("-")) for t in numeri(testo))


def ha_numero(tok, testo):
    """Il numero (stesso segno) e' uno dei numeri della fonte; mai cifre dentro un orario, un codice o un numero piu' lungo."""
    neg, num = tok.startswith("-"), tok.lstrip("-")
    presenti = _numeri_fonte(testo)
    return any((neg, v) in presenti for v in varianti(num))


def normalizza(t):
    t = unicodedata.normalize("NFKD", t.lower())
    return "".join(c for c in t if not unicodedata.combining(c)).replace("'", " ")


def parole_riga(testo):
    return {normalizza(w) for w in re.findall(r"[A-Za-zÀ-ÿ]{4,}", testo)}


def hanno_le_parole(parole, finestra):
    """Almeno il 40% (minimo una) delle parole della riga compare nella finestra di testo."""
    if not parole:
        return False
    f = normalizza(finestra)
    return sum(1 for p in parole if p in f) >= max(1, ceil(0.4 * len(parole)))


# --- frontmatter ---
def frontmatter_testo(fm):
    righe = ["---"]
    for k, v in fm.items():
        if isinstance(v, list):
            righe.append(f"{k}:" if v else f"{k}: []")
            righe += [f"  - {json.dumps(x, ensure_ascii=False)}" for x in v]
        else:
            righe.append(f"{k}: {json.dumps(v, ensure_ascii=False)}")
    righe.append("---")
    return "\n".join(righe)


def leggi_frontmatter(testo):
    """-> (dict, corpo). Legge il formato scritto da frontmatter_testo (valori JSON, liste a blocco)."""
    righe = testo.split("\n")
    fine = righe.index("---", 1)
    fm, chiave = {}, None
    for r in righe[1:fine]:
        m = re.match(r"^([A-Za-z_]\w*):\s*(.*)$", r)
        if m:
            chiave = m.group(1)
            fm[chiave] = json.loads(m.group(2)) if m.group(2) else []
        elif chiave and (m := re.match(r"^\s+-\s+(.*)$", r)):
            fm[chiave].append(json.loads(m.group(1)))
    return fm, "\n".join(righe[fine + 1:])


# --- lettura dell'inventario ---
def leggi_inventario(testo):
    sez, schede, ritiri, cur = "", [], [], None
    for n, r in enumerate(testo.split("\n"), 1):
        if r.startswith("## "):
            sez, cur = r[3:].strip(), None
            continue
        if sez.startswith("Ritiri"):
            if m := re.match(r"^\d+\.\s+(.*)$", r):
                ritiri += leggi_ritiro(m.group(1))
        elif sez.startswith("Schede studio"):
            if r.startswith("### "):
                cur = {"titolo": r[4:].strip(), "riga": n, "voci": {}}
                schede.append(cur)
            elif cur is not None and (m := re.match(r"^\|\s*(\d)\.\s*[^|]*?\|\s*(.*?)\s*\|\s*$", r)):
                cur["voci"][int(m.group(1))] = m.group(2)
    esclusi = {Path(p).name for r in ritiri for p in r["non_usare"]}
    for s in schede:
        completa_scheda(s)
        s["audit"] = [r for r in ritiri if set(r["ids"]) & set(s["ids"])]
        # `ritirato` solo per gli ID che la sezione dell'inventario dichiara ritirati; per gli altri una nota dell'audit
        s["ritirati"] = [i for i in s["ids"] if any(i in r["ids"] for r in s["audit"] if r["tipo"] == "ritirato")]
        s["audit_stato"] = "ritirato" if s["ritirati"] else "nota" if s["audit"] else ""
        s["audit_id"] = s["ritirati"] or [i for i in s["ids"] if any(i in r["ids"] for r in s["audit"])]
        s["file_esclusi"] = esclusi
    return schede, ritiri


def leggi_ritiro(item):
    out = []
    for sub in re.split(r";\s+(?=\*\*)", item):
        ids = ID_RE.findall(" ".join(re.findall(r"\*\*(.+?)\*\*", sub)))
        testo = sub.replace("**", "").strip()
        tipo = "ritirato" if re.search("ritirat", testo, re.I) else "nota"  # l'audit non dice "corretto": nessuna deduzione
        non_usare = re.findall(r"`([^`]+\.(?:json|csv|md|txt))`[^.;]{0,30}\bnon usare\b", testo)
        out.append({"ids": ids, "testo": testo, "tipo": tipo, "non_usare": non_usare})
    return out


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def completa_scheda(s):
    v = s["voci"]
    testa = s["titolo"].split(" — ")[0]
    s["ids"] = ID_RE.findall(testa)
    s["id"] = slug(s["ids"][0] if s["ids"] else testa[:40])
    p = v.get(6, "").strip()
    if re.match(r"NO\b", p):
        s["pubblicabilita"], s["avvertenza"] = "no", ""
    elif m := re.match(r"OK\s+con\s+avvertenza\s*(FORTE)?\s*:?\s*(.*)$", p, re.I | re.S):
        s["pubblicabilita"] = "avvertenza"
        s["avvertenza"] = (("Avvertenza forte: " if m.group(1) else "") + m.group(2)).strip()
    elif re.match(r"OK\b", p):
        s["pubblicabilita"], s["avvertenza"] = "ok", ""
    else:
        s["pubblicabilita"], s["avvertenza"] = "da_verificare", ""
    ident = v.get(1, "")
    m = re.match(r"^(?:Date\s+)?(\d{1,2})(?:-\d{1,2})?/(\d{2})/(\d{4})", ident)
    s["data"] = f"{m.group(3)}-{m.group(2)}-{int(m.group(1)):02d}" if m else ""
    resto = ident[m.end():].lstrip(" ;:") if m else ident
    mq = re.search(r"\b(?:domanda|domande)\b[^:]{0,80}:\s*", resto, re.I)
    if mq:
        s["finestra"], s["domanda"] = resto[:mq.start()].strip(" ;"), resto[mq.end():].strip()
    else:
        s["finestra"], s["domanda"] = resto.strip(), resto.strip()
    pre = s["finestra"]
    pos = {t: m.start() for t in STRUMENTI if (m := re.search(rf"(?<![A-Za-z0-9]){t}(?![A-Za-z0-9])", pre))}
    s["strumenti"] = sorted(pos, key=pos.get)


# --- testo: segmentazione, riferimenti, istruzioni, studi esclusi ---
ABBREVIAZIONE = re.compile(r"(?<![A-Za-zÀ-ÿ])(?:es|ecc|cfr|vs|sez|fig)$", re.I)


def _spans(testo):
    """Intervalli (inizio, fine) dei segmenti: ';' e fine frase fuori da parentesi e virgolette. I frammenti senza
    soggetto ("1 -2,84", "q 0,025", "es.") si uniscono al precedente."""
    out, inizio, depth, citato, i, n = [], 0, 0, False, 0, len(testo)
    while i < n:
        c = testo[i]
        if c == '"':
            citato = not citato
            if not citato and testo[i - 1:i] == "." and testo[i + 1:i + 2] == " " \
                    and re.match(r"[A-ZÀ-Ý]", testo[i + 2:i + 3] or " "):  # frase che finisce dentro la citazione
                out.append((inizio, i + 1))
                inizio, i = i + 2, i + 1
        elif not citato:
            if c in "([{":
                depth += 1
            elif c in ")]}":
                depth = max(0, depth - 1)
            elif depth == 0 and testo[i + 1:i + 2] == " ":
                if c == ";" or (c == "." and re.match(r'["A-ZÀ-Ý]', testo[i + 2:i + 3] or " ")
                                and not ABBREVIAZIONE.search(testo[:i])):
                    out.append((inizio, i if c == ";" else i + 1))
                    inizio, i = i + 2, i + 1
        i += 1
    out.append((inizio, n))
    merged = []
    for s, e in (x for x in out if testo[x[0]:x[1]].strip()):
        # soggetto = una parola di 3 lettere nei primi 14 caratteri, o un codice con la maiuscola (R1a, TT, M2K)
        if merged and not (re.search(r"[A-Za-zÀ-ÿ]{3,}", testo[s:s + 14])
                           or re.match(r"\W*[A-ZÀ-Ý][A-Za-z0-9À-ÿ_-]+", testo[s:e])):
            merged[-1] = (merged[-1][0], e)
        else:
            merged.append((s, e))
    return merged


def segmenta(testo):
    return [testo[s:e].strip() for s, e in _spans(testo)]


def unisci(segmenti):
    out = ""
    for seg in segmenti:
        out += ("" if not out else " " if out.endswith(".") else "; ") + seg
    return out


def estrai_riferimenti(testo):
    """-> (testo senza citazioni, [(a, b)] righe del ledger, [citazioni di documenti])."""
    refs, docs = [], []

    def intervallo(t):
        a, b = re.findall(r"\d+", t)[0], re.findall(r"\d+", t)[-1]
        refs.append((int(a), int(b)))

    def paren(m):
        parti = [p.strip() for p in re.split(r"\s*[;,]\s*", m.group(1))]
        if not any(RIF_SOLO.match(p) or re.match(r"[\w./-]+\.(?:txt|md|json)\b", p) for p in parti):
            return m.group(0)
        resto = []
        for p in parti:
            if mm := RIF_SOLO.match(p):
                intervallo(mm.group(1))
            elif re.match(r"[\w./-]+\.(?:txt|md|json)\b", p):
                docs.append(p)
            else:
                resto.append(p)
        return f"({', '.join(resto)})" if resto else ""

    t = PAREN.sub(paren, testo)
    t = RIF_NUDO.sub(lambda m: (intervallo(m.group(1)), "")[1], t)
    t = re.sub(r"\(\s*[,;]?\s*\)", "", t)
    t = re.sub(r"\s+([.,;:])", r"\1", t)
    t = re.sub(r"\s{2,}", " ", t).strip()
    return t, refs, docs


def cella(t):
    return t.replace("|", "\\|")


def prefisso_fattuale(s):
    """Di una clausola con istruzioni, la parte iniziale fino a una virgola o a due punti (fuori da parentesi e virgolette)
    se non ha istruzioni e regge da sola (almeno 3 parole, non comincia con "non", "ma", "e"...); altrimenti ''."""
    depth, citato, prefisso = 0, False, ""
    for i, c in enumerate(s):
        if c == '"':
            citato = not citato
        elif not citato:
            depth += (c in "([{") - (c in ")]}")
            if depth == 0 and c in ",:":
                if ISTRUZIONI.search(s[:i]):
                    break
                prefisso = s[:i]
    ok = (len(re.findall(r"[A-Za-zÀ-ÿ]{3,}", prefisso)) >= 3
          and not re.match(r"\W*(?:non|ma|e|o|con|senza|solo|quindi|cioe')\b", prefisso, re.I))
    return prefisso.strip(" ,:;") if ok else ""


def pulisci_clausola(seg):
    """Toglie le parentesi con istruzioni; di una clausola con istruzioni resta solo il prefisso fattuale (o niente)."""
    s = PAREN.sub(lambda m: "" if ISTRUZIONI.search(m.group(1)) else m.group(0), seg)
    s = re.sub(r"\s+([.,;:])", r"\1", re.sub(r"\s{2,}", " ", s)).strip()
    if ISTRUZIONI.search(s):
        s = prefisso_fattuale(s)
    return s if re.search(r"\w", s) else ""


def senza_istruzioni(testo):
    t = testo.strip()
    if (m := re.fullmatch(r"\((.*)\)\.?", t, re.S)) and m.group(1).count("(") == m.group(1).count(")"):
        t = m.group(1)
    segs = segmenta(t)
    puliti = [pulisci_clausola(x) for x in segs]
    return testo if puliti == segs else unisci([c for c in puliti if c])  # intatto se non c'e' nulla da togliere


def cita_escluso(testo):
    return any(i in testo or any(h in testo for h in hint) for i, hint in SENZA_ESITO.items())


def togli_esclusi(testo, fino_a_fine=False):
    """Toglie le clausole che citano LIMALL-1 / OPT-COND-1 (o le loro prove); con `fino_a_fine` anche tutto cio' che segue."""
    if not cita_escluso(testo):
        return testo
    segs, out = segmenta(testo), []
    for i, seg in enumerate(segs):
        if cita_escluso(seg):
            if fino_a_fine:
                break
            continue
        out.append(seg)
    return unisci(out)


CODA = re.compile(rf"\s*\(((?:docs/EXECUTION_LEDGER\.md:)?{RIF}(?:\s*[;,]\s*(?:docs/EXECUTION_LEDGER\.md:)?{RIF})*)\)\.?\s*$")


def separa_coda(testo):
    """Citazione condivisa in coda alla cella, "(L9161, L10178)": -> (testo senza coda, coda o '')."""
    m = CODA.search(testo)
    return (testo[:m.start()], m.group(1)) if m else (testo, "")


def citazioni_cella(esito, con_esclusi):
    """-> (righe di ledger, documenti) citati dalla cella. Se la scheda ha uno studio escluso, le citazioni delle
    clausole che lo nominano non contano (restano quelle in coda, che valgono per tutta la cella)."""
    if not con_esclusi:
        _, refs, docs = estrai_riferimenti(esito)
        return refs, docs
    corpo, coda = separa_coda(esito)
    refs, docs = [], []
    for seg in segmenta(corpo):
        if not any(i in seg for i in SENZA_ESITO):
            _, r, d = estrai_riferimenti(seg)
            refs, docs = refs + r, docs + d
    _, r, d = estrai_riferimenti(f"({coda})") if coda else ("", [], [])
    return refs + r, docs + d


def titolo_senza_esclusi(titolo):
    for i in SENZA_ESITO:
        e = re.escape(i)
        titolo = re.sub(rf"\s*(?:/|,|\+|\be\b)\s*{e}", "", titolo)
        titolo = re.sub(rf"{e}\s*(?:/|,|\+|\be\b)\s*", "", titolo)
        titolo = re.sub(rf"{e}\s*", "", titolo)
    return titolo.strip()


# --- contesto: ledger, prove, summary ---
class Raw(str):
    """Numero JSON con le cifre come scritte nel file."""


def _foglie(o, out):
    """Insiemi di foglie scalari (numeri grezzi e stringhe) per ogni oggetto/lista: i 'record' di un JSON."""
    figli = o.values() if isinstance(o, dict) else o
    scalari = [v for v in figli if isinstance(v, str)]
    if scalari:
        out.append(scalari)
    for v in figli:
        if isinstance(v, (dict, list)):
            _foglie(v, out)


class Contesto:
    def __init__(self, radice):
        self.radice = Path(radice)
        f = self.radice / LEDGER
        self.ledger = f.read_text(encoding="utf-8", errors="replace").split("\n") if f.is_file() else []
        self._testi, self._record = {}, {}
        self.contenuti = {}
        self.esiti = {}
        s = self.radice / SUMMARY
        if s.is_file():
            try:
                for g in json.loads(s.read_text(encoding="utf-8")).get("esiti", []):
                    self.esiti.setdefault(g["id"].split()[0], []).append(g)
            except (ValueError, OSError, KeyError):
                self.esiti = {}

    def righe_ledger(self, a, b):
        return "\n".join(self.ledger[a - 1:b])

    def testo(self, rel):
        if rel not in self._testi:
            f = self.radice / rel
            ok = f.is_file() and f.suffix.lower() in (".json", ".md", ".txt", ".log") and f.stat().st_size <= MAX_BYTE_PROVA
            self._testi[rel] = f.read_text(encoding="utf-8", errors="replace") if ok else ""
        return self._testi[rel]

    def record(self, rel):
        """Record di un JSON di prova: liste di foglie (numeri grezzi come `Raw`, stringhe) per ogni oggetto/lista."""
        if rel not in self._record:
            out = []
            try:
                o = json.loads(self.testo(rel) or "null", parse_float=Raw, parse_int=Raw)
                if isinstance(o, (dict, list)):
                    _foglie(o, out)
            except ValueError:
                pass
            self._record[rel] = out
        return self._record[rel]

    def documento(self, nome):
        base = nome.split()[0]
        if "/" in base:
            return base if (self.radice / base).is_file() else None
        trovati = sorted((self.radice / "docs").rglob(base)) if (self.radice / "docs").is_dir() else []
        return trovati[0].relative_to(self.radice).as_posix() if trovati else None


def record_ha(foglie, tok):
    neg, num = tok.startswith("-"), tok.lstrip("-")
    var = varianti(num)
    for f in foglie:
        if isinstance(f, Raw):
            if f.lstrip("-") in var and f.startswith("-") == neg:
                return True
        elif f in varianti(tok):
            return True
    return False


# --- prove ---
def espandi(tok):
    m = re.search(r"\{([^{}]*)\}", tok)
    if not m:
        return [tok]
    out = []
    for item in m.group(1).split(","):
        item = item.strip()
        for x in espandi(tok[:m.start()] + (item.split()[0] if item else "") + tok[m.end():]):
            if x not in out:
                out.append(x)
    return out


RADICI = ("runtime/", "docs/", "ninjatrader/", "src/", "scripts/", "tests/", "config/")
# cartelle madri citate a parole ("nessun file in `runtime/proofs/`"), non prove
RADICI_GENERICHE = {"runtime", "runtime/proofs", "runtime/research", "docs", "docs/research"}


def percorsi_prove(cella_prove, radice, file_esclusi=()):
    """-> ([(percorso, tipo)], [fuori repo]); tipo: file | cartella | schema. `file_esclusi`: nomi da non usare."""
    out, fuori, ultima = [], [], ""
    for tok in re.findall(r"`([^`]+)`", cella_prove):
        for p in espandi(tok.strip()):
            p = p.replace("\\", "/").rstrip(",;")
            if not p:
                continue
            if re.match(r"^[A-Za-z]:/", p) or p.startswith("/") or p.startswith("Engine/"):
                fuori.append(p)
                continue
            if not p.startswith(RADICI):
                prima = p.split("/")[0]
                if "/" in p and (radice / "runtime/proofs" / prima).exists():
                    p = "runtime/proofs/" + p
                else:
                    ext = "." in p.rsplit("/", 1)[-1].replace("..", "")
                    cand = [ultima + "/" + p if ultima else p, ultima.rsplit("/", 1)[0] + "/" + p if "/" in ultima else p,
                            "runtime/proofs/" + p]
                    p = next((c for c in cand if (radice / c.rstrip("/")).exists()), cand[0] if ext else cand[2])
            if p.rsplit("/", 1)[-1] in file_esclusi:
                continue
            if p.endswith("/") or "*" in p or "<" in p or ".." in p.rsplit("/", 1)[-1]:
                out.append((p, "cartella" if p.endswith("/") else "schema"))
            else:
                out.append((p, "cartella" if (radice / p).is_dir() else "file"))
            if "/" in p and not p.endswith("/"):
                ultima = p.rsplit("/", 1)[0]
            elif p.endswith("/"):
                ultima = p.rstrip("/")
    visti = []
    for x in out:
        if x not in visti:
            visti.append(x)
    return visti, fuori


def esiste(p, tipo, radice):
    if tipo == "schema":
        nome = p.rsplit("/", 1)[-1]
        padre = radice / p.rsplit("/", 1)[0] if "/" in p else radice
        if ".." in nome:
            return padre.is_dir()
        return bool(list(padre.glob(re.sub(r"<[^>]*>", "*", nome)))) if padre.is_dir() else False
    return (radice / p.rstrip("/")).exists()


# --- righe dell'esito ---
def ancora(a, b):
    return f"{LEDGER}#L{a}-L{b}"


def punteggio(riga, toks, parole):
    """(quanti numeri della riga di tabella stanno in questa riga della fonte, quante parole): serve a scegliere la riga
    vera tra piu' candidati, invece del primo posto in cui compaiono le stesse cifre."""
    n = normalizza(riga)
    return (sum(1 for t in toks if ha_numero(t, riga)), sum(1 for p in parole if p in n))


def riga_ledger_con(ctx, tok, lo, hi, parole, toks=()):
    """Riga (1-based) tra lo e hi che porta il numero E le parole del testo (sulla stessa riga), la migliore per
    `punteggio` (a parita' la prima); None se non c'e'."""
    migliore = None
    for n in range(max(1, lo), min(len(ctx.ledger), hi) + 1):
        r = ctx.ledger[n - 1]
        if ha_numero(tok, r) and hanno_le_parole(parole, r):
            p = punteggio(r, toks or (tok,), parole)
            if migliore is None or p > migliore[0]:
                migliore = (p, n)
    return migliore[1] if migliore else None


def righe_esito(esito, refs_cella, docs_cella, ctx, prove_file, ritirati=(), ids=()):
    """-> (righe pubblicate [{testo, fonte, ancore}], numero di righe non riportate).

    La Fonte di un numero e' la posizione in cui il numero E le parole della riga stanno insieme, scelta tra i candidati
    nell'ordine: (1) righe di ledger citate, sulla stessa riga; (2) entro 3 righe dall'intervallo citato, sulla stessa
    riga (Fonte = la riga vera); (3) documento citato, nella stessa sezione/tabella; (4) righe di ledger citate dove il
    numero c'e' ma le parole no (citato cosi' dall'inventario); (5) file di prova JSON, solo se tutti i numeri
    restanti sono valori dello stesso record. Altrimenti la riga non si pubblica. Il numero e' sempre un token intero
    (non cifre dentro un orario, un codice o un numero piu' lungo)."""
    segs = segmenta(esito)
    if ritirati:
        segs = senza_ritirati(segs, ids, ritirati)
    ok, non = [], 0
    for seg in segs:
        testo, refs, docs = estrai_riferimenti(seg)
        if not testo or not re.search(r"\w", testo) or ISTRUZIONI.search(testo):
            continue
        proprie = [r for r in dict.fromkeys(refs) if 0 < r[0] <= r[1] <= len(ctx.ledger)]
        primarie = proprie or refs_cella
        fonti = [(ancora(a, b), ctx.righe_ledger(a, b)) for a, b in primarie]
        elenco_docs = [d for d in dict.fromkeys([ctx.documento(x) for x in docs] + list(docs_cella)) if d]
        parole = parole_riga(testo)
        usate, resto = [], []  # in Fonte solo dove i numeri si ritrovano davvero (senza numeri: le citazioni della riga)
        toks = numeri(testo)
        for tok in toks:
            # Candidati (punteggio, fonte): (1) righe di ledger citate, (2) se non ce ne sono, entro 3 righe dall'intervallo,
            # (3) righe dei documenti citati (la riga vera, es. TEORIA_MOVIMENTO riga 58, non il file intero). Vince il
            # punteggio piu' alto (piu' numeri della riga di tabella sulla stessa riga, poi piu' parole), a parita' il primo.
            cand = [(punteggio(r, toks, parole), (nome, t)) for (a, b), (nome, t) in zip(primarie, fonti)
                    for r in ctx.ledger[a - 1:b] if ha_numero(tok, r) and hanno_le_parole(parole, r)]
            if not cand:
                for a, b in primarie:
                    if n := riga_ledger_con(ctx, tok, a - MARGINE_LEDGER, b + MARGINE_LEDGER, parole, toks):
                        cand.append((punteggio(ctx.ledger[n - 1], toks, parole), (ancora(n, n), ctx.ledger[n - 1])))
                        break
            for d in elenco_docs:
                righe_doc = ctx.testo(d).split("\n")
                cand += [(punteggio(r, toks, parole), (f"{d}#L{i + 1}-L{i + 1}", r)) for i, r in enumerate(righe_doc)
                         if ha_numero(tok, r) and hanno_le_parole(
                             parole, "\n".join(righe_doc[max(0, i - SEZIONE_DOC):i + MARGINE_LEDGER + 1]))]
            scelta = max(enumerate(cand), key=lambda e: (e[1][0], -e[0]))[1][1] if cand else None
            if not scelta:
                scelta = next(((n, t) for n, t in fonti if ha_numero(tok, t)), None)
            if not scelta:
                resto.append(tok)
            elif all(u[0] != scelta[0] for u in usate):
                usate.append(scelta)
        if resto:  # (5) prova JSON: tutti i numeri restanti come valori di uno stesso record
            for p in prove_file:
                if p.endswith(".json") and any(all(record_ha(rec, t) for t in resto) for rec in ctx.record(p)):
                    usate.append((p, ""))
                    resto = []
                    break
        if resto:
            non += 1
            continue
        scelte = usate or fonti
        ancore = [tuple(int(x) for x in re.findall(r"\d+", n.split("#")[1])) for n, _ in scelte if n.startswith(LEDGER + "#")]
        ok.append({"testo": testo, "fonte": " · ".join(n for n, _ in scelte) or "—", "ancore": ancore})
    return ok, non


def senza_ritirati(segs, ids, ritirati):
    """Toglie le righe dei soli studi ritirati dall'audit; restano quelle dell'audit (RITIRAT*) e degli altri studi."""
    if not ids:
        return segs
    ordine = sorted(ids, key=len, reverse=True)
    rx = re.compile(r"^\W*(" + "|".join(re.escape(i) for i in ordine) + r")(?![\w-])")
    out, proprietario = [], ids[0]
    for seg in segs:
        if m := rx.match(seg):
            proprietario = m.group(1)
        if re.search("RITIRAT", seg) or proprietario not in ritirati:
            out.append(seg)
    return out


def parole_registro(ctx, ancore, ids=()):
    """Parole di verdetto del registro (lista chiusa) nelle righe di ledger indicate, SOLO se ancorate a una frase di
    verdetto del registro (ANCORE e famiglie A/B), una volta ciascuna. In una scheda con piu' ID, quando la frase nomina
    uno degli ID della scheda la parola porta l'ID ("OVN-1: confermati · GOLDN-1: non confermato"); le voci sono nell'ordine
    degli ID della scheda (prima quelle senza ID), poi in quello in cui compaiono."""
    ids = tuple(i for i in ids if i not in SENZA_ESITO)
    con_id = len(ids) > 1
    viste, ordine = {}, 0
    for a, b in ancore:
        testo = ctx.righe_ledger(a, b)
        trovate = [(m.start("w"), m.groupdict().get("id"), m.group("w")) for rx in ANCORE for m in rx.finditer(testo)]
        trovate += list(_famiglia_a(testo)) + (list(_famiglia_b(testo, ids)) if ids else [])
        for _, i_d, w in sorted(trovate, key=lambda t: t[0]):
            if i_d and ids and i_d not in ids:
                continue  # la frase nomina un altro studio (un fratello, o uno escluso): non e' il verdetto di questa scheda
            voce = (i_d if con_id and i_d in ids else None, re.sub(r"\s+", " ", w).lower())
            if voce not in viste:
                viste[voce] = ordine
                ordine += 1
    voci = sorted(viste, key=lambda v: (ids.index(v[0]) if v[0] else -1, viste[v]))
    return " · ".join(f"{i}: {w}" if i else w for i, w in voci) or SENZA_VERDETTO


# --- dati strutturati per i grafici ---
ANNO = re.compile(r"^(?:19|20)\d{2}$")


def _numero(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def trova_serie(o, punto="", livello=0):
    """Primo dizionario {anno: numero} (>= 3 anni) di un JSON di prova -> (puntatore, chiave, righe)."""
    if livello > 3 or not isinstance(o, dict):
        return None
    ks = list(o)
    if len(ks) >= 3 and all(ANNO.match(str(k)) for k in ks) and all(_numero(v) for v in o.values()):
        return punto, punto.rsplit("/", 1)[-1], [[str(k), o[k]] for k in sorted(ks, key=str)]
    for k, v in o.items():
        if (r := trova_serie(v, f"{punto}/{k}", livello + 1)):
            return r
    return None


def dati_scheda(s, ctx, prove_file):
    """-> (dati|None, didascalia). Serie annuale da una prova JSON; altrimenti tabella dei test da summary.json."""
    for p in prove_file:
        f = ctx.radice / p
        if f.suffix == ".json" and f.stat().st_size <= 400_000:
            try:
                r = trova_serie(json.loads(f.read_text(encoding="utf-8")))
            except ValueError:
                continue
            if r:
                punto, chiave, righe = r
                cont = ctx.contenuti.get(p, "")
                return ({"tipo": "serie", "colonne": ["anno", chiave], "righe": righe, "fonte": f"{p}#{punto}"},
                        f"Serie per anno dal file di prova {p} (chiave {chiave})."
                        + (f" Contenuto del file secondo l'inventario: {cont}" if cont else ""))
    gruppi = []
    for i in s["ids"]:
        if i in SENZA_ESITO:
            continue
        gruppi += ctx.esiti.get(i, [])
    righe = [(g["id"], r) for g in gruppi for r in g["righe"]]
    if not righe or len(righe) > MAX_RIGHE_DATI:
        return None, ""
    colonne = []
    for _, r in righe:
        colonne += [k for k in r if k not in colonne]
    molti = len({g for g, _ in righe}) > 1
    cols = (["studio"] if molti else []) + colonne
    return ({"tipo": "tabella", "colonne": cols,
             "righe": [([g] if molti else []) + [r.get(c) for c in colonne] for g, r in righe],
             "fonte": SUMMARY},
            f"Test della scheda dal file {SUMMARY} (r riga, n campioni, m media nell'unita' u, t statistica t, "
            "p95 p95 dei placebo, ok = esito della rubrica; definizione delle colonne in runtime/research-scripts/sa_data.py).")


def leggi_contenuti(testo):
    """Appendice C.1 dell'inventario: percorso -> contenuto del file."""
    out = {}
    for r in testo.split("\n"):
        if m := re.match(r"^\|\s*`([^`]+)`\s*\|\s*(.*?)\s*\|\s*[\d.,]+ [KMB]+\s*\|", r):
            out[m.group(1)] = m.group(2)
    return out


def dump_dati(d):
    righe = ",\n".join("  " + json.dumps(r, ensure_ascii=False) for r in d["righe"])
    return (f'{{\n "tipo": {json.dumps(d["tipo"])},\n "colonne": {json.dumps(d["colonne"], ensure_ascii=False)},\n'
            f' "righe": [\n{righe}\n ],\n "fonte": {json.dumps(d["fonte"])}\n}}\n')


# --- pagina ---
def pulito(testo, esclusi=False):
    """Testo di prosa senza citazioni dei file ne' istruzioni di lavoro ne' studi esclusi."""
    return senza_istruzioni(togli_esclusi(testo, fino_a_fine=esclusi))


def pagina(s, ctx):
    """-> (testo md, frontmatter, dati|None, stats). Solleva ValueError per le schede non pubblicabili."""
    if s["pubblicabilita"] not in ("ok", "avvertenza"):
        raise ValueError(f"scheda {s['id']}: pubblicabilita '{s['pubblicabilita']}', nessuna pagina")
    v = s["voci"]
    esclusi = [i for i in s["ids"] if i in SENZA_ESITO]
    percorsi, fuori = percorsi_prove(v.get(5, ""), ctx.radice, s.get("file_esclusi", ()))
    percorsi = [(p, t) for p, t in percorsi if p.rstrip("/") not in RADICI_GENERICHE
                and not any(h in p for hint in SENZA_ESITO.values() for h in hint)]
    stato = [(p, t, esiste(p, t, ctx.radice)) for p, t in percorsi]
    prove_file = [p for p, t, e in stato if t == "file" and e]
    mancanti = [p for p, t, e in stato if not e]
    esito_orig = v.get(3, "")
    refs, docs = citazioni_cella(esito_orig, bool(esclusi))
    refs = [r for r in dict.fromkeys(refs) if 0 < r[0] <= r[1] <= len(ctx.ledger)]
    docs = [d for d in (ctx.documento(x) for x in docs) if d]
    esito = togli_esclusi(separa_coda(esito_orig)[0] if esclusi else esito_orig, fino_a_fine=bool(esclusi))
    ok, non = righe_esito(esito, refs, docs, ctx, prove_file, s["ritirati"], s["ids"])
    ritirata = s["audit_stato"] == "ritirato"
    # pagina ritirata: il locatore principale e' la riga dell'audit che ritira lo studio, non le righe degli altri studi
    audit_rif = next((r for a in s["audit"] if a["tipo"] == "ritirato" for r in estrai_riferimenti(a["testo"])[1]
                      if 0 < r[0] <= r[1] <= len(ctx.ledger)), None)
    prima = (audit_rif or (ok[0]["ancore"][0] if ok and ok[0]["ancore"] else None) or (refs[0] if refs else None)
             ) if ritirata else refs[0] if refs else None
    fonte_ledger = ancora(*prima) if prima else ""
    # il verdetto e' scritto nel locatore principale della scheda (`fonte_ledger`): le parole delle altre righe citate
    # (rubriche, esiti di altri studi) non sono verdetti della pagina
    verdetto = parole_registro(ctx, [prima] if prima else [], s["ids"])
    avv_prima = s["avvertenza"]
    avv = pulito(avv_prima)
    fm = {"id": s["id"], "titolo": titolo_senza_esclusi(s["titolo"]), "data": s["data"], "strumenti": s["strumenti"],
          "finestra": togli_esclusi(s["finestra"]), "verdetto": verdetto, "pubblicabilita": s["pubblicabilita"],
          "avvertenza": avv, "fonte_ledger": fonte_ledger, "prove": prove_file}
    if s["audit_stato"]:
        fm = {**{k: fm[k] for k in ("id", "titolo", "data", "strumenti", "finestra", "verdetto")},
              "audit": {"stato": s["audit_stato"], "id": s["audit_id"]},
              **{k: fm[k] for k in ("pubblicabilita", "avvertenza", "fonte_ledger", "prove")}}
    dati, didascalia = (None, "") if ritirata else dati_scheda(s, ctx, prove_file)
    md = [frontmatter_testo(fm), ""]
    if s["audit"]:
        md += ["## Ritiri e correzioni", ""] + [f"- {a['testo']}" for a in s["audit"]] + [""]
    domanda = pulito(estrai_riferimenti(s["domanda"])[0]) or "-"
    md += ["## Domanda", "", domanda, "",
           "## Metodo e rubrica", "", pulito(v.get(2, "")) or "-", "", "## Esito", "",
           "| Risultato | Fonte |", "|---|---|"]
    md += [f"| {cella(r['testo'])} | {cella(r['fonte'])} |" for r in ok]
    if non:
        md += ["", f"{non} righe della scheda non riportate: la prova citata non le contiene."]
    if dati:
        md += ["", "## Grafico", "", didascalia]
    regola = estrai_riferimenti(togli_esclusi(v.get(4, ""), fino_a_fine=bool(esclusi)))[0]
    md += ["", "## Cosa NON dice", ""]
    md += [f"- {x}" for x in (pulisci_clausola(c) for c in segmenta(regola)) if x] or ["- —"]
    md += ["", "## Prove", ""]
    md += [f"- {p}" if e else f"- prova non trovata su disco: {p}" for p, t, e in stato]
    if not stato:
        md += [f"- Nessun file di prova indicato dall'inventario: {estrai_riferimenti(v.get(5, ''))[0]}"]
    stats = {"prove_mancanti": len(mancanti), "mancanti": mancanti, "fuori_repo": fuori,
             "non_riportate": non, "righe": len(ok), "avvertenza": (avv_prima, avv)}
    return "\n".join(md) + "\n", fm, dati, stats


# --- orchestrazione ---
def scrivi(f, testo):
    with open(f, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(testo)


def genera(inventario, radice, out, limit=None):
    testo = Path(inventario).read_text(encoding="utf-8")
    schede, _ = leggi_inventario(testo)
    ctx, out = Contesto(radice), Path(out)
    ctx.contenuti = leggi_contenuti(testo)
    out.mkdir(parents=True, exist_ok=True)
    for f in [*out.glob("*.md"), *out.glob("*.dati.json"), out / "indice.json"]:
        f.unlink(missing_ok=True)
    st = {"ok": 0, "avvertenza": 0, "no": 0, "skipped": 0, "prove_mancanti": 0, "non_riportate": 0,
          "dati": 0, "mancanti": [], "fuori_repo": [], "righe": 0, "id_duplicati": [], "avvertenze": [],
          "verdetti": {}}
    indice, usati = [], set()
    for s in schede:
        if s["pubblicabilita"] == "no":
            st["no"] += 1
            continue
        if s["pubblicabilita"] != "ok" and s["pubblicabilita"] != "avvertenza":
            st["skipped"] += 1
            continue
        if limit is not None and st["ok"] + st["avvertenza"] >= limit:
            break
        if s["id"] in usati:
            st["id_duplicati"].append(s["id"])
            s["id"] = f"{s['id']}-{len(usati)}"
        usati.add(s["id"])
        md, fm, dati, ps = pagina(s, ctx)
        scrivi(out / f"{fm['id']}.md", md)
        if dati:
            scrivi(out / f"{fm['id']}.dati.json", dump_dati(dati))
            st["dati"] += 1
        st[s["pubblicabilita"]] += 1
        st["prove_mancanti"] += ps["prove_mancanti"]
        st["non_riportate"] += ps["non_riportate"]
        st["righe"] += ps["righe"]
        st["mancanti"] += [(fm["id"], p) for p in ps["mancanti"]]
        st["fuori_repo"] += [(fm["id"], p) for p in ps["fuori_repo"]]
        if ps["avvertenza"][0] != ps["avvertenza"][1]:
            st["avvertenze"].append((fm["id"],) + ps["avvertenza"])
        st["verdetti"][fm["verdetto"]] = st["verdetti"].get(fm["verdetto"], 0) + 1
        voce = {"id": fm["id"], "titolo": fm["titolo"], "data": fm["data"], "strumenti": fm["strumenti"],
                "verdetto": fm["verdetto"]}
        if "audit" in fm:
            voce["audit"] = fm["audit"]["stato"]
        indice.append({**voce, "pubblicabilita": fm["pubblicabilita"], "grafico": bool(dati)})
    indice = sorted(sorted(indice, key=lambda r: r["id"]), key=lambda r: r["data"], reverse=True)
    scrivi(out / "indice.json", json.dumps(indice, ensure_ascii=False, indent=1) + "\n")
    return st


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--inventario", default=INVENTARIO)
    ap.add_argument("--root", default=RADICE, help="radice del repo del motore (sola lettura)")
    ap.add_argument("--out", default=str(USCITA))
    ap.add_argument("--limit", type=int, default=None, help="genera al massimo N pagine (test)")
    ap.add_argument("--dettagli", action="store_true", help="stampa anche i verdetti e le avvertenze modificate")
    a = ap.parse_args(argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    st = genera(a.inventario, a.root, a.out, a.limit)
    print(f"ok={st['ok']} avvertenza={st['avvertenza']} no={st['no']} skipped={st['skipped']} "
          f"prove_mancanti={st['prove_mancanti']} dati={st['dati']} righe={st['righe']} "
          f"non_riportate={st['non_riportate']}")
    for i, p in st["mancanti"]:
        print(f"prova non trovata su disco: {p} ({i})")
    for i, p in st["fuori_repo"]:
        print(f"fuori dal repo (non pubblicato): {p} ({i})")
    if a.dettagli:
        for k, n in sorted(st["verdetti"].items(), key=lambda kv: (-kv[1], kv[0])):
            print(f"verdetto {n:3d} {k}")
        for i, prima, dopo in st["avvertenze"]:
            print(f"avvertenza {i}\n  prima: {prima}\n  dopo:  {dopo}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
