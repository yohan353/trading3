# Ventaja_Build_ConfigInicial_H1_BUY__Position_D1

*Original:* `Ventaja_Build_ConfigInicial_H1_BUY.cfx` · *Estilo:* Position Trading (momentum de largo plazo) · *Timeframe:* D1 · *Rol:* Builder de test de ventaja (entrada)

Tabla generada automáticamente a partir de los cambios aplicados al XML (cada fila es un valor que difiere del original). Estado: **no validado en SQX** (ver docs/04).

| Sección | Parámetro | Valor original | Valor nuevo | Justificación |
|---|---|---|---|---|
| Task | `Task@templateFile` | C:\Users\<usuario>\Desktop\Ventaja_Build_ConfigInicial_H1_BUY.cfx | Ventaja_Build_ConfigInicial_H1_BUY__Position_D1.cfx | Ruta local del autor (C:\Users\<usuario>\Desktop\...) sustituida por el nombre del nuevo archivo: no aporta nada y expone el nombre de usuario de Windows. |
| Trading options | `Param key="LimitTimeRange"` | true | false | Con velas D1 (apertura 00:00) la ventana 01:30-23:30 del original podría bloquear todas las señales. |
| Trading options | `Param key="MaxTradesPerDay"` | 0 | 1 | Position: una entrada como máximo. |
| Trading options | `Param key="MaxDistanceFromMarket"` | false | true | Tope de distancia para stops. |
| Trading options | `Param key="MaxDistancePct"` | 6 | 5 | 5 %: rupturas de máximos de 20-250 días. |
| Trading options | `Param key="ReservedBars"` | 50 | 260 | ≥ periodo máximo (250). |
| What to build · complejidad | `Chart@maxConditions` | 3 | 2 | 20-250 días (1 mes-1 año). Máximo 2 condiciones: con ~8 operaciones/año cada grado de libertad extra es sobreajuste casi seguro. |
| What to build · complejidad | `Chart@maxExitTypes` | 5 | 1 | Test de ventaja: sólo salida temporal, para medir la entrada aislada. |
| What to build · complejidad | `Chart@minPeriod` | 4 | 20 | 20-250 días (1 mes-1 año). Máximo 2 condiciones: con ~8 operaciones/año cada grado de libertad extra es sobreajuste casi seguro. |
| What to build · complejidad | `Chart@maxPeriod` | 200 | 250 | 20-250 días (1 mes-1 año). Máximo 2 condiciones: con ~8 operaciones/año cada grado de libertad extra es sobreajuste casi seguro. |
| Genetic options | `PopulationSize` | 15 | 50 | 5-15 individuos por isla es demasiado poco para que el cruce explore; 30-50 es un mínimo práctico. |
| Genetic options | `MaxGenerations` | 10 | 30 | Con 10 generaciones la evolución apenas actúa (y el reinicio por estancamiento a 30 nunca saltaba). |
| Genetic options | `Islands` | 5 | 4 | 4 islas: diversidad suficiente con menos coste. |
| Genetic options | `CrossoverProbability` | 46 | 80 | 46 % es bajo para un AG; 70-90 % es lo habitual (supuesto de práctica general, no de SQX). |
| Genetic options | `MutationProbability` | 35 | 30 | Algo menor para no destruir buenas soluciones. |
| Genetic options | `MigrationModulo` | 5 | 10 | Migrar cada 10 generaciones (con 30-40 generaciones). |
| Genetic options | `MigrationRate` | 6 | 10 | 6 % de 5 individuos = 0,3: la migración original era nula en la práctica. |
| Genetic options | `EvoRestartOnStagnation@generations` | 30 | 15 | Debe ser menor que MaxGenerations para poder actuar. |
| Genetic options | `BuildMode/Conditions (población inicial)` | ReturnDDRatio(IS) >= 2; AvgBarsInTrade(IS) >= 2; NumberOfTrades(IS) >= 250; WinningPct(IS) >= 35 | ReturnDDRatio(IS) >= 0.75; AvgBarsInTrade(IS) >= 5; NumberOfTrades(IS) >= 33; WinningPct(IS) >= 25 | Misma lógica del autor (≈60 % del Ret/DD final, ≈83 % de las operaciones, -5 puntos de acierto) con los umbrales del estilo. |
| Ranking | `Rankings/Conditions (filtros)` | AvgBarsInTrade(IS) >= 2; ReturnDDRatio(IS) >= 4; NumberOfTrades(IS) >= 300; WinningPct(IS) >= 40 | NumberOfTrades(IS) >= 40; ReturnDDRatio(IS) >= 1.5; WinningPct(IS) >= 30; ProfitFactor(IS) >= 1.3; AvgBarsInTrade(IS) >= 5 | Umbrales del estilo (frecuencia, acierto típico, Ret/DD) + exigencia en el tramo de validación OOS, que el original no tenía. Test de ventaja: Ret/DD a la mitad, PF mínimo 1,15. |
| Ranking | `FitnessCriteria/Settings/Ranking` | Weighted: Stagnation (peso 1, min) | Weighted: ProfitFactor (peso 2, max), StagnationPct (peso 1, min) | SQN mide la calidad estadística de la entrada (expectativa/desviación·√N); el original optimizaba sólo 'Stagnation', que ignora el beneficio. |
| Data | `Setup/Chart@timeframe` | H1 | D1 | Timeframe del estilo Position. |
| Data | `Setup@slippage` | 0 | 0.5 | D1 entra a la apertura del día (a menudo tras gap): 0,5 pips conservador. |
| Cross checks | `RetestOnAdditionalMarkets/Setup@timeframe` | H1 | D1 | Coherencia si se activa (sigue desactivado). |
| Building blocks | `Bloques activos · signals` | 146 activos | 12 activos: ADXHigher(w1), BarOpensAboveHighestAfterOpenBelow(w3), IchimokuKumoBreakoutBullish(w1), KAMARising(w1), LinRegRising(w1), MABarClosesAbove(w2), MACDMainCrossAboveZero(w1), MACDMainHigherZero(w1), MARising(w2), ROCAboveLevel(w2), ROCRising(w1), SuperTrendUPTrend(w1) | Momentum sin niveles absolutos (ROC en %, MACD vs 0, medias, máximos de 20-250 días). Se eliminan osciladores: no aportan nada a un horizonte de meses. |
| Building blocks | `Bloques activos · indicators` | 29 activos | 17 activos: CrossesAbove(w1), CrossesBelow(w1), Indicators.ATR(w1), Indicators.EMA(w1), Indicators.Highest(w2), Indicators.Lowest(w1), Indicators.SMA(w2), IsGreater(w1), IsLower(w1), Prices.Close(w1), Prices.CloseW(w1), Prices.High(w1), Prices.HighM(w1), Prices.HighW(w1), Prices.Low(w1), Prices.LowM(w1), Prices.LowW(w1) | Momentum sin niveles absolutos (ROC en %, MACD vs 0, medias, máximos de 20-250 días). Se eliminan osciladores: no aportan nada a un horizonte de meses. |
| Building blocks | `Bloques activos · stopLimitBlocks` | 29 activos | 5 activos: Stop/Limit Price Levels.High(w1), Stop/Limit Price Levels.HighM(w1), Stop/Limit Price Levels.HighW(w1), Stop/Limit Price Levels.Highest(w2), Stop/Limit Price Ranges.ATR(w1) | Momentum sin niveles absolutos (ROC en %, MACD vs 0, medias, máximos de 20-250 días). Se eliminan osciladores: no aportan nada a un horizonte de meses. |
| Building blocks | `ROCAboveLevel · Level` | -100..100/0.001 | 0..15/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `ADXHigher · Level` | 20..90/10 | 20..40/5 | Rango acotado al estilo (ver ficha). |
| Order types | `EnterAtMarket@weight` | 1 | 2 | Peso relativo entre tipos de orden. |
| Order types | `EnterAtMarket · ExitAfterBars min` | 5 | 20 | Alineado con el rango de ExitTypes para eliminar la ambigüedad del original (5-20 vs 2-15). |
| Order types | `EnterAtMarket · ExitAfterBars max` | 20 | 120 | Alineado con el rango de ExitTypes. |
| Order types | `EnterAtStop@use` | false | true | Mayoritariamente a mercado; stop opcional válido 1-5 días. |
| Order types | `EnterAtStop · BarsValid min` | 2 | 1 | Mayoritariamente a mercado; stop opcional válido 1-5 días. |
| Order types | `EnterAtStop · BarsValid max` | 10 | 5 | Mayoritariamente a mercado; stop opcional válido 1-5 días. |
| Order types | `EnterAtStop · ExitAfterBars min` | 5 | 20 | Alineado con el rango de ExitTypes para eliminar la ambigüedad del original (5-20 vs 2-15). |
| Order types | `EnterAtStop · ExitAfterBars max` | 20 | 120 | Alineado con el rango de ExitTypes. |
| Exit types | `ExitAfterBars@probability` | 50 | 100 | Explícito: es la única salida (el original ponía 50 y dependía de minExitTypes=1). |
| Exit types | `ExitAfterBars min` | 2 | 20 | Test de ventaja: salida por tiempo 1-6 meses. |
| Exit types | `ExitAfterBars max` | 15 | 120 | Test de ventaja: salida por tiempo 1-6 meses. |
| Notes | `Notes` | <b>Breakout strategies setup</b><div><br></div><div><br></div><div><br></div><div><br></div> | <b>Position Trading (momentum de largo plazo) – Builder de test de ventaja (entrada)</b><div>Derivado de Ventaja_Build_ConfigInicial_H1_BUY (build 140.2099). Timeframe D1. Ver docs/03 (ficha Position) y docs/04 (checklist).</div><div>NO VALIDADO EN SQX: revisar símbolo, costes, horario del servidor e importación.</div> | Descripción del estilo y advertencias. |
