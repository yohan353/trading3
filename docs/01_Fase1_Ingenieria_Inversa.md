# Fase 1 — Ingeniería inversa de los cuatro archivos

Convención: **(A)** explícito en el archivo · **(B)** deducido (confianza alta/media/baja) · **(C)** no determinable.
Los nombres entre `comillas de código` son nodos/atributos literales del XML. Rutas abreviadas desde `Task/Settings/`.

## 1.0 Visión de conjunto y claves de lectura

### El flujo de trabajo que implementan los cuatro archivos (B, alta)

```
 ┌───────────────────────┐   entradas con   ┌────────────────────────┐  ganadoras   ┌──────────────────────────┐
 │ 3. Ventaja_Build (H1) │ ───────────────▶ │ 4. Ventaja_Retest       │ ───────────▶ │ plantilla .sqx (AlgoWizard)│
 │ entrada aleatoria +   │   "ventaja"      │ 2013-2024, OOS 2021+    │  la entrada  │ Template_DOW_H1_BUY_1.8.4 │
 │ salida sólo por tiempo│                  │ tick real, MC, SPP      │  se fija     └─────────────┬────────────┘
 └───────────────────────┘                  └────────────────────────┘                            │
                                                                                                   ▼
 ┌────────────────────────┐  estrategias   ┌────────────────────────────┐
 │ 2. Estrategia_Retest    │ ◀───────────── │ 1. Estrategia_Build (H1)    │ entrada FIJA (plantilla, 0 condiciones
 │ 2013-2024, OOS 2021+    │   completas    │ el Builder sólo genera las  │ aleatorias) + SL/PT/trailing generados
 │ tick real, MC, SPP      │                │ salidas y sus parámetros    │
 └────────────────────────┘                └────────────────────────────┘
```

"Ventaja" = *edge*: primero se demuestra que una **entrada** tiene ventaja estadística con una salida neutra
(tiempo) y tamaño fijo; después se le construyen **salidas** y gestión de riesgo. Es una metodología sólida y
conocida (pruebas de entrada con salida a N barras). Evidencias: `Ventaja_Build` no exige SL/PT y sólo activa
`ExitAfterBars`; `Estrategia_Build` fija `minConditions="0" maxConditions="0"` (ninguna condición de entrada
aleatoria) y trabaja con plantilla; `PartsToImprove/ExitRules use="true"` apunta a mejorar salidas.

### Semántica de los códigos internos (necesaria para leer los filtros)

| Código en el XML | Significado | Confianza |
|---|---|---|
| `sampleType="10"` / `"20"` / `"127"` | In-sample / Out-of-sample / muestra completa | (B) alta: los filtros OOS del Retest usan 20 y las comparaciones "contra el original" 127 |
| `testPrecision="1"`; `<Precision>2</Precision>` | 1 = *1 minute data tick simulation*; 2 = *Real tick – custom spread*; 3 = *Real tick – real spread* (0 = *selected timeframe only*) | (B) alta (4 modos documentados por SQX, en ese orden) |
| `minValue="-1000003" maxValue="-1000004"` | "usar el rango global de Periodo" (`minPeriod`/`maxPeriod`) | (B) alta |
| `-1000001/-1000002` | rango global de Shift | (B) alta |
| `-1000005 … -1000016` | rangos de SL/PT definidos en `SLPTOptions` | (B) alta |
| Horas en `BuildTradingOptions` (`5400`, `84600`…) | segundos desde 00:00 (5400 = 01:30; 84600 = 23:30) | (B) alta |
| `LimitSLPTRRRFrom/To` | PT como % del SL (200-400 = PT 2-4 veces el SL) | (B) alta (documentación/foro oficial) |
| `Goal@valueType` 1/2/3 | maximizar / minimizar / objetivo | (B) media |
| `direction="0"`, `plType="10"` | ambas direcciones; resultado en dinero | (B) media |
| `confidenceLevel` | percentil de la distribución Monte Carlo (50 = mediana; neutro fuera de MC) | (B) alta |
| `pctRatio` | % aplicado al valor de ese lado (p. ej. 80 = "80 % del original") | (B) alta en el lado derecho; media en el izquierdo |
| `subresult="30/31/33"` | sub-resultado estándar / WF en % / métricas especiales WF | (B) baja-media |
| `ConditionsType=1` | todas las condiciones deben cumplirse (AND) | (B) media |
| `AutomaticDismissal` códigos 1,2,4,8,16,32,64,256,512,1024 | 10 "problemas" que SQX descarta automáticamente: sin operaciones, demasiadas ambiguas, demasiadas abiertas, órdenes no ejecutadas, P/L cero, duración cero, sin cerrar, <20 operaciones, operación atípica (outlier), muchas cierran en la misma vela | (B) alta en la lista; **(C)** qué código es cada problema |
| `EvoInSamplePeriod ratio="50"` | probablemente el % de la división IS en *entrenamiento/validación* de las opciones genéticas | (B) baja; si está activa o no: (C) |
| `RiskManagement maxDrawdown="30"`, `Rankings type="never"`, `additionalCharts` | sin efecto observable con la configuración actual | (C) |

---

## 1.1 Archivo 1 — `Estrategia_Build_ConfigInicial_H1_BUY.cfx`

### 1. Propósito y módulo
- (A) `Task type="Build"` → **Builder**; `BuildMode generationType="genetic-evolution"`; `StrategyType type="template"`
  con `templateFile=…\Template_DOW_H1_BUY_1.8.4.sqx`; `MarketSides type="long"`; `Notes`: "Breakout strategies setup".
- (B, alta) Genera **estrategias completas de compra sobre una entrada fija** (la de la plantilla): como
  `RulesComplexity/Chart minConditions="0" maxConditions="0"`, el Builder no inventa entradas; busca stop loss,
  objetivo, trailing y los parámetros que la plantilla deje como aleatorios.
- (C) Contenido de la plantilla: qué condiciones de entrada tiene, qué tipo de orden usa y qué partes marca como aleatorias.

