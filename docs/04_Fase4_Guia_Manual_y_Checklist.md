# Fase 4 — Entregables D y E: archivos, guía de aplicación manual y lista de verificación

## D) Qué se entrega

> **Opción entregada: la GUÍA PASO A PASO de esta página es el entregable principal.** No puedo garantizar que
> los `.cfx` abran sin errores en SQX **build 144**: los originales son de la build 140.2099 y no he podido
> ejecutar SQX. Como apoyo se entregan además 64 archivos `.cfx` **experimentales, NO validados en SQX**,
> generados modificando sólo valores de los originales (sin nodos ni atributos nuevos) y verificados
> estáticamente (`docs/validacion/informe_validacion.md`). Si un archivo no carga o SQX avisa de algo,
> aplica los valores a mano con las tablas de abajo, que contienen exactamente lo mismo que los archivos.

Archivos: `configs/<Estilo>/<NombreOriginal>__<Estilo>_<TF>_<BUY|SELL>.cfx` (4 por estilo y dirección × 8 estilos × 2 direcciones = 64). Detalle de cada valor cambiado y su justificación: `docs/cambios/`.

## A.1 Cargar un `.cfx` (vía rápida, experimental)

1. Haz una copia de seguridad de tu proyecto y trabaja en un proyecto personalizado nuevo (p. ej. `Kit_<Estilo>`).
2. Crea una tarea **Build** (para `*_Build_*`) o **Retest** (para `*_Retest_*`).
3. En la tarea, usa la opción de **cargar configuración** (*Load settings/config*, icono de carpeta en la barra de ajustes; el nombre exacto puede variar en la build 144) y elige el `.cfx`.
4. Si SQX muestra un aviso de versión o de símbolo no encontrado, **no lo ignores**: revisa la lista de verificación (E) y, si algo no cuadra, aplica los valores a mano (A.2).
5. Recorre todas las pestañas comparando con las tablas de A.2 antes de pulsar *Start*.

## A.2 Aplicación manual paso a paso

Procedimiento (para cada estilo):

1. Carga el **original** correspondiente (p. ej. `Ventaja_Build_ConfigInicial_H1_BUY.cfx`) en una tarea nueva.
2. Recorre las pestañas en este orden: **What to build → Genetic options → Data → Trading options → Building blocks → Money management → Ranking → Cross checks**, fijando los valores de la columna de tu estilo.
3. En **Building blocks**: desactiva todo (botón de deseleccionar categoría) y activa sólo los bloques de la tabla §3 de la ficha del estilo (docs/03), con sus pesos y rangos específicos. Haz lo mismo con *Order types* y *Exit types*.
4. Guarda la configuración con el nombre `<Original>__<Estilo>_<TF>.cfx`.
5. Repite para los otros 3 archivos del kit y verifica con la lista E.

Los nombres de campo de la interfaz son aproximados (pueden variar entre builds); la columna *Nodo XML* da el nombre exacto del parámetro en el archivo.

Las tablas muestran el kit **BUY**. El kit **SELL** es idéntico salvo dos cosas: (1) *What to build › Trading direction* = **Short only** (`MarketSides@type="short"`); (2) en *Building blocks* se activa el bloque espejo de cada bloque direccional con su peso, y los niveles de osciladores se espejan (RSI/estocástico 100−L, WPR −100−L, CCI y ROC −L, Laguerre/DeMarker 1−L). La lista exacta está en la columna *Espejo SELL* de cada ficha (docs/03 §3).

### A.2.1 `Estrategia_Build` (estrategia completa)

