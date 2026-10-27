"""Test di estrai_ricerche.py su un inventario finto (nessun dato reale).

Uso: .venv\\Scripts\\python.exe -m pytest web/scripts/test_estrai.py
"""
import json
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import estrai_ricerche as E  # noqa: E402

LEDGER = "\n".join(
    [f"riga {i}" for i in range(1, 101)]
    + [
        "riga 101",
        "riga 102",
        "Esito ALFA (alfa1.json): NON CONFERMATA: MES 120 trade +12,34 USD (t 1,50); MNQ 80 trade -3,21 USD",
        "q 0,48 placebo p95 9,9",
        "riga 105",
        "riga 106",
        "gamma +50,5 bp t 2,40 CONFERMATO",
        "riga 108",
        "CONFERMA RITIRATA; verdetto NON CONFERMATO per GAMMA-1; GAMMA-2 delta +3,21 bp",
        "riga 110",
        "aiutano 10 casi",
        "riga 112",
        "Esito zeta: FAIL, MES 55 trade +7,77 USD (t 2,22)",
        "NON CONFERMATA classifica 1 -2,84; 2 -1,57",
        # 115-127: casi di contesto per le parole di verdetto (sono frasi del registro, vedi ANCORE)
        "Suite: 120 PASS, 0 FAIL, 1924 s",  # 115: conteggi di test, non un verdetto (caso lab-2)
        "- Verdetto: CONFERMATO se media netta > 0 e t >= 2; NON CONFERMATO altrimenti",  # 116: rubrica (caso assorb-1)
        "DIXCLOSE-1 rubrica: CONFERMATA dopo 60 giorni-segnale se media netta > 0; FALSIFICATA altrimenti",  # 117 (oc-explore-1)
        "Esito DIXCLOSE-1: nessun esito; 2 test PASS; 0 CONFERMATE su 4",  # 118: test PASS e conteggio (phase-1)
        "Esito X (a/b.json, run.log): NON CONFERMATA, nessuna variante",  # 119: "Esito ...: PAROLA"
        "- Verdetto: PARZIALE",  # 120: "Verdetto: PAROLA"
        "Esito PASS (script eseguito), verdetto NON CONFERMATA su 4 varianti",  # 121: "Esito PAROLA" + "verdetto PAROLA"
        "Esito: **BLOCKED_ENV**, non PASS",  # 122: "Esito: PAROLA"; "non PASS" non e' ancorato
        "il verdetto NON CONFERMATA regge anche in lettura ottimistica",  # 123: "verdetto PAROLA"
        "- esito NON CONFERMATA (bilancio qui sopra)",  # 124: "esito PAROLA"
        "Outcome: CONFERMATA solo se media > 0",  # 125: seguita da "solo se": rubrica
        "Esito: 3643 PASS, 0 FAIL",  # 126: preceduta da un conteggio
        "Outcome: DESCRITTIVO con 0 eventi",  # 127: "Outcome: PAROLA"
        "client IB in sola lettura (ib_async 2.1.0)",  # 128
        "test_ibkr_opzioni 9 PASS",  # 129
        "riga 130",
        # 131-140: famiglie A e B, plurali, "esito PAROLA" solo a inizio riga
        "Esito KRT-1 (runtime/proofs/krt1/krt1.json, run.log, yahoo_daily.csv, 7 PASS nel pannello, "
        "rubrica congelata prima di ogni risultato): NON CONFERMATA, segni del paper",  # 131: famiglia A (parentesi lunga)
        "Esito Y (" + "p" * 120 + ") poi altre note: NON CONFERMATA",  # 132: i due punti non seguono la parentesi
        "Esito OVN-1 (a.json): CONFERMATI TT e WEAK; Esito GOLDN-1 (b.json): NON CONFERMATO",  # 133: plurale + ID
        "Esito Z-1 (a.json): 0 CONFERMATE su 4",  # 134: plurale dopo un conteggio
        "- Esito PASS, 2 test; il resto segue",  # 135: "esito PAROLA" a inizio di punto elenco
        "ma un esito NON CONFERMATA e' informativo quanto uno confermato",  # 136: frase ipotetica
        "VOLREV-1 (future VOLX, registrato CONFERMATO): CONFERMA RITIRATA, VOLREV-1 = NON CONFERMATO",  # 137: famiglia B
        "ripartito alle 20:47 su 69 sessioni (30/69), orari 15:30 e 22:00",  # 138: numeri dentro orari e rapporti
        "Esito (a.json): DESCRITTIVO senza ID",  # 139: Esito + parentesi + due punti, senza ID
        "Esito SAFE-1 (run.log, 3 PASS nel pannello): PASS, NON CONFERMATA",  # 140: famiglia A, PASS e verdetto di ricerca in catena
        "Esito W-1 (a.json): PASS, 2 CONFERMATE su 4",  # 141: la catena si ferma davanti a un conteggio
        "Esito W-2 (a.json): PASS, CONFERMATA se la media > 0",  # 142: la catena si ferma davanti a "se"
        "Esito W-3 (a.json): BLOCKED_ENV, NON CONFERMATA",  # 143: la catena parte solo da PASS o FAIL
    ]
)