### 2. Mercado y datos
| Elemento | Valor (A) | Comentario |
|---|---|---|
| `Data/Setups/Setup/Chart@symbol` | `GBPJPY_M1_M1_UTCPlus02` | (B, alta) datos M1 de GBPJPY en hora UTC+2. |
| `Chart@timeframe` | `H1` | |
| `Setup@dateFrom/dateTo` | `2013.09.30` – `2020.12.31` | 7,25 años. |
| `Data/OutOfSample` | **vacío** | **No hay OOS**: todo es in-sample. (B, alta) El periodo 2021-2024 queda reservado para el Retest. |
| `Setup@testPrecision` | `1` | Simulación de ticks con datos M1. |
| `Chart@spread` / `Setup@slippage` / `Setup@minDist` | `2` / `0` / `0` | Deslizamiento nulo: optimista. |
| `Commissions/Method type="SizeBased"` | `Commission=0.7` | (B, media) USD por lote. |
| `Swap` | `use="true" type="money" long="-7.67" short="4.3" tripleSwapOn="FRIDAY"` | **Son los swaps del Dow en Darwinex** (idénticos al `InstrumentInfo instrument="Dow_Darwinex"` de `Resources`). |
| `Setup@engine` / `session` | `MetaTrader5 (hedged)` / `No Session` | |
| `Resources/Symbols` | `USA30IDXUSD_Dukascopy_UTCPlus2` (M1, `timezone="Asia/Jerusalem"`, `cloneFrom="USA30IDXUSD_Dukascopy"`, 2013-09-30→2020-12-31) y `EURUSD_M1` | No se usan en ningún Setup. |

**Incoherencia grave (B, alta):** la plantilla y los costes son del **US30**, pero el símbolo de datos es **GBPJPY**.
En FX el triple swap es el miércoles (no el viernes) y los swaps de GBPJPY no son esos. El autor (o quien adaptó la
plantilla) cambió el símbolo sin cambiar los costes. Además, el reloj de los datos del Dow se emula con la zona
`Asia/Jerusalem`, cuyo horario de verano no coincide con el de EE. UU.: varias semanas al año las horas quedan
desplazadas 1 h respecto a un bróker con "cierre de Nueva York" (afecta a `LimitTimeRange` y a los bloques horarios).
(C) Zona horaria y DST reales de `GBPJPY_M1_M1_UTCPlus02`.

### 3. Bloques de construcción
**Catálogo** (A): 472 bloques (315 señales, 100 indicadores, 57 niveles stop/limit). **Activos: 204** (146 señales,
29 indicadores, 29 stop/limit), todos con `weight="1"`, `Generated weight="1"` y `Predefined changed="false"`.

| Familia (A) | Bloques activos |
|---|---|
| ADX / DI | `ADXChangesDown/Up`, `ADXCrossUp`, `ADXHigher`, `ADXLower`, `ADXRising`; `DIMinus*` (4), `DIPlus*` (6), `DICrossUp/Down` |
| Volatilidad | `ATRChangesDown/Up`, `ATRCrossUp/Down`, `ATRFalling/Rising`, `ATRHigher/Lower`; `StdDev*` (8); `BBUpper/LowerRising/Falling` |
| Bollinger (precio vs banda) | 12 bloques `BBBar{Closes,Opens}{Above,Below}{Up,Down}[After…]` |
| Ruptura de canal | `BarOpensAbove/BelowHighest/LowestAfterOpen…` (4) |
| Ichimoku | `IchimokuKumoBreakout{Bullish,Bearish}`, `KijunSenCross*`, `SenkouSpanCross*`, `TenkanKijunCross*` |
| Osciladores | `RSI*` (8), `Stoch*` (12), `LaguerreRSI*` (6), `Mom*` (8), `AWO*` (5), `MACD*` (18) |
| Tendencia | `MA*` (8), `LinReg*` (8), `PSARBarHigher/Lower`, `IsUptrend`, `IsDowntrend` |
| Velas | `BullishEngulfing`, `BearishEngulfing`, `DarkCloud`, `Doji`, `Hammer`, `PiercingLine`, `ShootingStar` |
| Indicadores (valores) | `ATR`, `BollingerBands`, `BullsPower`, `EMA`, `Fibo`, `LinearRegression`, `MACD`, `Pivots`, `ParabolicSAR`, `RSI`, `StdDev`, `Stochastic`, `Highest`, `HighestInRange`, `Lowest`, `LowestInRange` |
| Precios / comparadores | `Prices.Close/High/Low/HighD/LowD`; `IsGreater(OrEqual)`, `IsLower(OrEqual)`, `Is{Greater,Lower}Count`, `CrossesAbove/Below` |
| Niveles stop/limit | `Ask`, `Bid`, `Open/High/Low/Close`, `OpenD/HighD/LowD/CloseD`, `Highest`, `Lowest`, `BollingerBands`, `KeltnerChannel`, `MTKeltnerChannel`, `EMA/SMA/SMMA/LWMA/TEMA`, `LinearRegression`, `ParabolicSAR`, `Ichimoku` |
| Rangos stop/limit | `ATR`, `MTATR`, `BBRange`, `BarRange`, `BiggestRange`, `SmallestRange` |

Rangos relevantes (A): periodo global `minPeriod="4" maxPeriod="200"`, shift `1–1`; ADX `Level 20–90/10`; ATR
`Level 0.01–100`; StdDev `Level 0.0001–1`; MACD `Level ±0.1/±0.2`; Momentum `Level 0–200/5`; AWO `±10`; RSI/Stoch
`Level 0–100/5`; LaguerreRSI `Gamma 0–0.95`, `Level 0.05–0.95`; Bollinger `Deviation 0.5–3`; Keltner `0.1–3`;
PSAR `Step 0.001–0.04`, `Maximum 0.1–0.4`; `HighestInRange Time From/To 0–2359/30`; `IsGreaterCount Bars 2–10`.
Rangos de constantes de indicador (`indicatorMin/Max/Step`): ATR `-5000..5000/0.001`, MACD `-5..5/0.001`, RSI `0..100/0.5`,
StdDev `0..1/0.01`, Stochastic `0..100/1`, BullsPower `-0.5..0.5/0.01`, Highest/LowestInRange `-1000..1000/1`.

**Tipos de orden** (`Blocks/OrderTypes`, A): `EnterAtMarket use="true"`; `EnterAtStop`, `EnterAtLimit` y
`EnterReverseAtMarket` **`use="false"`** (`BarsValid 2–10` inactivo). Dentro de los bloques de orden,
`#ExitAfterBars.ExitAfterBars# 5–20`.

**Tipos de salida** (`Blocks/ExitTypes`, A):