| Pestaña › campo | Nodo XML | Scalping | DayTrading | Swing | Position | TrendFollowing | Range | PriceAction | NewsProxy |
|---|---|---|---|---|---|---|---|---|---|
| **What to build** › Strategy type | `WhatToBuild/StrategyType@type` | simple | simple | simple | simple | simple | simple | simple | simple |
| **What to build** › Trading direction | `WhatToBuild/MarketSides@type` | long | long | long | long | long | long | long | long |
| **What to build** › Entry conditions min–max | `RulesComplexity/Chart@min/maxConditions` | 1–3 | 1–3 | 1–3 | 1–2 | 1–3 | 1–3 | 1–3 | 1–3 |
| **What to build** › Exit conditions min–max | `Chart@min/maxExitConditions` | 1–2 | 1–2 | 1–2 | 1–1 | 1–2 | 1–2 | 1–2 | 1–1 |
| **What to build** › Exit types min–max | `Chart@min/maxExitTypes` | 2–4 | 2–4 | 2–4 | 1–3 | 2–4 | 2–4 | 2–4 | 2–4 |
| **What to build** › Indicator period min–max | `Chart@min/maxPeriod` | 5–100 | 5–100 | 5–120 | 20–250 | 10–250 | 5–60 | 2–50 | 4–48 |
| **What to build** › Shift min–max | `Chart@min/maxShift` | 1–1 | 1–1 | 1–1 | 1–1 | 1–1 | 1–1 | 1–3 | 1–1 |
| **What to build** › Stop Loss | `SLPTOptions/SL*` | obligatorio=true; 1-2.5 × ATR(14-50) | obligatorio=true; 1-2.5 × ATR(14-60) | obligatorio=true; 1.5-3.5 × ATR(14-100) | obligatorio=true; 2.5-5 × ATR(20-100) | obligatorio=true; 2-4 × ATR(14-100) | obligatorio=true; 1.5-3 × ATR(14-60) | obligatorio=true; 1-2.5 × ATR(14-50) | obligatorio=true; 1-2 × ATR(10-40) |
| **What to build** › Profit Target / Risk-Reward | `SLPTOptions/PT*, LimitSLPTRRR*` | obligatorio=true; 1-3 × ATR(14-50); PT=80-250 % del SL | obligatorio=false; 1.5-4 × ATR(14-60) | obligatorio=false; 2-6 × ATR(14-100) | obligatorio=false; 6-12 × ATR(20-100) | obligatorio=false; 4-10 × ATR(14-100) | obligatorio=true; 0.8-2 × ATR(14-60); PT=40-120 % del SL | obligatorio=true; 1.5-4 × ATR(14-50); PT=150-300 % del SL | obligatorio=false; 1.5-4 × ATR(10-40) |
| **Genetic options** › Población / islas / generaciones / cruce / mutación / migración / estancamiento | `BuildMode/*` | población 20 × 4 islas, 30 generaciones, cruce 80 %, mutación 30 %, migración 10 % cada 10, reinicio por estancamiento a 15 | población 25 × 4 islas, 30 generaciones, cruce 80 %, mutación 30 %, migración 10 % cada 10, reinicio por estancamiento a 15 | población 25 × 4 islas, 30 generaciones, cruce 80 %, mutación 30 %, migración 10 % cada 10, reinicio por estancamiento a 15 | población 25 × 4 islas, 30 generaciones, cruce 80 %, mutación 30 %, migración 10 % cada 10, reinicio por estancamiento a 15 | población 25 × 4 islas, 30 generaciones, cruce 80 %, mutación 30 %, migración 10 % cada 10, reinicio por estancamiento a 15 | población 25 × 4 islas, 30 generaciones, cruce 80 %, mutación 30 %, migración 10 % cada 10, reinicio por estancamiento a 15 | población 25 × 4 islas, 30 generaciones, cruce 80 %, mutación 30 %, migración 10 % cada 10, reinicio por estancamiento a 15 | población 20 × 4 islas, 30 generaciones, cruce 80 %, mutación 30 %, migración 10 % cada 10, reinicio por estancamiento a 15 |
| **Genetic options** › Initial population filters | `BuildMode/Conditions` | NumberOfTrades(IS) >= 320 | NumberOfTrades(IS) >= 190 | NumberOfTrades(IS) >= 70 | NumberOfTrades(IS) >= 40 | NumberOfTrades(IS) >= 80 | NumberOfTrades(IS) >= 100 | NumberOfTrades(IS) >= 100 | NumberOfTrades(IS) >= 60 |
| **Data** › Symbol | `Setup/Chart@symbol` | GBPJPY_M1_M1_UTCPlus02 | GBPJPY_M1_M1_UTCPlus02 | GBPJPY_M1_M1_UTCPlus02 | GBPJPY_M1_M1_UTCPlus02 | GBPJPY_M1_M1_UTCPlus02 | GBPJPY_M1_M1_UTCPlus02 | GBPJPY_M1_M1_UTCPlus02 | GBPJPY_M1_M1_UTCPlus02 |
| **Data** › Timeframe | `Setup/Chart@timeframe` | M5 | M15 | H4 | D1 | H1 | H1 | H1 | M15 |
| **Data** › Date from – to | `Setup@dateFrom/dateTo` | 2016.01.04 – 2020.12.31 | 2013.09.30 – 2020.12.31 | 2013.09.30 – 2020.12.31 | 2013.09.30 – 2020.12.31 | 2013.09.30 – 2020.12.31 | 2013.09.30 – 2020.12.31 | 2013.09.30 – 2020.12.31 | 2016.01.04 – 2020.12.31 |
| **Data** › Out of sample | `OutOfSample/Range` | 2019.07.01 – 2020.12.31 | 2019.01.01 – 2020.12.31 | 2019.01.01 – 2020.12.31 | sin OOS | 2019.01.01 – 2020.12.31 | 2019.01.01 – 2020.12.31 | 2019.01.01 – 2020.12.31 | 2019.07.01 – 2020.12.31 |
| **Data** › Precision | `Setup@testPrecision` | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| **Data** › Spread / Slippage | `Chart@spread, Setup@slippage` | 2 / 0.5 | 2 / 0.3 | 2 / 0.3 | 2 / 0.5 | 2 / 0.3 | 2 / 0.3 | 2 / 0.3 | 2 / 1.5 |
| **Trading options** › Limit signals to time range | `LimitTimeRange, SignalTimeRangeFrom/To, ExitAtEndOfRange` | 09:00-18:30 + cierre al final | 09:00-19:00 | sin ventana | sin ventana | 01:30-23:30 | 01:30-09:30 | 01:30-23:30 | 15:00-17:00 |
| **Trading options** › Exit at end of day / on Friday | `ExitAtEndOfDay/EODExitTime, ExitOnFriday/FridayExitTime` | diario 21:00; viernes 20:00 | diario 22:30; viernes 21:30 | no diario; no viernes | no diario; no viernes | no diario; no viernes | no diario; no viernes | no diario; no viernes | diario 22:00; viernes 21:00 |
| **Trading options** › Max trades per day | `MaxTradesPerDay` | 6 | 3 | 2 | 1 | 2 | 2 | 2 | 1 |
| **Trading options** › Max distance from market | `MaxDistanceFromMarket/MaxDistancePct` | 0.3 % | 0.6 % | 2 % | 5 % | 2 % | 1 % | 1 % | 0.5 % |
| **Trading options** › Reserved bars | `ReservedBars` | 120 | 120 | 150 | 260 | 260 | 80 | 60 | 60 |
| **Building blocks** › Order types | `Blocks/OrderTypes` | EnterAtMarket (w1), EnterAtStop (w3, válida 1-3 velas) | EnterAtMarket (w1), EnterAtStop (w3, válida 2-8 velas) | EnterAtMarket (w1), EnterAtStop (w3, válida 2-6 velas) | EnterAtMarket (w2), EnterAtStop (w2, válida 1-5 velas) | EnterAtMarket (w2), EnterAtStop (w2, válida 1-4 velas) | EnterAtMarket (w1), EnterAtLimit (w3, válida 1-5 velas) | EnterAtMarket (w1), EnterAtStop (w3, válida 1-3 velas), EnterAtLimit (w1, válida 1-3 velas) | EnterAtMarket (w1), EnterAtStop (w3, válida 1-4 velas) |
| **Building blocks** › Stop loss / Profit target | `ExitTypes StopLoss/ProfitTarget` | SL sí (100 %); PT sí (100 %) | SL sí (100 %); PT sí (50 %) | SL sí (100 %); PT sí (50 %) | SL sí (100 %); PT no | SL sí (100 %); PT sí (30 %) | SL sí (100 %); PT sí (100 %) | SL sí (100 %); PT sí (100 %) | SL sí (100 %); PT sí (50 %) |
| **Building blocks** › Trailing stop | `ExitTypes TrailingStop` | no | sí (30 %), 1.5-3 ATR | sí (50 %), 2-4 ATR | sí (70 %), 2.5-5 ATR | sí (80 %), 2.5-5 ATR | no | no | no |
| **Building blocks** › Move SL to BE | `ExitTypes MoveSL2BE` | sí (50 %), 0.5-1.5 ATR | sí (30 %), 1-2 ATR | sí (30 %), 1-2 ATR | no | no | no | sí (50 %), 1-2 ATR | sí (50 %), 0.5-1.5 ATR |
| **Building blocks** › Exit after bars | `ExitTypes ExitAfterBars` | sí (50 %), 6-36 velas | no | sí (40 %), 6-30 velas | sí (30 %), 10-40 velas | no | sí (50 %), 5-30 velas | sí (30 %), 5-30 velas | sí (70 %), 2-16 velas |
| **Building blocks** › Exit rule | `ExitTypes _ExitRule_` | sí (30 %) | sí (30 %) | sí (30 %) | sí (50 %) | sí (50 %) | sí (50 %) | sí (30 %) | no |
| **Building blocks** › Bloques activos (lista: docs/03 §3) | `BuildingBlocks` | 91 señales / 48 indicadores / 40 stop-limit | 110 señales / 52 indicadores / 40 stop-limit | 115 señales / 51 indicadores / 38 stop-limit | 93 señales / 48 indicadores / 31 stop-limit | 105 señales / 46 indicadores / 33 stop-limit | 47 señales / 48 indicadores / 36 stop-limit | 33 señales / 37 indicadores / 32 stop-limit | 54 señales / 38 indicadores / 26 stop-limit |
| **Money management** › Método | `MoneyManagement/Method` | FixedAmount: riesgo 50 por operación | FixedAmount: riesgo 50 por operación | FixedAmount: riesgo 100 por operación | FixedAmount: riesgo 100 por operación | FixedAmount: riesgo 100 por operación | FixedAmount: riesgo 75 por operación | FixedAmount: riesgo 100 por operación | FixedAmount: riesgo 50 por operación |
| **Ranking** › Fitness | `FitnessCriteria/Ranking` | Weighted: ReturnDDRatio (peso 1, max), SQN (peso 2, max) | Weighted: ReturnDDRatio (peso 2, max), StagnationPct (peso 1, min) | Weighted: ReturnDDRatio (peso 2, max), Stability (peso 1, max) | Weighted: ReturnDDRatio (peso 2, max), Stability (peso 1, max) | Weighted: ReturnDDRatio (peso 2, max), StagnationPct (peso 1, min) | Weighted: ProfitFactor (peso 1, max), ReturnDDRatio (peso 2, max) | Weighted: ReturnDDRatio (peso 2, max), SQN (peso 1, max) | Weighted: ProfitFactor (peso 1, max), ReturnDDRatio (peso 2, max) |
| **Ranking** › Filtering conditions | `Rankings/Conditions` | NumberOfTrades(IS) >= 1050; ReturnDDRatio(IS) >= 6; WinningPct(IS) >= 45; ProfitFactor(IS) >= 1.25; AvgBarsInTrade(IS) >= 3; NetProfit(OOS) > 0; NumberOfTrades(OOS) >= 360 | NumberOfTrades(IS) >= 630; ReturnDDRatio(IS) >= 5; WinningPct(IS) >= 40; ProfitFactor(IS) >= 1.25; AvgBarsInTrade(IS) >= 2; NetProfit(OOS) > 0; NumberOfTrades(OOS) >= 190 | NumberOfTrades(IS) >= 240; ReturnDDRatio(IS) >= 4; WinningPct(IS) >= 38; ProfitFactor(IS) >= 1.3; AvgBarsInTrade(IS) >= 3; NetProfit(OOS) > 0; NumberOfTrades(OOS) >= 70 | NumberOfTrades(IS) >= 150; ReturnDDRatio(IS) >= 3; WinningPct(IS) >= 33; ProfitFactor(IS) >= 1.4; AvgBarsInTrade(IS) >= 4 | NumberOfTrades(IS) >= 260; ReturnDDRatio(IS) >= 3.5; WinningPct(IS) >= 30; ProfitFactor(IS) >= 1.3; AvgBarsInTrade(IS) >= 5; NetProfit(OOS) > 0; NumberOfTrades(OOS) >= 80 | NumberOfTrades(IS) >= 320; ReturnDDRatio(IS) >= 4; WinningPct(IS) >= 55; ProfitFactor(IS) >= 1.25; AvgBarsInTrade(IS) >= 2; NetProfit(OOS) > 0; NumberOfTrades(OOS) >= 100 | NumberOfTrades(IS) >= 320; ReturnDDRatio(IS) >= 4; WinningPct(IS) >= 40; ProfitFactor(IS) >= 1.3; AvgBarsInTrade(IS) >= 2; NetProfit(OOS) > 0; NumberOfTrades(OOS) >= 100 | NumberOfTrades(IS) >= 210; ReturnDDRatio(IS) >= 3; WinningPct(IS) >= 35; ProfitFactor(IS) >= 1.3; AvgBarsInTrade(IS) >= 2; NetProfit(OOS) > 0; NumberOfTrades(OOS) >= 70 |

