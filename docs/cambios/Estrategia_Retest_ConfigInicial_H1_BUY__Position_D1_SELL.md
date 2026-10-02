# Estrategia_Retest_ConfigInicial_H1_BUY__Position_D1_SELL

*Original:* `Estrategia_Retest_ConfigInicial_H1_BUY.cfx` · *Estilo:* Position Trading (momentum de medio-largo plazo) · *Timeframe:* D1 · *Rol:* Retester de estrategia completa · *Dirección:* SELL

Tabla generada automáticamente a partir de los cambios aplicados al XML (cada fila es un valor que difiere del original). Estado: **no validado en SQX** (ver docs/04).

| Sección | Parámetro | Valor original | Valor nuevo | Justificación |
|---|---|---|---|---|
| Task | `Task@templateFile` | C:\Users\<usuario>\Desktop\Ventaja_Retest_ConfigInicial_H1_BUY.cfx | Estrategia_Retest_ConfigInicial_H1_BUY__Position_D1_SELL.cfx | Ruta local del autor (C:\Users\<usuario>\Desktop\...) sustituida por el nombre del nuevo archivo: no aporta nada y expone el nombre de usuario de Windows. |
| Trading options | `Param key="LimitTimeRange"` | true | false | Con velas D1 (apertura 00:00) la ventana 01:30-23:30 del original podría bloquear todas las señales. |
| Trading options | `Param key="MaxTradesPerDay"` | 0 | 1 | Position: una entrada como máximo. |
| Trading options | `Param key="MaxDistanceFromMarket"` | false | true | Tope de distancia para stops. |
| Trading options | `Param key="MaxDistancePct"` | 6 | 5 | 5 %: rupturas de máximos de 20-250 días. |
| Trading options | `Param key="ReservedBars"` | 50 | 260 | ≥ periodo máximo (250). |
| Data | `Setup/Chart@timeframe` | H1 | D1 | Timeframe del estilo Position. |
| Data | `Setup@slippage` | 0 | 0.5 | D1 entra a la apertura del día (a menudo tras gap): 0,5 pips conservador. |
| Cross checks | `RetestOnAdditionalMarkets/Setup[1]@timeframe` | H1 | D1 | Coherencia si se activa (sigue desactivado: el original repetía GBPJPY como 'mercado adicional'). |
| Cross checks | `RetestOnAdditionalMarkets/Setup[2]@timeframe` | H1 | D1 | Coherencia si se activa (sigue desactivado: el original repetía GBPJPY como 'mercado adicional'). |
| Ranking | `FitnessCriteria/Settings/Ranking` | type="ReturnDDRatio" | Weighted: ReturnDDRatio (peso 2, max), Stability (peso 1, max) | Mismo criterio que el Builder del estilo. |
| Ranking | `Rankings/Conditions (filtros)` | (ninguna activa) | NetProfit(OOS) > 0; ReturnDDRatio(Full) >= 4.5; NumberOfTrades(Full) >= 190; NumberOfTrades(OOS) >= 60; DrawdownPct(Full) <= 25 | El original no filtraba nada en el Retest (todas use=false) y no borraba fallidos: se exige OOS 2021-2024 positivo y métricas del periodo completo acordes al estilo. |
| Cross checks | `HigherPrecision · condición NumberOfTrades` | false | true | Activada: además del OOS ≥ 0, el nº de operaciones y el DD no deben degradarse con tick real. |
| Cross checks | `HigherPrecision · condición DrawdownPct` | false | true | Activada: además del OOS ≥ 0, el nº de operaciones y el DD no deben degradarse con tick real. |
| Cross checks | `MC · RandomizeSpread Min` | 1 | 2 | Desde el spread base (el original bajaba a 1, optimista). |
| Cross checks | `MC · RandomizeSpread Max` | 3 | 4 | Hasta 2x-4x el spread base según el estilo. |
| Cross checks | `MC · RandomizeSlippage@use` | false | true | El original no estresaba el deslizamiento. |
| Cross checks | `MC · RandomizeSlippage Max` | 5.0 | 1 | Rango de deslizamiento del estilo (pips). |
| Cross checks | `MC · RandomizeStartingBar@use` | false | true | Con pocas operaciones el resultado no debe depender de la vela de inicio. |
| Cross checks | `MC · NumberOfSimulations` | 1000 | 500 | 1000 simulaciones con backtest completo es muy costoso; 200-500 bastan para percentiles 95 %. |
| Cross checks | `MC · NetProfit nivel de confianza` | 100 | 95 | 100 = el peor de N simulaciones: depende de N y de un único caso extremo; 95 es estable. |
| Cross checks | `MC · NetProfit muestra` | 10 | 127 | Muestra completa (MCUseFullSample=true). |
| Cross checks | `MC · condición DrawdownPct@use` | false | true | Activada: el DD al 95 % no debe dispararse respecto al original. |
| Cross checks | `MC · DD nivel de confianza` | 80 | 95 | Coherente con la condición de beneficio. |
| Cross checks | `MC · DD % del original` | 200 | 175 | DD al 95 % ≤ 175 % del DD original (200 % del original es demasiado permisivo). |
| Cross checks | `MonteCarloManipulation@use` | false | true | Barato (no re-ejecuta backtest) y mide el riesgo de secuencia. |
| Cross checks | `MCManip · RandomizeTradesOrder Method` | exact | resampling | 'exact' sólo permuta (el beneficio neto no cambia); 'resampling' (bootstrap) varía beneficio y DD. |
| Cross checks | `MCManip · referencia de la condición NetProfit` | MonteCarloManipulation | main | Error del original: comparaba MC contra MC (resultType=MonteCarloManipulation); debe ser el resultado principal. |
| Cross checks | `MCManip · nivel de la referencia` | 60 | 50 | La referencia pasa a ser el backtest principal, que no tiene percentiles; 50 es el valor neutro que usan el resto de condiciones. |
| Cross checks | `SPP · MaxTests` | 15000 | 8000 | 15.000 backtests por estrategia es desproporcionado en M5/M15; se ajusta por estilo. |
| Cross checks | `SPP · DistributionUp` | 20 | 30 | ±% alrededor del valor. |
| Cross checks | `SPP · DistributionDown` | 20 | 30 | ±% alrededor del valor. |
| Cross checks | `SPP · ProfitOptPct` | 95 | 90 | % de permutaciones rentables exigido; 95 % penaliza en exceso a estilos sensibles a costes. |
| Cross checks | `SPP · Stagnation (pctRatio 70) muestra (izq.)` | 10 | 127 | Inconsistencia del original: comparaba IS (10) contra el original en muestra completa (127). |
| Cross checks | `SPP · ReturnDDRatio (pctRatio 130) muestra (izq.)` | 10 | 127 | Inconsistencia del original: comparaba IS (10) contra el original en muestra completa (127). |
| Cross checks | `SPP · ReturnDDRatio (pctRatio 70) muestra (izq.)` | 10 | 127 | Inconsistencia del original: comparaba IS (10) contra el original en muestra completa (127). |
| Cross checks | `WhatIf@use` | false | true | Mide la dependencia de operaciones extremas. |
| Cross checks | `WhatIf · ExcludePctTradesWithBiggestPl@use` | true | false | Estilo de pocas ganancias grandes: se quitan las 2 mejores y 2 peores (no el 5 %, que por diseño destruiría cualquier sistema tendencial). |
| Cross checks | `WhatIf · ExcludePctTradesWithLowestPl@use` | true | false | Estilo de pocas ganancias grandes: se quitan las 2 mejores y 2 peores (no el 5 %, que por diseño destruiría cualquier sistema tendencial). |
| Cross checks | `WhatIf · ExcludeTradesWithBiggestPl@use` | false | true | Estilo de pocas ganancias grandes: se quitan las 2 mejores y 2 peores (no el 5 %, que por diseño destruiría cualquier sistema tendencial). |
| Cross checks | `WhatIf · ExcludeTradesWithLowestPl@use` | false | true | Estilo de pocas ganancias grandes: se quitan las 2 mejores y 2 peores (no el 5 %, que por diseño destruiría cualquier sistema tendencial). |
| Notes | `Notes` | <b>Breakout strategies setup</b><div><br></div><div><br></div><div><br></div><div><br></div> | <b>Position Trading (momentum de medio-largo plazo) – Retester de estrategia completa – SELL</b><div>Derivado de Estrategia_Retest_ConfigInicial_H1_BUY (build 140.2099). Timeframe D1. Ver docs/03 (ficha Position) y docs/04 (checklist).</div><div>NO VALIDADO EN SQX: revisar símbolo, costes, horario del servidor e importación.</div> | Descripción del estilo y advertencias. |
