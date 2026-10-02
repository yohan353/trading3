# Ventaja_Build_ConfigInicial_H1_BUY__DayTrading_M15

*Original:* `Ventaja_Build_ConfigInicial_H1_BUY.cfx` · *Estilo:* Day Trading (ruptura del rango asiático) · *Timeframe:* M15 · *Rol:* Builder de test de ventaja (entrada)

Tabla generada automáticamente a partir de los cambios aplicados al XML (cada fila es un valor que difiere del original). Estado: **no validado en SQX** (ver docs/04).

| Sección | Parámetro | Valor original | Valor nuevo | Justificación |
|---|---|---|---|---|
| Task | `Task@templateFile` | C:\Users\<usuario>\Desktop\Ventaja_Build_ConfigInicial_H1_BUY.cfx | Ventaja_Build_ConfigInicial_H1_BUY__DayTrading_M15.cfx | Ruta local del autor (C:\Users\<usuario>\Desktop\...) sustituida por el nombre del nuevo archivo: no aporta nada y expone el nombre de usuario de Windows. |
| Trading options | `Param key="SignalTimeRangeFrom"` | 5400 | 32400 | Apertura de Londres (servidor UTC+2). |
| Trading options | `Param key="SignalTimeRangeTo"` | 84600 | 68400 | Tras las 19:00 queda poco recorrido intradía. |
| Trading options | `Param key="ExitAtEndOfDay"` | false | true | Definición de day trading: plano al cierre. |
| Trading options | `Param key="EODExitTime"` | 83040 | 81000 | Antes del rollover de las 00:00 servidor. |
| Trading options | `Param key="ExitOnFriday"` | false | true | Sin exposición de fin de semana. |
| Trading options | `Param key="FridayExitTime"` | 74400 | 77400 | Viernes, cierre algo antes. |
| Trading options | `Param key="MaxTradesPerDay"` | 0 | 2 | Una ruptura y, como mucho, un reintento. |
| Trading options | `Param key="MaxDistanceFromMarket"` | false | true | Evita órdenes stop alejadas del precio. |
| Trading options | `Param key="MaxDistancePct"` | 6 | 0.6 | ≈ 90 pips en GBPJPY: cubre rangos asiáticos amplios. |
| Trading options | `Param key="ReservedBars"` | 50 | 120 | ≥ periodo máximo (100). |
| What to build · complejidad | `Chart@maxExitTypes` | 5 | 1 | Test de ventaja: sólo salida temporal, para medir la entrada aislada. |
| What to build · complejidad | `Chart@minPeriod` | 4 | 5 | 5-100 velas de M15 = 1 h 15 min a 25 h: contexto intradía y del día anterior. |
| What to build · complejidad | `Chart@maxPeriod` | 200 | 100 | 5-100 velas de M15 = 1 h 15 min a 25 h: contexto intradía y del día anterior. |
| Genetic options | `PopulationSize` | 15 | 40 | 5-15 individuos por isla es demasiado poco para que el cruce explore; 30-50 es un mínimo práctico. |
| Genetic options | `MaxGenerations` | 10 | 40 | Con 10 generaciones la evolución apenas actúa (y el reinicio por estancamiento a 30 nunca saltaba). |
| Genetic options | `Islands` | 5 | 4 | 4 islas: diversidad suficiente con menos coste. |
| Genetic options | `CrossoverProbability` | 46 | 80 | 46 % es bajo para un AG; 70-90 % es lo habitual (supuesto de práctica general, no de SQX). |
| Genetic options | `MutationProbability` | 35 | 30 | Algo menor para no destruir buenas soluciones. |
| Genetic options | `MigrationModulo` | 5 | 10 | Migrar cada 10 generaciones (con 30-40 generaciones). |
| Genetic options | `MigrationRate` | 6 | 10 | 6 % de 5 individuos = 0,3: la migración original era nula en la práctica. |
| Genetic options | `EvoRestartOnStagnation@generations` | 30 | 15 | Debe ser menor que MaxGenerations para poder actuar. |
| Genetic options | `BuildMode/Conditions (población inicial)` | ReturnDDRatio(IS) >= 2; AvgBarsInTrade(IS) >= 2; NumberOfTrades(IS) >= 250; WinningPct(IS) >= 35 | ReturnDDRatio(IS) >= 1.25; AvgBarsInTrade(IS) >= 2; NumberOfTrades(IS) >= 415; WinningPct(IS) >= 30 | Misma lógica del autor (≈60 % del Ret/DD final, ≈83 % de las operaciones, -5 puntos de acierto) con los umbrales del estilo. |
| Ranking | `Rankings/Conditions (filtros)` | AvgBarsInTrade(IS) >= 2; ReturnDDRatio(IS) >= 4; NumberOfTrades(IS) >= 300; WinningPct(IS) >= 40 | NumberOfTrades(IS) >= 500; ReturnDDRatio(IS) >= 2.5; WinningPct(IS) >= 35; ProfitFactor(IS) >= 1.15; AvgBarsInTrade(IS) >= 2; NetProfit(OOS) > 0 | Umbrales del estilo (frecuencia, acierto típico, Ret/DD) + exigencia en el tramo de validación OOS, que el original no tenía. Test de ventaja: Ret/DD a la mitad, PF mínimo 1,15. |
| Ranking | `FitnessCriteria/Settings/Ranking` | Weighted: Stagnation (peso 1, min) | Weighted: SQN (peso 2, max), StagnationPct (peso 1, min) | SQN mide la calidad estadística de la entrada (expectativa/desviación·√N); el original optimizaba sólo 'Stagnation', que ignora el beneficio. |
| Data | `Setup/Chart@timeframe` | H1 | M15 | Timeframe del estilo DayTrading. |
| Data | `Setup@slippage` | 0 | 0.3 | El original usa 0; 0,3 pips por ejecución stop en apertura de Londres. |
| Data | `OutOfSample/Range` | (sin OOS) | 2019.01.01–2020.12.31 | Nuevo tramo de validación dentro del Builder (el original no tenía OOS y filtraba sólo sobre IS). |
| Cross checks | `RetestOnAdditionalMarkets/Setup@timeframe` | H1 | M15 | Coherencia si se activa (sigue desactivado). |
| Building blocks | `Bloques activos · signals` | 146 activos | 11 activos: ADXHigher(w1), ADXRising(w1), ATRRising(w1), BBBarOpensAboveUpAfterOpenBelow(w1), BarHourIsBigger(w1), BarHourIsSmaller(w1), BarOpensAboveHighestAfterOpenBelow(w2), KCBarOpensAboveUpperAfterOpenBelow(w1), LinRegRising(w1), MABarClosesAbove(w1), MARising(w1) | El nivel roto es el máximo del rango asiático (HighestInRange 00:00-03:00 → 07:00-10:00, en horas enteras: el rango original 0-2359 con paso 30 generaba horas HHMM inválidas como 0060) y los niveles del día anterior. |
| Building blocks | `Bloques activos · indicators` | 29 activos | 21 activos: CrossesAbove(w1), CrossesBelow(w1), Indicators.ATR(w1), Indicators.EMA(w1), Indicators.Highest(w1), Indicators.HighestInRange(w3), Indicators.Lowest(w1), Indicators.LowestInRange(w2), IsGreater(w1), IsLower(w1), Prices.Close(w1), Prices.CloseD(w1), Prices.High(w1), Prices.HighD(w1), Prices.Low(w1), Prices.LowD(w1), Prices.Open(w1), Prices.OpenD(w1), Prices.SessionHigh(w2), Prices.SessionLow(w1), Prices.SessionOpen(w1) | El nivel roto es el máximo del rango asiático (HighestInRange 00:00-03:00 → 07:00-10:00, en horas enteras: el rango original 0-2359 con paso 30 generaba horas HHMM inválidas como 0060) y los niveles del día anterior. |
| Building blocks | `Bloques activos · stopLimitBlocks` | 29 activos | 7 activos: Stop/Limit Price Levels.HighD(w1), Stop/Limit Price Levels.Highest(w1), Stop/Limit Price Levels.HighestInRange(w3), Stop/Limit Price Levels.OpenD(w1), Stop/Limit Price Levels.SessionHigh(w2), Stop/Limit Price Ranges.ATR(w2), Stop/Limit Price Ranges.BarRange(w1) | El nivel roto es el máximo del rango asiático (HighestInRange 00:00-03:00 → 07:00-10:00, en horas enteras: el rango original 0-2359 con paso 30 generaba horas HHMM inválidas como 0060) y los niveles del día anterior. |
| Building blocks | `Indicators.HighestInRange · Time From` | 0..2359/30 | 0..300/100 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Indicators.HighestInRange · Time To` | 0..2359/30 | 700..1000/100 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Indicators.LowestInRange · Time From` | 0..2359/30 | 0..300/100 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Indicators.LowestInRange · Time To` | 0..2359/30 | 700..1000/100 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Stop/Limit Price Levels.HighestInRange · Time From` | 0..2359/30 | 0..300/100 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Stop/Limit Price Levels.HighestInRange · Time To` | 0..2359/30 | 700..1000/100 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Prices.SessionHigh · Start Hours` | 0..23/1 | 1..3/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Prices.SessionHigh · Start Minutes` | 0..59/1 | 0..0/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Prices.SessionHigh · End Hours` | 0..23/1 | 8..10/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Prices.SessionHigh · End Minutes` | 0..59/1 | 0..0/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Prices.SessionLow · Start Hours` | 0..23/1 | 1..3/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Prices.SessionLow · Start Minutes` | 0..59/1 | 0..0/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Prices.SessionLow · End Hours` | 0..23/1 | 8..10/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Prices.SessionLow · End Minutes` | 0..59/1 | 0..0/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Stop/Limit Price Levels.SessionHigh · Start Hours` | 0..23/1 | 1..3/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Stop/Limit Price Levels.SessionHigh · Start Minutes` | 0..59/1 | 0..0/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Stop/Limit Price Levels.SessionHigh · End Hours` | 0..23/1 | 8..10/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Stop/Limit Price Levels.SessionHigh · End Minutes` | 0..59/1 | 0..0/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Prices.SessionOpen · Start Hours` | 0..23/1 | 9..10/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Prices.SessionOpen · Start Minutes` | 0..59/1 | 0..0/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `ADXHigher · Level` | 20..90/10 | 20..40/5 | Rango acotado al estilo (ver ficha). |
| Building blocks | `BarHourIsBigger · Hour` | 0..23/1 | 8..12/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `BarHourIsSmaller · Hour` | 0..23/1 | 12..19/1 | Rango acotado al estilo (ver ficha). |
| Order types | `EnterAtStop@use` | false | true | Stop en el extremo del rango; válida 30 min-2 h. |
| Order types | `EnterAtStop@weight` | 1 | 3 | Peso relativo entre tipos de orden. |
| Order types | `EnterAtStop · BarsValid max` | 10 | 8 | Stop en el extremo del rango; válida 30 min-2 h. |
| Order types | `EnterAtStop · ExitAfterBars min` | 5 | 4 | Alineado con el rango de ExitTypes para eliminar la ambigüedad del original (5-20 vs 2-15). |
| Order types | `EnterAtStop · ExitAfterBars max` | 20 | 24 | Alineado con el rango de ExitTypes. |
| Order types | `EnterAtMarket · ExitAfterBars min` | 5 | 4 | Alineado con el rango de ExitTypes para eliminar la ambigüedad del original (5-20 vs 2-15). |
| Order types | `EnterAtMarket · ExitAfterBars max` | 20 | 24 | Alineado con el rango de ExitTypes. |
| Exit types | `ExitAfterBars@probability` | 50 | 100 | Explícito: es la única salida (el original ponía 50 y dependía de minExitTypes=1). |
| Exit types | `ExitAfterBars min` | 2 | 4 | Test de ventaja: salida por tiempo 1-6 h + cierre de fin de día. |
| Exit types | `ExitAfterBars max` | 15 | 24 | Test de ventaja: salida por tiempo 1-6 h + cierre de fin de día. |
| Notes | `Notes` | <b>Breakout strategies setup</b><div><br></div><div><br></div><div><br></div><div><br></div> | <b>Day Trading (ruptura del rango asiático) – Builder de test de ventaja (entrada)</b><div>Derivado de Ventaja_Build_ConfigInicial_H1_BUY (build 140.2099). Timeframe M15. Ver docs/03 (ficha DayTrading) y docs/04 (checklist).</div><div>NO VALIDADO EN SQX: revisar símbolo, costes, horario del servidor e importación.</div> | Descripción del estilo y advertencias. |
