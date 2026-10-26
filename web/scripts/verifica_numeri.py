#!/usr/bin/env python3
"""Verifica che ogni numero delle tabelle di web/src/content/ricerche/*.md compaia nelle prove citate.

Per ogni tabella con una colonna "Fonte", ogni numero delle altre celle della riga
(interi, decimali, percentuali, coppie k/n come due numeri, date ISO e orari come stringhe
intere) deve comparire come cifre nel file di prova citato dalla cella Fonte, oppure nel
ledger (docs/EXECUTION_LEDGER.md) alle righe indicate.

Cella Fonte: un percorso (anche solo il nome del file, risolto tra le `prove` del frontmatter
o sotto la radice del motore) con locatore opzionale di righe `L10-L20` (es. `report.md#L3`,
`report.md L10-L20`); oppure `ledger` / `docs/EXECUTION_LEDGER.md` con l'intervallo `L10811-L10830`,
altrimenti vale `fonte_ledger` del frontmatter. Locatori non di riga (sezione, chiave JSON)
non restringono: si cerca nell'intero file.

Cosa NON controlla: i numeri nella prosa fuori dalle tabelle; le tabelle senza colonna Fonte;
gli identificatori con lettere prima delle cifre (S1, LENTI-1); i numeri della cella Fonte.
Virgola e punto decimali sono equivalenti ("57,9" = "57.9") e i separatori di migliaia si
ignorano ("1.234" = "1234"). Le percentuali si confrontano come scritte: "57.9%" cerca "57.9".

Uscita: 0 tutto trovato; 1 numeri mancanti o fonti non risolvibili; 2 uso errato / nessun file.
"""
import argparse
import os
import re
import sys
from decimal import ROUND_HALF_EVEN, ROUND_HALF_UP, Decimal
from pathlib import Path

AQUI = Path(__file__).resolve().parent
CONTENUTO = AQUI.parent / "src" / "content" / "ricerche"
RADICE = os.environ.get("ENGINE_ROOT", r"C:\Users\farne\TradingAgent-NinjaTrader")
LEDGER = "docs/EXECUTION_LEDGER.md"

NUMERO = re.compile(
    r"(?P<v>\d{4}-\d{2}-\d{2}|\d{1,2}:\d{2}(?::\d{2})?)"
    r"|(?<![A-Za-z_])(?<![A-Za-z]-)(?P<n>\d{1,3}(?:[.,]\d{3})+(?:[.,]\d+)?(?!\d)|\d+(?:[.,]\d+)?)"
)
PERCORSO = re.compile(r"[\w./\\-]+\.[A-Za-z][A-Za-z0-9]{0,4}")
LOC = re.compile(r"\s*(?:#|:|@)?\s*L(\d+)(?:\s*[-–—]\s*L?(\d+))?")
INTERVALLO = re.compile(r"L(\d+)(?:\s*[-–—]\s*L?(\d+))?")


def frontmatter(testo):
    """Frontmatter YAML minimo (chiave: valore, liste `- x` o `[a, b]`). -> (dict, prima riga del corpo)."""
    righe = testo.splitlines()
    if not righe or righe[0].strip() != "---":
        return {}, 0
    fine = next((i for i in range(1, len(righe)) if righe[i].strip() == "---"), None)
    if fine is None:
        return {}, 0
    fm, chiave = {}, None
    for r in righe[1:fine]:
        m = re.match(r"^([A-Za-z_][\w-]*)\s*:\s*(.*)$", r)
        if m:
            chiave, val = m.group(1), m.group(2).strip()
            if val.startswith("["):
                fm[chiave] = [unq(x) for x in val.strip("[]").split(",") if x.strip()]
            else:
                fm[chiave] = unq(val) if val else []
        elif chiave and isinstance(fm.get(chiave), list) and (m := re.match(r"^\s*-\s+(.*)$", r)):
            fm[chiave].append(unq(m.group(1)))
    return fm, fine + 1


