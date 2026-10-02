# Estrategia_Build_ConfigInicial_H1_BUY__Swing_H4

*Original:* `Estrategia_Build_ConfigInicial_H1_BUY.cfx` · *Estilo:* Swing Trading (ruptura de consolidación multi-día) · *Timeframe:* H4 · *Rol:* Builder de estrategia completa

Tabla generada automáticamente a partir de los cambios aplicados al XML (cada fila es un valor que difiere del original). Estado: **no validado en SQX** (ver docs/04).

| Sección | Parámetro | Valor original | Valor nuevo | Justificación |
|---|---|---|---|---|
| Task | `Task@templateFile` | C:\Users\<usuario>\Desktop\Estrategia_Build_ConfigInicial_H1_BUY.cfx | Estrategia_Build_ConfigInicial_H1_BUY__Swing_H4.cfx | Ruta local del autor (C:\Users\<usuario>\Desktop\...) sustituida por el nombre del nuevo archivo: no aporta nada y expone el nombre de usuario de Windows. |
| Trading options | `Param key="LimitTimeRange"` | true | false | En H4 la ventana 01:30-23:30 excluiría la vela de las 00:00 (1/6 de las señales) sin motivo de estilo. |
| Trading options | `Param key="MaxTradesPerDay"` | 0 | 1 | Swing: como mucho una entrada diaria. |
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
| Genetic options | `PopulationSize` | 5 | 50 | 5-15 individuos por isla es demasiado poco para que el cruce explore; 30-50 es un mínimo práctico. |
| Genetic options | `MaxGenerations` | 10 | 40 | Con 10 generaciones la evolución apenas actúa (y el reinicio por estancamiento a 30 nunca saltaba). |
| Genetic options | `Islands` | 5 | 4 | 4 islas: diversidad suficiente con menos coste. |
| Genetic options | `CrossoverProbability` | 46 | 80 | 46 % es bajo para un AG; 70-90 % es lo habitual (supuesto de práctica general, no de SQX). |
| Genetic options | `MutationProbability` | 35 | 30 | Algo menor para no destruir buenas soluciones. |
| Genetic options | `MigrationModulo` | 5 | 10 | Migrar cada 10 generaciones (con 30-40 generaciones). |
| Genetic options | `MigrationRate` | 6 | 10 | 6 % de 5 individuos = 0,3: la migración original era nula en la práctica. |
| Genetic options | `EvoRestartOnStagnation@generations` | 30 | 15 | Debe ser menor que MaxGenerations para poder actuar. |
| Genetic options | `BuildMode/Conditions (población inicial)` | ReturnDDRatio(IS) >= 5; AvgBarsInTrade(IS) >= 2; NumberOfTrades(IS) >= 250; WinningPct(IS) >= 35 | ReturnDDRatio(IS) >= 2.5; AvgBarsInTrade(IS) >= 3; NumberOfTrades(IS) >= 124; WinningPct(IS) >= 33 | Misma lógica del autor (≈60 % del Ret/DD final, ≈83 % de las operaciones, -5 puntos de acierto) con los umbrales del estilo. |
| Ranking | `Rankings/Conditions (filtros)` | AvgBarsInTrade(IS) >= 2; ReturnDDRatio(IS) >= 8; NumberOfTrades(IS) >= 300; WinningPct(IS) >= 40 | NumberOfTrades(IS) >= 150; ReturnDDRatio(IS) >= 4; WinningPct(IS) >= 38; ProfitFactor(IS) >= 1.3; AvgBarsInTrade(IS) >= 3; NetProfit(OOS) > 0; ProfitFactor(OOS) >= 1.1 | Umbrales del estilo (frecuencia, acierto típico, Ret/DD) + exigencia en el tramo de validación OOS, que el original no tenía. |
| Ranking | `FitnessCriteria/Settings/Ranking` | type="ReturnDDRatio" | Weighted: ReturnDDRatio (peso 2, max), Stability (peso 1, max) | Ret/DD + estabilidad de la curva: un swing con 30 operaciones/año necesita curvas regulares. |
| Data | `Setup/Chart@timeframe` | H1 | H4 | Timeframe del estilo Swing. |
| Data | `Setup@slippage` | 0 | 0.3 | El original usa 0; 0,3 pips es conservador en H4. |
| Data | `OutOfSample/Range` | (sin OOS) | 2019.01.01–2020.12.31 | Nuevo tramo de validación dentro del Builder (el original no tenía OOS y filtraba sólo sobre IS). |
| Cross checks | `RetestOnAdditionalMarkets/Setup@timeframe` | H1 | H4 | Coherencia si se activa (sigue desactivado). |
| Building blocks | `Bloques activos · signals` | 146 activos | 14 activos: ADXHigher(w1), ADXRising(w1), ATRRising(w1), BBBarOpensAboveUpAfterOpenBelow(w1), BBUpperRising(w1), BarOpensAboveHighestAfterOpenBelow(w3), IchimokuKumoBreakoutBullish(w1), KCBarOpensAboveUpperAfterOpenBelow(w1), KERaboveLevel(w1), LinRegRising(w1), MABarClosesAbove(w1), MARising(w1), RSIHigher(w1), SuperTrendUPTrend(w1) | Ruptura de máximos de N días (Donchian/Bollinger/Keltner/Kumo) filtrada por régimen (ADX, pendiente de medias, eficiencia de Kaufman). |
| Building blocks | `Bloques activos · indicators` | 29 activos | 20 activos: CrossesAbove(w1), CrossesBelow(w1), Indicators.ATR(w1), Indicators.BollingerBands(w1), Indicators.EMA(w1), Indicators.Highest(w2), Indicators.KeltnerChannel(w1), Indicators.Lowest(w1), Indicators.SMA(w1), IsGreater(w1), IsGreaterCount(w1), IsLower(w1), Prices.Close(w1), Prices.High(w1), Prices.HighD(w1), Prices.HighW(w1), Prices.Low(w1), Prices.LowD(w1), Prices.LowW(w1), Prices.Open(w1) | Ruptura de máximos de N días (Donchian/Bollinger/Keltner/Kumo) filtrada por régimen (ADX, pendiente de medias, eficiencia de Kaufman). |
| Building blocks | `Bloques activos · stopLimitBlocks` | 29 activos | 9 activos: Stop/Limit Price Levels.BollingerBands(w1), Stop/Limit Price Levels.High(w1), Stop/Limit Price Levels.HighD(w1), Stop/Limit Price Levels.HighW(w1), Stop/Limit Price Levels.Highest(w3), Stop/Limit Price Levels.KeltnerChannel(w1), Stop/Limit Price Ranges.ATR(w2), Stop/Limit Price Ranges.BBRange(w1), Stop/Limit Price Ranges.BarRange(w1) | Ruptura de máximos de N días (Donchian/Bollinger/Keltner/Kumo) filtrada por régimen (ADX, pendiente de medias, eficiencia de Kaufman). |
| Building blocks | `ADXHigher · Level` | 20..90/10 | 20..40/5 | Rango acotado al estilo (ver ficha). |
| Building blocks | `RSIHigher · Level` | 0..100/5 | 50..70/5 | Rango acotado al estilo (ver ficha). |
| Building blocks | `KERaboveLevel · Level` | 0..0.95/0.05 | 0.2..0.6/0.05 | Rango acotado al estilo (ver ficha). |
| Order types | `EnterAtStop@use` | false | true | Stop válida 8-24 h. |
| Order types | `EnterAtStop@weight` | 1 | 2 | Peso relativo entre tipos de orden. |
| Order types | `EnterAtStop · BarsValid max` | 10 | 6 | Stop válida 8-24 h. |
| Order types | `EnterAtStop · ExitAfterBars min` | 5 | 10 | Alineado con el rango de ExitTypes para eliminar la ambigüedad del original (5-20 vs 2-15). |
| Order types | `EnterAtStop · ExitAfterBars max` | 20 | 40 | Alineado con el rango de ExitTypes. |
| Order types | `EnterAtMarket · ExitAfterBars min` | 5 | 10 | Alineado con el rango de ExitTypes para eliminar la ambigüedad del original (5-20 vs 2-15). |
| Order types | `EnterAtMarket · ExitAfterBars max` | 20 | 40 | Alineado con el rango de ExitTypes. |
| Exit types | `StopLoss · PctValue` | true | false | Coherencia con SLPTOptions (SLPercent/PTPercent = false). |
| Exit types | `ProfitTarget@probability` | 100 | 50 | Stop amplio en ATR, objetivo y trailing opcionales, salida temporal 2-7 días. |
| Exit types | `ProfitTarget · PctValue` | true | false | Coherencia con SLPTOptions (SLPercent/PTPercent = false). |
| Exit types | `TrailingStop · FixedValue` | true | false | Valores fijos en pips no son trasladables entre timeframes/símbolos. |
| Exit types | `TrailingStop · ATR mult. min` | 1 | 2 | Stop amplio en ATR, objetivo y trailing opcionales, salida temporal 2-7 días. |
| Exit types | `TrailingStop · ATR mult. max` | 5 | 4 | Stop amplio en ATR, objetivo y trailing opcionales, salida temporal 2-7 días. |
| Exit types | `MoveSL2BE@use` | false | true | Stop amplio en ATR, objetivo y trailing opcionales, salida temporal 2-7 días. |
| Exit types | `MoveSL2BE@probability` | 50 | 30 | Stop amplio en ATR, objetivo y trailing opcionales, salida temporal 2-7 días. |
| Exit types | `MoveSL2BE · FixedValue` | true | false | Valores fijos en pips no son trasladables entre timeframes/símbolos. |
| Exit types | `MoveSL2BE · ATR mult. max` | 5 | 2 | Stop amplio en ATR, objetivo y trailing opcionales, salida temporal 2-7 días. |
| Exit types | `ExitAfterBars@use` | false | true | Stop amplio en ATR, objetivo y trailing opcionales, salida temporal 2-7 días. |
| Exit types | `ExitAfterBars@probability` | 50 | 30 | Stop amplio en ATR, objetivo y trailing opcionales, salida temporal 2-7 días. |
| Exit types | `ExitAfterBars min` | 2 | 10 | Stop amplio en ATR, objetivo y trailing opcionales, salida temporal 2-7 días. |
| Exit types | `ExitAfterBars max` | 15 | 40 | Stop amplio en ATR, objetivo y trailing opcionales, salida temporal 2-7 días. |
| Exit types | `_ExitRule_@use` | false | true | Salida por condición (cierre bajo media, oscilador en zona neutra...) coherente con el estilo. |
| Exit types | `_ExitRule_@probability` | 50 | 30 | Stop amplio en ATR, objetivo y trailing opcionales, salida temporal 2-7 días. |
| Notes | `Notes` | <b>Breakout strategies setup</b><div><br></div><div><br></div><div><br></div><div><br></div> | <b>Swing Trading (ruptura de consolidación multi-día) – Builder de estrategia completa</b><div>Derivado de Estrategia_Build_ConfigInicial_H1_BUY (build 140.2099). Timeframe H4. Ver docs/03 (ficha Swing) y docs/04 (checklist).</div><div>NO VALIDADO EN SQX: revisar símbolo, costes, horario del servidor e importación.</div> | Descripción del estilo y advertencias. |
