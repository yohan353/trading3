# Estrategia_Build_ConfigInicial_H1_BUY__Scalping_M5_SELL

*Original:* `Estrategia_Build_ConfigInicial_H1_BUY.cfx` · *Estilo:* Scalping (micro-ruptura en sesión líquida) · *Timeframe:* M5 · *Rol:* Builder de estrategia completa · *Dirección:* SELL

Tabla generada automáticamente a partir de los cambios aplicados al XML (cada fila es un valor que difiere del original). Estado: **no validado en SQX** (ver docs/04).

| Sección | Parámetro | Valor original | Valor nuevo | Justificación |
|---|---|---|---|---|
| Task | `Task@templateFile` | C:\Users\<usuario>\Desktop\Estrategia_Build_ConfigInicial_H1_BUY.cfx | Estrategia_Build_ConfigInicial_H1_BUY__Scalping_M5_SELL.cfx | Ruta local del autor (C:\Users\<usuario>\Desktop\...) sustituida por el nombre del nuevo archivo: no aporta nada y expone el nombre de usuario de Windows. |
| Trading options | `Param key="SignalTimeRangeFrom"` | 5400 | 32400 | 09:00 servidor ≈ apertura de Londres (UTC+2). |
| Trading options | `Param key="SignalTimeRangeTo"` | 84600 | 66600 | 18:30 servidor ≈ final del solape Londres-NY. |
| Trading options | `Param key="ExitAtEndOfRange"` | false | true | Un scalper no arrastra posiciones fuera de su ventana. |
| Trading options | `Param key="ExitAtEndOfDay"` | false | true | Red de seguridad: nada abierto al cierre del día. |
| Trading options | `Param key="EODExitTime"` | 83040 | 75600 | Antes del rollover (spreads anchos). |
| Trading options | `Param key="ExitOnFriday"` | false | true | Sin riesgo de gap de fin de semana. |
| Trading options | `Param key="FridayExitTime"` | 74400 | 72000 | Viernes tarde: liquidez decreciente. |
| Trading options | `Param key="MaxTradesPerDay"` | 0 | 6 | Permite varias operaciones/día sin sobre-operar en días de ruido. |
| Trading options | `Param key="MaxDistanceFromMarket"` | false | true | Evita órdenes stop lejos del precio. |
| Trading options | `Param key="MaxDistancePct"` | 6 | 0.3 | 0,3 % ≈ 45 pips en GBPJPY; tope razonable para M5. |
| Trading options | `Param key="ReservedBars"` | 50 | 120 | ≥ periodo máximo (100) para que los indicadores estén calculados. |
| What to build | `MarketSides@type` | long | short | Kit SELL: sólo ventas. Sin simetría, SQX usa los bloques tal cual, por eso se activan los equivalentes bajistas (espejo) en Building blocks. |
| What to build | `StrategyType@type` | template | simple | El original dependía de una plantilla .sqx externa (Template_DOW_H1_BUY_1.8.4.sqx) que no viene en el .cfx; en modo 'simple' el archivo funciona por sí solo y la selección de bloques del estilo pasa a determinar la entrada. Para volver al flujo plantilla, ver docs/04 §A.3. |
| What to build | `StrategyType@templateFile` | C:\Users\<usuario>\Documents\StrategyQuant\00 - Temp\Formación\DOWJONES_H1_BUY\Template\Template_DOW_H1_BUY_1.8.4.sqx | SQ3StrategyTemplateExample.sq4 | Valor por defecto (el mismo que Ventaja_Build); en modo 'simple' no se usa. |
| What to build · complejidad | `Chart@minConditions` | 0 | 1 | Entrada generada por el Builder. |
| What to build · complejidad | `Chart@maxConditions` | 0 | 3 | Periodos 5-100 velas de M5 (25 min a 8 h): horizonte de micro-estructura; ≥100 no aporta nada a un scalper y sobreajusta. |
| What to build · complejidad | `Chart@maxExitConditions` | 3 | 2 | Máximo 1-2: una salida por regla sencilla es más robusta. |
| What to build · complejidad | `Chart@minExitTypes` | 1 | 2 | Al menos SL + otra salida. |
| What to build · complejidad | `Chart@maxExitTypes` | 5 | 4 | El original pedía hasta 5 con sólo 3 tipos activos. |
| What to build · complejidad | `Chart@minPeriod` | 4 | 5 | Periodos 5-100 velas de M5 (25 min a 8 h): horizonte de micro-estructura; ≥100 no aporta nada a un scalper y sobreajusta. |
| What to build · complejidad | `Chart@maxPeriod` | 200 | 100 | Periodos 5-100 velas de M5 (25 min a 8 h): horizonte de micro-estructura; ≥100 no aporta nada a un scalper y sobreajusta. |
| What to build · SL/PT | `MaxSLATRMultiple` | 3 | 2.5 | Rango de SL del estilo: 1.0-2.5 ATR. |
| What to build · SL/PT | `MinSLATRPeriod` | 20 | 14 | ATR(14-50) en velas M5. |
| What to build · SL/PT | `MaxSLATRPeriod` | 100 | 50 | ATR(14-50) en velas M5. |
| What to build · SL/PT | `MinPTATRMultiple` | 2 | 1 | Rango de PT: 1.0-3.0 ATR. |
| What to build · SL/PT | `MaxPTATRMultiple` | 5 | 3 | Rango de PT: 1.0-3.0 ATR. |
| What to build · SL/PT | `MinPTATRPeriod` | 20 | 14 | ATR(14-50). |
| What to build · SL/PT | `MaxPTATRPeriod` | 100 | 50 | ATR(14-50). |
| What to build · SL/PT | `LimitSLPTRRRFrom` | 100 | 80 | PT = 80-250 % del SL. |
| What to build · SL/PT | `LimitSLPTRRRTo` | 500 | 250 | PT = 80-250 % del SL. |
| Genetic options | `PopulationSize` | 5 | 20 | 20 por isla × 4 islas = 80 por generación: más diversidad que el original (5-15) sin que la población inicial tarde horas en completarse. |
| Genetic options | `MaxGenerations` | 10 | 30 | Con 10 generaciones la evolución apenas actúa (y el reinicio por estancamiento a 30 nunca saltaba). |
| Genetic options | `Islands` | 5 | 4 | 4 islas: diversidad suficiente con menos coste. |
| Genetic options | `CrossoverProbability` | 46 | 80 | 46 % es bajo para un AG; 70-90 % es lo habitual (supuesto de práctica general, no de SQX). |
| Genetic options | `MutationProbability` | 35 | 30 | Algo menor para no destruir buenas soluciones. |
| Genetic options | `MigrationModulo` | 5 | 10 | Migrar cada 10 generaciones (con 30-40 generaciones). |
| Genetic options | `MigrationRate` | 6 | 10 | 6 % de 5 individuos = 0,3: la migración original era nula en la práctica. |
| Genetic options | `EvoRestartOnStagnation@generations` | 30 | 15 | Debe ser menor que MaxGenerations para poder actuar. |
| Genetic options | `BuildMode/Conditions (población inicial)` | ReturnDDRatio(IS) >= 5; AvgBarsInTrade(IS) >= 2; NumberOfTrades(IS) >= 250; WinningPct(IS) >= 35 | NumberOfTrades(IS) >= 320 | SÓLO nº mínimo de operaciones (30 % del mínimo final), como recomienda SQX. La población inicial no se guarda en el banco y SQX genera aleatorias hasta completarla: con 80-100 individuos y filtros de rentabilidad (Ret/DD, acierto) el Builder puede pasar horas o días sin producir nada. La exigencia de calidad está en los filtros del Ranking. |
| Ranking | `Rankings/Conditions (filtros)` | AvgBarsInTrade(IS) >= 2; ReturnDDRatio(IS) >= 8; NumberOfTrades(IS) >= 300; WinningPct(IS) >= 40 | NumberOfTrades(IS) >= 1050; ReturnDDRatio(IS) >= 6; WinningPct(IS) >= 45; ProfitFactor(IS) >= 1.25; AvgBarsInTrade(IS) >= 3; NetProfit(OOS) > 0; NumberOfTrades(OOS) >= 360 | Mínimo de operaciones = 300/año × años de cada tramo (el original exigía 300 en 7,25 años ≈ 41/año; ningún estilo baja de esa densidad salvo Position) + umbrales del estilo + exigencia en el tramo de validación OOS, que el original no tenía. |
| Ranking | `FitnessCriteria/Settings/Ranking` | type="ReturnDDRatio" | Weighted: ReturnDDRatio (peso 1, max), SQN (peso 2, max) | SQN premia expectativa consistente con muchas operaciones (lo propio de un scalper); Ret/DD evita curvas con drawdowns profundos. |
| Money management | `FixedAmount · RiskedMoney` | 100 | 50 | Riesgo fijo de 50 sobre 10.000 (0.5 %). Estilos de alta frecuencia: 0,5 % para contener el drawdown en R. |
| Data | `Setup/Chart@timeframe` | H1 | M5 | Timeframe del estilo Scalping. |
| Data | `Setup@slippage` | 0 | 0.5 | El original usa 0; en M5 un deslizamiento de 0,5 pips por orden stop/mercado es conservador-realista y cambia el signo de muchas estrategias. |
| Data | `Setup@dateFrom` | 2013.09.30 | 2016.01.04 | M5/M15: 5 años bastan en operaciones y reducen el cómputo. |
| Data | `OutOfSample/Range` | (sin OOS) | 2019.07.01–2020.12.31 | Nuevo tramo de validación dentro del Builder (el original no tenía OOS y filtraba sólo sobre IS). |
| Cross checks | `RetestOnAdditionalMarkets/Setup@timeframe` | H1 | M5 | Coherencia si se activa (sigue desactivado). |
| Building blocks | `Calibration@calibrateBeforeStart` | false | true | Recalibra antes de empezar los rangos de valores de los indicadores (p. ej. ATR y rangos de órdenes stop/limit, que traen ±5000 por defecto) con el símbolo y timeframe de Data. Sin ello, al cambiar de H1 a M5/M15/H4/D1 las comparaciones con números y los desplazamientos de órdenes stop/limit no tienen sentido. |
| Building blocks | `Bloques activos · signals` | 146 activos | 91 activos: ADXChangesUp(w1), ADXCrossUp(w1), ADXHigher(w1), ADXRising(w1), ATRChangesUp(w2), ATRRising(w2), AWOChangesDown(w1), AWOFalling(w1), AvgVolumeRising(w1), BBBarClosesBelowDown(w4), BBBarOpensBelowDown(w4), BBBarOpensBelowDownAfterOpenAbove(w4), BBLowerFalling(w2), BBUpperRising(w2), BarClosesBelowKAMA(w1), BarDayOfWeekIsNot(w1), BarHourIsBigger(w1), BarHourIsSmaller(w1), BarOpensBelowLowestAfterOpenAbove(w10), CCIChangesDown(w1), CCICrossDown(w1), CCIFalling(w1), CCILower(w1), DEMChangesDown(w1), DEMFalling(w1), FastKAMABelowSlowKAMA(w1), FastReflexCrossDownSlowReflex(w1), FasterHMAIsBelowSlowerHMA(w1), HMAChangesDown(w1), HMAFalling(w1), IsDowntrend(w1), KAMAFalling(w1), KCBarClosesBelowLower(w4), KCBarOpensBelowLower(w4), KCBarOpensBelowLowerAfterOpenAbove(w4), KCLowerFalling(w2), KCUpperRising(w2), KERaboveLevel(w1), LaguerreRSIChangesDown(w1), LaguerreRSICrossDown(w1), LaguerreRSIFalling(w1), LinRegBarClosesBelow(w1), LinRegBarOpensBelow(w1), LinRegBarOpensBelowAfterOpenAbove(w1), LinRegFalling(w1), MABarClosesBelow(w1), MABarOpensBelow(w1), MABarOpensBelowAfterOpenAbove(w1), MACDMainChangesDown(w1), MACDMainCrossBelowSignal(w1), MACDMainCrossBelowZero(w1), MACDMainFalling(w1), MACDMainLowerSignal(w1), MACDMainLowerZero(w1), MACDSignalFalling(w1), MAFalling(w1), MomChangesDown(w1), MomFalling(w1), OSMAChangesDown(w1), OSMACrossZeroDown(w1), OSMAFalling(w1), OSMALowerZero(w1), QQEValue1CrossBelow(w1), QQEValue1CrossBelowValue2(w1), QQEValue1Falling(w1), QQEValue1Lower(w1), QQEValue1LowerValue2(w1), QQEValue2Falling(w1), ROCBelowLevel(w1), ROCCrossesBelowLevel(w1), ROCFalling(w1), RSIChangesDown(w1), RSICrossDown(w1), RSIFalling(w1), RSILower(w1), ReflexChangesDirectionDown(w1), ReflexFalling(w1), SchaffTrendCycleBelowLevel(w1), SchaffTrendCycleCrossesBelowLevel(w1), StdDevChangesUp(w2), StdDevRising(w2), StochFastKDown(w1), StochSlowDChangesDown(w1), StochSlowDCrossDown(w1), StochSlowDFalling(w1), StochSlowDLower(w1), VolumeRising(w1), WPRChangesDown(w1), WPRCrossDown(w1), WPRFalling(w1), WPRLower(w1) | Núcleo: ruptura de canal/bandas y de los extremos de la sesión asiática (pesos 4-10, y órdenes stop en esos niveles, que son las que materializan la ruptura). Filtros a peso 1: expansión de volatilidad, momentum, tendencia corta, fuerza y hora. Sin bloques de nivel absoluto. Versión SELL: bloques y niveles espejados. |
| Building blocks | `Bloques activos · indicators` | 29 activos | 48 activos: CrossesAbove(w1), CrossesBelow(w1), Indicators.ATR(w1), Indicators.BollingerBands(w1), Indicators.CCI(w1), Indicators.DeMarker(w1), Indicators.EMA(w1), Indicators.GannHiLo(w1), Indicators.Highest(w1), Indicators.HighestInRange(w1), Indicators.HullMovingAverage(w1), Indicators.Ichimoku(w1), Indicators.KAMA(w1), Indicators.KeltnerChannel(w1), Indicators.LWMA(w1), Indicators.LaguerreRSI(w1), Indicators.LinearRegression(w1), Indicators.Lowest(w3), Indicators.LowestInRange(w2), Indicators.ParabolicSAR(w1), Indicators.RSI(w1), Indicators.SMA(w1), Indicators.SMMA(w1), Indicators.Stochastic(w1), Indicators.SuperTrend(w1), Indicators.TEMA(w1), Indicators.TrueRange(w1), Indicators.WilliamsPR(w1), IsFalling(w1), IsGreater(w1), IsGreaterCount(w1), IsGreaterOrEqual(w1), IsLower(w1), IsLowerCount(w1), IsLowerOrEqual(w1), IsRising(w1), Prices.Close(w1), Prices.CloseD(w1), Prices.High(w1), Prices.HighD(w1), Prices.Low(w1), Prices.LowD(w1), Prices.Open(w1), Prices.OpenD(w1), Prices.SessionClose(w2), Prices.SessionHigh(w1), Prices.SessionLow(w2), Prices.SessionOpen(w2) | Núcleo: ruptura de canal/bandas y de los extremos de la sesión asiática (pesos 4-10, y órdenes stop en esos niveles, que son las que materializan la ruptura). Filtros a peso 1: expansión de volatilidad, momentum, tendencia corta, fuerza y hora. Sin bloques de nivel absoluto. Versión SELL: bloques y niveles espejados. |
| Building blocks | `Bloques activos · stopLimitBlocks` | 29 activos | 40 activos: Stop/Limit Price Levels.BollingerBands(w2), Stop/Limit Price Levels.Close(w3), Stop/Limit Price Levels.CloseD(w1), Stop/Limit Price Levels.EMA(w1), Stop/Limit Price Levels.Fractal(w1), Stop/Limit Price Levels.GannHiLo(w1), Stop/Limit Price Levels.High(w1), Stop/Limit Price Levels.HighD(w1), Stop/Limit Price Levels.Highest(w1), Stop/Limit Price Levels.HighestInRange(w1), Stop/Limit Price Levels.HullMovingAverage(w1), Stop/Limit Price Levels.Ichimoku(w1), Stop/Limit Price Levels.KAMA(w1), Stop/Limit Price Levels.KeltnerChannel(w2), Stop/Limit Price Levels.LWMA(w1), Stop/Limit Price Levels.LinearRegression(w1), Stop/Limit Price Levels.Low(w3), Stop/Limit Price Levels.LowD(w1), Stop/Limit Price Levels.Lowest(w5), Stop/Limit Price Levels.LowestInRange(w3), Stop/Limit Price Levels.MTKeltnerChannel(w2), Stop/Limit Price Levels.Open(w3), Stop/Limit Price Levels.OpenD(w1), Stop/Limit Price Levels.ParabolicSAR(w1), Stop/Limit Price Levels.Pivots(w1), Stop/Limit Price Levels.SMA(w1), Stop/Limit Price Levels.SMMA(w1), Stop/Limit Price Levels.SessionHigh(w1), Stop/Limit Price Levels.SessionLow(w3), Stop/Limit Price Levels.SessionOpen(w3), Stop/Limit Price Levels.SuperTrend(w1), Stop/Limit Price Levels.TEMA(w1), Stop/Limit Price Ranges.ATR(w2), Stop/Limit Price Ranges.BBRange(w2), Stop/Limit Price Ranges.BBWidthRatio(w2), Stop/Limit Price Ranges.BarRange(w2), Stop/Limit Price Ranges.BiggestRange(w2), Stop/Limit Price Ranges.MTATR(w2), Stop/Limit Price Ranges.SmallestRange(w2), Stop/Limit Price Ranges.TrueRange(w2) | Núcleo: ruptura de canal/bandas y de los extremos de la sesión asiática (pesos 4-10, y órdenes stop en esos niveles, que son las que materializan la ruptura). Filtros a peso 1: expansión de volatilidad, momentum, tendencia corta, fuerza y hora. Sin bloques de nivel absoluto. Versión SELL: bloques y niveles espejados. |
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
| Building blocks | `Prices.SessionOpen · Start Hours` | 0..23/1 | 1..3/1 | Rango acotado al estilo (ver ficha) y espejado para SELL. |
| Building blocks | `Prices.SessionOpen · Start Minutes` | 0..59/1 | 0..0/1 | Rango acotado al estilo (ver ficha) y espejado para SELL. |
| Building blocks | `Stop/Limit Price Levels.SessionOpen · Start Hours` | 0..23/1 | 1..3/1 | Rango acotado al estilo (ver ficha) y espejado para SELL. |
| Building blocks | `Stop/Limit Price Levels.SessionOpen · Start Minutes` | 0..59/1 | 0..0/1 | Rango acotado al estilo (ver ficha) y espejado para SELL. |
| Building blocks | `Prices.SessionClose · End Hours` | 0..23/1 | 8..10/1 | Rango acotado al estilo (ver ficha) y espejado para SELL. |
| Building blocks | `Prices.SessionClose · End Minutes` | 0..59/1 | 0..0/1 | Rango acotado al estilo (ver ficha) y espejado para SELL. |
| Building blocks | `BarHourIsBigger · Hour` | 0..23/1 | 8..12/1 | Rango acotado al estilo (ver ficha) y espejado para SELL. |
| Building blocks | `BarHourIsSmaller · Hour` | 0..23/1 | 12..19/1 | Rango acotado al estilo (ver ficha) y espejado para SELL. |
| Order types | `EnterAtStop@use` | false | true | Orden stop en el nivel de ruptura: entra sólo si la ruptura ocurre; validez 1-3 velas (5-15 min) para no comprar rupturas viejas. |
| Order types | `EnterAtStop@weight` | 1 | 3 | Peso relativo entre tipos de orden. |
| Order types | `EnterAtStop · BarsValid min` | 2 | 1 | Orden stop en el nivel de ruptura: entra sólo si la ruptura ocurre; validez 1-3 velas (5-15 min) para no comprar rupturas viejas. |
| Order types | `EnterAtStop · BarsValid max` | 10 | 3 | Orden stop en el nivel de ruptura: entra sólo si la ruptura ocurre; validez 1-3 velas (5-15 min) para no comprar rupturas viejas. |
| Order types | `EnterAtStop · ExitAfterBars min` | 5 | 6 | Alineado con el rango de ExitTypes para eliminar la ambigüedad del original (5-20 vs 2-15). |
| Order types | `EnterAtStop · ExitAfterBars max` | 20 | 36 | Alineado con el rango de ExitTypes. |
| Order types | `EnterAtMarket · ExitAfterBars min` | 5 | 6 | Alineado con el rango de ExitTypes para eliminar la ambigüedad del original (5-20 vs 2-15). |
| Order types | `EnterAtMarket · ExitAfterBars max` | 20 | 36 | Alineado con el rango de ExitTypes. |
| Exit types | `StopLoss · PctValue` | true | false | Coherencia con SLPTOptions (SLPercent/PTPercent = false). |
| Exit types | `ProfitTarget · PctValue` | true | false | Coherencia con SLPTOptions (SLPercent/PTPercent = false). |
| Exit types | `TrailingStop@use` | true | false | El estilo no usa trailing. |
| Exit types | `MoveSL2BE@use` | false | true | SL/PT en ATR de M5 (adaptativos); break-even rápido; salida temporal 30 min-3 h: la ventaja de un scalp se agota en pocas velas. |
| Exit types | `MoveSL2BE · FixedValue` | true | false | Valores fijos en pips no son trasladables entre timeframes/símbolos. |
| Exit types | `MoveSL2BE · ATR mult. min` | 1 | 0.5 | SL/PT en ATR de M5 (adaptativos); break-even rápido; salida temporal 30 min-3 h: la ventaja de un scalp se agota en pocas velas. |
| Exit types | `MoveSL2BE · ATR mult. max` | 5 | 1.5 | SL/PT en ATR de M5 (adaptativos); break-even rápido; salida temporal 30 min-3 h: la ventaja de un scalp se agota en pocas velas. |
| Exit types | `ExitAfterBars@use` | false | true | SL/PT en ATR de M5 (adaptativos); break-even rápido; salida temporal 30 min-3 h: la ventaja de un scalp se agota en pocas velas. |
| Exit types | `ExitAfterBars min` | 2 | 6 | SL/PT en ATR de M5 (adaptativos); break-even rápido; salida temporal 30 min-3 h: la ventaja de un scalp se agota en pocas velas. |
| Exit types | `ExitAfterBars max` | 15 | 36 | SL/PT en ATR de M5 (adaptativos); break-even rápido; salida temporal 30 min-3 h: la ventaja de un scalp se agota en pocas velas. |
| Exit types | `_ExitRule_@use` | false | true | Salida por condición (cierre bajo media, oscilador en zona neutra...) coherente con el estilo. |
| Exit types | `_ExitRule_@probability` | 50 | 30 | SL/PT en ATR de M5 (adaptativos); break-even rápido; salida temporal 30 min-3 h: la ventaja de un scalp se agota en pocas velas. |
| Notes | `Notes` | <b>Breakout strategies setup</b><div><br></div><div><br></div><div><br></div><div><br></div> | <b>Scalping (micro-ruptura en sesión líquida) – Builder de estrategia completa – SELL</b><div>Derivado de Estrategia_Build_ConfigInicial_H1_BUY (build 140.2099). Timeframe M5. Ver docs/03 (ficha Scalping) y docs/04 (checklist).</div><div>NO VALIDADO EN SQX: revisar símbolo, costes, horario del servidor e importación.</div> | Descripción del estilo y advertencias. |