INVENTARIO = """# Inventario finto

## Ritiri, correzioni e margini sottili da riportare insieme ai risultati (prima di pubblicare numeri)

1. **GAMMA-1 (L109)**: la conferma e' stata RITIRATA dall'audit (artefatto di cambio contratto): ora "NON CONFERMATO".
2. **DELTA-1 (L108)**: prima misura corretta (contava due volte lo stesso trade).
3. **LAMBDA-1 (L111)**: file distorto `lambda1/lambda1-biased.json` da non usare.

## Schede studio (ordine del ledger)

### ALFA-1 — studio di prova
| Voce | Contenuto |
|---|---|
| 1. Identità | 12/10/2026; MES e MNQ 1 minuto 2020-2026; domanda: la regola X guadagna? |
| 2. Metodo | Rubrica prima: sì (L102). |
| 3. Esito | "NON CONFERMATA": MES 120 trade +12,34 USD (t 1,50); MNQ 80 trade -3,21 USD; q 0,48. (L103-L104) |
| 4. Regola di lettura | Frequenze, non segnali; il rialzo di fondo spiega parte del risultato. |
| 5. Prove | `runtime/proofs/alfa1/alfa1.json` |
| 6. Pubblicabilità | OK. |

### BETA-1 — studio non pubblicabile
| Voce | Contenuto |
|---|---|
| 1. Identità | 13/10/2026; dati di un fornitore; domanda: serve? |
| 2. Metodo | Rubrica prima: no. |
| 3. Esito | "descrittivo": 5 casi (L103). |
| 4. Regola di lettura | Nessuna. |
| 5. Prove | `runtime/proofs/beta1/beta1.json` |
| 6. Pubblicabilità | NO: contenuti licenziati di terzi. |

### GAMMA-1 / GAMMA-2 — studio ritirato
| Voce | Contenuto |
|---|---|
| 1. Identità | 14/10/2026; MES 1 minuto; domanda: il segnale gamma regge? |
| 2. Metodo | Terzili. |
| 3. Esito | GAMMA-1 registrato "CONFERMATO": gamma +50,5 bp t 2,40; RITIRATO dall'audit: "CONFERMA RITIRATA, GAMMA-1 = NON CONFERMATO"; GAMMA-2: delta +3,21 bp. (L107-L109) |
| 4. Regola di lettura | Solo descrittivo (AUDIT-FABLE, L109): GAMMA-1 ritirato; la scheda va pubblicata solo insieme al ritiro. |
| 5. Prove | `runtime/proofs/gamma1/gamma1.json` |
| 6. Pubblicabilità | OK con avvertenza: pubblicare solo il verdetto finale; conferma poi ritirata. |

### DELTA-1 — studio con prova mancante
| Voce | Contenuto |
|---|---|
| 1. Identità | 15/10/2026; MNQ; domanda: la misura tiene? |
| 2. Metodo | Una finestra. |
| 3. Esito | Misura corretta a 77,77 USD per trade (L108). |
| 4. Regola di lettura | Un solo campione. |
| 5. Prove | `runtime/proofs/delta1/delta1.json` |
| 6. Pubblicabilità | OK con avvertenza: un solo campione. |

### EPS-1 — studio con tabella strutturata
| Voce | Contenuto |
|---|---|
| 1. Identità | 16/10/2026; MES; domanda: quale riga vince? |
| 2. Metodo | Due righe. |
| 3. Esito | "NON CONFERMATA": riga A media 1,50 USD (L103). |
| 4. Regola di lettura | Nessuna. |
| 5. Prove | `runtime/proofs/eps1/eps1.json` |
| 6. Pubblicabilità | OK. |

### ETA-1 — studio con serie annuale
| Voce | Contenuto |
|---|---|
| 1. Identità | 11/10/2026; MNQ; domanda: come va anno per anno? |
| 2. Metodo | Un risultato per anno. |
| 3. Esito | MNQ 80 trade (L103). |
| 4. Regola di lettura | Nessuna. |
| 5. Prove | `runtime/proofs/eta1/eta1.json` |
| 6. Pubblicabilità | OK. |

### ZETA-1 — numeri sulla riga accanto alla citazione
| Voce | Contenuto |
|---|---|
| 1. Identità | 10/10/2026; MES; domanda: quanti trade? |
| 2. Metodo | Un test. |
| 3. Esito | MES 55 trade +7,77 USD (t 2,22). (L110) |
| 4. Regola di lettura | Nessuna. |
| 5. Prove | `runtime/proofs/alfa1/alfa1.json` |
| 6. Pubblicabilità | OK. |

### OMEGA-1 — parola di verdetto solo in una riga secondaria
| Voce | Contenuto |
|---|---|
| 1. Identità | 03/10/2026; MES; domanda: il locatore principale ha un verdetto? |
| 2. Metodo | Un test. |
| 3. Esito | MES 55 trade +7,77 USD (t 2,22) (L110); "NON CONFERMATA" classifica: 1 -2,84; 2 -1,57. (L114) |
| 4. Regola di lettura | Nessuna. |
| 5. Prove | `runtime/proofs/alfa1/alfa1.json` |
| 6. Pubblicabilità | OK. |

### PSI-1 — parola FAIL nel locatore principale
| Voce | Contenuto |
|---|---|
| 1. Identità | 02/10/2026; MES; domanda: quanti trade? |
| 2. Metodo | Un test. |
| 3. Esito | MES 55 trade +7,77 USD (t 2,22). (L113) |
| 4. Regola di lettura | Nessuna. |
| 5. Prove | `runtime/proofs/alfa1/alfa1.json` |
| 6. Pubblicabilità | OK. |

### THETA-1 e LIMALL-1 — prova con uno studio senza esito
| Voce | Contenuto |
|---|---|
| 1. Identità | 09/10/2026; MES 1 minuto 2020-2026; LIMALL-1 su tutte le famiglie (parte A: MR-1); domanda: la regola regge? |
| 2. Metodo | Rubrica prima: sì (L102). |
| 3. Esito | THETA-1: "NON CONFERMATA": MES 120 trade +12,34 USD (t 1,50); LIMALL-1: esito citato solo tra le prove (L110); numeri in `optfull_lim025/x.json`, non riportati nel ledger. (L103, L104) |
| 4. Regola di lettura | Selezione avversa; per LIMALL-1 manca l'esito numerico. |
| 5. Prove | `runtime/proofs/alfa1/alfa1.json`, `runtime/proofs/optfull_lim025/x.json` |
| 6. Pubblicabilità | OK con avvertenza: per LIMALL-1 serve prima leggere i file di proofs; dati licenziati solo aggregati. |

### IOTA-1 — avvertenze con istruzioni
| Voce | Contenuto |
|---|---|
| 1. Identità | 08/10/2026; MES; domanda: istruzioni? |
| 2. Metodo | Un test. |
| 3. Esito | MES 120 trade (L103). |
| 4. Regola di lettura | Esplorazione; da NON ripubblicare senza correzione. |
| 5. Prove | `runtime/proofs/alfa1/alfa1.json` |
| 6. Pubblicabilità | OK con avvertenza: pubblicare i soli aggregati; dati di terzi (ES 1m, citare fonti) solo aggregati; includere il caveat: esplorazione. |

### KAPPA-1 — avvertenza solo istruzione
| Voce | Contenuto |
|---|---|
| 1. Identità | 07/10/2026; MES; domanda: solo istruzioni? |
| 2. Metodo | Un test. |
| 3. Esito | MES 120 trade (L103). |
| 4. Regola di lettura | Nessuna. |
| 5. Prove | `runtime/proofs/alfa1/alfa1.json` |
| 6. Pubblicabilità | OK con avvertenza: citare solo i risultati sulle strategie. |

### LAMBDA-1 — file da non usare e nessuna parola di verdetto
| Voce | Contenuto |
|---|---|
| 1. Identità | 06/10/2026; MES; domanda: aiuta? |
| 2. Metodo | Un test. |
| 3. Esito | "aiutano" 10 casi (L111). |
| 4. Regola di lettura | Nessuna. |
| 5. Prove | `runtime/proofs/lambda1/lambda1.json`; `lambda1-biased.json` (risultato DISTORTO) |
| 6. Pubblicabilità | OK. |

### MU-1 — numeri solo nelle prove JSON
| Voce | Contenuto |
|---|---|
| 1. Identità | 05/10/2026; MES; domanda: dove stanno i numeri? |
| 2. Metodo | Un test. |
| 3. Esito | n 77 media 7,5; valore 99,99; n 77 e valore 12 (L112). |
| 4. Regola di lettura | Nessuna. |
| 5. Prove | `runtime/proofs/mu1/mu1.json` |
| 6. Pubblicabilità | OK. |

### NU-1 — frammenti senza soggetto
| Voce | Contenuto |
|---|---|
| 1. Identità | 04/10/2026; MES; domanda: classifica? |
| 2. Metodo | Un test. |
| 3. Esito | "NON CONFERMATA" classifica: 1 -2,84; 2 -1,57. (L114) |
| 4. Regola di lettura | Nota (AUDIT-FABLE, L109): classifica provvisoria. |
| 5. Prove | `runtime/proofs/alfa1/alfa1.json` |
| 6. Pubblicabilità | OK. |

### CHI-1 — pagina il cui locatore contiene solo conteggi di test
| Voce | Contenuto |
|---|---|
| 1. Identità | 01/10/2026; MES; domanda: conteggi? |
| 2. Metodo | Un test. |
| 3. Esito | MES 120 trade (L115). |
| 4. Regola di lettura | Nessuna. |
| 5. Prove | `runtime/proofs/alfa1/alfa1.json` |
| 6. Pubblicabilità | OK. |

### RHO-1 — pagina il cui locatore contiene solo una rubrica futura
| Voce | Contenuto |
|---|---|
| 1. Identità | 30/09/2026; MES; domanda: rubrica? |
| 2. Metodo | Un test. |
| 3. Esito | MES 60 giorni (L117). |
| 4. Regola di lettura | Nessuna. |
| 5. Prove | `runtime/proofs/alfa1/alfa1.json` |
| 6. Pubblicabilità | OK. |

### SIGMA-1 — versione con punti come un solo numero
| Voce | Contenuto |
|---|---|
| 1. Identità | 29/09/2026; MES; domanda: quale client? |
| 2. Metodo | Un test. |
| 3. Esito | client IB (ib_async 2.1.0), 9 test PASS (L128-L129) |
| 4. Regola di lettura | Nessuna. |
| 5. Prove | `runtime/proofs/alfa1/alfa1.json` |
| 6. Pubblicabilità | OK. |

### TAU-1 — numeri in una tabella di documento, intestazione 9 righe sopra
| Voce | Contenuto |
|---|---|
| 1. Identità | 28/09/2026; MES; domanda: escursione? |
| 2. Metodo | Un test. |
| 3. Esito | Documento: escursione mediana (sessioni, punti) 00:00-08:00 192, 08:00-14:30 195. (L103; TAB.txt sez. 3) |
| 4. Regola di lettura | Nessuna. |
| 5. Prove | `runtime/proofs/alfa1/alfa1.json` |
| 6. Pubblicabilità | OK. |

### UPSILON-1 — numero lontano dall'intestazione del documento
| Voce | Contenuto |
|---|---|
| 1. Identità | 27/09/2026; MES; domanda: escursione? |
| 2. Metodo | Un test. |
| 3. Esito | Documento: escursione mediana (sessioni, punti) 777. (L103; TAB.txt sez. 9) |
| 4. Regola di lettura | Nessuna. |
| 5. Prove | `runtime/proofs/alfa1/alfa1.json` |
| 6. Pubblicabilità | OK. |

### FI-1 — avvertenza con fatto e istruzione nella stessa clausola
| Voce | Contenuto |
|---|---|
| 1. Identità | 26/09/2026; MES; domanda: avvertenza mista? |
| 2. Metodo | Un test. |
| 3. Esito | MES 120 trade (L103). |
| 4. Regola di lettura | Nessuna. |
| 5. Prove | `runtime/proofs/alfa1/alfa1.json` |
| 6. Pubblicabilità | OK con avvertenza: la heatmap PNG mostra il book L2 di un giorno (dati licenziati): pubblicarla solo se la licenza lo consente; gli esiti numerici sì. |

### OVN-1 e GOLDN-1 — due studi con verdetti diversi nello stesso locatore
| Voce | Contenuto |
|---|---|
| 1. Identità | 25/09/2026; MES; domanda: quale studio ha quale verdetto? |
| 2. Metodo | Un test. |
| 3. Esito | Esito OVN-1 (a.json): CONFERMATI TT e WEAK; Esito GOLDN-1 (b.json): NON CONFERMATO. (L133) |
| 4. Regola di lettura | Nessuna. |
| 5. Prove | `runtime/proofs/alfa1/alfa1.json` |
| 6. Pubblicabilità | OK. |

### TEO-1 — numero dentro orari e rapporti nel registro, riga vera nel documento
| Voce | Contenuto |
|---|---|
| 1. Identità | 24/09/2026; MNQ; domanda: quando si supera il massimo notturno? |
| 2. Metodo | Un test. |
| 3. Esito | sopra il massimo notturno entro le 15:30 47%, entro le 22:00 69%. (L138; TEO.txt sez. 5) |
| 4. Regola di lettura | Nessuna. |
| 5. Prove | `runtime/proofs/alfa1/alfa1.json` |
| 6. Pubblicabilità | OK. |

### TEO-2 — numero che nel registro sta solo dentro un orario
| Voce | Contenuto |
|---|---|
| 1. Identità | 23/09/2026; MNQ; domanda: quanti trade? |
| 2. Metodo | Un test. |
| 3. Esito | MES 47 trade. (L138) |
| 4. Regola di lettura | Nessuna. |
| 5. Prove | `runtime/proofs/alfa1/alfa1.json` |
| 6. Pubblicabilità | OK. |

## Appendice A — Non pubblicabili: infrastruttura

| Gruppo | Schede |
|---|---|
| Infrastruttura | X-1 |
"""

