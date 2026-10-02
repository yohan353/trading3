# Ventaja_Retest_ConfigInicial_H1_BUY__Scalping_M5_SELL

*Original:* `Ventaja_Retest_ConfigInicial_H1_BUY.cfx` · *Estilo:* Scalping (micro-ruptura en sesión líquida) · *Timeframe:* M5 · *Rol:* Retester de test de ventaja · *Dirección:* SELL

Tabla generada automáticamente a partir de los cambios aplicados al XML (cada fila es un valor que difiere del original). Estado: **no validado en SQX** (ver docs/04).

| Sección | Parámetro | Valor original | Valor nuevo | Justificación |
|---|---|---|---|---|
| Task | `Task@templateFile` | C:\Users\<usuario>\Desktop\Ventaja_Retest_ConfigInicial_H1_BUY.cfx | Ventaja_Retest_ConfigInicial_H1_BUY__Scalping_M5_SELL.cfx | Ruta local del autor (C:\Users\<usuario>\Desktop\...) sustituida por el nombre del nuevo archivo: no aporta nada y expone el nombre de usuario de Windows. |
| Trading options | `Param key="SignalTimeRangeFrom"` | 5400 | 32400 | 09:00 servidor ≈ apertura de Londres (UTC+2). |
| Trading options | `Param key="SignalTimeRangeTo"` | 84600 | 66600 | 18:30 servidor ≈ final del solape Londres-NY. |
| Trading options | `Param key="ExitAtEndOfRange"` | false | true | Un scalper no arrastra posiciones fuera de su ventana. |
| Trading options | `Param key="ExitAtEndOfDay"` | false | true | Red de seguridad: nada abierto al cierre del día. |
| Trading options | `Param key="EODExitTime"` | 55800 | 75600 | Antes del rollover (spreads anchos). |
| Trading options | `Param key="ExitOnFriday"` | false | true | Sin riesgo de gap de fin de semana. |
| Trading options | `Param key="FridayExitTime"` | 82740 | 72000 | Viernes tarde: liquidez decreciente. |
| Trading options | `Param key="MaxTradesPerDay"` | 0 | 6 | Permite varias operaciones/día sin sobre-operar en días de ruido. |
| Trading options | `Param key="MaxDistanceFromMarket"` | false | true | Evita órdenes stop lejos del precio. |
| Trading options | `Param key="MaxDistancePct"` | 6 | 0.3 | 0,3 % ≈ 45 pips en GBPJPY; tope razonable para M5. |
| Trading options | `Param key="ReservedBars"` | 50 | 120 | ≥ periodo máximo (100) para que los indicadores estén calculados. |
| Data | `Setup/Chart@timeframe` | H1 | M5 | Timeframe del estilo Scalping. |
| Data | `Setup@slippage` | 0 | 0.5 | El original usa 0; en M5 un deslizamiento de 0,5 pips por orden stop/mercado es conservador-realista y cambia el signo de muchas estrategias. |
| Cross checks | `RetestOnAdditionalMarkets/Setup[1]@timeframe` | H1 | M5 | Coherencia si se activa (sigue desactivado: el original repetía GBPJPY como 'mercado adicional'). |
| Cross checks | `RetestOnAdditionalMarkets/Setup[2]@timeframe` | H1 | M5 | Coherencia si se activa (sigue desactivado: el original repetía GBPJPY como 'mercado adicional'). |
| Ranking | `FitnessCriteria/Settings/Ranking` | Weighted: Stagnation (peso 1, min) | Weighted: SQN (peso 2, max), StagnationPct (peso 1, min) | Mismo criterio que el Builder del estilo. |
| Ranking | `Rankings/Conditions (filtros)` | (ninguna activa) | NetProfit(OOS) > 0; ProfitFactor(Full) >= 1.1; NumberOfTrades(Full) >= 2920; NumberOfTrades(OOS) >= 850 | El original no filtraba nada en el Retest (todas use=false) y no borraba fallidos: se exige OOS 2021-2024 positivo y métricas del periodo completo acordes al estilo. |
| Cross checks | `HigherPrecision/Precision` | 2 | 3 | Precisión 3 (tick real con spread real): en M5 el spread variable decide el resultado. |
| Cross checks | `HigherPrecision · condición NumberOfTrades` | false | true | Activada: además del OOS ≥ 0, el nº de operaciones y el DD no deben degradarse con tick real. |
| Cross checks | `HigherPrecision · condición DrawdownPct` | false | true | Activada: además del OOS ≥ 0, el nº de operaciones y el DD no deben degradarse con tick real. |
| Cross checks | `MC · RandomizeSpread Min` | 1 | 2 | Desde el spread base (el original bajaba a 1, optimista). |
| Cross checks | `MC · RandomizeSpread Max` | 3 | 4 | Hasta 2x-4x el spread base según el estilo. |
| Cross checks | `MC · RandomizeSlippage@use` | false | true | El original no estresaba el deslizamiento. |
| Cross checks | `MC · RandomizeSlippage Max` | 5.0 | 1 | Rango de deslizamiento del estilo (pips). |
| Cross checks | `MC · NumberOfSimulations` | 1000 | 200 | 1000 simulaciones con backtest completo es muy costoso; 200-500 bastan para percentiles 95 %. |
| Cross checks | `MC · NetProfit nivel de confianza` | 100 | 95 | 100 = el peor de N simulaciones: depende de N y de un único caso extremo; 95 es estable. |
| Cross checks | `MC · NetProfit muestra` | 10 | 127 | Muestra completa (MCUseFullSample=true). |
| Cross checks | `MC · condición DrawdownPct@use` | false | true | Activada: el DD al 95 % no debe dispararse respecto al original. |
| Cross checks | `MC · DD nivel de confianza` | 80 | 95 | Coherente con la condición de beneficio. |
| Cross checks | `MC · DD % del original` | 200 | 150 | DD al 95 % ≤ 150 % del DD original (200 % del original es demasiado permisivo). |
| Cross checks | `MonteCarloManipulation@use` | false | true | Barato (no re-ejecuta backtest) y mide el riesgo de secuencia. |
| Cross checks | `MCManip · RandomizeTradesOrder Method` | exact | resampling | 'exact' sólo permuta (el beneficio neto no cambia); 'resampling' (bootstrap) varía beneficio y DD. |
| Cross checks | `MCManip · referencia de la condición NetProfit` | MonteCarloManipulation | main | Error del original: comparaba MC contra MC (resultType=MonteCarloManipulation); debe ser el resultado principal. |
| Cross checks | `MCManip · nivel de la referencia` | 60 | 50 | La referencia pasa a ser el backtest principal, que no tiene percentiles; 50 es el valor neutro que usan el resto de condiciones. |
| Cross checks | `SPP · MaxTests` | 15000 | 1500 | 15.000 backtests por estrategia es desproporcionado en M5/M15; se ajusta por estilo. |
| Cross checks | `SPP · ProfitOptPct` | 95 | 80 | % de permutaciones rentables exigido; 95 % penaliza en exceso a estilos sensibles a costes. |
| Cross checks | `SPP · Stagnation (pctRatio 70) muestra (izq.)` | 10 | 127 | Inconsistencia del original: comparaba IS (10) contra el original en muestra completa (127). |
| Cross checks | `WhatIf@use` | false | true | Mide la dependencia de operaciones extremas. |
| Notes | `Notes` | <b>Breakout strategies setup</b><div><br></div><div><br></div><div><br></div><div><br></div> | <b>Scalping (micro-ruptura en sesión líquida) – Retester de test de ventaja – SELL</b><div>Derivado de Ventaja_Retest_ConfigInicial_H1_BUY (build 140.2099). Timeframe M5. Ver docs/03 (ficha Scalping) y docs/04 (checklist).</div><div>NO VALIDADO EN SQX: revisar símbolo, costes, horario del servidor e importación.</div> | Descripción del estilo y advertencias. |
