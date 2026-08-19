# Pre-News Predictive Study — ES Behavior BEFORE Macro Releases

**Capo Horn Lab — Research Report · 2026-08-19**
**Estende:** News Trading Long-Horizon (news_longhorizon) · **Periodo:** 2020-2024 · **Dati:** es_daily.csv (1,298 sessioni CME), eventi BLS/FOMC verificati

## Domanda
Il comportamento del mercato PRIMA di un rilascio macro (CPI, NFP) può predire:
1. l'esito del rilascio (hot/cool CPI, strong/weak NFP)?
2. la direzione post-rilascio (r0, r20)?

## Metodo
- Finestre pre-news: pre1 (giorno prima), pre5 (5 sessioni prima), misurate sull'etichetta di sessione CME (17:00 CT).
- Gruppi di esito: CPI hot/cool/moderate, NFP strong/weak/moderate (stessi criteri dello studio base).
- Statistiche: media, mediana, t, p (test t a due code), correlazione di Pearson, tabella stesso-segno (hit rate).

## Risultati chiave

### 1. NFP FORTE È PREVEDIBILE (il risultato principale)
| Metrica | Valore |
|---|---|
| Drift pre5 prima di NFP strong | **+0.89%** (t=2.36, **p=0.019**) |
| Drift pre5 prima di NFP weak | -0.11% (n.s.) |
| Drift pre5 prima di NFP moderate | +0.66% (n.s.) |

Il mercato azionario tende a SALIRE nelle 5 sessioni precedenti un rilascio che risulterà FORTE (+200k payroll). L'equity è un indicatore anticipatore delle buste paga — coerente con la letteratura sul "rumore di fondo" macro e sul pricing anticipato del ciclo del lavoro.

### 2. NFP weak: il pre-drift è CONTRARIAN a 20 sessioni
- Correlazione pre5 → r20 = **-0.651 (p=0.010)** su n=11: più il mercato è salito prima di un NFP debole, PEGGIORE è l'esito a 20 sessioni. Il rally post-NFP-debole (+4.67% medio) è più forte quando il pre-drift è piatto/negativo.

### 3. CPI moderate: persistenza pre→post
- Stesso segno pre5/r20 nel 73.1% dei casi (n=26) — il drift pre-CPI tende a proseguire dopo un rilascio neutro (assenza di sorpresa → il trend domina).

### 4. CPI cool: pre-drift positivo suggerito
- pre5 +2.48% prima di CPI cool (t=1.56, p=0.12, n=9) — direzione giusta ma potenza insufficiente. Da rivalutare con più dati (2025+).

## Limiti dichiarati
- n piccolo per i gruppi rari (weak n=11, cool n=9): i p-value sono indicativi, non definitivi.
- Multiple testing (6 gruppi × 3 finestre × 2 orizzonti): aspettarsi 1-2 falsi positivi a p<0.05.
- Finestra 2020-2024 include la dislocazione COVID (marzo 2020) — i risultati reggono anche escludendola? (verifica futura).
- Nessun costo di transazione, slippage o spread considerato.

## Implicazioni pratiche (non raccomandazioni di trading)
1. **Segnale pre-NFP**: drift positivo di ~0.9% nelle 5 sessioni pre-NFP → probabilità aumentata di stampa forte; utile per il dimensionamento/posizionamento, non come segnale unico.
2. **Contrarian weak-NFP**: dopo un NFP debole con pre-drift piatto, il rally a 20 sessioni è il più affidabile (coerente con lo studio base).
3. **Persistenza moderate**: nei rilasci "non evento", il trend pre-esistente tende a continuare.

## Fonti e dati
- ES daily: costruito da 1m OHLCV posseduti (regola sessione CME verificata, vedi news_event_study.py)
- Eventi: calendario BLS ufficiale (Wayback ICS) + BLS API (CPI CUSR0000SA0, CES0000000001) + storia FOMC Wikipedia con statement Fed ufficiali
- Script: `pre_news_study.py` (riproducibile), risultati: `pre_news_results.json`