SUMMARY = {
    "esiti": [
        {
            "id": "EPS-1",
            "cosa": "prova",
            "righe": [
                {"r": "riga A", "n": 10, "m": 1.5, "t": 1.1, "u": "USD", "p95": 2.0, "ok": False},
                {"r": "riga B", "n": 12, "m": -0.5, "t": -0.2, "u": "USD", "p95": 2.0, "ok": False},
            ],
        }
    ]
}

PROVE = {
    "runtime/proofs/alfa1/alfa1.json": '{"mes": {"n": 120, "mean": 12.34}}',
    "runtime/proofs/gamma1/gamma1.json": "{}",
    "runtime/proofs/eps1/eps1.json": "{}",
    "runtime/proofs/eta1/eta1.json": '{"anni": {"2019": 1.5, "2020": -0.5, "2021": 2.0}}',
    "runtime/proofs/lambda1/lambda1.json": "{}",
    "runtime/proofs/lambda1/lambda1-biased.json": '{"x": 1}',
    "runtime/proofs/optfull_lim025/x.json": "{}",
    # 99.99 e' dentro 1999.9912 (non e' un valore); 77 e 7.5 stanno nello stesso record, 12 in un altro
    "runtime/proofs/mu1/mu1.json": '{"sparso": {"a": 1999.9912, "b": 12}, "rec": {"n": 77, "mean": 7.5}}',
    "runtime/research/sa-report/summary.json": json.dumps(SUMMARY),
    "docs/research/TEO.txt": "\n".join(
        ["5. MASSIMO E MINIMO DELLA NOTTE: PROBABILITA' DI SUPERAMENTO",
         "Riferimento: range medio fino alle 15:30 e alle 22:00 della notte",  # L2: due dei numeri, ma non il 47
         "Quale sia il lato grande e' moneta (sopra nel 47% dei giorni)",  # L3: il 47 e una parola, ma non gli orari
         "Tutte le sessioni:",
         "massimo superato entro le 15:30 nel 47%, entro le 22:00 nel 69%"]  # L5: tutti i numeri e le parole insieme
    ),
    # tabella di documento: l'intestazione sta 9 righe sopra la riga con i numeri, 40 righe sopra un'altra
    "docs/research/TAB.txt": "\n".join(
        ["4. TABELLA ESCURSIONE MEDIANA PER FINESTRA (sessioni, punti)", "finestra Roma   escursione   meta' centrale"]
        + [f"   altra finestra {chr(97 + i)}   senza numeri" for i in range(7)]
        + ["00:00-08:00 Asia               192        142-235              85",
           "08:00-14:30 Europa             195        160-232              94"]
        + [f"   riga di riempimento {chr(97 + i % 26)}" for i in range(30)]
        + ["    zona lontana 777"]
    ),
}