### A.2.2 `Ventaja_Build` (test de ventaja de la entrada)

| Pestaña › campo | Nodo XML | Scalping | DayTrading | Swing | Position | TrendFollowing | Range | PriceAction | NewsProxy |
|---|---|---|---|---|---|---|---|---|---|
| **What to build** › Strategy type | `WhatToBuild/StrategyType@type` | simple | simple | simple | simple | simple | simple | simple | simple |
| **What to build** › Trading direction | `WhatToBuild/MarketSides@type` | long | long | long | long | long | long | long | long |
| **What to build** › Entry conditions min–max | `RulesComplexity/Chart@min/maxConditions` | 1–3 | 1–3 | 1–3 | 1–2 | 1–3 | 1–3 | 1–3 | 1–3 |
| **What to build** › Exit conditions min–max | `Chart@min/maxExitConditions` | 1–3 | 1–3 | 1–3 | 1–3 | 1–3 | 1–3 | 1–3 | 1–3 |
| **What to build** › Exit types min–max | `Chart@min/maxExitTypes` | 1–1 | 1–1 | 1–1 | 1–1 | 1–1 | 1–1 | 1–1 | 1–1 |
| **What to build** › Indicator period min–max | `Chart@min/maxPeriod` | 5–100 | 5–100 | 5–120 | 20–250 | 10–250 | 5–60 | 2–50 | 4–48 |
| **What to build** › Shift min–max | `Chart@min/maxShift` | 1–1 | 1–1 | 1–1 | 1–1 | 1–1 | 1–1 | 1–3 | 1–1 |
| **What to build** › Stop Loss | `SLPTOptions/SL*` | obligatorio=false; sin ATR | obligatorio=false; sin ATR | obligatorio=false; sin ATR | obligatorio=false; sin ATR | obligatorio=false; sin ATR | obligatorio=false; sin ATR | obligatorio=false; sin ATR | obligatorio=false; sin ATR |
| **What to build** › Profit Target / Risk-Reward | `SLPTOptions/PT*, LimitSLPTRRR*` | obligatorio=false; sin ATR | obligatorio=false; sin ATR | obligatorio=false; sin ATR | obligatorio=false; sin ATR | obligatorio=false; sin ATR | obligatorio=false; sin ATR | obligatorio=false; sin ATR | obligatorio=false; sin ATR |
| **Genetic options** › Población / islas / generaciones / cruce / mutación / migración / estancamiento | `BuildMode/*` | población 20 × 4 islas, 30 generaciones, cruce 80 %, mutación 30 %, migración 10 % cada 10, reinicio por estancamiento a 15 | población 25 × 4 islas, 30 generaciones, cruce 80 %, mutación 30 %, migración 10 % cada 10, reinicio por estancamiento a 15 | población 25 × 4 islas, 30 generaciones, cruce 80 %, mutación 30 %, migración 10 % cada 10, reinicio por estancamiento a 15 | población 25 × 4 islas, 30 generaciones, cruce 80 %, mutación 30 %, migración 10 % cada 10, reinicio por estancamiento a 15 | población 25 × 4 islas, 30 generaciones, cruce 80 %, mutación 30 %, migración 10 % cada 10, reinicio por estancamiento a 15 | población 25 × 4 islas, 30 generaciones, cruce 80 %, mutación 30 %, migración 10 % cada 10, reinicio por estancamiento a 15 | población 25 × 4 islas, 30 generaciones, cruce 80 %, mutación 30 %, migración 10 % cada 10, reinicio por estancamiento a 15 | población 20 × 4 islas, 30 generaciones, cruce 80 %, mutación 30 %, migración 10 % cada 10, reinicio por estancamiento a 15 |
| **Genetic options** › Initial population filters | `BuildMode/Conditions` | NumberOfTrades(IS) >= 320 | NumberOfTrades(IS) >= 190 | NumberOfTrades(IS) >= 70 | NumberOfTrades(IS) >= 40 | NumberOfTrades(IS) >= 80 | NumberOfTrades(IS) >= 100 | NumberOfTrades(IS) >= 100 | NumberOfTrades(IS) >= 60 |
| **Data** › Symbol | `Setup/Chart@symbol` | GBPJPY_M1_M1_UTCPlus02 | GBPJPY_M1_M1_UTCPlus02 | GBPJPY_M1_M1_UTCPlus02 | GBPJPY_M1_M1_UTCPlus02 | GBPJPY_M1_M1_UTCPlus02 | GBPJPY_M1_M1_UTCPlus02 | GBPJPY_M1_M1_UTCPlus02 | GBPJPY_M1_M1_UTCPlus02 |
| **Data** › Timeframe | `Setup/Chart@timeframe` | M5 | M15 | H4 | D1 | H1 | H1 | H1 | M15 |
| **Data** › Date from – to | `Setup@dateFrom/dateTo` | 2016.01.04 – 2020.12.31 | 2013.09.30 – 2020.12.31 | 2013.09.30 – 2020.12.31 | 2013.09.30 – 2020.12.31 | 2013.09.30 – 2020.12.31 | 2013.09.30 – 2020.12.31 | 2013.09.30 – 2020.12.31 | 2016.01.04 – 2020.12.31 |
| **Data** › Out of sample | `OutOfSample/Range` | 2019.07.01 – 2020.12.31 | 2019.01.01 – 2020.12.31 | 2019.01.01 – 2020.12.31 | sin OOS | 2019.01.01 – 2020.12.31 | 2019.01.01 – 2020.12.31 | 2019.01.01 – 2020.12.31 | 2019.07.01 – 2020.12.31 |
| **Data** › Precision | `Setup@testPrecision` | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| **Data** › Spread / Slippage | `Chart@spread, Setup@slippage` | 2 / 0.5 | 2 / 0.3 | 2 / 0.3 | 2 / 0.5 | 2 / 0.3 | 2 / 0.3 | 2 / 0.3 | 2 / 1.5 |
| **Trading options** › Limit signals to time range | `LimitTimeRange, SignalTimeRangeFrom/To, ExitAtEndOfRange` | 09:00-18:30 + cierre al final | 09:00-19:00 | sin ventana | sin ventana | 01:30-23:30 | 01:30-09:30 | 01:30-23:30 | 15:00-17:00 |
| **Trading options** › Exit at end of day / on Friday | `ExitAtEndOfDay/EODExitTime, ExitOnFriday/FridayExitTime` | diario 21:00; viernes 20:00 | diario 22:30; viernes 21:30 | no diario; no viernes | no diario; no viernes | no diario; no viernes | no diario; no viernes | no diario; no viernes | diario 22:00; viernes 21:00 |
| **Trading options** › Max trades per day | `MaxTradesPerDay` | 6 | 3 | 2 | 1 | 2 | 2 | 2 | 1 |
| **Trading options** › Max distance from market | `MaxDistanceFromMarket/MaxDistancePct` | 0.3 % | 0.6 % | 2 % | 5 % | 2 % | 1 % | 1 % | 0.5 % |
| **Trading options** › Reserved bars | `ReservedBars` | 120 | 120 | 150 | 260 | 260 | 80 | 60 | 60 |
| **Building blocks** › Order types | `Blocks/OrderTypes` | EnterAtMarket (w1), EnterAtStop (w3, válida 1-3 velas) | EnterAtMarket (w1), EnterAtStop (w3, válida 2-8 velas) | EnterAtMarket (w1), EnterAtStop (w3, válida 2-6 velas) | EnterAtMarket (w2), EnterAtStop (w2, válida 1-5 velas) | EnterAtMarket (w2), EnterAtStop (w2, válida 1-4 velas) | EnterAtMarket (w1), EnterAtLimit (w3, válida 1-5 velas) | EnterAtMarket (w1), EnterAtStop (w3, válida 1-3 velas), EnterAtLimit (w1, válida 1-3 velas) | EnterAtMarket (w1), EnterAtStop (w3, válida 1-4 velas) |
| **Building blocks** › Stop loss / Profit target | `ExitTypes StopLoss/ProfitTarget` | SL no; PT no | SL no; PT no | SL no; PT no | SL no; PT no | SL no; PT no | SL no; PT no | SL no; PT no | SL no; PT no |
| **Building blocks** › Trailing stop | `ExitTypes TrailingStop` | no | no | no | no | no | no | no | no |
| **Building blocks** › Move SL to BE | `ExitTypes MoveSL2BE` | no | no | no | no | no | no | no | no |
| **Building blocks** › Exit after bars | `ExitTypes ExitAfterBars` | sí (100 %), 3-24 velas | sí (100 %), 4-24 velas | sí (100 %), 6-30 velas | sí (100 %), 5-40 velas | sí (100 %), 12-72 velas | sí (100 %), 3-24 velas | sí (100 %), 3-24 velas | sí (100 %), 2-12 velas |
| **Building blocks** › Exit rule | `ExitTypes _ExitRule_` | no | no | no | no | no | no | no | no |
| **Building blocks** › Bloques activos (lista: docs/03 §3) | `BuildingBlocks` | 91 señales / 48 indicadores / 40 stop-limit | 110 señales / 52 indicadores / 40 stop-limit | 115 señales / 51 indicadores / 38 stop-limit | 93 señales / 48 indicadores / 31 stop-limit | 105 señales / 46 indicadores / 33 stop-limit | 47 señales / 48 indicadores / 36 stop-limit | 33 señales / 37 indicadores / 32 stop-limit | 54 señales / 38 indicadores / 26 stop-limit |
| **Money management** › Método | `MoneyManagement/Method` | FixedSize: 1 lote | FixedSize: 1 lote | FixedSize: 1 lote | FixedSize: 1 lote | FixedSize: 1 lote | FixedSize: 1 lote | FixedSize: 1 lote | FixedSize: 1 lote |
| **Ranking** › Fitness | `FitnessCriteria/Ranking` | Weighted: SQN (peso 2, max), StagnationPct (peso 1, min) | Weighted: SQN (peso 2, max), StagnationPct (peso 1, min) | Weighted: SQN (peso 2, max), StagnationPct (peso 1, min) | Weighted: ProfitFactor (peso 2, max), StagnationPct (peso 1, min) | Weighted: SQN (peso 2, max), StagnationPct (peso 1, min) | Weighted: SQN (peso 2, max), StagnationPct (peso 1, min) | Weighted: SQN (peso 2, max), StagnationPct (peso 1, min) | Weighted: SQN (peso 2, max), StagnationPct (peso 1, min) |
| **Ranking** › Filtering conditions | `Rankings/Conditions` | NumberOfTrades(IS) >= 1050; ReturnDDRatio(IS) >= 3; WinningPct(IS) >= 40; ProfitFactor(IS) >= 1.15; AvgBarsInTrade(IS) >= 3; NetProfit(OOS) > 0; NumberOfTrades(OOS) >= 360 | NumberOfTrades(IS) >= 630; ReturnDDRatio(IS) >= 2.5; WinningPct(IS) >= 35; ProfitFactor(IS) >= 1.15; AvgBarsInTrade(IS) >= 2; NetProfit(OOS) > 0; NumberOfTrades(OOS) >= 190 | NumberOfTrades(IS) >= 240; ReturnDDRatio(IS) >= 2; WinningPct(IS) >= 33; ProfitFactor(IS) >= 1.15; AvgBarsInTrade(IS) >= 3; NetProfit(OOS) > 0; NumberOfTrades(OOS) >= 70 | NumberOfTrades(IS) >= 150; ReturnDDRatio(IS) >= 1.5; WinningPct(IS) >= 30; ProfitFactor(IS) >= 1.3; AvgBarsInTrade(IS) >= 4 | NumberOfTrades(IS) >= 260; ReturnDDRatio(IS) >= 1.75; WinningPct(IS) >= 30; ProfitFactor(IS) >= 1.15; AvgBarsInTrade(IS) >= 5; NetProfit(OOS) > 0; NumberOfTrades(OOS) >= 80 | NumberOfTrades(IS) >= 320; ReturnDDRatio(IS) >= 2; WinningPct(IS) >= 50; ProfitFactor(IS) >= 1.15; AvgBarsInTrade(IS) >= 2; NetProfit(OOS) > 0; NumberOfTrades(OOS) >= 100 | NumberOfTrades(IS) >= 320; ReturnDDRatio(IS) >= 2; WinningPct(IS) >= 35; ProfitFactor(IS) >= 1.15; AvgBarsInTrade(IS) >= 2; NetProfit(OOS) > 0; NumberOfTrades(OOS) >= 100 | NumberOfTrades(IS) >= 210; ReturnDDRatio(IS) >= 1.5; WinningPct(IS) >= 30; ProfitFactor(IS) >= 1.15; AvgBarsInTrade(IS) >= 2; NetProfit(OOS) > 0; NumberOfTrades(OOS) >= 70 |

