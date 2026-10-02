# Estrategia_Build_ConfigInicial_H1_BUY__PriceAction_H1_SELL

*Original:* `Estrategia_Build_ConfigInicial_H1_BUY.cfx` · *Estilo:* Acción del precio (patrones de vela en niveles) · *Timeframe:* H1 · *Rol:* Builder de estrategia completa · *Dirección:* SELL

Tabla generada automáticamente a partir de los cambios aplicados al XML (cada fila es un valor que difiere del original). Estado: **no validado en SQX** (ver docs/04).

| Sección | Parámetro | Valor original | Valor nuevo | Justificación |
|---|---|---|---|---|
| Task | `Task@templateFile` | C:\Users\<usuario>\Desktop\Estrategia_Build_ConfigInicial_H1_BUY.cfx | Estrategia_Build_ConfigInicial_H1_BUY__PriceAction_H1_SELL.cfx | Ruta local del autor (C:\Users\<usuario>\Desktop\...) sustituida por el nombre del nuevo archivo: no aporta nada y expone el nombre de usuario de Windows. |
| Trading options | `Param key="MaxTradesPerDay"` | 0 | 2 | Evita encadenar señales en el mismo nivel. |
| Trading options | `Param key="MaxDistanceFromMarket"` | false | true | Tope para stops. |
| Trading options | `Param key="MaxDistancePct"` | 6 | 1 | 1 %. |
| Trading options | `Param key="ReservedBars"` | 50 | 60 | ≥ periodo máximo (50). |
| What to build | `MarketSides@type` | long | short | Kit SELL: sólo ventas. Sin simetría, SQX usa los bloques tal cual, por eso se activan los equivalentes bajistas (espejo) en Building blocks. |
| What to build | `StrategyType@type` | template | simple | El original dependía de una plantilla .sqx externa (Template_DOW_H1_BUY_1.8.4.sqx) que no viene en el .cfx; en modo 'simple' el archivo funciona por sí solo y la selección de bloques del estilo pasa a determinar la entrada. Para volver al flujo plantilla, ver docs/04 §A.3. |
| What to build | `StrategyType@templateFile` | C:\Users\<usuario>\Documents\StrategyQuant\00 - Temp\Formación\DOWJONES_H1_BUY\Template\Template_DOW_H1_BUY_1.8.4.sqx | SQ3StrategyTemplateExample.sq4 | Valor por defecto (el mismo que Ventaja_Build); en modo 'simple' no se usa. |
| What to build · complejidad | `Chart@minConditions` | 0 | 1 | Entrada generada por el Builder. |
| What to build · complejidad | `Chart@maxConditions` | 0 | 3 | Periodos 2-50 (estructura reciente); desplazamiento 1-3 para patrones de 2-3 velas. |
| What to build · complejidad | `Chart@maxExitConditions` | 3 | 2 | Máximo 1-2: una salida por regla sencilla es más robusta. |
| What to build · complejidad | `Chart@minExitTypes` | 1 | 2 | Al menos SL + otra salida. |
| What to build · complejidad | `Chart@maxExitTypes` | 5 | 4 | El original pedía hasta 5 con sólo 3 tipos activos. |
| What to build · complejidad | `Chart@minPeriod` | 4 | 2 | Periodos 2-50 (estructura reciente); desplazamiento 1-3 para patrones de 2-3 velas. |
| What to build · complejidad | `Chart@maxPeriod` | 200 | 50 | Periodos 2-50 (estructura reciente); desplazamiento 1-3 para patrones de 2-3 velas. |
| What to build · complejidad | `Chart@maxShift` | 1 | 3 | Patrones de 2-3 velas. |
| What to build · SL/PT | `MaxSLATRMultiple` | 3 | 2.5 | Rango de SL del estilo: 1.0-2.5 ATR. |
| What to build · SL/PT | `MinSLATRPeriod` | 20 | 14 | ATR(14-50) en velas H1. |
| What to build · SL/PT | `MaxSLATRPeriod` | 100 | 50 | ATR(14-50) en velas H1. |
| What to build · SL/PT | `MinPTATRMultiple` | 2 | 1.5 | Rango de PT: 1.5-4.0 ATR. |
| What to build · SL/PT | `MaxPTATRMultiple` | 5 | 4 | Rango de PT: 1.5-4.0 ATR. |
| What to build · SL/PT | `MinPTATRPeriod` | 20 | 14 | ATR(14-50). |
| What to build · SL/PT | `MaxPTATRPeriod` | 100 | 50 | ATR(14-50). |
| What to build · SL/PT | `LimitSLPTRRRFrom` | 100 | 150 | PT = 150-300 % del SL. |
| What to build · SL/PT | `LimitSLPTRRRTo` | 500 | 300 | PT = 150-300 % del SL. |
| Genetic options | `PopulationSize` | 5 | 25 | 25 por isla × 4 islas = 100 por generación: más diversidad que el original (5-15) sin que la población inicial tarde horas en completarse. |
| Genetic options | `MaxGenerations` | 10 | 30 | Con 10 generaciones la evolución apenas actúa (y el reinicio por estancamiento a 30 nunca saltaba). |
| Genetic options | `Islands` | 5 | 4 | 4 islas: diversidad suficiente con menos coste. |
| Genetic options | `CrossoverProbability` | 46 | 80 | 46 % es bajo para un AG; 70-90 % es lo habitual (supuesto de práctica general, no de SQX). |
| Genetic options | `MutationProbability` | 35 | 30 | Algo menor para no destruir buenas soluciones. |
| Genetic options | `MigrationModulo` | 5 | 10 | Migrar cada 10 generaciones (con 30-40 generaciones). |
| Genetic options | `MigrationRate` | 6 | 10 | 6 % de 5 individuos = 0,3: la migración original era nula en la práctica. |
| Genetic options | `EvoRestartOnStagnation@generations` | 30 | 15 | Debe ser menor que MaxGenerations para poder actuar. |
| Genetic options | `BuildMode/Conditions (población inicial)` | ReturnDDRatio(IS) >= 5; AvgBarsInTrade(IS) >= 2; NumberOfTrades(IS) >= 250; WinningPct(IS) >= 35 | NumberOfTrades(IS) >= 100 | SÓLO nº mínimo de operaciones (30 % del mínimo final), como recomienda SQX. La población inicial no se guarda en el banco y SQX genera aleatorias hasta completarla: con 80-100 individuos y filtros de rentabilidad (Ret/DD, acierto) el Builder puede pasar horas o días sin producir nada. La exigencia de calidad está en los filtros del Ranking. |
| Ranking | `Rankings/Conditions (filtros)` | AvgBarsInTrade(IS) >= 2; ReturnDDRatio(IS) >= 8; NumberOfTrades(IS) >= 300; WinningPct(IS) >= 40 | NumberOfTrades(IS) >= 320; ReturnDDRatio(IS) >= 4; WinningPct(IS) >= 40; ProfitFactor(IS) >= 1.3; AvgBarsInTrade(IS) >= 2; NetProfit(OOS) > 0; NumberOfTrades(OOS) >= 100 | Mínimo de operaciones = 60/año × años de cada tramo (el original exigía 300 en 7,25 años ≈ 41/año; ningún estilo baja de esa densidad salvo Position) + umbrales del estilo + exigencia en el tramo de validación OOS, que el original no tenía. |
| Ranking | `FitnessCriteria/Settings/Ranking` | type="ReturnDDRatio" | Weighted: ReturnDDRatio (peso 2, max), SQN (peso 1, max) | Ret/DD + SQN (consistencia por operación). |
| Data | `Setup@slippage` | 0 | 0.3 | El original usa 0. |
| Data | `OutOfSample/Range` | (sin OOS) | 2019.01.01–2020.12.31 | Nuevo tramo de validación dentro del Builder (el original no tenía OOS y filtraba sólo sobre IS). |
| Building blocks | `Calibration@calibrateBeforeStart` | false | true | Recalibra antes de empezar los rangos de valores de los indicadores (p. ej. ATR y rangos de órdenes stop/limit, que traen ±5000 por defecto) con el símbolo y timeframe de Data. Sin ello, al cambiar de H1 a M5/M15/H4/D1 las comparaciones con números y los desplazamientos de órdenes stop/limit no tienen sentido. |
| Building blocks | `Bloques activos · signals` | 146 activos | 33 activos: ATRChangesDown(w1), ATRChangesUp(w1), ATRFalling(w1), ATRRising(w1), BBBarClosesBelowDown(w1), BBBarOpensBelowDown(w1), BBBarOpensBelowDownAfterOpenAbove(w1), BBLowerFalling(w1), BBLowerRising(w1), BBUpperFalling(w1), BBUpperRising(w1), BarDayOfWeekIsNot(w1), BarHourIsBigger(w1), BarHourIsSmaller(w1), BarMonthIsNot(w1), BarOpensBelowHighestAfterOpenAbove(w4), BarOpensBelowLowestAfterOpenAbove(w3), BearishEngulfing(w8), DarkCloud(w8), Doji(w2), IsBearishFractal(w8), KCBarClosesBelowLower(w1), KCBarOpensBelowLower(w1), KCBarOpensBelowLowerAfterOpenAbove(w1), KCLowerFalling(w1), KCLowerRising(w1), KCUpperFalling(w1), KCUpperRising(w1), ShootingStar(w8), StdDevChangesDown(w1), StdDevChangesUp(w1), StdDevFalling(w1), StdDevRising(w1) | Núcleo: velas de giro y falsas rupturas, precio puro, Heikin-Ashi y estructura (niveles diarios/semanales, fractales); ATR sólo como normalizador. Sin osciladores ni medias. Versión SELL: bloques y niveles espejados. |
| Building blocks | `Bloques activos · indicators` | 29 activos | 37 activos: CrossesAbove(w2), CrossesBelow(w2), Indicators.ATR(w1), Indicators.Fractal(w2), Indicators.Highest(w2), Indicators.HighestInRange(w1), Indicators.Lowest(w2), Indicators.LowestInRange(w1), Indicators.TrueRange(w1), IsFalling(w2), IsGreater(w2), IsGreaterCount(w2), IsGreaterOrEqual(w2), IsLower(w2), IsLowerCount(w2), IsLowerOrEqual(w2), IsRising(w2), Prices.Close(w3), Prices.CloseD(w2), Prices.CloseW(w1), Prices.HeikenAshiClose(w2), Prices.HeikenAshiHigh(w2), Prices.HeikenAshiLow(w2), Prices.HeikenAshiOpen(w2), Prices.High(w3), Prices.HighD(w2), Prices.HighW(w1), Prices.Low(w3), Prices.LowD(w2), Prices.LowW(w1), Prices.Open(w3), Prices.OpenD(w2), Prices.OpenW(w1), Prices.SessionClose(w1), Prices.SessionHigh(w1), Prices.SessionLow(w1), Prices.SessionOpen(w1) | Núcleo: velas de giro y falsas rupturas, precio puro, Heikin-Ashi y estructura (niveles diarios/semanales, fractales); ATR sólo como normalizador. Sin osciladores ni medias. Versión SELL: bloques y niveles espejados. |
| Building blocks | `Bloques activos · stopLimitBlocks` | 29 activos | 32 activos: Stop/Limit Price Levels.Close(w5), Stop/Limit Price Levels.CloseD(w2), Stop/Limit Price Levels.Fractal(w2), Stop/Limit Price Levels.HeikenAshiClose(w1), Stop/Limit Price Levels.HeikenAshiHigh(w1), Stop/Limit Price Levels.HeikenAshiLow(w1), Stop/Limit Price Levels.HeikenAshiOpen(w1), Stop/Limit Price Levels.High(w1), Stop/Limit Price Levels.HighD(w1), Stop/Limit Price Levels.HighW(w1), Stop/Limit Price Levels.Highest(w1), Stop/Limit Price Levels.HighestInRange(w1), Stop/Limit Price Levels.Low(w5), Stop/Limit Price Levels.LowD(w2), Stop/Limit Price Levels.LowW(w1), Stop/Limit Price Levels.Lowest(w2), Stop/Limit Price Levels.LowestInRange(w1), Stop/Limit Price Levels.Open(w5), Stop/Limit Price Levels.OpenD(w2), Stop/Limit Price Levels.OpenW(w1), Stop/Limit Price Levels.Pivots(w2), Stop/Limit Price Levels.SessionHigh(w1), Stop/Limit Price Levels.SessionLow(w1), Stop/Limit Price Levels.SessionOpen(w1), Stop/Limit Price Ranges.ATR(w2), Stop/Limit Price Ranges.BBRange(w2), Stop/Limit Price Ranges.BBWidthRatio(w2), Stop/Limit Price Ranges.BarRange(w2), Stop/Limit Price Ranges.BiggestRange(w2), Stop/Limit Price Ranges.MTATR(w2), Stop/Limit Price Ranges.SmallestRange(w2), Stop/Limit Price Ranges.TrueRange(w2) | Núcleo: velas de giro y falsas rupturas, precio puro, Heikin-Ashi y estructura (niveles diarios/semanales, fractales); ATR sólo como normalizador. Sin osciladores ni medias. Versión SELL: bloques y niveles espejados. |
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
| Order types | `EnterAtStop@use` | false | true | Stop sobre el extremo de la vela señal (confirmación) o límite en retroceso. |
| Order types | `EnterAtStop@weight` | 1 | 3 | Peso relativo entre tipos de orden. |
| Order types | `EnterAtStop · BarsValid min` | 2 | 1 | Stop sobre el extremo de la vela señal (confirmación) o límite en retroceso. |
| Order types | `EnterAtStop · BarsValid max` | 10 | 3 | Stop sobre el extremo de la vela señal (confirmación) o límite en retroceso. |
| Order types | `EnterAtStop · ExitAfterBars max` | 20 | 30 | Alineado con el rango de ExitTypes. |
| Order types | `EnterAtLimit@use` | false | true | Stop sobre el extremo de la vela señal (confirmación) o límite en retroceso. |
| Order types | `EnterAtLimit · BarsValid min` | 2 | 1 | Stop sobre el extremo de la vela señal (confirmación) o límite en retroceso. |
| Order types | `EnterAtLimit · BarsValid max` | 10 | 3 | Stop sobre el extremo de la vela señal (confirmación) o límite en retroceso. |
| Order types | `EnterAtLimit · ExitAfterBars max` | 20 | 30 | Alineado con el rango de ExitTypes. |
| Order types | `EnterAtMarket · ExitAfterBars max` | 20 | 30 | Alineado con el rango de ExitTypes. |
| Exit types | `StopLoss · PctValue` | true | false | Coherencia con SLPTOptions (SLPercent/PTPercent = false). |
| Exit types | `ProfitTarget · PctValue` | true | false | Coherencia con SLPTOptions (SLPercent/PTPercent = false). |
| Exit types | `TrailingStop@use` | true | false | El estilo no usa trailing. |
| Exit types | `MoveSL2BE@use` | false | true | R:R 1,5-3 sobre el riesgo de la vela; break-even tras 1-2 ATR. |
| Exit types | `MoveSL2BE · FixedValue` | true | false | Valores fijos en pips no son trasladables entre timeframes/símbolos. |
| Exit types | `MoveSL2BE · ATR mult. max` | 5 | 2 | R:R 1,5-3 sobre el riesgo de la vela; break-even tras 1-2 ATR. |
| Exit types | `ExitAfterBars@use` | false | true | R:R 1,5-3 sobre el riesgo de la vela; break-even tras 1-2 ATR. |
| Exit types | `ExitAfterBars@probability` | 50 | 30 | R:R 1,5-3 sobre el riesgo de la vela; break-even tras 1-2 ATR. |
| Exit types | `ExitAfterBars min` | 2 | 5 | R:R 1,5-3 sobre el riesgo de la vela; break-even tras 1-2 ATR. |
| Exit types | `ExitAfterBars max` | 15 | 30 | R:R 1,5-3 sobre el riesgo de la vela; break-even tras 1-2 ATR. |
| Exit types | `_ExitRule_@use` | false | true | Salida por condición (cierre bajo media, oscilador en zona neutra...) coherente con el estilo. |
| Exit types | `_ExitRule_@probability` | 50 | 30 | R:R 1,5-3 sobre el riesgo de la vela; break-even tras 1-2 ATR. |
| Notes | `Notes` | <b>Breakout strategies setup</b><div><br></div><div><br></div><div><br></div><div><br></div> | <b>Acción del precio (patrones de vela en niveles) – Builder de estrategia completa – SELL</b><div>Derivado de Estrategia_Build_ConfigInicial_H1_BUY (build 140.2099). Timeframe H1. Ver docs/03 (ficha PriceAction) y docs/04 (checklist).</div><div>NO VALIDADO EN SQX: revisar símbolo, costes, horario del servidor e importación.</div> | Descripción del estilo y advertencias. |
