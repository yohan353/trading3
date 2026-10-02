# Ventaja_Build_ConfigInicial_H1_BUY__Swing_H4

*Original:* `Ventaja_Build_ConfigInicial_H1_BUY.cfx` · *Estilo:* Swing Trading (ruptura de consolidación multi-día) · *Timeframe:* H4 · *Rol:* Builder de test de ventaja (entrada)

Tabla generada automáticamente a partir de los cambios aplicados al XML (cada fila es un valor que difiere del original). Estado: **no validado en SQX** (ver docs/04).

| Sección | Parámetro | Valor original | Valor nuevo | Justificación |
|---|---|---|---|---|
| Task | `Task@templateFile` | C:\Users\<usuario>\Desktop\Ventaja_Build_ConfigInicial_H1_BUY.cfx | Ventaja_Build_ConfigInicial_H1_BUY__Swing_H4.cfx | Ruta local del autor (C:\Users\<usuario>\Desktop\...) sustituida por el nombre del nuevo archivo: no aporta nada y expone el nombre de usuario de Windows. |
| Trading options | `Param key="LimitTimeRange"` | true | false | En H4 la ventana 01:30-23:30 excluiría la vela de las 00:00 (1/6 de las señales) sin motivo de estilo. |
| Trading options | `Param key="MaxTradesPerDay"` | 0 | 1 | Swing: como mucho una entrada diaria. |
| Trading options | `Param key="MaxDistanceFromMarket"` | false | true | Evita stops lejanos. |
| Trading options | `Param key="MaxDistancePct"` | 6 | 2 | 2 %: holgura para rupturas de rangos de varios días. |
| Trading options | `Param key="ReservedBars"` | 50 | 150 | ≥ periodo máximo (120). |
| What to build · complejidad | `Chart@maxExitTypes` | 5 | 1 | Test de ventaja: sólo salida temporal, para medir la entrada aislada. |
| What to build · complejidad | `Chart@minPeriod` | 4 | 5 | 5-120 velas H4 = 1-20 días: horizonte de swing. |
| What to build · complejidad | `Chart@maxPeriod` | 200 | 120 | 5-120 velas H4 = 1-20 días: horizonte de swing. |
| Genetic options | `PopulationSize` | 15 | 50 | 5-15 individuos por isla es demasiado poco para que el cruce explore; 30-50 es un mínimo práctico. |
| Genetic options | `MaxGenerations` | 10 | 40 | Con 10 generaciones la evolución apenas actúa (y el reinicio por estancamiento a 30 nunca saltaba). |
| Genetic options | `Islands` | 5 | 4 | 4 islas: diversidad suficiente con menos coste. |
| Genetic options | `CrossoverProbability` | 46 | 80 | 46 % es bajo para un AG; 70-90 % es lo habitual (supuesto de práctica general, no de SQX). |
| Genetic options | `MutationProbability` | 35 | 30 | Algo menor para no destruir buenas soluciones. |
| Genetic options | `MigrationModulo` | 5 | 10 | Migrar cada 10 generaciones (con 30-40 generaciones). |
| Genetic options | `MigrationRate` | 6 | 10 | 6 % de 5 individuos = 0,3: la migración original era nula en la práctica. |
| Genetic options | `EvoRestartOnStagnation@generations` | 30 | 15 | Debe ser menor que MaxGenerations para poder actuar. |
| Genetic options | `BuildMode/Conditions (población inicial)` | ReturnDDRatio(IS) >= 2; AvgBarsInTrade(IS) >= 2; NumberOfTrades(IS) >= 250; WinningPct(IS) >= 35 | ReturnDDRatio(IS) >= 1; AvgBarsInTrade(IS) >= 3; NumberOfTrades(IS) >= 124; WinningPct(IS) >= 28 | Misma lógica del autor (≈60 % del Ret/DD final, ≈83 % de las operaciones, -5 puntos de acierto) con los umbrales del estilo. |
| Ranking | `Rankings/Conditions (filtros)` | AvgBarsInTrade(IS) >= 2; ReturnDDRatio(IS) >= 4; NumberOfTrades(IS) >= 300; WinningPct(IS) >= 40 | NumberOfTrades(IS) >= 150; ReturnDDRatio(IS) >= 2; WinningPct(IS) >= 33; ProfitFactor(IS) >= 1.15; AvgBarsInTrade(IS) >= 3; NetProfit(OOS) > 0 | Umbrales del estilo (frecuencia, acierto típico, Ret/DD) + exigencia en el tramo de validación OOS, que el original no tenía. Test de ventaja: Ret/DD a la mitad, PF mínimo 1,15. |
| Ranking | `FitnessCriteria/Settings/Ranking` | Weighted: Stagnation (peso 1, min) | Weighted: SQN (peso 2, max), StagnationPct (peso 1, min) | SQN mide la calidad estadística de la entrada (expectativa/desviación·√N); el original optimizaba sólo 'Stagnation', que ignora el beneficio. |
| Data | `Setup/Chart@timeframe` | H1 | H4 | Timeframe del estilo Swing. |
| Data | `Setup@slippage` | 0 | 0.3 | El original usa 0; 0,3 pips es conservador en H4. |
| Data | `OutOfSample/Range` | (sin OOS) | 2019.01.01–2020.12.31 | Nuevo tramo de validación dentro del Builder (el original no tenía OOS y filtraba sólo sobre IS). |
| Cross checks | `RetestOnAdditionalMarkets/Setup@timeframe` | H1 | H4 | Coherencia si se activa (sigue desactivado). |
| Building blocks | `Bloques activos · signals` | 146 activos | 14 activos: ADXHigher(w1), ADXRising(w1), ATRRising(w1), BBBarOpensAboveUpAfterOpenBelow(w1), BBUpperRising(w1), BarOpensAboveHighestAfterOpenBelow(w3), IchimokuKumoBreakoutBullish(w1), KCBarOpensAboveUpperAfterOpenBelow(w1), KERaboveLevel(w1), LinRegRising(w1), MABarClosesAbove(w1), MARising(w1), RSIHigher(w1), SuperTrendUPTrend(w1) | Ruptura de máximos de N días (Donchian/Bollinger/Keltner/Kumo) filtrada por régimen (ADX, pendiente de medias, eficiencia de Kaufman). |
| Building blocks | `Bloques activos · indicators` | 29 activos | 20 activos: CrossesAbove(w1), CrossesBelow(w1), Indicators.ATR(w1), Indicators.BollingerBands(w1), Indicators.EMA(w1), Indicators.Highest(w2), Indicators.KeltnerChannel(w1), Indicators.Lowest(w1), Indicators.SMA(w1), IsGreater(w1), IsGreaterCount(w1), IsLower(w1), Prices.Close(w1), Prices.High(w1), Prices.HighD(w1), Prices.HighW(w1), Prices.Low(w1), Prices.LowD(w1), Prices.LowW(w1), Prices.Open(w1) | Ruptura de máximos de N días (Donchian/Bollinger/Keltner/Kumo) filtrada por régimen (ADX, pendiente de medias, eficiencia de Kaufman). |
| Building blocks | `Bloques activos · stopLimitBlocks` | 29 activos | 9 activos: Stop/Limit Price Levels.BollingerBands(w1), Stop/Limit Price Levels.High(w1), Stop/Limit Price Levels.HighD(w1), Stop/Limit Price Levels.HighW(w1), Stop/Limit Price Levels.Highest(w3), Stop/Limit Price Levels.KeltnerChannel(w1), Stop/Limit Price Ranges.ATR(w2), Stop/Limit Price Ranges.BBRange(w1), Stop/Limit Price Ranges.BarRange(w1) | Ruptura de máximos de N días (Donchian/Bollinger/Keltner/Kumo) filtrada por régimen (ADX, pendiente de medias, eficiencia de Kaufman). |
| Building blocks | `ADXHigher · Level` | 20..90/10 | 20..40/5 | Rango acotado al estilo (ver ficha). |
| Building blocks | `RSIHigher · Level` | 0..100/5 | 50..70/5 | Rango acotado al estilo (ver ficha). |
| Building blocks | `KERaboveLevel · Level` | 0..0.95/0.05 | 0.2..0.6/0.05 | Rango acotado al estilo (ver ficha). |
| Order types | `EnterAtStop@use` | false | true | Stop válida 8-24 h. |
| Order types | `EnterAtStop@weight` | 1 | 2 | Peso relativo entre tipos de orden. |
| Order types | `EnterAtStop · BarsValid max` | 10 | 6 | Stop válida 8-24 h. |
| Order types | `EnterAtStop · ExitAfterBars min` | 5 | 6 | Alineado con el rango de ExitTypes para eliminar la ambigüedad del original (5-20 vs 2-15). |
| Order types | `EnterAtStop · ExitAfterBars max` | 20 | 30 | Alineado con el rango de ExitTypes. |
| Order types | `EnterAtMarket · ExitAfterBars min` | 5 | 6 | Alineado con el rango de ExitTypes para eliminar la ambigüedad del original (5-20 vs 2-15). |
| Order types | `EnterAtMarket · ExitAfterBars max` | 20 | 30 | Alineado con el rango de ExitTypes. |
| Exit types | `ExitAfterBars@probability` | 50 | 100 | Explícito: es la única salida (el original ponía 50 y dependía de minExitTypes=1). |
| Exit types | `ExitAfterBars min` | 2 | 6 | Test de ventaja: salida por tiempo 1-5 días. |
| Exit types | `ExitAfterBars max` | 15 | 30 | Test de ventaja: salida por tiempo 1-5 días. |
| Notes | `Notes` | <b>Breakout strategies setup</b><div><br></div><div><br></div><div><br></div><div><br></div> | <b>Swing Trading (ruptura de consolidación multi-día) – Builder de test de ventaja (entrada)</b><div>Derivado de Ventaja_Build_ConfigInicial_H1_BUY (build 140.2099). Timeframe H4. Ver docs/03 (ficha Swing) y docs/04 (checklist).</div><div>NO VALIDADO EN SQX: revisar símbolo, costes, horario del servidor e importación.</div> | Descripción del estilo y advertencias. |