| Salida | `use` | `probability` | Valores |
|---|---|---|---|
| `StopLoss.StopLoss` | true | 100 | `ATRBasedValue` y `PctValue` activos, `FixedValue` no |
| `ProfitTarget.ProfitTarget` | true | 100 | ídem |
| `TrailingStop.TrailingStop` | true | 50 | fijo 50–100 pips o 1–5 × ATR(periodo global) |
| `TrailingStop.TrailingActivation`, `MoveSL2BE.*`, `ExitAfterBars` (2–15), `_ExitRule_` | false | 50 | — |

**SL/PT** (`WhatToBuild/SLPTOptions`, A): `SLRequired=true`, `SLATR=true` 1–3 × ATR(20–100); `PTRequired=true`,
`PTATR=true` 2–5 × ATR(20–100); `LimitSLPTRRR=true` 100–500 (PT = 1 a 5 veces el SL); `SeparatedSettings=true`;
pips fijos (30–80 / 60–200) y porcentaje (1–10 %) desactivados.

**Complejidad** (A): condiciones de entrada 0–0, de salida 1–3, tipos de salida 1–5, periodo 4–200, shift 1–1.

**Opciones de trading** (`Options/BuildTradingOptions`, A): `LimitTimeRange=true` de `5400` (01:30) a `84600`
(23:30), `ExitAtEndOfRange=false`; `ExitAtEndOfDay=false`; `ExitOnFriday=false`; `DontTradeOnWeekends=false`
(con `FridayCloseTime=2280` y `SundayOpenTime=2280`, valores anómalos pero inactivos); `MaxTradesPerDay=0` (sin
límite); `MaxDistanceFromMarket=false` (6 %); `Min/MaximumSL/PT=0` (sin límites); `ReservedBars=50`;
`RealisticGapsHandling=true`; `Session`/`MarketOpenSession = No Session`; parámetros `Picker*` (stock picker) irrelevantes en FX.

(B, alta) La ventana 01:30-23:30 sirve para no generar señales en el *rollover* (00:00 servidor), cuando el spread se dispara.

(B, alta) Con plantilla y 0 condiciones de entrada, los 204 bloques activos **sólo intervienen si la plantilla tiene
huecos aleatorios** (condiciones de salida, niveles de orden). (C) si los tiene. El rango de condiciones de salida
1–3 sólo actúa si la plantilla define reglas de salida aleatorias, porque `_ExitRule_` está desactivado.

### 4. Lógica de breakout
- (A) **Nada en el `.cfx` define el nivel roto.** La única referencia explícita es la nota "Breakout strategies setup".
- (B, alta) El breakout está en la plantilla `Template_DOW_H1_BUY_1.8.4.sqx` → **(C)** qué nivel usa (máximo de N
  velas, rango horario, máximo diario…), cómo confirma y cómo entra.
- (B, media) Como sólo `EnterAtMarket` está activo, si la plantilla tuviera la orden como hueco aleatorio la entrada
  sería a mercado tras la señal (confirmación por cierre/apertura), no con orden stop en el nivel.
- Bloques disponibles que podrían formar un breakout: `BarOpensAboveHighestAfterOpenBelow` (Donchian), señales de
  Bollinger "abre por encima de la banda tras abrir por debajo", `IchimokuKumoBreakoutBullish`, `Highest`/`HighestInRange`
  + `CrossesAbove`, niveles `HighD`/`LowD`.

### 5. Gestión de dinero y riesgo
- (A) `InitialCapital=10000`; `Method type="FixedAmount" use="true"`: `RiskedMoney=100`, `Decimals=2`,
  `LotsIfNoMM=0.01`, `MaxLots=100`. Resto de métodos `use="false"`. `RiskManagement maxDrawdown="30"` con
  `AllowAllTrades use="true"`.
- (B, alta) **Riesgo fijo de 100 (1 % del capital inicial) por operación**, calculado sobre la distancia del SL en
  ATR → el tamaño se adapta a la volatilidad. No compone (riesgo constante): las métricas son comparables en el tiempo.
  Buena práctica.
- (A) Sin límite de operaciones diarias (`MaxTradesPerDay=0`) ni de posiciones abiertas (no hay parámetro activo).
- (C) Función de `maxDrawdown="30"`: sin efecto con `AllowAllTrades`.

### 6. Motor de generación
| Parámetro (A) | Valor | Lectura |
|---|---|---|
| `generationType` | `genetic-evolution` | Evolución genética con islas. |
| `PopulationSize` / `Islands` | 5 / 5 | 25 individuos por generación. |
| `MaxGenerations` | 10 | |
| `CrossoverProbability` / `MutationProbability` | 46 / 35 | |
| `MigrationModulo` / `MigrationRate` | 5 / 6 | Migra el 6 % cada 5 generaciones. |
| `InitGenerationType` / `DecimationCoef` | 1 / 1 | Población inicial aleatoria sin sobre-muestreo (B, media). |
| `BuildMode/Conditions` (filtro de población inicial) | Ret/DD ≥ 5, AvgBarsInTrade ≥ 2, Trades ≥ 250, Win% ≥ 35 (IS) | |
| `EvoRestartOnFinish` | true | Al acabar las 10 generaciones, reinicia. |
| `EvoRestartOnStagnation` | `status="true" fitnessType="10" generations="30"` | Reinicio si la fitness IS no mejora en 30 generaciones. |
| `FreshBloodReplaceSimilar` / `…Weakest` | true / false (10 %, 2) | Sustituye clones por sangre nueva. |
| `Rankings/StopCondition` | `type="never"` | Corre indefinidamente. |
| `Rankings/MaxStrategies` | 1000 | Tamaño del banco de resultados. |
| `Calibration` | `useMaxSteps="true" maxSteps="50" calibrateBeforeStart="false"` | (B, media) calibración de niveles constantes. |

**Crítica (B, alta):** 5 individuos por isla y 10 generaciones no permiten que el algoritmo genético funcione: el cruce
entre 5 individuos casi no explora, `6 %` de 5 = 0,3 individuos (la migración es nula en la práctica) y el reinicio por
estancamiento a 30 generaciones **nunca puede saltar** con un máximo de 10. En la práctica es una **búsqueda aleatoria
con micro-evolución y reinicios continuos**. Con la entrada fija de la plantilla el espacio de búsqueda es pequeño
(sólo salidas), lo que lo hace menos grave que en el archivo 3, pero sigue siendo un diseño incoherente.

