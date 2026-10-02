# Estrategia_Build_ConfigInicial_H1_BUY__Swing_H4_BUY

*Original:* `Estrategia_Build_ConfigInicial_H1_BUY.cfx` · *Estilo:* Swing Trading (ruptura de consolidación multi-día) · *Timeframe:* H4 · *Rol:* Builder de estrategia completa · *Dirección:* BUY

Tabla generada automáticamente a partir de los cambios aplicados al XML (cada fila es un valor que difiere del original). Estado: **no validado en SQX** (ver docs/04).

| Sección | Parámetro | Valor original | Valor nuevo | Justificación |
|---|---|---|---|---|
| Task | `Task@templateFile` | C:\Users\<usuario>\Desktop\Estrategia_Build_ConfigInicial_H1_BUY.cfx | Estrategia_Build_ConfigInicial_H1_BUY__Swing_H4_BUY.cfx | Ruta local del autor (C:\Users\<usuario>\Desktop\...) sustituida por el nombre del nuevo archivo: no aporta nada y expone el nombre de usuario de Windows. |
| Trading options | `Param key="LimitTimeRange"` | true | false | En H4 la ventana 01:30-23:30 excluiría la vela de las 00:00 (1/6 de las señales) sin motivo de estilo. |
| Trading options | `Param key="MaxTradesPerDay"` | 0 | 2 | Swing: hasta dos entradas diarias. |
| Trading options | `Param key="MaxDistanceFromMarket"` | false | true | Evita stops lejanos. |
| Trading options | `Param key="MaxDistancePct"` | 6 | 2 | 2 %: holgura para rupturas de rangos de varios días. |
| Trading options | `Param key="ReservedBars"` | 50 | 150 | ≥ periodo máximo (120). |
| What to build | `StrategyType@type` | template | simple | El original dependía de una plantilla .sqx externa (Template_DOW_H1_BUY_1.8.4.sqx) que no viene en el .cfx; en modo 'simple' el archivo funciona por sí solo y la selección de bloques del estilo pasa a determinar la entrada. Para volver al flujo plantilla, ver docs/04 §A.3. |
| What to build | `StrategyType@templateFile` | C:\Users\<usuario>\Documents\StrategyQuant\00 - Temp\Formación\DOWJONES_H1_BUY\Template\Template_DOW_H1_BUY_1.8.4.sqx | SQ3StrategyTemplateExample.sq4 | Valor por defecto (el mismo que Ventaja_Build); en modo 'simple' no se usa. |
| What to build · complejidad | `Chart@minConditions` | 0 | 1 | Entrada generada por el Builder. |
| What to build · complejidad | `Chart@maxConditions` | 0 | 3 | 5-120 velas H4 = 1-20 días: horizonte de swing. |
| What to build · complejidad | `Chart@maxExitConditions` | 3 | 2 | Máximo 1-2: una salida por regla sencilla es más robusta. |
| What to build · complejidad | `Chart@minExitTypes` | 1 | 2 | Al menos SL + otra salida. |
| What to build · complejidad | `Chart@maxExitTypes` | 5 | 4 | El original pedía hasta 5 con sólo 3 tipos activos. |
| What to build · complejidad | `Chart@minPeriod` | 4 | 5 | 5-120 velas H4 = 1-20 días: horizonte de swing. |
| What to build · complejidad | `Chart@maxPeriod` | 200 | 120 | 5-120 velas H4 = 1-20 días: horizonte de swing. |
| What to build · SL/PT | `MinSLATRMultiple` | 1 | 1.5 | Rango de SL del estilo: 1.5-3.5 ATR. |
| What to build · SL/PT | `MaxSLATRMultiple` | 3 | 3.5 | Rango de SL del estilo: 1.5-3.5 ATR. |
| What to build · SL/PT | `MinSLATRPeriod` | 20 | 14 | ATR(14-100) en velas H4. |
| What to build · SL/PT | `PTRequired` | true | false | Objetivo opcional: el estilo sale por trailing/tiempo/fin de día. |
| What to build · SL/PT | `MaxPTATRMultiple` | 5 | 6 | Rango de PT: 2.0-6.0 ATR. |
| What to build · SL/PT | `MinPTATRPeriod` | 20 | 14 | ATR(14-100). |
| What to build · SL/PT | `LimitSLPTRRR` | true | false | Sin límite R:R: el PT es opcional y la salida principal es otra. |
| Genetic options | `PopulationSize` | 5 | 25 | 25 por isla × 4 islas = 100 por generación: más diversidad que el original (5-15) sin que la población inicial tarde horas en completarse. |
| Genetic options | `MaxGenerations` | 10 | 30 | Con 10 generaciones la evolución apenas actúa (y el reinicio por estancamiento a 30 nunca saltaba). |
| Genetic options | `Islands` | 5 | 4 | 4 islas: diversidad suficiente con menos coste. |
| Genetic options | `CrossoverProbability` | 46 | 80 | 46 % es bajo para un AG; 70-90 % es lo habitual (supuesto de práctica general, no de SQX). |
| Genetic options | `MutationProbability` | 35 | 30 | Algo menor para no destruir buenas soluciones. |
| Genetic options | `MigrationModulo` | 5 | 10 | Migrar cada 10 generaciones (con 30-40 generaciones). |
| Genetic options | `MigrationRate` | 6 | 10 | 6 % de 5 individuos = 0,3: la migración original era nula en la práctica. |
| Genetic options | `EvoRestartOnStagnation@generations` | 30 | 15 | Debe ser menor que MaxGenerations para poder actuar. |
| Genetic options | `BuildMode/Conditions (población inicial)` | ReturnDDRatio(IS) >= 5; AvgBarsInTrade(IS) >= 2; NumberOfTrades(IS) >= 250; WinningPct(IS) >= 35 | NumberOfTrades(IS) >= 70 | SÓLO nº mínimo de operaciones (30 % del mínimo final), como recomienda SQX. La población inicial no se guarda en el banco y SQX genera aleatorias hasta completarla: con 80-100 individuos y filtros de rentabilidad (Ret/DD, acierto) el Builder puede pasar horas o días sin producir nada. La exigencia de calidad está en los filtros del Ranking. |
| Ranking | `Rankings/Conditions (filtros)` | AvgBarsInTrade(IS) >= 2; ReturnDDRatio(IS) >= 8; NumberOfTrades(IS) >= 300; WinningPct(IS) >= 40 | NumberOfTrades(IS) >= 240; ReturnDDRatio(IS) >= 4; WinningPct(IS) >= 38; ProfitFactor(IS) >= 1.3; AvgBarsInTrade(IS) >= 3; NetProfit(OOS) > 0; NumberOfTrades(OOS) >= 70 | Mínimo de operaciones = 45/año × años de cada tramo (el original exigía 300 en 7,25 años ≈ 41/año; ningún estilo baja de esa densidad salvo Position) + umbrales del estilo + exigencia en el tramo de validación OOS, que el original no tenía. |
| Ranking | `FitnessCriteria/Settings/Ranking` | type="ReturnDDRatio" | Weighted: ReturnDDRatio (peso 2, max), Stability (peso 1, max) | Ret/DD + estabilidad de la curva. |
| Data | `Setup/Chart@timeframe` | H1 | H4 | Timeframe del estilo Swing. |
| Data | `Setup@slippage` | 0 | 0.3 | El original usa 0; 0,3 pips es conservador en H4. |
| Data | `OutOfSample/Range` | (sin OOS) | 2019.01.01–2020.12.31 | Nuevo tramo de validación dentro del Builder (el original no tenía OOS y filtraba sólo sobre IS). |
| Cross checks | `RetestOnAdditionalMarkets/Setup@timeframe` | H1 | H4 | Coherencia si se activa (sigue desactivado). |
| Building blocks | `Calibration@calibrateBeforeStart` | false | true | Recalibra antes de empezar los rangos de valores de los indicadores (p. ej. ATR y rangos de órdenes stop/limit, que traen ±5000 por defecto) con el símbolo y timeframe de Data. Sin ello, al cambiar de H1 a M5/M15/H4/D1 las comparaciones con números y los desplazamientos de órdenes stop/limit no tienen sentido. |
| Building blocks | `Bloques activos · signals` | 146 activos | 115 activos: ADXChangesUp(w2), ADXCrossUp(w2), ADXHigher(w2), ADXRising(w2), ATRChangesDown(w1), ATRChangesUp(w1), ATRFalling(w1), ATRRising(w1), AWOChangesUp(w1), AWORising(w1), AroonCrossesAbove(w1), BBBarClosesAboveUp(w3), BBBarOpensAboveUp(w3), BBBarOpensAboveUpAfterOpenBelow(w3), BBLowerFalling(w1), BBLowerRising(w1), BBUpperFalling(w1), BBUpperRising(w1), BarClosesAboveKAMA(w1), BarClosesAboveSuperTrend(w1), BarDayOfWeekIsNot(w1), BarMonthIsNot(w1), BarOpensAboveHighestAfterOpenBelow(w8), CCIChangesUp(w1), CCICrossUp(w1), CCIHigher(w1), CCIRising(w1), DEMChangesUp(w1), DEMRising(w1), DICrossUp(w1), DIMinusChangesDown(w1), DIMinusFalling(w1), DIPlusChangesUp(w1), DIPlusHigher(w1), DIPlusRising(w1), FastKAMAAboveSlowKAMA(w1), FastReflexCrossUPSlowReflex(w1), FasterHMAIsAboveSlowerHMA(w1), GannHiLoUPTrend(w1), HMAChangesUP(w1), HMARising(w1), IchimokuKijunSenCrossBullish(w2), IchimokuKumoBreakoutBullish(w2), IchimokuSenkouSpanCrossBullish(w2), IchimokuTenkanKijunCrossBullish(w2), IsUptrend(w1), KAMARising(w1), KCBarClosesAboveUpper(w3), KCBarOpensAboveUpper(w3), KCBarOpensAboveUpperAfterOpenBelow(w3), KCLowerFalling(w1), KCLowerRising(w1), KCUpperFalling(w1), KCUpperRising(w1), KERaboveLevel(w2), LaguerreRSIChangesUP(w1), LaguerreRSICrossUP(w1), LaguerreRSIRising(w1), LinRegBarClosesAbove(w1), LinRegBarOpensAbove(w1), LinRegBarOpensAboveAfterOpenBelow(w1), LinRegRising(w1), MABarClosesAbove(w1), MABarOpensAbove(w1), MABarOpensAboveAfterOpenBelow(w1), MACDMainChangesUp(w1), MACDMainCrossAboveSignal(w1), MACDMainCrossAboveZero(w1), MACDMainHigherSignal(w1), MACDMainHigherZero(w1), MACDMainRising(w1), MACDSignalRising(w1), MARising(w1), MomChangesUp(w1), MomRising(w1), OSMAChangesUp(w1), OSMACrossZeroUp(w1), OSMAHigherZero(w1), OSMARising(w1), PSARBarLower(w1), QQEValue1CrossAbove(w1), QQEValue1CrossAboveValue2(w1), QQEValue1Higher(w1), QQEValue1HigherValue2(w1), QQEValue1Rising(w1), QQEValue2Rising(w1), ROCAboveLevel(w1), ROCCrossesAboveLevel(w1), ROCRising(w1), RSIChangesUp(w1), RSICrossUp(w1), RSIHigher(w1), RSIRising(w1), ReflexChangesDirectionUP(w1), ReflexRising(w1), SchaffTrendCycleAboveLevel(w1), SchaffTrendCycleCrossesAboveLevel(w1), StdDevChangesDown(w1), StdDevChangesUp(w1), StdDevFalling(w1), StdDevRising(w1), StochFastKUp(w1), StochSlowDChangesUp(w1), StochSlowDCrossUp(w1), StochSlowDHigher(w1), StochSlowDRising(w1), SuperTrendUPTrend(w1), VortexChangesTrendUP(w1), VortexUptrend(w1), WPRChangesUp(w1), WPRCrossUp(w1), WPRHigher(w1), WPRRising(w1), WoodiesCCIZeroLineBreakUP(w1), WoodiesTrendUP(w1) | Núcleo: ruptura de máximos de N velas/día/semana, bandas y nube de Ichimoku, con órdenes stop; filtros de régimen (ADX, KER, medias, sistemas de tendencia), volatilidad y calendario. |
| Building blocks | `Bloques activos · indicators` | 29 activos | 51 activos: CrossesAbove(w1), CrossesBelow(w1), Indicators.ADX(w1), Indicators.ATR(w1), Indicators.Aroon(w1), Indicators.BollingerBands(w1), Indicators.CCI(w1), Indicators.DeMarker(w1), Indicators.EMA(w1), Indicators.Fractal(w1), Indicators.GannHiLo(w1), Indicators.Highest(w3), Indicators.HullMovingAverage(w1), Indicators.Ichimoku(w1), Indicators.KAMA(w1), Indicators.KaufmanEfficiencyRatio(w1), Indicators.KeltnerChannel(w1), Indicators.LWMA(w1), Indicators.LaguerreRSI(w1), Indicators.LinearRegression(w1), Indicators.Lowest(w1), Indicators.ParabolicSAR(w1), Indicators.RSI(w1), Indicators.SMA(w1), Indicators.SMMA(w1), Indicators.Stochastic(w1), Indicators.SuperTrend(w1), Indicators.TEMA(w1), Indicators.TrueRange(w1), Indicators.Vortex(w1), Indicators.WilliamsPR(w1), IsFalling(w1), IsGreater(w1), IsGreaterCount(w1), IsGreaterOrEqual(w1), IsLower(w1), IsLowerCount(w1), IsLowerOrEqual(w1), IsRising(w1), Prices.Close(w1), Prices.CloseD(w2), Prices.CloseW(w2), Prices.High(w1), Prices.HighD(w2), Prices.HighW(w2), Prices.Low(w1), Prices.LowD(w2), Prices.LowW(w2), Prices.Open(w1), Prices.OpenD(w2), Prices.OpenW(w2) | Núcleo: ruptura de máximos de N velas/día/semana, bandas y nube de Ichimoku, con órdenes stop; filtros de régimen (ADX, KER, medias, sistemas de tendencia), volatilidad y calendario. |
| Building blocks | `Bloques activos · stopLimitBlocks` | 29 activos | 38 activos: Stop/Limit Price Levels.BollingerBands(w2), Stop/Limit Price Levels.Close(w1), Stop/Limit Price Levels.CloseD(w2), Stop/Limit Price Levels.EMA(w1), Stop/Limit Price Levels.Fractal(w1), Stop/Limit Price Levels.GannHiLo(w1), Stop/Limit Price Levels.High(w1), Stop/Limit Price Levels.HighD(w2), Stop/Limit Price Levels.HighW(w2), Stop/Limit Price Levels.Highest(w5), Stop/Limit Price Levels.HullMovingAverage(w1), Stop/Limit Price Levels.Ichimoku(w1), Stop/Limit Price Levels.KAMA(w1), Stop/Limit Price Levels.KeltnerChannel(w2), Stop/Limit Price Levels.LWMA(w1), Stop/Limit Price Levels.LinearRegression(w1), Stop/Limit Price Levels.Low(w1), Stop/Limit Price Levels.LowD(w1), Stop/Limit Price Levels.LowW(w1), Stop/Limit Price Levels.Lowest(w1), Stop/Limit Price Levels.MTKeltnerChannel(w2), Stop/Limit Price Levels.Open(w1), Stop/Limit Price Levels.OpenD(w2), Stop/Limit Price Levels.OpenW(w2), Stop/Limit Price Levels.ParabolicSAR(w1), Stop/Limit Price Levels.Pivots(w1), Stop/Limit Price Levels.SMA(w1), Stop/Limit Price Levels.SMMA(w1), Stop/Limit Price Levels.SuperTrend(w1), Stop/Limit Price Levels.TEMA(w1), Stop/Limit Price Ranges.ATR(w2), Stop/Limit Price Ranges.BBRange(w2), Stop/Limit Price Ranges.BBWidthRatio(w2), Stop/Limit Price Ranges.BarRange(w2), Stop/Limit Price Ranges.BiggestRange(w2), Stop/Limit Price Ranges.MTATR(w2), Stop/Limit Price Ranges.SmallestRange(w2), Stop/Limit Price Ranges.TrueRange(w2) | Núcleo: ruptura de máximos de N velas/día/semana, bandas y nube de Ichimoku, con órdenes stop; filtros de régimen (ADX, KER, medias, sistemas de tendencia), volatilidad y calendario. |
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
| Building blocks | `ROCAboveLevel · Level` | -100..100/0.001 | 0..3/0.1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `ROCCrossesAboveLevel · Level` | -100..100/0.001 | 0..3/0.1 | Rango acotado al estilo (ver ficha). |
| Order types | `EnterAtStop@use` | false | true | Stop válida 8-24 h. |
| Order types | `EnterAtStop@weight` | 1 | 3 | Peso relativo entre tipos de orden. |
| Order types | `EnterAtStop · BarsValid max` | 10 | 6 | Stop válida 8-24 h. |
| Order types | `EnterAtStop · ExitAfterBars min` | 5 | 6 | Alineado con el rango de ExitTypes para eliminar la ambigüedad del original (5-20 vs 2-15). |
| Order types | `EnterAtStop · ExitAfterBars max` | 20 | 30 | Alineado con el rango de ExitTypes. |
| Order types | `EnterAtMarket · ExitAfterBars min` | 5 | 6 | Alineado con el rango de ExitTypes para eliminar la ambigüedad del original (5-20 vs 2-15). |
| Order types | `EnterAtMarket · ExitAfterBars max` | 20 | 30 | Alineado con el rango de ExitTypes. |
| Exit types | `StopLoss · PctValue` | true | false | Coherencia con SLPTOptions (SLPercent/PTPercent = false). |
| Exit types | `ProfitTarget@probability` | 100 | 50 | Stop amplio en ATR, objetivo y trailing opcionales, salida temporal 1-5 días. |
| Exit types | `ProfitTarget · PctValue` | true | false | Coherencia con SLPTOptions (SLPercent/PTPercent = false). |
| Exit types | `TrailingStop · FixedValue` | true | false | Valores fijos en pips no son trasladables entre timeframes/símbolos. |
| Exit types | `TrailingStop · ATR mult. min` | 1 | 2 | Stop amplio en ATR, objetivo y trailing opcionales, salida temporal 1-5 días. |
| Exit types | `TrailingStop · ATR mult. max` | 5 | 4 | Stop amplio en ATR, objetivo y trailing opcionales, salida temporal 1-5 días. |
| Exit types | `MoveSL2BE@use` | false | true | Stop amplio en ATR, objetivo y trailing opcionales, salida temporal 1-5 días. |
| Exit types | `MoveSL2BE@probability` | 50 | 30 | Stop amplio en ATR, objetivo y trailing opcionales, salida temporal 1-5 días. |
| Exit types | `MoveSL2BE · FixedValue` | true | false | Valores fijos en pips no son trasladables entre timeframes/símbolos. |
| Exit types | `MoveSL2BE · ATR mult. max` | 5 | 2 | Stop amplio en ATR, objetivo y trailing opcionales, salida temporal 1-5 días. |
| Exit types | `ExitAfterBars@use` | false | true | Stop amplio en ATR, objetivo y trailing opcionales, salida temporal 1-5 días. |
| Exit types | `ExitAfterBars@probability` | 50 | 40 | Stop amplio en ATR, objetivo y trailing opcionales, salida temporal 1-5 días. |
| Exit types | `ExitAfterBars min` | 2 | 6 | Stop amplio en ATR, objetivo y trailing opcionales, salida temporal 1-5 días. |
| Exit types | `ExitAfterBars max` | 15 | 30 | Stop amplio en ATR, objetivo y trailing opcionales, salida temporal 1-5 días. |
| Exit types | `_ExitRule_@use` | false | true | Salida por condición (cierre bajo media, oscilador en zona neutra...) coherente con el estilo. |
| Exit types | `_ExitRule_@probability` | 50 | 30 | Stop amplio en ATR, objetivo y trailing opcionales, salida temporal 1-5 días. |
| Notes | `Notes` | <b>Breakout strategies setup</b><div><br></div><div><br></div><div><br></div><div><br></div> | <b>Swing Trading (ruptura de consolidación multi-día) – Builder de estrategia completa – BUY</b><div>Derivado de Estrategia_Build_ConfigInicial_H1_BUY (build 140.2099). Timeframe H4. Ver docs/03 (ficha Swing) y docs/04 (checklist).</div><div>NO VALIDADO EN SQX: revisar símbolo, costes, horario del servidor e importación.</div> | Descripción del estilo y advertencias. |
