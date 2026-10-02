# Ventaja_Build_ConfigInicial_H1_BUY__Range_H1_BUY

*Original:* `Ventaja_Build_ConfigInicial_H1_BUY.cfx` · *Estilo:* Trading de rango (reversión a la media en régimen lateral) · *Timeframe:* H1 · *Rol:* Builder de test de ventaja (entrada) · *Dirección:* BUY

Tabla generada automáticamente a partir de los cambios aplicados al XML (cada fila es un valor que difiere del original). Estado: **no validado en SQX** (ver docs/04).

| Sección | Parámetro | Valor original | Valor nuevo | Justificación |
|---|---|---|---|---|
| Task | `Task@templateFile` | C:\Users\<usuario>\Desktop\Ventaja_Build_ConfigInicial_H1_BUY.cfx | Ventaja_Build_ConfigInicial_H1_BUY__Range_H1_BUY.cfx | Ruta local del autor (C:\Users\<usuario>\Desktop\...) sustituida por el nombre del nuevo archivo: no aporta nada y expone el nombre de usuario de Windows. |
| Trading options | `Param key="SignalTimeRangeTo"` | 84600 | 34200 | Sesión asiática: menor deriva direccional en FX. |
| Trading options | `Param key="MaxTradesPerDay"` | 0 | 2 | Evita promediar en tendencia. |
| Trading options | `Param key="MaxDistanceFromMarket"` | false | true | Las órdenes límite lejanas casi nunca se ejecutan. |
| Trading options | `Param key="MaxDistancePct"` | 6 | 1 | 1 %. |
| Trading options | `Param key="ReservedBars"` | 50 | 80 | ≥ periodo máximo (60). |
| What to build · complejidad | `Chart@maxExitTypes` | 5 | 1 | Test de ventaja: sólo salida temporal, para medir la entrada aislada. |
| What to build · complejidad | `Chart@minPeriod` | 4 | 5 | 5-60 velas H1: la reversión a la media es un fenómeno de corto plazo. |
| What to build · complejidad | `Chart@maxPeriod` | 200 | 60 | 5-60 velas H1: la reversión a la media es un fenómeno de corto plazo. |
| Genetic options | `PopulationSize` | 15 | 25 | 25 por isla × 4 islas = 100 por generación: más diversidad que el original (5-15) sin que la población inicial tarde horas en completarse. |
| Genetic options | `MaxGenerations` | 10 | 30 | Con 10 generaciones la evolución apenas actúa (y el reinicio por estancamiento a 30 nunca saltaba). |
| Genetic options | `Islands` | 5 | 4 | 4 islas: diversidad suficiente con menos coste. |
| Genetic options | `CrossoverProbability` | 46 | 80 | 46 % es bajo para un AG; 70-90 % es lo habitual (supuesto de práctica general, no de SQX). |
| Genetic options | `MutationProbability` | 35 | 30 | Algo menor para no destruir buenas soluciones. |
| Genetic options | `MigrationModulo` | 5 | 10 | Migrar cada 10 generaciones (con 30-40 generaciones). |
| Genetic options | `MigrationRate` | 6 | 10 | 6 % de 5 individuos = 0,3: la migración original era nula en la práctica. |
| Genetic options | `EvoRestartOnStagnation@generations` | 30 | 15 | Debe ser menor que MaxGenerations para poder actuar. |
| Genetic options | `BuildMode/Conditions (población inicial)` | ReturnDDRatio(IS) >= 2; AvgBarsInTrade(IS) >= 2; NumberOfTrades(IS) >= 250; WinningPct(IS) >= 35 | NumberOfTrades(IS) >= 100 | SÓLO nº mínimo de operaciones (30 % del mínimo final), como recomienda SQX. La población inicial no se guarda en el banco y SQX genera aleatorias hasta completarla: con 80-100 individuos y filtros de rentabilidad (Ret/DD, acierto) el Builder puede pasar horas o días sin producir nada. La exigencia de calidad está en los filtros del Ranking. |
| Ranking | `Rankings/Conditions (filtros)` | AvgBarsInTrade(IS) >= 2; ReturnDDRatio(IS) >= 4; NumberOfTrades(IS) >= 300; WinningPct(IS) >= 40 | NumberOfTrades(IS) >= 320; ReturnDDRatio(IS) >= 2; WinningPct(IS) >= 50; ProfitFactor(IS) >= 1.15; AvgBarsInTrade(IS) >= 2; NetProfit(OOS) > 0; NumberOfTrades(OOS) >= 100 | Mínimo de operaciones = 60/año × años de cada tramo (el original exigía 300 en 7,25 años ≈ 41/año; ningún estilo baja de esa densidad salvo Position) + umbrales del estilo + exigencia en el tramo de validación OOS, que el original no tenía. Test de ventaja: Ret/DD a la mitad, PF mínimo 1,15. |
| Ranking | `FitnessCriteria/Settings/Ranking` | Weighted: Stagnation (peso 1, min) | Weighted: SQN (peso 2, max), StagnationPct (peso 1, min) | SQN mide la calidad estadística de la entrada (expectativa/desviación·√N); el original optimizaba sólo 'Stagnation', que ignora el beneficio. |
| Data | `Setup@slippage` | 0 | 0.3 | El original usa 0. |
| Data | `OutOfSample/Range` | (sin OOS) | 2019.01.01–2020.12.31 | Nuevo tramo de validación dentro del Builder (el original no tenía OOS y filtraba sólo sobre IS). |
| Building blocks | `Calibration@calibrateBeforeStart` | false | true | Recalibra antes de empezar los rangos de valores de los indicadores (p. ej. ATR y rangos de órdenes stop/limit, que traen ±5000 por defecto) con el símbolo y timeframe de Data. Sin ello, al cambiar de H1 a M5/M15/H4/D1 las comparaciones con números y los desplazamientos de órdenes stop/limit no tienen sentido. |
| Building blocks | `Bloques activos · signals` | 146 activos | 47 activos: ADXChangesDown(w4), ADXCrossDown(w4), ADXFalling(w4), ADXLower(w4), ATRChangesDown(w1), ATRFalling(w1), BBBarClosesAboveDown(w6), BBBarClosesBelowDown(w6), BBBarOpensAboveDownAfterOpenBelow(w6), BBBarOpensBelowDown(w6), BBLowerRising(w1), BBUpperFalling(w1), BarDayOfWeekIsNot(w1), BarHourIsBigger(w1), BarHourIsSmaller(w1), BarOpensAboveLowestAfterOpenBelow(w3), BullishEngulfing(w1), CCICrossUp(w3), CCILower(w3), DEMCrossUp(w3), DEMLower(w3), Doji(w1), Hammer(w1), IsBullishFractal(w1), KCBarClosesAboveLower(w6), KCBarClosesBelowLower(w6), KCBarOpensAboveLowerAfterOpenBelow(w6), KCBarOpensBelowLower(w6), KCLowerRising(w1), KCUpperFalling(w1), KERbelowLevel(w4), LaguerreRSICrossUP(w3), PiercingLine(w1), QQEValue1CrossAbove(w3), QQEValue1Lower(w3), RSICrossUp(w3), RSILower(w3), SchaffTrendCycleBelowLevel(w3), SchaffTrendCycleCrossesAboveLevel(w3), StdDevChangesDown(w1), StdDevFalling(w1), StochFastKCrossUp(w3), StochSlowDCrossUp(w3), StochSlowDLower(w3), SuperTrendInRange(w4), WPRCrossUp(w3), WPRLower(w3) | Núcleo: reentrada en bandas tras exceso, osciladores restringidos a sobreventa (sobrecompra en SELL) y filtros de régimen lateral; órdenes límite en la banda/extremo. Los rangos 0-100 originales permitían 'comprar en sobrecompra'. |
| Building blocks | `Bloques activos · indicators` | 29 activos | 48 activos: CrossesAbove(w1), CrossesBelow(w1), Indicators.ADX(w1), Indicators.ATR(w1), Indicators.Aroon(w1), Indicators.BollingerBands(w3), Indicators.CCI(w2), Indicators.DeMarker(w2), Indicators.EMA(w2), Indicators.Highest(w2), Indicators.HighestInRange(w1), Indicators.HullMovingAverage(w2), Indicators.KAMA(w2), Indicators.KaufmanEfficiencyRatio(w1), Indicators.KeltnerChannel(w3), Indicators.LWMA(w2), Indicators.LaguerreRSI(w2), Indicators.LinearRegression(w2), Indicators.Lowest(w2), Indicators.LowestInRange(w1), Indicators.RSI(w2), Indicators.SMA(w2), Indicators.SMMA(w2), Indicators.Stochastic(w2), Indicators.TEMA(w2), Indicators.TrueRange(w1), Indicators.Vortex(w1), Indicators.WilliamsPR(w2), IsFalling(w2), IsGreater(w1), IsGreaterCount(w2), IsGreaterOrEqual(w1), IsLower(w1), IsLowerCount(w2), IsLowerOrEqual(w1), IsRising(w2), Prices.Close(w1), Prices.CloseD(w1), Prices.High(w1), Prices.HighD(w1), Prices.Low(w1), Prices.LowD(w1), Prices.Open(w1), Prices.OpenD(w1), Prices.SessionClose(w1), Prices.SessionHigh(w1), Prices.SessionLow(w1), Prices.SessionOpen(w1) | Núcleo: reentrada en bandas tras exceso, osciladores restringidos a sobreventa (sobrecompra en SELL) y filtros de régimen lateral; órdenes límite en la banda/extremo. Los rangos 0-100 originales permitían 'comprar en sobrecompra'. |
| Building blocks | `Bloques activos · stopLimitBlocks` | 29 activos | 36 activos: Stop/Limit Price Levels.BollingerBands(w5), Stop/Limit Price Levels.Close(w2), Stop/Limit Price Levels.CloseD(w1), Stop/Limit Price Levels.EMA(w2), Stop/Limit Price Levels.Fractal(w1), Stop/Limit Price Levels.High(w1), Stop/Limit Price Levels.HighD(w1), Stop/Limit Price Levels.Highest(w1), Stop/Limit Price Levels.HighestInRange(w1), Stop/Limit Price Levels.HullMovingAverage(w2), Stop/Limit Price Levels.KAMA(w2), Stop/Limit Price Levels.KeltnerChannel(w5), Stop/Limit Price Levels.LWMA(w2), Stop/Limit Price Levels.LinearRegression(w2), Stop/Limit Price Levels.Low(w3), Stop/Limit Price Levels.LowD(w2), Stop/Limit Price Levels.Lowest(w3), Stop/Limit Price Levels.LowestInRange(w2), Stop/Limit Price Levels.MTKeltnerChannel(w5), Stop/Limit Price Levels.Open(w2), Stop/Limit Price Levels.OpenD(w1), Stop/Limit Price Levels.Pivots(w1), Stop/Limit Price Levels.SMA(w2), Stop/Limit Price Levels.SMMA(w2), Stop/Limit Price Levels.SessionHigh(w1), Stop/Limit Price Levels.SessionLow(w2), Stop/Limit Price Levels.SessionOpen(w1), Stop/Limit Price Levels.TEMA(w2), Stop/Limit Price Ranges.ATR(w2), Stop/Limit Price Ranges.BBRange(w2), Stop/Limit Price Ranges.BBWidthRatio(w2), Stop/Limit Price Ranges.BarRange(w2), Stop/Limit Price Ranges.BiggestRange(w2), Stop/Limit Price Ranges.MTATR(w2), Stop/Limit Price Ranges.SmallestRange(w2), Stop/Limit Price Ranges.TrueRange(w2) | Núcleo: reentrada en bandas tras exceso, osciladores restringidos a sobreventa (sobrecompra en SELL) y filtros de régimen lateral; órdenes límite en la banda/extremo. Los rangos 0-100 originales permitían 'comprar en sobrecompra'. |
| Building blocks | `RSICrossUp · Level` | 0..100/5 | 15..40/5 | Rango acotado al estilo (ver ficha). |
| Building blocks | `RSILower · Level` | 0..100/5 | 20..40/5 | Rango acotado al estilo (ver ficha). |
| Building blocks | `StochSlowDCrossUp · Level` | 0..100/5 | 10..30/5 | Rango acotado al estilo (ver ficha). |
| Building blocks | `StochFastKCrossUp · Level` | 0..100/5 | 10..30/5 | Rango acotado al estilo (ver ficha). |
| Building blocks | `StochSlowDLower · Level` | 0..100/5 | 10..30/5 | Rango acotado al estilo (ver ficha). |
| Building blocks | `WPRCrossUp · Level` | -100..0/5 | -95..-75/5 | Rango acotado al estilo (ver ficha). |
| Building blocks | `WPRLower · Level` | -100..0/5 | -95..-75/5 | Rango acotado al estilo (ver ficha). |
| Building blocks | `CCICrossUp · Level` | -120..120/5 | -200..-80/10 | Rango acotado al estilo (ver ficha). |
| Building blocks | `CCILower · Level` | -120..120/5 | -200..-80/10 | Rango acotado al estilo (ver ficha). |
| Building blocks | `LaguerreRSICrossUP · Gamma` | 0..0.95/0.01 | 0.3..0.8/0.05 | Rango acotado al estilo (ver ficha). |
| Building blocks | `LaguerreRSICrossUP · Level` | 0.05..0.95/0.05 | 0.05..0.3/0.05 | Rango acotado al estilo (ver ficha). |
| Building blocks | `DEMCrossUp · Level` | 0..1/0.1 | 0.1..0.3/0.05 | Rango acotado al estilo (ver ficha). |
| Building blocks | `DEMLower · Level` | 0..1/0.1 | 0.1..0.3/0.05 | Rango acotado al estilo (ver ficha). |
| Building blocks | `QQEValue1CrossAbove · Level` | 20..90/5 | 20..40/5 | Rango acotado al estilo (ver ficha). |
| Building blocks | `QQEValue1Lower · Level` | 20..90/5 | 20..40/5 | Rango acotado al estilo (ver ficha). |
| Building blocks | `SchaffTrendCycleCrossesAboveLevel · Level` | 0.1..99.9/0.1 | 5..25/5 | Rango acotado al estilo (ver ficha). |
| Building blocks | `SchaffTrendCycleBelowLevel · Level` | 0.1..90/0.1 | 5..25/5 | Rango acotado al estilo (ver ficha). |
| Building blocks | `ADXLower · Level` | 20..90/10 | 15..30/5 | Rango acotado al estilo (ver ficha). |
| Building blocks | `ADXCrossDown · Level` | 20..90/10 | 20..30/5 | Rango acotado al estilo (ver ficha). |
| Building blocks | `KERbelowLevel · Level` | 0.05..1/0.05 | 0.1..0.4/0.05 | Rango acotado al estilo (ver ficha). |
| Building blocks | `SuperTrendInRange · ATR Mult` | 0.5..10/0.1 | 1.5..5/0.5 | Rango acotado al estilo (ver ficha). |
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
| Building blocks | `Prices.SessionOpen · Start Hours` | 0..23/1 | 1..3/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Prices.SessionOpen · Start Minutes` | 0..59/1 | 0..0/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Stop/Limit Price Levels.SessionOpen · Start Hours` | 0..23/1 | 1..3/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Stop/Limit Price Levels.SessionOpen · Start Minutes` | 0..59/1 | 0..0/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Prices.SessionClose · End Hours` | 0..23/1 | 8..10/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Prices.SessionClose · End Minutes` | 0..59/1 | 0..0/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `BarHourIsBigger · Hour` | 0..23/1 | 1..4/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `BarHourIsSmaller · Hour` | 0..23/1 | 5..10/1 | Rango acotado al estilo (ver ficha). |
| Order types | `EnterAtLimit@use` | false | true | Límite bajo la banda/mínimo (sobre la banda/máximo en SELL): se opera el exceso, no la ruptura. |
| Order types | `EnterAtLimit@weight` | 1 | 3 | Peso relativo entre tipos de orden. |
| Order types | `EnterAtLimit · BarsValid min` | 2 | 1 | Límite bajo la banda/mínimo (sobre la banda/máximo en SELL): se opera el exceso, no la ruptura. |
| Order types | `EnterAtLimit · BarsValid max` | 10 | 5 | Límite bajo la banda/mínimo (sobre la banda/máximo en SELL): se opera el exceso, no la ruptura. |
| Order types | `EnterAtLimit · ExitAfterBars min` | 5 | 3 | Alineado con el rango de ExitTypes para eliminar la ambigüedad del original (5-20 vs 2-15). |
| Order types | `EnterAtLimit · ExitAfterBars max` | 20 | 24 | Alineado con el rango de ExitTypes. |
| Order types | `EnterAtMarket · ExitAfterBars min` | 5 | 3 | Alineado con el rango de ExitTypes para eliminar la ambigüedad del original (5-20 vs 2-15). |
| Order types | `EnterAtMarket · ExitAfterBars max` | 20 | 24 | Alineado con el rango de ExitTypes. |
| Exit types | `ExitAfterBars@probability` | 50 | 100 | Explícito: es la única salida (el original ponía 50 y dependía de minExitTypes=1). |
| Exit types | `ExitAfterBars min` | 2 | 3 | Test de ventaja: salida por tiempo 3-24 h. |
| Exit types | `ExitAfterBars max` | 15 | 24 | Test de ventaja: salida por tiempo 3-24 h. |
| Notes | `Notes` | <b>Breakout strategies setup</b><div><br></div><div><br></div><div><br></div><div><br></div> | <b>Trading de rango (reversión a la media en régimen lateral) – Builder de test de ventaja (entrada) – BUY</b><div>Derivado de Ventaja_Build_ConfigInicial_H1_BUY (build 140.2099). Timeframe H1. Ver docs/03 (ficha Range) y docs/04 (checklist).</div><div>NO VALIDADO EN SQX: revisar símbolo, costes, horario del servidor e importación.</div> | Descripción del estilo y advertencias. |
