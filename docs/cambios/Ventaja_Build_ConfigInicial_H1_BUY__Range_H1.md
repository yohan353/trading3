# Ventaja_Build_ConfigInicial_H1_BUY__Range_H1

*Original:* `Ventaja_Build_ConfigInicial_H1_BUY.cfx` · *Estilo:* Trading de rango (reversión a la media en régimen lateral) · *Timeframe:* H1 · *Rol:* Builder de test de ventaja (entrada)

Tabla generada automáticamente a partir de los cambios aplicados al XML (cada fila es un valor que difiere del original). Estado: **no validado en SQX** (ver docs/04).

| Sección | Parámetro | Valor original | Valor nuevo | Justificación |
|---|---|---|---|---|
| Task | `Task@templateFile` | C:\Users\<usuario>\Desktop\Ventaja_Build_ConfigInicial_H1_BUY.cfx | Ventaja_Build_ConfigInicial_H1_BUY__Range_H1.cfx | Ruta local del autor (C:\Users\<usuario>\Desktop\...) sustituida por el nombre del nuevo archivo: no aporta nada y expone el nombre de usuario de Windows. |
| Trading options | `Param key="SignalTimeRangeTo"` | 84600 | 34200 | Sesión asiática: menor drift direccional en FX. |
| Trading options | `Param key="MaxTradesPerDay"` | 0 | 2 | Evita promediar a la baja en tendencia. |
| Trading options | `Param key="MaxDistanceFromMarket"` | false | true | Las órdenes límite lejanas casi nunca se ejecutan. |
| Trading options | `Param key="MaxDistancePct"` | 6 | 1 | 1 %. |
| Trading options | `Param key="ReservedBars"` | 50 | 80 | ≥ periodo máximo (60). |
| What to build · complejidad | `Chart@maxExitTypes` | 5 | 1 | Test de ventaja: sólo salida temporal, para medir la entrada aislada. |
| What to build · complejidad | `Chart@minPeriod` | 4 | 5 | 5-60 velas H1: la reversión a la media es un fenómeno de corto plazo. |
| What to build · complejidad | `Chart@maxPeriod` | 200 | 60 | 5-60 velas H1: la reversión a la media es un fenómeno de corto plazo. |
| Genetic options | `PopulationSize` | 15 | 40 | 5-15 individuos por isla es demasiado poco para que el cruce explore; 30-50 es un mínimo práctico. |
| Genetic options | `MaxGenerations` | 10 | 40 | Con 10 generaciones la evolución apenas actúa (y el reinicio por estancamiento a 30 nunca saltaba). |
| Genetic options | `Islands` | 5 | 4 | 4 islas: diversidad suficiente con menos coste. |
| Genetic options | `CrossoverProbability` | 46 | 80 | 46 % es bajo para un AG; 70-90 % es lo habitual (supuesto de práctica general, no de SQX). |
| Genetic options | `MutationProbability` | 35 | 30 | Algo menor para no destruir buenas soluciones. |
| Genetic options | `MigrationModulo` | 5 | 10 | Migrar cada 10 generaciones (con 30-40 generaciones). |
| Genetic options | `MigrationRate` | 6 | 10 | 6 % de 5 individuos = 0,3: la migración original era nula en la práctica. |
| Genetic options | `EvoRestartOnStagnation@generations` | 30 | 15 | Debe ser menor que MaxGenerations para poder actuar. |
| Genetic options | `BuildMode/Conditions (población inicial)` | ReturnDDRatio(IS) >= 2; AvgBarsInTrade(IS) >= 2; NumberOfTrades(IS) >= 250; WinningPct(IS) >= 35 | ReturnDDRatio(IS) >= 1; AvgBarsInTrade(IS) >= 2; NumberOfTrades(IS) >= 207; WinningPct(IS) >= 45 | Misma lógica del autor (≈60 % del Ret/DD final, ≈83 % de las operaciones, -5 puntos de acierto) con los umbrales del estilo. |
| Ranking | `Rankings/Conditions (filtros)` | AvgBarsInTrade(IS) >= 2; ReturnDDRatio(IS) >= 4; NumberOfTrades(IS) >= 300; WinningPct(IS) >= 40 | NumberOfTrades(IS) >= 250; ReturnDDRatio(IS) >= 2; WinningPct(IS) >= 50; ProfitFactor(IS) >= 1.15; AvgBarsInTrade(IS) >= 2; NetProfit(OOS) > 0 | Umbrales del estilo (frecuencia, acierto típico, Ret/DD) + exigencia en el tramo de validación OOS, que el original no tenía. Test de ventaja: Ret/DD a la mitad, PF mínimo 1,15. |
| Ranking | `FitnessCriteria/Settings/Ranking` | Weighted: Stagnation (peso 1, min) | Weighted: SQN (peso 2, max), StagnationPct (peso 1, min) | SQN mide la calidad estadística de la entrada (expectativa/desviación·√N); el original optimizaba sólo 'Stagnation', que ignora el beneficio. |
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
| Order types | `EnterAtLimit · ExitAfterBars min` | 5 | 3 | Alineado con el rango de ExitTypes para eliminar la ambigüedad del original (5-20 vs 2-15). |
| Order types | `EnterAtLimit · ExitAfterBars max` | 20 | 24 | Alineado con el rango de ExitTypes. |
| Order types | `EnterAtMarket · ExitAfterBars min` | 5 | 3 | Alineado con el rango de ExitTypes para eliminar la ambigüedad del original (5-20 vs 2-15). |
| Order types | `EnterAtMarket · ExitAfterBars max` | 20 | 24 | Alineado con el rango de ExitTypes. |
| Exit types | `ExitAfterBars@probability` | 50 | 100 | Explícito: es la única salida (el original ponía 50 y dependía de minExitTypes=1). |
| Exit types | `ExitAfterBars min` | 2 | 3 | Test de ventaja: salida por tiempo 3-24 h. |
| Exit types | `ExitAfterBars max` | 15 | 24 | Test de ventaja: salida por tiempo 3-24 h. |
| Notes | `Notes` | <b>Breakout strategies setup</b><div><br></div><div><br></div><div><br></div><div><br></div> | <b>Trading de rango (reversión a la media en régimen lateral) – Builder de test de ventaja (entrada)</b><div>Derivado de Ventaja_Build_ConfigInicial_H1_BUY (build 140.2099). Timeframe H1. Ver docs/03 (ficha Range) y docs/04 (checklist).</div><div>NO VALIDADO EN SQX: revisar símbolo, costes, horario del servidor e importación.</div> | Descripción del estilo y advertencias. |
