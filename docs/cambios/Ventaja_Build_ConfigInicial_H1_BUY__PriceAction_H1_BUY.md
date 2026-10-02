# Ventaja_Build_ConfigInicial_H1_BUY__PriceAction_H1_BUY

*Original:* `Ventaja_Build_ConfigInicial_H1_BUY.cfx` · *Estilo:* Acción del precio (patrones de vela en niveles) · *Timeframe:* H1 · *Rol:* Builder de test de ventaja (entrada) · *Dirección:* BUY

Tabla generada automáticamente a partir de los cambios aplicados al XML (cada fila es un valor que difiere del original). Estado: **no validado en SQX** (ver docs/04).

| Sección | Parámetro | Valor original | Valor nuevo | Justificación |
|---|---|---|---|---|
| Task | `Task@templateFile` | C:\Users\<usuario>\Desktop\Ventaja_Build_ConfigInicial_H1_BUY.cfx | Ventaja_Build_ConfigInicial_H1_BUY__PriceAction_H1_BUY.cfx | Ruta local del autor (C:\Users\<usuario>\Desktop\...) sustituida por el nombre del nuevo archivo: no aporta nada y expone el nombre de usuario de Windows. |
| Trading options | `Param key="MaxTradesPerDay"` | 0 | 2 | Evita encadenar señales en el mismo nivel. |
| Trading options | `Param key="MaxDistanceFromMarket"` | false | true | Tope para stops. |
| Trading options | `Param key="MaxDistancePct"` | 6 | 1 | 1 %. |
| Trading options | `Param key="ReservedBars"` | 50 | 60 | ≥ periodo máximo (50). |
| What to build · complejidad | `Chart@maxExitTypes` | 5 | 1 | Test de ventaja: sólo salida temporal, para medir la entrada aislada. |
| What to build · complejidad | `Chart@minPeriod` | 4 | 2 | Periodos 2-50 (estructura reciente); desplazamiento 1-3 para patrones de 2-3 velas. |
| What to build · complejidad | `Chart@maxPeriod` | 200 | 50 | Periodos 2-50 (estructura reciente); desplazamiento 1-3 para patrones de 2-3 velas. |
| What to build · complejidad | `Chart@maxShift` | 1 | 3 | Patrones de 2-3 velas. |
| Genetic options | `PopulationSize` | 15 | 40 | 5-15 individuos por isla es demasiado poco para que el cruce explore; 30-50 es un mínimo práctico. |
| Genetic options | `MaxGenerations` | 10 | 40 | Con 10 generaciones la evolución apenas actúa (y el reinicio por estancamiento a 30 nunca saltaba). |
| Genetic options | `Islands` | 5 | 4 | 4 islas: diversidad suficiente con menos coste. |
| Genetic options | `CrossoverProbability` | 46 | 80 | 46 % es bajo para un AG; 70-90 % es lo habitual (supuesto de práctica general, no de SQX). |
| Genetic options | `MutationProbability` | 35 | 30 | Algo menor para no destruir buenas soluciones. |
| Genetic options | `MigrationModulo` | 5 | 10 | Migrar cada 10 generaciones (con 30-40 generaciones). |
| Genetic options | `MigrationRate` | 6 | 10 | 6 % de 5 individuos = 0,3: la migración original era nula en la práctica. |
| Genetic options | `EvoRestartOnStagnation@generations` | 30 | 15 | Debe ser menor que MaxGenerations para poder actuar. |
| Genetic options | `BuildMode/Conditions (población inicial)` | ReturnDDRatio(IS) >= 2; AvgBarsInTrade(IS) >= 2; NumberOfTrades(IS) >= 250; WinningPct(IS) >= 35 | ReturnDDRatio(IS) >= 1; AvgBarsInTrade(IS) >= 2; NumberOfTrades(IS) >= 265; WinningPct(IS) >= 30 | Misma lógica del autor (≈60 % del Ret/DD final, ≈83 % de las operaciones, -5 puntos de acierto) con los umbrales del estilo. |
| Ranking | `Rankings/Conditions (filtros)` | AvgBarsInTrade(IS) >= 2; ReturnDDRatio(IS) >= 4; NumberOfTrades(IS) >= 300; WinningPct(IS) >= 40 | NumberOfTrades(IS) >= 320; ReturnDDRatio(IS) >= 2; WinningPct(IS) >= 35; ProfitFactor(IS) >= 1.15; AvgBarsInTrade(IS) >= 2; NetProfit(OOS) > 0; NumberOfTrades(OOS) >= 100 | Mínimo de operaciones = 60/año × años de cada tramo (el original exigía 300 en 7,25 años ≈ 41/año; ningún estilo baja de esa densidad salvo Position) + umbrales del estilo + exigencia en el tramo de validación OOS, que el original no tenía. Test de ventaja: Ret/DD a la mitad, PF mínimo 1,15. |
| Ranking | `FitnessCriteria/Settings/Ranking` | Weighted: Stagnation (peso 1, min) | Weighted: SQN (peso 2, max), StagnationPct (peso 1, min) | SQN mide la calidad estadística de la entrada (expectativa/desviación·√N); el original optimizaba sólo 'Stagnation', que ignora el beneficio. |
| Data | `Setup@slippage` | 0 | 0.3 | El original usa 0. |
| Data | `OutOfSample/Range` | (sin OOS) | 2019.01.01–2020.12.31 | Nuevo tramo de validación dentro del Builder (el original no tenía OOS y filtraba sólo sobre IS). |
| Building blocks | `Bloques activos · signals` | 146 activos | 38 activos: ATRChangesDown(w1), ATRChangesUp(w1), ATRFalling(w1), ATRRising(w1), BBBarClosesAboveUp(w1), BBBarOpensAboveUp(w1), BBBarOpensAboveUpAfterOpenBelow(w1), BBLowerFalling(w1), BBLowerRising(w1), BBUpperFalling(w1), BBUpperRising(w1), BarDayOfWeekIs(w1), BarDayOfWeekIsNot(w1), BarHourIs(w1), BarHourIsBigger(w1), BarHourIsSmaller(w1), BarMonthIs(w1), BarMonthIsNot(w1), BarOpensAboveHighestAfterOpenBelow(w3), BarOpensAboveLowestAfterOpenBelow(w4), BullishEngulfing(w8), Doji(w2), Hammer(w8), IsBullishFractal(w8), IsMonthFirstTradingDay(w1), IsMonthLastTradingDay(w1), KCBarClosesAboveUpper(w1), KCBarOpensAboveUpper(w1), KCBarOpensAboveUpperAfterOpenBelow(w1), KCLowerFalling(w1), KCLowerRising(w1), KCUpperFalling(w1), KCUpperRising(w1), PiercingLine(w8), StdDevChangesDown(w1), StdDevChangesUp(w1), StdDevFalling(w1), StdDevRising(w1) | Núcleo: velas de giro y falsas rupturas, precio puro, Heikin-Ashi y estructura (niveles diarios/semanales, fractales); ATR sólo como normalizador. Sin osciladores ni medias. |
| Building blocks | `Bloques activos · indicators` | 29 activos | 37 activos: CrossesAbove(w2), CrossesBelow(w2), Indicators.ATR(w1), Indicators.Fractal(w2), Indicators.Highest(w2), Indicators.HighestInRange(w1), Indicators.Lowest(w2), Indicators.LowestInRange(w1), Indicators.TrueRange(w1), IsFalling(w2), IsGreater(w2), IsGreaterCount(w2), IsGreaterOrEqual(w2), IsLower(w2), IsLowerCount(w2), IsLowerOrEqual(w2), IsRising(w2), Prices.Close(w3), Prices.CloseD(w2), Prices.CloseW(w1), Prices.HeikenAshiClose(w2), Prices.HeikenAshiHigh(w2), Prices.HeikenAshiLow(w2), Prices.HeikenAshiOpen(w2), Prices.High(w3), Prices.HighD(w2), Prices.HighW(w1), Prices.Low(w3), Prices.LowD(w2), Prices.LowW(w1), Prices.Open(w3), Prices.OpenD(w2), Prices.OpenW(w1), Prices.SessionClose(w1), Prices.SessionHigh(w1), Prices.SessionLow(w1), Prices.SessionOpen(w1) | Núcleo: velas de giro y falsas rupturas, precio puro, Heikin-Ashi y estructura (niveles diarios/semanales, fractales); ATR sólo como normalizador. Sin osciladores ni medias. |
| Building blocks | `Bloques activos · stopLimitBlocks` | 29 activos | 32 activos: Stop/Limit Price Levels.Close(w5), Stop/Limit Price Levels.CloseD(w2), Stop/Limit Price Levels.Fractal(w2), Stop/Limit Price Levels.HeikenAshiClose(w1), Stop/Limit Price Levels.HeikenAshiHigh(w1), Stop/Limit Price Levels.HeikenAshiLow(w1), Stop/Limit Price Levels.HeikenAshiOpen(w1), Stop/Limit Price Levels.High(w5), Stop/Limit Price Levels.HighD(w2), Stop/Limit Price Levels.HighW(w1), Stop/Limit Price Levels.Highest(w2), Stop/Limit Price Levels.HighestInRange(w1), Stop/Limit Price Levels.Low(w1), Stop/Limit Price Levels.LowD(w1), Stop/Limit Price Levels.LowW(w1), Stop/Limit Price Levels.Lowest(w1), Stop/Limit Price Levels.LowestInRange(w1), Stop/Limit Price Levels.Open(w5), Stop/Limit Price Levels.OpenD(w2), Stop/Limit Price Levels.OpenW(w1), Stop/Limit Price Levels.Pivots(w2), Stop/Limit Price Levels.SessionHigh(w1), Stop/Limit Price Levels.SessionLow(w1), Stop/Limit Price Levels.SessionOpen(w1), Stop/Limit Price Ranges.ATR(w2), Stop/Limit Price Ranges.BBRange(w2), Stop/Limit Price Ranges.BBWidthRatio(w2), Stop/Limit Price Ranges.BarRange(w2), Stop/Limit Price Ranges.BiggestRange(w2), Stop/Limit Price Ranges.MTATR(w2), Stop/Limit Price Ranges.SmallestRange(w2), Stop/Limit Price Ranges.TrueRange(w2) | Núcleo: velas de giro y falsas rupturas, precio puro, Heikin-Ashi y estructura (niveles diarios/semanales, fractales); ATR sólo como normalizador. Sin osciladores ni medias. |
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
| Order types | `EnterAtStop@use` | false | true | Stop sobre el extremo de la vela señal (confirmación) o límite en retroceso. |
| Order types | `EnterAtStop@weight` | 1 | 3 | Peso relativo entre tipos de orden. |
| Order types | `EnterAtStop · BarsValid min` | 2 | 1 | Stop sobre el extremo de la vela señal (confirmación) o límite en retroceso. |
| Order types | `EnterAtStop · BarsValid max` | 10 | 3 | Stop sobre el extremo de la vela señal (confirmación) o límite en retroceso. |
| Order types | `EnterAtStop · ExitAfterBars min` | 5 | 3 | Alineado con el rango de ExitTypes para eliminar la ambigüedad del original (5-20 vs 2-15). |
| Order types | `EnterAtStop · ExitAfterBars max` | 20 | 24 | Alineado con el rango de ExitTypes. |
| Order types | `EnterAtLimit@use` | false | true | Stop sobre el extremo de la vela señal (confirmación) o límite en retroceso. |
| Order types | `EnterAtLimit · BarsValid min` | 2 | 1 | Stop sobre el extremo de la vela señal (confirmación) o límite en retroceso. |
| Order types | `EnterAtLimit · BarsValid max` | 10 | 3 | Stop sobre el extremo de la vela señal (confirmación) o límite en retroceso. |
| Order types | `EnterAtLimit · ExitAfterBars min` | 5 | 3 | Alineado con el rango de ExitTypes para eliminar la ambigüedad del original (5-20 vs 2-15). |
| Order types | `EnterAtLimit · ExitAfterBars max` | 20 | 24 | Alineado con el rango de ExitTypes. |
| Order types | `EnterAtMarket · ExitAfterBars min` | 5 | 3 | Alineado con el rango de ExitTypes para eliminar la ambigüedad del original (5-20 vs 2-15). |
| Order types | `EnterAtMarket · ExitAfterBars max` | 20 | 24 | Alineado con el rango de ExitTypes. |
| Exit types | `ExitAfterBars@probability` | 50 | 100 | Explícito: es la única salida (el original ponía 50 y dependía de minExitTypes=1). |
| Exit types | `ExitAfterBars min` | 2 | 3 | Test de ventaja: salida por tiempo 3-24 h. |
| Exit types | `ExitAfterBars max` | 15 | 24 | Test de ventaja: salida por tiempo 3-24 h. |
| Notes | `Notes` | <b>Breakout strategies setup</b><div><br></div><div><br></div><div><br></div><div><br></div> | <b>Acción del precio (patrones de vela en niveles) – Builder de test de ventaja (entrada) – BUY</b><div>Derivado de Ventaja_Build_ConfigInicial_H1_BUY (build 140.2099). Timeframe H1. Ver docs/03 (ficha PriceAction) y docs/04 (checklist).</div><div>NO VALIDADO EN SQX: revisar símbolo, costes, horario del servidor e importación.</div> | Descripción del estilo y advertencias. |
