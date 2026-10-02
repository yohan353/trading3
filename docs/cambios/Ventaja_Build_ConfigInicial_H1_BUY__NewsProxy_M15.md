# Ventaja_Build_ConfigInicial_H1_BUY__NewsProxy_M15

*Original:* `Ventaja_Build_ConfigInicial_H1_BUY.cfx` · *Estilo:* Noticias (APROXIMACIÓN horaria: ventana de datos de EE. UU.) · *Timeframe:* M15 · *Rol:* Builder de test de ventaja (entrada)

Tabla generada automáticamente a partir de los cambios aplicados al XML (cada fila es un valor que difiere del original). Estado: **no validado en SQX** (ver docs/04).

| Sección | Parámetro | Valor original | Valor nuevo | Justificación |
|---|---|---|---|---|
| Task | `Task@templateFile` | C:\Users\<usuario>\Desktop\Ventaja_Build_ConfigInicial_H1_BUY.cfx | Ventaja_Build_ConfigInicial_H1_BUY__NewsProxy_M15.cfx | Ruta local del autor (C:\Users\<usuario>\Desktop\...) sustituida por el nombre del nuevo archivo: no aporta nada y expone el nombre de usuario de Windows. |
| Trading options | `Param key="SignalTimeRangeFrom"` | 5400 | 54000 | Media hora antes de las 15:30 (8:30 ET). |
| Trading options | `Param key="SignalTimeRangeTo"` | 84600 | 61200 | Incluye datos de las 10:00 ET (17:00 servidor). |
| Trading options | `Param key="ExitAtEndOfDay"` | false | true | Sin exposición nocturna. |
| Trading options | `Param key="EODExitTime"` | 83040 | 79200 | Antes del rollover. |
| Trading options | `Param key="ExitOnFriday"` | false | true | El NFP cae en viernes: no arrastrar al fin de semana. |
| Trading options | `Param key="FridayExitTime"` | 74400 | 75600 | Viernes. |
| Trading options | `Param key="MaxTradesPerDay"` | 0 | 1 | Una reacción por día. |
| Trading options | `Param key="MaxDistanceFromMarket"` | false | true | Tope para stops. |
| Trading options | `Param key="MaxDistancePct"` | 6 | 0.5 | 0,5 %. |
| Trading options | `Param key="ReservedBars"` | 50 | 60 | ≥ periodo máximo (48). |
| What to build · complejidad | `Chart@maxExitTypes` | 5 | 1 | Test de ventaja: sólo salida temporal, para medir la entrada aislada. |
| What to build · complejidad | `Chart@maxPeriod` | 200 | 48 | 4-48 velas M15 (1-12 h): contexto del día de la publicación. |
| Genetic options | `PopulationSize` | 15 | 30 | 5-15 individuos por isla es demasiado poco para que el cruce explore; 30-50 es un mínimo práctico. |
| Genetic options | `MaxGenerations` | 10 | 30 | Con 10 generaciones la evolución apenas actúa (y el reinicio por estancamiento a 30 nunca saltaba). |
| Genetic options | `Islands` | 5 | 4 | 4 islas: diversidad suficiente con menos coste. |
| Genetic options | `CrossoverProbability` | 46 | 80 | 46 % es bajo para un AG; 70-90 % es lo habitual (supuesto de práctica general, no de SQX). |
| Genetic options | `MutationProbability` | 35 | 30 | Algo menor para no destruir buenas soluciones. |
| Genetic options | `MigrationModulo` | 5 | 10 | Migrar cada 10 generaciones (con 30-40 generaciones). |
| Genetic options | `MigrationRate` | 6 | 10 | 6 % de 5 individuos = 0,3: la migración original era nula en la práctica. |
| Genetic options | `EvoRestartOnStagnation@generations` | 30 | 15 | Debe ser menor que MaxGenerations para poder actuar. |
| Genetic options | `BuildMode/Conditions (población inicial)` | ReturnDDRatio(IS) >= 2; AvgBarsInTrade(IS) >= 2; NumberOfTrades(IS) >= 250; WinningPct(IS) >= 35 | ReturnDDRatio(IS) >= 0.75; AvgBarsInTrade(IS) >= 2; NumberOfTrades(IS) >= 207; WinningPct(IS) >= 25 | Misma lógica del autor (≈60 % del Ret/DD final, ≈83 % de las operaciones, -5 puntos de acierto) con los umbrales del estilo. |
| Ranking | `Rankings/Conditions (filtros)` | AvgBarsInTrade(IS) >= 2; ReturnDDRatio(IS) >= 4; NumberOfTrades(IS) >= 300; WinningPct(IS) >= 40 | NumberOfTrades(IS) >= 250; ReturnDDRatio(IS) >= 1.5; WinningPct(IS) >= 30; ProfitFactor(IS) >= 1.15; AvgBarsInTrade(IS) >= 2; NetProfit(OOS) > 0 | Umbrales del estilo (frecuencia, acierto típico, Ret/DD) + exigencia en el tramo de validación OOS, que el original no tenía. Test de ventaja: Ret/DD a la mitad, PF mínimo 1,15. |
| Ranking | `FitnessCriteria/Settings/Ranking` | Weighted: Stagnation (peso 1, min) | Weighted: SQN (peso 2, max), StagnationPct (peso 1, min) | SQN mide la calidad estadística de la entrada (expectativa/desviación·√N); el original optimizaba sólo 'Stagnation', que ignora el beneficio. |
| Data | `Setup/Chart@timeframe` | H1 | M15 | Timeframe del estilo NewsProxy. |
| Data | `Setup@slippage` | 0 | 1.5 | En publicaciones el deslizamiento real es de varios pips; 1,5 pips es el mínimo prudente. |
| Data | `Setup@dateFrom` | 2013.09.30 | 2016.01.04 | M5/M15: 5 años bastan en operaciones y reducen el cómputo. |
| Data | `OutOfSample/Range` | (sin OOS) | 2019.07.01–2020.12.31 | Nuevo tramo de validación dentro del Builder (el original no tenía OOS y filtraba sólo sobre IS). |
| Cross checks | `RetestOnAdditionalMarkets/Setup@timeframe` | H1 | M15 | Coherencia si se activa (sigue desactivado). |
| Building blocks | `Bloques activos · signals` | 146 activos | 8 activos: ATRChangesUp(w1), ATRRising(w2), BBBarOpensAboveUpAfterOpenBelow(w1), BarDayOfWeekIs(w1), BarHourIs(w2), BarOpensAboveHighestAfterOpenBelow(w2), KCBarOpensAboveUpperAfterOpenBelow(w1), StdDevRising(w1) | Rango previo a la publicación (12:00-15:00 → 15:00/15:30) y filtros de hora/día; expansión de volatilidad como confirmación. |
| Building blocks | `Bloques activos · indicators` | 29 activos | 14 activos: CrossesAbove(w1), CrossesBelow(w1), Indicators.ATR(w1), Indicators.Highest(w1), Indicators.HighestInRange(w3), Indicators.Lowest(w1), Indicators.LowestInRange(w1), Indicators.TrueRange(w1), IsGreater(w1), IsLower(w1), Prices.Close(w1), Prices.High(w1), Prices.Low(w1), Prices.Open(w1) | Rango previo a la publicación (12:00-15:00 → 15:00/15:30) y filtros de hora/día; expansión de volatilidad como confirmación. |
| Building blocks | `Bloques activos · stopLimitBlocks` | 29 activos | 6 activos: Stop/Limit Price Levels.High(w1), Stop/Limit Price Levels.Highest(w1), Stop/Limit Price Levels.HighestInRange(w3), Stop/Limit Price Ranges.ATR(w2), Stop/Limit Price Ranges.BarRange(w1), Stop/Limit Price Ranges.TrueRange(w1) | Rango previo a la publicación (12:00-15:00 → 15:00/15:30) y filtros de hora/día; expansión de volatilidad como confirmación. |
| Building blocks | `Indicators.HighestInRange · Time From` | 0..2359/30 | 1200..1500/100 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Indicators.HighestInRange · Time To` | 0..2359/30 | 1500..1530/30 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Indicators.LowestInRange · Time From` | 0..2359/30 | 1200..1500/100 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Indicators.LowestInRange · Time To` | 0..2359/30 | 1500..1530/30 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Stop/Limit Price Levels.HighestInRange · Time From` | 0..2359/30 | 1200..1500/100 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Stop/Limit Price Levels.HighestInRange · Time To` | 0..2359/30 | 1500..1530/30 | Rango acotado al estilo (ver ficha). |
| Building blocks | `BarHourIs · Hour` | 0..23/1 | 15..16/1 | Rango acotado al estilo (ver ficha). |
| Order types | `EnterAtStop@use` | false | true | Stop sobre el rango pre-dato, caduca en 15-60 min. |
| Order types | `EnterAtStop@weight` | 1 | 3 | Peso relativo entre tipos de orden. |
| Order types | `EnterAtStop · BarsValid min` | 2 | 1 | Stop sobre el rango pre-dato, caduca en 15-60 min. |
| Order types | `EnterAtStop · BarsValid max` | 10 | 4 | Stop sobre el rango pre-dato, caduca en 15-60 min. |
| Order types | `EnterAtStop · ExitAfterBars min` | 5 | 2 | Alineado con el rango de ExitTypes para eliminar la ambigüedad del original (5-20 vs 2-15). |
| Order types | `EnterAtStop · ExitAfterBars max` | 20 | 12 | Alineado con el rango de ExitTypes. |
| Order types | `EnterAtMarket · ExitAfterBars min` | 5 | 2 | Alineado con el rango de ExitTypes para eliminar la ambigüedad del original (5-20 vs 2-15). |
| Order types | `EnterAtMarket · ExitAfterBars max` | 20 | 12 | Alineado con el rango de ExitTypes. |
| Exit types | `ExitAfterBars@probability` | 50 | 100 | Explícito: es la única salida (el original ponía 50 y dependía de minExitTypes=1). |
| Exit types | `ExitAfterBars max` | 15 | 12 | Test de ventaja: salida por tiempo 30 min-3 h. |
| Notes | `Notes` | <b>Breakout strategies setup</b><div><br></div><div><br></div><div><br></div><div><br></div> | <b>Noticias (APROXIMACIÓN horaria: ventana de datos de EE. UU.) – Builder de test de ventaja (entrada)</b><div>Derivado de Ventaja_Build_ConfigInicial_H1_BUY (build 140.2099). Timeframe M15. Ver docs/03 (ficha NewsProxy) y docs/04 (checklist).</div><div>NO VALIDADO EN SQX: revisar símbolo, costes, horario del servidor e importación.</div> | Descripción del estilo y advertencias. |