@pytest.fixture()
def mondo(tmp_path):
    radice = tmp_path / "motore"
    (radice / "docs").mkdir(parents=True)
    (radice / "docs" / "EXECUTION_LEDGER.md").write_text(LEDGER, encoding="utf-8")
    for rel, testo in PROVE.items():
        f = radice / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(testo, encoding="utf-8")
    inv = tmp_path / "inventario.md"
    inv.write_text(INVENTARIO, encoding="utf-8")
    return inv, radice, tmp_path / "out"


def front(md):
    return E.leggi_frontmatter(md.read_text(encoding="utf-8"))[0]


def leggi_md(out, id_):
    return (out / f"{id_}.md").read_text(encoding="utf-8")


def righe_tabella(md):
    esito = md.split("## Esito")[1].split("\n## ")[0]
    return [r for r in esito.splitlines() if r.startswith("|")][2:]


def genera(mondo):
    inv, radice, out = mondo
    return E.genera(inv, radice, out), out


# --- struttura e contenuti di base ---
def test_studio_ok_ha_numero_e_fonte(mondo):
    st, out = genera(mondo)
    md = leggi_md(out, "alfa-1")
    assert "+12,34 USD" in md
    assert "| Risultato | Fonte |" in md
    assert "docs/EXECUTION_LEDGER.md#L103-L104" in md
    assert "## Cosa NON dice" in md
    assert front(out / "alfa-1.md")["pubblicabilita"] == "ok"
    assert st["ok"] >= 1


def test_studio_no_non_genera_file(mondo):
    st, out = genera(mondo)
    assert not (out / "beta-1.md").exists()
    assert "beta-1" not in {r["id"] for r in json.loads((out / "indice.json").read_text(encoding="utf-8"))}
    assert st["no"] == 1


def test_genera_pagina_rifiuta_no():
    with pytest.raises(ValueError):
        E.pagina({"pubblicabilita": "no", "id": "x"}, None)


def test_frontmatter_fisso(mondo):
    _, out = genera(mondo)
    fm = front(out / "alfa-1.md")
    assert list(fm) == [
        "id", "titolo", "data", "strumenti", "finestra", "verdetto",
        "pubblicabilita", "avvertenza", "fonte_ledger", "prove",
    ]
    assert fm["data"] == "2026-10-12" and fm["strumenti"] == ["MES", "MNQ"]
    assert fm["fonte_ledger"] == "docs/EXECUTION_LEDGER.md#L103-L104"
    assert fm["prove"] == ["runtime/proofs/alfa1/alfa1.json"]