### 7. Filtrado y ranking
- (A) `FitnessCriteria … <Ranking type="ReturnDDRatio"/>` → fitness = **beneficio neto / drawdown máximo**.
- (A) `Rankings/Conditions` (todas IS, `resultType="main"`, `ConditionsType=1`): `AvgBarsInTrade ≥ 2`,
  `ReturnDDRatio ≥ 8`, `NumberOfTrades ≥ 300` (con `format="Decimal2"`, cosmético), `WinningPct ≥ 40`.
- (A) `DismissTooSimilarStrategies=true`; `AutomaticDismissal` con 10 problemas activados; `FitPortfolio active="false"`
  (correlación máx. 0,3); `CustomAnalysis method="none"`.
- (B) Efectos: Ret/DD ≥ 8 en 7,25 años ≈ 1,1 por año; ≥300 operaciones ≈ 41/año; `AvgBarsInTrade ≥ 2` evita operaciones
  de una vela (ambiguas en H1). **Win% ≥ 40 combinado con PT 2-5 ATR y SL 1-3 ATR empuja hacia ratios PT/SL bajos**,
  contradiciendo en parte el rango R:R 1-5.
- **Mala práctica (B, alta):** fitness y filtros se calculan **sobre la misma muestra** (no hay OOS en el Builder) y no
  hay filtro de Profit Factor ni de estabilidad → sesgo de selección; se confía todo al Retest posterior.

### 8. Pruebas de robustez
- (A) `CrossChecks use="true" evaluateAll="true"`, pero **todos los cross checks tienen `use="false"`**: no se ejecuta
  ninguno en el Builder.
- (A) Configuraciones inactivas presentes: `RetestOnAdditionalMarkets` (GBPJPY 2013.09.29–2020.12.30; PF > 1,1);
  `WalkForwardOptimization` (`type="1" period="10" optimization="15"`, `Param1=20`, `Param2=10`, `MaxTests=100`,
  umbral 80 %: beneficio OOS > 0, beneficio WF > 60 % (en % del IS, B media), % de ejecuciones rentables > 70,
  máx. beneficio en una ejecución < 50 %, > 20 operaciones por ejecución, DD por ejecución ≤ 25 %); `RetestWithHigherPrecision` (`Precision=2`, `Spread=3`;
  beneficio ≥ 80 %, operaciones ≥ 80 %, DD < 130 % del original); `MonteCarloRetest` (datos ±30 %, distancia mínima
  0–10, deslizamiento 0–5, spread 1–5, vela de inicio 100, parámetros 10 %/20 %; **sólo 10 simulaciones**);
  `WalkForwardMatrix` (10–40/10 × 5–20/5, 2×2); `MonteCarloManipulation` (*resampling*, saltar 10 %, 30 sims);
  `OptProfileSysParamPermutation` (1.000 tests, ≥ 30 % rentables); `WhatIf` (sin las 2 mejores/peores, sin condiciones);
  `SequentialOptimization`.
- (B, alta) Es deliberado: la robustez se hace en el Retest (archivo 2).

### 9. Dependencias entre secciones (qué cambia en cascada)
1. `StrategyType=template` ⇄ `RulesComplexity` (entrada 0–0) ⇄ `BuildingBlocks`: pasar a `simple` exige condiciones
   de entrada > 0 y convierte la selección de bloques en la lógica de entrada.
2. `SLPTOptions` ⇄ `ExitTypes` (los valores centinela `-1000005…-1000016` apuntan a `SLPTOptions`) ⇄ `FixedAmount`
   (el lote sale de la distancia del SL) ⇄ filtro `WinningPct`.
3. `minPeriod/maxPeriod` ⇄ todos los parámetros con centinela de periodo ⇄ `ReservedBars` (**50 < 200**: los
   indicadores largos se calculan con historia incompleta al inicio).
4. `Chart@timeframe` ⇄ periodos ATR, `ExitAfterBars`, `BarsValid`, ventana horaria (en H4/D1 la ventana 01:30-23:30
   cambia de significado).
5. `Chart@symbol` ⇄ spread, comisión, swap, `minDist` ⇄ bloques con **niveles absolutos** (ATR, StdDev, MACD, AWO,
   BullsPower).
6. `BuildTradingOptions` del Builder ⇄ las del Retest: si difieren, el Retest no reproduce lo construido.
7. `Setup@dateTo=2020.12.31` ⇄ OOS del Retest `2021.01.01`: el *holdout* sólo es limpio si el Builder no ve 2021+.
8. `FitnessCriteria` ⇄ `EvoRestartOnStagnation@fitnessType` ⇄ ranking del banco de resultados.

