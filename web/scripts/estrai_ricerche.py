#!/usr/bin/env python3
"""Genera le pagine delle ricerche del sito dall'inventario del motore (FREQ-SITO-3, Task 4).

Legge `inventario-ricerche.md` (sorgente unica) e per ogni scheda classificata OK o
"OK con avvertenza" scrive `<id>.md` (+ `<id>.dati.json` quando esiste una tabella strutturata)
in `web/src/content/ricerche/`, piu' `indice.json`. Schede NO / da verificare: nessun file.

Regole (vincolanti):
- i numeri sono COPIATI dal testo dell'inventario: lo script non calcola, non arrotonda, non parafrasa;
- ogni riga della tabella "Esito" ha una colonna Fonte (ledger `docs/EXECUTION_LEDGER.md#La-Lb`
  e/o file di prova); una riga con un numero che non compare nelle fonti citate NON entra in tabella:
  va nell'elenco "non verificabile";
- prova citata e assente su disco: "prova non trovata su disco: <percorso>";
- deterministico: stesso input, stessi byte (LF).

Solo libreria standard. Uso:
  .venv\\Scripts\\python.exe web/scripts/estrai_ricerche.py [--inventario P] [--root R] [--out D] [--limit N]
"""
import argparse
import json
import re
import sys
from pathlib import Path

INVENTARIO = r"C:\Users\farne\TradingAgent-NinjaTrader\runtime\proofs\freqsito3\inventario-ricerche.md"
RADICE = r"C:\Users\farne\TradingAgent-NinjaTrader"
USCITA = Path(__file__).resolve().parent.parent / "src" / "content" / "ricerche"
LEDGER = "docs/EXECUTION_LEDGER.md"
SUMMARY = "runtime/research/sa-report/summary.json"
MAX_RIGHE_DATI = 150
MAX_BYTE_PROVA = 12_000_000

FRONTMATTER = ("id", "titolo", "data", "strumenti", "finestra", "verdetto",
               "pubblicabilita", "avvertenza", "fonte_ledger", "prove")

# Studi elencati nelle schede ma senza esito chiuso nel ledger: mai pubblicati (regola del proprietario).
SENZA_ESITO = {
    "LIMALL-1": ("optfull_lim025", "optfull_lim05", "optfull_barra"),
    "OPT-COND-1": ("optcond",),
}

STRUMENTI = ("MES", "MNQ", "M2K", "MYM", "MCL", "MGC", "M6E", "MBT", "ES", "NQ", "RTY", "CL", "ZN",
             "SPY", "QQQ", "IWM", "DIA", "TLT", "IEF", "GLD", "SLV", "USO", "UNG", "UUP", "FXE", "FXY",
             "SPX", "NDX", "VIX", "VX", "BTC", "ETH", "FESX", "FDXM", "FDXS", "FSXE")

ID_RE = re.compile(r"\b[A-Z][A-Za-z0-9]*(?:-[A-Za-z0-9]+)+\b|\b[A-Z]+\d+[A-Za-z]*\b")
RIF = r"L\d{3,5}(?:\s*-\s*L?\d{3,5})?"
RIF_SOLO = re.compile(rf"^(?:docs/EXECUTION_LEDGER\.md:)?({RIF})$")
RIF_NUDO = re.compile(rf"(?<![\w-])({RIF})(?![\w])")
PAREN = re.compile(r"\(([^()]*)\)")
CORREZIONE = re.compile(r"artefatto|NON VALIDO|corrett[ao]|look-ahead|scartat|incompatibile|rettific|non passa|"
                        r"ristrett|difettos|contava due volte", re.I)

# --- numeri: stesse regole di verifica_numeri.py (un numero e' verificato se compare come cifre nella fonte) ---
NUMERO = re.compile(
    r"(?P<v>\d{4}-\d{2}-\d{2}|\d{1,2}:\d{2}(?::\d{2})?)"
    r"|(?<![A-Za-z_])(?<![A-Za-z]-)(?P<n>\d{1,3}(?:[.,]\d{3})+(?:[.,]\d+)?(?!\d)|\d+(?:[.,]\d+)?)"
)


