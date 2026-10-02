# Ventaja_Build_ConfigInicial_H1_BUY__DayTrading_M15_SELL

*Original:* `Ventaja_Build_ConfigInicial_H1_BUY.cfx` · *Estilo:* Day Trading (ruptura del rango asiático) · *Timeframe:* M15 · *Rol:* Builder de test de ventaja (entrada) · *Dirección:* SELL

Tabla generada automáticamente a partir de los cambios aplicados al XML (cada fila es un valor que difiere del original). Estado: **no validado en SQX** (ver docs/04).

| Sección | Parámetro | Valor original | Valor nuevo | Justificación |
|---|---|---|---|---|
| Task | `Task@templateFile` | C:\Users\<usuario>\Desktop\Ventaja_Build_ConfigInicial_H1_BUY.cfx | Ventaja_Build_ConfigInicial_H1_BUY__DayTrading_M15_SELL.cfx | Ruta local del autor (C:\Users\<usuario>\Desktop\...) sustituida por el nombre del nuevo archivo: no aporta nada y expone el nombre de usuario de Windows. |
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
| What to build | `MarketSides@type` | long | short | Kit SELL: sólo ventas. Sin simetría, SQX usa los bloques tal cual, por eso se activan los equivalentes bajistas (espejo) en Building blocks. |
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
| Genetic options | `BuildMode/Conditions (población inicial)` | ReturnDDRatio(IS) >= 2; AvgBarsInTrade(IS) >= 2; NumberOfTrades(IS) >= 250; WinningPct(IS) >= 35 | ReturnDDRatio(IS) >= 1.25; AvgBarsInTrade(IS) >= 2; NumberOfTrades(IS) >= 522; WinningPct(IS) >= 30 | Misma lógica del autor (≈60 % del Ret/DD final, ≈83 % de las operaciones, -5 puntos de acierto) con los umbrales del estilo. |
| Ranking | `Rankings/Conditions (filtros)` | AvgBarsInTrade(IS) >= 2; ReturnDDRatio(IS) >= 4; NumberOfTrades(IS) >= 300; WinningPct(IS) >= 40 | NumberOfTrades(IS) >= 630; ReturnDDRatio(IS) >= 2.5; WinningPct(IS) >= 35; ProfitFactor(IS) >= 1.15; AvgBarsInTrade(IS) >= 2; NetProfit(OOS) > 0; NumberOfTrades(OOS) >= 190 | Mínimo de operaciones = 120/año × años de cada tramo (el original exigía 300 en 7,25 años ≈ 41/año; ningún estilo baja de esa densidad salvo Position) + umbrales del estilo + exigencia en el tramo de validación OOS, que el original no tenía. Test de ventaja: Ret/DD a la mitad, PF mínimo 1,15. |
| Ranking | `FitnessCriteria/Settings/Ranking` | Weighted: Stagnation (peso 1, min) | Weighted: SQN (peso 2, max), StagnationPct (peso 1, min) | SQN mide la calidad estadística de la entrada (expectativa/desviación·√N); el original optimizaba sólo 'Stagnation', que ignora el beneficio. |
| Data | `Setup/Chart@timeframe` | H1 | M15 | Timeframe del estilo DayTrading. |
| Data | `Setup@slippage` | 0 | 0.3 | El original usa 0; 0,3 pips por ejecución stop en apertura de Londres. |
| Data | `OutOfSample/Range` | (sin OOS) | 2019.01.01–2020.12.31 | Nuevo tramo de validación dentro del Builder (el original no tenía OOS y filtraba sólo sobre IS). |
| Cross checks | `RetestOnAdditionalMarkets/Setup@timeframe` | H1 | M15 | Coherencia si se activa (sigue desactivado). |
| Building blocks | `Bloques activos · signals` | 146 activos | 112 activos: ADXChangesUp(w1), ADXCrossUp(w1), ADXHigher(w1), ADXRising(w1), ATRChangesUp(w2), ATRRising(w2), AWOChangesDown(w1), AWOFalling(w1), AroonCrossesBelow(w1), AvgVolumeRising(w1), BBBarClosesBelowDown(w3), BBBarOpensBelowDown(w3), BBBarOpensBelowDownAfterOpenAbove(w3), BBLowerFalling(w2), BBUpperRising(w2), BarClosesBelowKAMA(w1), BarClosesBelowSuperTrend(w1), BarDayOfWeekIs(w2), BarDayOfWeekIsNot(w2), BarHourIs(w2), BarHourIsBigger(w2), BarHourIsSmaller(w2), BarOpensBelowLowestAfterOpenAbove(w8), CCIChangesDown(w1), CCICrossDown(w1), CCIFalling(w1), CCILower(w1), DEMChangesDown(w1), DEMFalling(w1), DICrossDown(w1), DIMinusChangesUp(w1), DIMinusRising(w1), DIPlusChangesDown(w1), DIPlusFalling(w1), DIPlusLower(w1), FastKAMABelowSlowKAMA(w1), FastReflexCrossDownSlowReflex(w1), FasterHMAIsBelowSlowerHMA(w1), GannHiLoDownTrend(w1), HMAChangesDown(w1), HMAFalling(w1), IchimokuKijunSenCrossBearish(w1), IchimokuKumoBreakoutBearish(w1), IchimokuSenkouSpanCrossBearish(w1), IchimokuTenkanKijunCrossBearish(w1), IsDowntrend(w1), KAMAFalling(w1), KCBarClosesBelowLower(w3), KCBarOpensBelowLower(w3), KCBarOpensBelowLowerAfterOpenAbove(w3), KCLowerFalling(w2), KCUpperRising(w2), KERaboveLevel(w1), LaguerreRSIChangesDown(w1), LaguerreRSICrossDown(w1), LaguerreRSIFalling(w1), LinRegBarClosesBelow(w1), LinRegBarOpensBelow(w1), LinRegBarOpensBelowAfterOpenAbove(w1), LinRegFalling(w1), MABarClosesBelow(w1), MABarOpensBelow(w1), MABarOpensBelowAfterOpenAbove(w1), MACDMainChangesDown(w1), MACDMainCrossBelowSignal(w1), MACDMainCrossBelowZero(w1), MACDMainFalling(w1), MACDMainLowerSignal(w1), MACDMainLowerZero(w1), MACDSignalFalling(w1), MAFalling(w1), MomChangesDown(w1), MomFalling(w1), OSMAChangesDown(w1), OSMACrossZeroDown(w1), OSMAFalling(w1), OSMALowerZero(w1), PSARBarHigher(w1), QQEValue1CrossBelow(w1), QQEValue1CrossBelowValue2(w1), QQEValue1Falling(w1), QQEValue1Lower(w1), QQEValue1LowerValue2(w1), QQEValue2Falling(w1), ROCBelowLevel(w1), ROCCrossesBelowLevel(w1), ROCFalling(w1), RSIChangesDown(w1), RSICrossDown(w1), RSIFalling(w1), RSILower(w1), ReflexChangesDirectionDown(w1), ReflexFalling(w1), SchaffTrendCycleBelowLevel(w1), SchaffTrendCycleCrossesBelowLevel(w1), StdDevChangesUp(w2), StdDevRising(w2), StochFastKDown(w1), StochSlowDChangesDown(w1), StochSlowDCrossDown(w1), StochSlowDFalling(w1), StochSlowDLower(w1), SuperTrendDownTrend(w1), VolumeRising(w1), VortexChangesTrendDown(w1), VortexDowntrend(w1), WPRChangesDown(w1), WPRCrossDown(w1), WPRFalling(w1), WPRLower(w1), WoodiesCCIZeroLineBreakDown(w1), WoodiesTrendDown(w1) | Núcleo: extremos del rango asiático (HighestInRange 00:00-03:00 → 07:00-10:00 en horas enteras; el original usaba paso 30 sobre HHMM, que genera horas inválidas como 0060), niveles del día anterior y aperturas de sesión, con órdenes stop en ellos. Filtros amplios a peso 1. Versión SELL: bloques y niveles espejados. |
| Building blocks | `Bloques activos · indicators` | 29 activos | 52 activos: CrossesAbove(w1), CrossesBelow(w1), Indicators.ADX(w1), Indicators.ATR(w1), Indicators.Aroon(w1), Indicators.BollingerBands(w1), Indicators.CCI(w1), Indicators.DeMarker(w1), Indicators.EMA(w1), Indicators.GannHiLo(w1), Indicators.Highest(w2), Indicators.HighestInRange(w2), Indicators.HullMovingAverage(w1), Indicators.Ichimoku(w1), Indicators.KAMA(w1), Indicators.KaufmanEfficiencyRatio(w1), Indicators.KeltnerChannel(w1), Indicators.LWMA(w1), Indicators.LaguerreRSI(w1), Indicators.LinearRegression(w1), Indicators.Lowest(w2), Indicators.LowestInRange(w4), Indicators.ParabolicSAR(w1), Indicators.RSI(w1), Indicators.SMA(w1), Indicators.SMMA(w1), Indicators.Stochastic(w1), Indicators.SuperTrend(w1), Indicators.TEMA(w1), Indicators.TrueRange(w1), Indicators.Vortex(w1), Indicators.WilliamsPR(w1), IsFalling(w1), IsGreater(w1), IsGreaterCount(w1), IsGreaterOrEqual(w1), IsLower(w1), IsLowerCount(w1), IsLowerOrEqual(w1), IsRising(w1), Prices.Close(w1), Prices.CloseD(w2), Prices.High(w1), Prices.HighD(w2), Prices.Low(w1), Prices.LowD(w2), Prices.Open(w1), Prices.OpenD(w2), Prices.SessionClose(w4), Prices.SessionHigh(w2), Prices.SessionLow(w4), Prices.SessionOpen(w4) | Núcleo: extremos del rango asiático (HighestInRange 00:00-03:00 → 07:00-10:00 en horas enteras; el original usaba paso 30 sobre HHMM, que genera horas inválidas como 0060), niveles del día anterior y aperturas de sesión, con órdenes stop en ellos. Filtros amplios a peso 1. Versión SELL: bloques y niveles espejados. |
| Building blocks | `Bloques activos · stopLimitBlocks` | 29 activos | 40 activos: Stop/Limit Price Levels.BollingerBands(w1), Stop/Limit Price Levels.Close(w2), Stop/Limit Price Levels.CloseD(w3), Stop/Limit Price Levels.EMA(w1), Stop/Limit Price Levels.Fractal(w1), Stop/Limit Price Levels.GannHiLo(w1), Stop/Limit Price Levels.High(w1), Stop/Limit Price Levels.HighD(w1), Stop/Limit Price Levels.Highest(w1), Stop/Limit Price Levels.HighestInRange(w1), Stop/Limit Price Levels.HullMovingAverage(w1), Stop/Limit Price Levels.Ichimoku(w1), Stop/Limit Price Levels.KAMA(w1), Stop/Limit Price Levels.KeltnerChannel(w1), Stop/Limit Price Levels.LWMA(w1), Stop/Limit Price Levels.LinearRegression(w1), Stop/Limit Price Levels.Low(w2), Stop/Limit Price Levels.LowD(w3), Stop/Limit Price Levels.Lowest(w2), Stop/Limit Price Levels.LowestInRange(w5), Stop/Limit Price Levels.MTKeltnerChannel(w1), Stop/Limit Price Levels.Open(w2), Stop/Limit Price Levels.OpenD(w3), Stop/Limit Price Levels.ParabolicSAR(w1), Stop/Limit Price Levels.Pivots(w1), Stop/Limit Price Levels.SMA(w1), Stop/Limit Price Levels.SMMA(w1), Stop/Limit Price Levels.SessionHigh(w1), Stop/Limit Price Levels.SessionLow(w5), Stop/Limit Price Levels.SessionOpen(w5), Stop/Limit Price Levels.SuperTrend(w1), Stop/Limit Price Levels.TEMA(w1), Stop/Limit Price Ranges.ATR(w2), Stop/Limit Price Ranges.BBRange(w2), Stop/Limit Price Ranges.BBWidthRatio(w2), Stop/Limit Price Ranges.BarRange(w2), Stop/Limit Price Ranges.BiggestRange(w2), Stop/Limit Price Ranges.MTATR(w2), Stop/Limit Price Ranges.SmallestRange(w2), Stop/Limit Price Ranges.TrueRange(w2) | Núcleo: extremos del rango asiático (HighestInRange 00:00-03:00 → 07:00-10:00 en horas enteras; el original usaba paso 30 sobre HHMM, que genera horas inválidas como 0060), niveles del día anterior y aperturas de sesión, con órdenes stop en ellos. Filtros amplios a peso 1. Versión SELL: bloques y niveles espejados. |
| Building blocks | `RSILower · Level` | 0..100/5 | 30..50/5 | Rango acotado al estilo (ver ficha) y espejado para SELL. |
| Building blocks | `RSICrossDown · Level` | 0..100/5 | 30..50/5 | Rango acotado al estilo (ver ficha) y espejado para SELL. |
| Building blocks | `LaguerreRSICrossDown · Gamma` | 0..0.95/0.01 | 0.3..0.8/0.05 | Rango acotado al estilo (ver ficha) y espejado para SELL. |
| Building blocks | `LaguerreRSICrossDown · Level` | 0.05..0.95/0.05 | 0.15..0.6/0.05 | Rango acotado al estilo (ver ficha) y espejado para SELL. |
| Building blocks | `StochSlowDLower · Level` | 0..100/5 | 20..50/5 | Rango acotado al estilo (ver ficha) y espejado para SELL. |
| Building blocks | `StochSlowDCrossDown · Level` | 0..100/5 | 20..50/5 | Rango acotado al estilo (ver ficha) y espejado para SELL. |
| Building blocks | `CCILower · Level` | -120..120/5 | -150..0/10 | Rango acotado al estilo (ver ficha) y espejado para SELL. |
| Building blocks | `CCICrossDown · Level` | -120..120/5 | -150..0/10 | Rango acotado al estilo (ver ficha) y espejado para SELL. |
| Building blocks | `WPRLower · Level` | -100..0/5 | -80..-50/5 | Rango acotado al estilo (ver ficha) y espejado para SELL. |
| Building blocks | `WPRCrossDown · Level` | -100..0/5 | -80..-50/5 | Rango acotado al estilo (ver ficha) y espejado para SELL. |
| Building blocks | `QQEValue1Lower · Level` | 20..90/5 | 30..50/5 | Rango acotado al estilo (ver ficha) y espejado para SELL. |
| Building blocks | `QQEValue1CrossBelow · Level` | 20..90/5 | 30..50/5 | Rango acotado al estilo (ver ficha) y espejado para SELL. |
| Building blocks | `SchaffTrendCycleBelowLevel · Level` | 0.1..90/0.1 | 10..50/5 | Rango acotado al estilo (ver ficha) y espejado para SELL. |
| Building blocks | `SchaffTrendCycleCrossesBelowLevel · Level` | 0.1..99.9/0.1 | 25..75/5 | Rango acotado al estilo (ver ficha) y espejado para SELL. |
| Building blocks | `ADXHigher · Level` | 20..90/10 | 20..40/5 | Rango acotado al estilo (ver ficha) y espejado para SELL. |
| Building blocks | `ADXCrossUp · Level` | 20..90/10 | 20..35/5 | Rango acotado al estilo (ver ficha) y espejado para SELL. |
| Building blocks | `KERaboveLevel · Level` | 0..0.95/0.05 | 0.3..0.7/0.05 | Rango acotado al estilo (ver ficha) y espejado para SELL. |
| Building blocks | `SuperTrendDownTrend · ATR Mult` | 0.5..10/0.1 | 1.5..5/0.5 | Rango acotado al estilo (ver ficha) y espejado para SELL. |
| Building blocks | `BarClosesBelowSuperTrend · ATR Mult` | 0.5..10/0.1 | 1.5..5/0.5 | Rango acotado al estilo (ver ficha) y espejado para SELL. |
| Building blocks | `Indicators.SuperTrend · ATR Mult` | 0.5..10/0.1 | 1.5..5/0.5 | Rango acotado al estilo (ver ficha) y espejado para SELL. |
| Building blocks | `Stop/Limit Price Levels.SuperTrend · ATR Mult` | 0.5..10/0.1 | 1.5..5/0.5 | Rango acotado al estilo (ver ficha) y espejado para SELL. |
| Building blocks | `ROCBelowLevel · Level` | -100..100/0.001 | -1..0/0.05 | Rango acotado al estilo (ver ficha) y espejado para SELL. |
| Building blocks | `ROCCrossesBelowLevel · Level` | -100..100/0.001 | -1..0/0.05 | Rango acotado al estilo (ver ficha) y espejado para SELL. |
| Building blocks | `Indicators.LowestInRange · Time From` | 0..2359/30 | 0..300/100 | Rango acotado al estilo (ver ficha) y espejado para SELL. |
| Building blocks | `Indicators.LowestInRange · Time To` | 0..2359/30 | 700..1000/100 | Rango acotado al estilo (ver ficha) y espejado para SELL. |
| Building blocks | `Indicators.HighestInRange · Time From` | 0..2359/30 | 0..300/100 | Rango acotado al estilo (ver ficha) y espejado para SELL. |
| Building blocks | `Indicators.HighestInRange · Time To` | 0..2359/30 | 700..1000/100 | Rango acotado al estilo (ver ficha) y espejado para SELL. |
| Building blocks | `Stop/Limit Price Levels.LowestInRange · Time From` | 0..2359/30 | 0..300/100 | Rango acotado al estilo (ver ficha) y espejado para SELL. |
| Building blocks | `Stop/Limit Price Levels.LowestInRange · Time To` | 0..2359/30 | 700..1000/100 | Rango acotado al estilo (ver ficha) y espejado para SELL. |
| Building blocks | `Stop/Limit Price Levels.HighestInRange · Time From` | 0..2359/30 | 0..300/100 | Rango acotado al estilo (ver ficha) y espejado para SELL. |
| Building blocks | `Stop/Limit Price Levels.HighestInRange · Time To` | 0..2359/30 | 700..1000/100 | Rango acotado al estilo (ver ficha) y espejado para SELL. |
| Building blocks | `Prices.SessionLow · Start Hours` | 0..23/1 | 1..3/1 | Rango acotado al estilo (ver ficha) y espejado para SELL. |
| Building blocks | `Prices.SessionLow · Start Minutes` | 0..59/1 | 0..0/1 | Rango acotado al estilo (ver ficha) y espejado para SELL. |
| Building blocks | `Prices.SessionLow · End Hours` | 0..23/1 | 8..10/1 | Rango acotado al estilo (ver ficha) y espejado para SELL. |
| Building blocks | `Prices.SessionLow · End Minutes` | 0..59/1 | 0..0/1 | Rango acotado al estilo (ver ficha) y espejado para SELL. |
| Building blocks | `Prices.SessionHigh · Start Hours` | 0..23/1 | 1..3/1 | Rango acotado al estilo (ver ficha) y espejado para SELL. |
| Building blocks | `Prices.SessionHigh · Start Minutes` | 0..59/1 | 0..0/1 | Rango acotado al estilo (ver ficha) y espejado para SELL. |
| Building blocks | `Prices.SessionHigh · End Hours` | 0..23/1 | 8..10/1 | Rango acotado al estilo (ver ficha) y espejado para SELL. |
| Building blocks | `Prices.SessionHigh · End Minutes` | 0..59/1 | 0..0/1 | Rango acotado al estilo (ver ficha) y espejado para SELL. |
| Building blocks | `Stop/Limit Price Levels.SessionLow · Start Hours` | 0..23/1 | 1..3/1 | Rango acotado al estilo (ver ficha) y espejado para SELL. |
| Building blocks | `Stop/Limit Price Levels.SessionLow · Start Minutes` | 0..59/1 | 0..0/1 | Rango acotado al estilo (ver ficha) y espejado para SELL. |
| Building blocks | `Stop/Limit Price Levels.SessionLow · End Hours` | 0..23/1 | 8..10/1 | Rango acotado al estilo (ver ficha) y espejado para SELL. |
| Building blocks | `Stop/Limit Price Levels.SessionLow · End Minutes` | 0..59/1 | 0..0/1 | Rango acotado al estilo (ver ficha) y espejado para SELL. |
| Building blocks | `Stop/Limit Price Levels.SessionHigh · Start Hours` | 0..23/1 | 1..3/1 | Rango acotado al estilo (ver ficha) y espejado para SELL. |
| Building blocks | `Stop/Limit Price Levels.SessionHigh · Start Minutes` | 0..59/1 | 0..0/1 | Rango acotado al estilo (ver ficha) y espejado para SELL. |
| Building blocks | `Stop/Limit Price Levels.SessionHigh · End Hours` | 0..23/1 | 8..10/1 | Rango acotado al estilo (ver ficha) y espejado para SELL. |
| Building blocks | `Stop/Limit Price Levels.SessionHigh · End Minutes` | 0..59/1 | 0..0/1 | Rango acotado al estilo (ver ficha) y espejado para SELL. |
| Building blocks | `Prices.SessionOpen · Start Hours` | 0..23/1 | 8..10/1 | Rango acotado al estilo (ver ficha) y espejado para SELL. |
| Building blocks | `Prices.SessionOpen · Start Minutes` | 0..59/1 | 0..0/1 | Rango acotado al estilo (ver ficha) y espejado para SELL. |
| Building blocks | `Stop/Limit Price Levels.SessionOpen · Start Hours` | 0..23/1 | 8..10/1 | Rango acotado al estilo (ver ficha) y espejado para SELL. |
| Building blocks | `Stop/Limit Price Levels.SessionOpen · Start Minutes` | 0..59/1 | 0..0/1 | Rango acotado al estilo (ver ficha) y espejado para SELL. |
| Building blocks | `Prices.SessionClose · End Hours` | 0..23/1 | 8..10/1 | Rango acotado al estilo (ver ficha) y espejado para SELL. |
| Building blocks | `Prices.SessionClose · End Minutes` | 0..59/1 | 0..0/1 | Rango acotado al estilo (ver ficha) y espejado para SELL. |
| Building blocks | `BarHourIs · Hour` | 0..23/1 | 9..18/1 | Rango acotado al estilo (ver ficha) y espejado para SELL. |
| Building blocks | `BarHourIsBigger · Hour` | 0..23/1 | 8..12/1 | Rango acotado al estilo (ver ficha) y espejado para SELL. |
| Building blocks | `BarHourIsSmaller · Hour` | 0..23/1 | 12..19/1 | Rango acotado al estilo (ver ficha) y espejado para SELL. |
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
| Notes | `Notes` | <b>Breakout strategies setup</b><div><br></div><div><br></div><div><br></div><div><br></div> | <b>Day Trading (ruptura del rango asiático) – Builder de test de ventaja (entrada) – SELL</b><div>Derivado de Ventaja_Build_ConfigInicial_H1_BUY (build 140.2099). Timeframe M15. Ver docs/03 (ficha DayTrading) y docs/04 (checklist).</div><div>NO VALIDADO EN SQX: revisar símbolo, costes, horario del servidor e importación.</div> | Descripción del estilo y advertencias. |
