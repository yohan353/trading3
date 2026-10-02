# Ventaja_Build_ConfigInicial_H1_BUY__DayTrading_M15_BUY

*Original:* `Ventaja_Build_ConfigInicial_H1_BUY.cfx` · *Estilo:* Day Trading (ruptura del rango asiático) · *Timeframe:* M15 · *Rol:* Builder de test de ventaja (entrada) · *Dirección:* BUY

Tabla generada automáticamente a partir de los cambios aplicados al XML (cada fila es un valor que difiere del original). Estado: **no validado en SQX** (ver docs/04).

| Sección | Parámetro | Valor original | Valor nuevo | Justificación |
|---|---|---|---|---|
| Task | `Task@templateFile` | C:\Users\<usuario>\Desktop\Ventaja_Build_ConfigInicial_H1_BUY.cfx | Ventaja_Build_ConfigInicial_H1_BUY__DayTrading_M15_BUY.cfx | Ruta local del autor (C:\Users\<usuario>\Desktop\...) sustituida por el nombre del nuevo archivo: no aporta nada y expone el nombre de usuario de Windows. |
| Trading options | `Param key="SignalTimeRangeFrom"` | 5400 | 32400 | Apertura de Londres (servidor UTC+2). |
| Trading options | `Param key="SignalTimeRangeTo"` | 84600 | 68400 | Tras las 19:00 queda poco recorrido intradía. |
| Trading options | `Param key="ExitAtEndOfDay"` | false | true | Definición de day trading: plano al cierre. |
| Trading options | `Param key="EODExitTime"` | 83040 | 81000 | Antes del rollover de las 00:00 servidor. |
| Trading options | `Param key="ExitOnFriday"` | false | true | Sin exposición de fin de semana. |
| Trading options | `Param key="FridayExitTime"` | 74400 | 77400 | Viernes, cierre algo antes. |
| Trading options | `Param key="MaxTradesPerDay"` | 0 | 3 | La ruptura y hasta dos reintentos. |
| Trading options | `Param key="MaxDistanceFromMarket"` | false | true | Evita órdenes stop alejadas del precio. |
| Trading options | `Param key="MaxDistancePct"` | 6 | 0.6 | ≈ 90 pips en GBPJPY: cubre rangos asiáticos amplios. |
| Trading options | `Param key="ReservedBars"` | 50 | 120 | ≥ periodo máximo (100). |
| What to build · complejidad | `Chart@maxExitTypes` | 5 | 1 | Test de ventaja: sólo salida temporal, para medir la entrada aislada. |
| What to build · complejidad | `Chart@minPeriod` | 4 | 5 | 5-100 velas de M15 = 1 h 15 min a 25 h: contexto intradía y del día anterior. |
| What to build · complejidad | `Chart@maxPeriod` | 200 | 100 | 5-100 velas de M15 = 1 h 15 min a 25 h: contexto intradía y del día anterior. |
| Genetic options | `PopulationSize` | 15 | 25 | 25 por isla × 4 islas = 100 por generación: más diversidad que el original (5-15) sin que la población inicial tarde horas en completarse. |
| Genetic options | `MaxGenerations` | 10 | 30 | Con 10 generaciones la evolución apenas actúa (y el reinicio por estancamiento a 30 nunca saltaba). |
| Genetic options | `Islands` | 5 | 4 | 4 islas: diversidad suficiente con menos coste. |
| Genetic options | `CrossoverProbability` | 46 | 80 | 46 % es bajo para un AG; 70-90 % es lo habitual (supuesto de práctica general, no de SQX). |
| Genetic options | `MutationProbability` | 35 | 30 | Algo menor para no destruir buenas soluciones. |
| Genetic options | `MigrationModulo` | 5 | 10 | Migrar cada 10 generaciones (con 30-40 generaciones). |
| Genetic options | `MigrationRate` | 6 | 10 | 6 % de 5 individuos = 0,3: la migración original era nula en la práctica. |
| Genetic options | `EvoRestartOnStagnation@generations` | 30 | 15 | Debe ser menor que MaxGenerations para poder actuar. |
| Genetic options | `BuildMode/Conditions (población inicial)` | ReturnDDRatio(IS) >= 2; AvgBarsInTrade(IS) >= 2; NumberOfTrades(IS) >= 250; WinningPct(IS) >= 35 | NumberOfTrades(IS) >= 190 | SÓLO nº mínimo de operaciones (30 % del mínimo final), como recomienda SQX. La población inicial no se guarda en el banco y SQX genera aleatorias hasta completarla: con 80-100 individuos y filtros de rentabilidad (Ret/DD, acierto) el Builder puede pasar horas o días sin producir nada. La exigencia de calidad está en los filtros del Ranking. |
| Ranking | `Rankings/Conditions (filtros)` | AvgBarsInTrade(IS) >= 2; ReturnDDRatio(IS) >= 4; NumberOfTrades(IS) >= 300; WinningPct(IS) >= 40 | NumberOfTrades(IS) >= 630; ReturnDDRatio(IS) >= 2.5; WinningPct(IS) >= 35; ProfitFactor(IS) >= 1.15; AvgBarsInTrade(IS) >= 2; NetProfit(OOS) > 0; NumberOfTrades(OOS) >= 190 | Mínimo de operaciones = 120/año × años de cada tramo (el original exigía 300 en 7,25 años ≈ 41/año; ningún estilo baja de esa densidad salvo Position) + umbrales del estilo + exigencia en el tramo de validación OOS, que el original no tenía. Test de ventaja: Ret/DD a la mitad, PF mínimo 1,15. |
| Ranking | `FitnessCriteria/Settings/Ranking` | Weighted: Stagnation (peso 1, min) | Weighted: SQN (peso 2, max), StagnationPct (peso 1, min) | SQN mide la calidad estadística de la entrada (expectativa/desviación·√N); el original optimizaba sólo 'Stagnation', que ignora el beneficio. |
| Data | `Setup/Chart@timeframe` | H1 | M15 | Timeframe del estilo DayTrading. |
| Data | `Setup@slippage` | 0 | 0.3 | El original usa 0; 0,3 pips por ejecución stop en apertura de Londres. |
| Data | `OutOfSample/Range` | (sin OOS) | 2019.01.01–2020.12.31 | Nuevo tramo de validación dentro del Builder (el original no tenía OOS y filtraba sólo sobre IS). |
| Cross checks | `RetestOnAdditionalMarkets/Setup@timeframe` | H1 | M15 | Coherencia si se activa (sigue desactivado). |
| Building blocks | `Calibration@calibrateBeforeStart` | false | true | Recalibra antes de empezar los rangos de valores de los indicadores (p. ej. ATR y rangos de órdenes stop/limit, que traen ±5000 por defecto) con el símbolo y timeframe de Data. Sin ello, al cambiar de H1 a M5/M15/H4/D1 las comparaciones con números y los desplazamientos de órdenes stop/limit no tienen sentido. |
| Building blocks | `Bloques activos · signals` | 146 activos | 110 activos: ADXChangesUp(w1), ADXCrossUp(w1), ADXHigher(w1), ADXRising(w1), ATRChangesUp(w2), ATRRising(w2), AWOChangesUp(w1), AWORising(w1), AroonCrossesAbove(w1), AvgVolumeRising(w1), BBBarClosesAboveUp(w3), BBBarOpensAboveUp(w3), BBBarOpensAboveUpAfterOpenBelow(w3), BBLowerFalling(w2), BBUpperRising(w2), BarClosesAboveKAMA(w1), BarClosesAboveSuperTrend(w1), BarDayOfWeekIsNot(w2), BarHourIsBigger(w2), BarHourIsSmaller(w2), BarOpensAboveHighestAfterOpenBelow(w8), CCIChangesUp(w1), CCICrossUp(w1), CCIHigher(w1), CCIRising(w1), DEMChangesUp(w1), DEMRising(w1), DICrossUp(w1), DIMinusChangesDown(w1), DIMinusFalling(w1), DIPlusChangesUp(w1), DIPlusHigher(w1), DIPlusRising(w1), FastKAMAAboveSlowKAMA(w1), FastReflexCrossUPSlowReflex(w1), FasterHMAIsAboveSlowerHMA(w1), GannHiLoUPTrend(w1), HMAChangesUP(w1), HMARising(w1), IchimokuKijunSenCrossBullish(w1), IchimokuKumoBreakoutBullish(w1), IchimokuSenkouSpanCrossBullish(w1), IchimokuTenkanKijunCrossBullish(w1), IsUptrend(w1), KAMARising(w1), KCBarClosesAboveUpper(w3), KCBarOpensAboveUpper(w3), KCBarOpensAboveUpperAfterOpenBelow(w3), KCLowerFalling(w2), KCUpperRising(w2), KERaboveLevel(w1), LaguerreRSIChangesUP(w1), LaguerreRSICrossUP(w1), LaguerreRSIRising(w1), LinRegBarClosesAbove(w1), LinRegBarOpensAbove(w1), LinRegBarOpensAboveAfterOpenBelow(w1), LinRegRising(w1), MABarClosesAbove(w1), MABarOpensAbove(w1), MABarOpensAboveAfterOpenBelow(w1), MACDMainChangesUp(w1), MACDMainCrossAboveSignal(w1), MACDMainCrossAboveZero(w1), MACDMainHigherSignal(w1), MACDMainHigherZero(w1), MACDMainRising(w1), MACDSignalRising(w1), MARising(w1), MomChangesUp(w1), MomRising(w1), OSMAChangesUp(w1), OSMACrossZeroUp(w1), OSMAHigherZero(w1), OSMARising(w1), PSARBarLower(w1), QQEValue1CrossAbove(w1), QQEValue1CrossAboveValue2(w1), QQEValue1Higher(w1), QQEValue1HigherValue2(w1), QQEValue1Rising(w1), QQEValue2Rising(w1), ROCAboveLevel(w1), ROCCrossesAboveLevel(w1), ROCRising(w1), RSIChangesUp(w1), RSICrossUp(w1), RSIHigher(w1), RSIRising(w1), ReflexChangesDirectionUP(w1), ReflexRising(w1), SchaffTrendCycleAboveLevel(w1), SchaffTrendCycleCrossesAboveLevel(w1), StdDevChangesUp(w2), StdDevRising(w2), StochFastKUp(w1), StochSlowDChangesUp(w1), StochSlowDCrossUp(w1), StochSlowDHigher(w1), StochSlowDRising(w1), SuperTrendUPTrend(w1), VolumeRising(w1), VortexChangesTrendUP(w1), VortexUptrend(w1), WPRChangesUp(w1), WPRCrossUp(w1), WPRHigher(w1), WPRRising(w1), WoodiesCCIZeroLineBreakUP(w1), WoodiesTrendUP(w1) | Núcleo: extremos del rango asiático (HighestInRange 00:00-03:00 → 07:00-10:00 en horas enteras; el original usaba paso 30 sobre HHMM, que genera horas inválidas como 0060), niveles del día anterior y aperturas de sesión, con órdenes stop en ellos. Filtros amplios a peso 1. |
| Building blocks | `Bloques activos · indicators` | 29 activos | 52 activos: CrossesAbove(w1), CrossesBelow(w1), Indicators.ADX(w1), Indicators.ATR(w1), Indicators.Aroon(w1), Indicators.BollingerBands(w1), Indicators.CCI(w1), Indicators.DeMarker(w1), Indicators.EMA(w1), Indicators.GannHiLo(w1), Indicators.Highest(w2), Indicators.HighestInRange(w4), Indicators.HullMovingAverage(w1), Indicators.Ichimoku(w1), Indicators.KAMA(w1), Indicators.KaufmanEfficiencyRatio(w1), Indicators.KeltnerChannel(w1), Indicators.LWMA(w1), Indicators.LaguerreRSI(w1), Indicators.LinearRegression(w1), Indicators.Lowest(w2), Indicators.LowestInRange(w2), Indicators.ParabolicSAR(w1), Indicators.RSI(w1), Indicators.SMA(w1), Indicators.SMMA(w1), Indicators.Stochastic(w1), Indicators.SuperTrend(w1), Indicators.TEMA(w1), Indicators.TrueRange(w1), Indicators.Vortex(w1), Indicators.WilliamsPR(w1), IsFalling(w1), IsGreater(w1), IsGreaterCount(w1), IsGreaterOrEqual(w1), IsLower(w1), IsLowerCount(w1), IsLowerOrEqual(w1), IsRising(w1), Prices.Close(w1), Prices.CloseD(w2), Prices.High(w1), Prices.HighD(w2), Prices.Low(w1), Prices.LowD(w2), Prices.Open(w1), Prices.OpenD(w2), Prices.SessionClose(w4), Prices.SessionHigh(w4), Prices.SessionLow(w2), Prices.SessionOpen(w4) | Núcleo: extremos del rango asiático (HighestInRange 00:00-03:00 → 07:00-10:00 en horas enteras; el original usaba paso 30 sobre HHMM, que genera horas inválidas como 0060), niveles del día anterior y aperturas de sesión, con órdenes stop en ellos. Filtros amplios a peso 1. |
| Building blocks | `Bloques activos · stopLimitBlocks` | 29 activos | 40 activos: Stop/Limit Price Levels.BollingerBands(w1), Stop/Limit Price Levels.Close(w2), Stop/Limit Price Levels.CloseD(w3), Stop/Limit Price Levels.EMA(w1), Stop/Limit Price Levels.Fractal(w1), Stop/Limit Price Levels.GannHiLo(w1), Stop/Limit Price Levels.High(w2), Stop/Limit Price Levels.HighD(w3), Stop/Limit Price Levels.Highest(w2), Stop/Limit Price Levels.HighestInRange(w5), Stop/Limit Price Levels.HullMovingAverage(w1), Stop/Limit Price Levels.Ichimoku(w1), Stop/Limit Price Levels.KAMA(w1), Stop/Limit Price Levels.KeltnerChannel(w1), Stop/Limit Price Levels.LWMA(w1), Stop/Limit Price Levels.LinearRegression(w1), Stop/Limit Price Levels.Low(w1), Stop/Limit Price Levels.LowD(w1), Stop/Limit Price Levels.Lowest(w1), Stop/Limit Price Levels.LowestInRange(w1), Stop/Limit Price Levels.MTKeltnerChannel(w1), Stop/Limit Price Levels.Open(w2), Stop/Limit Price Levels.OpenD(w3), Stop/Limit Price Levels.ParabolicSAR(w1), Stop/Limit Price Levels.Pivots(w1), Stop/Limit Price Levels.SMA(w1), Stop/Limit Price Levels.SMMA(w1), Stop/Limit Price Levels.SessionHigh(w5), Stop/Limit Price Levels.SessionLow(w1), Stop/Limit Price Levels.SessionOpen(w5), Stop/Limit Price Levels.SuperTrend(w1), Stop/Limit Price Levels.TEMA(w1), Stop/Limit Price Ranges.ATR(w2), Stop/Limit Price Ranges.BBRange(w2), Stop/Limit Price Ranges.BBWidthRatio(w2), Stop/Limit Price Ranges.BarRange(w2), Stop/Limit Price Ranges.BiggestRange(w2), Stop/Limit Price Ranges.MTATR(w2), Stop/Limit Price Ranges.SmallestRange(w2), Stop/Limit Price Ranges.TrueRange(w2) | Núcleo: extremos del rango asiático (HighestInRange 00:00-03:00 → 07:00-10:00 en horas enteras; el original usaba paso 30 sobre HHMM, que genera horas inválidas como 0060), niveles del día anterior y aperturas de sesión, con órdenes stop en ellos. Filtros amplios a peso 1. |
| Building blocks | `RSIHigher · Level` | 0..100/5 | 50..70/5 | Rango acotado al estilo (ver ficha). |
| Building blocks | `RSICrossUp · Level` | 0..100/5 | 50..70/5 | Rango acotado al estilo (ver ficha). |
| Building blocks | `LaguerreRSICrossUP · Gamma` | 0..0.95/0.01 | 0.3..0.8/0.05 | Rango acotado al estilo (ver ficha). |
| Building blocks | `LaguerreRSICrossUP · Level` | 0.05..0.95/0.05 | 0.4..0.85/0.05 | Rango acotado al estilo (ver ficha). |
| Building blocks | `StochSlowDHigher · Level` | 0..100/5 | 50..80/5 | Rango acotado al estilo (ver ficha). |
| Building blocks | `StochSlowDCrossUp · Level` | 0..100/5 | 50..80/5 | Rango acotado al estilo (ver ficha). |
| Building blocks | `CCIHigher · Level` | -120..120/5 | 0..150/10 | Rango acotado al estilo (ver ficha). |
| Building blocks | `CCICrossUp · Level` | -120..120/5 | 0..150/10 | Rango acotado al estilo (ver ficha). |
| Building blocks | `WPRHigher · Level` | -100..0/5 | -50..-20/5 | Rango acotado al estilo (ver ficha). |
| Building blocks | `WPRCrossUp · Level` | -100..0/5 | -50..-20/5 | Rango acotado al estilo (ver ficha). |
| Building blocks | `QQEValue1Higher · Level` | 20..90/5 | 50..70/5 | Rango acotado al estilo (ver ficha). |
| Building blocks | `QQEValue1CrossAbove · Level` | 20..90/5 | 50..70/5 | Rango acotado al estilo (ver ficha). |
| Building blocks | `SchaffTrendCycleAboveLevel · Level` | 10..99.9/0.1 | 50..90/5 | Rango acotado al estilo (ver ficha). |
| Building blocks | `SchaffTrendCycleCrossesAboveLevel · Level` | 0.1..99.9/0.1 | 25..75/5 | Rango acotado al estilo (ver ficha). |
| Building blocks | `ADXHigher · Level` | 20..90/10 | 20..40/5 | Rango acotado al estilo (ver ficha). |
| Building blocks | `ADXCrossUp · Level` | 20..90/10 | 20..35/5 | Rango acotado al estilo (ver ficha). |
| Building blocks | `KERaboveLevel · Level` | 0..0.95/0.05 | 0.3..0.7/0.05 | Rango acotado al estilo (ver ficha). |
| Building blocks | `SuperTrendUPTrend · ATR Mult` | 0.5..10/0.1 | 1.5..5/0.5 | Rango acotado al estilo (ver ficha). |
| Building blocks | `BarClosesAboveSuperTrend · ATR Mult` | 0.5..10/0.1 | 1.5..5/0.5 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Indicators.SuperTrend · ATR Mult` | 0.5..10/0.1 | 1.5..5/0.5 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Stop/Limit Price Levels.SuperTrend · ATR Mult` | 0.5..10/0.1 | 1.5..5/0.5 | Rango acotado al estilo (ver ficha). |
| Building blocks | `ROCAboveLevel · Level` | -100..100/0.001 | 0..1/0.05 | Rango acotado al estilo (ver ficha). |
| Building blocks | `ROCCrossesAboveLevel · Level` | -100..100/0.001 | 0..1/0.05 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Indicators.HighestInRange · Time From` | 0..2359/30 | 0..300/100 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Indicators.HighestInRange · Time To` | 0..2359/30 | 700..1000/100 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Indicators.LowestInRange · Time From` | 0..2359/30 | 0..300/100 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Indicators.LowestInRange · Time To` | 0..2359/30 | 700..1000/100 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Stop/Limit Price Levels.HighestInRange · Time From` | 0..2359/30 | 0..300/100 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Stop/Limit Price Levels.HighestInRange · Time To` | 0..2359/30 | 700..1000/100 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Stop/Limit Price Levels.LowestInRange · Time From` | 0..2359/30 | 0..300/100 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Stop/Limit Price Levels.LowestInRange · Time To` | 0..2359/30 | 700..1000/100 | Rango acotado al estilo (ver ficha). |
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
| Building blocks | `Stop/Limit Price Levels.SessionLow · Start Hours` | 0..23/1 | 1..3/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Stop/Limit Price Levels.SessionLow · Start Minutes` | 0..59/1 | 0..0/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Stop/Limit Price Levels.SessionLow · End Hours` | 0..23/1 | 8..10/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Stop/Limit Price Levels.SessionLow · End Minutes` | 0..59/1 | 0..0/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Prices.SessionOpen · Start Hours` | 0..23/1 | 8..10/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Prices.SessionOpen · Start Minutes` | 0..59/1 | 0..0/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Stop/Limit Price Levels.SessionOpen · Start Hours` | 0..23/1 | 8..10/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Stop/Limit Price Levels.SessionOpen · Start Minutes` | 0..59/1 | 0..0/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Prices.SessionClose · End Hours` | 0..23/1 | 8..10/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Prices.SessionClose · End Minutes` | 0..59/1 | 0..0/1 | Rango acotado al estilo (ver ficha). |
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
| Notes | `Notes` | <b>Breakout strategies setup</b><div><br></div><div><br></div><div><br></div><div><br></div> | <b>Day Trading (ruptura del rango asiático) – Builder de test de ventaja (entrada) – BUY</b><div>Derivado de Ventaja_Build_ConfigInicial_H1_BUY (build 140.2099). Timeframe M15. Ver docs/03 (ficha DayTrading) y docs/04 (checklist).</div><div>NO VALIDADO EN SQX: revisar símbolo, costes, horario del servidor e importación.</div> | Descripción del estilo y advertencias. |