def test_indice_ordinato_e_chiavi(mondo):
    _, out = genera(mondo)
    indice = json.loads((out / "indice.json").read_text(encoding="utf-8"))
    date = [r["data"] for r in indice]
    assert date == sorted(date, reverse=True) and date[0] == "2026-10-16"
    base = {"id", "titolo", "data", "strumenti", "verdetto", "pubblicabilita", "grafico", "serie"}
    for r in indice:
        assert set(r) - {"audit"} == base
    assert {r["id"]: r.get("audit") for r in indice if "audit" in r} == {
        "gamma-1": "ritirato", "delta-1": "nota", "lambda-1": "nota",
    }


def test_limit_e_determinismo(mondo):
    inv, radice, out = mondo
    st = E.genera(inv, radice, out, limit=1)
    assert len(list(out.glob("*.md"))) == 1 and st["ok"] + st["avvertenza"] == 1
    out2, out3 = out.parent / "o2", out.parent / "o3"
    E.genera(inv, radice, out2)
    E.genera(inv, radice, out3)
    for f in sorted(out2.iterdir()):
        assert f.read_bytes() == (out3 / f.name).read_bytes()


def test_cli_stampa_conteggi(mondo, capsys):
    inv, radice, out = mondo
    assert E.main(["--inventario", str(inv), "--root", str(radice), "--out", str(out)]) == 0
    s = capsys.readouterr().out
    for k in ("ok=", "avvertenza=", "no=", "skipped=", "prove_mancanti=", "non_riportate="):
        assert k in s


# --- regola (a): i numeri non trovati nella prova citata non si pubblicano ---
def test_numero_non_trovato_non_si_pubblica_e_si_conta(mondo):
    st, out = genera(mondo)
    md = leggi_md(out, "delta-1")
    assert "77,77" not in md  # da nessuna parte
    assert "1 righe della scheda non riportate: la prova citata non le contiene." in md
    assert "non verificabile" not in md
    assert "prova non trovata su disco: runtime/proofs/delta1/delta1.json" in md
    assert st["prove_mancanti"] == 1 and st["non_riportate"] >= 1


def test_numero_entro_tre_righe_si_pubblica_con_la_fonte_vera(mondo):
    _, out = genera(mondo)
    righe = righe_tabella(leggi_md(out, "zeta-1"))
    assert len(righe) == 1 and "+7,77 USD" in righe[0]
    assert righe[0].endswith("| docs/EXECUTION_LEDGER.md#L113-L113 |")
    assert "righe della scheda non riportate" not in leggi_md(out, "zeta-1")


def test_numero_gia_nell_intervallo_citato_niente_riga_vicina_in_piu(tmp_path):
    # come trend-1: "0" e "2" stanno nell'intervallo citato (L5) senza le parole della riga; due righe sopra (L3) una rubrica
    # ha le stesse cifre e le parole. Il ripiego a +-3 righe vale solo per un numero che nell'intervallo non c'e'.
    led = ["riga 1", "riga 2", "rubrica TSMOM portafogli: CONFERMATO se media mensile > 0 con t >= 2", "riga 4",
           "TSMOM: 0 su 2", "riga 6"]
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "EXECUTION_LEDGER.md").write_text("\n".join(led), encoding="utf-8")
    ok, non = E.righe_esito("TSMOM portafogli mensile: 0 confermati su 2", [(5, 5)], [], E.Contesto(tmp_path), [])
    assert non == 0 and [r["fonte"] for r in ok] == ["docs/EXECUTION_LEDGER.md#L5-L5"]


def test_passo_4_preferisce_la_fonte_gia_scelta_per_la_riga(tmp_path):
    # come safehaven-1 (CP-1): la riga cita due intervalli; "0,228" sta con le parole nel secondo (L5-L7), "2019" sta in
    # tutti e due senza le parole. Il 2019 non apre una seconda Fonte (il primo intervallo, L1-L3): basta quella gia' scelta.
    led = ["riga 1", "anno 2019 altro studio", "riga 3", "riga 4", "CP-1 scoperta R2 0,228 portafogli verifica",
           "2019-2025 pendenza", "riga 7"]
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "EXECUTION_LEDGER.md").write_text("\n".join(led), encoding="utf-8")
    riga = "CP-1 scoperta portafogli verifica: R2 0,228, fuori campione 2019"
    ok, non = E.righe_esito(riga, [(1, 3), (5, 7)], [], E.Contesto(tmp_path), [])
    assert non == 0 and [r["fonte"] for r in ok] == ["docs/EXECUTION_LEDGER.md#L5-L7"]


def test_cella_con_studio_escluso_tiene_le_citazioni_in_coda(mondo):
    _, out = genera(mondo)
    righe = righe_tabella(leggi_md(out, "theta-1"))
    assert len(righe) == 1 and "+12,34 USD" in righe[0]
    assert righe[0].endswith("| docs/EXECUTION_LEDGER.md#L103-L103 |")
    assert front(out / "theta-1.md")["fonte_ledger"] == "docs/EXECUTION_LEDGER.md#L103-L103"


# --- regola (b): niente istruzioni di lavoro ---
def test_avvertenze_senza_istruzioni(mondo):
    st, out = genera(mondo)
    assert front(out / "iota-1.md")["avvertenza"] == "dati di terzi solo aggregati"
    assert front(out / "kappa-1.md")["avvertenza"] == ""
    assert front(out / "kappa-1.md")["pubblicabilita"] == "avvertenza"
    assert front(out / "theta-1.md")["avvertenza"] == "dati licenziati solo aggregati."
    assert front(out / "gamma-1.md")["avvertenza"] == "conferma poi ritirata."
    assert {i for i, _, _ in st["avvertenze"]} >= {"iota-1", "kappa-1", "theta-1", "gamma-1"}


def test_nessuna_istruzione_in_nessun_file(mondo):
    _, out = genera(mondo)
    rx = re.compile(r"\b(pubblicar|ripubblic|citare|dichiarare|riportare|includere|serve prima)\w*", re.I)
    for f in out.iterdir():
        assert not rx.search(f.read_text(encoding="utf-8")), f.name
    assert "da NON ripubblicare" not in leggi_md(out, "iota-1")
    assert "- Esplorazione" in leggi_md(out, "iota-1")