### A.2.3 `Estrategia_Retest`

| Pestaña › campo | Nodo XML | Scalping | DayTrading | Swing | Position | TrendFollowing | Range | PriceAction | NewsProxy |
|---|---|---|---|---|---|---|---|---|---|
| **Data** › Timeframe | `Setup/Chart@timeframe` | M5 | M15 | H4 | D1 | H1 | H1 | H1 | M15 |
| **Data** › Date from – to / OOS | `Setup, OutOfSample` | 2013.09.30 – 2024.07.22; OOS 2021.01.01 – 2024.07.22 | 2013.09.30 – 2024.07.22; OOS 2021.01.01 – 2024.07.22 | 2013.09.30 – 2024.07.22; OOS 2021.01.01 – 2024.07.22 | 2013.09.30 – 2024.07.22; OOS 2021.01.01 – 2024.07.22 | 2013.09.30 – 2024.07.22; OOS 2021.01.01 – 2024.07.22 | 2013.09.30 – 2024.07.22; OOS 2021.01.01 – 2024.07.22 | 2013.09.30 – 2024.07.22; OOS 2021.01.01 – 2024.07.22 | 2013.09.30 – 2024.07.22; OOS 2021.01.01 – 2024.07.22 |
| **Data** › Slippage | `Setup@slippage` | 0.5 | 0.3 | 0.3 | 0.5 | 0.3 | 0.3 | 0.3 | 1.5 |
| **Trading options** › Ventana / cierres / máx. ops | `BuildTradingOptions` | 09:00-18:30 + cierre al final; diario 21:00; viernes 20:00; máx. 6 | 09:00-19:00; diario 22:30; viernes 21:30; máx. 3 | sin ventana; no diario; no viernes; máx. 2 | sin ventana; no diario; no viernes; máx. 1 | 01:30-23:30; no diario; no viernes; máx. 2 | 01:30-09:30; no diario; no viernes; máx. 2 | 01:30-23:30; no diario; no viernes; máx. 2 | 15:00-17:00; diario 22:00; viernes 21:00; máx. 1 |
| **Money management** › Método | `MoneyManagement` | FixedAmount: riesgo 50 por operación | FixedAmount: riesgo 50 por operación | FixedAmount: riesgo 100 por operación | FixedAmount: riesgo 100 por operación | FixedAmount: riesgo 100 por operación | FixedAmount: riesgo 75 por operación | FixedAmount: riesgo 100 por operación | FixedAmount: riesgo 50 por operación |
| **Ranking** › Fitness | `FitnessCriteria` | Weighted: ReturnDDRatio (peso 1, max), SQN (peso 2, max) | Weighted: ReturnDDRatio (peso 2, max), StagnationPct (peso 1, min) | Weighted: ReturnDDRatio (peso 2, max), Stability (peso 1, max) | Weighted: ReturnDDRatio (peso 2, max), Stability (peso 1, max) | Weighted: ReturnDDRatio (peso 2, max), StagnationPct (peso 1, min) | Weighted: ProfitFactor (peso 1, max), ReturnDDRatio (peso 2, max) | Weighted: ReturnDDRatio (peso 2, max), SQN (peso 1, max) | Weighted: ProfitFactor (peso 1, max), ReturnDDRatio (peso 2, max) |
| **Ranking** › Filtering conditions | `Rankings/Conditions` | NetProfit(OOS) > 0; ProfitFactor(OOS) >= 1.1; ReturnDDRatio(Full) >= 9; NumberOfTrades(Full) >= 2920; NumberOfTrades(OOS) >= 850; DrawdownPct(Full) <= 20 | NetProfit(OOS) > 0; ProfitFactor(OOS) >= 1.1; ReturnDDRatio(Full) >= 7.5; NumberOfTrades(Full) >= 1170; NumberOfTrades(OOS) >= 340; DrawdownPct(Full) <= 20 | NetProfit(OOS) > 0; ProfitFactor(OOS) >= 1.1; ReturnDDRatio(Full) >= 6; NumberOfTrades(Full) >= 440; NumberOfTrades(OOS) >= 130; DrawdownPct(Full) <= 20 | NetProfit(OOS) > 0; ReturnDDRatio(Full) >= 4.5; NumberOfTrades(Full) >= 190; NumberOfTrades(OOS) >= 60; DrawdownPct(Full) <= 25 | NetProfit(OOS) > 0; ProfitFactor(OOS) >= 1.05; ReturnDDRatio(Full) >= 5.25; NumberOfTrades(Full) >= 490; NumberOfTrades(OOS) >= 140; DrawdownPct(Full) <= 25 | NetProfit(OOS) > 0; ProfitFactor(OOS) >= 1.1; ReturnDDRatio(Full) >= 6; NumberOfTrades(Full) >= 580; NumberOfTrades(OOS) >= 170; DrawdownPct(Full) <= 20 | NetProfit(OOS) > 0; ProfitFactor(OOS) >= 1.1; ReturnDDRatio(Full) >= 6; NumberOfTrades(Full) >= 580; NumberOfTrades(OOS) >= 170; DrawdownPct(Full) <= 20 | NetProfit(OOS) > 0; ProfitFactor(OOS) >= 1.05; ReturnDDRatio(Full) >= 4.5; NumberOfTrades(Full) >= 580; NumberOfTrades(OOS) >= 170; DrawdownPct(Full) <= 20 |
| **Cross checks** › Retest with higher precision | `RetestWithHigherPrecision` | activo; precisión 3 (tick real + spread real); 3 condiciones | activo; precisión 2 (tick real + spread personalizado); 3 condiciones | activo; precisión 2 (tick real + spread personalizado); 3 condiciones | activo; precisión 2 (tick real + spread personalizado); 3 condiciones | activo; precisión 2 (tick real + spread personalizado); 3 condiciones | activo; precisión 2 (tick real + spread personalizado); 3 condiciones | activo; precisión 2 (tick real + spread personalizado); 3 condiciones | activo; precisión 3 (tick real + spread real); 3 condiciones |
| **Cross checks** › Monte Carlo retest | `MonteCarloRetest` | activo; 200 sims; OHLC ±10 % ATR(14), desliz. 0-1, spread 2-4. Acepta: NetProfit(Full) >= 0; DrawdownPct(Full) <= 150% de DrawdownPct[main] | activo; 300 sims; OHLC ±10 % ATR(14), desliz. 0-0.5, spread 2-4. Acepta: NetProfit(Full) >= 0; DrawdownPct(Full) <= 150% de DrawdownPct[main] | activo; 500 sims; OHLC ±10 % ATR(14), desliz. 0-0.5, spread 2-4, vela de inicio. Acepta: NetProfit(Full) >= 0; DrawdownPct(Full) <= 150% de DrawdownPct[main] | activo; 500 sims; OHLC ±10 % ATR(14), desliz. 0-1, spread 2-4, vela de inicio. Acepta: NetProfit(Full) >= 0; DrawdownPct(Full) <= 175% de DrawdownPct[main] | activo; 500 sims; OHLC ±10 % ATR(14), desliz. 0-0.5, spread 2-4, vela de inicio. Acepta: NetProfit(Full) >= 0; DrawdownPct(Full) <= 175% de DrawdownPct[main] | activo; 500 sims; OHLC ±10 % ATR(14), desliz. 0-0.5, spread 2-4. Acepta: NetProfit(Full) >= 0; DrawdownPct(Full) <= 150% de DrawdownPct[main] | activo; 500 sims; OHLC ±10 % ATR(14), desliz. 0-0.5, spread 2-4. Acepta: NetProfit(Full) >= 0; DrawdownPct(Full) <= 150% de DrawdownPct[main] | activo; 200 sims; OHLC ±10 % ATR(14), desliz. 0-3, spread 2-8. Acepta: NetProfit(Full) >= 0; DrawdownPct(Full) <= 150% de DrawdownPct[main] |
| **Cross checks** › Monte Carlo trades manipulation | `MonteCarloManipulation` | activo; orden de operaciones 'resampling', saltar 10 % | activo; orden de operaciones 'resampling', saltar 10 % | activo; orden de operaciones 'resampling', saltar 10 % | activo; orden de operaciones 'resampling', saltar 10 % | activo; orden de operaciones 'resampling', saltar 10 % | activo; orden de operaciones 'resampling', saltar 10 % | activo; orden de operaciones 'resampling', saltar 10 % | activo; orden de operaciones 'resampling', saltar 10 % |
| **Cross checks** › Optimization profile / SPP | `OptProfileSysParamPermutation` | activo; 1500 tests, ±20 %, 6 pasos; ≥80 % rentables | activo; 3000 tests, ±20 %, 6 pasos; ≥85 % rentables | activo; 5000 tests, ±20 %, 6 pasos; ≥85 % rentables | activo; 8000 tests, ±30 %, 6 pasos; ≥90 % rentables | activo; 5000 tests, ±30 %, 6 pasos; ≥90 % rentables | activo; 5000 tests, ±20 %, 6 pasos; ≥85 % rentables | activo; 5000 tests, ±20 %, 6 pasos; ≥85 % rentables | activo; 1500 tests, ±20 %, 6 pasos; ≥80 % rentables |
| **Cross checks** › What if | `WhatIf` | activo; ExcludePctTradesWithBiggestPl, ExcludePctTradesWithLowestPl | activo; ExcludePctTradesWithBiggestPl, ExcludePctTradesWithLowestPl | activo; ExcludeTradesWithBiggestPl, ExcludeTradesWithLowestPl | activo; ExcludeTradesWithBiggestPl, ExcludeTradesWithLowestPl | activo; ExcludeTradesWithBiggestPl, ExcludeTradesWithLowestPl | activo; ExcludePctTradesWithBiggestPl, ExcludePctTradesWithLowestPl | activo; ExcludePctTradesWithBiggestPl, ExcludePctTradesWithLowestPl | activo; ExcludePctTradesWithBiggestPl, ExcludePctTradesWithLowestPl |