### 10. Tabla resumen
| Parámetro | Valor | Función | Efecto en el resultado |
|---|---|---|---|
| `StrategyType@type` | template | Construir sobre plantilla | La entrada viene dada; el Builder sólo explora salidas. Irreproducible sin el `.sqx`. |
| `MarketSides@type` | long | Sólo compras | Mitad del espacio; sesgo alcista del periodo favorece. |
| `Chart@symbol` / `timeframe` | GBPJPY_M1_M1_UTCPlus02 / H1 | Mercado de prueba | Resultados sólo válidos para ese símbolo/horario. |
| `Setup dateFrom–dateTo` | 2013.09.30–2020.12.31 | Periodo de construcción | 7,25 años; deja 2021-2024 para OOS. |
| `OutOfSample` | vacío | Sin validación | Selección sobre IS → sobreajuste. |
| `testPrecision` | 1 | Simulación M1 | Precisión razonable en H1. |
| `spread`/`slippage` | 2 / 0 | Costes | Deslizamiento nulo: optimista. |
| `Commission` / `Swap` | 0,7 / -7,67, +4,3, viernes | Costes | **Del US30, no de GBPJPY**: resultados de carry erróneos. |
| `LimitTimeRange` | 01:30–23:30 | Ventana de señales | Evita el rollover. |
| `ReservedBars` | 50 | Calentamiento | Insuficiente para periodos de hasta 200. |
| `minPeriod–maxPeriod` | 4–200 | Rango de periodos | Amplio: más grados de libertad. |
| `minConditions–maxConditions` | 0–0 | Entrada aleatoria | Ninguna (entrada en plantilla). |
| `minExitTypes–maxExitTypes` | 1–5 | Nº de tipos de salida | Sólo hay 3 disponibles. |
| `OrderTypes` | sólo `EnterAtMarket` | Tipo de orden | Sin órdenes stop: no se entra "en el nivel". |
| `SLRequired`/`SLATR` | true / 1–3 × ATR(20–100) | Stop loss | Riesgo acotado y adaptativo. |
| `PTRequired`/`PTATR` | true / 2–5 × ATR(20–100) | Objetivo | Siempre hay objetivo. |
| `LimitSLPTRRR` | 100–500 | R:R | PT 1-5 × SL; con SL/PT en ATR SQX puede no respetarlo (B, media). |
| `TrailingStop` | 50 %, 50–100 pips o 1–5 ATR | Trailing | Pips fijos no trasladables entre mercados. |
| `FixedAmount RiskedMoney` | 100 | Riesgo por operación | 1 % fijo, no compuesto. |
| `PopulationSize`/`Islands`/`MaxGenerations` | 5/5/10 | Motor | Evolución ineficaz: casi búsqueda aleatoria. |
| `Crossover`/`Mutation` | 46/35 | Operadores | Cruce bajo. |
| `EvoRestartOnStagnation` | 30 gen. | Reinicio | Nunca actúa (máx. 10). |
| Filtro inicial | Ret/DD≥5, Trades≥250, Win≥35, Bars≥2 | Población inicial | Descarta candidatos pobres antes de evolucionar. |
| Fitness | ReturnDDRatio | Selección | Premia beneficio por unidad de DD. |
| Filtros finales | Ret/DD≥8, Trades≥300, Win≥40, Bars≥2 | Banco de resultados | Exigentes en IS, sin OOS ni PF. |
| `CrossChecks` | todos `use=false` | Robustez | Ninguna en el Builder. |
| `StopCondition` | never | Parada | Corre hasta parar a mano. |

---

## 1.2 Archivo 3 — `Ventaja_Build_ConfigInicial_H1_BUY.cfx`

Se documenta completo; lo idéntico al archivo 1 se indica como tal (verificado nodo a nodo: **los 472 bloques son
idénticos**, igual que `OrderTypes`, opciones de trading, datos y cross checks).

### 1. Propósito y módulo
- (A) `Task type="Build"`; `StrategyType type="simple"` (`templateFile="SQ3StrategyTemplateExample.sq4"`, no usado);
  `minConditions="1" maxConditions="3"`; `SLRequired=false`, `PTRequired=false`; sólo `ExitAfterBars` activo.
- (B, alta) **Test de ventaja de entradas**: genera entradas aleatorias (1-3 condiciones) y las evalúa con una salida
  neutra por tiempo y tamaño fijo, para medir si la entrada predice el movimiento posterior sin que SL/PT lo enmascaren.

### 2. Mercado y datos
- (A) Idéntico al archivo 1 (GBPJPY H1, 2013.09.30–2020.12.31, sin OOS, precisión 1, spread 2, deslizamiento 0,
  comisión 0,7, swap del US30).
- (A) `Resources/Symbols`: `GBPUSD_M1` (2003-05-05→2019-12-31, spread 2,5) y `EURUSD_M1` (2003-05-05→2019-12-31).
  (B, alta) Restos; no se usan.

### 3. Bloques de construcción
- (A) Mismos 204 bloques activos que el archivo 1, aquí **sí determinan la entrada**.
- (A) `OrderTypes`: sólo `EnterAtMarket`.
- (A) `ExitTypes`: `ExitAfterBars.ExitAfterBars use="true" probability="50"`, 2–15 velas; `StopLoss`, `ProfitTarget`,
  `TrailingStop`, `MoveSL2BE`, `_ExitRule_` → `use="false"`.
- (A) `SLPTOptions`: `SLATR=false` (1,5–3 × ATR(20–20)), `PTATR=false` (2–5 × ATR(20–30)), `LimitSLPTRRR=false` (50–80):
  valores inactivos.
- (A) Complejidad: entrada 1–3, salida 1–3 (sin efecto: `_ExitRule_` desactivado), tipos de salida 1–5, periodo 4–200,
  shift 1–1.
- (B, alta) Con `minExitTypes=1` y un único tipo de salida disponible, la salida temporal es efectivamente obligatoria
  aunque `probability="50"`. Ambigüedad: el bloque de orden define `#ExitAfterBars# 5–20` y `ExitTypes` define 2–15;
  (C) cuál prevalece.

### 4. Lógica de breakout
- (A) Ninguna condición obliga a que la entrada sea una ruptura: hay **146 señales genéricas con el mismo peso**.
- (B, alta) Sólo 12-16 de ellas son rupturas de nivel según cómo se cuenten (4 `BarOpens…Highest/Lowest…`, 2
  `IchimokuKumoBreakout*`, 6 señales de Bollinger "abre/cierra fuera de la banda" y, si se incluyen, 4 cruces de
  Kijun/Senkou), es decir, un 8-11 % del total. Con 1-3 condiciones elegidas al azar,
  **la mayoría de las estrategias generadas no son de ruptura**. El título "Breakout" no se refleja en la configuración.
- (B, alta) Además se permiten como entrada larga patrones bajistas (`BearishEngulfing`, `DarkCloud`, `ShootingStar`,
  `IchimokuKumoBreakoutBearish`…), incoherente con una tesis de ruptura alcista.
- (A) Entrada sólo a mercado: la ruptura se confirma con la señal y se entra en la apertura siguiente.

### 5. Gestión de dinero y riesgo
- (A) `Method type="FixedSize" use="true"`, `Size=1` (1 lote); `FixedAmount use="false"` (`RiskedMoney=100`,
  `Decimals=1`, `LotsIfNoMM=0.1`, `MaxLots=10`); `InitialCapital=10000`; `RiskManagement maxDrawdown="30"`.
- (B, alta) Tamaño fijo: correcto para comparar entradas (cada operación pesa igual). 1 lote de GBPJPY con 10.000 de
  capital es un apalancamiento de ~13:1 → el DD % es poco realista, pero Ret/DD (cociente) no se ve afectado.

### 6. Motor de generación
- (A) Igual que el archivo 1 salvo `PopulationSize=15` y filtro de población inicial `ReturnDDRatio ≥ 2` (resto igual:
  Bars ≥ 2, Trades ≥ 250, Win ≥ 35).
