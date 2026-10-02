# Estrategia_Build_ConfigInicial_H1_BUY__Position_D1

*Original:* `Estrategia_Build_ConfigInicial_H1_BUY.cfx` · *Estilo:* Position Trading (momentum de largo plazo) · *Timeframe:* D1 · *Rol:* Builder de estrategia completa

Tabla generada automáticamente a partir de los cambios aplicados al XML (cada fila es un valor que difiere del original). Estado: **no validado en SQX** (ver docs/04).

| Sección | Parámetro | Valor original | Valor nuevo | Justificación |
|---|---|---|---|---|
| Task | `Task@templateFile` | C:\Users\<usuario>\Desktop\Estrategia_Build_ConfigInicial_H1_BUY.cfx | Estrategia_Build_ConfigInicial_H1_BUY__Position_D1.cfx | Ruta local del autor (C:\Users\<usuario>\Desktop\...) sustituida por el nombre del nuevo archivo: no aporta nada y expone el nombre de usuario de Windows. |
| Trading options | `Param key="LimitTimeRange"` | true | false | Con velas D1 (apertura 00:00) la ventana 01:30-23:30 del original podría bloquear todas las señales. |
| Trading options | `Param key="MaxTradesPerDay"` | 0 | 1 | Position: una entrada como máximo. |
| Trading options | `Param key="MaxDistanceFromMarket"` | false | true | Tope de distancia para stops. |
| Trading options | `Param key="MaxDistancePct"` | 6 | 5 | 5 %: rupturas de máximos de 20-250 días. |
| Trading options | `Param key="ReservedBars"` | 50 | 260 | ≥ periodo máximo (250). |
| What to build | `StrategyType@type` | template | simple | El original dependía de una plantilla .sqx externa (Template_DOW_H1_BUY_1.8.4.sqx) que no viene en el .cfx; en modo 'simple' el archivo funciona por sí solo y la selección de bloques del estilo pasa a determinar la entrada. Para volver al flujo plantilla, ver docs/04 §A.3. |
| What to build | `StrategyType@templateFile` | C:\Users\<usuario>\Documents\StrategyQuant\00 - Temp\Formación\DOWJONES_H1_BUY\Template\Template_DOW_H1_BUY_1.8.4.sqx | SQ3StrategyTemplateExample.sq4 | Valor por defecto (el mismo que Ventaja_Build); en modo 'simple' no se usa. |
| What to build · complejidad | `Chart@minConditions` | 0 | 1 | Entrada generada por el Builder. |
| What to build · complejidad | `Chart@maxConditions` | 0 | 2 | 20-250 días (1 mes-1 año). Máximo 2 condiciones: con ~8 operaciones/año cada grado de libertad extra es sobreajuste casi seguro. |
| What to build · complejidad | `Chart@maxExitConditions` | 3 | 1 | Máximo 1-2: una salida por regla sencilla es más robusta. |
| What to build · complejidad | `Chart@maxExitTypes` | 5 | 3 | El original pedía hasta 5 con sólo 3 tipos activos. |
| What to build · complejidad | `Chart@minPeriod` | 4 | 20 | 20-250 días (1 mes-1 año). Máximo 2 condiciones: con ~8 operaciones/año cada grado de libertad extra es sobreajuste casi seguro. |
| What to build · complejidad | `Chart@maxPeriod` | 200 | 250 | 20-250 días (1 mes-1 año). Máximo 2 condiciones: con ~8 operaciones/año cada grado de libertad extra es sobreajuste casi seguro. |
| What to build · SL/PT | `MinSLATRMultiple` | 1 | 2.5 | Rango de SL del estilo: 2.5-6.0 ATR. |
| What to build · SL/PT | `MaxSLATRMultiple` | 3 | 6 | Rango de SL del estilo: 2.5-6.0 ATR. |
| What to build · SL/PT | `PTRequired` | true | false | Objetivo opcional: el estilo sale por trailing/tiempo/fin de día. |
| What to build · SL/PT | `MinPTATRMultiple` | 2 | 6 | Rango de PT: 6.0-12.0 ATR. |
| What to build · SL/PT | `MaxPTATRMultiple` | 5 | 12 | Rango de PT: 6.0-12.0 ATR. |
| What to build · SL/PT | `LimitSLPTRRR` | true | false | Sin límite R:R: el PT es opcional y la salida principal es otra. |
| Genetic options | `PopulationSize` | 5 | 50 | 5-15 individuos por isla es demasiado poco para que el cruce explore; 30-50 es un mínimo práctico. |
| Genetic options | `MaxGenerations` | 10 | 30 | Con 10 generaciones la evolución apenas actúa (y el reinicio por estancamiento a 30 nunca saltaba). |
| Genetic options | `Islands` | 5 | 4 | 4 islas: diversidad suficiente con menos coste. |
| Genetic options | `CrossoverProbability` | 46 | 80 | 46 % es bajo para un AG; 70-90 % es lo habitual (supuesto de práctica general, no de SQX). |
| Genetic options | `MutationProbability` | 35 | 30 | Algo menor para no destruir buenas soluciones. |
| Genetic options | `MigrationModulo` | 5 | 10 | Migrar cada 10 generaciones (con 30-40 generaciones). |
| Genetic options | `MigrationRate` | 6 | 10 | 6 % de 5 individuos = 0,3: la migración original era nula en la práctica. |
| Genetic options | `EvoRestartOnStagnation@generations` | 30 | 15 | Debe ser menor que MaxGenerations para poder actuar. |
| Genetic options | `BuildMode/Conditions (población inicial)` | ReturnDDRatio(IS) >= 5; AvgBarsInTrade(IS) >= 2; NumberOfTrades(IS) >= 250; WinningPct(IS) >= 35 | ReturnDDRatio(IS) >= 1.88; AvgBarsInTrade(IS) >= 5; NumberOfTrades(IS) >= 33; WinningPct(IS) >= 25 | Misma lógica del autor (≈60 % del Ret/DD final, ≈83 % de las operaciones, -5 puntos de acierto) con los umbrales del estilo. |
| Ranking | `Rankings/Conditions (filtros)` | AvgBarsInTrade(IS) >= 2; ReturnDDRatio(IS) >= 8; NumberOfTrades(IS) >= 300; WinningPct(IS) >= 40 | NumberOfTrades(IS) >= 40; ReturnDDRatio(IS) >= 3; WinningPct(IS) >= 30; ProfitFactor(IS) >= 1.5; AvgBarsInTrade(IS) >= 5 | Umbrales del estilo (frecuencia, acierto típico, Ret/DD) + exigencia en el tramo de validación OOS, que el original no tenía. |
| Ranking | `FitnessCriteria/Settings/Ranking` | type="ReturnDDRatio" | Weighted: ReturnDDRatio (peso 2, max), Stability (peso 1, max) | Ret/DD + estabilidad; SQN es poco fiable con <100 operaciones. |
| Data | `Setup/Chart@timeframe` | H1 | D1 | Timeframe del estilo Position. |
| Data | `Setup@slippage` | 0 | 0.5 | D1 entra a la apertura del día (a menudo tras gap): 0,5 pips conservador. |
| Cross checks | `RetestOnAdditionalMarkets/Setup@timeframe` | H1 | D1 | Coherencia si se activa (sigue desactivado). |
| Building blocks | `Bloques activos · signals` | 146 activos | 12 activos: ADXHigher(w1), BarOpensAboveHighestAfterOpenBelow(w3), IchimokuKumoBreakoutBullish(w1), KAMARising(w1), LinRegRising(w1), MABarClosesAbove(w2), MACDMainCrossAboveZero(w1), MACDMainHigherZero(w1), MARising(w2), ROCAboveLevel(w2), ROCRising(w1), SuperTrendUPTrend(w1) | Momentum sin niveles absolutos (ROC en %, MACD vs 0, medias, máximos de 20-250 días). Se eliminan osciladores: no aportan nada a un horizonte de meses. |
| Building blocks | `Bloques activos · indicators` | 29 activos | 17 activos: CrossesAbove(w1), CrossesBelow(w1), Indicators.ATR(w1), Indicators.EMA(w1), Indicators.Highest(w2), Indicators.Lowest(w1), Indicators.SMA(w2), IsGreater(w1), IsLower(w1), Prices.Close(w1), Prices.CloseW(w1), Prices.High(w1), Prices.HighM(w1), Prices.HighW(w1), Prices.Low(w1), Prices.LowM(w1), Prices.LowW(w1) | Momentum sin niveles absolutos (ROC en %, MACD vs 0, medias, máximos de 20-250 días). Se eliminan osciladores: no aportan nada a un horizonte de meses. |
| Building blocks | `Bloques activos · stopLimitBlocks` | 29 activos | 5 activos: Stop/Limit Price Levels.High(w1), Stop/Limit Price Levels.HighM(w1), Stop/Limit Price Levels.HighW(w1), Stop/Limit Price Levels.Highest(w2), Stop/Limit Price Ranges.ATR(w1) | Momentum sin niveles absolutos (ROC en %, MACD vs 0, medias, máximos de 20-250 días). Se eliminan osciladores: no aportan nada a un horizonte de meses. |
| Building blocks | `ROCAboveLevel · Level` | -100..100/0.001 | 0..15/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `ADXHigher · Level` | 20..90/10 | 20..40/5 | Rango acotado al estilo (ver ficha). |
| Order types | `EnterAtMarket@weight` | 1 | 2 | Peso relativo entre tipos de orden. |
| Order types | `EnterAtMarket · ExitAfterBars min` | 5 | 60 | Alineado con el rango de ExitTypes para eliminar la ambigüedad del original (5-20 vs 2-15). |
| Order types | `EnterAtMarket · ExitAfterBars max` | 20 | 250 | Alineado con el rango de ExitTypes. |
| Order types | `EnterAtStop@use` | false | true | Mayoritariamente a mercado; stop opcional válido 1-5 días. |
| Order types | `EnterAtStop · BarsValid min` | 2 | 1 | Mayoritariamente a mercado; stop opcional válido 1-5 días. |
| Order types | `EnterAtStop · BarsValid max` | 10 | 5 | Mayoritariamente a mercado; stop opcional válido 1-5 días. |
| Order types | `EnterAtStop · ExitAfterBars min` | 5 | 60 | Alineado con el rango de ExitTypes para eliminar la ambigüedad del original (5-20 vs 2-15). |
| Order types | `EnterAtStop · ExitAfterBars max` | 20 | 250 | Alineado con el rango de ExitTypes. |
| Exit types | `StopLoss · PctValue` | true | false | Coherencia con SLPTOptions (SLPercent/PTPercent = false). |
| Exit types | `ProfitTarget@use` | true | false | Sin objetivo (dejar correr); trailing de 3-6 ATR como salida principal; salida por regla (p. ej. cierre bajo media) y temporal 3-12 meses. |
| Exit types | `ProfitTarget@probability` | 100 | 30 | Sin objetivo (dejar correr); trailing de 3-6 ATR como salida principal; salida por regla (p. ej. cierre bajo media) y temporal 3-12 meses. |
| Exit types | `ProfitTarget · PctValue` | true | false | Coherencia con SLPTOptions (SLPercent/PTPercent = false). |
| Exit types | `TrailingStop@probability` | 50 | 70 | Sin objetivo (dejar correr); trailing de 3-6 ATR como salida principal; salida por regla (p. ej. cierre bajo media) y temporal 3-12 meses. |
| Exit types | `TrailingStop · FixedValue` | true | false | Valores fijos en pips no son trasladables entre timeframes/símbolos. |
| Exit types | `TrailingStop · ATR mult. min` | 1 | 3 | Sin objetivo (dejar correr); trailing de 3-6 ATR como salida principal; salida por regla (p. ej. cierre bajo media) y temporal 3-12 meses. |
| Exit types | `TrailingStop · ATR mult. max` | 5 | 6 | Sin objetivo (dejar correr); trailing de 3-6 ATR como salida principal; salida por regla (p. ej. cierre bajo media) y temporal 3-12 meses. |
| Exit types | `ExitAfterBars@use` | false | true | Sin objetivo (dejar correr); trailing de 3-6 ATR como salida principal; salida por regla (p. ej. cierre bajo media) y temporal 3-12 meses. |
| Exit types | `ExitAfterBars@probability` | 50 | 30 | Sin objetivo (dejar correr); trailing de 3-6 ATR como salida principal; salida por regla (p. ej. cierre bajo media) y temporal 3-12 meses. |
| Exit types | `ExitAfterBars min` | 2 | 60 | Sin objetivo (dejar correr); trailing de 3-6 ATR como salida principal; salida por regla (p. ej. cierre bajo media) y temporal 3-12 meses. |
| Exit types | `ExitAfterBars max` | 15 | 250 | Sin objetivo (dejar correr); trailing de 3-6 ATR como salida principal; salida por regla (p. ej. cierre bajo media) y temporal 3-12 meses. |
| Exit types | `_ExitRule_@use` | false | true | Salida por condición (cierre bajo media, oscilador en zona neutra...) coherente con el estilo. |
| Notes | `Notes` | <b>Breakout strategies setup</b><div><br></div><div><br></div><div><br></div><div><br></div> | <b>Position Trading (momentum de largo plazo) – Builder de estrategia completa</b><div>Derivado de Estrategia_Build_ConfigInicial_H1_BUY (build 140.2099). Timeframe D1. Ver docs/03 (ficha Position) y docs/04 (checklist).</div><div>NO VALIDADO EN SQX: revisar símbolo, costes, horario del servidor e importación.</div> | Descripción del estilo y advertencias. |