### A.2.4 `Ventaja_Retest`

| Pestaña › campo | Nodo XML | Scalping | DayTrading | Swing | Position | TrendFollowing | Range | PriceAction | NewsProxy |
|---|---|---|---|---|---|---|---|---|---|
| **Data** › Timeframe | `Setup/Chart@timeframe` | M5 | M15 | H4 | D1 | H1 | H1 | H1 | M15 |
| **Data** › Date from – to / OOS | `Setup, OutOfSample` | 2013.09.30 – 2024.07.22; OOS 2021.01.01 – 2024.07.22 | 2013.09.30 – 2024.07.22; OOS 2021.01.01 – 2024.07.22 | 2013.09.30 – 2024.07.22; OOS 2021.01.01 – 2024.07.22 | 2013.09.30 – 2024.07.22; OOS 2021.01.01 – 2024.07.22 | 2013.09.30 – 2024.07.22; OOS 2021.01.01 – 2024.07.22 | 2013.09.30 – 2024.07.22; OOS 2021.01.01 – 2024.07.22 | 2013.09.30 – 2024.07.22; OOS 2021.01.01 – 2024.07.22 | 2013.09.30 – 2024.07.22; OOS 2021.01.01 – 2024.07.22 |
| **Data** › Slippage | `Setup@slippage` | 0.5 | 0.3 | 0.3 | 0.5 | 0.3 | 0.3 | 0.3 | 1.5 |
| **Trading options** › Ventana / cierres / máx. ops | `BuildTradingOptions` | 09:00-18:30 + cierre al final; diario 21:00; viernes 20:00; máx. 6 | 09:00-19:00; diario 22:30; viernes 21:30; máx. 3 | sin ventana; no diario; no viernes; máx. 2 | sin ventana; no diario; no viernes; máx. 1 | 01:30-23:30; no diario; no viernes; máx. 2 | 01:30-09:30; no diario; no viernes; máx. 2 | 01:30-23:30; no diario; no viernes; máx. 2 | 15:00-17:00; diario 22:00; viernes 21:00; máx. 1 |
| **Money management** › Método | `MoneyManagement` | FixedSize: 1 lote | FixedSize: 1 lote | FixedSize: 1 lote | FixedSize: 1 lote | FixedSize: 1 lote | FixedSize: 1 lote | FixedSize: 1 lote | FixedSize: 1 lote |
| **Ranking** › Fitness | `FitnessCriteria` | Weighted: SQN (peso 2, max), StagnationPct (peso 1, min) | Weighted: SQN (peso 2, max), StagnationPct (peso 1, min) | Weighted: SQN (peso 2, max), StagnationPct (peso 1, min) | Weighted: ProfitFactor (peso 2, max), StagnationPct (peso 1, min) | Weighted: SQN (peso 2, max), StagnationPct (peso 1, min) | Weighted: SQN (peso 2, max), StagnationPct (peso 1, min) | Weighted: SQN (peso 2, max), StagnationPct (peso 1, min) | Weighted: SQN (peso 2, max), StagnationPct (peso 1, min) |
| **Ranking** › Filtering conditions | `Rankings/Conditions` | NetProfit(OOS) > 0; ProfitFactor(Full) >= 1.1; NumberOfTrades(Full) >= 2920; NumberOfTrades(OOS) >= 850 | NetProfit(OOS) > 0; ProfitFactor(Full) >= 1.1; NumberOfTrades(Full) >= 1170; NumberOfTrades(OOS) >= 340 | NetProfit(OOS) > 0; ProfitFactor(Full) >= 1.1; NumberOfTrades(Full) >= 440; NumberOfTrades(OOS) >= 130 | NetProfit(OOS) > 0; ProfitFactor(Full) >= 1.2; NumberOfTrades(Full) >= 190; NumberOfTrades(OOS) >= 60 | NetProfit(OOS) > 0; ProfitFactor(Full) >= 1.1; NumberOfTrades(Full) >= 490; NumberOfTrades(OOS) >= 140 | NetProfit(OOS) > 0; ProfitFactor(Full) >= 1.1; NumberOfTrades(Full) >= 580; NumberOfTrades(OOS) >= 170 | NetProfit(OOS) > 0; ProfitFactor(Full) >= 1.1; NumberOfTrades(Full) >= 580; NumberOfTrades(OOS) >= 170 | NetProfit(OOS) > 0; ProfitFactor(Full) >= 1.1; NumberOfTrades(Full) >= 580; NumberOfTrades(OOS) >= 170 |
| **Cross checks** › Retest with higher precision | `RetestWithHigherPrecision` | activo; precisión 3 (tick real + spread real); 3 condiciones | activo; precisión 2 (tick real + spread personalizado); 3 condiciones | activo; precisión 2 (tick real + spread personalizado); 3 condiciones | activo; precisión 2 (tick real + spread personalizado); 3 condiciones | activo; precisión 2 (tick real + spread personalizado); 3 condiciones | activo; precisión 2 (tick real + spread personalizado); 3 condiciones | activo; precisión 2 (tick real + spread personalizado); 3 condiciones | activo; precisión 3 (tick real + spread real); 3 condiciones |
| **Cross checks** › Monte Carlo retest | `MonteCarloRetest` | activo; 200 sims; OHLC ±10 % ATR(14), desliz. 0-1, spread 2-4. Acepta: NetProfit(Full) >= 0; DrawdownPct(Full) <= 150% de DrawdownPct[main] | activo; 300 sims; OHLC ±10 % ATR(14), desliz. 0-0.5, spread 2-4. Acepta: NetProfit(Full) >= 0; DrawdownPct(Full) <= 150% de DrawdownPct[main] | activo; 500 sims; OHLC ±10 % ATR(14), desliz. 0-0.5, spread 2-4, vela de inicio. Acepta: NetProfit(Full) >= 0; DrawdownPct(Full) <= 150% de DrawdownPct[main] | activo; 500 sims; OHLC ±10 % ATR(14), desliz. 0-1, spread 2-4, vela de inicio. Acepta: NetProfit(Full) >= 0; DrawdownPct(Full) <= 175% de DrawdownPct[main] | activo; 500 sims; OHLC ±10 % ATR(14), desliz. 0-0.5, spread 2-4, vela de inicio. Acepta: NetProfit(Full) >= 0; DrawdownPct(Full) <= 175% de DrawdownPct[main] | activo; 500 sims; OHLC ±10 % ATR(14), desliz. 0-0.5, spread 2-4. Acepta: NetProfit(Full) >= 0; DrawdownPct(Full) <= 150% de DrawdownPct[main] | activo; 500 sims; OHLC ±10 % ATR(14), desliz. 0-0.5, spread 2-4. Acepta: NetProfit(Full) >= 0; DrawdownPct(Full) <= 150% de DrawdownPct[main] | activo; 200 sims; OHLC ±10 % ATR(14), desliz. 0-3, spread 2-8. Acepta: NetProfit(Full) >= 0; DrawdownPct(Full) <= 150% de DrawdownPct[main] |
| **Cross checks** › Monte Carlo trades manipulation | `MonteCarloManipulation` | activo; orden de operaciones 'resampling', saltar 10 % | activo; orden de operaciones 'resampling', saltar 10 % | activo; orden de operaciones 'resampling', saltar 10 % | activo; orden de operaciones 'resampling', saltar 10 % | activo; orden de operaciones 'resampling', saltar 10 % | activo; orden de operaciones 'resampling', saltar 10 % | activo; orden de operaciones 'resampling', saltar 10 % | activo; orden de operaciones 'resampling', saltar 10 % |
| **Cross checks** › Optimization profile / SPP | `OptProfileSysParamPermutation` | activo; 1500 tests, ±20 %, 6 pasos; ≥80 % rentables | activo; 3000 tests, ±20 %, 6 pasos; ≥85 % rentables | activo; 5000 tests, ±20 %, 6 pasos; ≥85 % rentables | activo; 8000 tests, ±30 %, 6 pasos; ≥90 % rentables | activo; 5000 tests, ±30 %, 6 pasos; ≥90 % rentables | activo; 5000 tests, ±20 %, 6 pasos; ≥85 % rentables | activo; 5000 tests, ±20 %, 6 pasos; ≥85 % rentables | activo; 1500 tests, ±20 %, 6 pasos; ≥80 % rentables |
| **Cross checks** › What if | `WhatIf` | activo; ExcludePctTradesWithBiggestPl, ExcludePctTradesWithLowestPl | activo; ExcludePctTradesWithBiggestPl, ExcludePctTradesWithLowestPl | activo; ExcludeTradesWithBiggestPl, ExcludeTradesWithLowestPl | activo; ExcludeTradesWithBiggestPl, ExcludeTradesWithLowestPl | activo; ExcludeTradesWithBiggestPl, ExcludeTradesWithLowestPl | activo; ExcludePctTradesWithBiggestPl, ExcludePctTradesWithLowestPl | activo; ExcludePctTradesWithBiggestPl, ExcludePctTradesWithLowestPl | activo; ExcludePctTradesWithBiggestPl, ExcludePctTradesWithLowestPl |

