# Estrategia_Build_ConfigInicial_H1_BUY__Range_H1

*Original:* `Estrategia_Build_ConfigInicial_H1_BUY.cfx` · *Estilo:* Trading de rango (reversión a la media en régimen lateral) · *Timeframe:* H1 · *Rol:* Builder de estrategia completa

Tabla generada automáticamente a partir de los cambios aplicados al XML (cada fila es un valor que difiere del original). Estado: **no validado en SQX** (ver docs/04).

| Sección | Parámetro | Valor original | Valor nuevo | Justificación |
|---|---|---|---|---|
| Task | `Task@templateFile` | C:\Users\<usuario>\Desktop\Estrategia_Build_ConfigInicial_H1_BUY.cfx | Estrategia_Build_ConfigInicial_H1_BUY__Range_H1.cfx | Ruta local del autor (C:\Users\<usuario>\Desktop\...) sustituida por el nombre del nuevo archivo: no aporta nada y expone el nombre de usuario de Windows. |
| Trading options | `Param key="SignalTimeRangeTo"` | 84600 | 34200 | Sesión asiática: menor drift direccional en FX. |
| Trading options | `Param key="MaxTradesPerDay"` | 0 | 2 | Evita promediar a la baja en tendencia. |
| Trading options | `Param key="MaxDistanceFromMarket"` | false | true | Las órdenes límite lejanas casi nunca se ejecutan. |
| Trading options | `Param key="MaxDistancePct"` | 6 | 1 | 1 %. |
| Trading options | `Param key="ReservedBars"` | 50 | 80 | ≥ periodo máximo (60). |
| What to build | `StrategyType@type` | template | simple | El original dependía de una plantilla .sqx externa (Template_DOW_H1_BUY_1.8.4.sqx) que no viene en el .cfx; en modo 'simple' el archivo funciona por sí solo y la selección de bloques del estilo pasa a determinar la entrada. Para volver al flujo plantilla, ver docs/04 §A.3. |
| What to build | `StrategyType@templateFile` | C:\Users\<usuario>\Documents\StrategyQuant\00 - Temp\Formación\DOWJONES_H1_BUY\Template\Template_DOW_H1_BUY_1.8.4.sqx | SQ3StrategyTemplateExample.sq4 | Valor por defecto (el mismo que Ventaja_Build); en modo 'simple' no se usa. |
| What to build · complejidad | `Chart@minConditions` | 0 | 1 | Entrada generada por el Builder. |
| What to build · complejidad | `Chart@maxConditions` | 0 | 3 | 5-60 velas H1: la reversión a la media es un fenómeno de corto plazo. |
| What to build · complejidad | `Chart@maxExitConditions` | 3 | 2 | Máximo 1-2: una salida por regla sencilla es más robusta. |
| What to build · complejidad | `Chart@minExitTypes` | 1 | 2 | Al menos SL + otra salida. |
| What to build · complejidad | `Chart@maxExitTypes` | 5 | 4 | El original pedía hasta 5 con sólo 3 tipos activos. |
| What to build · complejidad | `Chart@minPeriod` | 4 | 5 | 5-60 velas H1: la reversión a la media es un fenómeno de corto plazo. |
| What to build · complejidad | `Chart@maxPeriod` | 200 | 60 | 5-60 velas H1: la reversión a la media es un fenómeno de corto plazo. |
| What to build · SL/PT | `MinSLATRMultiple` | 1 | 1.5 | Rango de SL del estilo: 1.5-3.0 ATR. |
| What to build · SL/PT | `MinSLATRPeriod` | 20 | 14 | ATR(14-60) en velas H1. |
| What to build · SL/PT | `MaxSLATRPeriod` | 100 | 60 | ATR(14-60) en velas H1. |
| What to build · SL/PT | `MinPTATRMultiple` | 2 | 0.8 | Rango de PT: 0.8-2.0 ATR. |
| What to build · SL/PT | `MaxPTATRMultiple` | 5 | 2 | Rango de PT: 0.8-2.0 ATR. |
| What to build · SL/PT | `MinPTATRPeriod` | 20 | 14 | ATR(14-60). |
| What to build · SL/PT | `MaxPTATRPeriod` | 100 | 60 | ATR(14-60). |
| What to build · SL/PT | `LimitSLPTRRRFrom` | 100 | 40 | PT = 40-120 % del SL. |
| What to build · SL/PT | `LimitSLPTRRRTo` | 500 | 120 | PT = 40-120 % del SL. |
| Genetic options | `PopulationSize` | 5 | 40 | 5-15 individuos por isla es demasiado poco para que el cruce explore; 30-50 es un mínimo práctico. |
| Genetic options | `MaxGenerations` | 10 | 40 | Con 10 generaciones la evolución apenas actúa (y el reinicio por estancamiento a 30 nunca saltaba). |
| Genetic options | `Islands` | 5 | 4 | 4 islas: diversidad suficiente con menos coste. |
| Genetic options | `CrossoverProbability` | 46 | 80 | 46 % es bajo para un AG; 70-90 % es lo habitual (supuesto de práctica general, no de SQX). |
| Genetic options | `MutationProbability` | 35 | 30 | Algo menor para no destruir buenas soluciones. |
| Genetic options | `MigrationModulo` | 5 | 10 | Migrar cada 10 generaciones (con 30-40 generaciones). |
| Genetic options | `MigrationRate` | 6 | 10 | 6 % de 5 individuos = 0,3: la migración original era nula en la práctica. |
| Genetic options | `EvoRestartOnStagnation@generations` | 30 | 15 | Debe ser menor que MaxGenerations para poder actuar. |
| Genetic options | `BuildMode/Conditions (población inicial)` | ReturnDDRatio(IS) >= 5; AvgBarsInTrade(IS) >= 2; NumberOfTrades(IS) >= 250; WinningPct(IS) >= 35 | ReturnDDRatio(IS) >= 2.5; AvgBarsInTrade(IS) >= 2; NumberOfTrades(IS) >= 207; WinningPct(IS) >= 50 | Misma lógica del autor (≈60 % del Ret/DD final, ≈83 % de las operaciones, -5 puntos de acierto) con los umbrales del estilo. |
| Ranking | `Rankings/Conditions (filtros)` | AvgBarsInTrade(IS) >= 2; ReturnDDRatio(IS) >= 8; NumberOfTrades(IS) >= 300; WinningPct(IS) >= 40 | NumberOfTrades(IS) >= 250; ReturnDDRatio(IS) >= 4; WinningPct(IS) >= 55; ProfitFactor(IS) >= 1.25; AvgBarsInTrade(IS) >= 2; NetProfit(OOS) > 0; ProfitFactor(OOS) >= 1.1 | Umbrales del estilo (frecuencia, acierto típico, Ret/DD) + exigencia en el tramo de validación OOS, que el original no tenía. |
| Ranking | `FitnessCriteria/Settings/Ranking` | type="ReturnDDRatio" | Weighted: ProfitFactor (peso 1, max), ReturnDDRatio (peso 2, max) | PF alto es imprescindible en reversión (pérdidas medias > ganancias medias). |
| Money management | `FixedAmount · RiskedMoney` | 100 | 75 | Riesgo fijo de 75 sobre 10.000 (0.75 %). Estilos de alta frecuencia: 0,5 % para contener el drawdown en R. |
| Data | `Setup@slippage` | 0 | 0.3 | El original usa 0. |
| Data | `OutOfSample/Range` | (sin OOS) | 2019.01.01–2020.12.31 | Nuevo tramo de validación dentro del Builder (el original no tenía OOS y filtraba sólo sobre IS). |
| Building blocks | `Bloques activos · signals` | 146 activos | 16 activos: ADXFalling(w1), ADXLower(w2), BBBarClosesBelowDown(w1), BBBarOpensAboveDownAfterOpenBelow(w2), BarOpensAboveLowestAfterOpenBelow(w1), CCICrossUp(w1), DEMCrossUp(w1), KCBarClosesBelowLower(w1), KCBarOpensAboveLowerAfterOpenBelow(w2), KERbelowLevel(w2), LaguerreRSICrossUP(w1), RSICrossUp(w1), RSILower(w1), StochFastKCrossUp(w1), StochSlowDCrossUp(w1), WPRCrossUp(w1) | Osciladores sólo en zona de sobreventa (sus rangos 0-100 originales permitían 'comprar en sobrecompra'); filtros de régimen lateral (ADX bajo, KER bajo). |
| Building blocks | `Bloques activos · indicators` | 29 activos | 18 activos: CrossesAbove(w1), CrossesBelow(w1), Indicators.BollingerBands(w1), Indicators.CCI(w1), Indicators.EMA(w1), Indicators.Highest(w1), Indicators.KeltnerChannel(w1), Indicators.Lowest(w1), Indicators.RSI(w1), Indicators.SMA(w1), Indicators.Stochastic(w1), Indicators.WilliamsPR(w1), IsGreater(w1), IsLower(w1), IsLowerCount(w1), Prices.Close(w1), Prices.Low(w1), Prices.Open(w1) | Osciladores sólo en zona de sobreventa (sus rangos 0-100 originales permitían 'comprar en sobrecompra'); filtros de régimen lateral (ADX bajo, KER bajo). |
| Building blocks | `Bloques activos · stopLimitBlocks` | 29 activos | 9 activos: Stop/Limit Price Levels.BollingerBands(w2), Stop/Limit Price Levels.EMA(w1), Stop/Limit Price Levels.KeltnerChannel(w2), Stop/Limit Price Levels.Low(w1), Stop/Limit Price Levels.Lowest(w1), Stop/Limit Price Levels.SMA(w1), Stop/Limit Price Ranges.ATR(w2), Stop/Limit Price Ranges.BBRange(w1), Stop/Limit Price Ranges.BarRange(w1) | Osciladores sólo en zona de sobreventa (sus rangos 0-100 originales permitían 'comprar en sobrecompra'); filtros de régimen lateral (ADX bajo, KER bajo). |
| Building blocks | `RSICrossUp · Level` | 0..100/5 | 15..40/5 | Rango acotado al estilo (ver ficha). |
| Building blocks | `RSILower · Level` | 0..100/5 | 20..40/5 | Rango acotado al estilo (ver ficha). |
| Building blocks | `StochSlowDCrossUp · Level` | 0..100/5 | 10..30/5 | Rango acotado al estilo (ver ficha). |
| Building blocks | `StochFastKCrossUp · Level` | 0..100/5 | 10..30/5 | Rango acotado al estilo (ver ficha). |
| Building blocks | `WPRCrossUp · Level` | -100..0/5 | -95..-75/5 | Rango acotado al estilo (ver ficha). |
| Building blocks | `CCICrossUp · Level` | -120..120/5 | -150..-80/5 | Rango acotado al estilo (ver ficha). |
| Building blocks | `LaguerreRSICrossUP · Level` | 0.05..0.95/0.05 | 0.05..0.3/0.05 | Rango acotado al estilo (ver ficha). |
| Building blocks | `DEMCrossUp · Level` | 0..1/0.1 | 0.1..0.3/0.1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `ADXLower · Level` | 20..90/10 | 15..30/5 | Rango acotado al estilo (ver ficha). |
| Building blocks | `KERbelowLevel · Level` | 0.05..1/0.05 | 0.1..0.4/0.05 | Rango acotado al estilo (ver ficha). |
| Order types | `EnterAtLimit@use` | false | true | Límite bajo la banda/mínimo: se compra el exceso, no la ruptura. |
| Order types | `EnterAtLimit@weight` | 1 | 2 | Peso relativo entre tipos de orden. |
| Order types | `EnterAtLimit · BarsValid min` | 2 | 1 | Límite bajo la banda/mínimo: se compra el exceso, no la ruptura. |
| Order types | `EnterAtLimit · BarsValid max` | 10 | 5 | Límite bajo la banda/mínimo: se compra el exceso, no la ruptura. |
| Order types | `EnterAtLimit · ExitAfterBars max` | 20 | 30 | Alineado con el rango de ExitTypes. |
| Order types | `EnterAtMarket · ExitAfterBars max` | 20 | 30 | Alineado con el rango de ExitTypes. |
| Exit types | `StopLoss · PctValue` | true | false | Coherencia con SLPTOptions (SLPercent/PTPercent = false). |
| Exit types | `ProfitTarget · PctValue` | true | false | Coherencia con SLPTOptions (SLPercent/PTPercent = false). |
| Exit types | `TrailingStop@use` | true | false | El estilo no usa trailing. |
| Exit types | `ExitAfterBars@use` | false | true | Objetivo corto obligatorio (PT 40-120 % del SL) y alta tasa de acierto; salida temporal: si no revierte en 5-30 h la tesis falló. |
| Exit types | `ExitAfterBars min` | 2 | 5 | Objetivo corto obligatorio (PT 40-120 % del SL) y alta tasa de acierto; salida temporal: si no revierte en 5-30 h la tesis falló. |
| Exit types | `ExitAfterBars max` | 15 | 30 | Objetivo corto obligatorio (PT 40-120 % del SL) y alta tasa de acierto; salida temporal: si no revierte en 5-30 h la tesis falló. |
| Exit types | `_ExitRule_@use` | false | true | Salida por condición (cierre bajo media, oscilador en zona neutra...) coherente con el estilo. |
| Notes | `Notes` | <b>Breakout strategies setup</b><div><br></div><div><br></div><div><br></div><div><br></div> | <b>Trading de rango (reversión a la media en régimen lateral) – Builder de estrategia completa</b><div>Derivado de Estrategia_Build_ConfigInicial_H1_BUY (build 140.2099). Timeframe H1. Ver docs/03 (ficha Range) y docs/04 (checklist).</div><div>NO VALIDADO EN SQX: revisar símbolo, costes, horario del servidor e importación.</div> | Descripción del estilo y advertencias. |
