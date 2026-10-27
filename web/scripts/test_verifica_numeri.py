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


# ---- fix round 1 (FREQ-SITO-3): segno, guard dell'arrotondamento, numeri di riga, uso errato

MENO = "\N{MINUS SIGN}"


def prova(tmp_path, sorgente, celle, *opzioni):
    """Una tabella con una riga per cella di `celle`, tutte con Fonte = prova.txt (= `sorgente`, in una radice di scratch)."""
    rad = tmp_path / "rad"
    rad.mkdir(exist_ok=True)
    (rad / "prova.txt").write_text(sorgente, encoding="utf-8")
    righe = "".join(f"| r{i} | {c} | prova.txt |\n" for i, c in enumerate(celle))
    f = md(tmp_path, (TAB + righe).rstrip("\n"), prove="[prova.txt]")
    return esegui("--root", rad, *opzioni, f)


def test_negativo_presente_nella_fonte_e_ok(tmp_path):
    sorgente = f"Delta -0.2301; Brier {MENO}0.5; Z=-0.12; (-3/5)\n"
    celle = ["-0.2301", f"{MENO}0.2301", "-0.5", f"{MENO}0,5", f"Z={MENO}0.12", "(-3/5)"]
    rc, out = prova(tmp_path, sorgente, celle)
    assert rc == 0, out
    assert "0 mancanti" in out


def test_negativo_con_fonte_positiva_e_mancante_e_nomina_il_segno(tmp_path):
    rc, out = prova(tmp_path, "Delta 0.2301 e 0.5\n", ["-0.2301", f"{MENO}0.5"])
    assert rc == 1
    assert "numero -0.2301 non trovato" in out and "numero -0.5 non trovato" in out  # U+2212 normalizzato a '-'
    assert out.count("non trovato") == 2


def test_positivo_con_fonte_negativa_e_mancante(tmp_path):
    rc, out = prova(tmp_path, f"Delta -0.5 e {MENO}0.7\n", ["0.5", "0.7"])
    assert rc == 1 and out.count("non trovato") == 2, out


def test_trattini_di_intervallo_e_date_non_sono_segni(tmp_path):
    sorgente = "tra 10-20 e 0.57-0.58, dal 2026-10-26, righe L10-L20, serie LENTI-1\n"
    rc, out = prova(tmp_path, sorgente, ["10-20", "0.57-0.58", "2026-10-26", "10, 20", "LENTI-1"])
    assert rc == 0, out


def test_arrotondamento_rispetta_il_segno(tmp_path):
    sorgente = "x -0.5789\n"
    assert prova(tmp_path, sorgente, ["-0.58"], "--rounding")[0] == 0
    rc, out = prova(tmp_path, sorgente, ["0.58"], "--rounding")
    assert rc == 1 and "numero 0.58 non trovato" in out


def test_rounding_non_va_in_crash_su_date_orari_e_migliaia(tmp_path):
    rc, out = prova(tmp_path, "niente di tutto cio'\n", ["2099-01-01", "10:45", "1,234,567", "1.234.567"], "--rounding")
    assert rc == 1 and "Traceback" not in out, out
    assert out.count("non trovato") == 4, out


def test_valore_prefisso_di_un_numero_piu_lungo_e_mancante(tmp_path):
    rc, out = prova(tmp_path, "Tasso 0.5791 su 1234 barre\n", ["0.57", "123", "0.579"])
    assert rc == 1 and out.count("non trovato") == 3, out


def test_numeri_di_riga_come_negli_editor_non_come_splitlines(tmp_path):
    # splitlines() spezza anche su U+2028: sposterebbe le righe del ledger e quelle dell'md
    rad = tmp_path / "rad"
    (rad / "docs").mkdir(parents=True)
    (rad / "docs" / "EXECUTION_LEDGER.md").write_text("uno\ndue\N{LINE SEPARATOR}due-bis\nvalore 4242\nquattro 5252\n", encoding="utf-8")
    righe = "prosa\N{LINE SEPARATOR}ancora prosa\n\n" + TAB + "| a | 4242 | ledger L3 |\n| b | 5252 | ledger L3 |"
    rc, out = esegui("--root", rad, md(tmp_path, righe, prove="[]"))
    assert rc == 1 and out.count("non trovato") == 1, out  # 4242 sta alla riga 3, 5252 alla 4
    assert "numero 5252" in out
    assert "x.md:11:" in out, out  # riga dell'editor: i separatori Unicode non vanno contati