Valores que **no cambian** respecto al original en ningún estilo: símbolo, spread 2, comisión 0,7, swap (ver checklist punto 3), `testPrecision=1`, `MarketSides=long`, capital 10.000, `MaxStrategies=1000`, `DismissTooSimilarStrategies`, `AutomaticDismissal`, `ATMs` desactivado, cross checks desactivados en los Builders, `evaluateAll=false` y `DeleteFailedStrategies=false` en los Retest.

## A.3 Volver al flujo con plantilla (fiel al original)

El original construía la estrategia completa sobre una plantilla con la entrada fija. Para reproducirlo con cualquier estilo:

1. Ejecuta `Ventaja_Build…<Estilo>` y `Ventaja_Retest…<Estilo>`; elige 1-3 entradas que pasen todos los cross checks y tengan OOS 2021-2024 positivo.
2. Abre la estrategia en **AlgoWizard**, activa el modo plantilla y deja la entrada **fija** (condiciones y tipo de orden). Sustituye las salidas por los huecos aleatorios de salida que quieras que explore el Builder.
3. Guarda como `Template_<Estilo>_<TF>_BUY.sqx`.
4. En `Estrategia_Build…<Estilo>`: *What to build* → *Strategy from template* → elige la plantilla; pon *Entry conditions* 0–0 (como el original).
5. Mantén el resto de la configuración del estilo (SL/PT, salidas, filtros, motor).