- (A) `StopCondition type="databank-full"` (para al llenar 1.000 estrategias).
- (B, alta) Mismas debilidades (15 × 5 islas, 10 generaciones, migración ≈ 0,9 individuos, reinicio inalcanzable) y
  aquí sí importan, porque el espacio de búsqueda (entradas de 204 bloques) es enorme.

### 7. Filtrado y ranking
- (A) Fitness `Ranking type="Weighted"` con **un único objetivo activo: `Stagnation` (`valueType="2"`, minimizar)**;
  los otros 104 objetivos `use="false"`.
- (A) Filtros: `AvgBarsInTrade ≥ 2`, `ReturnDDRatio ≥ 4`, `NumberOfTrades ≥ 300`, `WinningPct ≥ 40` (IS).
- (B, alta) La fitness ignora el beneficio: entre las estrategias que pasan los filtros, se prefieren las de menor
  periodo sin nuevos máximos, aunque ganen poco. Es una idea defendible (consistencia) pero tosca: depende de cuándo se
  produjo el último máximo y no pondera la magnitud de la ventaja. Mejor: SQN o Ret/DD + StagnationPct.

### 8. Pruebas de robustez
- (A) Idéntico al archivo 1: ningún cross check activo.

### 9. Dependencias
- Las del archivo 1 (puntos 3–8) más: `ExitTypes` (sólo `ExitAfterBars`) ⇄ `minExitTypes` ⇄ `SLRequired/PTRequired=false`;
  el rango de `ExitAfterBars` ⇄ timeframe (2–15 velas de H1 = 2–15 h); `FixedSize` ⇄ métricas en dinero.

### 10. Tabla resumen (sólo lo que difiere del archivo 1; el resto es idéntico)
| Parámetro | Valor | Función | Efecto en el resultado |
|---|---|---|---|
| `StrategyType@type` | simple | Generación libre | El Builder inventa la entrada con los 204 bloques. |
| `minConditions–maxConditions` | 1–3 | Complejidad de entrada | Hasta 3 condiciones: riesgo de sobreajuste moderado. |
| `SLRequired`/`PTRequired` | false/false | SL/PT | Sin SL/PT: se mide la entrada pura. |
| `ExitAfterBars` | 50 %, 2–15 velas | Única salida | Horizonte de 2-15 h. |
| `FixedSize Size` | 1 | Tamaño fijo | Operaciones comparables. |
| `PopulationSize` | 15 | Motor | Algo mejor que 5, aún insuficiente. |
| Filtro inicial Ret/DD | ≥ 2 | Población inicial | Más permisivo que el archivo 1. |
| Fitness | Weighted: sólo Stagnation | Selección | Ignora el beneficio. |
| Filtro final Ret/DD | ≥ 4 | Banco | Mitad que el archivo 1 (coherente con un test sin SL/PT). |
| `StopCondition` | databank-full | Parada | Para con 1.000 estrategias. |
| `Resources/Symbols` | GBPUSD_M1, EURUSD_M1 | Definiciones | Sin uso. |

---

## 1.3 Archivo 2 — `Estrategia_Retest_ConfigInicial_H1_BUY.cfx`

### 1. Propósito y módulo
- (A) `Task type="Retest"` → **Retester**. `Databanks`: entrada `Results` → salida `Results` (`retestSelected="true"`;
  nodo duplicado). `Notes`: "Breakout strategies setup".
- (B, alta) Re-evalúa las estrategias completas producidas por el archivo 1 sobre **todo el histórico, con OOS
  2021-2024** y les aplica tres pruebas de robustez.

### 2. Mercado y datos
- (A) GBPJPY H1, **2013.09.30 – 2024.07.22**, `OutOfSample/Range dateFrom="2021.01.01" dateTo="2024.07.22"` (≈33 %
  del periodo), precisión 1, spread 2, deslizamiento 0, comisión 0,7, swap del US30 (misma incoherencia).
- (A) Opciones de trading iguales al Builder salvo valores inactivos (`FridayCloseTime=57600`, `SundayOpenTime=86340`,
  `EODExitTime=55800`, `FridayExitTime=82740`).

### 3. Bloques de construcción
- No aplica (el Retester no genera estrategias). No hay sección `Blocks` ni `Resources`.

### 4. Lógica de breakout
- No aplica; ningún filtro ni cross check comprueba que la estrategia sea de ruptura.

### 5. Gestión de dinero y riesgo
- (A) `FixedAmount use="true"`, `RiskedMoney=100` (como el Builder); `InitialCapital=10000`. Incluye `CryptoSizeByPrice`
  (inactivo), ausente en el Builder.

### 6. Motor
- No aplica (sin evolución). Coste computacional (B, alta): **SPP de 15.000 backtests con precisión M1 + Monte Carlo
  de 1.000 backtests** por estrategia es muy elevado; con 1.000 estrategias en el banco, impracticable sin preselección.

### 7. Filtrado y ranking
- (A) Fitness `ReturnDDRatio`. `Rankings/Conditions` (con `resultType="portfolio"`): Ret/DD IS ≥ 6, beneficio IS ≥ 50.000,
  beneficio OOS ≥ 0, operaciones IS ≥ 700, AvgBars ≥ 2, Win% ≥ 40, Ret/DD completo ≥ 6 — **todas `use="false"`**.
- (A) `DeleteFailedStrategies=false`, `ForceRunCrossChecks=false`, `StopCondition never`.
- (B, alta) Tal como está, **el Retest no filtra nada** y tampoco borra las que fallan los cross checks: hay que ordenar
  y filtrar el banco a mano. Las condiciones son un "menú" que el autor activa según el caso.