def test_crlf_non_sposta_le_righe(tmp_path):
    rad = tmp_path / "rad"
    (rad / "docs").mkdir(parents=True)
    (rad / "docs" / "EXECUTION_LEDGER.md").write_bytes(b"uno\r\ndue\r\nvalore 4242\r\nquattro 5252\r\n")
    testo = f"---\nid: x\nprove: []\n---\n\n{TAB}| a | 4242 | ledger L3 |\n| b | 5252 | ledger L3 |\n"
    (tmp_path / "x.md").write_bytes(testo.replace("\n", "\r\n").encode())
    rc, out = esegui("--root", rad, tmp_path / "x.md")
    assert rc == 1 and out.count("non trovato") == 1 and "numero 5252" in out and "x.md:9:" in out, out


def test_opzione_sconosciuta_esce_2():
    assert esegui("--non-esiste")[0] == 2


# ---- fix round 2: un numero comincia solo a confine di parola; una versione a punti e' un token solo

def test_cifre_dopo_lettere_o_cifre_non_sono_numeri(tmp_path):
    # "p95" non e' 5, "MMLU-20" non e' 0, "DSR1000" non e' 1000: la fonte non ha ne' 5 ne' 0 ne' 1000 da soli
    rc, out = prova(tmp_path, "placebo 109 e valori 19, 20 su DSR1000\n", ["placebo p95 109", "MMLU-20 19/20", "DSR1000"])
    assert rc == 0, out
    assert "3 numeri verificati" in out, out  # 109, 19, 20: nient'altro e' un numero


def test_versione_a_punti_e_un_token_e_si_confronta_intera(tmp_path):
    rc, out = prova(tmp_path, "client ib_async 2.1.0 e 3.2.10.\n", ["ib_async 2.1.0", "versione 3.2.10"])
    assert rc == 0, out
    assert "2 numeri verificati" in out, out


def test_versione_a_punti_assente_e_mancante_col_numero_intero(tmp_path):
    # la fonte ha 2.1 e 0 ma non 2.1.0: manca UN numero, "2.1.0", non "2.1" e "0"
    rc, out = prova(tmp_path, "client ib_async 2.1 e 0\n", ["ib_async 2.1.0"])
    assert rc == 1 and out.count("non trovato") == 1 and "numero 2.1.0 non trovato" in out, out


def test_lettera_trattino_numero_non_e_un_numero_firmato(tmp_path):
    # "x-5" e' un identificatore: dalla tabella non esce un numero, e nella fonte "x-5" non vale "-5"
    rc, out = prova(tmp_path, "7\n", ["x-5", "7"])
    assert rc == 0 and "1 numeri verificati" in out, out
    rc, out = prova(tmp_path, "x-5 e 7\n", ["-5"])
    assert rc == 1 and "numero -5 non trovato" in out, out


def test_confine_di_parola_non_rompe_negativi_kn_date_virgola_e_migliaia(tmp_path):
    sorgente = "d -0.5; 110/190; 2026-10-26 10:45; 3,5; 1.234; 1.234.567,89 e -2,64 (-3)\n"
    celle = ["-0.5", "110/190", "2026-10-26 10:45", "3,5", "1.234", "1.234.567,89", "-2,64", "(-3)"]
    rc, out = prova(tmp_path, sorgente, celle)
    assert rc == 0, out
    assert "10 numeri verificati" in out, out  # -0.5, 110, 190, data, ora, 3,5, 1.234, 1.234.567,89, -2,64, -3