# --- regola (c): pagine ritirate ---
def test_ritirato_senza_numeri_ritirati_ma_con_i_fratelli(mondo):
    _, out = genera(mondo)
    md = leggi_md(out, "gamma-1")
    assert "+50,5" not in md and "t 2,40" not in md
    assert "RITIRATA dall'audit" in md and "## Ritiri e correzioni" in md
    righe = righe_tabella(md)
    assert any("CONFERMA RITIRATA" in r for r in righe)  # il motivo dal registro
    assert any("GAMMA-2" in r and "+3,21 bp" in r for r in righe)  # lo studio non ritirato resta
    assert not (out / "gamma-1.dati.json").exists()
    assert front(out / "gamma-1.md")["audit"] == {"stato": "ritirato", "id": ["GAMMA-1"]}
    assert "(AUDIT-FABLE)" in md and "va pubblicata" not in md


# --- regola (d): l'etichetta viene dal registro ---
def test_verdetto_dal_solo_locatore_principale(mondo):
    _, out = genera(mondo)
    assert front(out / "alfa-1.md")["verdetto"] == "non confermata"
    assert front(out / "psi-1.md")["verdetto"] == "fail"  # L113 e' il locatore della scheda
    assert front(out / "eps-1.md")["verdetto"] == "non confermata"


def test_parole_di_righe_secondarie_non_sono_verdetti(mondo):
    _, out = genera(mondo)
    # ZETA cita L110 e trova i numeri su L113 ("FAIL"); OMEGA cita anche L114 ("NON CONFERMATA"): solo L110 e' il locatore
    for id_ in ("zeta-1", "omega-1"):
        assert front(out / f"{id_}.md")["verdetto"] == "senza verdetto nel registro"
    assert len(righe_tabella(leggi_md(out, "omega-1"))) == 2  # le righe secondarie restano pubblicate, con la loro Fonte
    assert "docs/EXECUTION_LEDGER.md#L114-L114" in leggi_md(out, "omega-1")


def test_parole_deduplicate(mondo):
    inv, radice, out = mondo
    ctx = E.Contesto(radice)
    assert E.parole_registro(ctx, [(103, 103), (103, 104), (103, 103)]) == "non confermata"
    assert E.parole_registro(ctx, [(109, 109)]) == "non confermato"  # "CONFERMA RITIRATA" non e' ancorata
    assert E.parole_registro(ctx, [(110, 110)]) == "senza verdetto nel registro"
    assert E.parole_registro(ctx, []) == "senza verdetto nel registro"


SENZA = "senza verdetto nel registro"


@pytest.mark.parametrize(
    "riga, atteso",
    [
        (115, SENZA),  # lab-2: "Suite: 120 PASS, 0 FAIL" sono conteggi di test
        (116, SENZA),  # assorb-1: "Verdetto: CONFERMATO se ..." e' la definizione della rubrica
        (117, SENZA),  # oc-explore-1: "CONFERMATA dopo 60 giorni-segnale se ..." e' una rubrica futura
        (118, SENZA),  # phase-1: "2 test PASS" e "0 CONFERMATE" non sono un verdetto
        (125, SENZA),  # "Outcome: CONFERMATA solo se ..." e' una definizione
        (126, SENZA),  # "Esito: 3643 PASS, 0 FAIL": la parola e' preceduta da un conteggio
        (119, "non confermata"),  # "Esito X (...): PAROLA"
        (120, "parziale"),  # "Verdetto: PAROLA"
        (121, "pass · non confermata"),  # "Esito PAROLA" + "verdetto PAROLA"
        (122, "blocked_env"),  # "Esito: PAROLA" ("non PASS" non e' ancorato)
        (123, "non confermata"),  # "verdetto PAROLA"
        (124, "non confermata"),  # "esito PAROLA"
        (127, "descrittivo"),  # "Outcome: PAROLA"
        (131, "non confermata"),  # famiglia A: "Esito ID (provenienza lunga, 7 PASS ...): PAROLA"; il "7 PASS" dentro la parentesi non conta
        (132, SENZA),  # famiglia A, negativo: i due punti non seguono la parentesi e la frase supera i 100 caratteri
        (134, SENZA),  # "Esito Z-1 (a.json): 0 CONFERMATE su 4": plurale dopo un conteggio
        (135, "pass"),  # "- Esito PASS" a inizio di punto elenco
        (136, SENZA),  # "ma un esito NON CONFERMATA e' informativo ...": frase ipotetica a meta' riga
        (139, "descrittivo"),  # "Esito (a.json): PAROLA" senza ID
        (140, "pass · non confermata"),  # famiglia A: "PASS, NON CONFERMATA" (SAFEHAVEN-1, L9863): il PASS della prova e il verdetto di ricerca
        (141, "pass"),  # catena: "PASS, 2 CONFERMATE su 4" -> il conteggio non e' un verdetto
        (142, "pass"),  # catena: "PASS, CONFERMATA se ..." -> definizione di rubrica
        (143, "blocked_env"),  # catena: solo dopo PASS o FAIL
    ],
)
def test_verdetto_solo_da_frasi_ancorate(mondo, riga, atteso):
    inv, radice, out = mondo
    assert E.parole_registro(E.Contesto(radice), [(riga, riga)]) == atteso


def test_plurali_e_id_nelle_schede_con_piu_studi(mondo):
    inv, radice, out = mondo
    ctx = E.Contesto(radice)
    # L133: "Esito OVN-1 (a.json): CONFERMATI ...; Esito GOLDN-1 (b.json): NON CONFERMATO"
    assert E.parole_registro(ctx, [(133, 133)], ("OVN-1", "GOLDN-1")) == "OVN-1: confermati · GOLDN-1: non confermato"
    assert E.parole_registro(ctx, [(133, 133)], ("GOLDN-1", "OVN-1")) == "GOLDN-1: non confermato · OVN-1: confermati"
    assert E.parole_registro(ctx, [(133, 133)], ("OVN-1",)) == "confermati"  # un solo ID: nessun prefisso; il fratello e' escluso
    assert E.parole_registro(ctx, [(133, 133)]) == "confermati · non confermato"  # senza ID di scheda: parole nude
    assert E.parole_registro(ctx, [(134, 134)], ("Z-1", "W-1")) == SENZA  # "0 CONFERMATE": il conteggio blocca il plurale