### 8. Pruebas de robustez (`CrossChecks use="true" evaluateAll="false"`: se detiene en el primer fallo)
| Cross check | `use` | Configuración (A) | Aceptación (A) | Valoración (B) |
|---|---|---|---|---|
| `RetestWithHigherPrecision` | **true** | `Precision=2` (tick real, spread personalizado), `Spread=2` | Beneficio **OOS ≥ 0**; (operaciones ≥ 80 % y DD < 130 % del original: `use=false`) | Bien planteado, pero sólo exige OOS ≥ 0. Requiere datos tick. |
| `MonteCarloRetest` | **true** | `RandomizeHistoryDataOHLC` (O/H/L/C 100 %, `MaxChange=10` % del ATR(14), `KeepConnected`, gaps 100 %/10 %) + `RandomizeSpread 1–3`; 1.000 sims; `MCUseFullSample=true`; `MCBacktestPrecision=-1` | Beneficio IS al **nivel de confianza 100** ≥ 0; (DD ≤ 200 %: `use=false`) | Buena prueba de sobreajuste a los datos. El 100 % = el peor de 1.000 simulaciones: inestable y extremadamente exigente; además mide IS con muestra completa activada. Spread 1-3 incluye spreads menores que el base. |
| `OptProfileSysParamPermutation` (SPP) | **true** | 15.000 tests, ±20 %, 6 pasos; parametriza `Periods` y `ExitParamsUsed` | `ProfitOptPct=95` (sólo se evalúa este criterio) + 4 condiciones: Stagnation y Ret/DD del original dentro de [70 %, 130 %] de la mediana SPP | Concepto excelente (¿es el original un pico aislado?). Muestras mezcladas: lado izquierdo IS (10) en 3 condiciones y completo (127) en otra, frente al original en completo. 95 % rentables es muy estricto. |
| `RetestOnAdditionalMarkets` | false | **Dos setups idénticos de GBPJPY** 2019.12.02–2024.07.22 | Mercado 2 ≥ 70 % del mercado 1 | Error de configuración: el "mercado adicional" es el mismo símbolo. |
| `MonteCarloManipulation` | false | `exact`, saltar 10 %, 1.000 sims | Beneficio al 80 % ≥ 50 % de… **otro resultado de MC** (`resultType="MonteCarloManipulation"`); Stagnation al 95 % ≤ 300 % del original | La primera condición compara MC contra MC: error. `exact` sólo permuta el orden (no cambia el beneficio neto). |
| `WhatIf` | false | Excluir 5 % mejores y 5 % peores | PF ≥ 70 % del original | Buena prueba de dependencia de outliers, desactivada. |
| `WalkForwardOptimization`, `WalkForwardMatrix`, `SequentialOptimization` | false | Como en el Builder; Sequential ±20 %, 40 pasos, 80 % | — | La validación walk-forward no se usa. |

### 9. Dependencias
1. El timeframe, el símbolo y las **opciones de trading** deben coincidir con los del Builder que generó las estrategias.
2. `OutOfSample 2021.01.01` debe ser posterior al `dateTo` del Builder (2020.12.31): se cumple.
3. `MCBacktestPrecision=-1` hereda `testPrecision` (B, media) → el coste del MC escala con la precisión.
4. SPP ⇄ parámetros de la estrategia (sólo `Periods` y salidas usadas): si la estrategia tiene niveles constantes,
   no se perturban.
5. `evaluateAll=false` ⇄ orden de los cross checks: los que fallan antes ahorran el resto.

### 10. Tabla resumen
| Parámetro | Valor | Función | Efecto en el resultado |
|---|---|---|---|
| `Setup dateFrom–dateTo` | 2013.09.30–2024.07.22 | Periodo de retest | Incluye 3,5 años no vistos. |
| `OutOfSample/Range` | 2021.01.01–2024.07.22 | Holdout | Validación limpia si el Builder no vio 2021+. |
| `FixedAmount` | 100 | Riesgo | Igual que el Builder: resultados comparables. |
| Fitness | ReturnDDRatio | Orden del banco | Igual que el Builder. |
| `Rankings/Conditions` | todas `use=false` | Filtros | **No filtra**. |
| `DeleteFailedStrategies` | false | Limpieza | Las que fallan permanecen en el banco. |
| `evaluateAll` | false | Ejecución | Para en el primer cross check fallido. |
| HP `Precision`/`Spread` | 2 / 2 | Tick real | Detecta estrategias que dependen de la simulación M1. |
| HP aceptación | OOS ≥ 0 | Filtro | Laxo (no controla operaciones ni DD). |
| MC métodos | OHLC ±10 % ATR, spread 1–3 | Perturbación | Robustez frente a datos y costes. |
| MC simulaciones | 1.000 | Precisión estadística | Muy costoso. |
| MC aceptación | Beneficio IS @100 ≥ 0 | Filtro | Peor caso: muy estricto e inestable. |
| SPP | 15.000 tests, ±20 %, 6 pasos | Sensibilidad de parámetros | Coste muy alto. |
| SPP aceptación | ≥95 % rentables + bandas 70-130 % | Filtro | Estricto; muestras mezcladas. |
| AdditionalMarkets | GBPJPY ×2, desactivado | Multi-mercado | Mal configurado. |

---

## 1.4 Archivo 4 — `Ventaja_Retest_ConfigInicial_H1_BUY.cfx`

### 1. Propósito y módulo
- (A) `Task type="Retest"`. (B, alta) Valida la robustez de las **entradas con ventaja** del archivo 3 antes de
  convertirlas en plantilla.

### 2. Mercado y datos
- (A) Idéntico al archivo 2 (2013.09.30–2024.07.22, OOS 2021.01.01–2024.07.22, mismos costes y opciones).

### 3–4. Bloques y breakout
- No aplica (Retester).

### 5. Gestión de dinero
- (A) `FixedSize use="true"` (`Size=1`); `FixedAmount use="false"` (`LotsIfNoMM=0.1`, `MaxLots=10`). Coherente con el
  archivo 3.

### 6. Motor
- No aplica. Mismo coste computacional que el archivo 2.

### 7. Filtrado y ranking
- (A) Fitness `Weighted` con sólo `Stagnation` (minimizar), como el archivo 3. Catálogo de 107 objetivos (incluye
  `VaR`, `CVaR`). Mismas 7 condiciones, todas `use="false"`.

### 8. Pruebas de robustez
- (A) Idénticas al archivo 2 (HP, MC y SPP activos) **salvo el SPP**, que aquí sólo tiene las 2 condiciones de
  `Stagnation` (sin las de Ret/DD).
- (B, media) En un test de ventaja, `ExitParamsUsed` del SPP perturba la salida temporal (`ExitAfterBars`), lo que mide
  la sensibilidad de la ventaja al horizonte: muy pertinente.

### 9. Dependencias
- Las del archivo 2; además, el tamaño fijo hace que las condiciones en dinero (beneficio ≥ 0) sean independientes del
  capital.

