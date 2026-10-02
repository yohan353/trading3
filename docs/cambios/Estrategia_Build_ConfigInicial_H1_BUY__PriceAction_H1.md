# Estrategia_Build_ConfigInicial_H1_BUY__PriceAction_H1

*Original:* `Estrategia_Build_ConfigInicial_H1_BUY.cfx` · *Estilo:* Acción del precio (patrones de vela en niveles) · *Timeframe:* H1 · *Rol:* Builder de estrategia completa

Tabla generada automáticamente a partir de los cambios aplicados al XML (cada fila es un valor que difiere del original). Estado: **no validado en SQX** (ver docs/04).

| Sección | Parámetro | Valor original | Valor nuevo | Justificación |
|---|---|---|---|---|
| Task | `Task@templateFile` | C:\Users\<usuario>\Desktop\Estrategia_Build_ConfigInicial_H1_BUY.cfx | Estrategia_Build_ConfigInicial_H1_BUY__PriceAction_H1.cfx | Ruta local del autor (C:\Users\<usuario>\Desktop\...) sustituida por el nombre del nuevo archivo: no aporta nada y expone el nombre de usuario de Windows. |
| Trading options | `Param key="MaxTradesPerDay"` | 0 | 2 | Evita encadenar señales en el mismo nivel. |
| Trading options | `Param key="MaxDistanceFromMarket"` | false | true | Tope para stops. |
| Trading options | `Param key="MaxDistancePct"` | 6 | 1 | 1 %. |
| Trading options | `Param key="ReservedBars"` | 50 | 60 | ≥ periodo máximo (50). |
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
| Genetic options | `PopulationSize` | 5 | 40 | 5-15 individuos por isla es demasiado poco para que el cruce explore; 30-50 es un mínimo práctico. |
| Genetic options | `MaxGenerations` | 10 | 40 | Con 10 generaciones la evolución apenas actúa (y el reinicio por estancamiento a 30 nunca saltaba). |
| Genetic options | `Islands` | 5 | 4 | 4 islas: diversidad suficiente con menos coste. |
| Genetic options | `CrossoverProbability` | 46 | 80 | 46 % es bajo para un AG; 70-90 % es lo habitual (supuesto de práctica general, no de SQX). |
| Genetic options | `MutationProbability` | 35 | 30 | Algo menor para no destruir buenas soluciones. |
| Genetic options | `MigrationModulo` | 5 | 10 | Migrar cada 10 generaciones (con 30-40 generaciones). |
| Genetic options | `MigrationRate` | 6 | 10 | 6 % de 5 individuos = 0,3: la migración original era nula en la práctica. |
| Genetic options | `EvoRestartOnStagnation@generations` | 30 | 15 | Debe ser menor que MaxGenerations para poder actuar. |
| Genetic options | `BuildMode/Conditions (población inicial)` | ReturnDDRatio(IS) >= 5; AvgBarsInTrade(IS) >= 2; NumberOfTrades(IS) >= 250; WinningPct(IS) >= 35 | ReturnDDRatio(IS) >= 2.5; AvgBarsInTrade(IS) >= 2; NumberOfTrades(IS) >= 166; WinningPct(IS) >= 35 | Misma lógica del autor (≈60 % del Ret/DD final, ≈83 % de las operaciones, -5 puntos de acierto) con los umbrales del estilo. |
| Ranking | `Rankings/Conditions (filtros)` | AvgBarsInTrade(IS) >= 2; ReturnDDRatio(IS) >= 8; NumberOfTrades(IS) >= 300; WinningPct(IS) >= 40 | NumberOfTrades(IS) >= 200; ReturnDDRatio(IS) >= 4; WinningPct(IS) >= 40; ProfitFactor(IS) >= 1.3; AvgBarsInTrade(IS) >= 2; NetProfit(OOS) > 0; ProfitFactor(OOS) >= 1.1 | Umbrales del estilo (frecuencia, acierto típico, Ret/DD) + exigencia en el tramo de validación OOS, que el original no tenía. |
| Ranking | `FitnessCriteria/Settings/Ranking` | type="ReturnDDRatio" | Weighted: ReturnDDRatio (peso 2, max), SQN (peso 1, max) | Ret/DD + SQN (consistencia por operación). |
| Data | `Setup@slippage` | 0 | 0.3 | El original usa 0. |
| Data | `OutOfSample/Range` | (sin OOS) | 2019.01.01–2020.12.31 | Nuevo tramo de validación dentro del Builder (el original no tenía OOS y filtraba sólo sobre IS). |
| Building blocks | `Bloques activos · signals` | 146 activos | 7 activos: BarOpensAboveHighestAfterOpenBelow(w1), BarOpensAboveLowestAfterOpenBelow(w2), BullishEngulfing(w2), Doji(w1), Hammer(w2), IsBullishFractal(w1), PiercingLine(w2) | Sólo precio, velas y estructura; ATR únicamente como normalizador. Se excluyen patrones bajistas (el original los usaba como entrada larga, incoherente). |
| Building blocks | `Bloques activos · indicators` | 29 activos | 29 activos: CrossesAbove(w1), CrossesBelow(w1), Indicators.ATR(w1), Indicators.Fractal(w1), Indicators.Highest(w1), Indicators.Lowest(w1), Indicators.TrueRange(w1), IsFalling(w1), IsGreater(w1), IsGreaterCount(w1), IsLower(w1), IsLowerCount(w1), IsRising(w1), Prices.Close(w2), Prices.CloseD(w1), Prices.HeikenAshiClose(w1), Prices.HeikenAshiHigh(w1), Prices.HeikenAshiLow(w1), Prices.HeikenAshiOpen(w1), Prices.High(w2), Prices.HighD(w1), Prices.HighW(w1), Prices.Low(w2), Prices.LowD(w1), Prices.LowW(w1), Prices.Open(w2), Prices.OpenD(w1), Prices.SessionHigh(w1), Prices.SessionLow(w1) | Sólo precio, velas y estructura; ATR únicamente como normalizador. Se excluyen patrones bajistas (el original los usaba como entrada larga, incoherente). |
| Building blocks | `Bloques activos · stopLimitBlocks` | 29 activos | 9 activos: Stop/Limit Price Levels.Fractal(w1), Stop/Limit Price Levels.High(w3), Stop/Limit Price Levels.HighD(w1), Stop/Limit Price Levels.Highest(w1), Stop/Limit Price Levels.Low(w1), Stop/Limit Price Levels.OpenD(w1), Stop/Limit Price Ranges.ATR(w1), Stop/Limit Price Ranges.BarRange(w2), Stop/Limit Price Ranges.SmallestRange(w1) | Sólo precio, velas y estructura; ATR únicamente como normalizador. Se excluyen patrones bajistas (el original los usaba como entrada larga, incoherente). |
| Building blocks | `Prices.SessionHigh · Start Hours` | 0..23/1 | 1..3/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Prices.SessionHigh · Start Minutes` | 0..59/1 | 0..0/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Prices.SessionHigh · End Hours` | 0..23/1 | 8..10/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Prices.SessionHigh · End Minutes` | 0..59/1 | 0..0/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Prices.SessionLow · Start Hours` | 0..23/1 | 1..3/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Prices.SessionLow · Start Minutes` | 0..59/1 | 0..0/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Prices.SessionLow · End Hours` | 0..23/1 | 8..10/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Prices.SessionLow · End Minutes` | 0..59/1 | 0..0/1 | Rango acotado al estilo (ver ficha). |
| Order types | `EnterAtStop@use` | false | true | Stop sobre el máximo de la vela señal (confirmación) o límite en retroceso. |
| Order types | `EnterAtStop@weight` | 1 | 2 | Peso relativo entre tipos de orden. |
| Order types | `EnterAtStop · BarsValid min` | 2 | 1 | Stop sobre el máximo de la vela señal (confirmación) o límite en retroceso. |
| Order types | `EnterAtStop · BarsValid max` | 10 | 3 | Stop sobre el máximo de la vela señal (confirmación) o límite en retroceso. |
| Order types | `EnterAtStop · ExitAfterBars max` | 20 | 30 | Alineado con el rango de ExitTypes. |
| Order types | `EnterAtLimit@use` | false | true | Stop sobre el máximo de la vela señal (confirmación) o límite en retroceso. |
| Order types | `EnterAtLimit · BarsValid min` | 2 | 1 | Stop sobre el máximo de la vela señal (confirmación) o límite en retroceso. |
| Order types | `EnterAtLimit · BarsValid max` | 10 | 3 | Stop sobre el máximo de la vela señal (confirmación) o límite en retroceso. |
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
| Notes | `Notes` | <b>Breakout strategies setup</b><div><br></div><div><br></div><div><br></div><div><br></div> | <b>Acción del precio (patrones de vela en niveles) – Builder de estrategia completa</b><div>Derivado de Estrategia_Build_ConfigInicial_H1_BUY (build 140.2099). Timeframe H1. Ver docs/03 (ficha PriceAction) y docs/04 (checklist).</div><div>NO VALIDADO EN SQX: revisar símbolo, costes, horario del servidor e importación.</div> | Descripción del estilo y advertencias. |
