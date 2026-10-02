# Ventaja_Build_ConfigInicial_H1_BUY__NewsProxy_M15_BUY

*Original:* `Ventaja_Build_ConfigInicial_H1_BUY.cfx` · *Estilo:* Noticias (APROXIMACIÓN horaria: ventana de datos de EE. UU.) · *Timeframe:* M15 · *Rol:* Builder de test de ventaja (entrada) · *Dirección:* BUY

Tabla generada automáticamente a partir de los cambios aplicados al XML (cada fila es un valor que difiere del original). Estado: **no validado en SQX** (ver docs/04).

| Sección | Parámetro | Valor original | Valor nuevo | Justificación |
|---|---|---|---|---|
| Task | `Task@templateFile` | C:\Users\<usuario>\Desktop\Ventaja_Build_ConfigInicial_H1_BUY.cfx | Ventaja_Build_ConfigInicial_H1_BUY__NewsProxy_M15_BUY.cfx | Ruta local del autor (C:\Users\<usuario>\Desktop\...) sustituida por el nombre del nuevo archivo: no aporta nada y expone el nombre de usuario de Windows. |
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
| Genetic options | `PopulationSize` | 15 | 20 | 20 por isla × 4 islas = 80 por generación: más diversidad que el original (5-15) sin que la población inicial tarde horas en completarse. |
| Genetic options | `MaxGenerations` | 10 | 30 | Con 10 generaciones la evolución apenas actúa (y el reinicio por estancamiento a 30 nunca saltaba). |
| Genetic options | `Islands` | 5 | 4 | 4 islas: diversidad suficiente con menos coste. |
| Genetic options | `CrossoverProbability` | 46 | 80 | 46 % es bajo para un AG; 70-90 % es lo habitual (supuesto de práctica general, no de SQX). |
| Genetic options | `MutationProbability` | 35 | 30 | Algo menor para no destruir buenas soluciones. |
| Genetic options | `MigrationModulo` | 5 | 10 | Migrar cada 10 generaciones (con 30-40 generaciones). |
| Genetic options | `MigrationRate` | 6 | 10 | 6 % de 5 individuos = 0,3: la migración original era nula en la práctica. |
| Genetic options | `EvoRestartOnStagnation@generations` | 30 | 15 | Debe ser menor que MaxGenerations para poder actuar. |
| Genetic options | `BuildMode/Conditions (población inicial)` | ReturnDDRatio(IS) >= 2; AvgBarsInTrade(IS) >= 2; NumberOfTrades(IS) >= 250; WinningPct(IS) >= 35 | NumberOfTrades(IS) >= 60 | SÓLO nº mínimo de operaciones (30 % del mínimo final), como recomienda SQX. La población inicial no se guarda en el banco y SQX genera aleatorias hasta completarla: con 80-100 individuos y filtros de rentabilidad (Ret/DD, acierto) el Builder puede pasar horas o días sin producir nada. La exigencia de calidad está en los filtros del Ranking. |
| Ranking | `Rankings/Conditions (filtros)` | AvgBarsInTrade(IS) >= 2; ReturnDDRatio(IS) >= 4; NumberOfTrades(IS) >= 300; WinningPct(IS) >= 40 | NumberOfTrades(IS) >= 210; ReturnDDRatio(IS) >= 1.5; WinningPct(IS) >= 30; ProfitFactor(IS) >= 1.15; AvgBarsInTrade(IS) >= 2; NetProfit(OOS) > 0; NumberOfTrades(OOS) >= 70 | Mínimo de operaciones = 60/año × años de cada tramo (el original exigía 300 en 7,25 años ≈ 41/año; ningún estilo baja de esa densidad salvo Position) + umbrales del estilo + exigencia en el tramo de validación OOS, que el original no tenía. Test de ventaja: Ret/DD a la mitad, PF mínimo 1,15. |
| Ranking | `FitnessCriteria/Settings/Ranking` | Weighted: Stagnation (peso 1, min) | Weighted: SQN (peso 2, max), StagnationPct (peso 1, min) | SQN mide la calidad estadística de la entrada (expectativa/desviación·√N); el original optimizaba sólo 'Stagnation', que ignora el beneficio. |
| Data | `Setup/Chart@timeframe` | H1 | M15 | Timeframe del estilo NewsProxy. |
| Data | `Setup@slippage` | 0 | 1.5 | En publicaciones el deslizamiento real es de varios pips; 1,5 pips es el mínimo prudente. |
| Data | `Setup@dateFrom` | 2013.09.30 | 2016.01.04 | M5/M15: 5 años bastan en operaciones y reducen el cómputo. |
| Data | `OutOfSample/Range` | (sin OOS) | 2019.07.01–2020.12.31 | Nuevo tramo de validación dentro del Builder (el original no tenía OOS y filtraba sólo sobre IS). |
| Cross checks | `RetestOnAdditionalMarkets/Setup@timeframe` | H1 | M15 | Coherencia si se activa (sigue desactivado). |
| Building blocks | `Calibration@calibrateBeforeStart` | false | true | Recalibra antes de empezar los rangos de valores de los indicadores (p. ej. ATR y rangos de órdenes stop/limit, que traen ±5000 por defecto) con el símbolo y timeframe de Data. Sin ello, al cambiar de H1 a M5/M15/H4/D1 las comparaciones con números y los desplazamientos de órdenes stop/limit no tienen sentido. |
| Building blocks | `Bloques activos · signals` | 146 activos | 54 activos: ATRChangesUp(w4), ATRRising(w4), AWOChangesUp(w1), AWORising(w1), AvgVolumeRising(w2), BBBarClosesAboveUp(w2), BBBarOpensAboveUp(w2), BBBarOpensAboveUpAfterOpenBelow(w2), BBLowerFalling(w4), BBUpperRising(w4), BarDayOfWeekIs(w3), BarDayOfWeekIsNot(w2), BarHourIs(w3), BarHourIsBigger(w2), BarHourIsSmaller(w2), BarOpensAboveHighestAfterOpenBelow(w6), CCIChangesUp(w1), CCIRising(w1), DEMChangesUp(w1), DEMRising(w1), FastReflexCrossUPSlowReflex(w1), KCBarClosesAboveUpper(w2), KCBarOpensAboveUpper(w2), KCBarOpensAboveUpperAfterOpenBelow(w2), KCLowerFalling(w4), KCUpperRising(w4), LaguerreRSIChangesUP(w1), LaguerreRSIRising(w1), MACDMainChangesUp(w1), MACDMainCrossAboveSignal(w1), MACDMainHigherSignal(w1), MACDMainRising(w1), MACDSignalRising(w1), MomChangesUp(w1), MomRising(w1), OSMAChangesUp(w1), OSMARising(w1), QQEValue1CrossAboveValue2(w1), QQEValue1HigherValue2(w1), QQEValue1Rising(w1), QQEValue2Rising(w1), ROCRising(w1), RSIChangesUp(w1), RSIRising(w1), ReflexChangesDirectionUP(w1), ReflexRising(w1), StdDevChangesUp(w4), StdDevRising(w4), StochFastKUp(w1), StochSlowDChangesUp(w1), StochSlowDRising(w1), VolumeRising(w2), WPRChangesUp(w1), WPRRising(w1) | Núcleo: rango previo a la publicación (12:00-15:00 → 15:00/15:30), filtros de hora/día y expansión de volatilidad y de volumen de ticks; órdenes stop sobre el rango pre-dato. |
| Building blocks | `Bloques activos · indicators` | 29 activos | 38 activos: CrossesAbove(w1), CrossesBelow(w1), Indicators.ATR(w2), Indicators.BollingerBands(w1), Indicators.EMA(w1), Indicators.Highest(w2), Indicators.HighestInRange(w4), Indicators.HullMovingAverage(w1), Indicators.KAMA(w1), Indicators.KeltnerChannel(w1), Indicators.LWMA(w1), Indicators.LinearRegression(w1), Indicators.Lowest(w2), Indicators.LowestInRange(w2), Indicators.SMA(w1), Indicators.SMMA(w1), Indicators.TEMA(w1), Indicators.TrueRange(w2), IsFalling(w1), IsGreater(w1), IsGreaterCount(w1), IsGreaterOrEqual(w1), IsLower(w1), IsLowerCount(w1), IsLowerOrEqual(w1), IsRising(w1), Prices.Close(w1), Prices.CloseD(w1), Prices.High(w1), Prices.HighD(w1), Prices.Low(w1), Prices.LowD(w1), Prices.Open(w1), Prices.OpenD(w1), Prices.SessionClose(w4), Prices.SessionHigh(w4), Prices.SessionLow(w2), Prices.SessionOpen(w4) | Núcleo: rango previo a la publicación (12:00-15:00 → 15:00/15:30), filtros de hora/día y expansión de volatilidad y de volumen de ticks; órdenes stop sobre el rango pre-dato. |
| Building blocks | `Bloques activos · stopLimitBlocks` | 29 activos | 26 activos: Stop/Limit Price Levels.BollingerBands(w1), Stop/Limit Price Levels.Close(w2), Stop/Limit Price Levels.CloseD(w1), Stop/Limit Price Levels.High(w2), Stop/Limit Price Levels.HighD(w1), Stop/Limit Price Levels.Highest(w2), Stop/Limit Price Levels.HighestInRange(w5), Stop/Limit Price Levels.KeltnerChannel(w1), Stop/Limit Price Levels.Low(w1), Stop/Limit Price Levels.LowD(w1), Stop/Limit Price Levels.Lowest(w1), Stop/Limit Price Levels.LowestInRange(w1), Stop/Limit Price Levels.MTKeltnerChannel(w1), Stop/Limit Price Levels.Open(w2), Stop/Limit Price Levels.OpenD(w1), Stop/Limit Price Levels.SessionHigh(w5), Stop/Limit Price Levels.SessionLow(w1), Stop/Limit Price Levels.SessionOpen(w5), Stop/Limit Price Ranges.ATR(w3), Stop/Limit Price Ranges.BBRange(w3), Stop/Limit Price Ranges.BBWidthRatio(w3), Stop/Limit Price Ranges.BarRange(w3), Stop/Limit Price Ranges.BiggestRange(w3), Stop/Limit Price Ranges.MTATR(w3), Stop/Limit Price Ranges.SmallestRange(w3), Stop/Limit Price Ranges.TrueRange(w3) | Núcleo: rango previo a la publicación (12:00-15:00 → 15:00/15:30), filtros de hora/día y expansión de volatilidad y de volumen de ticks; órdenes stop sobre el rango pre-dato. |
| Building blocks | `Indicators.HighestInRange · Time From` | 0..2359/30 | 1200..1500/100 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Indicators.HighestInRange · Time To` | 0..2359/30 | 1500..1530/30 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Indicators.LowestInRange · Time From` | 0..2359/30 | 1200..1500/100 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Indicators.LowestInRange · Time To` | 0..2359/30 | 1500..1530/30 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Stop/Limit Price Levels.HighestInRange · Time From` | 0..2359/30 | 1200..1500/100 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Stop/Limit Price Levels.HighestInRange · Time To` | 0..2359/30 | 1500..1530/30 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Stop/Limit Price Levels.LowestInRange · Time From` | 0..2359/30 | 1200..1500/100 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Stop/Limit Price Levels.LowestInRange · Time To` | 0..2359/30 | 1500..1530/30 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Prices.SessionHigh · Start Hours` | 0..23/1 | 12..14/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Prices.SessionHigh · Start Minutes` | 0..59/1 | 0..0/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Prices.SessionHigh · End Hours` | 0..23/1 | 15..15/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Prices.SessionHigh · End Minutes` | 0..59/1 | 0..0/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Prices.SessionLow · Start Hours` | 0..23/1 | 12..14/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Prices.SessionLow · Start Minutes` | 0..59/1 | 0..0/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Prices.SessionLow · End Hours` | 0..23/1 | 15..15/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Prices.SessionLow · End Minutes` | 0..59/1 | 0..0/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Stop/Limit Price Levels.SessionHigh · Start Hours` | 0..23/1 | 12..14/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Stop/Limit Price Levels.SessionHigh · Start Minutes` | 0..59/1 | 0..0/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Stop/Limit Price Levels.SessionHigh · End Hours` | 0..23/1 | 15..15/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Stop/Limit Price Levels.SessionHigh · End Minutes` | 0..59/1 | 0..0/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Stop/Limit Price Levels.SessionLow · Start Hours` | 0..23/1 | 12..14/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Stop/Limit Price Levels.SessionLow · Start Minutes` | 0..59/1 | 0..0/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Stop/Limit Price Levels.SessionLow · End Hours` | 0..23/1 | 15..15/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Stop/Limit Price Levels.SessionLow · End Minutes` | 0..59/1 | 0..0/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Prices.SessionOpen · Start Hours` | 0..23/1 | 12..14/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Prices.SessionOpen · Start Minutes` | 0..59/1 | 0..0/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Stop/Limit Price Levels.SessionOpen · Start Hours` | 0..23/1 | 12..14/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Stop/Limit Price Levels.SessionOpen · Start Minutes` | 0..59/1 | 0..0/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Prices.SessionClose · End Hours` | 0..23/1 | 15..15/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Prices.SessionClose · End Minutes` | 0..59/1 | 0..0/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `BarHourIs · Hour` | 0..23/1 | 15..16/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `BarHourIsBigger · Hour` | 0..23/1 | 14..16/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `BarHourIsSmaller · Hour` | 0..23/1 | 16..18/1 | Rango acotado al estilo (ver ficha). |
| Order types | `EnterAtStop@use` | false | true | Stop sobre el rango pre-dato (bajo él en SELL), caduca en 15-60 min. |
| Order types | `EnterAtStop@weight` | 1 | 3 | Peso relativo entre tipos de orden. |
| Order types | `EnterAtStop · BarsValid min` | 2 | 1 | Stop sobre el rango pre-dato (bajo él en SELL), caduca en 15-60 min. |
| Order types | `EnterAtStop · BarsValid max` | 10 | 4 | Stop sobre el rango pre-dato (bajo él en SELL), caduca en 15-60 min. |
| Order types | `EnterAtStop · ExitAfterBars min` | 5 | 2 | Alineado con el rango de ExitTypes para eliminar la ambigüedad del original (5-20 vs 2-15). |
| Order types | `EnterAtStop · ExitAfterBars max` | 20 | 12 | Alineado con el rango de ExitTypes. |
| Order types | `EnterAtMarket · ExitAfterBars min` | 5 | 2 | Alineado con el rango de ExitTypes para eliminar la ambigüedad del original (5-20 vs 2-15). |
| Order types | `EnterAtMarket · ExitAfterBars max` | 20 | 12 | Alineado con el rango de ExitTypes. |
| Exit types | `ExitAfterBars@probability` | 50 | 100 | Explícito: es la única salida (el original ponía 50 y dependía de minExitTypes=1). |
| Exit types | `ExitAfterBars max` | 15 | 12 | Test de ventaja: salida por tiempo 30 min-3 h. |
| Notes | `Notes` | <b>Breakout strategies setup</b><div><br></div><div><br></div><div><br></div><div><br></div> | <b>Noticias (APROXIMACIÓN horaria: ventana de datos de EE. UU.) – Builder de test de ventaja (entrada) – BUY</b><div>Derivado de Ventaja_Build_ConfigInicial_H1_BUY (build 140.2099). Timeframe M15. Ver docs/03 (ficha NewsProxy) y docs/04 (checklist).</div><div>NO VALIDADO EN SQX: revisar símbolo, costes, horario del servidor e importación.</div> | Descripción del estilo y advertencias. |
