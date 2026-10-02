# Estrategia_Retest_ConfigInicial_H1_BUY__DayTrading_M15

*Original:* `Estrategia_Retest_ConfigInicial_H1_BUY.cfx` · *Estilo:* Day Trading (ruptura del rango asiático) · *Timeframe:* M15 · *Rol:* Retester de estrategia completa

Tabla generada automáticamente a partir de los cambios aplicados al XML (cada fila es un valor que difiere del original). Estado: **no validado en SQX** (ver docs/04).

| Sección | Parámetro | Valor original | Valor nuevo | Justificación |
|---|---|---|---|---|
| Task | `Task@templateFile` | C:\Users\<usuario>\Desktop\Ventaja_Retest_ConfigInicial_H1_BUY.cfx | Estrategia_Retest_ConfigInicial_H1_BUY__DayTrading_M15.cfx | Ruta local del autor (C:\Users\<usuario>\Desktop\...) sustituida por el nombre del nuevo archivo: no aporta nada y expone el nombre de usuario de Windows. |
| Trading options | `Param key="SignalTimeRangeFrom"` | 5400 | 32400 | Apertura de Londres (servidor UTC+2). |
| Trading options | `Param key="SignalTimeRangeTo"` | 84600 | 68400 | Tras las 19:00 queda poco recorrido intradía. |
| Trading options | `Param key="ExitAtEndOfDay"` | false | true | Definición de day trading: plano al cierre. |
| Trading options | `Param key="EODExitTime"` | 55800 | 81000 | Antes del rollover de las 00:00 servidor. |
| Trading options | `Param key="ExitOnFriday"` | false | true | Sin exposición de fin de semana. |
| Trading options | `Param key="FridayExitTime"` | 82740 | 77400 | Viernes, cierre algo antes. |
| Trading options | `Param key="MaxTradesPerDay"` | 0 | 2 | Una ruptura y, como mucho, un reintento. |
| Trading options | `Param key="MaxDistanceFromMarket"` | false | true | Evita órdenes stop alejadas del precio. |
| Trading options | `Param key="MaxDistancePct"` | 6 | 0.6 | ≈ 90 pips en GBPJPY: cubre rangos asiáticos amplios. |
| Trading options | `Param key="ReservedBars"` | 50 | 120 | ≥ periodo máximo (100). |
| Money management | `FixedAmount · RiskedMoney` | 100 | 50 | Riesgo fijo de 50 sobre 10.000 (0.5 %). Estilos de alta frecuencia: 0,5 % para contener el drawdown en R. |
| Data | `Setup/Chart@timeframe` | H1 | M15 | Timeframe del estilo DayTrading. |
| Data | `Setup@slippage` | 0 | 0.3 | El original usa 0; 0,3 pips por ejecución stop en apertura de Londres. |
| Cross checks | `RetestOnAdditionalMarkets/Setup[1]@timeframe` | H1 | M15 | Coherencia si se activa (sigue desactivado: el original repetía GBPJPY como 'mercado adicional'). |
| Cross checks | `RetestOnAdditionalMarkets/Setup[2]@timeframe` | H1 | M15 | Coherencia si se activa (sigue desactivado: el original repetía GBPJPY como 'mercado adicional'). |
| Ranking | `FitnessCriteria/Settings/Ranking` | type="ReturnDDRatio" | Weighted: ReturnDDRatio (peso 2, max), StagnationPct (peso 1, min) | Mismo criterio que el Builder del estilo. |
| Ranking | `Rankings/Conditions (filtros)` | (ninguna activa) | NetProfit(OOS) > 0; ProfitFactor(OOS) >= 1.1; ReturnDDRatio(Full) >= 7.5; NumberOfTrades(Full) >= 750; DrawdownPct(Full) <= 20 | El original no filtraba nada en el Retest (todas use=false) y no borraba fallidos: se exige OOS 2021-2024 positivo y métricas del periodo completo acordes al estilo. |
| Cross checks | `HigherPrecision · condición NumberOfTrades` | false | true | Activada: además del OOS ≥ 0, el nº de operaciones y el DD no deben degradarse con tick real. |
| Cross checks | `HigherPrecision · condición DrawdownPct` | false | true | Activada: además del OOS ≥ 0, el nº de operaciones y el DD no deben degradarse con tick real. |
| Cross checks | `MC · RandomizeSpread Min` | 1 | 2 | Desde el spread base (el original bajaba a 1, optimista). |
| Cross checks | `MC · RandomizeSpread Max` | 3 | 4 | Hasta 2x-4x el spread base según el estilo. |
| Cross checks | `MC · RandomizeSlippage@use` | false | true | El original no estresaba el deslizamiento. |
| Cross checks | `MC · RandomizeSlippage Max` | 5.0 | 0.5 | Rango de deslizamiento del estilo (pips). |
| Cross checks | `MC · NumberOfSimulations` | 1000 | 300 | 1000 simulaciones con backtest completo es muy costoso; 200-500 bastan para percentiles 95 %. |
| Cross checks | `MC · NetProfit nivel de confianza` | 100 | 95 | 100 = el peor de N simulaciones: depende de N y de un único caso extremo; 95 es estable. |
| Cross checks | `MC · NetProfit muestra` | 10 | 127 | Muestra completa (MCUseFullSample=true). |
| Cross checks | `MC · condición DrawdownPct@use` | false | true | Activada: el DD al 95 % no debe dispararse respecto al original. |
| Cross checks | `MC · DD nivel de confianza` | 80 | 95 | Coherente con la condición de beneficio. |
| Cross checks | `MC · DD % del original` | 200 | 150 | DD al 95 % ≤ 150 % del DD original (200 % del original es demasiado permisivo). |
| Cross checks | `MonteCarloManipulation@use` | false | true | Barato (no re-ejecuta backtest) y mide el riesgo de secuencia. |
| Cross checks | `MCManip · RandomizeTradesOrder Method` | exact | resampling | 'exact' sólo permuta (el beneficio neto no cambia); 'resampling' (bootstrap) varía beneficio y DD. |
| Cross checks | `MCManip · referencia de la condición NetProfit` | MonteCarloManipulation | main | Error del original: comparaba MC contra MC (resultType=MonteCarloManipulation); debe ser el resultado principal. |
| Cross checks | `MCManip · nivel de la referencia` | 60 | 50 | La referencia pasa a ser el backtest principal, que no tiene percentiles; 50 es el valor neutro que usan el resto de condiciones. |
| Cross checks | `SPP · MaxTests` | 15000 | 3000 | 15.000 backtests por estrategia es desproporcionado en M5/M15; se ajusta por estilo. |
| Cross checks | `SPP · ProfitOptPct` | 95 | 85 | % de permutaciones rentables exigido; 95 % penaliza en exceso a estilos sensibles a costes. |
| Cross checks | `SPP · Stagnation (pctRatio 70) muestra (izq.)` | 10 | 127 | Inconsistencia del original: comparaba IS (10) contra el original en muestra completa (127). |
| Cross checks | `SPP · ReturnDDRatio (pctRatio 130) muestra (izq.)` | 10 | 127 | Inconsistencia del original: comparaba IS (10) contra el original en muestra completa (127). |
| Cross checks | `SPP · ReturnDDRatio (pctRatio 70) muestra (izq.)` | 10 | 127 | Inconsistencia del original: comparaba IS (10) contra el original en muestra completa (127). |
| Cross checks | `WhatIf@use` | false | true | Mide la dependencia de operaciones extremas. |
| Notes | `Notes` | <b>Breakout strategies setup</b><div><br></div><div><br></div><div><br></div><div><br></div> | <b>Day Trading (ruptura del rango asiático) – Retester de estrategia completa</b><div>Derivado de Estrategia_Retest_ConfigInicial_H1_BUY (build 140.2099). Timeframe M15. Ver docs/03 (ficha DayTrading) y docs/04 (checklist).</div><div>NO VALIDADO EN SQX: revisar símbolo, costes, horario del servidor e importación.</div> | Descripción del estilo y advertencias. |