def unq(s):
    s = s.strip()
    return s[1:-1] if len(s) > 1 and s[0] == s[-1] and s[0] in "\"'" else s


def celle(riga):
    r = riga.strip().strip("|")
    return [c.strip() for c in re.split(r"(?<!\\)\|", r)]


def tabelle(righe, da):
    """Genera (intestazione, [(n_riga_1based, celle)]) per ogni tabella markdown."""
    i = da
    while i < len(righe):
        if righe[i].lstrip().startswith("|") and i + 1 < len(righe) and re.match(r"^\s*\|?\s*:?-{2,}", righe[i + 1]):
            testata, i, dati = celle(righe[i]), i + 2, []
            while i < len(righe) and righe[i].lstrip().startswith("|"):
                dati.append((i + 1, celle(righe[i])))
                i += 1
            yield testata, dati
        else:
            i += 1


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


class Fonte:
    def __init__(self, etichetta, testo):
        self.etichetta, self.testo, self._tondi = etichetta, testo, {}

    def ha(self, tok, arrotonda):
        for v in varianti(tok):
            if re.search(rf"(?<!\d)(?<!\d\.){re.escape(v)}(?!\d)(?!\.\d)", self.testo):
                return True
        if arrotonda:  # solo numeri con decimali: la fonte deve averne di piu'
            d = Decimal(tok.replace(",", "."))
            nd = -d.as_tuple().exponent
            if nd >= 1 and d == d.quantize(Decimal(1).scaleb(-nd)) and re.fullmatch(r"\d+[.,]\d+", tok):
                return d in self._arrotondati(nd)
        return False

    def _arrotondati(self, nd):
        if nd not in self._tondi:
            q, s = Decimal(1).scaleb(-nd), set()
            for x in set(re.findall(rf"(?<![\d.])\d+\.\d{{{nd + 1},}}", self.testo)):
                s |= {Decimal(x).quantize(q, ROUND_HALF_UP), Decimal(x).quantize(q, ROUND_HALF_EVEN)}
            self._tondi[nd] = s
        return self._tondi[nd]


class Radice:
    def __init__(self, radice):
        self.radice, self._cache = Path(radice), {}

    def righe(self, rel):
        if rel not in self._cache:
            self._cache[rel] = (self.radice / rel).read_text(encoding="utf-8", errors="replace").splitlines()
        return self._cache[rel]

    def fonte(self, rel, intervalli=None):
        r = self.righe(rel)
        if intervalli:
            return Fonte(f"{rel} L{intervalli[0][0]}-L{intervalli[-1][1]}" if len(intervalli) == 1 else rel,
                         "\n".join(x for a, b in intervalli for x in r[a - 1:b]))
        return Fonte(rel, "\n".join(r))


def intervalli(testo):
    return [(int(m.group(1)), int(m.group(2) or m.group(1))) for m in INTERVALLO.finditer(testo)]


def risolvi(cella, prove, ledger_fm, rad):
    """Cella Fonte -> ([Fonte], [errori])."""
    t = re.sub(r"[`*]", "", cella)
    fonti, errori, visti = [], [], False
    for m in PERCORSO.finditer(t):
        p = m.group(0).replace("\\", "/")
        p = p[2:] if p.startswith("./") else p
        loc = LOC.match(t, m.end())
        iv = [(int(loc.group(1)), int(loc.group(2) or loc.group(1)))] if loc else None
        visti = True
        if p.endswith("EXECUTION_LEDGER.md"):
            fonti_l, err = ledger(iv or ledger_fm, rad)
            fonti += fonti_l
            errori += err
            continue
        rel = next((x for x in prove if x == p or x.endswith("/" + p) or x.rsplit("/", 1)[-1] == p.rsplit("/", 1)[-1]), p)
        if not (rad.radice / rel).is_file():
            errori.append(f"fonte citata non trovata: {p}")
        else:
            fonti.append(rad.fonte(rel, iv))
    if not visti and re.search("ledger", t, re.I):
        fonti_l, err = ledger(intervalli(t) or ledger_fm, rad)
        fonti, errori = fonti + fonti_l, errori + err
    return fonti, errori