def test_famiglia_b_id_uguale_parola_solo_per_gli_id_della_scheda(mondo):
    inv, radice, out = mondo
    ctx = E.Contesto(radice)
    # L137: "... CONFERMA RITIRATA, VOLREV-1 = NON CONFERMATO" ("registrato CONFERMATO" non e' ancorato)
    assert E.parole_registro(ctx, [(137, 137)], ("VOLREV-1", "H-NEXT-8")) == "VOLREV-1: non confermato"
    assert E.parole_registro(ctx, [(137, 137)], ("VOLREV-1",)) == "non confermato"
    assert E.parole_registro(ctx, [(137, 137)], ("ALTRO-1", "H-NEXT-8")) == SENZA  # non e' un ID della scheda
    assert E.parole_registro(ctx, [(137, 137)]) == SENZA  # senza ID di scheda la famiglia B non si applica


def test_pagina_con_due_studi_porta_gli_id_nell_etichetta(mondo):
    _, out = genera(mondo)
    assert front(out / "ovn-1.md")["verdetto"] == "OVN-1: confermati · GOLDN-1: non confermato"


def test_numero_sorgente_dentro_orari_e_rapporti(mondo):
    assert not E.ha_numero("47", "ripartito alle 20:47 su 250")  # "20:47" e' un orario, un token solo
    assert E.ha_numero("20:47", "ripartito alle 20:47")
    assert E.ha_numero("69", "69 sessioni su 250") and E.ha_numero("69", "casi 30/69")  # k/n restano due numeri
    assert not E.ha_numero("5", "sotto il p95") and not E.ha_numero("0", "MMLU-20")
    assert E.ha_numero("2.1.0", "client ib_async 2.1.0") and not E.ha_numero("2.1", "client ib_async 2.1.0")
    assert E.ha_numero("1,5", "media 1.5") and E.ha_numero("29.900", "tondo 29900")
    assert E.ha_numero("-3,21", "MNQ -3,21 USD") and not E.ha_numero("3,21", "MNQ -3,21 USD")


def test_fonte_e_dove_numero_e_parole_stanno_insieme(mondo):
    _, out = genera(mondo)
    md = leggi_md(out, "teo-1")
    righe = righe_tabella(md)
    # L138 ha "69" (in "69 sessioni") e gli orari, ma non "47" e non le parole della riga: la riga vera e' nel documento
    # il documento ha il 47 anche alla L3 e gli orari alla L2: la Fonte e' la L5, dove ci sono tutti i numeri e le parole
    assert len(righe) == 1 and righe[0].endswith("| docs/research/TEO.txt#L5-L5 |")
    assert "righe della scheda non riportate" not in md
    # un numero che nel registro sta solo dentro "20:47" non e' verificato: nessuna riga, frase vera
    md2 = leggi_md(out, "teo-2")
    assert "1 righe della scheda non riportate: la prova citata non le contiene." in md2 and "MES 47" not in md2


def test_pagine_con_solo_conteggi_o_rubriche_senza_verdetto(mondo):
    _, out = genera(mondo)
    for id_ in ("chi-1", "rho-1"):
        assert front(out / f"{id_}.md")["verdetto"] == SENZA
        assert front(out / f"{id_}.md")["fonte_ledger"] in ("docs/EXECUTION_LEDGER.md#L115-L115", "docs/EXECUTION_LEDGER.md#L117-L117")


def test_versione_con_punti_e_un_token_e_i_codici_non_danno_numeri(mondo):
    assert E.numeri("client IB (ib_async 2.1.0), 9 test PASS") == ["2.1.0", "9"]
    assert E.numeri("sotto il p95 dei placebo (85,83); DSR1000 su L38, 27,3") == ["85,83", "27,3"]
    _, out = genera(mondo)
    md = leggi_md(out, "sigma-1")
    assert "righe della scheda non riportate" not in md
    righe = righe_tabella(md)
    assert len(righe) == 1 and righe[0].endswith("| docs/EXECUTION_LEDGER.md#L128-L129 |")


def test_numeri_in_tabella_di_documento_per_sezione_non_per_riga(mondo):
    _, out = genera(mondo)
    md = leggi_md(out, "tau-1")
    assert "righe della scheda non riportate" not in md
    righe = righe_tabella(md)
    assert len(righe) == 1 and righe[0].endswith("| docs/research/TAB.txt#L10-L10 · docs/research/TAB.txt#L11-L11 |")
    # la frase compare solo se il numero manca davvero: qui sta 30 righe sotto l'intestazione
    md = leggi_md(out, "upsilon-1")
    assert "1 righe della scheda non riportate: la prova citata non le contiene." in md and "777" not in md


def test_ritirato_ha_il_locatore_della_riga_dell_audit(mondo):
    _, out = genera(mondo)
    assert front(out / "gamma-1.md")["fonte_ledger"] == "docs/EXECUTION_LEDGER.md#L109-L109"
    assert front(out / "gamma-1.md")["verdetto"] == "non confermato"


@pytest.mark.parametrize(
    "clausola, atteso",
    [
        ("la heatmap PNG mostra il book L2 di un giorno (dati di mercato licenziati): pubblicarla solo se la licenza lo consente",
         "la heatmap PNG mostra il book L2 di un giorno (dati di mercato licenziati)"),
        ("orari ufficiali di terzi: citare fonti UFF come nel documento", "orari ufficiali di terzi"),
        ("regole pubbliche di terzi, citare fonti", "regole pubbliche di terzi"),
        ("dati di mercato di terzi (ES 1m) non ripubblicabili", ""),  # fatto e istruzione non separabili: cade
        ("pubblicare solo i numeri del walk-forward, non il resto", ""),  # niente frammenti sospesi
        ("solo aggregati: citare", ""),  # il prefisso e' troppo corto per reggere da solo
        ("dati licenziati solo aggregati", "dati licenziati solo aggregati"),  # nessuna istruzione: intatta
    ],
)
def test_clausola_mista_tiene_il_prefisso_fattuale(clausola, atteso):
    assert E.pulisci_clausola(clausola) == atteso