## A.4 Walk-Forward Matrix en el Optimizer (no incluido en los originales)

Recomendado para Day Trading, Swing, Trend Following y Range (no para Position: pocas operaciones por ventana).

1. Crea una tarea **Optimizer** sobre las estrategias que superen `Estrategia_Retest`.
2. Parámetros a optimizar: periodos de indicadores y parámetros de salida (los mismos que el SPP), ±20-30 %, 5-10 pasos.
3. Matriz: ejecuciones 5-15 y OOS 10-30 %; mismo símbolo, timeframe, costes y opciones de trading que el kit.
4. Aceptación sugerida (la misma lógica que el WFM inactivo de los originales): ≥ 70 % de ejecuciones rentables, ninguna ejecución con > 50 % del beneficio total, DD por ejecución ≤ 25 %, y una zona de la matriz (no una celda aislada) que pase.

## A.5 Si el Builder no genera ninguna estrategia

Revisión 3 de los archivos: la causa principal era la **población inicial**. Las versiones anteriores pedían 160-200 estrategias aleatorias que cumpliesen Ret/DD, % de acierto y 200-870 operaciones antes de empezar a evolucionar; SQX no guarda nada hasta completarla, así que podía pasar horas o días sin mostrar ninguna. Ahora la población inicial sólo exige un mínimo de operaciones, la calibración de indicadores está activa y se han quitado los filtros de calendario muy restrictivos. Si aun así no aparece nada:

1. **Mira en qué fase está.** Si el progreso indica *initial population* / población inicial durante mucho tiempo, el filtro de *Genetic options › Initial population* sigue siendo demasiado estricto: déjalo sólo con nº de operaciones (o desactívalo).
2. **Mira las estadísticas de rechazo** (generadas / aceptadas / rechazadas y motivo). Si casi todo se rechaza por *NumberOfTrades*, baja la densidad del estilo; si es por *Ret/DD* o *PF*, los costes del símbolo probablemente se comen la ventaja (típico de Scalping y NewsProxy con GBPJPY).
3. **Calibra a mano**: *Building blocks › Calibrate* con el símbolo y timeframe ya puestos en *Data*. Comprueba que `ATR` ya no tiene rango −5000…5000.
4. **Prueba de humo**: pon *Generation type* = generación aleatoria y quita temporalmente los filtros del *Ranking* salvo `NumberOfTrades`. Si en 10-15 minutos tampoco salen estrategias, el problema es de datos o de importación (símbolo, fechas, timeframe, dirección), no de los filtros.
5. **Control con el original**: ejecuta el `Ventaja_Build_ConfigInicial_H1_BUY.cfx` original. Si tampoco genera nada, el problema está en los datos (`GBPJPY_M1_M1_UTCPlus02`, rango 2013-2020) y no en los archivos nuevos.
6. **Empieza por un estilo de barras largas** (Swing H4, Trend H1, Range H1): Scalping y NewsProxy sobre GBPJPY con 2 pips de spread + deslizamiento casi nunca encuentran estrategias rentables (ver Fase 2).

## E) Lista de verificación al importar

### E.1 Para los 64 archivos

1. **Versión:** SQX puede avisar de que el archivo es de la build 140.2099. Anota cualquier aviso; si dice que ignora o reinicia secciones, aplica esas secciones a mano (A.2).
2. **Símbolo:** `Data` → el símbolo `GBPJPY_M1_M1_UTCPlus02` debe existir en tu *Data Manager*. Si usas otro instrumento (recomendado en Scalping, Range, Noticias), cámbialo aquí **y en los 4 archivos del kit**.
3. **Costes:** spread, comisión (unidad y por lado/ida-vuelta) y swaps **de tu bróker**. Los heredados (swap -7,67/+4,30, triple **viernes**, comisión 0,7) son del US30 en Darwinex; para FX el triple swap es el **miércoles**.
4. **Horario del servidor:** confirma si los datos son UTC+2 fijo o UTC+2/+3 con DST de Nueva York. Si no coincide con el supuesto S5, desplaza todas las horas (ventana de señales, cierres, rangos horarios de `HighestInRange`/`Session*`, `BarHour*`).
5. **Fechas:** el rango del *Setup* debe estar dentro de tus datos; el OOS del Builder dentro del periodo de construcción; el OOS del Retest (2021.01.01-2024.07.22) **nunca** dentro del periodo de construcción.
6. **Opciones de trading idénticas** entre el Builder y el Retest del mismo kit (ventana, cierres, máx. operaciones/día, distancia máxima).
7. **Timeframe idéntico** en los 4 archivos del kit y en los *Setup* de *RetestOnAdditionalMarkets*.
8. **Money management:** `FixedAmount` en `Estrategia_*` (riesgo en dinero coherente con tu capital) y `FixedSize 1` en `Ventaja_*`.
9. **Fitness ponderada:** en *Ranking* deben aparecer exactamente los objetivos y pesos de la ficha (docs/03 §6).
10. **Filtros:** revisa que las condiciones IS/OOS/Full aparecen con la muestra correcta (IS, OOS, *Full*).
11. **Bases de datos:** Builder → salida `Results`; Retest → entrada y salida `Results`. Si encadenas Builder y Retest en un proyecto, apunta la entrada del Retest al banco de resultados del Builder.
12. **Población inicial y calibración** (*Genetic options* y *Building blocks*): el filtro de población inicial debe tener sólo `NumberOfTrades`; la calibración antes de empezar debe estar activa.
13. **No mezclar direcciones:** retestea las estrategias BUY con los Retest `_BUY` y las SELL con los `_SELL` (o en bancos de datos separados).

### E.1b Sólo kits SELL

- *What to build › Trading direction* debe mostrar **Short only**. `short` es el valor deducido del XML (los originales sólo traen `long`): si SQX lo ignora y muestra *Long only*, cámbialo a mano.
- En *Building blocks* deben estar activos los bloques bajistas (p. ej. `BarOpensBelowLowestAfterOpenAbove`, `BearishEngulfing`, `RSICrossDown`) y desactivados sus equivalentes alcistas; los niveles stop de mayor peso son los mínimos (`Lowest`, `Low`, `LowestInRange`, `SessionLow`…).
- **Swap corto**: el heredado (+4,30 triple viernes) es del US30; pon el swap corto real de tu bróker.
- Un kit SELL sobre un activo con deriva alcista de largo plazo (índices) encontrará menos estrategias: es esperable, no un fallo de configuración.

### E.2 Builders

14. *What to build*: `Simple strategy` (o plantilla, si sigues A.3), dirección del kit, rangos de complejidad de la tabla A.2.
15. *Building blocks*: nº de bloques activos = el de la tabla A.2 (p. ej. Scalping 93/48/40). Si la build 144 añade bloques nuevos, deben quedar **desactivados**.
16. *Order types* y *Exit types*: sólo los de la tabla; en `Ventaja_*`, **únicamente** *Exit after bars*.
17. Prueba corta: lanza el Builder 10-15 minutos y comprueba que se generan estrategias con el nº de operaciones esperado y que los rechazos no se deben a un filtro mal puesto (p. ej. todas descartadas por `NumberOfTrades`). Si casi todo se descarta por número de operaciones, baja la densidad del estilo en `tools/estilos.py` en vez de quitar el filtro.
18. Abre 2-3 estrategias generadas y verifica a ojo que su lógica corresponde al estilo (p. ej. órdenes stop en el máximo del rango asiático en Day Trading BUY / en el mínimo en SELL, órdenes límite en Range).

### E.3 Retesters

19. **Datos tick:** *Retest with higher precision* usa precisión 2 (tick real + spread personalizado) o 3 (tick real + spread real, en Scalping y Noticias). Sin datos tick ese cross check fallará o no se ejecutará.
20. Monte Carlo: nº de simulaciones, métodos (OHLC, spread, deslizamiento, vela de inicio) y condiciones al 95 %.
21. Monte Carlo de manipulación: la condición de beneficio debe compararse contra el resultado **principal** (no contra otro Monte Carlo).
22. SPP: nº de tests y % de rentables de la tabla; empieza con pocas estrategias (el coste es alto).
23. *Retest on additional markets* sigue **desactivado**: configúralo con 1-3 símbolos reales relacionados si vas a usarlo (el original repetía GBPJPY).

### E.4 Comprobaciones específicas por estilo

| Estilo | Comprobar |
|---|---|
| Scalping | Instrumento de spread bruto bajo; datos tick con spread real; coste total < 15 % del ATR(M5); cierre al final de la ventana activo. |
| Day Trading | Rango asiático en horas del servidor correctas; cierre diario 22:30 y viernes 21:30; órdenes stop activas. |
| Swing | Swap real del instrumento (se mantienen noches y fines de semana); `RealisticGapsHandling=true`. |
| Position | Mínimo 150 operaciones en 7,25 años (límite físico de un solo mercado con duraciones de semanas); ampliar datos a ≥15 años; sin filtro horario; retest multi-mercado. |
| Trend Following | H1 (no H4); trailing activo con prob. 80 %; acierto mínimo 30 % (no 40 %); what-if de 2 mejores/peores. |
| Range | Símbolo de rango (no GBPJPY); órdenes límite; PT obligatorio 40-120 % del SL; ventana 01:30-09:30. |
| Price Action | Sólo patrones alcistas; desplazamiento 1-3; MC de OHLC activo. |
| Noticias (proxy) | Ventana 15:00-17:00 = 8:00-10:00 ET con tu servidor; spread MC hasta 8 pips; precisión 3; cruzar después las operaciones con un calendario real. |