def ledger(iv, rad):
    if not iv:
        return [], ["ledger citato senza intervallo di righe (L10-L20 nella cella o fonte_ledger nel frontmatter)"]
    if not (rad.radice / LEDGER).is_file():
        return [], [f"ledger non trovato: {rad.radice / LEDGER}"]
    return [rad.fonte(LEDGER, iv)], []


def controlla(file, rad, arrotonda, out):
    """-> (tabelle controllate, righe, numeri, mancanti)."""
    testo = file.read_text(encoding="utf-8")
    fm, corpo = frontmatter(testo)
    prove = fm.get("prove") or []
    prove = [prove] if isinstance(prove, str) else [p.replace("\\", "/") for p in prove]
    ledger_fm = intervalli(fm["fonte_ledger"]) if isinstance(fm.get("fonte_ledger"), str) else None
    n_tab = n_righe = n_num = mancanti = 0
    for p in prove:
        if not (rad.radice / p).is_file():
            out.append(f"{file.name}: prova del frontmatter non trovata: {p}")
            mancanti += 1
    for testata, dati in tabelle(testo.splitlines(), corpo):
        col = next((i for i, h in enumerate(testata) if re.sub(r"[`*]", "", h).strip().lower().startswith("font")), None)
        if col is None:
            continue
        n_tab += 1
        for n, c in dati:
            toks = [t for i, cella in enumerate(c) if i != col for t in numeri(cella)]
            if not toks:
                continue
            n_righe += 1
            fonti, errori = risolvi(c[col] if col < len(c) else "", prove, ledger_fm, rad)
            if not fonti and not errori:
                errori = ["riga con numeri senza fonte risolvibile (colonna Fonte vuota o senza percorso)"]
            for e in errori:
                out.append(f"{file.name}:{n}: {e}")
                mancanti += 1
            for t in toks if fonti else []:
                n_num += 1
                if not any(f.ha(t, arrotonda) for f in fonti):
                    out.append(f'{file.name}:{n}: riga "{c[0][:40]}": numero {t} non trovato in {", ".join(f.etichetta for f in fonti)}')
                    mancanti += 1
    if n_tab == 0:
        out.append(f"{file.name}: nessuna tabella con colonna Fonte")
        mancanti += 1
    return n_tab, n_righe, n_num, mancanti


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("percorsi", nargs="*", help=f"file .md o cartelle (default: {CONTENUTO})")
    ap.add_argument("--root", default=RADICE, help="radice del repo del motore (default: $ENGINE_ROOT o il repo del proprietario)")
    ap.add_argument("--rounding", action="store_true",
                    help="accetta un numero con decimali se la fonte lo ha con piu' decimali e arrotondato coincide (0.579 vs 0.5789); spento di default")
    a = ap.parse_args(argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    files = []
    for p in map(Path, a.percorsi or [CONTENUTO]):
        if not p.exists():
            print(f"percorso non trovato: {p}", file=sys.stderr)
            return 2
        files += sorted(p.glob("*.md")) if p.is_dir() else [p]
    if not files:
        print(f"nessun file .md da verificare (cercato in {a.percorsi or [str(CONTENUTO)]})", file=sys.stderr)
        return 2
    rad, out, tot = Radice(a.root), [], [0, 0, 0, 0]
    for f in files:
        tot = [x + y for x, y in zip(tot, controlla(f, rad, a.rounding, out))]
    print("\n".join(out))
    print(f"{'OK' if not tot[3] else 'FALLITO'}: {len(files)} file, {tot[0]} tabelle, {tot[1]} righe, {tot[2]} numeri verificati, {tot[3]} mancanti")
    return 1 if tot[3] else 0


if __name__ == "__main__":
    sys.exit(main())
