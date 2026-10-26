"""Test di estrai_ricerche.py su un inventario finto (nessun dato reale).

Uso: .venv\\Scripts\\python.exe -m pytest web/scripts/test_estrai.py
"""
import json
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
        "MES 120 trade +12,34 USD (t 1,50); MNQ 80 trade -3,21 USD",
        "q 0,48 placebo p95 9,9",
        "riga 105",
        "riga 106",
        "gamma +50,5 bp t 2,40",
        "riga 108",
        "riga 109",
        "riga 110",
    ]
)

INVENTARIO = """# Inventario finto

## Ritiri, correzioni e margini sottili da riportare insieme ai risultati (prima di pubblicare numeri)

1. **GAMMA-1 (L109)**: la conferma e' stata RITIRATA dall'audit (artefatto di cambio contratto): ora "NON CONFERMATO".
2. **DELTA-1 (L108)**: prima misura corretta (contava due volte lo stesso trade).

## Indice sintetico

| # | Scheda | ID | Verdetto (come scritto, inizio dell'esito) | Pubblicabilità |
|---|---|---|---|---|
| 1 | ALFA-1 | 1 | "NON CONFERMATA": MES 120 trade. | OK |
| 2 | BETA-1 | 1 | "descrittivo". | NO |
| 3 | GAMMA-1 | 1 | "CONFERMATO" (poi ritirato). | OK con avvertenza |
| 4 | DELTA-1 | 1 | "descrittivo". | OK con avvertenza |
| 5 | EPS-1 | 1 | "NON CONFERMATA". | OK |

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

### GAMMA-1 — studio ritirato
| Voce | Contenuto |
|---|---|
| 1. Identità | 14/10/2026; MES 1 minuto; domanda: il segnale gamma regge? |
| 2. Metodo | Terzili. |
| 3. Esito | "CONFERMATO": gamma +50,5 bp t 2,40 (L107). |
| 4. Regola di lettura | Solo descrittivo. |
| 5. Prove | `runtime/proofs/gamma1/gamma1.json` |
| 6. Pubblicabilità | OK con avvertenza: conferma poi ritirata. |

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
| 3. Esito | "NON CONFERMATA": riga A media 1,5 USD (L103). |
| 4. Regola di lettura | Nessuna. |
| 5. Prove | `runtime/proofs/eps1/eps1.json` |
| 6. Pubblicabilità | OK. |

### ETA-1 — studio con serie annuale
| Voce | Contenuto |
|---|---|
| 1. Identità | 11/10/2026; MNQ; domanda: come va anno per anno? |
| 2. Metodo | Un risultato per anno. |
| 3. Esito | "descrittivo": MNQ 80 trade (L103). |
| 4. Regola di lettura | Nessuna. |
| 5. Prove | `runtime/proofs/eta1/eta1.json` |
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


@pytest.fixture()
def mondo(tmp_path):
    radice = tmp_path / "motore"
    (radice / "docs").mkdir(parents=True)
    (radice / "docs" / "EXECUTION_LEDGER.md").write_text(LEDGER, encoding="utf-8")
    for rel, testo in {
        "runtime/proofs/alfa1/alfa1.json": '{"mes": {"n": 120, "mean": 12.34}}',
        "runtime/proofs/gamma1/gamma1.json": "{}",
        "runtime/proofs/eps1/eps1.json": "{}",
        "runtime/proofs/eta1/eta1.json": '{"anni": {"2019": 1.5, "2020": -0.5, "2021": 2.0}}',
        "runtime/research/sa-report/summary.json": json.dumps(SUMMARY),
    }.items():
        f = radice / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(testo, encoding="utf-8")
    inv = tmp_path / "inventario.md"
    inv.write_text(INVENTARIO, encoding="utf-8")
    return inv, radice, tmp_path / "out"


def front(md):
    return E.leggi_frontmatter(md.read_text(encoding="utf-8"))[0]


def test_studio_ok_ha_numero_e_fonte(mondo):
    inv, radice, out = mondo
    st = E.genera(inv, radice, out)
    md = (out / "alfa-1.md").read_text(encoding="utf-8")
    assert "+12,34 USD" in md
    assert "| Risultato | Fonte |" in md
    assert "docs/EXECUTION_LEDGER.md#L103-L104" in md
    assert "## Cosa NON dice" in md
    assert front(out / "alfa-1.md")["pubblicabilita"] == "ok"
    assert st["ok"] >= 1


def test_studio_no_non_genera_file(mondo):
    inv, radice, out = mondo
    st = E.genera(inv, radice, out)
    assert not (out / "beta-1.md").exists()
    assert "beta-1" not in {r["id"] for r in json.loads((out / "indice.json").read_text(encoding="utf-8"))}
    assert st["no"] == 1


def test_genera_pagina_rifiuta_no():
    with pytest.raises(ValueError):
        E.pagina({"pubblicabilita": "no", "id": "x"}, None)


def test_ritirato_ha_verdetto_e_parole_dell_audit(mondo):
    inv, radice, out = mondo
    E.genera(inv, radice, out)
    assert front(out / "gamma-1.md")["verdetto"] == "ritirato"
    md = (out / "gamma-1.md").read_text(encoding="utf-8")
    assert "RITIRATA dall'audit" in md
    assert front(out / "delta-1.md")["verdetto"] == "corretto"


def test_prova_mancante_dichiarata_e_numero_non_verificabile(mondo):
    inv, radice, out = mondo
    st = E.genera(inv, radice, out)
    md = (out / "delta-1.md").read_text(encoding="utf-8")
    assert "prova non trovata su disco: runtime/proofs/delta1/delta1.json" in md
    assert st["prove_mancanti"] == 1
    # 77,77 non e' nel ledger citato (L108): fuori dalla tabella, marcato non verificabile
    tabella = md.split("## Esito")[1].split("## Cosa NON dice")[0]
    righe_tab = [r for r in tabella.splitlines() if r.startswith("|")]
    assert not any("77,77" in r for r in righe_tab)
    assert "non verificabile" in tabella and "77,77" in tabella


def test_dati_json_da_summary_e_indice_con_grafico(mondo):
    inv, radice, out = mondo
    E.genera(inv, radice, out)
    d = json.loads((out / "eps-1.dati.json").read_text(encoding="utf-8"))
    assert d["tipo"] == "tabella"
    assert d["fonte"] == "runtime/research/sa-report/summary.json"
    assert d["colonne"][0] == "r" and d["righe"][0][0] == "riga A"
    ind = {r["id"]: r for r in json.loads((out / "indice.json").read_text(encoding="utf-8"))}
    assert ind["eps-1"]["grafico"] is True and ind["alfa-1"]["grafico"] is False
    assert not (out / "gamma-1.dati.json").exists()  # ritirato: nessun grafico


def test_serie_annuale_da_prova_json(mondo):
    inv, radice, out = mondo
    E.genera(inv, radice, out)
    d = json.loads((out / "eta-1.dati.json").read_text(encoding="utf-8"))
    assert d["tipo"] == "serie" and d["colonne"] == ["anno", "anni"]
    assert d["righe"] == [["2019", 1.5], ["2020", -0.5], ["2021", 2.0]]
    assert d["fonte"] == "runtime/proofs/eta1/eta1.json#/anni"
    assert "## Grafico" in (out / "eta-1.md").read_text(encoding="utf-8")


def test_indice_ordinato_per_data_decrescente(mondo):
    inv, radice, out = mondo
    E.genera(inv, radice, out)
    date = [r["data"] for r in json.loads((out / "indice.json").read_text(encoding="utf-8"))]
    assert date == sorted(date, reverse=True) and date[0] == "2026-10-16"
    assert set(json.loads((out / "indice.json").read_text(encoding="utf-8"))[0]) == {
        "id", "titolo", "data", "strumenti", "verdetto", "pubblicabilita", "grafico",
    }


def test_frontmatter_fisso(mondo):
    inv, radice, out = mondo
    E.genera(inv, radice, out)
    fm = front(out / "alfa-1.md")
    assert list(fm) == [
        "id", "titolo", "data", "strumenti", "finestra", "verdetto",
        "pubblicabilita", "avvertenza", "fonte_ledger", "prove",
    ]
    assert fm["data"] == "2026-10-12" and fm["strumenti"] == ["MES", "MNQ"]
    assert fm["verdetto"] == "non confermata"
    assert fm["fonte_ledger"] == "docs/EXECUTION_LEDGER.md#L103-L104"
    assert fm["prove"] == ["runtime/proofs/alfa1/alfa1.json"]


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
    for k in ("ok=", "avvertenza=", "no=", "skipped=", "prove_mancanti="):
        assert k in s