def test_avvertenza_mista_tiene_la_parte_fattuale(mondo):
    _, out = genera(mondo)
    assert front(out / "fi-1.md")["avvertenza"] == "la heatmap PNG mostra il book L2 di un giorno (dati licenziati)"


def test_senza_parola_nelle_righe_citate_senza_verdetto(mondo):
    _, out = genera(mondo)
    assert front(out / "lambda-1.md")["verdetto"] == "senza verdetto nel registro"  # "aiutano" non e' un verdetto
    assert front(out / "eta-1.md")["verdetto"] == "non confermata"


def test_audit_non_sovrascrive_il_verdetto(mondo):
    _, out = genera(mondo)
    fm = front(out / "delta-1.md")
    assert fm["audit"] == {"stato": "nota", "id": ["DELTA-1"]}
    assert fm["verdetto"] == "senza verdetto nel registro"  # L108 non ha parole di verdetto
    g = front(out / "gamma-1.md")
    assert "non confermato" in g["verdetto"] and g["verdetto"] != "ritirato"


def test_ritirato_solo_per_gli_id_dichiarati_ritirati_il_resto_e_nota(mondo):
    _, out = genera(mondo)
    stati = {p.stem: front(p)["audit"]["stato"] for p in out.glob("*.md") if "audit" in front(p)}
    assert stati == {"gamma-1": "ritirato", "delta-1": "nota", "lambda-1": "nota"}  # "corretto" non esiste piu'
    assert front(out / "gamma-1.md")["audit"]["id"] == ["GAMMA-1"]  # non GAMMA-2
    assert "corretto" not in (out / "indice.json").read_text(encoding="utf-8")


# --- LIMALL-1 / OPT-COND-1 non compaiono ---
def test_studi_senza_esito_non_compaiono(mondo):
    _, out = genera(mondo)
    for f in out.iterdir():
        t = f.read_text(encoding="utf-8")
        assert "LIMALL" not in t and "OPT-COND" not in t and "optfull_lim025" not in t, f.name
    fm = front(out / "theta-1.md")
    assert fm["titolo"] == "THETA-1 — prova con uno studio senza esito"
    assert "LIMALL" not in fm["finestra"] and fm["finestra"].endswith("2020-2026")
    assert fm["prove"] == ["runtime/proofs/alfa1/alfa1.json"]


# --- fonte controllata nel contesto ---
def test_json_conta_solo_come_valore_nello_stesso_record(mondo):
    _, out = genera(mondo)
    md = leggi_md(out, "mu-1")
    righe = righe_tabella(md)
    assert len(righe) == 1 and righe[0].startswith("| n 77 media 7,5 |")
    assert righe[0].endswith("| runtime/proofs/mu1/mu1.json |")
    assert "99,99" not in md and "valore 12" not in md  # 99.99 e' dentro 1999.9912; 12 sta in un altro record
    assert "2 righe della scheda non riportate" in md


def test_file_da_non_usare_fuori_da_prove(mondo):
    _, out = genera(mondo)
    assert front(out / "lambda-1.md")["prove"] == ["runtime/proofs/lambda1/lambda1.json"]
    prove = leggi_md(out, "lambda-1").split("## Prove")[1]
    assert "biased" not in prove


# --- frammenti ---
def test_frammenti_senza_soggetto_si_uniscono(mondo):
    _, out = genera(mondo)
    md = leggi_md(out, "nu-1")
    righe = righe_tabella(md)
    assert len(righe) == 1 and "1 -2,84; 2 -1,57" in righe[0]
    assert "(AUDIT-FABLE)" in md and ", )" not in md


# --- serie e tabelle strutturate ---
def test_dati_json_da_summary_e_indice_con_grafico(mondo):
    _, out = genera(mondo)
    d = json.loads((out / "eps-1.dati.json").read_text(encoding="utf-8"))
    assert d["tipo"] == "tabella"
    assert d["fonte"] == "runtime/research/sa-report/summary.json"
    assert d["colonne"][0] == "r" and d["righe"][0][0] == "riga A"
    ind = {r["id"]: r for r in json.loads((out / "indice.json").read_text(encoding="utf-8"))}
    assert ind["eps-1"]["grafico"] is True and ind["alfa-1"]["grafico"] is False
    # serie solo per i dati.json di tipo serie (l'indice carica solo quelli per le sparkline)
    assert ind["eps-1"]["serie"] is False and ind["eta-1"]["serie"] is True and ind["alfa-1"]["serie"] is False


def test_serie_annuale_da_prova_json(mondo):
    _, out = genera(mondo)
    d = json.loads((out / "eta-1.dati.json").read_text(encoding="utf-8"))
    assert d["tipo"] == "serie" and d["colonne"] == ["anno", "anni"]
    assert d["righe"] == [["2019", 1.5], ["2020", -0.5], ["2021", 2.0]]
    assert d["fonte"] == "runtime/proofs/eta1/eta1.json#/anni"
    assert "## Grafico" in leggi_md(out, "eta-1")


def test_metodo_md_elenca_le_stesse_parole_del_codice():
    # la lista mostrata in /metodo e' quella che il generatore accetta davvero (_PAROLA), ne' una in piu' ne' una in meno
    metodo = (Path(__file__).resolve().parents[1] / "src" / "content" / "metodo.md").read_text(encoding="utf-8")
    elenco = re.search(r"Le parole sono ([^.(]+)", metodo).group(1)
    mostrate = {p.strip() for p in elenco.split(",")}
    radici = ["CONFERMAT", "ADOTTAT", "RITIRAT", "PARZIAL", "DESCRITTIV"]
    candidate = {r + s for r in radici for s in "AOIE"} | {"PASS", "FAIL", "BLOCKED_ENV", "NOT_RUN"}
    candidate |= {"NON " + c for c in candidate}
    accettate = {c for c in candidate if re.fullmatch(E._PAROLA, c)}
    assert mostrate == accettate