### 10. Tabla resumen (diferencias con el archivo 2)
| Parámetro | Valor | Función | Efecto |
|---|---|---|---|
| `FixedSize Size` | 1 | Tamaño | Igual que el Builder de ventaja. |
| Fitness | Weighted: Stagnation | Orden | Ignora el beneficio. |
| SPP condiciones | 2 (Stagnation 70–130 %) | Filtro | Menos exigente que el archivo 2. |
| Resto | = archivo 2 | — | — |

---

## 1.5 Errores, incoherencias y malas prácticas (ordenados por gravedad)

| # | Gravedad | Hallazgo | Archivos | Evidencia (A) | Consecuencia |
|---|---|---|---|---|---|
| 1 | Crítica | La lógica de entrada depende de una plantilla `.sqx` externa no incluida | 1 | `StrategyType type="template" templateFile=…Template_DOW_H1_BUY_1.8.4.sqx` | El archivo 1 no es reproducible; el *breakout* es una caja negra. |
| 2 | Crítica | Costes del US30 aplicados a GBPJPY; deslizamiento 0 | 1-4 | `Swap long="-7.67" short="4.3" tripleSwapOn="FRIDAY"`, `Commission 0.7`, `slippage="0"` | Resultados de carry y costes erróneos; sobreestimación. |
| 3 | Alta | Builders sin OOS: fitness y filtros sobre la misma muestra | 1, 3 | `<OutOfSample showGraph="false"/>` vacío | Sesgo de selección; todo se fía al Retest. |
| 4 | Alta | Motor genético degenerado | 1, 3 | `PopulationSize` 5/15, `MaxGenerations 10`, `MigrationRate 6`, `EvoRestartOnStagnation generations="30"` | Búsqueda casi aleatoria; reinicio por estancamiento inalcanzable. |
| 5 | Alta | "Breakout" no impuesto en el Builder de ventaja | 3 | 146 señales genéricas con peso 1; `EnterAtStop use="false"` | La mayoría de entradas no son rupturas. |
| 6 | Alta | Retest sin filtros y sin borrar fallidas | 2, 4 | condiciones `use="false"`, `DeleteFailedStrategies=false` | El "filtrado" es manual. |
| 7 | Media | Bloques con niveles absolutos dependientes de la escala de precio | 1, 3 | ATR `Level 0.01–100`, StdDev `0.0001–1`, MACD `±0.2`, AWO `±10`, BullsPower `±0.5` | En GBPJPY/US30 muchas condiciones son siempre verdaderas o falsas: ruido y falsa complejidad. |
| 8 | Media | Osciladores con niveles 0–100 sin restringir y patrones bajistas en un sistema sólo largo | 1, 3 | `RSICrossUp Level 0–100`, `BearishEngulfing use="true"` | Incoherencia con la tesis. |
| 9 | Media | Aceptación MC al 100 % (peor caso) sobre IS | 2, 4 | `confidenceLevel="100" sampleType="10"` | Inestable; depende de una sola simulación. |
| 10 | Media | Condición de MC-manipulación comparada contra otro MC | 2, 4 | `Right-Side … resultType="MonteCarloManipulation"` | Condición sin sentido (inactiva). |
| 11 | Media | SPP con muestras mezcladas (IS frente a completo) | 2, 4 | `sampleType="10"` frente a `sampleType="127"` | Comparación incoherente. |
| 12 | Media | "Mercado adicional" = el mismo GBPJPY dos veces | 2, 4 | dos `Setup` idénticos | La prueba multi-mercado no prueba nada. |
| 13 | Media | `LimitSLPTRRR` con SL/PT en ATR de periodos distintos | 1 | `LimitSLPTRRR=true` + `SLATR`/`PTATR` | SQX puede no respetarlo (B, media); además choca con `WinningPct ≥ 40`. |
| 14 | Media | `ReservedBars=50` con periodos hasta 200 | 1, 3 | `ReservedBars 50`, `maxPeriod 200` | Señales al inicio con indicadores sin calentar. |
| 15 | Media | Horas `HighestInRange` 0–2359 con paso 30 | 1, 3 | `Time From/To 0..2359/30` | Genera horas HHMM inválidas (0060, 0090…) (B, media). |
| 16 | Media | Fitness "sólo Stagnation" | 3, 4 | `Goal use="true" type="Stagnation"` | Ignora la magnitud del beneficio. |
| 17 | Baja | Zona `Asia/Jerusalem` para emular hora de bróker | 1 | `timezone="Asia/Jerusalem"` | Desfase de 1 h algunas semanas al año. |
| 18 | Baja | Valores anómalos/inactivos y restos | 1-4 | `FridayCloseTime=2280`, símbolos sin uso en `Resources`, `Databanks` duplicado, `NumberOfTrades format="Decimal2"` | Ruido; confunde al usuario. |
| 19 | Baja | Trailing en pips fijos (50–100) | 1 | `RangeLevel.FixedValue 50–100` | No trasladable entre mercados ni timeframes. |
| 20 | Baja | Ambigüedad del rango de salida temporal | 1, 3 | `#ExitAfterBars# 5–20` en órdenes vs `2–15` en `ExitTypes` | (C) cuál prevalece. |

**Aciertos del autor** (para conservarlos): flujo en dos etapas ventaja → estrategia; *holdout* 2021-2024 nunca visto
por el Builder; SL en ATR y riesgo fijo no compuesto; ventana horaria que evita el rollover; precisión M1; Retest con
tick real; Monte Carlo de OHLC; SPP como prueba anti-sobreajuste.

## 1.6 Lo que no se ha analizado en detalle (y por qué)

- **Los 2.183 conjuntos de parámetros predefinidos** (`Predefined/Params`, p. ej. RSI con periodo fijo 14/20/30…): todos
  `changed="false"` (valores por defecto de SQX). (C) si SQX los usa además de los rangos generados; por prudencia, al
  acotar un rango en las versiones nuevas se acota también en los conjuntos predefinidos.
- **Los 268 bloques inactivos** del catálogo: se listaron para elegir los de cada estilo (todos los usados en Fase 3
  existen en este catálogo), pero no se describe cada uno.
- **Opciones de *stock picker*** (`Picker*`), `ATMs` (desactivado, sin salidas) y `PartsToImprove` (sólo actúa en modo
  "mejorar estrategias"): sin efecto en estas tareas.
- **Lógica de la plantilla `.sqx`**: no recibida (C).