def numeri(testo):
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", testo).replace("`", "").replace("*", "")
    return [m.group("v") or m.group("n") for m in NUMERO.finditer(t)]


def varianti(tok):
    v = {tok, tok.replace(",", ".")}
    if re.fullmatch(r"[1-9]\d{0,2}(?:[.,]\d{3})+", tok):
        v.add(re.sub(r"[.,]", "", tok))
    if re.fullmatch(r"[1-9]\d{0,2}(?:\.\d{3})+,\d+", tok):
        v.add(tok.replace(".", "").replace(",", "."))
    return v


def ha_numero(tok, testo):
    return any(re.search(rf"(?<!\d)(?<!\d\.){re.escape(v)}(?!\d)(?!\.\d)", testo) for v in varianti(tok))


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
    sez, schede, ritiri, indice, cur = "", [], [], [], None
    for n, r in enumerate(testo.split("\n"), 1):
        if r.startswith("## "):
            sez, cur = r[3:].strip(), None
            continue
        if sez.startswith("Ritiri"):
            if m := re.match(r"^\d+\.\s+(.*)$", r):
                ritiri += leggi_ritiro(m.group(1))
        elif sez.startswith("Indice sintetico"):
            if re.match(r"^\|\s*\d+\s*\|", r):
                c = re.split(r"(?<!\\)\|", r.strip()[1:-1])
                indice.append((int(c[0]), "|".join(c[3:-1]).strip()))
        elif sez.startswith("Schede studio"):
            if r.startswith("### "):
                cur = {"titolo": r[4:].strip(), "riga": n, "voci": {}}
                schede.append(cur)
            elif cur is not None and (m := re.match(r"^\|\s*(\d)\.\s*[^|]*?\|\s*(.*?)\s*\|\s*$", r)):
                cur["voci"][int(m.group(1))] = m.group(2)
    for s in schede:
        completa_scheda(s)
    for num, verdetto in indice:  # il numero dell'indice = ordine delle schede
        if 0 < num <= len(schede):
            schede[num - 1]["verdetto_indice"] = verdetto
    for s in schede:
        s["audit"] = [r for r in ritiri if set(r["ids"]) & set(s["ids"])]
        s["verdetto"] = verdetto_scheda(s)
    return schede, ritiri


def leggi_ritiro(item):
    out = []
    for sub in re.split(r";\s+(?=\*\*)", item):
        ids = ID_RE.findall(" ".join(re.findall(r"\*\*(.+?)\*\*", sub)))
        testo = sub.replace("**", "").strip()
        tipo = "ritirato" if re.search("ritirat", testo, re.I) else "corretto" if CORREZIONE.search(testo) else "nota"
        out.append({"ids": ids, "testo": testo, "tipo": tipo})
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


# --- verdetto ---
NEG = re.compile(r"NON\s+(?:CONFERMAT|ADOTTAT|AIUTA|VALE|PRECISO|INFORMATIV|VALID)|NESSUNA\s+VARIANTE\s+ADOTTATA|"
                 r"\b0\s+(?:\w+\s+){0,3}?(?:confermat|adottat|adottabil|candidat)|\b0\s+su\s+\d+|"
                 r"nessun[ao]?\s+(?:vantaggio|segnale|decadimento|regola|variante|candidat)|\bFAIL\b|OTTIMISTA", re.I)
POS = re.compile(r"CONFERMAT|ADOTTAT|ROBUST|REGGONO|\bAIUTA|\bVALE\b|RIPRODOTT", re.I)
PAR = re.compile(r"PARZIAL", re.I)


KSUN = re.compile(r"\b(\d+)\s+(?:\w+\s+)?(?:conferma\w+|adottat\w+|aiuta\w*|veritier\w+)\s+su\s+(\d+)", re.I)


def verdetto_vocabolario(testo):
    """Etichetta di navigazione dal vocabolario del ledger; il testo esatto resta nella pagina.
    Senza alcuna parola di verdetto: descrittivo (la scheda riporta misure, non un test)."""
    t = re.sub(r"\b0\s+(?:\w+\s+)?parzial\w*", " ", testo, flags=re.I)
    if re.match(r"\W*Nessun verdetto", t):
        return "descrittivo"
    if PAR.search(t):
        return "parziale"
    kn = KSUN.search(t)
    if (kn and 0 < int(kn.group(1)) < int(kn.group(2))) or re.search(r"\b[1-9]\d*\s+AIUTA\b", t):
        return "misto"
    n, p = NEG.search(t), POS.search(NEG.sub(lambda m: " " * len(m.group(0)), t))
    if n and p:  # la parola di verdetto che compare per prima vale come verdetto scritto
        return "non confermata" if n.start() < p.start() else "misto"
    return "non confermata" if n else "confermata" if p else "descrittivo"


def verdetto_scheda(s):
    tipi = [r["tipo"] for r in s["audit"]]
    if "ritirato" in tipi:
        return "ritirato"
    if "corretto" in tipi:
        return "corretto"
    return verdetto_vocabolario(s.get("verdetto_indice") or s["voci"].get(3, "")[:300])


# --- testo: segmentazione e riferimenti ---
def segmenta(testo):
    out, buf, depth, citato, i = [], [], 0, False, 0
    while i < len(testo):
        c = testo[i]
        buf.append(c)
        if c == '"':
            citato = not citato
        elif not citato:
            if c in "([{":
                depth += 1
            elif c in ")]}":
                depth = max(0, depth - 1)
            elif depth == 0 and testo[i + 1:i + 2] == " ":
                if c == ";" or (c == "." and re.match(r'["A-ZÀ-Ý]', testo[i + 2:i + 3] or " ")):
                    out.append("".join(buf[:-1] if c == ";" else buf).strip())
                    buf, i = [], i + 1
        i += 1
    out.append("".join(buf).strip())
    return [x for x in out if x]


def estrai_riferimenti(testo):
    """-> (testo senza citazioni, [(a, b)] righe del ledger, [citazioni di documenti])."""
    refs, docs = [], []

    def intervallo(t):
        a, b = re.findall(r"\d+", t)[0], re.findall(r"\d+", t)[-1]
        refs.append((int(a), int(b)))

    def paren(m):
        parti = [p.strip() for p in re.split(r"\s*[;,]\s*", m.group(1))]
        if not parti or not RIF_SOLO.match(parti[0]) and not re.match(rf"{RIF}\b", parti[0]):
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
    t = re.sub(r"\s+([.,;:])", r"\1", t)
    t = re.sub(r"\s{2,}", " ", t).strip()
    return t, refs, docs


def cella(t):
    return t.replace("|", "\\|")


# --- contesto: ledger, prove, summary ---
class Contesto:
    def __init__(self, radice):
        self.radice = Path(radice)
        f = self.radice / LEDGER
        self.ledger = f.read_text(encoding="utf-8", errors="replace").split("\n") if f.is_file() else []
        self._testi = {}
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

    def documento(self, nome):
        base = nome.split()[0]
        if "/" in base:
            return base if (self.radice / base).is_file() else None
        trovati = sorted((self.radice / "docs").rglob(base)) if (self.radice / "docs").is_dir() else []
        return trovati[0].relative_to(self.radice).as_posix() if trovati else None


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


def percorsi_prove(cella_prove, radice):
    """-> ([(percorso, tipo)], [fuori repo]); tipo: file | cartella | schema."""
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
def righe_esito(esito, scheda, ctx, prove_file):
    """-> (righe verificate [(testo, fonte)], non verificabili [(testo, [numeri])])."""
    _, refs_cella, docs_cella = estrai_riferimenti(esito)
    refs_cella = [r for r in dict.fromkeys(refs_cella) if 0 < r[0] <= r[1] <= len(ctx.ledger)]
    docs_cella = [d for d in (ctx.documento(x) for x in docs_cella) if d]
    ok, no = [], []
    for seg in segmenta(esito):
        testo, refs, docs = estrai_riferimenti(seg)
        if not testo or not re.search(r"\w", testo):
            continue
        proprie = [r for r in dict.fromkeys(refs) if 0 < r[0] <= r[1] <= len(ctx.ledger)]
        primarie = proprie or refs_cella
        fonti = [(f"{LEDGER}#L{a}-L{b}", ctx.righe_ledger(a, b)) for a, b in primarie]
        extra = [(f"{LEDGER}#L{a}-L{b}", ctx.righe_ledger(a, b)) for a, b in refs_cella if (a, b) not in primarie]
        extra += [(d, ctx.testo(d)) for d in dict.fromkeys(docs + docs_cella)]
        extra += [(p, ctx.testo(p)) for p in prove_file]
        # citazioni proprie del segmento: sempre in Fonte; altrimenti solo le fonti dove i numeri si ritrovano
        usate, mancanti = (list(fonti) if proprie else []), []
        for tok in numeri(testo):
            if any(ha_numero(tok, t) for _, t in usate):
                continue
            trovata = next(((n, t) for n, t in fonti + extra if ha_numero(tok, t)), None)
            if trovata:
                usate.append(trovata)
            else:
                mancanti.append(tok)
        if mancanti:
            no.append((testo, list(dict.fromkeys(mancanti))))
        else:
            ok.append((testo, " · ".join(n for n, _ in (usate or fonti)) or "—"))
    return ok, no


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
def senza_esito(s, ctx_testo):
    """Toglie da un testo cio' che riguarda studi senza esito chiuso (dal primo accenno alla fine del blocco)."""
    for i in s["ids"]:
        if i in SENZA_ESITO:
            segs, out = segmenta(ctx_testo), []
            for seg in segs:
                if i in seg:
                    break
                out.append(seg)
            ctx_testo = "; ".join(out)
    return ctx_testo


def pagina(s, ctx):
    """-> (testo md, frontmatter, dati|None, stats). Solleva ValueError per le schede non pubblicabili."""
    if s["pubblicabilita"] not in ("ok", "avvertenza"):
        raise ValueError(f"scheda {s['id']}: pubblicabilita '{s['pubblicabilita']}', nessuna pagina")
    v = s["voci"]
    esclusi = [i for i in s["ids"] if i in SENZA_ESITO]
    verdetto = s["verdetto"]
    percorsi, fuori = percorsi_prove(v.get(5, ""), ctx.radice)
    percorsi = [(p, t) for p, t in percorsi if p.rstrip("/") not in RADICI_GENERICHE
                and not any(h in p for i in esclusi for h in SENZA_ESITO[i])]
    stato = [(p, t, esiste(p, t, ctx.radice)) for p, t in percorsi]
    prove_file = [p for p, t, e in stato if t == "file" and e]
    mancanti = [p for p, t, e in stato if not e]
    esito = senza_esito(s, v.get(3, ""))
    ok, no = righe_esito(esito, s, ctx, prove_file)
    _, refs, _ = estrai_riferimenti(v.get(3, ""))
    refs = [r for r in dict.fromkeys(refs) if 0 < r[0] <= r[1] <= len(ctx.ledger)]
    avv = s["avvertenza"]
    for i in esclusi:
        avv = (avv + " " if avv else "") + f"{i}: esito non chiuso nel ledger, non pubblicato."
    fm = {"id": s["id"], "titolo": s["titolo"], "data": s["data"], "strumenti": s["strumenti"],
          "finestra": s["finestra"], "verdetto": verdetto, "pubblicabilita": s["pubblicabilita"],
          "avvertenza": avv, "fonte_ledger": f"{LEDGER}#L{refs[0][0]}-L{refs[0][1]}" if refs else "",
          "prove": prove_file}
    dati, didascalia = (None, "") if verdetto == "ritirato" else dati_scheda(s, ctx, prove_file)
    md = [frontmatter_testo(fm), ""]
    if s["audit"]:
        md += ["## Ritiri e correzioni", ""] + [f"- {a['testo']}" for a in s["audit"]] + [""]
    md += ["## Domanda", "", senza_esito(s, estrai_riferimenti(s["domanda"])[0]) or s["domanda"], "",
           "## Metodo e rubrica", "", senza_esito(s, v.get(2, "")), "", "## Esito", "",
           "| Risultato | Fonte |", "|---|---|"]
    md += [f"| {cella(t)} | {cella(f)} |" for t, f in ok]
    if no:
        md += ["", "Non verificabile (i numeri non compaiono nelle fonti citate: restano fuori dalla tabella):", ""]
        md += [f"- {t} — non verificabile: {', '.join(n)}" for t, n in no]
    if dati:
        md += ["", "## Grafico", "", didascalia]
    md += ["", "## Cosa NON dice", ""]
    md += [f"- {x}" for x in segmenta(estrai_riferimenti(senza_esito(s, v.get(4, "")))[0])]
    md += [f"- {i}: esito non chiuso nel ledger, non pubblicato." for i in esclusi]
    md += ["", "## Prove", ""]
    md += [f"- {p}" if e else f"- prova non trovata su disco: {p}" for p, t, e in stato]
    if not stato:
        md += [f"- Nessun file di prova indicato dall'inventario: {estrai_riferimenti(v.get(5, ''))[0]}"]
    stats = {"prove_mancanti": len(mancanti), "mancanti": mancanti, "fuori_repo": fuori,
             "non_verificabili": sum(len(n) for _, n in no), "righe": len(ok)}
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
    st = {"ok": 0, "avvertenza": 0, "no": 0, "skipped": 0, "prove_mancanti": 0, "non_verificabili": 0,
          "dati": 0, "mancanti": [], "fuori_repo": [], "ids_senza_esito": [], "righe": 0, "id_duplicati": []}
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
        st["non_verificabili"] += ps["non_verificabili"]
        st["righe"] += ps["righe"]
        st["mancanti"] += [(fm["id"], p) for p in ps["mancanti"]]
        st["fuori_repo"] += [(fm["id"], p) for p in ps["fuori_repo"]]
        st["ids_senza_esito"] += [i for i in s["ids"] if i in SENZA_ESITO]
        indice.append({"id": fm["id"], "titolo": fm["titolo"], "data": fm["data"], "strumenti": fm["strumenti"],
                       "verdetto": fm["verdetto"], "pubblicabilita": fm["pubblicabilita"], "grafico": bool(dati)})
    indice = sorted(sorted(indice, key=lambda r: r["id"]), key=lambda r: r["data"], reverse=True)
    scrivi(out / "indice.json", json.dumps(indice, ensure_ascii=False, indent=1) + "\n")
    return st


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--inventario", default=INVENTARIO)
    ap.add_argument("--root", default=RADICE, help="radice del repo del motore (sola lettura)")
    ap.add_argument("--out", default=str(USCITA))
    ap.add_argument("--limit", type=int, default=None, help="genera al massimo N pagine (test)")
    a = ap.parse_args(argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    st = genera(a.inventario, a.root, a.out, a.limit)
    print(f"ok={st['ok']} avvertenza={st['avvertenza']} no={st['no']} skipped={st['skipped']} "
          f"prove_mancanti={st['prove_mancanti']} dati={st['dati']} righe={st['righe']} "
          f"non_verificabili={st['non_verificabili']} ids_senza_esito={','.join(sorted(set(st['ids_senza_esito']))) or '-'}")
    for i, p in st["mancanti"]:
        print(f"prova non trovata su disco: {p} ({i})")
    for i, p in st["fuori_repo"]:
        print(f"fuori dal repo (non pubblicato): {p} ({i})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
