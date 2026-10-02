# Estrategia_Build_ConfigInicial_H1_BUY__TrendFollowing_H4

*Original:* `Estrategia_Build_ConfigInicial_H1_BUY.cfx` · *Estilo:* Seguimiento de tendencia (multi-filtro con trailing) · *Timeframe:* H4 · *Rol:* Builder de estrategia completa

Tabla generada automáticamente a partir de los cambios aplicados al XML (cada fila es un valor que difiere del original). Estado: **no validado en SQX** (ver docs/04).

| Sección | Parámetro | Valor original | Valor nuevo | Justificación |
|---|---|---|---|---|
| Task | `Task@templateFile` | C:\Users\<usuario>\Desktop\Estrategia_Build_ConfigInicial_H1_BUY.cfx | Estrategia_Build_ConfigInicial_H1_BUY__TrendFollowing_H4.cfx | Ruta local del autor (C:\Users\<usuario>\Desktop\...) sustituida por el nombre del nuevo archivo: no aporta nada y expone el nombre de usuario de Windows. |
| Trading options | `Param key="LimitTimeRange"` | true | false | Igual que Swing: en H4 la ventana del original sesga señales. |
| Trading options | `Param key="MaxTradesPerDay"` | 0 | 1 | Una entrada diaria como máximo. |
| Trading options | `Param key="MaxDistanceFromMarket"` | false | true | Tope para órdenes stop. |
| Trading options | `Param key="MaxDistancePct"` | 6 | 3 | 3 %: rupturas de canales largos. |
| Trading options | `Param key="ReservedBars"` | 50 | 220 | ≥ periodo máximo (200). |
| What to build | `StrategyType@type` | template | simple | El original dependía de una plantilla .sqx externa (Template_DOW_H1_BUY_1.8.4.sqx) que no viene en el .cfx; en modo 'simple' el archivo funciona por sí solo y la selección de bloques del estilo pasa a determinar la entrada. Para volver al flujo plantilla, ver docs/04 §A.3. |
| What to build | `StrategyType@templateFile` | C:\Users\<usuario>\Documents\StrategyQuant\00 - Temp\Formación\DOWJONES_H1_BUY\Template\Template_DOW_H1_BUY_1.8.4.sqx | SQ3StrategyTemplateExample.sq4 | Valor por defecto (el mismo que Ventaja_Build); en modo 'simple' no se usa. |
| What to build · complejidad | `Chart@minConditions` | 0 | 1 | Entrada generada por el Builder. |
| What to build · complejidad | `Chart@maxConditions` | 0 | 3 | 10-200 velas H4 = 2-33 días. |
| What to build · complejidad | `Chart@maxExitConditions` | 3 | 2 | Máximo 1-2: una salida por regla sencilla es más robusta. |
| What to build · complejidad | `Chart@minExitTypes` | 1 | 2 | Al menos SL + otra salida. |
| What to build · complejidad | `Chart@maxExitTypes` | 5 | 4 | El original pedía hasta 5 con sólo 3 tipos activos. |
| What to build · complejidad | `Chart@minPeriod` | 4 | 10 | 10-200 velas H4 = 2-33 días. |
| What to build · SL/PT | `MinSLATRMultiple` | 1 | 2 | Rango de SL del estilo: 2.0-4.0 ATR. |
| What to build · SL/PT | `MaxSLATRMultiple` | 3 | 4 | Rango de SL del estilo: 2.0-4.0 ATR. |
| What to build · SL/PT | `MinSLATRPeriod` | 20 | 14 | ATR(14-100) en velas H4. |
| What to build · SL/PT | `PTRequired` | true | false | Objetivo opcional: el estilo sale por trailing/tiempo/fin de día. |
| What to build · SL/PT | `MinPTATRMultiple` | 2 | 4 | Rango de PT: 4.0-10.0 ATR. |
| What to build · SL/PT | `MaxPTATRMultiple` | 5 | 10 | Rango de PT: 4.0-10.0 ATR. |
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
| Genetic options | `BuildMode/Conditions (población inicial)` | ReturnDDRatio(IS) >= 5; AvgBarsInTrade(IS) >= 2; NumberOfTrades(IS) >= 250; WinningPct(IS) >= 35 | ReturnDDRatio(IS) >= 2.19; AvgBarsInTrade(IS) >= 5; NumberOfTrades(IS) >= 83; WinningPct(IS) >= 25 | Misma lógica del autor (≈60 % del Ret/DD final, ≈83 % de las operaciones, -5 puntos de acierto) con los umbrales del estilo. |
| Ranking | `Rankings/Conditions (filtros)` | AvgBarsInTrade(IS) >= 2; ReturnDDRatio(IS) >= 8; NumberOfTrades(IS) >= 300; WinningPct(IS) >= 40 | NumberOfTrades(IS) >= 100; ReturnDDRatio(IS) >= 3.5; WinningPct(IS) >= 30; ProfitFactor(IS) >= 1.4; AvgBarsInTrade(IS) >= 5; NetProfit(OOS) > 0; ProfitFactor(OOS) >= 1.05 | Umbrales del estilo (frecuencia, acierto típico, Ret/DD) + exigencia en el tramo de validación OOS, que el original no tenía. |
| Ranking | `FitnessCriteria/Settings/Ranking` | type="ReturnDDRatio" | Weighted: ReturnDDRatio (peso 2, max), StagnationPct (peso 1, min) | El talón de Aquiles del TF son las rachas planas largas: StagnationPct las penaliza. |
| Data | `Setup/Chart@timeframe` | H1 | H4 | Timeframe del estilo TrendFollowing. |
| Data | `Setup@slippage` | 0 | 0.3 | El original usa 0. |
| Data | `OutOfSample/Range` | (sin OOS) | 2019.01.01–2020.12.31 | Nuevo tramo de validación dentro del Builder (el original no tenía OOS y filtraba sólo sobre IS). |
| Cross checks | `RetestOnAdditionalMarkets/Setup@timeframe` | H1 | H4 | Coherencia si se activa (sigue desactivado). |
| Building blocks | `Bloques activos · signals` | 146 activos | 19 activos: ADXHigher(w2), ADXRising(w1), AroonCrossesAbove(w1), BarClosesAboveSuperTrend(w2), BarOpensAboveHighestAfterOpenBelow(w2), DICrossUp(w1), FastKAMAAboveSlowKAMA(w1), FasterHMAIsAboveSlowerHMA(w1), GannHiLoUPTrend(w1), IchimokuKumoBreakoutBullish(w1), IchimokuTenkanKijunCrossBullish(w1), KERaboveLevel(w1), MABarClosesAbove(w1), MACDMainCrossAboveSignal(w1), MACDMainHigherZero(w1), MARising(w1), PSARBarLower(w1), SuperTrendUPTrend(w2), VortexUptrend(w1) | Sólo filtros de dirección/fuerza de tendencia; sin osciladores de sobrecompra/sobreventa (contradicen la tesis). |
| Building blocks | `Bloques activos · indicators` | 29 activos | 15 activos: CrossesAbove(w1), CrossesBelow(w1), Indicators.ATR(w1), Indicators.EMA(w1), Indicators.Highest(w2), Indicators.HullMovingAverage(w1), Indicators.KAMA(w1), Indicators.Lowest(w1), Indicators.SMA(w1), Indicators.SuperTrend(w1), IsGreater(w1), IsLower(w1), Prices.Close(w1), Prices.High(w1), Prices.Low(w1) | Sólo filtros de dirección/fuerza de tendencia; sin osciladores de sobrecompra/sobreventa (contradicen la tesis). |
| Building blocks | `Bloques activos · stopLimitBlocks` | 29 activos | 5 activos: Stop/Limit Price Levels.High(w1), Stop/Limit Price Levels.Highest(w2), Stop/Limit Price Levels.KeltnerChannel(w1), Stop/Limit Price Levels.SuperTrend(w1), Stop/Limit Price Ranges.ATR(w1) | Sólo filtros de dirección/fuerza de tendencia; sin osciladores de sobrecompra/sobreventa (contradicen la tesis). |
| Building blocks | `ADXHigher · Level` | 20..90/10 | 20..40/5 | Rango acotado al estilo (ver ficha). |
| Building blocks | `KERaboveLevel · Level` | 0..0.95/0.05 | 0.3..0.7/0.05 | Rango acotado al estilo (ver ficha). |
| Building blocks | `SuperTrendUPTrend · ATR Mult` | 0.5..10/0.1 | 1.5..5/0.5 | Rango acotado al estilo (ver ficha). |
| Building blocks | `BarClosesAboveSuperTrend · ATR Mult` | 0.5..10/0.1 | 1.5..5/0.5 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Indicators.SuperTrend · ATR Mult` | 0.5..10/0.1 | 1.5..5/0.5 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Stop/Limit Price Levels.SuperTrend · ATR Mult` | 0.5..10/0.1 | 1.5..5/0.5 | Rango acotado al estilo (ver ficha). |
| Order types | `EnterAtMarket@weight` | 1 | 2 | Peso relativo entre tipos de orden. |
| Order types | `EnterAtStop@use` | false | true | A mercado con confirmación o stop sobre máximo reciente. |
| Order types | `EnterAtStop · BarsValid min` | 2 | 1 | A mercado con confirmación o stop sobre máximo reciente. |
| Order types | `EnterAtStop · BarsValid max` | 10 | 4 | A mercado con confirmación o stop sobre máximo reciente. |
| Exit types | `StopLoss · PctValue` | true | false | Coherencia con SLPTOptions (SLPercent/PTPercent = false). |
| Exit types | `ProfitTarget@probability` | 100 | 30 | El trailing (prob. 80 %) es la salida natural; objetivo raro y lejano. |
| Exit types | `ProfitTarget · PctValue` | true | false | Coherencia con SLPTOptions (SLPercent/PTPercent = false). |
| Exit types | `TrailingStop@probability` | 50 | 80 | El trailing (prob. 80 %) es la salida natural; objetivo raro y lejano. |
| Exit types | `TrailingStop · FixedValue` | true | false | Valores fijos en pips no son trasladables entre timeframes/símbolos. |
| Exit types | `TrailingStop · ATR mult. min` | 1 | 2.5 | El trailing (prob. 80 %) es la salida natural; objetivo raro y lejano. |
| Exit types | `_ExitRule_@use` | false | true | Salida por condición (cierre bajo media, oscilador en zona neutra...) coherente con el estilo. |
| Notes | `Notes` | <b>Breakout strategies setup</b><div><br></div><div><br></div><div><br></div><div><br></div> | <b>Seguimiento de tendencia (multi-filtro con trailing) – Builder de estrategia completa</b><div>Derivado de Estrategia_Build_ConfigInicial_H1_BUY (build 140.2099). Timeframe H4. Ver docs/03 (ficha TrendFollowing) y docs/04 (checklist).</div><div>NO VALIDADO EN SQX: revisar símbolo, costes, horario del servidor e importación.</div> | Descripción del estilo y advertencias. |
