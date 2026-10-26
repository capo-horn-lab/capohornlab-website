"""Test di verifica_numeri.py su fixture (scripts/fixtures/numeri).

Uso: .venv\\Scripts\\python.exe -m pytest web/scripts/test_verifica_numeri.py
"""
import subprocess
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
SCRIPT = AQUI / "verifica_numeri.py"
FIX = AQUI / "fixtures" / "numeri"
ROOT = FIX / "root"


def esegui(*args):
    p = subprocess.run(
        [sys.executable, str(SCRIPT), "--root", str(ROOT), *map(str, args)],
        capture_output=True, text=True, encoding="utf-8",
    )
    return p.returncode, p.stdout + p.stderr


def md(tmp_path, righe, prove="[runtime/proofs/prova1/report.md]", extra=""):
    f = tmp_path / "x.md"
    f.write_text(f"---\nid: x\nprove: {prove}\n{extra}---\n\n{righe}\n", encoding="utf-8")
    return f


TAB = "| Misura | Valore | Fonte |\n|---|---|---|\n"


def test_tutto_trovato_esce_0():
    rc, out = esegui(FIX / "ok")
    assert rc == 0, out
    assert "0 mancanti" in out


def test_numero_sbagliato_esce_1_e_lo_nomina():
    rc, out = esegui(FIX / "bad")
    assert rc == 1
    assert "0.2999" in out and "prova-2.md" in out
    assert out.count("non trovato") == 1  # solo quello sbagliato


def test_arrotondamento_spento_di_default():
    rc, out = esegui(FIX / "arrotondamento")
    assert rc == 1 and "0.579" in out and "0.58" in out


def test_arrotondamento_acceso_accetta_piu_decimali_nella_fonte():
    rc, out = esegui("--rounding", FIX / "arrotondamento")
    assert rc == 0, out


def test_arrotondamento_non_accetta_troncamento_ne_interi():
    rc, out = esegui("--rounding", FIX / "arrotondamento_troncato")
    assert rc == 1 and "0.578" in out
    rc, out = esegui("--rounding", FIX / "arrotondamento_intero")
    assert rc == 1 and "58" in out


def test_ledger_fuori_intervallo(tmp_path):
    f = md(tmp_path, TAB + "| Fuori | 999 | ledger L3-L4 |")
    rc, out = esegui(f)
    assert rc == 1 and "999" in out
    f = md(tmp_path, TAB + "| Dentro | 999 | ledger L6 |")
    assert esegui(f)[0] == 0


def test_ledger_senza_intervallo_e_errore(tmp_path):
    f = md(tmp_path, TAB + "| Barre | 4321 | ledger |")
    rc, out = esegui(f)
    assert rc == 1 and "intervallo" in out


def test_riga_con_numeri_senza_fonte(tmp_path):
    f = md(tmp_path, TAB + "| Barre | 1234 |  |")
    rc, out = esegui(f)
    assert rc == 1 and "senza fonte" in out


def test_fonte_citata_inesistente(tmp_path):
    f = md(tmp_path, TAB + "| Barre | 1234 | nonesiste.json |")
    rc, out = esegui(f)
    assert rc == 1 and "nonesiste.json" in out


def test_prova_del_frontmatter_inesistente(tmp_path):
    f = md(tmp_path, TAB + "| Barre | 1234 | report.md |", prove="[runtime/proofs/mancante.md, runtime/proofs/prova1/report.md]")
    rc, out = esegui(f)
    assert rc == 1 and "mancante.md" in out


def test_senza_tabella_con_fonte_e_errore(tmp_path):
    f = md(tmp_path, "| Misura | Valore |\n|---|---|\n| Barre | 1234 |")
    rc, out = esegui(f)
    assert rc == 1 and "Fonte" in out


def test_nessun_file_o_percorso_inesistente_esce_2(tmp_path):
    assert esegui(tmp_path)[0] == 2
    assert esegui(tmp_path / "nope")[0] == 2


def test_help_dichiara_che_la_prosa_non_si_controlla():
    p = subprocess.run([sys.executable, str(SCRIPT), "--help"], capture_output=True, text=True, encoding="utf-8")
    assert p.returncode == 0
    assert "prosa" in p.stdout and "--rounding" in p.stdout
