# Fase 3 — Fichas de diseño por estilo

Documento generado por `tools/generar_fichas.py`: las tablas "Original → Nuevo" se leen de los XML, por lo que coinciden con los `.cfx` de `configs/`. El detalle exhaustivo (cada valor modificado) está en `docs/cambios/`.

## Preguntas abiertas (máximo 5)

Se formulan antes de diseñar; al no tener respuesta se continúa con los supuestos de la tabla siguiente. Cualquier respuesta distinta se traslada cambiando `tools/estilos.py` y regenerando.

1. **Instrumento y bróker reales.** Los originales mezclan una plantilla de US30 (Dow, costes de Darwinex: swap -7,67/+4,30 con triple swap en viernes, comisión 0,7) con datos de GBPJPY. ¿Sobre qué símbolo(s) vas a operar y cuáles son su spread típico, comisión por lote y swaps?
2. **Datos disponibles en SQX.** ¿Desde qué año tienes M1 para cada símbolo? ¿Tienes datos tick con spread real (necesarios para la precisión 3 de Scalping y Noticias)? ¿El símbolo `*_UTCPlus02` es UTC+2 fijo o UTC+2/+3 con horario de verano de Nueva York?
3. **Capital y riesgo.** ¿Capital inicial, riesgo por operación y drawdown máximo tolerable?
4. **Dirección y plataforma.** ¿Sólo largos (como los originales "BUY") o también cortos? ¿Ejecutarás en MT4, MT5 u otra plataforma?
5. **Noticias.** ¿Dispones de un calendario económico histórico (CSV) o de MT5 (que tiene calendario nativo)? ¿Aceptas la aproximación por ventana horaria descrita en la Fase 2?

## Supuestos explícitos

| Id | Tema | Supuesto |
|---|---|---|
| S1 | Símbolo | Se conserva `GBPJPY_M1_M1_UTCPlus02` en los 64 archivos para que carguen en tu instalación (es el único símbolo presente en los Setup de los 4 originales). Cada ficha indica el instrumento recomendado; cámbialo en *Data* antes de ejecutar. |
| S2 | Costes | Se conservan los costes del original (spread 2, comisión SizeBased 0,7, swap -7,67/+4,30 triple viernes) porque no conozco tu bróker; **son incoherentes con GBPJPY** y deben corregirse (checklist, punto 3). Sólo se cambia el deslizamiento (0 → 0,3-1,5 según estilo). |
| S3 | Datos | M1 disponible de 2013.09.30 a 2024.07.22 (el rango que usan los originales). |
| S4 | Partición temporal | Se conserva la partición del autor: construcción hasta 2020.12.31 y OOS final 2021.01.01-2024.07.22 en el Retest (nunca visto por el Builder). Se añade un tramo de validación dentro del Builder (2019-2020, o 2019.07-2020 en M5/M15). |
| S5 | Horario del servidor | UTC+2 en invierno / UTC+3 en verano siguiendo el cambio de hora de EE. UU. (convención "cierre de Nueva York = 00:00"). Con ella, 8:30 ET = 15:30 servidor todo el año. |
| S6 | Dirección | Dos kits por estilo: BUY (*Market sides* = long, como los originales) y SELL (*Market sides* = short) con los bloques y niveles espejados. El valor `short` del XML es deducido (sólo hay `long` en los originales): verifica la dirección al importar. |
| S7 | Capital y riesgo | 10.000 de capital; riesgo fijo 0,5 % (alta frecuencia) o 1 % por operación; drawdown máximo tolerable 20 % (25 % en Position/Trend). |
| S8 | Build | Los archivos son de la build 140.2099. Se asume que la build 144 los importa (SQX suele mantener compatibilidad hacia atrás), pero **no está verificado**. |

## Estructura común de cada kit

Cada estilo tiene **dos kits idénticos salvo la dirección**: BUY (`Market sides` = long) y SELL (`Market sides` = short, bloques y niveles espejados). Cada kit conserva la arquitectura de dos etapas del autor, que es su principal acierto:

1. **`Ventaja_Build`** busca *entradas* con ventaja usando sólo una salida temporal y tamaño fijo (sin SL/PT), para medir la entrada aislada.
2. **`Ventaja_Retest`** comprueba la robustez de esa ventaja (tick real, Monte Carlo, SPP, OOS 2021-2024).
3. **`Estrategia_Build`** genera la estrategia completa (entrada + SL/PT/trailing/salidas) con riesgo fijo. *Cambio metodológico*: el original usaba una plantilla externa con la entrada fija; los nuevos están en modo `simple` para funcionar sin ese archivo (docs/04 §A.3 explica cómo volver al modo plantilla).
4. **`Estrategia_Retest`** valida la estrategia completa con los mismos tests y el holdout 2021-2024.

Índice: [Scalping](#scalping) · [DayTrading](#daytrading) · [Swing](#swing) · [Position](#position) · [TrendFollowing](#trendfollowing) · [Range](#range) · [PriceAction](#priceaction) · [NewsProxy](#newsproxy)

---

## Scalping

**Scalping (micro-ruptura en sesión líquida)** · timeframe `M5`

> **Viabilidad:** Scalping de ticks/segundos (libro de órdenes, latencia) **no es viable en SQX**: el motor trabaja con barras (mínimo M1). Esta ficha es la alternativa más cercana (M5). Si no tienes datos tick con spread real ni spreads brutos ≤0,3 pips, usa la ficha Day Trading.

**Archivos del kit** (todos *no validados en SQX*; tabla completa de cambios en `docs/cambios/`):

| Rol | BUY | SELL |
|---|---|---|
| EB | [`Estrategia_Build_ConfigInicial_H1_BUY__Scalping_M5_BUY.cfx`](cambios/Estrategia_Build_ConfigInicial_H1_BUY__Scalping_M5_BUY.md) | [`Estrategia_Build_ConfigInicial_H1_BUY__Scalping_M5_SELL.cfx`](cambios/Estrategia_Build_ConfigInicial_H1_BUY__Scalping_M5_SELL.md) |
| ER | [`Estrategia_Retest_ConfigInicial_H1_BUY__Scalping_M5_BUY.cfx`](cambios/Estrategia_Retest_ConfigInicial_H1_BUY__Scalping_M5_BUY.md) | [`Estrategia_Retest_ConfigInicial_H1_BUY__Scalping_M5_SELL.cfx`](cambios/Estrategia_Retest_ConfigInicial_H1_BUY__Scalping_M5_SELL.md) |
| VB | [`Ventaja_Build_ConfigInicial_H1_BUY__Scalping_M5_BUY.cfx`](cambios/Ventaja_Build_ConfigInicial_H1_BUY__Scalping_M5_BUY.md) | [`Ventaja_Build_ConfigInicial_H1_BUY__Scalping_M5_SELL.cfx`](cambios/Ventaja_Build_ConfigInicial_H1_BUY__Scalping_M5_SELL.md) |
| VR | [`Ventaja_Retest_ConfigInicial_H1_BUY__Scalping_M5_BUY.cfx`](cambios/Ventaja_Retest_ConfigInicial_H1_BUY__Scalping_M5_BUY.md) | [`Ventaja_Retest_ConfigInicial_H1_BUY__Scalping_M5_SELL.cfx`](cambios/Ventaja_Retest_ConfigInicial_H1_BUY__Scalping_M5_SELL.md) |

**Operaciones mínimas exigidas** (300/año): Builder IS ≥ 1050, OOS 2019-2020 ≥ 360 (≈1410 en 5.0 años de construcción); Retest periodo completo ≥ 2920 y holdout 2021-2024 ≥ 850.

### 1. Tesis

En las aperturas de Londres y el solape Londres-Nueva York entra liquidez direccional; tras una micro-consolidación, la ruptura de su extremo tiende a continuar unas pocas velas. La ventaja es pequeña y sólo existe si el coste total (spread+comisión+deslizamiento) es una fracción pequeña del ATR de M5.

### 2. Cambios respecto al original

#### 2.a Builder de estrategia completa (`Estrategia_Build`)

| Parámetro | Original | Nuevo | Justificación |
|---|---|---|---|
| Timeframe | H1 | M5 | Horizonte típico del estilo (M5). |
| Periodo de datos | 2013.09.30 – 2020.12.31 | 2016.01.04 – 2020.12.31 | M5/M15: 5 años dan miles de operaciones y reducen el cómputo; 2021-2024 sigue reservado (S4). |
| Tramo OOS | sin OOS | 2019.07.01 – 2020.12.31 | Validación dentro del Builder: el original filtraba sólo sobre IS. |
| Deslizamiento (pips) | 0 | 0.5 | El original usa 0; en M5 un deslizamiento de 0,5 pips por orden stop/mercado es conservador-realista y cambia el signo de muchas estrategias. |
| Modo de generación | template (plantilla externa .sqx) | simple | El original dependía de una plantilla .sqx no incluida; en modo simple el archivo es autónomo (docs/04 §A.3 para volver a plantilla). |
| Condiciones de entrada | 0–0 | 1–3 | Nivel + 1-2 filtros como máximo; más condiciones = más grados de libertad. |
| Periodos de indicadores | 4–200 | 5–100 | Periodos 5-100 velas de M5 (25 min a 8 h): horizonte de micro-estructura; ≥100 no aporta nada a un scalper y sobreajusta. |
| Desplazamiento (shift) | 1–1 | 1–1 | Sin cambio. |
| Tipos de salida (mín–máx) | 1–5 | 2–4 | SL obligatorio + salidas propias del estilo (el original pedía hasta 5 con 3 disponibles). |
| Tipos de orden | EnterAtMarket (w1) | EnterAtMarket (w1), EnterAtStop (w3, válida 1-3 velas) | Orden stop en el nivel de ruptura: entra sólo si la ruptura ocurre; validez 1-3 velas (5-15 min) para no comprar rupturas viejas. |
| Stop loss | obligatorio=true; 1-3 × ATR(20-100) | obligatorio=true; 1-2.5 × ATR(14-50) | SL/PT en ATR de M5 (adaptativos); break-even rápido; salida temporal 30 min-3 h: la ventaja de un scalp se agota en pocas velas. |
| Profit target | obligatorio=true; 2-5 × ATR(20-100); PT=100-500 % del SL | obligatorio=true; 1-3 × ATR(14-50); PT=80-250 % del SL | SL/PT en ATR de M5 (adaptativos); break-even rápido; salida temporal 30 min-3 h: la ventaja de un scalp se agota en pocas velas. |
| Trailing stop | sí (50 %), fijo 50-100 pips, 1-5 ATR | no | SL/PT en ATR de M5 (adaptativos); break-even rápido; salida temporal 30 min-3 h: la ventaja de un scalp se agota en pocas velas. |
| Break-even | no | sí (50 %), 0.5-1.5 ATR | SL/PT en ATR de M5 (adaptativos); break-even rápido; salida temporal 30 min-3 h: la ventaja de un scalp se agota en pocas velas. |
| Salida temporal | no | sí (50 %), 6-36 velas | SL/PT en ATR de M5 (adaptativos); break-even rápido; salida temporal 30 min-3 h: la ventaja de un scalp se agota en pocas velas. |
| Salida por regla | no | sí (30 %) | SL/PT en ATR de M5 (adaptativos); break-even rápido; salida temporal 30 min-3 h: la ventaja de un scalp se agota en pocas velas. |
| Ventana de señales | 01:30-23:30 | 09:00-18:30 + cierre al final | 18:30 servidor ≈ final del solape Londres-NY. |
| Cierres forzados | no diario; no viernes | diario 21:00; viernes 20:00 | Red de seguridad: nada abierto al cierre del día. |
| Máx. operaciones/día | 0 (sin límite) | 6 | Permite varias operaciones/día sin sobre-operar en días de ruido. |
| Distancia máx. orden | no | 0.3 % | 0,3 % ≈ 45 pips en GBPJPY; tope razonable para M5. |
| Bloques activos | 146 señales / 29 indicadores / 29 stop-limit | 91 señales / 48 indicadores / 40 stop-limit | Núcleo: ruptura de canal/bandas y de los extremos de la sesión asiática (pesos 4-10, y órdenes stop en esos niveles, que son las que materializan la ruptura). Filtros a peso 1: expansión de volatilidad, momentum, tendencia corta, fuerza y hora. Sin bloques de nivel absoluto. |
| Gestión monetaria | FixedAmount: riesgo 100 por operación | FixedAmount: riesgo 50 por operación | Riesgo fijo 0.5 % (no compuesto: Ret/DD comparable en el tiempo). |
| Fitness | type="ReturnDDRatio" | Weighted: ReturnDDRatio (peso 1, max), SQN (peso 2, max) | SQN premia expectativa consistente con muchas operaciones (lo propio de un scalper); Ret/DD evita curvas con drawdowns profundos. |
| Filtros (Ranking) | AvgBarsInTrade(IS) >= 2; ReturnDDRatio(IS) >= 8; NumberOfTrades(IS) >= 300; WinningPct(IS) >= 40 | NumberOfTrades(IS) >= 1050; ReturnDDRatio(IS) >= 6; WinningPct(IS) >= 45; ProfitFactor(IS) >= 1.25; AvgBarsInTrade(IS) >= 3; NetProfit(OOS) > 0; NumberOfTrades(OOS) >= 360 | Umbrales del estilo + exigencia OOS. |
| Filtro población inicial | ReturnDDRatio(IS) >= 5; AvgBarsInTrade(IS) >= 2; NumberOfTrades(IS) >= 250; WinningPct(IS) >= 35 | NumberOfTrades(IS) >= 320 | Sólo nº mínimo de operaciones (recomendación de SQX): con filtros de rentabilidad la población inicial puede tardar horas/días y el Builder no guarda nada mientras tanto. |
| Motor genético | población 5 × 5 islas, 10 generaciones, cruce 46 %, mutación 35 %, migración 6 % cada 5, reinicio por estancamiento a 30 | población 20 × 4 islas, 30 generaciones, cruce 80 %, mutación 30 %, migración 10 % cada 10, reinicio por estancamiento a 15 | 80-100 individuos por generación (el original 25-75) y 30 generaciones (el original 10, insuficiente para que la evolución actúe). |
| Calibración de indicadores | false | true | Recalibra los rangos de valores de indicadores y de rangos stop/limit (±5000 por defecto) para el símbolo y timeframe antes de construir. |

#### 2.b Builder de test de ventaja (`Ventaja_Build`)

| Parámetro | Original | Nuevo | Justificación |
|---|---|---|---|
| Timeframe | H1 | M5 | Horizonte típico del estilo (M5). |
| Periodo de datos | 2013.09.30 – 2020.12.31 | 2016.01.04 – 2020.12.31 | M5/M15: 5 años dan miles de operaciones y reducen el cómputo; 2021-2024 sigue reservado (S4). |
| Tramo OOS | sin OOS | 2019.07.01 – 2020.12.31 | Validación dentro del Builder: el original filtraba sólo sobre IS. |
| Deslizamiento (pips) | 0 | 0.5 | El original usa 0; en M5 un deslizamiento de 0,5 pips por orden stop/mercado es conservador-realista y cambia el signo de muchas estrategias. |
| Modo de generación | simple | simple | Sin cambio. |
| Condiciones de entrada | 1–3 | 1–3 | Sin cambio. |
| Periodos de indicadores | 4–200 | 5–100 | Periodos 5-100 velas de M5 (25 min a 8 h): horizonte de micro-estructura; ≥100 no aporta nada a un scalper y sobreajusta. |
| Desplazamiento (shift) | 1–1 | 1–1 | Sin cambio. |
| Tipos de salida (mín–máx) | 1–5 | 1–1 | Sólo la salida temporal (test de ventaja). |
| Tipos de orden | EnterAtMarket (w1) | EnterAtMarket (w1), EnterAtStop (w3, válida 1-3 velas) | Orden stop en el nivel de ruptura: entra sólo si la ruptura ocurre; validez 1-3 velas (5-15 min) para no comprar rupturas viejas. |
| Stop loss | obligatorio=false; sin ATR | obligatorio=false; sin ATR | Sin cambio. |
| Profit target | obligatorio=false; sin ATR | obligatorio=false; sin ATR | Sin cambio. |
| Trailing stop | no | no | Sin cambio. |
| Break-even | no | no | Sin cambio. |
| Salida temporal | sí (50 %), 2-15 velas | sí (100 %), 3-24 velas | Test de ventaja: salida pura por tiempo 15 min-2 h, sin SL/PT. |
| Salida por regla | no | no | Sin cambio. |
| Ventana de señales | 01:30-23:30 | 09:00-18:30 + cierre al final | 18:30 servidor ≈ final del solape Londres-NY. |
| Cierres forzados | no diario; no viernes | diario 21:00; viernes 20:00 | Red de seguridad: nada abierto al cierre del día. |
| Máx. operaciones/día | 0 (sin límite) | 6 | Permite varias operaciones/día sin sobre-operar en días de ruido. |
| Distancia máx. orden | no | 0.3 % | 0,3 % ≈ 45 pips en GBPJPY; tope razonable para M5. |
| Bloques activos | 146 señales / 29 indicadores / 29 stop-limit | 91 señales / 48 indicadores / 40 stop-limit | Núcleo: ruptura de canal/bandas y de los extremos de la sesión asiática (pesos 4-10, y órdenes stop en esos niveles, que son las que materializan la ruptura). Filtros a peso 1: expansión de volatilidad, momentum, tendencia corta, fuerza y hora. Sin bloques de nivel absoluto. |
| Gestión monetaria | FixedSize: 1 lote | FixedSize: 1 lote | Sin cambio. |
| Fitness | Weighted: Stagnation (peso 1, min) | Weighted: SQN (peso 2, max), StagnationPct (peso 1, min) | SQN mide la calidad estadística de la entrada; el original optimizaba sólo 'Stagnation', que ignora el beneficio. |
| Filtros (Ranking) | AvgBarsInTrade(IS) >= 2; ReturnDDRatio(IS) >= 4; NumberOfTrades(IS) >= 300; WinningPct(IS) >= 40 | NumberOfTrades(IS) >= 1050; ReturnDDRatio(IS) >= 3; WinningPct(IS) >= 40; ProfitFactor(IS) >= 1.15; AvgBarsInTrade(IS) >= 3; NetProfit(OOS) > 0; NumberOfTrades(OOS) >= 360 | Umbrales del estilo + exigencia OOS. Test de ventaja: Ret/DD a la mitad y PF ≥1,15. |
| Filtro población inicial | ReturnDDRatio(IS) >= 2; AvgBarsInTrade(IS) >= 2; NumberOfTrades(IS) >= 250; WinningPct(IS) >= 35 | NumberOfTrades(IS) >= 320 | Sólo nº mínimo de operaciones (recomendación de SQX): con filtros de rentabilidad la población inicial puede tardar horas/días y el Builder no guarda nada mientras tanto. |
| Motor genético | población 15 × 5 islas, 10 generaciones, cruce 46 %, mutación 35 %, migración 6 % cada 5, reinicio por estancamiento a 30 | población 20 × 4 islas, 30 generaciones, cruce 80 %, mutación 30 %, migración 10 % cada 10, reinicio por estancamiento a 15 | 80-100 individuos por generación (el original 25-75) y 30 generaciones (el original 10, insuficiente para que la evolución actúe). |
| Calibración de indicadores | false | true | Recalibra los rangos de valores de indicadores y de rangos stop/limit (±5000 por defecto) para el símbolo y timeframe antes de construir. |

#### 2.c Retesters (`Estrategia_Retest` / `Ventaja_Retest`)

| Parámetro | Original | Nuevo | Justificación |
|---|---|---|---|
| Timeframe | H1 | M5 | Debe coincidir con el Builder del estilo. |
| Periodo / OOS | 2013.09.30 – 2024.07.22; OOS 2021.01.01 – 2024.07.22 | 2013.09.30 – 2024.07.22; OOS 2021.01.01 – 2024.07.22 | Sin cambio. |
| Deslizamiento | 0 | 0.5 | El original usa 0; en M5 un deslizamiento de 0,5 pips por orden stop/mercado es conservador-realista y cambia el signo de muchas estrategias. |
| Ventana de señales | 01:30-23:30 | 09:00-18:30 + cierre al final | Idéntica al Builder: si difiere, el Retest no reproduce lo construido. |
| Cierres forzados | no diario; no viernes | diario 21:00; viernes 20:00 | Idénticos al Builder. |
| Gestión monetaria | FixedAmount: riesgo 100 por operación | FixedAmount: riesgo 50 por operación | Igual que el Builder correspondiente. |
| Fitness | type="ReturnDDRatio" | Weighted: ReturnDDRatio (peso 1, max), SQN (peso 2, max) | Igual que el Builder correspondiente. |
| Filtros (Ranking) | (ninguna activa) | NetProfit(OOS) > 0; ProfitFactor(OOS) >= 1.1; ReturnDDRatio(Full) >= 9; NumberOfTrades(Full) >= 2920; NumberOfTrades(OOS) >= 850; DrawdownPct(Full) <= 20 | El original no filtraba nada (todas use=false) ni borraba fallidas. |
| Mayor precisión | activo; precisión 2 (tick real + spread personalizado); 1 condiciones | activo; precisión 3 (tick real + spread real); 3 condiciones | Precisión 3 (tick real con spread real): en M5 el spread variable decide el resultado. |
| Monte Carlo retest | activo; 1000 sims; OHLC ±10 % ATR(14), spread 1-3. Acepta: NetProfit(IS) >= 0 | activo; 200 sims; OHLC ±10 % ATR(14), desliz. 0-1, spread 2-4. Acepta: NetProfit(Full) >= 0; DrawdownPct(Full) <= 150% de DrawdownPct[main] | Spread desde el base hasta 2-4x, deslizamiento, percentil 95 (no el peor caso) y control del DD. |
| Monte Carlo manipulación | no; orden de operaciones 'exact', saltar 10 % | activo; orden de operaciones 'resampling', saltar 10 % | Barato; 'resampling' y referencia corregida (el original comparaba MC contra MC). |
| SPP / perfil de optimización | activo; 15000 tests, ±20 %, 6 pasos; ≥95 % rentables | activo; 1500 tests, ±20 %, 6 pasos; ≥80 % rentables | Tests y exigencia ajustados al coste de cómputo y a la sensibilidad del estilo. |
| What-if | no; ExcludePctTradesWithBiggestPl, ExcludePctTradesWithLowestPl | activo; ExcludePctTradesWithBiggestPl, ExcludePctTradesWithLowestPl | Quitar el 5 % de extremos: el estilo no debe depender de outliers. |

Diferencias del `Ventaja_Retest` respecto al anterior:

- **Gestión monetaria:** FixedSize: 1 lote
- **Fitness:** Weighted: SQN (peso 2, max), StagnationPct (peso 1, min)
- **Filtros (Ranking):** NetProfit(OOS) > 0; ProfitFactor(Full) >= 1.1; NumberOfTrades(Full) >= 2920; NumberOfTrades(OOS) >= 850

### 3. Indicadores y bloques seleccionados

Criterio general: Núcleo: ruptura de canal/bandas y de los extremos de la sesión asiática (pesos 4-10, y órdenes stop en esos niveles, que son las que materializan la ruptura). Filtros a peso 1: expansión de volatilidad, momentum, tendencia corta, fuerza y hora. Sin bloques de nivel absoluto.

Recuento: **91 señales, 48 indicadores y 40 niveles/rangos stop-limit** (el original: 146 / 29 / 29, todos con peso 1 y sin relación con la tesis). Las familias con peso ≥ 2 son el núcleo del estilo; las de peso 1 son filtros auxiliares que amplían la variedad de estrategias sin cambiar la tesis. Se excluyen siempre los bloques con niveles absolutos dependientes del precio. La columna SELL muestra el bloque espejo que se activa en el kit de ventas.

#### Señales

| Familia (peso) | Qué mide | Por qué en este estilo | Bloques BUY | Espejo SELL |
|---|---|---|---|---|
| rup_canal (10) | Apertura por encima del máximo de N velas tras abrir por debajo (ruptura Donchian confirmada). | La tesis es la micro-ruptura: define el nivel roto. | `BarOpensAboveHighestAfterOpenBelow` | `BarOpensBelowLowestAfterOpenAbove` |
| rup_bandas (4) | Apertura/cierre fuera de la banda superior de Bollinger o Keltner. | Ruptura de bandas de volatilidad: variante de la misma tesis. | `BBBarOpensAboveUpAfterOpenBelow`, `BBBarClosesAboveUp`, `BBBarOpensAboveUp`, `KCBarOpensAboveUpperAfterOpenBelow`, `KCBarClosesAboveUpper`, `KCBarOpensAboveUpper` | `BBBarOpensBelowDownAfterOpenAbove`, `BBBarClosesBelowDown`, `BBBarOpensBelowDown`, `KCBarOpensBelowLowerAfterOpenAbove`, `KCBarClosesBelowLower`, `KCBarOpensBelowLower` |
| vol_expansion (2) | ATR/desviación típica/bandas abriéndose: entra volatilidad. | Sin expansión de volatilidad la ruptura no cubre costes. | `ATRRising`, `ATRChangesUp`, `StdDevRising`, `StdDevChangesUp`, `BBUpperRising`, `BBLowerFalling`, `KCUpperRising`, `KCLowerFalling` | igual (neutral) |
| vol_tick (1) | Volumen de ticks creciente (en FX es actividad, no volumen real). | Filtro auxiliar: amplía la variedad. | `VolumeRising`, `AvgVolumeRising` | igual (neutral) |
| mom_direccion (1) | Osciladores y momentum girando o subiendo (RSI, estocástico, MACD, OSMA, QQE, Reflex, ROC, CCI, WPR, DeMarker…), sin niveles absolutos. | Filtro auxiliar: amplía la variedad. | `RSIRising`, `RSIChangesUp`, `LaguerreRSIRising`, `LaguerreRSIChangesUP`, `StochSlowDRising`, `StochSlowDChangesUp`, `StochFastKUp`, `MomRising`, `MomChangesUp`, `MACDMainRising`, `MACDMainChangesUp`, `MACDMainCrossAboveSignal`, `MACDMainHigherSignal`, `MACDSignalRising`, `OSMARising`, `OSMAChangesUp`, `AWORising`, `AWOChangesUp`, `QQEValue1Rising`, `QQEValue1CrossAboveValue2`, `QQEValue1HigherValue2`, `QQEValue2Rising`, `ReflexRising`, `ReflexChangesDirectionUP`, `FastReflexCrossUPSlowReflex`, `ROCRising`, `CCIRising`, `CCIChangesUp`, `WPRRising`, `WPRChangesUp`, `DEMRising`, `DEMChangesUp` | `RSIFalling`, `RSIChangesDown`, `LaguerreRSIFalling`, `LaguerreRSIChangesDown`, `StochSlowDFalling`, `StochSlowDChangesDown`, `StochFastKDown`, `MomFalling`, `MomChangesDown`, `MACDMainFalling`, `MACDMainChangesDown`, `MACDMainCrossBelowSignal`, `MACDMainLowerSignal`, `MACDSignalFalling`, `OSMAFalling`, `OSMAChangesDown`, `AWOFalling`, `AWOChangesDown`, `QQEValue1Falling`, `QQEValue1CrossBelowValue2`, `QQEValue1LowerValue2`, `QQEValue2Falling`, `ReflexFalling`, `ReflexChangesDirectionDown`, `FastReflexCrossDownSlowReflex`, `ROCFalling`, `CCIFalling`, `CCIChangesDown`, `WPRFalling`, `WPRChangesDown`, `DEMFalling`, `DEMChangesDown` |
| mom_nivel (1) | Osciladores en zona de fuerza (RSI 50-70, estocástico 50-80, CCI 0-150…) y MACD/OSMA/ROC por encima de cero. | Filtro auxiliar: amplía la variedad. | `RSIHigher`, `RSICrossUp`, `LaguerreRSICrossUP`, `StochSlowDHigher`, `StochSlowDCrossUp`, `CCIHigher`, `CCICrossUp`, `WPRHigher`, `WPRCrossUp`, `QQEValue1Higher`, `QQEValue1CrossAbove`, `MACDMainHigherZero`, `MACDMainCrossAboveZero`, `OSMAHigherZero`, `OSMACrossZeroUp`, `ROCAboveLevel`, `ROCCrossesAboveLevel`, `SchaffTrendCycleAboveLevel`, `SchaffTrendCycleCrossesAboveLevel` | `RSILower`, `RSICrossDown`, `LaguerreRSICrossDown`, `StochSlowDLower`, `StochSlowDCrossDown`, `CCILower`, `CCICrossDown`, `WPRLower`, `WPRCrossDown`, `QQEValue1Lower`, `QQEValue1CrossBelow`, `MACDMainLowerZero`, `MACDMainCrossBelowZero`, `OSMALowerZero`, `OSMACrossZeroDown`, `ROCBelowLevel`, `ROCCrossesBelowLevel`, `SchaffTrendCycleBelowLevel`, `SchaffTrendCycleCrossesBelowLevel` |
| tend_medias (1) | Pendiente y posición del precio respecto a medias (simple, Hull, KAMA, regresión lineal). | Filtro auxiliar: amplía la variedad. | `MARising`, `MABarClosesAbove`, `MABarOpensAbove`, `MABarOpensAboveAfterOpenBelow`, `LinRegRising`, `LinRegBarClosesAbove`, `LinRegBarOpensAbove`, `LinRegBarOpensAboveAfterOpenBelow`, `HMARising`, `HMAChangesUP`, `FasterHMAIsAboveSlowerHMA`, `KAMARising`, `FastKAMAAboveSlowKAMA`, `BarClosesAboveKAMA`, `IsUptrend` | `MAFalling`, `MABarClosesBelow`, `MABarOpensBelow`, `MABarOpensBelowAfterOpenAbove`, `LinRegFalling`, `LinRegBarClosesBelow`, `LinRegBarOpensBelow`, `LinRegBarOpensBelowAfterOpenAbove`, `HMAFalling`, `HMAChangesDown`, `FasterHMAIsBelowSlowerHMA`, `KAMAFalling`, `FastKAMABelowSlowKAMA`, `BarClosesBelowKAMA`, `IsDowntrend` |
| fuerza (1) | ADX creciente o alto y eficiencia de Kaufman alta: hay tendencia. | Filtro auxiliar: amplía la variedad. | `ADXRising`, `ADXChangesUp`, `ADXHigher`, `ADXCrossUp`, `KERaboveLevel` | igual (neutral) |
| tiempo_intradia (1) | Franja horaria (hora mayor/menor que) y excluir un día de la semana. | Filtro auxiliar: amplía la variedad. | `BarHourIsBigger`, `BarHourIsSmaller`, `BarDayOfWeekIsNot` | igual (neutral) |

#### Indicadores

| Familia (peso) | Qué mide | Por qué en este estilo | Bloques BUY | Espejo SELL |
|---|---|---|---|---|
| niv_canal (3) | Máximo/mínimo de N velas. | Máximos/mínimos recientes: el nivel que se rompe. | `Highest`, `Lowest`(w1) | `Lowest`, `Highest` |
| niv_horario (2) | Máximo/mínimo de un rango horario y de la sesión (apertura/cierre de sesión). | Extremos de la sesión asiática, que la apertura de Londres rompe. | `HighestInRange`, `LowestInRange`(w1), `SessionHigh`, `SessionLow`(w1), `SessionOpen`, `SessionClose` | `LowestInRange`, `HighestInRange`, `SessionLow`, `SessionHigh`, `SessionOpen`, `SessionClose` |
| niv_diario (1) | Máximo/mínimo/apertura/cierre del día. | Filtro auxiliar: amplía la variedad. | `HighD`, `LowD`, `OpenD`, `CloseD` | `LowD`, `HighD`, `OpenD`, `CloseD` |
| precio (1) | Apertura, máximo, mínimo y cierre de la vela. | Filtro auxiliar: amplía la variedad. | `Close`, `Open`, `High`, `Low` | `Close`, `Open`, `Low`, `High` |
| medias (1) | Medias móviles (SMA, EMA, LWMA, SMMA, TEMA, Hull, KAMA) y regresión lineal. | Filtro auxiliar: amplía la variedad. | `SMA`, `EMA`, `LWMA`, `SMMA`, `TEMA`, `HullMovingAverage`, `KAMA`, `LinearRegression` | igual (neutral) |
| bandas (1) | Bandas de Bollinger y canal de Keltner. | Filtro auxiliar: amplía la variedad. | `BollingerBands`, `KeltnerChannel` | igual (neutral) |
| sistemas (1) | SuperTrend, Parabolic SAR, Ichimoku y Gann HiLo como valores. | Filtro auxiliar: amplía la variedad. | `SuperTrend`, `ParabolicSAR`, `Ichimoku`, `GannHiLo` | igual (neutral) |
| osciladores (1) | RSI, estocástico, CCI, Williams %R, RSI de Laguerre y DeMarker como valores. | Filtro auxiliar: amplía la variedad. | `RSI`, `Stochastic`, `CCI`, `WilliamsPR`, `LaguerreRSI`, `DeMarker` | igual (neutral) |
| volat_ind (1) | ATR y rango verdadero (para comparaciones relativas). | Filtro auxiliar: amplía la variedad. | `ATR`, `TrueRange` | igual (neutral) |
| comparadores (1) | Mayor/menor, mayor o igual, cruces. | Filtro auxiliar: amplía la variedad. | `IsGreater`, `IsLower`, `IsGreaterOrEqual`, `IsLowerOrEqual`, `CrossesAbove`, `CrossesBelow` | `IsLower`, `IsGreater`, `IsLowerOrEqual`, `IsGreaterOrEqual`, `CrossesBelow`, `CrossesAbove` |
| secuencias (1) | N velas seguidas por encima/debajo, subiendo/bajando. | Filtro auxiliar: amplía la variedad. | `IsGreaterCount`, `IsLowerCount`, `IsRising`, `IsFalling` | `IsLowerCount`, `IsGreaterCount`, `IsFalling`, `IsRising` |

#### Niveles y rangos stop/limit

| Familia (peso) | Qué mide | Por qué en este estilo | Bloques BUY | Espejo SELL |
|---|---|---|---|---|
| stl_canal (5) | Orden en el máximo/mínimo de N velas. | Orden stop en el extremo de N velas: materializa la ruptura. | `Highest`, `Lowest`(w1) | `Lowest`, `Highest` |
| stl_vela (3) | Orden en el máximo/mínimo/apertura/cierre de una vela. | Stop sobre el extremo de la vela previa (micro-ruptura). | `High`, `Low`(w1), `Open`, `Close` | `Low`, `High`, `Open`, `Close` |
| stl_horario (3) | Orden en el extremo de un rango horario o de sesión. | Stop en el extremo de la sesión asiática. | `HighestInRange`, `LowestInRange`(w1), `SessionHigh`, `SessionLow`(w1), `SessionOpen` | `LowestInRange`, `HighestInRange`, `SessionLow`, `SessionHigh`, `SessionOpen` |
| stl_diario (1) | Orden en niveles del día. | Filtro auxiliar: amplía la variedad. | `HighD`, `LowD`, `OpenD`, `CloseD` | `LowD`, `HighD`, `OpenD`, `CloseD` |
| stl_bandas (2) | Orden en Bollinger/Keltner. | Stop en la banda de volatilidad. | `BollingerBands`, `KeltnerChannel`, `MTKeltnerChannel` | igual (neutral) |
| stl_medias (1) | Orden en una media móvil. | Filtro auxiliar: amplía la variedad. | `SMA`, `EMA`, `LWMA`, `SMMA`, `TEMA`, `HullMovingAverage`, `KAMA`, `LinearRegression` | igual (neutral) |
| stl_sistemas (1) | Orden en SuperTrend, PSAR, Ichimoku o Gann HiLo. | Filtro auxiliar: amplía la variedad. | `SuperTrend`, `ParabolicSAR`, `Ichimoku`, `GannHiLo` | igual (neutral) |
| stl_estructura (1) | Orden en fractales o pivotes. | Filtro auxiliar: amplía la variedad. | `Fractal`, `Pivots` | igual (neutral) |
| stl_rangos (2) | Desplazamiento de la orden: k·ATR, rango de vela, rango verdadero, mayor/menor rango, anchura de Bollinger. | Margen sobre el nivel para filtrar toques. | `ATR`, `MTATR`, `BarRange`, `TrueRange`, `BiggestRange`, `SmallestRange`, `BBRange`, `BBWidthRatio` | igual (neutral) |

#### Rangos específicos (BUY → SELL)

| Bloque BUY | Rango BUY | Bloque SELL | Rango SELL |
|---|---|---|---|
| `RSIHigher` | Level 50 a 70 (paso 5) | `RSILower` | Level 30 a 50 (paso 5) |
| `RSICrossUp` | Level 50 a 70 (paso 5) | `RSICrossDown` | Level 30 a 50 (paso 5) |
| `LaguerreRSICrossUP` | Gamma 0.3 a 0.8 (paso 0.05); Level 0.4 a 0.85 (paso 0.05) | `LaguerreRSICrossDown` | Gamma 0.3 a 0.8 (paso 0.05); Level 0.15 a 0.6 (paso 0.05) |
| `StochSlowDHigher` | Level 50 a 80 (paso 5) | `StochSlowDLower` | Level 20 a 50 (paso 5) |
| `StochSlowDCrossUp` | Level 50 a 80 (paso 5) | `StochSlowDCrossDown` | Level 20 a 50 (paso 5) |
| `CCIHigher` | Level 0 a 150 (paso 10) | `CCILower` | Level -150 a 0 (paso 10) |
| `CCICrossUp` | Level 0 a 150 (paso 10) | `CCICrossDown` | Level -150 a 0 (paso 10) |
| `WPRHigher` | Level -50 a -20 (paso 5) | `WPRLower` | Level -80 a -50 (paso 5) |
| `WPRCrossUp` | Level -50 a -20 (paso 5) | `WPRCrossDown` | Level -80 a -50 (paso 5) |
| `QQEValue1Higher` | Level 50 a 70 (paso 5) | `QQEValue1Lower` | Level 30 a 50 (paso 5) |
| `QQEValue1CrossAbove` | Level 50 a 70 (paso 5) | `QQEValue1CrossBelow` | Level 30 a 50 (paso 5) |
| `SchaffTrendCycleAboveLevel` | Level 50 a 90 (paso 5) | `SchaffTrendCycleBelowLevel` | Level 10 a 50 (paso 5) |
| `SchaffTrendCycleCrossesAboveLevel` | Level 25 a 75 (paso 5) | `SchaffTrendCycleCrossesBelowLevel` | Level 25 a 75 (paso 5) |
| `ADXHigher` | Level 20 a 40 (paso 5) | `ADXHigher` | Level 20 a 40 (paso 5) |
| `ADXCrossUp` | Level 20 a 35 (paso 5) | `ADXCrossUp` | Level 20 a 35 (paso 5) |
| `KERaboveLevel` | Level 0.3 a 0.7 (paso 0.05) | `KERaboveLevel` | Level 0.3 a 0.7 (paso 0.05) |
| `Indicators.SuperTrend` | ATR Mult 1.5 a 5 (paso 0.5) | `Indicators.SuperTrend` | ATR Mult 1.5 a 5 (paso 0.5) |
| `Stop/Limit Price Levels.SuperTrend` | ATR Mult 1.5 a 5 (paso 0.5) | `Stop/Limit Price Levels.SuperTrend` | ATR Mult 1.5 a 5 (paso 0.5) |
| `ROCAboveLevel` | Level 0 a 1 (paso 0.05) | `ROCBelowLevel` | Level -1 a 0 (paso 0.05) |
| `ROCCrossesAboveLevel` | Level 0 a 1 (paso 0.05) | `ROCCrossesBelowLevel` | Level -1 a 0 (paso 0.05) |
| `Indicators.HighestInRange` | Time From 0 a 300 (paso 100); Time To 700 a 1000 (paso 100) | `Indicators.LowestInRange` | Time From 0 a 300 (paso 100); Time To 700 a 1000 (paso 100) |
| `Stop/Limit Price Levels.HighestInRange` | Time From 0 a 300 (paso 100); Time To 700 a 1000 (paso 100) | `Stop/Limit Price Levels.LowestInRange` | Time From 0 a 300 (paso 100); Time To 700 a 1000 (paso 100) |
| `Prices.SessionHigh` | Start Hours 1 a 3 (paso 1); Start Minutes 0 a 0 (paso 1); End Hours 8 a 10 (paso 1); End Minutes 0 a 0 (paso 1) | `Prices.SessionLow` | Start Hours 1 a 3 (paso 1); Start Minutes 0 a 0 (paso 1); End Hours 8 a 10 (paso 1); End Minutes 0 a 0 (paso 1) |
| `Stop/Limit Price Levels.SessionHigh` | Start Hours 1 a 3 (paso 1); Start Minutes 0 a 0 (paso 1); End Hours 8 a 10 (paso 1); End Minutes 0 a 0 (paso 1) | `Stop/Limit Price Levels.SessionLow` | Start Hours 1 a 3 (paso 1); Start Minutes 0 a 0 (paso 1); End Hours 8 a 10 (paso 1); End Minutes 0 a 0 (paso 1) |
| `Prices.SessionOpen` | Start Hours 1 a 3 (paso 1); Start Minutes 0 a 0 (paso 1) | `Prices.SessionOpen` | Start Hours 1 a 3 (paso 1); Start Minutes 0 a 0 (paso 1) |
| `Stop/Limit Price Levels.SessionOpen` | Start Hours 1 a 3 (paso 1); Start Minutes 0 a 0 (paso 1) | `Stop/Limit Price Levels.SessionOpen` | Start Hours 1 a 3 (paso 1); Start Minutes 0 a 0 (paso 1) |
| `Prices.SessionClose` | End Hours 8 a 10 (paso 1); End Minutes 0 a 0 (paso 1) | `Prices.SessionClose` | End Hours 8 a 10 (paso 1); End Minutes 0 a 0 (paso 1) |
| `BarHourIsBigger` | Hour 8 a 12 (paso 1) | `BarHourIsBigger` | Hour 8 a 12 (paso 1) |
| `BarHourIsSmaller` | Hour 12 a 19 (paso 1) | `BarHourIsSmaller` | Hour 12 a 19 (paso 1) |

### 4. Timeframe, símbolos y horarios

- **Timeframe:** M5.
- **Instrumento recomendado:** EURUSD o índice US500/NAS100 con spread bruto ≤0,3 pips/0,5 pts + comisión. GBPJPY con 2 pips de spread NO es apto (coste ≈30 % del ATR de M5).
- **Horario:** Señales 09:00-18:30 servidor (apertura de Londres + solape con Nueva York); cierre forzado al final de la ventana (`ExitAtEndOfRange`), a las 21:00 y los viernes a las 20:00. Se evita 23:00-01:30 (rollover, spreads anchos). El rango 'asiático' de los bloques de sesión es 01:00-03:00 → 08:00-10:00.

### 5. Salidas y gestión del riesgo

SL 1-2,5 ATR(14-50) de M5 (≈6-25 pips en EURUSD), PT 1-3 ATR con PT = 80-250 % del SL, break-even a 0,5-1,5 ATR (50 % de las estrategias), salida temporal 6-36 velas (30 min-3 h) y regla de salida opcional. Riesgo 0,5 % por operación y máximo 4 operaciones/día (≤2 % de riesgo diario).

### 6. Filtros y ranking

| Archivo | Fitness | Filtros |
|---|---|---|
| `Estrategia_Build_ConfigInicial_H1_BUY__Scalping_M5_BUY` | Weighted: ReturnDDRatio (peso 1, max), SQN (peso 2, max) | NumberOfTrades(IS) >= 1050; ReturnDDRatio(IS) >= 6; WinningPct(IS) >= 45; ProfitFactor(IS) >= 1.25; AvgBarsInTrade(IS) >= 3; NetProfit(OOS) > 0; NumberOfTrades(OOS) >= 360 |
| `Estrategia_Retest_ConfigInicial_H1_BUY__Scalping_M5_BUY` | Weighted: ReturnDDRatio (peso 1, max), SQN (peso 2, max) | NetProfit(OOS) > 0; ProfitFactor(OOS) >= 1.1; ReturnDDRatio(Full) >= 9; NumberOfTrades(Full) >= 2920; NumberOfTrades(OOS) >= 850; DrawdownPct(Full) <= 20 |
| `Ventaja_Build_ConfigInicial_H1_BUY__Scalping_M5_BUY` | Weighted: SQN (peso 2, max), StagnationPct (peso 1, min) | NumberOfTrades(IS) >= 1050; ReturnDDRatio(IS) >= 3; WinningPct(IS) >= 40; ProfitFactor(IS) >= 1.15; AvgBarsInTrade(IS) >= 3; NetProfit(OOS) > 0; NumberOfTrades(OOS) >= 360 |
| `Ventaja_Retest_ConfigInicial_H1_BUY__Scalping_M5_BUY` | Weighted: SQN (peso 2, max), StagnationPct (peso 1, min) | NetProfit(OOS) > 0; ProfitFactor(Full) >= 1.1; NumberOfTrades(Full) >= 2920; NumberOfTrades(OOS) >= 850 |

Justificación: SQN premia expectativa consistente con muchas operaciones (lo propio de un scalper); Ret/DD evita curvas con drawdowns profundos. El mínimo de operaciones sale de la densidad del estilo (300/año) multiplicada por los años de cada tramo; el acierto y el Ret/DD se adaptan al estilo. Los archivos SELL usan exactamente los mismos filtros.

### 7. Motor y robustez

- **Builder:** población 20 × 4 islas, 30 generaciones, cruce 80 %, mutación 30 %, migración 10 % cada 10, reinicio por estancamiento a 15.
- **Retest:** activo; precisión 3 (tick real + spread real); 3 condiciones. Precisión 3 (tick real con spread real): en M5 el spread variable decide el resultado.
- **Monte Carlo:** activo; 200 sims; OHLC ±10 % ATR(14), desliz. 0-1, spread 2-4. Acepta: NetProfit(Full) >= 0; DrawdownPct(Full) <= 150% de DrawdownPct[main].
- **Manipulación MC:** activo; orden de operaciones 'resampling', saltar 10 %.
- **SPP:** activo; 1500 tests, ±20 %, 6 pasos; ≥80 % rentables.
- **What-if:** activo; ExcludePctTradesWithBiggestPl, ExcludePctTradesWithLowestPl.

### 8. Riesgos conocidos, sobreoptimización y mitigación

Riesgos propios del estilo: Sensibilidad extrema a costes y latencia; datos M1 con spread fijo sobreestiman; el deslizamiento real en aperturas es mayor que el modelado.

1. El ruido de microestructura en M5 es enorme: con miles de estrategias candidatas, algunas 'ganarán' por azar. Mitigación: ≥1.000 operaciones en IS, OOS 2019.07-2020 y holdout 2021-2024.
2. El Builder usa simulación M1: una orden stop y su SL dentro del mismo minuto son ambiguos. Mitigación: `AvgBarsInTrade ≥ 3` y Retest con tick real y spread real (precisión 3).
3. Costes: un spread fijo de backtest infravalora la apertura de Londres. Mitigación: MC de spread 2-4 pips y deslizamiento 0-1 pip; prueba manual con coste ×2.
4. Ventana horaria y niveles de sesión son parámetros muy ajustables: SPP con 1.500 permutaciones y exigencia del 80 % de variantes rentables.

### 9. Plan de validación

1. Ejecuta `Ventaja_Build…Scalping_M5` (salida sólo por tiempo). Si no aparecen entradas con SQN > 2 y OOS positivo **con costes reales**, detente: no hay ventaja que gestionar.
2. Pasa las supervivientes por `Ventaja_Retest…Scalping_M5` (tick real, MC de spread y deslizamiento, SPP).
3. Ejecuta `Estrategia_Build…Scalping_M5` (o, mejor, el flujo plantilla con la entrada ganadora, docs/04 §A.3).
4. `Estrategia_Retest…Scalping_M5`: el holdout 2021-2024 debe ser positivo y el DD con tick real ≤130 % del original.
5. Retest manual con spread ×2 y deslizamiento 1 pip: si el beneficio desaparece, la ventaja no es explotable.
6. Retest en un segundo símbolo de la misma clase (EURUSD ↔ GBPUSD, US500 ↔ NAS100).
7. Demo 2-3 meses registrando spread y deslizamiento reales y comparándolos con los modelados.

---

## DayTrading

**Day Trading (ruptura del rango asiático)** · timeframe `M15`

**Archivos del kit** (todos *no validados en SQX*; tabla completa de cambios en `docs/cambios/`):

| Rol | BUY | SELL |
|---|---|---|
| EB | [`Estrategia_Build_ConfigInicial_H1_BUY__DayTrading_M15_BUY.cfx`](cambios/Estrategia_Build_ConfigInicial_H1_BUY__DayTrading_M15_BUY.md) | [`Estrategia_Build_ConfigInicial_H1_BUY__DayTrading_M15_SELL.cfx`](cambios/Estrategia_Build_ConfigInicial_H1_BUY__DayTrading_M15_SELL.md) |
| ER | [`Estrategia_Retest_ConfigInicial_H1_BUY__DayTrading_M15_BUY.cfx`](cambios/Estrategia_Retest_ConfigInicial_H1_BUY__DayTrading_M15_BUY.md) | [`Estrategia_Retest_ConfigInicial_H1_BUY__DayTrading_M15_SELL.cfx`](cambios/Estrategia_Retest_ConfigInicial_H1_BUY__DayTrading_M15_SELL.md) |
| VB | [`Ventaja_Build_ConfigInicial_H1_BUY__DayTrading_M15_BUY.cfx`](cambios/Ventaja_Build_ConfigInicial_H1_BUY__DayTrading_M15_BUY.md) | [`Ventaja_Build_ConfigInicial_H1_BUY__DayTrading_M15_SELL.cfx`](cambios/Ventaja_Build_ConfigInicial_H1_BUY__DayTrading_M15_SELL.md) |
| VR | [`Ventaja_Retest_ConfigInicial_H1_BUY__DayTrading_M15_BUY.cfx`](cambios/Ventaja_Retest_ConfigInicial_H1_BUY__DayTrading_M15_BUY.md) | [`Ventaja_Retest_ConfigInicial_H1_BUY__DayTrading_M15_SELL.cfx`](cambios/Ventaja_Retest_ConfigInicial_H1_BUY__DayTrading_M15_SELL.md) |

**Operaciones mínimas exigidas** (120/año): Builder IS ≥ 630, OOS 2019-2020 ≥ 190 (≈820 en 7.3 años de construcción); Retest periodo completo ≥ 1170 y holdout 2021-2024 ≥ 340.

### 1. Tesis

El rango de la sesión asiática concentra órdenes en sus extremos; la apertura de Londres aporta el volumen que rompe uno de ellos y el movimiento tiende a extenderse durante la sesión europea. Se cierra todo al final del día: no se asume riesgo nocturno.

### 2. Cambios respecto al original

#### 2.a Builder de estrategia completa (`Estrategia_Build`)

| Parámetro | Original | Nuevo | Justificación |
|---|---|---|---|
| Timeframe | H1 | M15 | Horizonte típico del estilo (M15). |
| Periodo de datos | 2013.09.30 – 2020.12.31 | 2013.09.30 – 2020.12.31 | Sin cambio. |
| Tramo OOS | sin OOS | 2019.01.01 – 2020.12.31 | Validación dentro del Builder: el original filtraba sólo sobre IS. |
| Deslizamiento (pips) | 0 | 0.3 | El original usa 0; 0,3 pips por ejecución stop en apertura de Londres. |
| Modo de generación | template (plantilla externa .sqx) | simple | El original dependía de una plantilla .sqx no incluida; en modo simple el archivo es autónomo (docs/04 §A.3 para volver a plantilla). |
| Condiciones de entrada | 0–0 | 1–3 | Nivel + 1-2 filtros como máximo; más condiciones = más grados de libertad. |
| Periodos de indicadores | 4–200 | 5–100 | 5-100 velas de M15 = 1 h 15 min a 25 h: contexto intradía y del día anterior. |
| Desplazamiento (shift) | 1–1 | 1–1 | Sin cambio. |
| Tipos de salida (mín–máx) | 1–5 | 2–4 | SL obligatorio + salidas propias del estilo (el original pedía hasta 5 con 3 disponibles). |
| Tipos de orden | EnterAtMarket (w1) | EnterAtMarket (w1), EnterAtStop (w3, válida 2-8 velas) | Stop en el extremo del rango; válida 30 min-2 h. |
| Stop loss | obligatorio=true; 1-3 × ATR(20-100) | obligatorio=true; 1-2.5 × ATR(14-60) | SL en ATR; objetivo opcional porque el cierre de fin de día ya acota la operación. |
| Profit target | obligatorio=true; 2-5 × ATR(20-100); PT=100-500 % del SL | obligatorio=false; 1.5-4 × ATR(14-60) | SL en ATR; objetivo opcional porque el cierre de fin de día ya acota la operación. |
| Trailing stop | sí (50 %), fijo 50-100 pips, 1-5 ATR | sí (30 %), 1.5-3 ATR | SL en ATR; objetivo opcional porque el cierre de fin de día ya acota la operación. |
| Break-even | no | sí (30 %), 1-2 ATR | SL en ATR; objetivo opcional porque el cierre de fin de día ya acota la operación. |
| Salida temporal | no | no | Sin cambio. |
| Salida por regla | no | sí (30 %) | SL en ATR; objetivo opcional porque el cierre de fin de día ya acota la operación. |
| Ventana de señales | 01:30-23:30 | 09:00-19:00 | Tras las 19:00 queda poco recorrido intradía. |
| Cierres forzados | no diario; no viernes | diario 22:30; viernes 21:30 | Definición de day trading: plano al cierre. |
| Máx. operaciones/día | 0 (sin límite) | 3 | La ruptura y hasta dos reintentos. |
| Distancia máx. orden | no | 0.6 % | ≈ 90 pips en GBPJPY: cubre rangos asiáticos amplios. |
| Bloques activos | 146 señales / 29 indicadores / 29 stop-limit | 110 señales / 52 indicadores / 40 stop-limit | Núcleo: extremos del rango asiático (HighestInRange 00:00-03:00 → 07:00-10:00 en horas enteras; el original usaba paso 30 sobre HHMM, que genera horas inválidas como 0060), niveles del día anterior y aperturas de sesión, con órdenes stop en ellos. Filtros amplios a peso 1. |
| Gestión monetaria | FixedAmount: riesgo 100 por operación | FixedAmount: riesgo 50 por operación | Riesgo fijo 0.5 % (no compuesto: Ret/DD comparable en el tiempo). |
| Fitness | type="ReturnDDRatio" | Weighted: ReturnDDRatio (peso 2, max), StagnationPct (peso 1, min) | Ret/DD como el original; StagnationPct penaliza meses planos (típico de rupturas intradía en régimen de baja volatilidad). |
| Filtros (Ranking) | AvgBarsInTrade(IS) >= 2; ReturnDDRatio(IS) >= 8; NumberOfTrades(IS) >= 300; WinningPct(IS) >= 40 | NumberOfTrades(IS) >= 630; ReturnDDRatio(IS) >= 5; WinningPct(IS) >= 40; ProfitFactor(IS) >= 1.25; AvgBarsInTrade(IS) >= 2; NetProfit(OOS) > 0; NumberOfTrades(OOS) >= 190 | Umbrales del estilo + exigencia OOS. |
| Filtro población inicial | ReturnDDRatio(IS) >= 5; AvgBarsInTrade(IS) >= 2; NumberOfTrades(IS) >= 250; WinningPct(IS) >= 35 | NumberOfTrades(IS) >= 190 | Sólo nº mínimo de operaciones (recomendación de SQX): con filtros de rentabilidad la población inicial puede tardar horas/días y el Builder no guarda nada mientras tanto. |
| Motor genético | población 5 × 5 islas, 10 generaciones, cruce 46 %, mutación 35 %, migración 6 % cada 5, reinicio por estancamiento a 30 | población 25 × 4 islas, 30 generaciones, cruce 80 %, mutación 30 %, migración 10 % cada 10, reinicio por estancamiento a 15 | 80-100 individuos por generación (el original 25-75) y 30 generaciones (el original 10, insuficiente para que la evolución actúe). |
| Calibración de indicadores | false | true | Recalibra los rangos de valores de indicadores y de rangos stop/limit (±5000 por defecto) para el símbolo y timeframe antes de construir. |

#### 2.b Builder de test de ventaja (`Ventaja_Build`)

| Parámetro | Original | Nuevo | Justificación |
|---|---|---|---|
| Timeframe | H1 | M15 | Horizonte típico del estilo (M15). |
| Periodo de datos | 2013.09.30 – 2020.12.31 | 2013.09.30 – 2020.12.31 | Sin cambio. |
| Tramo OOS | sin OOS | 2019.01.01 – 2020.12.31 | Validación dentro del Builder: el original filtraba sólo sobre IS. |
| Deslizamiento (pips) | 0 | 0.3 | El original usa 0; 0,3 pips por ejecución stop en apertura de Londres. |
| Modo de generación | simple | simple | Sin cambio. |
| Condiciones de entrada | 1–3 | 1–3 | Sin cambio. |
| Periodos de indicadores | 4–200 | 5–100 | 5-100 velas de M15 = 1 h 15 min a 25 h: contexto intradía y del día anterior. |
| Desplazamiento (shift) | 1–1 | 1–1 | Sin cambio. |
| Tipos de salida (mín–máx) | 1–5 | 1–1 | Sólo la salida temporal (test de ventaja). |
| Tipos de orden | EnterAtMarket (w1) | EnterAtMarket (w1), EnterAtStop (w3, válida 2-8 velas) | Stop en el extremo del rango; válida 30 min-2 h. |
| Stop loss | obligatorio=false; sin ATR | obligatorio=false; sin ATR | Sin cambio. |
| Profit target | obligatorio=false; sin ATR | obligatorio=false; sin ATR | Sin cambio. |
| Trailing stop | no | no | Sin cambio. |
| Break-even | no | no | Sin cambio. |
| Salida temporal | sí (50 %), 2-15 velas | sí (100 %), 4-24 velas | Test de ventaja: salida por tiempo 1-6 h + cierre de fin de día. |
| Salida por regla | no | no | Sin cambio. |
| Ventana de señales | 01:30-23:30 | 09:00-19:00 | Tras las 19:00 queda poco recorrido intradía. |
| Cierres forzados | no diario; no viernes | diario 22:30; viernes 21:30 | Definición de day trading: plano al cierre. |
| Máx. operaciones/día | 0 (sin límite) | 3 | La ruptura y hasta dos reintentos. |
| Distancia máx. orden | no | 0.6 % | ≈ 90 pips en GBPJPY: cubre rangos asiáticos amplios. |
| Bloques activos | 146 señales / 29 indicadores / 29 stop-limit | 110 señales / 52 indicadores / 40 stop-limit | Núcleo: extremos del rango asiático (HighestInRange 00:00-03:00 → 07:00-10:00 en horas enteras; el original usaba paso 30 sobre HHMM, que genera horas inválidas como 0060), niveles del día anterior y aperturas de sesión, con órdenes stop en ellos. Filtros amplios a peso 1. |
| Gestión monetaria | FixedSize: 1 lote | FixedSize: 1 lote | Sin cambio. |
| Fitness | Weighted: Stagnation (peso 1, min) | Weighted: SQN (peso 2, max), StagnationPct (peso 1, min) | SQN mide la calidad estadística de la entrada; el original optimizaba sólo 'Stagnation', que ignora el beneficio. |
| Filtros (Ranking) | AvgBarsInTrade(IS) >= 2; ReturnDDRatio(IS) >= 4; NumberOfTrades(IS) >= 300; WinningPct(IS) >= 40 | NumberOfTrades(IS) >= 630; ReturnDDRatio(IS) >= 2.5; WinningPct(IS) >= 35; ProfitFactor(IS) >= 1.15; AvgBarsInTrade(IS) >= 2; NetProfit(OOS) > 0; NumberOfTrades(OOS) >= 190 | Umbrales del estilo + exigencia OOS. Test de ventaja: Ret/DD a la mitad y PF ≥1,15. |
| Filtro población inicial | ReturnDDRatio(IS) >= 2; AvgBarsInTrade(IS) >= 2; NumberOfTrades(IS) >= 250; WinningPct(IS) >= 35 | NumberOfTrades(IS) >= 190 | Sólo nº mínimo de operaciones (recomendación de SQX): con filtros de rentabilidad la población inicial puede tardar horas/días y el Builder no guarda nada mientras tanto. |
| Motor genético | población 15 × 5 islas, 10 generaciones, cruce 46 %, mutación 35 %, migración 6 % cada 5, reinicio por estancamiento a 30 | población 25 × 4 islas, 30 generaciones, cruce 80 %, mutación 30 %, migración 10 % cada 10, reinicio por estancamiento a 15 | 80-100 individuos por generación (el original 25-75) y 30 generaciones (el original 10, insuficiente para que la evolución actúe). |
| Calibración de indicadores | false | true | Recalibra los rangos de valores de indicadores y de rangos stop/limit (±5000 por defecto) para el símbolo y timeframe antes de construir. |

#### 2.c Retesters (`Estrategia_Retest` / `Ventaja_Retest`)

| Parámetro | Original | Nuevo | Justificación |
|---|---|---|---|
| Timeframe | H1 | M15 | Debe coincidir con el Builder del estilo. |
| Periodo / OOS | 2013.09.30 – 2024.07.22; OOS 2021.01.01 – 2024.07.22 | 2013.09.30 – 2024.07.22; OOS 2021.01.01 – 2024.07.22 | Sin cambio. |
| Deslizamiento | 0 | 0.3 | El original usa 0; 0,3 pips por ejecución stop en apertura de Londres. |
| Ventana de señales | 01:30-23:30 | 09:00-19:00 | Idéntica al Builder: si difiere, el Retest no reproduce lo construido. |
| Cierres forzados | no diario; no viernes | diario 22:30; viernes 21:30 | Idénticos al Builder. |
| Gestión monetaria | FixedAmount: riesgo 100 por operación | FixedAmount: riesgo 50 por operación | Igual que el Builder correspondiente. |
| Fitness | type="ReturnDDRatio" | Weighted: ReturnDDRatio (peso 2, max), StagnationPct (peso 1, min) | Igual que el Builder correspondiente. |
| Filtros (Ranking) | (ninguna activa) | NetProfit(OOS) > 0; ProfitFactor(OOS) >= 1.1; ReturnDDRatio(Full) >= 7.5; NumberOfTrades(Full) >= 1170; NumberOfTrades(OOS) >= 340; DrawdownPct(Full) <= 20 | El original no filtraba nada (todas use=false) ni borraba fallidas. |
| Mayor precisión | activo; precisión 2 (tick real + spread personalizado); 1 condiciones | activo; precisión 2 (tick real + spread personalizado); 3 condiciones | Se activan también las condiciones de nº de operaciones y DD. |
| Monte Carlo retest | activo; 1000 sims; OHLC ±10 % ATR(14), spread 1-3. Acepta: NetProfit(IS) >= 0 | activo; 300 sims; OHLC ±10 % ATR(14), desliz. 0-0.5, spread 2-4. Acepta: NetProfit(Full) >= 0; DrawdownPct(Full) <= 150% de DrawdownPct[main] | Spread desde el base hasta 2-4x, deslizamiento, percentil 95 (no el peor caso) y control del DD. |
| Monte Carlo manipulación | no; orden de operaciones 'exact', saltar 10 % | activo; orden de operaciones 'resampling', saltar 10 % | Barato; 'resampling' y referencia corregida (el original comparaba MC contra MC). |
| SPP / perfil de optimización | activo; 15000 tests, ±20 %, 6 pasos; ≥95 % rentables | activo; 3000 tests, ±20 %, 6 pasos; ≥85 % rentables | Tests y exigencia ajustados al coste de cómputo y a la sensibilidad del estilo. |
| What-if | no; ExcludePctTradesWithBiggestPl, ExcludePctTradesWithLowestPl | activo; ExcludePctTradesWithBiggestPl, ExcludePctTradesWithLowestPl | Quitar el 5 % de extremos: el estilo no debe depender de outliers. |

Diferencias del `Ventaja_Retest` respecto al anterior:

- **Gestión monetaria:** FixedSize: 1 lote
- **Fitness:** Weighted: SQN (peso 2, max), StagnationPct (peso 1, min)
- **Filtros (Ranking):** NetProfit(OOS) > 0; ProfitFactor(Full) >= 1.1; NumberOfTrades(Full) >= 1170; NumberOfTrades(OOS) >= 340

### 3. Indicadores y bloques seleccionados

Criterio general: Núcleo: extremos del rango asiático (HighestInRange 00:00-03:00 → 07:00-10:00 en horas enteras; el original usaba paso 30 sobre HHMM, que genera horas inválidas como 0060), niveles del día anterior y aperturas de sesión, con órdenes stop en ellos. Filtros amplios a peso 1.

Recuento: **110 señales, 52 indicadores y 40 niveles/rangos stop-limit** (el original: 146 / 29 / 29, todos con peso 1 y sin relación con la tesis). Las familias con peso ≥ 2 son el núcleo del estilo; las de peso 1 son filtros auxiliares que amplían la variedad de estrategias sin cambiar la tesis. Se excluyen siempre los bloques con niveles absolutos dependientes del precio. La columna SELL muestra el bloque espejo que se activa en el kit de ventas.

#### Señales

| Familia (peso) | Qué mide | Por qué en este estilo | Bloques BUY | Espejo SELL |
|---|---|---|---|---|
| rup_canal (8) | Apertura por encima del máximo de N velas tras abrir por debajo (ruptura Donchian confirmada). | Ruptura de canal intradía. | `BarOpensAboveHighestAfterOpenBelow` | `BarOpensBelowLowestAfterOpenAbove` |
| rup_bandas (3) | Apertura/cierre fuera de la banda superior de Bollinger o Keltner. | Ruptura de bandas. | `BBBarOpensAboveUpAfterOpenBelow`, `BBBarClosesAboveUp`, `BBBarOpensAboveUp`, `KCBarOpensAboveUpperAfterOpenBelow`, `KCBarClosesAboveUpper`, `KCBarOpensAboveUpper` | `BBBarOpensBelowDownAfterOpenAbove`, `BBBarClosesBelowDown`, `BBBarOpensBelowDown`, `KCBarOpensBelowLowerAfterOpenAbove`, `KCBarClosesBelowLower`, `KCBarOpensBelowLower` |
| rup_ichimoku (1) | Salida de la nube y cruces alcistas de Ichimoku. | Filtro auxiliar: amplía la variedad. | `IchimokuKumoBreakoutBullish`, `IchimokuKijunSenCrossBullish`, `IchimokuSenkouSpanCrossBullish`, `IchimokuTenkanKijunCrossBullish` | `IchimokuKumoBreakoutBearish`, `IchimokuKijunSenCrossBearish`, `IchimokuSenkouSpanCrossBearish`, `IchimokuTenkanKijunCrossBearish` |
| vol_expansion (2) | ATR/desviación típica/bandas abriéndose: entra volatilidad. | La ruptura necesita expansión. | `ATRRising`, `ATRChangesUp`, `StdDevRising`, `StdDevChangesUp`, `BBUpperRising`, `BBLowerFalling`, `KCUpperRising`, `KCLowerFalling` | igual (neutral) |
| vol_tick (1) | Volumen de ticks creciente (en FX es actividad, no volumen real). | Filtro auxiliar: amplía la variedad. | `VolumeRising`, `AvgVolumeRising` | igual (neutral) |
| mom_direccion (1) | Osciladores y momentum girando o subiendo (RSI, estocástico, MACD, OSMA, QQE, Reflex, ROC, CCI, WPR, DeMarker…), sin niveles absolutos. | Filtro auxiliar: amplía la variedad. | `RSIRising`, `RSIChangesUp`, `LaguerreRSIRising`, `LaguerreRSIChangesUP`, `StochSlowDRising`, `StochSlowDChangesUp`, `StochFastKUp`, `MomRising`, `MomChangesUp`, `MACDMainRising`, `MACDMainChangesUp`, `MACDMainCrossAboveSignal`, `MACDMainHigherSignal`, `MACDSignalRising`, `OSMARising`, `OSMAChangesUp`, `AWORising`, `AWOChangesUp`, `QQEValue1Rising`, `QQEValue1CrossAboveValue2`, `QQEValue1HigherValue2`, `QQEValue2Rising`, `ReflexRising`, `ReflexChangesDirectionUP`, `FastReflexCrossUPSlowReflex`, `ROCRising`, `CCIRising`, `CCIChangesUp`, `WPRRising`, `WPRChangesUp`, `DEMRising`, `DEMChangesUp` | `RSIFalling`, `RSIChangesDown`, `LaguerreRSIFalling`, `LaguerreRSIChangesDown`, `StochSlowDFalling`, `StochSlowDChangesDown`, `StochFastKDown`, `MomFalling`, `MomChangesDown`, `MACDMainFalling`, `MACDMainChangesDown`, `MACDMainCrossBelowSignal`, `MACDMainLowerSignal`, `MACDSignalFalling`, `OSMAFalling`, `OSMAChangesDown`, `AWOFalling`, `AWOChangesDown`, `QQEValue1Falling`, `QQEValue1CrossBelowValue2`, `QQEValue1LowerValue2`, `QQEValue2Falling`, `ReflexFalling`, `ReflexChangesDirectionDown`, `FastReflexCrossDownSlowReflex`, `ROCFalling`, `CCIFalling`, `CCIChangesDown`, `WPRFalling`, `WPRChangesDown`, `DEMFalling`, `DEMChangesDown` |
| mom_nivel (1) | Osciladores en zona de fuerza (RSI 50-70, estocástico 50-80, CCI 0-150…) y MACD/OSMA/ROC por encima de cero. | Filtro auxiliar: amplía la variedad. | `RSIHigher`, `RSICrossUp`, `LaguerreRSICrossUP`, `StochSlowDHigher`, `StochSlowDCrossUp`, `CCIHigher`, `CCICrossUp`, `WPRHigher`, `WPRCrossUp`, `QQEValue1Higher`, `QQEValue1CrossAbove`, `MACDMainHigherZero`, `MACDMainCrossAboveZero`, `OSMAHigherZero`, `OSMACrossZeroUp`, `ROCAboveLevel`, `ROCCrossesAboveLevel`, `SchaffTrendCycleAboveLevel`, `SchaffTrendCycleCrossesAboveLevel` | `RSILower`, `RSICrossDown`, `LaguerreRSICrossDown`, `StochSlowDLower`, `StochSlowDCrossDown`, `CCILower`, `CCICrossDown`, `WPRLower`, `WPRCrossDown`, `QQEValue1Lower`, `QQEValue1CrossBelow`, `MACDMainLowerZero`, `MACDMainCrossBelowZero`, `OSMALowerZero`, `OSMACrossZeroDown`, `ROCBelowLevel`, `ROCCrossesBelowLevel`, `SchaffTrendCycleBelowLevel`, `SchaffTrendCycleCrossesBelowLevel` |
| tend_medias (1) | Pendiente y posición del precio respecto a medias (simple, Hull, KAMA, regresión lineal). | Filtro auxiliar: amplía la variedad. | `MARising`, `MABarClosesAbove`, `MABarOpensAbove`, `MABarOpensAboveAfterOpenBelow`, `LinRegRising`, `LinRegBarClosesAbove`, `LinRegBarOpensAbove`, `LinRegBarOpensAboveAfterOpenBelow`, `HMARising`, `HMAChangesUP`, `FasterHMAIsAboveSlowerHMA`, `KAMARising`, `FastKAMAAboveSlowKAMA`, `BarClosesAboveKAMA`, `IsUptrend` | `MAFalling`, `MABarClosesBelow`, `MABarOpensBelow`, `MABarOpensBelowAfterOpenAbove`, `LinRegFalling`, `LinRegBarClosesBelow`, `LinRegBarOpensBelow`, `LinRegBarOpensBelowAfterOpenAbove`, `HMAFalling`, `HMAChangesDown`, `FasterHMAIsBelowSlowerHMA`, `KAMAFalling`, `FastKAMABelowSlowKAMA`, `BarClosesBelowKAMA`, `IsDowntrend` |
| tend_sistemas (1) | Sistemas de tendencia: SuperTrend, PSAR, Vortex, Gann HiLo, Aroon, DMI, Woodies. | Filtro auxiliar: amplía la variedad. | `SuperTrendUPTrend`, `BarClosesAboveSuperTrend`, `PSARBarLower`, `VortexUptrend`, `VortexChangesTrendUP`, `GannHiLoUPTrend`, `AroonCrossesAbove`, `WoodiesTrendUP`, `WoodiesCCIZeroLineBreakUP`, `DIPlusRising`, `DIPlusChangesUp`, `DICrossUp`, `DIPlusHigher`, `DIMinusFalling`, `DIMinusChangesDown` | `SuperTrendDownTrend`, `BarClosesBelowSuperTrend`, `PSARBarHigher`, `VortexDowntrend`, `VortexChangesTrendDown`, `GannHiLoDownTrend`, `AroonCrossesBelow`, `WoodiesTrendDown`, `WoodiesCCIZeroLineBreakDown`, `DIMinusRising`, `DIMinusChangesUp`, `DICrossDown`, `DIPlusLower`, `DIPlusFalling`, `DIPlusChangesDown` |
| fuerza (1) | ADX creciente o alto y eficiencia de Kaufman alta: hay tendencia. | Filtro auxiliar: amplía la variedad. | `ADXRising`, `ADXChangesUp`, `ADXHigher`, `ADXCrossUp`, `KERaboveLevel` | igual (neutral) |
| tiempo_intradia (2) | Franja horaria (hora mayor/menor que) y excluir un día de la semana. | Acotan la franja de entrada dentro de la ventana global. | `BarHourIsBigger`, `BarHourIsSmaller`, `BarDayOfWeekIsNot` | igual (neutral) |

#### Indicadores

| Familia (peso) | Qué mide | Por qué en este estilo | Bloques BUY | Espejo SELL |
|---|---|---|---|---|
| niv_horario (4) | Máximo/mínimo de un rango horario y de la sesión (apertura/cierre de sesión). | Rango asiático y aperturas de sesión: los niveles clásicos intradía. | `HighestInRange`, `LowestInRange`(w2), `SessionHigh`, `SessionLow`(w2), `SessionOpen`, `SessionClose` | `LowestInRange`, `HighestInRange`, `SessionLow`, `SessionHigh`, `SessionOpen`, `SessionClose` |
| niv_canal (2) | Máximo/mínimo de N velas. | Extremos recientes. | `Highest`, `Lowest` | `Lowest`, `Highest` |
| niv_diario (2) | Máximo/mínimo/apertura/cierre del día. | Niveles del día anterior. | `HighD`, `LowD`, `OpenD`, `CloseD` | `LowD`, `HighD`, `OpenD`, `CloseD` |
| precio (1) | Apertura, máximo, mínimo y cierre de la vela. | Filtro auxiliar: amplía la variedad. | `Close`, `Open`, `High`, `Low` | `Close`, `Open`, `Low`, `High` |
| medias (1) | Medias móviles (SMA, EMA, LWMA, SMMA, TEMA, Hull, KAMA) y regresión lineal. | Filtro auxiliar: amplía la variedad. | `SMA`, `EMA`, `LWMA`, `SMMA`, `TEMA`, `HullMovingAverage`, `KAMA`, `LinearRegression` | igual (neutral) |
| bandas (1) | Bandas de Bollinger y canal de Keltner. | Filtro auxiliar: amplía la variedad. | `BollingerBands`, `KeltnerChannel` | igual (neutral) |
| sistemas (1) | SuperTrend, Parabolic SAR, Ichimoku y Gann HiLo como valores. | Filtro auxiliar: amplía la variedad. | `SuperTrend`, `ParabolicSAR`, `Ichimoku`, `GannHiLo` | igual (neutral) |
| osciladores (1) | RSI, estocástico, CCI, Williams %R, RSI de Laguerre y DeMarker como valores. | Filtro auxiliar: amplía la variedad. | `RSI`, `Stochastic`, `CCI`, `WilliamsPR`, `LaguerreRSI`, `DeMarker` | igual (neutral) |
| fuerza_ind (1) | ADX, eficiencia de Kaufman, Aroon y Vortex como valores. | Filtro auxiliar: amplía la variedad. | `ADX`, `KaufmanEfficiencyRatio`, `Aroon`, `Vortex` | igual (neutral) |
| volat_ind (1) | ATR y rango verdadero (para comparaciones relativas). | Filtro auxiliar: amplía la variedad. | `ATR`, `TrueRange` | igual (neutral) |
| comparadores (1) | Mayor/menor, mayor o igual, cruces. | Filtro auxiliar: amplía la variedad. | `IsGreater`, `IsLower`, `IsGreaterOrEqual`, `IsLowerOrEqual`, `CrossesAbove`, `CrossesBelow` | `IsLower`, `IsGreater`, `IsLowerOrEqual`, `IsGreaterOrEqual`, `CrossesBelow`, `CrossesAbove` |
| secuencias (1) | N velas seguidas por encima/debajo, subiendo/bajando. | Filtro auxiliar: amplía la variedad. | `IsGreaterCount`, `IsLowerCount`, `IsRising`, `IsFalling` | `IsLowerCount`, `IsGreaterCount`, `IsFalling`, `IsRising` |

#### Niveles y rangos stop/limit

| Familia (peso) | Qué mide | Por qué en este estilo | Bloques BUY | Espejo SELL |
|---|---|---|---|---|
| stl_horario (5) | Orden en el extremo de un rango horario o de sesión. | Stop en el extremo del rango asiático: el núcleo del estilo. | `HighestInRange`, `LowestInRange`(w1), `SessionHigh`, `SessionLow`(w1), `SessionOpen` | `LowestInRange`, `HighestInRange`, `SessionLow`, `SessionHigh`, `SessionOpen` |
| stl_diario (3) | Orden en niveles del día. | Stop en máximo/mínimo/apertura del día. | `HighD`, `LowD`(w1), `OpenD`, `CloseD` | `LowD`, `HighD`, `OpenD`, `CloseD` |
| stl_canal (2) | Orden en el máximo/mínimo de N velas. | Stop en extremo de N velas. | `Highest`, `Lowest`(w1) | `Lowest`, `Highest` |
| stl_vela (2) | Orden en el máximo/mínimo/apertura/cierre de una vela. | Stop en la vela previa. | `High`, `Low`(w1), `Open`, `Close` | `Low`, `High`, `Open`, `Close` |
| stl_bandas (1) | Orden en Bollinger/Keltner. | Filtro auxiliar: amplía la variedad. | `BollingerBands`, `KeltnerChannel`, `MTKeltnerChannel` | igual (neutral) |
| stl_medias (1) | Orden en una media móvil. | Filtro auxiliar: amplía la variedad. | `SMA`, `EMA`, `LWMA`, `SMMA`, `TEMA`, `HullMovingAverage`, `KAMA`, `LinearRegression` | igual (neutral) |
| stl_sistemas (1) | Orden en SuperTrend, PSAR, Ichimoku o Gann HiLo. | Filtro auxiliar: amplía la variedad. | `SuperTrend`, `ParabolicSAR`, `Ichimoku`, `GannHiLo` | igual (neutral) |
| stl_estructura (1) | Orden en fractales o pivotes. | Filtro auxiliar: amplía la variedad. | `Fractal`, `Pivots` | igual (neutral) |
| stl_rangos (2) | Desplazamiento de la orden: k·ATR, rango de vela, rango verdadero, mayor/menor rango, anchura de Bollinger. | Margen sobre el nivel. | `ATR`, `MTATR`, `BarRange`, `TrueRange`, `BiggestRange`, `SmallestRange`, `BBRange`, `BBWidthRatio` | igual (neutral) |

#### Rangos específicos (BUY → SELL)

| Bloque BUY | Rango BUY | Bloque SELL | Rango SELL |
|---|---|---|---|
| `RSIHigher` | Level 50 a 70 (paso 5) | `RSILower` | Level 30 a 50 (paso 5) |
| `RSICrossUp` | Level 50 a 70 (paso 5) | `RSICrossDown` | Level 30 a 50 (paso 5) |
| `LaguerreRSICrossUP` | Gamma 0.3 a 0.8 (paso 0.05); Level 0.4 a 0.85 (paso 0.05) | `LaguerreRSICrossDown` | Gamma 0.3 a 0.8 (paso 0.05); Level 0.15 a 0.6 (paso 0.05) |
| `StochSlowDHigher` | Level 50 a 80 (paso 5) | `StochSlowDLower` | Level 20 a 50 (paso 5) |
| `StochSlowDCrossUp` | Level 50 a 80 (paso 5) | `StochSlowDCrossDown` | Level 20 a 50 (paso 5) |
| `CCIHigher` | Level 0 a 150 (paso 10) | `CCILower` | Level -150 a 0 (paso 10) |
| `CCICrossUp` | Level 0 a 150 (paso 10) | `CCICrossDown` | Level -150 a 0 (paso 10) |
| `WPRHigher` | Level -50 a -20 (paso 5) | `WPRLower` | Level -80 a -50 (paso 5) |
| `WPRCrossUp` | Level -50 a -20 (paso 5) | `WPRCrossDown` | Level -80 a -50 (paso 5) |
| `QQEValue1Higher` | Level 50 a 70 (paso 5) | `QQEValue1Lower` | Level 30 a 50 (paso 5) |
| `QQEValue1CrossAbove` | Level 50 a 70 (paso 5) | `QQEValue1CrossBelow` | Level 30 a 50 (paso 5) |
| `SchaffTrendCycleAboveLevel` | Level 50 a 90 (paso 5) | `SchaffTrendCycleBelowLevel` | Level 10 a 50 (paso 5) |
| `SchaffTrendCycleCrossesAboveLevel` | Level 25 a 75 (paso 5) | `SchaffTrendCycleCrossesBelowLevel` | Level 25 a 75 (paso 5) |
| `ADXHigher` | Level 20 a 40 (paso 5) | `ADXHigher` | Level 20 a 40 (paso 5) |
| `ADXCrossUp` | Level 20 a 35 (paso 5) | `ADXCrossUp` | Level 20 a 35 (paso 5) |
| `KERaboveLevel` | Level 0.3 a 0.7 (paso 0.05) | `KERaboveLevel` | Level 0.3 a 0.7 (paso 0.05) |
| `SuperTrendUPTrend` | ATR Mult 1.5 a 5 (paso 0.5) | `SuperTrendDownTrend` | ATR Mult 1.5 a 5 (paso 0.5) |
| `BarClosesAboveSuperTrend` | ATR Mult 1.5 a 5 (paso 0.5) | `BarClosesBelowSuperTrend` | ATR Mult 1.5 a 5 (paso 0.5) |
| `Indicators.SuperTrend` | ATR Mult 1.5 a 5 (paso 0.5) | `Indicators.SuperTrend` | ATR Mult 1.5 a 5 (paso 0.5) |
| `Stop/Limit Price Levels.SuperTrend` | ATR Mult 1.5 a 5 (paso 0.5) | `Stop/Limit Price Levels.SuperTrend` | ATR Mult 1.5 a 5 (paso 0.5) |
| `ROCAboveLevel` | Level 0 a 1 (paso 0.05) | `ROCBelowLevel` | Level -1 a 0 (paso 0.05) |
| `ROCCrossesAboveLevel` | Level 0 a 1 (paso 0.05) | `ROCCrossesBelowLevel` | Level -1 a 0 (paso 0.05) |
| `Indicators.HighestInRange` | Time From 0 a 300 (paso 100); Time To 700 a 1000 (paso 100) | `Indicators.LowestInRange` | Time From 0 a 300 (paso 100); Time To 700 a 1000 (paso 100) |
| `Stop/Limit Price Levels.HighestInRange` | Time From 0 a 300 (paso 100); Time To 700 a 1000 (paso 100) | `Stop/Limit Price Levels.LowestInRange` | Time From 0 a 300 (paso 100); Time To 700 a 1000 (paso 100) |
| `Prices.SessionHigh` | Start Hours 1 a 3 (paso 1); Start Minutes 0 a 0 (paso 1); End Hours 8 a 10 (paso 1); End Minutes 0 a 0 (paso 1) | `Prices.SessionLow` | Start Hours 1 a 3 (paso 1); Start Minutes 0 a 0 (paso 1); End Hours 8 a 10 (paso 1); End Minutes 0 a 0 (paso 1) |
| `Stop/Limit Price Levels.SessionHigh` | Start Hours 1 a 3 (paso 1); Start Minutes 0 a 0 (paso 1); End Hours 8 a 10 (paso 1); End Minutes 0 a 0 (paso 1) | `Stop/Limit Price Levels.SessionLow` | Start Hours 1 a 3 (paso 1); Start Minutes 0 a 0 (paso 1); End Hours 8 a 10 (paso 1); End Minutes 0 a 0 (paso 1) |
| `Prices.SessionOpen` | Start Hours 8 a 10 (paso 1); Start Minutes 0 a 0 (paso 1) | `Prices.SessionOpen` | Start Hours 8 a 10 (paso 1); Start Minutes 0 a 0 (paso 1) |
| `Stop/Limit Price Levels.SessionOpen` | Start Hours 8 a 10 (paso 1); Start Minutes 0 a 0 (paso 1) | `Stop/Limit Price Levels.SessionOpen` | Start Hours 8 a 10 (paso 1); Start Minutes 0 a 0 (paso 1) |
| `Prices.SessionClose` | End Hours 8 a 10 (paso 1); End Minutes 0 a 0 (paso 1) | `Prices.SessionClose` | End Hours 8 a 10 (paso 1); End Minutes 0 a 0 (paso 1) |
| `BarHourIsBigger` | Hour 8 a 12 (paso 1) | `BarHourIsBigger` | Hour 8 a 12 (paso 1) |
| `BarHourIsSmaller` | Hour 12 a 19 (paso 1) | `BarHourIsSmaller` | Hour 12 a 19 (paso 1) |

### 4. Timeframe, símbolos y horarios

- **Timeframe:** M15.
- **Instrumento recomendado:** GBPUSD/GBPJPY/EURJPY (rango asiático + apertura de Londres) o DAX/US30 con su apertura de contado. GBPJPY es razonable aquí.
- **Horario:** Rango asiático: inicio entre 00:00 y 03:00, fin entre 07:00 y 10:00 (horas enteras). Entradas 09:00-19:00 servidor; cierre de todo a las 22:30 (viernes 21:30); máximo 2 operaciones/día.

### 5. Salidas y gestión del riesgo

SL 1-2,5 ATR(14-60) de M15; objetivo opcional 1,5-4 ATR (50 %); trailing 1,5-3 ATR (30 %); break-even 1-2 ATR (30 %); regla de salida (30 %); cierre de fin de día siempre. Riesgo 0,5 %.

### 6. Filtros y ranking

| Archivo | Fitness | Filtros |
|---|---|---|
| `Estrategia_Build_ConfigInicial_H1_BUY__DayTrading_M15_BUY` | Weighted: ReturnDDRatio (peso 2, max), StagnationPct (peso 1, min) | NumberOfTrades(IS) >= 630; ReturnDDRatio(IS) >= 5; WinningPct(IS) >= 40; ProfitFactor(IS) >= 1.25; AvgBarsInTrade(IS) >= 2; NetProfit(OOS) > 0; NumberOfTrades(OOS) >= 190 |
| `Estrategia_Retest_ConfigInicial_H1_BUY__DayTrading_M15_BUY` | Weighted: ReturnDDRatio (peso 2, max), StagnationPct (peso 1, min) | NetProfit(OOS) > 0; ProfitFactor(OOS) >= 1.1; ReturnDDRatio(Full) >= 7.5; NumberOfTrades(Full) >= 1170; NumberOfTrades(OOS) >= 340; DrawdownPct(Full) <= 20 |
| `Ventaja_Build_ConfigInicial_H1_BUY__DayTrading_M15_BUY` | Weighted: SQN (peso 2, max), StagnationPct (peso 1, min) | NumberOfTrades(IS) >= 630; ReturnDDRatio(IS) >= 2.5; WinningPct(IS) >= 35; ProfitFactor(IS) >= 1.15; AvgBarsInTrade(IS) >= 2; NetProfit(OOS) > 0; NumberOfTrades(OOS) >= 190 |
| `Ventaja_Retest_ConfigInicial_H1_BUY__DayTrading_M15_BUY` | Weighted: SQN (peso 2, max), StagnationPct (peso 1, min) | NetProfit(OOS) > 0; ProfitFactor(Full) >= 1.1; NumberOfTrades(Full) >= 1170; NumberOfTrades(OOS) >= 340 |

Justificación: Ret/DD como el original; StagnationPct penaliza meses planos (típico de rupturas intradía en régimen de baja volatilidad). El mínimo de operaciones sale de la densidad del estilo (120/año) multiplicada por los años de cada tramo; el acierto y el Ret/DD se adaptan al estilo. Los archivos SELL usan exactamente los mismos filtros.

### 7. Motor y robustez

- **Builder:** población 25 × 4 islas, 30 generaciones, cruce 80 %, mutación 30 %, migración 10 % cada 10, reinicio por estancamiento a 15.
- **Retest:** activo; precisión 2 (tick real + spread personalizado); 3 condiciones. Tick real con spread personalizado, como el original.
- **Monte Carlo:** activo; 300 sims; OHLC ±10 % ATR(14), desliz. 0-0.5, spread 2-4. Acepta: NetProfit(Full) >= 0; DrawdownPct(Full) <= 150% de DrawdownPct[main].
- **Manipulación MC:** activo; orden de operaciones 'resampling', saltar 10 %.
- **SPP:** activo; 3000 tests, ±20 %, 6 pasos; ≥85 % rentables.
- **What-if:** activo; ExcludePctTradesWithBiggestPl, ExcludePctTradesWithLowestPl.

### 8. Riesgos conocidos, sobreoptimización y mitigación

Riesgos propios del estilo: Dependencia del horario del servidor (DST); rupturas falsas en días sin catalizador; sobreajuste de la ventana horaria.

1. Las horas del rango (Time From/To) son el parámetro más sobreajustable: se limitan a horas enteras y se someten a SPP; prueba manual desplazando el rango ±1 h.
2. El cambio de hora (DST) desplaza 1 h las sesiones varias semanas al año si el servidor no sigue la convención de Nueva York: verifica la zona horaria del símbolo.
3. Rupturas falsas en días sin catalizador: `ADXRising`/`ATRRising` como filtros y `StagnationPct` en la fitness.

### 9. Plan de validación

1. `Ventaja_Build…DayTrading_M15` → entradas con ventaja (salida 1-6 h + cierre diario).
2. `Ventaja_Retest…DayTrading_M15` → tick real, MC, SPP, what-if.
3. `Estrategia_Build…` y `Estrategia_Retest…DayTrading_M15`.
4. What-if 'ByDays' manual: ningún día de la semana debe concentrar el beneficio.
5. Retest en GBPUSD/EURJPY (misma mecánica de sesión).
6. Walk-Forward Matrix en el Optimizer (docs/04 §A.4) con 5-10 ventanas.

---

## Swing

**Swing Trading (ruptura de consolidación multi-día)** · timeframe `H4`

**Archivos del kit** (todos *no validados en SQX*; tabla completa de cambios en `docs/cambios/`):

| Rol | BUY | SELL |
|---|---|---|
| EB | [`Estrategia_Build_ConfigInicial_H1_BUY__Swing_H4_BUY.cfx`](cambios/Estrategia_Build_ConfigInicial_H1_BUY__Swing_H4_BUY.md) | [`Estrategia_Build_ConfigInicial_H1_BUY__Swing_H4_SELL.cfx`](cambios/Estrategia_Build_ConfigInicial_H1_BUY__Swing_H4_SELL.md) |
| ER | [`Estrategia_Retest_ConfigInicial_H1_BUY__Swing_H4_BUY.cfx`](cambios/Estrategia_Retest_ConfigInicial_H1_BUY__Swing_H4_BUY.md) | [`Estrategia_Retest_ConfigInicial_H1_BUY__Swing_H4_SELL.cfx`](cambios/Estrategia_Retest_ConfigInicial_H1_BUY__Swing_H4_SELL.md) |
| VB | [`Ventaja_Build_ConfigInicial_H1_BUY__Swing_H4_BUY.cfx`](cambios/Ventaja_Build_ConfigInicial_H1_BUY__Swing_H4_BUY.md) | [`Ventaja_Build_ConfigInicial_H1_BUY__Swing_H4_SELL.cfx`](cambios/Ventaja_Build_ConfigInicial_H1_BUY__Swing_H4_SELL.md) |
| VR | [`Ventaja_Retest_ConfigInicial_H1_BUY__Swing_H4_BUY.cfx`](cambios/Ventaja_Retest_ConfigInicial_H1_BUY__Swing_H4_BUY.md) | [`Ventaja_Retest_ConfigInicial_H1_BUY__Swing_H4_SELL.cfx`](cambios/Ventaja_Retest_ConfigInicial_H1_BUY__Swing_H4_SELL.md) |

**Operaciones mínimas exigidas** (45/año): Builder IS ≥ 240, OOS 2019-2020 ≥ 70 (≈310 en 7.3 años de construcción); Retest periodo completo ≥ 440 y holdout 2021-2024 ≥ 130.

### 1. Tesis

Tras una contracción de volatilidad, la ruptura del rango tiende a continuar durante 1-5 días en la dirección del régimen de fondo. Se mantiene la posición noches y fines de semana.

### 2. Cambios respecto al original

#### 2.a Builder de estrategia completa (`Estrategia_Build`)

| Parámetro | Original | Nuevo | Justificación |
|---|---|---|---|
| Timeframe | H1 | H4 | Horizonte típico del estilo (H4). |
| Periodo de datos | 2013.09.30 – 2020.12.31 | 2013.09.30 – 2020.12.31 | Sin cambio. |
| Tramo OOS | sin OOS | 2019.01.01 – 2020.12.31 | Validación dentro del Builder: el original filtraba sólo sobre IS. |
| Deslizamiento (pips) | 0 | 0.3 | El original usa 0; 0,3 pips es conservador en H4. |
| Modo de generación | template (plantilla externa .sqx) | simple | El original dependía de una plantilla .sqx no incluida; en modo simple el archivo es autónomo (docs/04 §A.3 para volver a plantilla). |
| Condiciones de entrada | 0–0 | 1–3 | Nivel + 1-2 filtros como máximo; más condiciones = más grados de libertad. |
| Periodos de indicadores | 4–200 | 5–120 | 5-120 velas H4 = 1-20 días: horizonte de swing. |
| Desplazamiento (shift) | 1–1 | 1–1 | Sin cambio. |
| Tipos de salida (mín–máx) | 1–5 | 2–4 | SL obligatorio + salidas propias del estilo (el original pedía hasta 5 con 3 disponibles). |
| Tipos de orden | EnterAtMarket (w1) | EnterAtMarket (w1), EnterAtStop (w3, válida 2-6 velas) | Stop válida 8-24 h. |
| Stop loss | obligatorio=true; 1-3 × ATR(20-100) | obligatorio=true; 1.5-3.5 × ATR(14-100) | Stop amplio en ATR, objetivo y trailing opcionales, salida temporal 1-5 días. |
| Profit target | obligatorio=true; 2-5 × ATR(20-100); PT=100-500 % del SL | obligatorio=false; 2-6 × ATR(14-100) | Stop amplio en ATR, objetivo y trailing opcionales, salida temporal 1-5 días. |
| Trailing stop | sí (50 %), fijo 50-100 pips, 1-5 ATR | sí (50 %), 2-4 ATR | Stop amplio en ATR, objetivo y trailing opcionales, salida temporal 1-5 días. |
| Break-even | no | sí (30 %), 1-2 ATR | Stop amplio en ATR, objetivo y trailing opcionales, salida temporal 1-5 días. |
| Salida temporal | no | sí (40 %), 6-30 velas | Stop amplio en ATR, objetivo y trailing opcionales, salida temporal 1-5 días. |
| Salida por regla | no | sí (30 %) | Stop amplio en ATR, objetivo y trailing opcionales, salida temporal 1-5 días. |
| Ventana de señales | 01:30-23:30 | sin ventana | En H4 la ventana 01:30-23:30 excluiría la vela de las 00:00 (1/6 de las señales) sin motivo de estilo. |
| Cierres forzados | no diario; no viernes | no diario; no viernes | Sin cambio. |
| Máx. operaciones/día | 0 (sin límite) | 2 | Swing: hasta dos entradas diarias. |
| Distancia máx. orden | no | 2 % | 2 %: holgura para rupturas de rangos de varios días. |
| Bloques activos | 146 señales / 29 indicadores / 29 stop-limit | 115 señales / 51 indicadores / 38 stop-limit | Núcleo: ruptura de máximos de N velas/día/semana, bandas y nube de Ichimoku, con órdenes stop; filtros de régimen (ADX, KER, medias, sistemas de tendencia), volatilidad y calendario. |
| Gestión monetaria | FixedAmount: riesgo 100 por operación | FixedAmount: riesgo 100 por operación | Sin cambio. |
| Fitness | type="ReturnDDRatio" | Weighted: ReturnDDRatio (peso 2, max), Stability (peso 1, max) | Ret/DD + estabilidad de la curva. |
| Filtros (Ranking) | AvgBarsInTrade(IS) >= 2; ReturnDDRatio(IS) >= 8; NumberOfTrades(IS) >= 300; WinningPct(IS) >= 40 | NumberOfTrades(IS) >= 240; ReturnDDRatio(IS) >= 4; WinningPct(IS) >= 38; ProfitFactor(IS) >= 1.3; AvgBarsInTrade(IS) >= 3; NetProfit(OOS) > 0; NumberOfTrades(OOS) >= 70 | Umbrales del estilo + exigencia OOS. |
| Filtro población inicial | ReturnDDRatio(IS) >= 5; AvgBarsInTrade(IS) >= 2; NumberOfTrades(IS) >= 250; WinningPct(IS) >= 35 | NumberOfTrades(IS) >= 70 | Sólo nº mínimo de operaciones (recomendación de SQX): con filtros de rentabilidad la población inicial puede tardar horas/días y el Builder no guarda nada mientras tanto. |
| Motor genético | población 5 × 5 islas, 10 generaciones, cruce 46 %, mutación 35 %, migración 6 % cada 5, reinicio por estancamiento a 30 | población 25 × 4 islas, 30 generaciones, cruce 80 %, mutación 30 %, migración 10 % cada 10, reinicio por estancamiento a 15 | 80-100 individuos por generación (el original 25-75) y 30 generaciones (el original 10, insuficiente para que la evolución actúe). |
| Calibración de indicadores | false | true | Recalibra los rangos de valores de indicadores y de rangos stop/limit (±5000 por defecto) para el símbolo y timeframe antes de construir. |

#### 2.b Builder de test de ventaja (`Ventaja_Build`)

| Parámetro | Original | Nuevo | Justificación |
|---|---|---|---|
| Timeframe | H1 | H4 | Horizonte típico del estilo (H4). |
| Periodo de datos | 2013.09.30 – 2020.12.31 | 2013.09.30 – 2020.12.31 | Sin cambio. |
| Tramo OOS | sin OOS | 2019.01.01 – 2020.12.31 | Validación dentro del Builder: el original filtraba sólo sobre IS. |
| Deslizamiento (pips) | 0 | 0.3 | El original usa 0; 0,3 pips es conservador en H4. |
| Modo de generación | simple | simple | Sin cambio. |
| Condiciones de entrada | 1–3 | 1–3 | Sin cambio. |
| Periodos de indicadores | 4–200 | 5–120 | 5-120 velas H4 = 1-20 días: horizonte de swing. |
| Desplazamiento (shift) | 1–1 | 1–1 | Sin cambio. |
| Tipos de salida (mín–máx) | 1–5 | 1–1 | Sólo la salida temporal (test de ventaja). |
| Tipos de orden | EnterAtMarket (w1) | EnterAtMarket (w1), EnterAtStop (w3, válida 2-6 velas) | Stop válida 8-24 h. |
| Stop loss | obligatorio=false; sin ATR | obligatorio=false; sin ATR | Sin cambio. |
| Profit target | obligatorio=false; sin ATR | obligatorio=false; sin ATR | Sin cambio. |
| Trailing stop | no | no | Sin cambio. |
| Break-even | no | no | Sin cambio. |
| Salida temporal | sí (50 %), 2-15 velas | sí (100 %), 6-30 velas | Test de ventaja: salida por tiempo 1-5 días. |
| Salida por regla | no | no | Sin cambio. |
| Ventana de señales | 01:30-23:30 | sin ventana | En H4 la ventana 01:30-23:30 excluiría la vela de las 00:00 (1/6 de las señales) sin motivo de estilo. |
| Cierres forzados | no diario; no viernes | no diario; no viernes | Sin cambio. |
| Máx. operaciones/día | 0 (sin límite) | 2 | Swing: hasta dos entradas diarias. |
| Distancia máx. orden | no | 2 % | 2 %: holgura para rupturas de rangos de varios días. |
| Bloques activos | 146 señales / 29 indicadores / 29 stop-limit | 115 señales / 51 indicadores / 38 stop-limit | Núcleo: ruptura de máximos de N velas/día/semana, bandas y nube de Ichimoku, con órdenes stop; filtros de régimen (ADX, KER, medias, sistemas de tendencia), volatilidad y calendario. |
| Gestión monetaria | FixedSize: 1 lote | FixedSize: 1 lote | Sin cambio. |
| Fitness | Weighted: Stagnation (peso 1, min) | Weighted: SQN (peso 2, max), StagnationPct (peso 1, min) | SQN mide la calidad estadística de la entrada; el original optimizaba sólo 'Stagnation', que ignora el beneficio. |
| Filtros (Ranking) | AvgBarsInTrade(IS) >= 2; ReturnDDRatio(IS) >= 4; NumberOfTrades(IS) >= 300; WinningPct(IS) >= 40 | NumberOfTrades(IS) >= 240; ReturnDDRatio(IS) >= 2; WinningPct(IS) >= 33; ProfitFactor(IS) >= 1.15; AvgBarsInTrade(IS) >= 3; NetProfit(OOS) > 0; NumberOfTrades(OOS) >= 70 | Umbrales del estilo + exigencia OOS. Test de ventaja: Ret/DD a la mitad y PF ≥1,15. |
| Filtro población inicial | ReturnDDRatio(IS) >= 2; AvgBarsInTrade(IS) >= 2; NumberOfTrades(IS) >= 250; WinningPct(IS) >= 35 | NumberOfTrades(IS) >= 70 | Sólo nº mínimo de operaciones (recomendación de SQX): con filtros de rentabilidad la población inicial puede tardar horas/días y el Builder no guarda nada mientras tanto. |
| Motor genético | población 15 × 5 islas, 10 generaciones, cruce 46 %, mutación 35 %, migración 6 % cada 5, reinicio por estancamiento a 30 | población 25 × 4 islas, 30 generaciones, cruce 80 %, mutación 30 %, migración 10 % cada 10, reinicio por estancamiento a 15 | 80-100 individuos por generación (el original 25-75) y 30 generaciones (el original 10, insuficiente para que la evolución actúe). |
| Calibración de indicadores | false | true | Recalibra los rangos de valores de indicadores y de rangos stop/limit (±5000 por defecto) para el símbolo y timeframe antes de construir. |

#### 2.c Retesters (`Estrategia_Retest` / `Ventaja_Retest`)

| Parámetro | Original | Nuevo | Justificación |
|---|---|---|---|
| Timeframe | H1 | H4 | Debe coincidir con el Builder del estilo. |
| Periodo / OOS | 2013.09.30 – 2024.07.22; OOS 2021.01.01 – 2024.07.22 | 2013.09.30 – 2024.07.22; OOS 2021.01.01 – 2024.07.22 | Sin cambio. |
| Deslizamiento | 0 | 0.3 | El original usa 0; 0,3 pips es conservador en H4. |
| Ventana de señales | 01:30-23:30 | sin ventana | Idéntica al Builder: si difiere, el Retest no reproduce lo construido. |
| Cierres forzados | no diario; no viernes | no diario; no viernes | Sin cambio. |
| Gestión monetaria | FixedAmount: riesgo 100 por operación | FixedAmount: riesgo 100 por operación | Sin cambio. |
| Fitness | type="ReturnDDRatio" | Weighted: ReturnDDRatio (peso 2, max), Stability (peso 1, max) | Igual que el Builder correspondiente. |
| Filtros (Ranking) | (ninguna activa) | NetProfit(OOS) > 0; ProfitFactor(OOS) >= 1.1; ReturnDDRatio(Full) >= 6; NumberOfTrades(Full) >= 440; NumberOfTrades(OOS) >= 130; DrawdownPct(Full) <= 20 | El original no filtraba nada (todas use=false) ni borraba fallidas. |
| Mayor precisión | activo; precisión 2 (tick real + spread personalizado); 1 condiciones | activo; precisión 2 (tick real + spread personalizado); 3 condiciones | Se activan también las condiciones de nº de operaciones y DD. |
| Monte Carlo retest | activo; 1000 sims; OHLC ±10 % ATR(14), spread 1-3. Acepta: NetProfit(IS) >= 0 | activo; 500 sims; OHLC ±10 % ATR(14), desliz. 0-0.5, spread 2-4, vela de inicio. Acepta: NetProfit(Full) >= 0; DrawdownPct(Full) <= 150% de DrawdownPct[main] | Spread desde el base hasta 2-4x, deslizamiento, percentil 95 (no el peor caso) y control del DD. |
| Monte Carlo manipulación | no; orden de operaciones 'exact', saltar 10 % | activo; orden de operaciones 'resampling', saltar 10 % | Barato; 'resampling' y referencia corregida (el original comparaba MC contra MC). |
| SPP / perfil de optimización | activo; 15000 tests, ±20 %, 6 pasos; ≥95 % rentables | activo; 5000 tests, ±20 %, 6 pasos; ≥85 % rentables | Tests y exigencia ajustados al coste de cómputo y a la sensibilidad del estilo. |
| What-if | no; ExcludePctTradesWithBiggestPl, ExcludePctTradesWithLowestPl | activo; ExcludeTradesWithBiggestPl, ExcludeTradesWithLowestPl | Quitar 2 mejores/peores (estilos de outliers). |

Diferencias del `Ventaja_Retest` respecto al anterior:

- **Gestión monetaria:** FixedSize: 1 lote
- **Fitness:** Weighted: SQN (peso 2, max), StagnationPct (peso 1, min)
- **Filtros (Ranking):** NetProfit(OOS) > 0; ProfitFactor(Full) >= 1.1; NumberOfTrades(Full) >= 440; NumberOfTrades(OOS) >= 130

### 3. Indicadores y bloques seleccionados

Criterio general: Núcleo: ruptura de máximos de N velas/día/semana, bandas y nube de Ichimoku, con órdenes stop; filtros de régimen (ADX, KER, medias, sistemas de tendencia), volatilidad y calendario.

Recuento: **115 señales, 51 indicadores y 38 niveles/rangos stop-limit** (el original: 146 / 29 / 29, todos con peso 1 y sin relación con la tesis). Las familias con peso ≥ 2 son el núcleo del estilo; las de peso 1 son filtros auxiliares que amplían la variedad de estrategias sin cambiar la tesis. Se excluyen siempre los bloques con niveles absolutos dependientes del precio. La columna SELL muestra el bloque espejo que se activa en el kit de ventas.

#### Señales

| Familia (peso) | Qué mide | Por qué en este estilo | Bloques BUY | Espejo SELL |
|---|---|---|---|---|
| rup_canal (8) | Apertura por encima del máximo de N velas tras abrir por debajo (ruptura Donchian confirmada). | Ruptura de consolidaciones de varios días. | `BarOpensAboveHighestAfterOpenBelow` | `BarOpensBelowLowestAfterOpenAbove` |
| rup_bandas (3) | Apertura/cierre fuera de la banda superior de Bollinger o Keltner. | Ruptura de bandas. | `BBBarOpensAboveUpAfterOpenBelow`, `BBBarClosesAboveUp`, `BBBarOpensAboveUp`, `KCBarOpensAboveUpperAfterOpenBelow`, `KCBarClosesAboveUpper`, `KCBarOpensAboveUpper` | `BBBarOpensBelowDownAfterOpenAbove`, `BBBarClosesBelowDown`, `BBBarOpensBelowDown`, `KCBarOpensBelowLowerAfterOpenAbove`, `KCBarClosesBelowLower`, `KCBarOpensBelowLower` |
| rup_ichimoku (2) | Salida de la nube y cruces alcistas de Ichimoku. | Salida de la nube: ruptura de equilibrio de medio plazo. | `IchimokuKumoBreakoutBullish`, `IchimokuKijunSenCrossBullish`, `IchimokuSenkouSpanCrossBullish`, `IchimokuTenkanKijunCrossBullish` | `IchimokuKumoBreakoutBearish`, `IchimokuKijunSenCrossBearish`, `IchimokuSenkouSpanCrossBearish`, `IchimokuTenkanKijunCrossBearish` |
| vol_expansion (1) | ATR/desviación típica/bandas abriéndose: entra volatilidad. | Filtro auxiliar: amplía la variedad. | `ATRRising`, `ATRChangesUp`, `StdDevRising`, `StdDevChangesUp`, `BBUpperRising`, `BBLowerFalling`, `KCUpperRising`, `KCLowerFalling` | igual (neutral) |
| vol_contraccion (1) | ATR/desviación típica/bandas cerrándose: compresión previa a un movimiento. | Filtro auxiliar: amplía la variedad. | `ATRFalling`, `ATRChangesDown`, `StdDevFalling`, `StdDevChangesDown`, `BBUpperFalling`, `BBLowerRising`, `KCUpperFalling`, `KCLowerRising` | igual (neutral) |
| mom_direccion (1) | Osciladores y momentum girando o subiendo (RSI, estocástico, MACD, OSMA, QQE, Reflex, ROC, CCI, WPR, DeMarker…), sin niveles absolutos. | Filtro auxiliar: amplía la variedad. | `RSIRising`, `RSIChangesUp`, `LaguerreRSIRising`, `LaguerreRSIChangesUP`, `StochSlowDRising`, `StochSlowDChangesUp`, `StochFastKUp`, `MomRising`, `MomChangesUp`, `MACDMainRising`, `MACDMainChangesUp`, `MACDMainCrossAboveSignal`, `MACDMainHigherSignal`, `MACDSignalRising`, `OSMARising`, `OSMAChangesUp`, `AWORising`, `AWOChangesUp`, `QQEValue1Rising`, `QQEValue1CrossAboveValue2`, `QQEValue1HigherValue2`, `QQEValue2Rising`, `ReflexRising`, `ReflexChangesDirectionUP`, `FastReflexCrossUPSlowReflex`, `ROCRising`, `CCIRising`, `CCIChangesUp`, `WPRRising`, `WPRChangesUp`, `DEMRising`, `DEMChangesUp` | `RSIFalling`, `RSIChangesDown`, `LaguerreRSIFalling`, `LaguerreRSIChangesDown`, `StochSlowDFalling`, `StochSlowDChangesDown`, `StochFastKDown`, `MomFalling`, `MomChangesDown`, `MACDMainFalling`, `MACDMainChangesDown`, `MACDMainCrossBelowSignal`, `MACDMainLowerSignal`, `MACDSignalFalling`, `OSMAFalling`, `OSMAChangesDown`, `AWOFalling`, `AWOChangesDown`, `QQEValue1Falling`, `QQEValue1CrossBelowValue2`, `QQEValue1LowerValue2`, `QQEValue2Falling`, `ReflexFalling`, `ReflexChangesDirectionDown`, `FastReflexCrossDownSlowReflex`, `ROCFalling`, `CCIFalling`, `CCIChangesDown`, `WPRFalling`, `WPRChangesDown`, `DEMFalling`, `DEMChangesDown` |
| mom_nivel (1) | Osciladores en zona de fuerza (RSI 50-70, estocástico 50-80, CCI 0-150…) y MACD/OSMA/ROC por encima de cero. | Filtro auxiliar: amplía la variedad. | `RSIHigher`, `RSICrossUp`, `LaguerreRSICrossUP`, `StochSlowDHigher`, `StochSlowDCrossUp`, `CCIHigher`, `CCICrossUp`, `WPRHigher`, `WPRCrossUp`, `QQEValue1Higher`, `QQEValue1CrossAbove`, `MACDMainHigherZero`, `MACDMainCrossAboveZero`, `OSMAHigherZero`, `OSMACrossZeroUp`, `ROCAboveLevel`, `ROCCrossesAboveLevel`, `SchaffTrendCycleAboveLevel`, `SchaffTrendCycleCrossesAboveLevel` | `RSILower`, `RSICrossDown`, `LaguerreRSICrossDown`, `StochSlowDLower`, `StochSlowDCrossDown`, `CCILower`, `CCICrossDown`, `WPRLower`, `WPRCrossDown`, `QQEValue1Lower`, `QQEValue1CrossBelow`, `MACDMainLowerZero`, `MACDMainCrossBelowZero`, `OSMALowerZero`, `OSMACrossZeroDown`, `ROCBelowLevel`, `ROCCrossesBelowLevel`, `SchaffTrendCycleBelowLevel`, `SchaffTrendCycleCrossesBelowLevel` |
| tend_medias (1) | Pendiente y posición del precio respecto a medias (simple, Hull, KAMA, regresión lineal). | Filtro auxiliar: amplía la variedad. | `MARising`, `MABarClosesAbove`, `MABarOpensAbove`, `MABarOpensAboveAfterOpenBelow`, `LinRegRising`, `LinRegBarClosesAbove`, `LinRegBarOpensAbove`, `LinRegBarOpensAboveAfterOpenBelow`, `HMARising`, `HMAChangesUP`, `FasterHMAIsAboveSlowerHMA`, `KAMARising`, `FastKAMAAboveSlowKAMA`, `BarClosesAboveKAMA`, `IsUptrend` | `MAFalling`, `MABarClosesBelow`, `MABarOpensBelow`, `MABarOpensBelowAfterOpenAbove`, `LinRegFalling`, `LinRegBarClosesBelow`, `LinRegBarOpensBelow`, `LinRegBarOpensBelowAfterOpenAbove`, `HMAFalling`, `HMAChangesDown`, `FasterHMAIsBelowSlowerHMA`, `KAMAFalling`, `FastKAMABelowSlowKAMA`, `BarClosesBelowKAMA`, `IsDowntrend` |
| tend_sistemas (1) | Sistemas de tendencia: SuperTrend, PSAR, Vortex, Gann HiLo, Aroon, DMI, Woodies. | Filtro auxiliar: amplía la variedad. | `SuperTrendUPTrend`, `BarClosesAboveSuperTrend`, `PSARBarLower`, `VortexUptrend`, `VortexChangesTrendUP`, `GannHiLoUPTrend`, `AroonCrossesAbove`, `WoodiesTrendUP`, `WoodiesCCIZeroLineBreakUP`, `DIPlusRising`, `DIPlusChangesUp`, `DICrossUp`, `DIPlusHigher`, `DIMinusFalling`, `DIMinusChangesDown` | `SuperTrendDownTrend`, `BarClosesBelowSuperTrend`, `PSARBarHigher`, `VortexDowntrend`, `VortexChangesTrendDown`, `GannHiLoDownTrend`, `AroonCrossesBelow`, `WoodiesTrendDown`, `WoodiesCCIZeroLineBreakDown`, `DIMinusRising`, `DIMinusChangesUp`, `DICrossDown`, `DIPlusLower`, `DIPlusFalling`, `DIPlusChangesDown` |
| fuerza (2) | ADX creciente o alto y eficiencia de Kaufman alta: hay tendencia. | El swing a favor de un régimen con fuerza tiene más recorrido. | `ADXRising`, `ADXChangesUp`, `ADXHigher`, `ADXCrossUp`, `KERaboveLevel` | igual (neutral) |
| tiempo_calendario (1) | Excluir un día de la semana o un mes. | Filtro auxiliar: amplía la variedad. | `BarDayOfWeekIsNot`, `BarMonthIsNot` | igual (neutral) |

#### Indicadores

| Familia (peso) | Qué mide | Por qué en este estilo | Bloques BUY | Espejo SELL |
|---|---|---|---|---|
| niv_canal (3) | Máximo/mínimo de N velas. | Máximos de N velas. | `Highest`, `Lowest`(w1) | `Lowest`, `Highest` |
| niv_diario (2) | Máximo/mínimo/apertura/cierre del día. | Niveles diarios. | `HighD`, `LowD`, `OpenD`, `CloseD` | `LowD`, `HighD`, `OpenD`, `CloseD` |
| niv_semanal (2) | Máximo/mínimo/apertura/cierre de la semana. | Niveles semanales. | `HighW`, `LowW`, `OpenW`, `CloseW` | `LowW`, `HighW`, `OpenW`, `CloseW` |
| precio (1) | Apertura, máximo, mínimo y cierre de la vela. | Filtro auxiliar: amplía la variedad. | `Close`, `Open`, `High`, `Low` | `Close`, `Open`, `Low`, `High` |
| medias (1) | Medias móviles (SMA, EMA, LWMA, SMMA, TEMA, Hull, KAMA) y regresión lineal. | Filtro auxiliar: amplía la variedad. | `SMA`, `EMA`, `LWMA`, `SMMA`, `TEMA`, `HullMovingAverage`, `KAMA`, `LinearRegression` | igual (neutral) |
| bandas (1) | Bandas de Bollinger y canal de Keltner. | Filtro auxiliar: amplía la variedad. | `BollingerBands`, `KeltnerChannel` | igual (neutral) |
| sistemas (1) | SuperTrend, Parabolic SAR, Ichimoku y Gann HiLo como valores. | Filtro auxiliar: amplía la variedad. | `SuperTrend`, `ParabolicSAR`, `Ichimoku`, `GannHiLo` | igual (neutral) |
| osciladores (1) | RSI, estocástico, CCI, Williams %R, RSI de Laguerre y DeMarker como valores. | Filtro auxiliar: amplía la variedad. | `RSI`, `Stochastic`, `CCI`, `WilliamsPR`, `LaguerreRSI`, `DeMarker` | igual (neutral) |
| fuerza_ind (1) | ADX, eficiencia de Kaufman, Aroon y Vortex como valores. | Filtro auxiliar: amplía la variedad. | `ADX`, `KaufmanEfficiencyRatio`, `Aroon`, `Vortex` | igual (neutral) |
| volat_ind (1) | ATR y rango verdadero (para comparaciones relativas). | Filtro auxiliar: amplía la variedad. | `ATR`, `TrueRange` | igual (neutral) |
| estructura (1) | Fractales (máximos/mínimos locales). | Filtro auxiliar: amplía la variedad. | `Fractal` | igual (neutral) |
| comparadores (1) | Mayor/menor, mayor o igual, cruces. | Filtro auxiliar: amplía la variedad. | `IsGreater`, `IsLower`, `IsGreaterOrEqual`, `IsLowerOrEqual`, `CrossesAbove`, `CrossesBelow` | `IsLower`, `IsGreater`, `IsLowerOrEqual`, `IsGreaterOrEqual`, `CrossesBelow`, `CrossesAbove` |
| secuencias (1) | N velas seguidas por encima/debajo, subiendo/bajando. | Filtro auxiliar: amplía la variedad. | `IsGreaterCount`, `IsLowerCount`, `IsRising`, `IsFalling` | `IsLowerCount`, `IsGreaterCount`, `IsFalling`, `IsRising` |

#### Niveles y rangos stop/limit

| Familia (peso) | Qué mide | Por qué en este estilo | Bloques BUY | Espejo SELL |
|---|---|---|---|---|
| stl_canal (5) | Orden en el máximo/mínimo de N velas. | Stop sobre el máximo de la consolidación. | `Highest`, `Lowest`(w1) | `Lowest`, `Highest` |
| stl_diario (2) | Orden en niveles del día. | Stop en niveles diarios. | `HighD`, `LowD`(w1), `OpenD`, `CloseD` | `LowD`, `HighD`, `OpenD`, `CloseD` |
| stl_semanal (2) | Orden en niveles de la semana. | Stop en niveles semanales. | `HighW`, `LowW`(w1), `OpenW` | `LowW`, `HighW`, `OpenW` |
| stl_vela (1) | Orden en el máximo/mínimo/apertura/cierre de una vela. | Filtro auxiliar: amplía la variedad. | `High`, `Low`, `Open`, `Close` | `Low`, `High`, `Open`, `Close` |
| stl_bandas (2) | Orden en Bollinger/Keltner. | Stop en la banda. | `BollingerBands`, `KeltnerChannel`, `MTKeltnerChannel` | igual (neutral) |
| stl_medias (1) | Orden en una media móvil. | Filtro auxiliar: amplía la variedad. | `SMA`, `EMA`, `LWMA`, `SMMA`, `TEMA`, `HullMovingAverage`, `KAMA`, `LinearRegression` | igual (neutral) |
| stl_sistemas (1) | Orden en SuperTrend, PSAR, Ichimoku o Gann HiLo. | Filtro auxiliar: amplía la variedad. | `SuperTrend`, `ParabolicSAR`, `Ichimoku`, `GannHiLo` | igual (neutral) |
| stl_estructura (1) | Orden en fractales o pivotes. | Filtro auxiliar: amplía la variedad. | `Fractal`, `Pivots` | igual (neutral) |
| stl_rangos (2) | Desplazamiento de la orden: k·ATR, rango de vela, rango verdadero, mayor/menor rango, anchura de Bollinger. | Margen proporcional a la volatilidad. | `ATR`, `MTATR`, `BarRange`, `TrueRange`, `BiggestRange`, `SmallestRange`, `BBRange`, `BBWidthRatio` | igual (neutral) |

#### Rangos específicos (BUY → SELL)

| Bloque BUY | Rango BUY | Bloque SELL | Rango SELL |
|---|---|---|---|
| `RSIHigher` | Level 50 a 70 (paso 5) | `RSILower` | Level 30 a 50 (paso 5) |
| `RSICrossUp` | Level 50 a 70 (paso 5) | `RSICrossDown` | Level 30 a 50 (paso 5) |
| `LaguerreRSICrossUP` | Gamma 0.3 a 0.8 (paso 0.05); Level 0.4 a 0.85 (paso 0.05) | `LaguerreRSICrossDown` | Gamma 0.3 a 0.8 (paso 0.05); Level 0.15 a 0.6 (paso 0.05) |
| `StochSlowDHigher` | Level 50 a 80 (paso 5) | `StochSlowDLower` | Level 20 a 50 (paso 5) |
| `StochSlowDCrossUp` | Level 50 a 80 (paso 5) | `StochSlowDCrossDown` | Level 20 a 50 (paso 5) |
| `CCIHigher` | Level 0 a 150 (paso 10) | `CCILower` | Level -150 a 0 (paso 10) |
| `CCICrossUp` | Level 0 a 150 (paso 10) | `CCICrossDown` | Level -150 a 0 (paso 10) |
| `WPRHigher` | Level -50 a -20 (paso 5) | `WPRLower` | Level -80 a -50 (paso 5) |
| `WPRCrossUp` | Level -50 a -20 (paso 5) | `WPRCrossDown` | Level -80 a -50 (paso 5) |
| `QQEValue1Higher` | Level 50 a 70 (paso 5) | `QQEValue1Lower` | Level 30 a 50 (paso 5) |
| `QQEValue1CrossAbove` | Level 50 a 70 (paso 5) | `QQEValue1CrossBelow` | Level 30 a 50 (paso 5) |
| `SchaffTrendCycleAboveLevel` | Level 50 a 90 (paso 5) | `SchaffTrendCycleBelowLevel` | Level 10 a 50 (paso 5) |
| `SchaffTrendCycleCrossesAboveLevel` | Level 25 a 75 (paso 5) | `SchaffTrendCycleCrossesBelowLevel` | Level 25 a 75 (paso 5) |
| `ADXHigher` | Level 20 a 40 (paso 5) | `ADXHigher` | Level 20 a 40 (paso 5) |
| `ADXCrossUp` | Level 20 a 35 (paso 5) | `ADXCrossUp` | Level 20 a 35 (paso 5) |
| `KERaboveLevel` | Level 0.3 a 0.7 (paso 0.05) | `KERaboveLevel` | Level 0.3 a 0.7 (paso 0.05) |
| `SuperTrendUPTrend` | ATR Mult 1.5 a 5 (paso 0.5) | `SuperTrendDownTrend` | ATR Mult 1.5 a 5 (paso 0.5) |
| `BarClosesAboveSuperTrend` | ATR Mult 1.5 a 5 (paso 0.5) | `BarClosesBelowSuperTrend` | ATR Mult 1.5 a 5 (paso 0.5) |
| `Indicators.SuperTrend` | ATR Mult 1.5 a 5 (paso 0.5) | `Indicators.SuperTrend` | ATR Mult 1.5 a 5 (paso 0.5) |
| `Stop/Limit Price Levels.SuperTrend` | ATR Mult 1.5 a 5 (paso 0.5) | `Stop/Limit Price Levels.SuperTrend` | ATR Mult 1.5 a 5 (paso 0.5) |
| `ROCAboveLevel` | Level 0 a 3 (paso 0.1) | `ROCBelowLevel` | Level -3 a 0 (paso 0.1) |
| `ROCCrossesAboveLevel` | Level 0 a 3 (paso 0.1) | `ROCCrossesBelowLevel` | Level -3 a 0 (paso 0.1) |

### 4. Timeframe, símbolos y horarios

- **Timeframe:** H4.
- **Instrumento recomendado:** Pares mayores y cruces líquidos, índices (US30/DAX) y oro. GBPJPY apto (swap relevante: comprobar).
- **Horario:** H4 sin filtro horario (en H4 la ventana 01:30-23:30 del original eliminaría la vela de las 00:00). Mantiene posiciones de noche y fin de semana (`RealisticGapsHandling` = true se conserva para simular gaps).

### 5. Salidas y gestión del riesgo

SL 1,5-3,5 ATR(14-100) de H4; objetivo opcional 2-6 ATR; trailing 2-4 ATR (50 %); break-even (30 %); salida temporal 6-30 velas = 1-5 días (40 %). Riesgo 1 %; hasta 2 entradas/día.

### 6. Filtros y ranking

| Archivo | Fitness | Filtros |
|---|---|---|
| `Estrategia_Build_ConfigInicial_H1_BUY__Swing_H4_BUY` | Weighted: ReturnDDRatio (peso 2, max), Stability (peso 1, max) | NumberOfTrades(IS) >= 240; ReturnDDRatio(IS) >= 4; WinningPct(IS) >= 38; ProfitFactor(IS) >= 1.3; AvgBarsInTrade(IS) >= 3; NetProfit(OOS) > 0; NumberOfTrades(OOS) >= 70 |
| `Estrategia_Retest_ConfigInicial_H1_BUY__Swing_H4_BUY` | Weighted: ReturnDDRatio (peso 2, max), Stability (peso 1, max) | NetProfit(OOS) > 0; ProfitFactor(OOS) >= 1.1; ReturnDDRatio(Full) >= 6; NumberOfTrades(Full) >= 440; NumberOfTrades(OOS) >= 130; DrawdownPct(Full) <= 20 |
| `Ventaja_Build_ConfigInicial_H1_BUY__Swing_H4_BUY` | Weighted: SQN (peso 2, max), StagnationPct (peso 1, min) | NumberOfTrades(IS) >= 240; ReturnDDRatio(IS) >= 2; WinningPct(IS) >= 33; ProfitFactor(IS) >= 1.15; AvgBarsInTrade(IS) >= 3; NetProfit(OOS) > 0; NumberOfTrades(OOS) >= 70 |
| `Ventaja_Retest_ConfigInicial_H1_BUY__Swing_H4_BUY` | Weighted: SQN (peso 2, max), StagnationPct (peso 1, min) | NetProfit(OOS) > 0; ProfitFactor(Full) >= 1.1; NumberOfTrades(Full) >= 440; NumberOfTrades(OOS) >= 130 |

Justificación: Ret/DD + estabilidad de la curva. El mínimo de operaciones sale de la densidad del estilo (45/año) multiplicada por los años de cada tramo; el acierto y el Ret/DD se adaptan al estilo. Los archivos SELL usan exactamente los mismos filtros.

### 7. Motor y robustez

- **Builder:** población 25 × 4 islas, 30 generaciones, cruce 80 %, mutación 30 %, migración 10 % cada 10, reinicio por estancamiento a 15.
- **Retest:** activo; precisión 2 (tick real + spread personalizado); 3 condiciones. Se añade aleatorizar la vela de inicio: el resultado no debe depender del punto de arranque.
- **Monte Carlo:** activo; 500 sims; OHLC ±10 % ATR(14), desliz. 0-0.5, spread 2-4, vela de inicio. Acepta: NetProfit(Full) >= 0; DrawdownPct(Full) <= 150% de DrawdownPct[main].
- **Manipulación MC:** activo; orden de operaciones 'resampling', saltar 10 %.
- **SPP:** activo; 5000 tests, ±20 %, 6 pasos; ≥85 % rentables.
- **What-if:** activo; ExcludeTradesWithBiggestPl, ExcludeTradesWithLowestPl.

### 8. Riesgos conocidos, sobreoptimización y mitigación

Riesgos propios del estilo: Gaps de fin de semana; swap; exposición nocturna.

1. ≥45 operaciones/año exigidas (≈310 en 7,25 años): muestra suficiente, pero sigue siendo recomendable Stability en la fitness, OOS 2019-2020, holdout 2021-2024 y validación multi-mercado.
2. Sensibilidad al punto de inicio: MC con vela de inicio aleatoria.
3. Swap: el original aplica el swap del Dow; con GBPJPY el carry real cambia el resultado de un swing.

### 9. Plan de validación

1. `Ventaja_Build…Swing_H4` (salida 1-5 días) → `Ventaja_Retest…Swing_H4`.
2. `Estrategia_Build…` → `Estrategia_Retest…Swing_H4`.
3. Retest en 3+ mercados (p. ej. GBPUSD, EURJPY, US30): ≥2 deben ser rentables.
4. Walk-Forward Matrix (Optimizer) 5-10 ventanas, 20-30 % OOS.
5. Revisar el resultado año a año: ningún año debe aportar >40 % del beneficio.

---

## Position

**Position Trading (momentum de medio-largo plazo)** · timeframe `D1`

**Archivos del kit** (todos *no validados en SQX*; tabla completa de cambios en `docs/cambios/`):

| Rol | BUY | SELL |
|---|---|---|
| EB | [`Estrategia_Build_ConfigInicial_H1_BUY__Position_D1_BUY.cfx`](cambios/Estrategia_Build_ConfigInicial_H1_BUY__Position_D1_BUY.md) | [`Estrategia_Build_ConfigInicial_H1_BUY__Position_D1_SELL.cfx`](cambios/Estrategia_Build_ConfigInicial_H1_BUY__Position_D1_SELL.md) |
| ER | [`Estrategia_Retest_ConfigInicial_H1_BUY__Position_D1_BUY.cfx`](cambios/Estrategia_Retest_ConfigInicial_H1_BUY__Position_D1_BUY.md) | [`Estrategia_Retest_ConfigInicial_H1_BUY__Position_D1_SELL.cfx`](cambios/Estrategia_Retest_ConfigInicial_H1_BUY__Position_D1_SELL.md) |
| VB | [`Ventaja_Build_ConfigInicial_H1_BUY__Position_D1_BUY.cfx`](cambios/Ventaja_Build_ConfigInicial_H1_BUY__Position_D1_BUY.md) | [`Ventaja_Build_ConfigInicial_H1_BUY__Position_D1_SELL.cfx`](cambios/Ventaja_Build_ConfigInicial_H1_BUY__Position_D1_SELL.md) |
| VR | [`Ventaja_Retest_ConfigInicial_H1_BUY__Position_D1_BUY.cfx`](cambios/Ventaja_Retest_ConfigInicial_H1_BUY__Position_D1_BUY.md) | [`Ventaja_Retest_ConfigInicial_H1_BUY__Position_D1_SELL.cfx`](cambios/Ventaja_Retest_ConfigInicial_H1_BUY__Position_D1_SELL.md) |

**Operaciones mínimas exigidas** (20/año): Builder IS ≥ 150 (≈150 en 7.3 años de construcción); Retest periodo completo ≥ 190 y holdout 2021-2024 ≥ 60.

### 1. Tesis

El momentum de series temporales (rupturas de máximos de semanas/meses y pendiente de medias largas) es una de las anomalías más documentadas. Para obtener una muestra estadística útil en un solo mercado, las posiciones duran de 1 a 8 semanas (no meses).

### 2. Cambios respecto al original

#### 2.a Builder de estrategia completa (`Estrategia_Build`)

| Parámetro | Original | Nuevo | Justificación |
|---|---|---|---|
| Timeframe | H1 | D1 | Horizonte típico del estilo (D1). |
| Periodo de datos | 2013.09.30 – 2020.12.31 | 2013.09.30 – 2020.12.31 | Sin cambio. |
| Tramo OOS | sin OOS | sin OOS | Sin cambio. |
| Deslizamiento (pips) | 0 | 0.5 | D1 entra a la apertura del día (a menudo tras gap): 0,5 pips conservador. |
| Modo de generación | template (plantilla externa .sqx) | simple | El original dependía de una plantilla .sqx no incluida; en modo simple el archivo es autónomo (docs/04 §A.3 para volver a plantilla). |
| Condiciones de entrada | 0–0 | 1–2 | Nivel + 1-2 filtros como máximo; más condiciones = más grados de libertad. Position: máx. 2 por la muestra pequeña. |
| Periodos de indicadores | 4–200 | 20–250 | 20-250 días (1 mes-1 año). Máximo 2 condiciones: con ~20 operaciones/año cada grado de libertad extra es sobreajuste casi seguro. |
| Desplazamiento (shift) | 1–1 | 1–1 | Sin cambio. |
| Tipos de salida (mín–máx) | 1–5 | 1–3 | SL obligatorio + salidas propias del estilo (el original pedía hasta 5 con 3 disponibles). |
| Tipos de orden | EnterAtMarket (w1) | EnterAtMarket (w2), EnterAtStop (w2, válida 1-5 velas) | A mercado o con stop sobre el máximo, válida 1-5 días. |
| Stop loss | obligatorio=true; 1-3 × ATR(20-100) | obligatorio=true; 2.5-5 × ATR(20-100) | Sin objetivo (dejar correr); trailing de 2,5-5 ATR como salida principal; salida por regla y temporal de 2-8 semanas. |
| Profit target | obligatorio=true; 2-5 × ATR(20-100); PT=100-500 % del SL | obligatorio=false; 6-12 × ATR(20-100) | Sin objetivo (dejar correr); trailing de 2,5-5 ATR como salida principal; salida por regla y temporal de 2-8 semanas. |
| Trailing stop | sí (50 %), fijo 50-100 pips, 1-5 ATR | sí (70 %), 2.5-5 ATR | Sin objetivo (dejar correr); trailing de 2,5-5 ATR como salida principal; salida por regla y temporal de 2-8 semanas. |
| Break-even | no | no | Sin cambio. |
| Salida temporal | no | sí (30 %), 10-40 velas | Sin objetivo (dejar correr); trailing de 2,5-5 ATR como salida principal; salida por regla y temporal de 2-8 semanas. |
| Salida por regla | no | sí (50 %) | Sin objetivo (dejar correr); trailing de 2,5-5 ATR como salida principal; salida por regla y temporal de 2-8 semanas. |
| Ventana de señales | 01:30-23:30 | sin ventana | Con velas D1 (apertura 00:00) la ventana 01:30-23:30 del original podría bloquear todas las señales. |
| Cierres forzados | no diario; no viernes | no diario; no viernes | Sin cambio. |
| Máx. operaciones/día | 0 (sin límite) | 1 | Position: una entrada como máximo. |
| Distancia máx. orden | no | 5 % | 5 %: rupturas de máximos de 20-250 días. |
| Bloques activos | 146 señales / 29 indicadores / 29 stop-limit | 93 señales / 48 indicadores / 31 stop-limit | Núcleo: nuevos máximos de 20-250 días, semanales y mensuales; momentum sin niveles absolutos (ROC en %, MACD/OSMA frente a cero) y tendencia de medias/sistemas. |
| Gestión monetaria | FixedAmount: riesgo 100 por operación | FixedAmount: riesgo 100 por operación | Sin cambio. |
| Fitness | type="ReturnDDRatio" | Weighted: ReturnDDRatio (peso 2, max), Stability (peso 1, max) | Ret/DD + estabilidad; SQN es poco fiable con <200 operaciones. |
| Filtros (Ranking) | AvgBarsInTrade(IS) >= 2; ReturnDDRatio(IS) >= 8; NumberOfTrades(IS) >= 300; WinningPct(IS) >= 40 | NumberOfTrades(IS) >= 150; ReturnDDRatio(IS) >= 3; WinningPct(IS) >= 33; ProfitFactor(IS) >= 1.4; AvgBarsInTrade(IS) >= 4 | Umbrales del estilo + exigencia OOS. |
| Filtro población inicial | ReturnDDRatio(IS) >= 5; AvgBarsInTrade(IS) >= 2; NumberOfTrades(IS) >= 250; WinningPct(IS) >= 35 | NumberOfTrades(IS) >= 40 | Sólo nº mínimo de operaciones (recomendación de SQX): con filtros de rentabilidad la población inicial puede tardar horas/días y el Builder no guarda nada mientras tanto. |
| Motor genético | población 5 × 5 islas, 10 generaciones, cruce 46 %, mutación 35 %, migración 6 % cada 5, reinicio por estancamiento a 30 | población 25 × 4 islas, 30 generaciones, cruce 80 %, mutación 30 %, migración 10 % cada 10, reinicio por estancamiento a 15 | 80-100 individuos por generación (el original 25-75) y 30 generaciones (el original 10, insuficiente para que la evolución actúe). |
| Calibración de indicadores | false | true | Recalibra los rangos de valores de indicadores y de rangos stop/limit (±5000 por defecto) para el símbolo y timeframe antes de construir. |

#### 2.b Builder de test de ventaja (`Ventaja_Build`)

| Parámetro | Original | Nuevo | Justificación |
|---|---|---|---|
| Timeframe | H1 | D1 | Horizonte típico del estilo (D1). |
| Periodo de datos | 2013.09.30 – 2020.12.31 | 2013.09.30 – 2020.12.31 | Sin cambio. |
| Tramo OOS | sin OOS | sin OOS | Sin cambio. |
| Deslizamiento (pips) | 0 | 0.5 | D1 entra a la apertura del día (a menudo tras gap): 0,5 pips conservador. |
| Modo de generación | simple | simple | Sin cambio. |
| Condiciones de entrada | 1–3 | 1–2 | Nivel + 1-2 filtros como máximo; más condiciones = más grados de libertad. Position: máx. 2 por la muestra pequeña. |
| Periodos de indicadores | 4–200 | 20–250 | 20-250 días (1 mes-1 año). Máximo 2 condiciones: con ~20 operaciones/año cada grado de libertad extra es sobreajuste casi seguro. |
| Desplazamiento (shift) | 1–1 | 1–1 | Sin cambio. |
| Tipos de salida (mín–máx) | 1–5 | 1–1 | Sólo la salida temporal (test de ventaja). |
| Tipos de orden | EnterAtMarket (w1) | EnterAtMarket (w2), EnterAtStop (w2, válida 1-5 velas) | A mercado o con stop sobre el máximo, válida 1-5 días. |
| Stop loss | obligatorio=false; sin ATR | obligatorio=false; sin ATR | Sin cambio. |
| Profit target | obligatorio=false; sin ATR | obligatorio=false; sin ATR | Sin cambio. |
| Trailing stop | no | no | Sin cambio. |
| Break-even | no | no | Sin cambio. |
| Salida temporal | sí (50 %), 2-15 velas | sí (100 %), 5-40 velas | Test de ventaja: salida por tiempo 1-8 semanas. |
| Salida por regla | no | no | Sin cambio. |
| Ventana de señales | 01:30-23:30 | sin ventana | Con velas D1 (apertura 00:00) la ventana 01:30-23:30 del original podría bloquear todas las señales. |
| Cierres forzados | no diario; no viernes | no diario; no viernes | Sin cambio. |
| Máx. operaciones/día | 0 (sin límite) | 1 | Position: una entrada como máximo. |
| Distancia máx. orden | no | 5 % | 5 %: rupturas de máximos de 20-250 días. |
| Bloques activos | 146 señales / 29 indicadores / 29 stop-limit | 93 señales / 48 indicadores / 31 stop-limit | Núcleo: nuevos máximos de 20-250 días, semanales y mensuales; momentum sin niveles absolutos (ROC en %, MACD/OSMA frente a cero) y tendencia de medias/sistemas. |
| Gestión monetaria | FixedSize: 1 lote | FixedSize: 1 lote | Sin cambio. |
| Fitness | Weighted: Stagnation (peso 1, min) | Weighted: ProfitFactor (peso 2, max), StagnationPct (peso 1, min) | SQN mide la calidad estadística de la entrada; el original optimizaba sólo 'Stagnation', que ignora el beneficio. |
| Filtros (Ranking) | AvgBarsInTrade(IS) >= 2; ReturnDDRatio(IS) >= 4; NumberOfTrades(IS) >= 300; WinningPct(IS) >= 40 | NumberOfTrades(IS) >= 150; ReturnDDRatio(IS) >= 1.5; WinningPct(IS) >= 30; ProfitFactor(IS) >= 1.3; AvgBarsInTrade(IS) >= 4 | Umbrales del estilo + exigencia OOS. Test de ventaja: Ret/DD a la mitad y PF ≥1,15. |
| Filtro población inicial | ReturnDDRatio(IS) >= 2; AvgBarsInTrade(IS) >= 2; NumberOfTrades(IS) >= 250; WinningPct(IS) >= 35 | NumberOfTrades(IS) >= 40 | Sólo nº mínimo de operaciones (recomendación de SQX): con filtros de rentabilidad la población inicial puede tardar horas/días y el Builder no guarda nada mientras tanto. |
| Motor genético | población 15 × 5 islas, 10 generaciones, cruce 46 %, mutación 35 %, migración 6 % cada 5, reinicio por estancamiento a 30 | población 25 × 4 islas, 30 generaciones, cruce 80 %, mutación 30 %, migración 10 % cada 10, reinicio por estancamiento a 15 | 80-100 individuos por generación (el original 25-75) y 30 generaciones (el original 10, insuficiente para que la evolución actúe). |
| Calibración de indicadores | false | true | Recalibra los rangos de valores de indicadores y de rangos stop/limit (±5000 por defecto) para el símbolo y timeframe antes de construir. |

#### 2.c Retesters (`Estrategia_Retest` / `Ventaja_Retest`)

| Parámetro | Original | Nuevo | Justificación |
|---|---|---|---|
| Timeframe | H1 | D1 | Debe coincidir con el Builder del estilo. |
| Periodo / OOS | 2013.09.30 – 2024.07.22; OOS 2021.01.01 – 2024.07.22 | 2013.09.30 – 2024.07.22; OOS 2021.01.01 – 2024.07.22 | Sin cambio. |
| Deslizamiento | 0 | 0.5 | D1 entra a la apertura del día (a menudo tras gap): 0,5 pips conservador. |
| Ventana de señales | 01:30-23:30 | sin ventana | Idéntica al Builder: si difiere, el Retest no reproduce lo construido. |
| Cierres forzados | no diario; no viernes | no diario; no viernes | Sin cambio. |
| Gestión monetaria | FixedAmount: riesgo 100 por operación | FixedAmount: riesgo 100 por operación | Sin cambio. |
| Fitness | type="ReturnDDRatio" | Weighted: ReturnDDRatio (peso 2, max), Stability (peso 1, max) | Igual que el Builder correspondiente. |
| Filtros (Ranking) | (ninguna activa) | NetProfit(OOS) > 0; ReturnDDRatio(Full) >= 4.5; NumberOfTrades(Full) >= 190; NumberOfTrades(OOS) >= 60; DrawdownPct(Full) <= 25 | El original no filtraba nada (todas use=false) ni borraba fallidas. |
| Mayor precisión | activo; precisión 2 (tick real + spread personalizado); 1 condiciones | activo; precisión 2 (tick real + spread personalizado); 3 condiciones | Se activan también las condiciones de nº de operaciones y DD. |
| Monte Carlo retest | activo; 1000 sims; OHLC ±10 % ATR(14), spread 1-3. Acepta: NetProfit(IS) >= 0 | activo; 500 sims; OHLC ±10 % ATR(14), desliz. 0-1, spread 2-4, vela de inicio. Acepta: NetProfit(Full) >= 0; DrawdownPct(Full) <= 175% de DrawdownPct[main] | Spread desde el base hasta 2-4x, deslizamiento, percentil 95 (no el peor caso) y control del DD. |
| Monte Carlo manipulación | no; orden de operaciones 'exact', saltar 10 % | activo; orden de operaciones 'resampling', saltar 10 % | Barato; 'resampling' y referencia corregida (el original comparaba MC contra MC). |
| SPP / perfil de optimización | activo; 15000 tests, ±20 %, 6 pasos; ≥95 % rentables | activo; 8000 tests, ±30 %, 6 pasos; ≥90 % rentables | Tests y exigencia ajustados al coste de cómputo y a la sensibilidad del estilo. |
| What-if | no; ExcludePctTradesWithBiggestPl, ExcludePctTradesWithLowestPl | activo; ExcludeTradesWithBiggestPl, ExcludeTradesWithLowestPl | Quitar 2 mejores/peores (estilos de outliers). |

Diferencias del `Ventaja_Retest` respecto al anterior:

- **Gestión monetaria:** FixedSize: 1 lote
- **Fitness:** Weighted: ProfitFactor (peso 2, max), StagnationPct (peso 1, min)
- **Filtros (Ranking):** NetProfit(OOS) > 0; ProfitFactor(Full) >= 1.2; NumberOfTrades(Full) >= 190; NumberOfTrades(OOS) >= 60

### 3. Indicadores y bloques seleccionados

Criterio general: Núcleo: nuevos máximos de 20-250 días, semanales y mensuales; momentum sin niveles absolutos (ROC en %, MACD/OSMA frente a cero) y tendencia de medias/sistemas.

Recuento: **93 señales, 48 indicadores y 31 niveles/rangos stop-limit** (el original: 146 / 29 / 29, todos con peso 1 y sin relación con la tesis). Las familias con peso ≥ 2 son el núcleo del estilo; las de peso 1 son filtros auxiliares que amplían la variedad de estrategias sin cambiar la tesis. Se excluyen siempre los bloques con niveles absolutos dependientes del precio. La columna SELL muestra el bloque espejo que se activa en el kit de ventas.

#### Señales

| Familia (peso) | Qué mide | Por qué en este estilo | Bloques BUY | Espejo SELL |
|---|---|---|---|---|
| rup_canal (8) | Apertura por encima del máximo de N velas tras abrir por debajo (ruptura Donchian confirmada). | Nuevos máximos de 20-250 días (momentum de series temporales). | `BarOpensAboveHighestAfterOpenBelow` | `BarOpensBelowLowestAfterOpenAbove` |
| rup_ichimoku (1) | Salida de la nube y cruces alcistas de Ichimoku. | Filtro auxiliar: amplía la variedad. | `IchimokuKumoBreakoutBullish`, `IchimokuKijunSenCrossBullish`, `IchimokuSenkouSpanCrossBullish`, `IchimokuTenkanKijunCrossBullish` | `IchimokuKumoBreakoutBearish`, `IchimokuKijunSenCrossBearish`, `IchimokuSenkouSpanCrossBearish`, `IchimokuTenkanKijunCrossBearish` |
| mom_direccion (1) | Osciladores y momentum girando o subiendo (RSI, estocástico, MACD, OSMA, QQE, Reflex, ROC, CCI, WPR, DeMarker…), sin niveles absolutos. | Filtro auxiliar: amplía la variedad. | `RSIRising`, `RSIChangesUp`, `LaguerreRSIRising`, `LaguerreRSIChangesUP`, `StochSlowDRising`, `StochSlowDChangesUp`, `StochFastKUp`, `MomRising`, `MomChangesUp`, `MACDMainRising`, `MACDMainChangesUp`, `MACDMainCrossAboveSignal`, `MACDMainHigherSignal`, `MACDSignalRising`, `OSMARising`, `OSMAChangesUp`, `AWORising`, `AWOChangesUp`, `QQEValue1Rising`, `QQEValue1CrossAboveValue2`, `QQEValue1HigherValue2`, `QQEValue2Rising`, `ReflexRising`, `ReflexChangesDirectionUP`, `FastReflexCrossUPSlowReflex`, `ROCRising`, `CCIRising`, `CCIChangesUp`, `WPRRising`, `WPRChangesUp`, `DEMRising`, `DEMChangesUp` | `RSIFalling`, `RSIChangesDown`, `LaguerreRSIFalling`, `LaguerreRSIChangesDown`, `StochSlowDFalling`, `StochSlowDChangesDown`, `StochFastKDown`, `MomFalling`, `MomChangesDown`, `MACDMainFalling`, `MACDMainChangesDown`, `MACDMainCrossBelowSignal`, `MACDMainLowerSignal`, `MACDSignalFalling`, `OSMAFalling`, `OSMAChangesDown`, `AWOFalling`, `AWOChangesDown`, `QQEValue1Falling`, `QQEValue1CrossBelowValue2`, `QQEValue1LowerValue2`, `QQEValue2Falling`, `ReflexFalling`, `ReflexChangesDirectionDown`, `FastReflexCrossDownSlowReflex`, `ROCFalling`, `CCIFalling`, `CCIChangesDown`, `WPRFalling`, `WPRChangesDown`, `DEMFalling`, `DEMChangesDown` |
| mom_nivel (2) | Osciladores en zona de fuerza (RSI 50-70, estocástico 50-80, CCI 0-150…) y MACD/OSMA/ROC por encima de cero. | ROC en % y MACD/OSMA frente a cero: escalan a cualquier precio. | `RSIHigher`, `RSICrossUp`, `LaguerreRSICrossUP`, `StochSlowDHigher`, `StochSlowDCrossUp`, `CCIHigher`, `CCICrossUp`, `WPRHigher`, `WPRCrossUp`, `QQEValue1Higher`, `QQEValue1CrossAbove`, `MACDMainHigherZero`, `MACDMainCrossAboveZero`, `OSMAHigherZero`, `OSMACrossZeroUp`, `ROCAboveLevel`, `ROCCrossesAboveLevel`, `SchaffTrendCycleAboveLevel`, `SchaffTrendCycleCrossesAboveLevel` | `RSILower`, `RSICrossDown`, `LaguerreRSICrossDown`, `StochSlowDLower`, `StochSlowDCrossDown`, `CCILower`, `CCICrossDown`, `WPRLower`, `WPRCrossDown`, `QQEValue1Lower`, `QQEValue1CrossBelow`, `MACDMainLowerZero`, `MACDMainCrossBelowZero`, `OSMALowerZero`, `OSMACrossZeroDown`, `ROCBelowLevel`, `ROCCrossesBelowLevel`, `SchaffTrendCycleBelowLevel`, `SchaffTrendCycleCrossesBelowLevel` |
| tend_medias (2) | Pendiente y posición del precio respecto a medias (simple, Hull, KAMA, regresión lineal). | Pendiente de medias largas. | `MARising`, `MABarClosesAbove`, `MABarOpensAbove`, `MABarOpensAboveAfterOpenBelow`, `LinRegRising`, `LinRegBarClosesAbove`, `LinRegBarOpensAbove`, `LinRegBarOpensAboveAfterOpenBelow`, `HMARising`, `HMAChangesUP`, `FasterHMAIsAboveSlowerHMA`, `KAMARising`, `FastKAMAAboveSlowKAMA`, `BarClosesAboveKAMA`, `IsUptrend` | `MAFalling`, `MABarClosesBelow`, `MABarOpensBelow`, `MABarOpensBelowAfterOpenAbove`, `LinRegFalling`, `LinRegBarClosesBelow`, `LinRegBarOpensBelow`, `LinRegBarOpensBelowAfterOpenAbove`, `HMAFalling`, `HMAChangesDown`, `FasterHMAIsBelowSlowerHMA`, `KAMAFalling`, `FastKAMABelowSlowKAMA`, `BarClosesBelowKAMA`, `IsDowntrend` |
| tend_sistemas (2) | Sistemas de tendencia: SuperTrend, PSAR, Vortex, Gann HiLo, Aroon, DMI, Woodies. | Sistemas de tendencia lentos. | `SuperTrendUPTrend`, `BarClosesAboveSuperTrend`, `PSARBarLower`, `VortexUptrend`, `VortexChangesTrendUP`, `GannHiLoUPTrend`, `AroonCrossesAbove`, `WoodiesTrendUP`, `WoodiesCCIZeroLineBreakUP`, `DIPlusRising`, `DIPlusChangesUp`, `DICrossUp`, `DIPlusHigher`, `DIMinusFalling`, `DIMinusChangesDown` | `SuperTrendDownTrend`, `BarClosesBelowSuperTrend`, `PSARBarHigher`, `VortexDowntrend`, `VortexChangesTrendDown`, `GannHiLoDownTrend`, `AroonCrossesBelow`, `WoodiesTrendDown`, `WoodiesCCIZeroLineBreakDown`, `DIMinusRising`, `DIMinusChangesUp`, `DICrossDown`, `DIPlusLower`, `DIPlusFalling`, `DIPlusChangesDown` |
| fuerza (1) | ADX creciente o alto y eficiencia de Kaufman alta: hay tendencia. | Filtro auxiliar: amplía la variedad. | `ADXRising`, `ADXChangesUp`, `ADXHigher`, `ADXCrossUp`, `KERaboveLevel` | igual (neutral) |
| tiempo_calendario (1) | Excluir un día de la semana o un mes. | Filtro auxiliar: amplía la variedad. | `BarDayOfWeekIsNot`, `BarMonthIsNot` | igual (neutral) |

#### Indicadores

| Familia (peso) | Qué mide | Por qué en este estilo | Bloques BUY | Espejo SELL |
|---|---|---|---|---|
| niv_canal (3) | Máximo/mínimo de N velas. | Máximos de N días. | `Highest`, `Lowest`(w1) | `Lowest`, `Highest` |
| niv_semanal (2) | Máximo/mínimo/apertura/cierre de la semana. | Máximos semanales. | `HighW`, `LowW`, `OpenW`, `CloseW` | `LowW`, `HighW`, `OpenW`, `CloseW` |
| niv_mensual (2) | Máximo/mínimo/apertura/cierre del mes. | Máximos mensuales. | `HighM`, `LowM`, `OpenM`, `CloseM` | `LowM`, `HighM`, `OpenM`, `CloseM` |
| precio (1) | Apertura, máximo, mínimo y cierre de la vela. | Filtro auxiliar: amplía la variedad. | `Close`, `Open`, `High`, `Low` | `Close`, `Open`, `Low`, `High` |
| medias (2) | Medias móviles (SMA, EMA, LWMA, SMMA, TEMA, Hull, KAMA) y regresión lineal. | Medias largas para comparar. | `SMA`, `EMA`, `LWMA`, `SMMA`, `TEMA`, `HullMovingAverage`, `KAMA`, `LinearRegression` | igual (neutral) |
| sistemas (1) | SuperTrend, Parabolic SAR, Ichimoku y Gann HiLo como valores. | Filtro auxiliar: amplía la variedad. | `SuperTrend`, `ParabolicSAR`, `Ichimoku`, `GannHiLo` | igual (neutral) |
| osciladores (1) | RSI, estocástico, CCI, Williams %R, RSI de Laguerre y DeMarker como valores. | Filtro auxiliar: amplía la variedad. | `RSI`, `Stochastic`, `CCI`, `WilliamsPR`, `LaguerreRSI`, `DeMarker` | igual (neutral) |
| fuerza_ind (1) | ADX, eficiencia de Kaufman, Aroon y Vortex como valores. | Filtro auxiliar: amplía la variedad. | `ADX`, `KaufmanEfficiencyRatio`, `Aroon`, `Vortex` | igual (neutral) |
| volat_ind (1) | ATR y rango verdadero (para comparaciones relativas). | Filtro auxiliar: amplía la variedad. | `ATR`, `TrueRange` | igual (neutral) |
| comparadores (1) | Mayor/menor, mayor o igual, cruces. | Filtro auxiliar: amplía la variedad. | `IsGreater`, `IsLower`, `IsGreaterOrEqual`, `IsLowerOrEqual`, `CrossesAbove`, `CrossesBelow` | `IsLower`, `IsGreater`, `IsLowerOrEqual`, `IsGreaterOrEqual`, `CrossesBelow`, `CrossesAbove` |
| secuencias (1) | N velas seguidas por encima/debajo, subiendo/bajando. | Filtro auxiliar: amplía la variedad. | `IsGreaterCount`, `IsLowerCount`, `IsRising`, `IsFalling` | `IsLowerCount`, `IsGreaterCount`, `IsFalling`, `IsRising` |

#### Niveles y rangos stop/limit

| Familia (peso) | Qué mide | Por qué en este estilo | Bloques BUY | Espejo SELL |
|---|---|---|---|---|
| stl_canal (4) | Orden en el máximo/mínimo de N velas. | Stop sobre máximo de N días. | `Highest`, `Lowest`(w1) | `Lowest`, `Highest` |
| stl_semanal (2) | Orden en niveles de la semana. | Stop sobre máximo semanal. | `HighW`, `LowW`(w1), `OpenW` | `LowW`, `HighW`, `OpenW` |
| stl_mensual (2) | Orden en niveles del mes. | Stop sobre máximo mensual. | `HighM`, `LowM`(w1) | `LowM`, `HighM` |
| stl_vela (1) | Orden en el máximo/mínimo/apertura/cierre de una vela. | Filtro auxiliar: amplía la variedad. | `High`, `Low`, `Open`, `Close` | `Low`, `High`, `Open`, `Close` |
| stl_medias (1) | Orden en una media móvil. | Filtro auxiliar: amplía la variedad. | `SMA`, `EMA`, `LWMA`, `SMMA`, `TEMA`, `HullMovingAverage`, `KAMA`, `LinearRegression` | igual (neutral) |
| stl_sistemas (1) | Orden en SuperTrend, PSAR, Ichimoku o Gann HiLo. | Filtro auxiliar: amplía la variedad. | `SuperTrend`, `ParabolicSAR`, `Ichimoku`, `GannHiLo` | igual (neutral) |
| stl_rangos (1) | Desplazamiento de la orden: k·ATR, rango de vela, rango verdadero, mayor/menor rango, anchura de Bollinger. | Filtro auxiliar: amplía la variedad. | `ATR`, `MTATR`, `BarRange`, `TrueRange`, `BiggestRange`, `SmallestRange`, `BBRange`, `BBWidthRatio` | igual (neutral) |

#### Rangos específicos (BUY → SELL)

| Bloque BUY | Rango BUY | Bloque SELL | Rango SELL |
|---|---|---|---|
| `RSIHigher` | Level 50 a 70 (paso 5) | `RSILower` | Level 30 a 50 (paso 5) |
| `RSICrossUp` | Level 50 a 70 (paso 5) | `RSICrossDown` | Level 30 a 50 (paso 5) |
| `LaguerreRSICrossUP` | Gamma 0.3 a 0.8 (paso 0.05); Level 0.4 a 0.85 (paso 0.05) | `LaguerreRSICrossDown` | Gamma 0.3 a 0.8 (paso 0.05); Level 0.15 a 0.6 (paso 0.05) |
| `StochSlowDHigher` | Level 50 a 80 (paso 5) | `StochSlowDLower` | Level 20 a 50 (paso 5) |
| `StochSlowDCrossUp` | Level 50 a 80 (paso 5) | `StochSlowDCrossDown` | Level 20 a 50 (paso 5) |
| `CCIHigher` | Level 0 a 150 (paso 10) | `CCILower` | Level -150 a 0 (paso 10) |
| `CCICrossUp` | Level 0 a 150 (paso 10) | `CCICrossDown` | Level -150 a 0 (paso 10) |
| `WPRHigher` | Level -50 a -20 (paso 5) | `WPRLower` | Level -80 a -50 (paso 5) |
| `WPRCrossUp` | Level -50 a -20 (paso 5) | `WPRCrossDown` | Level -80 a -50 (paso 5) |
| `QQEValue1Higher` | Level 50 a 70 (paso 5) | `QQEValue1Lower` | Level 30 a 50 (paso 5) |
| `QQEValue1CrossAbove` | Level 50 a 70 (paso 5) | `QQEValue1CrossBelow` | Level 30 a 50 (paso 5) |
| `SchaffTrendCycleAboveLevel` | Level 50 a 90 (paso 5) | `SchaffTrendCycleBelowLevel` | Level 10 a 50 (paso 5) |
| `SchaffTrendCycleCrossesAboveLevel` | Level 25 a 75 (paso 5) | `SchaffTrendCycleCrossesBelowLevel` | Level 25 a 75 (paso 5) |
| `ADXHigher` | Level 20 a 40 (paso 5) | `ADXHigher` | Level 20 a 40 (paso 5) |
| `ADXCrossUp` | Level 20 a 35 (paso 5) | `ADXCrossUp` | Level 20 a 35 (paso 5) |
| `KERaboveLevel` | Level 0.3 a 0.7 (paso 0.05) | `KERaboveLevel` | Level 0.3 a 0.7 (paso 0.05) |
| `SuperTrendUPTrend` | ATR Mult 1.5 a 5 (paso 0.5) | `SuperTrendDownTrend` | ATR Mult 1.5 a 5 (paso 0.5) |
| `BarClosesAboveSuperTrend` | ATR Mult 1.5 a 5 (paso 0.5) | `BarClosesBelowSuperTrend` | ATR Mult 1.5 a 5 (paso 0.5) |
| `Indicators.SuperTrend` | ATR Mult 1.5 a 5 (paso 0.5) | `Indicators.SuperTrend` | ATR Mult 1.5 a 5 (paso 0.5) |
| `Stop/Limit Price Levels.SuperTrend` | ATR Mult 1.5 a 5 (paso 0.5) | `Stop/Limit Price Levels.SuperTrend` | ATR Mult 1.5 a 5 (paso 0.5) |
| `ROCAboveLevel` | Level 0 a 15 (paso 1) | `ROCBelowLevel` | Level -15 a 0 (paso 1) |
| `ROCCrossesAboveLevel` | Level 0 a 15 (paso 1) | `ROCCrossesBelowLevel` | Level -15 a 0 (paso 1) |

### 4. Timeframe, símbolos y horarios

- **Timeframe:** D1.
- **Instrumento recomendado:** Índices (US500/US30/DAX), oro, y pares con tendencia macro. Recomendable ≥15 años de datos.
- **Horario:** D1 sin filtro horario. Las posiciones duran de 1 a 8 semanas; el swap es un componente importante del resultado.

### 5. Salidas y gestión del riesgo

SL 2,5-5 ATR(20-100) diario obligatorio, **sin objetivo**, trailing 2,5-5 ATR (70 %), salida temporal 10-40 días (30 %) y salida por regla (50 %). Riesgo 1 %.

### 6. Filtros y ranking

| Archivo | Fitness | Filtros |
|---|---|---|
| `Estrategia_Build_ConfigInicial_H1_BUY__Position_D1_BUY` | Weighted: ReturnDDRatio (peso 2, max), Stability (peso 1, max) | NumberOfTrades(IS) >= 150; ReturnDDRatio(IS) >= 3; WinningPct(IS) >= 33; ProfitFactor(IS) >= 1.4; AvgBarsInTrade(IS) >= 4 |
| `Estrategia_Retest_ConfigInicial_H1_BUY__Position_D1_BUY` | Weighted: ReturnDDRatio (peso 2, max), Stability (peso 1, max) | NetProfit(OOS) > 0; ReturnDDRatio(Full) >= 4.5; NumberOfTrades(Full) >= 190; NumberOfTrades(OOS) >= 60; DrawdownPct(Full) <= 25 |
| `Ventaja_Build_ConfigInicial_H1_BUY__Position_D1_BUY` | Weighted: ProfitFactor (peso 2, max), StagnationPct (peso 1, min) | NumberOfTrades(IS) >= 150; ReturnDDRatio(IS) >= 1.5; WinningPct(IS) >= 30; ProfitFactor(IS) >= 1.3; AvgBarsInTrade(IS) >= 4 |
| `Ventaja_Retest_ConfigInicial_H1_BUY__Position_D1_BUY` | Weighted: ProfitFactor (peso 2, max), StagnationPct (peso 1, min) | NetProfit(OOS) > 0; ProfitFactor(Full) >= 1.2; NumberOfTrades(Full) >= 190; NumberOfTrades(OOS) >= 60 |

Justificación: Ret/DD + estabilidad; SQN es poco fiable con <200 operaciones. El mínimo de operaciones sale de la densidad del estilo (20/año) multiplicada por los años de cada tramo; el acierto y el Ret/DD se adaptan al estilo. Los archivos SELL usan exactamente los mismos filtros.

### 7. Motor y robustez

- **Builder:** población 25 × 4 islas, 30 generaciones, cruce 80 %, mutación 30 %, migración 10 % cada 10, reinicio por estancamiento a 15.
- **Retest:** activo; precisión 2 (tick real + spread personalizado); 3 condiciones. SPP ±30 %: con periodos largos la superficie debe ser lisa; exigencia 90 %.
- **Monte Carlo:** activo; 500 sims; OHLC ±10 % ATR(14), desliz. 0-1, spread 2-4, vela de inicio. Acepta: NetProfit(Full) >= 0; DrawdownPct(Full) <= 175% de DrawdownPct[main].
- **Manipulación MC:** activo; orden de operaciones 'resampling', saltar 10 %.
- **SPP:** activo; 8000 tests, ±30 %, 6 pasos; ≥90 % rentables.
- **What-if:** activo; ExcludeTradesWithBiggestPl, ExcludeTradesWithLowestPl.

### 8. Riesgos conocidos, sobreoptimización y mitigación

Riesgos propios del estilo: Muestra limitada; dependencia de pocas operaciones grandes; swap acumulado; cambio de régimen macro.

1. Límite físico: con una sola posición abierta y duraciones de semanas, un mercado no da más de ~20-25 operaciones/año. Se exige ese máximo razonable (≥150 en 7,25 años); 300 en 7 años sólo es posible acortando la duración (eso ya es Swing/Trend) o construyendo sobre varios mercados. Máximo 2 condiciones de entrada.
2. Dependencia de 2-3 tendencias grandes: what-if sin las 2 mejores operaciones.
3. Sin OOS en el Builder (no hay muestra suficiente): toda la validación recae en el Retest y en otros mercados.

### 9. Plan de validación

1. **Requisito previo**: ampliar datos (Dukascopy ofrece M1 desde 2003 en mayores e índices) y repetir la construcción con ≥15 años.
2. `Ventaja_Build…Position_D1` (salida 1-6 meses) → `Ventaja_Retest…`.
3. `Estrategia_Build…` → `Estrategia_Retest…Position_D1`.
4. Retest obligatorio en 5+ mercados con los mismos parámetros (el momentum es un fenómeno de cartera).
5. SPP ±30 % y MC con vela de inicio aleatoria.
6. Operar en demo/real con tamaño mínimo al menos 6-12 meses antes de escalar.

---

## TrendFollowing

**Seguimiento de tendencia (multi-filtro con trailing)** · timeframe `H1`

**Archivos del kit** (todos *no validados en SQX*; tabla completa de cambios en `docs/cambios/`):

| Rol | BUY | SELL |
|---|---|---|
| EB | [`Estrategia_Build_ConfigInicial_H1_BUY__TrendFollowing_H1_BUY.cfx`](cambios/Estrategia_Build_ConfigInicial_H1_BUY__TrendFollowing_H1_BUY.md) | [`Estrategia_Build_ConfigInicial_H1_BUY__TrendFollowing_H1_SELL.cfx`](cambios/Estrategia_Build_ConfigInicial_H1_BUY__TrendFollowing_H1_SELL.md) |
| ER | [`Estrategia_Retest_ConfigInicial_H1_BUY__TrendFollowing_H1_BUY.cfx`](cambios/Estrategia_Retest_ConfigInicial_H1_BUY__TrendFollowing_H1_BUY.md) | [`Estrategia_Retest_ConfigInicial_H1_BUY__TrendFollowing_H1_SELL.cfx`](cambios/Estrategia_Retest_ConfigInicial_H1_BUY__TrendFollowing_H1_SELL.md) |
| VB | [`Ventaja_Build_ConfigInicial_H1_BUY__TrendFollowing_H1_BUY.cfx`](cambios/Ventaja_Build_ConfigInicial_H1_BUY__TrendFollowing_H1_BUY.md) | [`Ventaja_Build_ConfigInicial_H1_BUY__TrendFollowing_H1_SELL.cfx`](cambios/Ventaja_Build_ConfigInicial_H1_BUY__TrendFollowing_H1_SELL.md) |
| VR | [`Ventaja_Retest_ConfigInicial_H1_BUY__TrendFollowing_H1_BUY.cfx`](cambios/Ventaja_Retest_ConfigInicial_H1_BUY__TrendFollowing_H1_BUY.md) | [`Ventaja_Retest_ConfigInicial_H1_BUY__TrendFollowing_H1_SELL.cfx`](cambios/Ventaja_Retest_ConfigInicial_H1_BUY__TrendFollowing_H1_SELL.md) |

**Operaciones mínimas exigidas** (50/año): Builder IS ≥ 260, OOS 2019-2020 ≥ 80 (≈340 en 7.3 años de construcción); Retest periodo completo ≥ 490 y holdout 2021-2024 ≥ 140.

### 1. Tesis

Las tendencias persisten más de lo que predice un paseo aleatorio (reacción lenta a la información, flujos institucionales). Se entra cuando varios filtros de tendencia coinciden y se sale por trailing: pocas ganancias grandes pagan muchas pérdidas pequeñas. En H1 para tener una muestra de cientos de operaciones (tendencias de 1-5 días).

### 2. Cambios respecto al original

#### 2.a Builder de estrategia completa (`Estrategia_Build`)

| Parámetro | Original | Nuevo | Justificación |
|---|---|---|---|
| Timeframe | H1 | H1 | Sin cambio. |
| Periodo de datos | 2013.09.30 – 2020.12.31 | 2013.09.30 – 2020.12.31 | Sin cambio. |
| Tramo OOS | sin OOS | 2019.01.01 – 2020.12.31 | Validación dentro del Builder: el original filtraba sólo sobre IS. |
| Deslizamiento (pips) | 0 | 0.3 | El original usa 0. |
| Modo de generación | template (plantilla externa .sqx) | simple | El original dependía de una plantilla .sqx no incluida; en modo simple el archivo es autónomo (docs/04 §A.3 para volver a plantilla). |
| Condiciones de entrada | 0–0 | 1–3 | Nivel + 1-2 filtros como máximo; más condiciones = más grados de libertad. |
| Periodos de indicadores | 4–200 | 10–250 | 10-250 velas H1 = 10 h a 10 días. |
| Desplazamiento (shift) | 1–1 | 1–1 | Sin cambio. |
| Tipos de salida (mín–máx) | 1–5 | 2–4 | SL obligatorio + salidas propias del estilo (el original pedía hasta 5 con 3 disponibles). |
| Tipos de orden | EnterAtMarket (w1) | EnterAtMarket (w2), EnterAtStop (w2, válida 1-4 velas) | A mercado con confirmación o stop sobre máximo reciente. |
| Stop loss | obligatorio=true; 1-3 × ATR(20-100) | obligatorio=true; 2-4 × ATR(14-100) | El trailing (prob. 80 %) es la salida natural; objetivo raro y lejano. |
| Profit target | obligatorio=true; 2-5 × ATR(20-100); PT=100-500 % del SL | obligatorio=false; 4-10 × ATR(14-100) | El trailing (prob. 80 %) es la salida natural; objetivo raro y lejano. |
| Trailing stop | sí (50 %), fijo 50-100 pips, 1-5 ATR | sí (80 %), 2.5-5 ATR | El trailing (prob. 80 %) es la salida natural; objetivo raro y lejano. |
| Break-even | no | no | Sin cambio. |
| Salida temporal | no | no | Sin cambio. |
| Salida por regla | no | sí (50 %) | El trailing (prob. 80 %) es la salida natural; objetivo raro y lejano. |
| Ventana de señales | 01:30-23:30 | 01:30-23:30 | Sin cambio. |
| Cierres forzados | no diario; no viernes | no diario; no viernes | Sin cambio. |
| Máx. operaciones/día | 0 (sin límite) | 2 | Hasta dos entradas diarias. |
| Distancia máx. orden | no | 2 % | 2 %: rupturas de canales largos en H1. |
| Bloques activos | 146 señales / 29 indicadores / 29 stop-limit | 105 señales / 46 indicadores / 33 stop-limit | Núcleo: sistemas y medias de tendencia, fuerza (ADX/KER) y ruptura de canal; sin osciladores de sobrecompra/sobreventa (contradicen la tesis). |
| Gestión monetaria | FixedAmount: riesgo 100 por operación | FixedAmount: riesgo 100 por operación | Sin cambio. |
| Fitness | type="ReturnDDRatio" | Weighted: ReturnDDRatio (peso 2, max), StagnationPct (peso 1, min) | El talón de Aquiles del TF son las rachas planas largas: StagnationPct las penaliza. |
| Filtros (Ranking) | AvgBarsInTrade(IS) >= 2; ReturnDDRatio(IS) >= 8; NumberOfTrades(IS) >= 300; WinningPct(IS) >= 40 | NumberOfTrades(IS) >= 260; ReturnDDRatio(IS) >= 3.5; WinningPct(IS) >= 30; ProfitFactor(IS) >= 1.3; AvgBarsInTrade(IS) >= 5; NetProfit(OOS) > 0; NumberOfTrades(OOS) >= 80 | Umbrales del estilo + exigencia OOS. |
| Filtro población inicial | ReturnDDRatio(IS) >= 5; AvgBarsInTrade(IS) >= 2; NumberOfTrades(IS) >= 250; WinningPct(IS) >= 35 | NumberOfTrades(IS) >= 80 | Sólo nº mínimo de operaciones (recomendación de SQX): con filtros de rentabilidad la población inicial puede tardar horas/días y el Builder no guarda nada mientras tanto. |
| Motor genético | población 5 × 5 islas, 10 generaciones, cruce 46 %, mutación 35 %, migración 6 % cada 5, reinicio por estancamiento a 30 | población 25 × 4 islas, 30 generaciones, cruce 80 %, mutación 30 %, migración 10 % cada 10, reinicio por estancamiento a 15 | 80-100 individuos por generación (el original 25-75) y 30 generaciones (el original 10, insuficiente para que la evolución actúe). |
| Calibración de indicadores | false | true | Recalibra los rangos de valores de indicadores y de rangos stop/limit (±5000 por defecto) para el símbolo y timeframe antes de construir. |

#### 2.b Builder de test de ventaja (`Ventaja_Build`)

| Parámetro | Original | Nuevo | Justificación |
|---|---|---|---|
| Timeframe | H1 | H1 | Sin cambio. |
| Periodo de datos | 2013.09.30 – 2020.12.31 | 2013.09.30 – 2020.12.31 | Sin cambio. |
| Tramo OOS | sin OOS | 2019.01.01 – 2020.12.31 | Validación dentro del Builder: el original filtraba sólo sobre IS. |
| Deslizamiento (pips) | 0 | 0.3 | El original usa 0. |
| Modo de generación | simple | simple | Sin cambio. |
| Condiciones de entrada | 1–3 | 1–3 | Sin cambio. |
| Periodos de indicadores | 4–200 | 10–250 | 10-250 velas H1 = 10 h a 10 días. |
| Desplazamiento (shift) | 1–1 | 1–1 | Sin cambio. |
| Tipos de salida (mín–máx) | 1–5 | 1–1 | Sólo la salida temporal (test de ventaja). |
| Tipos de orden | EnterAtMarket (w1) | EnterAtMarket (w2), EnterAtStop (w2, válida 1-4 velas) | A mercado con confirmación o stop sobre máximo reciente. |
| Stop loss | obligatorio=false; sin ATR | obligatorio=false; sin ATR | Sin cambio. |
| Profit target | obligatorio=false; sin ATR | obligatorio=false; sin ATR | Sin cambio. |
| Trailing stop | no | no | Sin cambio. |
| Break-even | no | no | Sin cambio. |
| Salida temporal | sí (50 %), 2-15 velas | sí (100 %), 12-72 velas | Test de ventaja: salida por tiempo 12 h-3 días. |
| Salida por regla | no | no | Sin cambio. |
| Ventana de señales | 01:30-23:30 | 01:30-23:30 | Sin cambio. |
| Cierres forzados | no diario; no viernes | no diario; no viernes | Sin cambio. |
| Máx. operaciones/día | 0 (sin límite) | 2 | Hasta dos entradas diarias. |
| Distancia máx. orden | no | 2 % | 2 %: rupturas de canales largos en H1. |
| Bloques activos | 146 señales / 29 indicadores / 29 stop-limit | 105 señales / 46 indicadores / 33 stop-limit | Núcleo: sistemas y medias de tendencia, fuerza (ADX/KER) y ruptura de canal; sin osciladores de sobrecompra/sobreventa (contradicen la tesis). |
| Gestión monetaria | FixedSize: 1 lote | FixedSize: 1 lote | Sin cambio. |
| Fitness | Weighted: Stagnation (peso 1, min) | Weighted: SQN (peso 2, max), StagnationPct (peso 1, min) | SQN mide la calidad estadística de la entrada; el original optimizaba sólo 'Stagnation', que ignora el beneficio. |
| Filtros (Ranking) | AvgBarsInTrade(IS) >= 2; ReturnDDRatio(IS) >= 4; NumberOfTrades(IS) >= 300; WinningPct(IS) >= 40 | NumberOfTrades(IS) >= 260; ReturnDDRatio(IS) >= 1.75; WinningPct(IS) >= 30; ProfitFactor(IS) >= 1.15; AvgBarsInTrade(IS) >= 5; NetProfit(OOS) > 0; NumberOfTrades(OOS) >= 80 | Umbrales del estilo + exigencia OOS. Test de ventaja: Ret/DD a la mitad y PF ≥1,15. |
| Filtro población inicial | ReturnDDRatio(IS) >= 2; AvgBarsInTrade(IS) >= 2; NumberOfTrades(IS) >= 250; WinningPct(IS) >= 35 | NumberOfTrades(IS) >= 80 | Sólo nº mínimo de operaciones (recomendación de SQX): con filtros de rentabilidad la población inicial puede tardar horas/días y el Builder no guarda nada mientras tanto. |
| Motor genético | población 15 × 5 islas, 10 generaciones, cruce 46 %, mutación 35 %, migración 6 % cada 5, reinicio por estancamiento a 30 | población 25 × 4 islas, 30 generaciones, cruce 80 %, mutación 30 %, migración 10 % cada 10, reinicio por estancamiento a 15 | 80-100 individuos por generación (el original 25-75) y 30 generaciones (el original 10, insuficiente para que la evolución actúe). |
| Calibración de indicadores | false | true | Recalibra los rangos de valores de indicadores y de rangos stop/limit (±5000 por defecto) para el símbolo y timeframe antes de construir. |

#### 2.c Retesters (`Estrategia_Retest` / `Ventaja_Retest`)

| Parámetro | Original | Nuevo | Justificación |
|---|---|---|---|
| Timeframe | H1 | H1 | Sin cambio. |
| Periodo / OOS | 2013.09.30 – 2024.07.22; OOS 2021.01.01 – 2024.07.22 | 2013.09.30 – 2024.07.22; OOS 2021.01.01 – 2024.07.22 | Sin cambio. |
| Deslizamiento | 0 | 0.3 | El original usa 0. |
| Ventana de señales | 01:30-23:30 | 01:30-23:30 | Sin cambio. |
| Cierres forzados | no diario; no viernes | no diario; no viernes | Sin cambio. |
| Gestión monetaria | FixedAmount: riesgo 100 por operación | FixedAmount: riesgo 100 por operación | Sin cambio. |
| Fitness | type="ReturnDDRatio" | Weighted: ReturnDDRatio (peso 2, max), StagnationPct (peso 1, min) | Igual que el Builder correspondiente. |
| Filtros (Ranking) | (ninguna activa) | NetProfit(OOS) > 0; ProfitFactor(OOS) >= 1.05; ReturnDDRatio(Full) >= 5.25; NumberOfTrades(Full) >= 490; NumberOfTrades(OOS) >= 140; DrawdownPct(Full) <= 25 | El original no filtraba nada (todas use=false) ni borraba fallidas. |
| Mayor precisión | activo; precisión 2 (tick real + spread personalizado); 1 condiciones | activo; precisión 2 (tick real + spread personalizado); 3 condiciones | Se activan también las condiciones de nº de operaciones y DD. |
| Monte Carlo retest | activo; 1000 sims; OHLC ±10 % ATR(14), spread 1-3. Acepta: NetProfit(IS) >= 0 | activo; 500 sims; OHLC ±10 % ATR(14), desliz. 0-0.5, spread 2-4, vela de inicio. Acepta: NetProfit(Full) >= 0; DrawdownPct(Full) <= 175% de DrawdownPct[main] | Spread desde el base hasta 2-4x, deslizamiento, percentil 95 (no el peor caso) y control del DD. |
| Monte Carlo manipulación | no; orden de operaciones 'exact', saltar 10 % | activo; orden de operaciones 'resampling', saltar 10 % | Barato; 'resampling' y referencia corregida (el original comparaba MC contra MC). |
| SPP / perfil de optimización | activo; 15000 tests, ±20 %, 6 pasos; ≥95 % rentables | activo; 5000 tests, ±30 %, 6 pasos; ≥90 % rentables | Tests y exigencia ajustados al coste de cómputo y a la sensibilidad del estilo. |
| What-if | no; ExcludePctTradesWithBiggestPl, ExcludePctTradesWithLowestPl | activo; ExcludeTradesWithBiggestPl, ExcludeTradesWithLowestPl | Quitar 2 mejores/peores (estilos de outliers). |

Diferencias del `Ventaja_Retest` respecto al anterior:

- **Gestión monetaria:** FixedSize: 1 lote
- **Fitness:** Weighted: SQN (peso 2, max), StagnationPct (peso 1, min)
- **Filtros (Ranking):** NetProfit(OOS) > 0; ProfitFactor(Full) >= 1.1; NumberOfTrades(Full) >= 490; NumberOfTrades(OOS) >= 140

### 3. Indicadores y bloques seleccionados

Criterio general: Núcleo: sistemas y medias de tendencia, fuerza (ADX/KER) y ruptura de canal; sin osciladores de sobrecompra/sobreventa (contradicen la tesis).

Recuento: **105 señales, 46 indicadores y 33 niveles/rangos stop-limit** (el original: 146 / 29 / 29, todos con peso 1 y sin relación con la tesis). Las familias con peso ≥ 2 son el núcleo del estilo; las de peso 1 son filtros auxiliares que amplían la variedad de estrategias sin cambiar la tesis. Se excluyen siempre los bloques con niveles absolutos dependientes del precio. La columna SELL muestra el bloque espejo que se activa en el kit de ventas.

#### Señales

| Familia (peso) | Qué mide | Por qué en este estilo | Bloques BUY | Espejo SELL |
|---|---|---|---|---|
| tend_sistemas (4) | Sistemas de tendencia: SuperTrend, PSAR, Vortex, Gann HiLo, Aroon, DMI, Woodies. | Núcleo: estimadores independientes de tendencia. | `SuperTrendUPTrend`, `BarClosesAboveSuperTrend`, `PSARBarLower`, `VortexUptrend`, `VortexChangesTrendUP`, `GannHiLoUPTrend`, `AroonCrossesAbove`, `WoodiesTrendUP`, `WoodiesCCIZeroLineBreakUP`, `DIPlusRising`, `DIPlusChangesUp`, `DICrossUp`, `DIPlusHigher`, `DIMinusFalling`, `DIMinusChangesDown` | `SuperTrendDownTrend`, `BarClosesBelowSuperTrend`, `PSARBarHigher`, `VortexDowntrend`, `VortexChangesTrendDown`, `GannHiLoDownTrend`, `AroonCrossesBelow`, `WoodiesTrendDown`, `WoodiesCCIZeroLineBreakDown`, `DIMinusRising`, `DIMinusChangesUp`, `DICrossDown`, `DIPlusLower`, `DIPlusFalling`, `DIPlusChangesDown` |
| tend_medias (2) | Pendiente y posición del precio respecto a medias (simple, Hull, KAMA, regresión lineal). | Pendiente y posición frente a medias. | `MARising`, `MABarClosesAbove`, `MABarOpensAbove`, `MABarOpensAboveAfterOpenBelow`, `LinRegRising`, `LinRegBarClosesAbove`, `LinRegBarOpensAbove`, `LinRegBarOpensAboveAfterOpenBelow`, `HMARising`, `HMAChangesUP`, `FasterHMAIsAboveSlowerHMA`, `KAMARising`, `FastKAMAAboveSlowKAMA`, `BarClosesAboveKAMA`, `IsUptrend` | `MAFalling`, `MABarClosesBelow`, `MABarOpensBelow`, `MABarOpensBelowAfterOpenAbove`, `LinRegFalling`, `LinRegBarClosesBelow`, `LinRegBarOpensBelow`, `LinRegBarOpensBelowAfterOpenAbove`, `HMAFalling`, `HMAChangesDown`, `FasterHMAIsBelowSlowerHMA`, `KAMAFalling`, `FastKAMABelowSlowKAMA`, `BarClosesBelowKAMA`, `IsDowntrend` |
| fuerza (3) | ADX creciente o alto y eficiencia de Kaufman alta: hay tendencia. | Sólo operar tendencias con fuerza. | `ADXRising`, `ADXChangesUp`, `ADXHigher`, `ADXCrossUp`, `KERaboveLevel` | igual (neutral) |
| rup_canal (6) | Apertura por encima del máximo de N velas tras abrir por debajo (ruptura Donchian confirmada). | Entrada por ruptura de canal (Donchian), la clásica del TF. | `BarOpensAboveHighestAfterOpenBelow` | `BarOpensBelowLowestAfterOpenAbove` |
| rup_ichimoku (2) | Salida de la nube y cruces alcistas de Ichimoku. | Ruptura de la nube. | `IchimokuKumoBreakoutBullish`, `IchimokuKijunSenCrossBullish`, `IchimokuSenkouSpanCrossBullish`, `IchimokuTenkanKijunCrossBullish` | `IchimokuKumoBreakoutBearish`, `IchimokuKijunSenCrossBearish`, `IchimokuSenkouSpanCrossBearish`, `IchimokuTenkanKijunCrossBearish` |
| rup_bandas (1) | Apertura/cierre fuera de la banda superior de Bollinger o Keltner. | Filtro auxiliar: amplía la variedad. | `BBBarOpensAboveUpAfterOpenBelow`, `BBBarClosesAboveUp`, `BBBarOpensAboveUp`, `KCBarOpensAboveUpperAfterOpenBelow`, `KCBarClosesAboveUpper`, `KCBarOpensAboveUpper` | `BBBarOpensBelowDownAfterOpenAbove`, `BBBarClosesBelowDown`, `BBBarOpensBelowDown`, `KCBarOpensBelowLowerAfterOpenAbove`, `KCBarClosesBelowLower`, `KCBarOpensBelowLower` |
| mom_direccion (1) | Osciladores y momentum girando o subiendo (RSI, estocástico, MACD, OSMA, QQE, Reflex, ROC, CCI, WPR, DeMarker…), sin niveles absolutos. | Filtro auxiliar: amplía la variedad. | `RSIRising`, `RSIChangesUp`, `LaguerreRSIRising`, `LaguerreRSIChangesUP`, `StochSlowDRising`, `StochSlowDChangesUp`, `StochFastKUp`, `MomRising`, `MomChangesUp`, `MACDMainRising`, `MACDMainChangesUp`, `MACDMainCrossAboveSignal`, `MACDMainHigherSignal`, `MACDSignalRising`, `OSMARising`, `OSMAChangesUp`, `AWORising`, `AWOChangesUp`, `QQEValue1Rising`, `QQEValue1CrossAboveValue2`, `QQEValue1HigherValue2`, `QQEValue2Rising`, `ReflexRising`, `ReflexChangesDirectionUP`, `FastReflexCrossUPSlowReflex`, `ROCRising`, `CCIRising`, `CCIChangesUp`, `WPRRising`, `WPRChangesUp`, `DEMRising`, `DEMChangesUp` | `RSIFalling`, `RSIChangesDown`, `LaguerreRSIFalling`, `LaguerreRSIChangesDown`, `StochSlowDFalling`, `StochSlowDChangesDown`, `StochFastKDown`, `MomFalling`, `MomChangesDown`, `MACDMainFalling`, `MACDMainChangesDown`, `MACDMainCrossBelowSignal`, `MACDMainLowerSignal`, `MACDSignalFalling`, `OSMAFalling`, `OSMAChangesDown`, `AWOFalling`, `AWOChangesDown`, `QQEValue1Falling`, `QQEValue1CrossBelowValue2`, `QQEValue1LowerValue2`, `QQEValue2Falling`, `ReflexFalling`, `ReflexChangesDirectionDown`, `FastReflexCrossDownSlowReflex`, `ROCFalling`, `CCIFalling`, `CCIChangesDown`, `WPRFalling`, `WPRChangesDown`, `DEMFalling`, `DEMChangesDown` |
| mom_nivel (1) | Osciladores en zona de fuerza (RSI 50-70, estocástico 50-80, CCI 0-150…) y MACD/OSMA/ROC por encima de cero. | Filtro auxiliar: amplía la variedad. | `RSIHigher`, `RSICrossUp`, `LaguerreRSICrossUP`, `StochSlowDHigher`, `StochSlowDCrossUp`, `CCIHigher`, `CCICrossUp`, `WPRHigher`, `WPRCrossUp`, `QQEValue1Higher`, `QQEValue1CrossAbove`, `MACDMainHigherZero`, `MACDMainCrossAboveZero`, `OSMAHigherZero`, `OSMACrossZeroUp`, `ROCAboveLevel`, `ROCCrossesAboveLevel`, `SchaffTrendCycleAboveLevel`, `SchaffTrendCycleCrossesAboveLevel` | `RSILower`, `RSICrossDown`, `LaguerreRSICrossDown`, `StochSlowDLower`, `StochSlowDCrossDown`, `CCILower`, `CCICrossDown`, `WPRLower`, `WPRCrossDown`, `QQEValue1Lower`, `QQEValue1CrossBelow`, `MACDMainLowerZero`, `MACDMainCrossBelowZero`, `OSMALowerZero`, `OSMACrossZeroDown`, `ROCBelowLevel`, `ROCCrossesBelowLevel`, `SchaffTrendCycleBelowLevel`, `SchaffTrendCycleCrossesBelowLevel` |
| vol_expansion (1) | ATR/desviación típica/bandas abriéndose: entra volatilidad. | Filtro auxiliar: amplía la variedad. | `ATRRising`, `ATRChangesUp`, `StdDevRising`, `StdDevChangesUp`, `BBUpperRising`, `BBLowerFalling`, `KCUpperRising`, `KCLowerFalling` | igual (neutral) |

#### Indicadores

| Familia (peso) | Qué mide | Por qué en este estilo | Bloques BUY | Espejo SELL |
|---|---|---|---|---|
| medias (2) | Medias móviles (SMA, EMA, LWMA, SMMA, TEMA, Hull, KAMA) y regresión lineal. | Medias para comparar. | `SMA`, `EMA`, `LWMA`, `SMMA`, `TEMA`, `HullMovingAverage`, `KAMA`, `LinearRegression` | igual (neutral) |
| sistemas (2) | SuperTrend, Parabolic SAR, Ichimoku y Gann HiLo como valores. | SuperTrend/PSAR/Ichimoku. | `SuperTrend`, `ParabolicSAR`, `Ichimoku`, `GannHiLo` | igual (neutral) |
| niv_canal (2) | Máximo/mínimo de N velas. | Canales. | `Highest`, `Lowest`(w1) | `Lowest`, `Highest` |
| niv_diario (1) | Máximo/mínimo/apertura/cierre del día. | Filtro auxiliar: amplía la variedad. | `HighD`, `LowD`, `OpenD`, `CloseD` | `LowD`, `HighD`, `OpenD`, `CloseD` |
| precio (1) | Apertura, máximo, mínimo y cierre de la vela. | Filtro auxiliar: amplía la variedad. | `Close`, `Open`, `High`, `Low` | `Close`, `Open`, `Low`, `High` |
| bandas (1) | Bandas de Bollinger y canal de Keltner. | Filtro auxiliar: amplía la variedad. | `BollingerBands`, `KeltnerChannel` | igual (neutral) |
| fuerza_ind (1) | ADX, eficiencia de Kaufman, Aroon y Vortex como valores. | Filtro auxiliar: amplía la variedad. | `ADX`, `KaufmanEfficiencyRatio`, `Aroon`, `Vortex` | igual (neutral) |
| osciladores (1) | RSI, estocástico, CCI, Williams %R, RSI de Laguerre y DeMarker como valores. | Filtro auxiliar: amplía la variedad. | `RSI`, `Stochastic`, `CCI`, `WilliamsPR`, `LaguerreRSI`, `DeMarker` | igual (neutral) |
| volat_ind (1) | ATR y rango verdadero (para comparaciones relativas). | Filtro auxiliar: amplía la variedad. | `ATR`, `TrueRange` | igual (neutral) |
| comparadores (1) | Mayor/menor, mayor o igual, cruces. | Filtro auxiliar: amplía la variedad. | `IsGreater`, `IsLower`, `IsGreaterOrEqual`, `IsLowerOrEqual`, `CrossesAbove`, `CrossesBelow` | `IsLower`, `IsGreater`, `IsLowerOrEqual`, `IsGreaterOrEqual`, `CrossesBelow`, `CrossesAbove` |
| secuencias (1) | N velas seguidas por encima/debajo, subiendo/bajando. | Filtro auxiliar: amplía la variedad. | `IsGreaterCount`, `IsLowerCount`, `IsRising`, `IsFalling` | `IsLowerCount`, `IsGreaterCount`, `IsFalling`, `IsRising` |

#### Niveles y rangos stop/limit

| Familia (peso) | Qué mide | Por qué en este estilo | Bloques BUY | Espejo SELL |
|---|---|---|---|---|
| stl_canal (4) | Orden en el máximo/mínimo de N velas. | Stop sobre máximo reciente. | `Highest`, `Lowest`(w1) | `Lowest`, `Highest` |
| stl_sistemas (2) | Orden en SuperTrend, PSAR, Ichimoku o Gann HiLo. | Stop en SuperTrend/PSAR. | `SuperTrend`, `ParabolicSAR`, `Ichimoku`, `GannHiLo` | igual (neutral) |
| stl_medias (1) | Orden en una media móvil. | Filtro auxiliar: amplía la variedad. | `SMA`, `EMA`, `LWMA`, `SMMA`, `TEMA`, `HullMovingAverage`, `KAMA`, `LinearRegression` | igual (neutral) |
| stl_bandas (1) | Orden en Bollinger/Keltner. | Filtro auxiliar: amplía la variedad. | `BollingerBands`, `KeltnerChannel`, `MTKeltnerChannel` | igual (neutral) |
| stl_vela (1) | Orden en el máximo/mínimo/apertura/cierre de una vela. | Filtro auxiliar: amplía la variedad. | `High`, `Low`, `Open`, `Close` | `Low`, `High`, `Open`, `Close` |
| stl_diario (1) | Orden en niveles del día. | Filtro auxiliar: amplía la variedad. | `HighD`, `LowD`, `OpenD`, `CloseD` | `LowD`, `HighD`, `OpenD`, `CloseD` |
| stl_rangos (2) | Desplazamiento de la orden: k·ATR, rango de vela, rango verdadero, mayor/menor rango, anchura de Bollinger. | Margen en ATR. | `ATR`, `MTATR`, `BarRange`, `TrueRange`, `BiggestRange`, `SmallestRange`, `BBRange`, `BBWidthRatio` | igual (neutral) |

#### Rangos específicos (BUY → SELL)

| Bloque BUY | Rango BUY | Bloque SELL | Rango SELL |
|---|---|---|---|
| `RSIHigher` | Level 50 a 70 (paso 5) | `RSILower` | Level 30 a 50 (paso 5) |
| `RSICrossUp` | Level 50 a 70 (paso 5) | `RSICrossDown` | Level 30 a 50 (paso 5) |
| `LaguerreRSICrossUP` | Gamma 0.3 a 0.8 (paso 0.05); Level 0.4 a 0.85 (paso 0.05) | `LaguerreRSICrossDown` | Gamma 0.3 a 0.8 (paso 0.05); Level 0.15 a 0.6 (paso 0.05) |
| `StochSlowDHigher` | Level 50 a 80 (paso 5) | `StochSlowDLower` | Level 20 a 50 (paso 5) |
| `StochSlowDCrossUp` | Level 50 a 80 (paso 5) | `StochSlowDCrossDown` | Level 20 a 50 (paso 5) |
| `CCIHigher` | Level 0 a 150 (paso 10) | `CCILower` | Level -150 a 0 (paso 10) |
| `CCICrossUp` | Level 0 a 150 (paso 10) | `CCICrossDown` | Level -150 a 0 (paso 10) |
| `WPRHigher` | Level -50 a -20 (paso 5) | `WPRLower` | Level -80 a -50 (paso 5) |
| `WPRCrossUp` | Level -50 a -20 (paso 5) | `WPRCrossDown` | Level -80 a -50 (paso 5) |
| `QQEValue1Higher` | Level 50 a 70 (paso 5) | `QQEValue1Lower` | Level 30 a 50 (paso 5) |
| `QQEValue1CrossAbove` | Level 50 a 70 (paso 5) | `QQEValue1CrossBelow` | Level 30 a 50 (paso 5) |
| `SchaffTrendCycleAboveLevel` | Level 50 a 90 (paso 5) | `SchaffTrendCycleBelowLevel` | Level 10 a 50 (paso 5) |
| `SchaffTrendCycleCrossesAboveLevel` | Level 25 a 75 (paso 5) | `SchaffTrendCycleCrossesBelowLevel` | Level 25 a 75 (paso 5) |
| `ADXHigher` | Level 20 a 40 (paso 5) | `ADXHigher` | Level 20 a 40 (paso 5) |
| `ADXCrossUp` | Level 20 a 35 (paso 5) | `ADXCrossUp` | Level 20 a 35 (paso 5) |
| `KERaboveLevel` | Level 0.3 a 0.7 (paso 0.05) | `KERaboveLevel` | Level 0.3 a 0.7 (paso 0.05) |
| `SuperTrendUPTrend` | ATR Mult 1.5 a 5 (paso 0.5) | `SuperTrendDownTrend` | ATR Mult 1.5 a 5 (paso 0.5) |
| `BarClosesAboveSuperTrend` | ATR Mult 1.5 a 5 (paso 0.5) | `BarClosesBelowSuperTrend` | ATR Mult 1.5 a 5 (paso 0.5) |
| `Indicators.SuperTrend` | ATR Mult 1.5 a 5 (paso 0.5) | `Indicators.SuperTrend` | ATR Mult 1.5 a 5 (paso 0.5) |
| `Stop/Limit Price Levels.SuperTrend` | ATR Mult 1.5 a 5 (paso 0.5) | `Stop/Limit Price Levels.SuperTrend` | ATR Mult 1.5 a 5 (paso 0.5) |
| `ROCAboveLevel` | Level 0 a 3 (paso 0.1) | `ROCBelowLevel` | Level -3 a 0 (paso 0.1) |
| `ROCCrossesAboveLevel` | Level 0 a 3 (paso 0.1) | `ROCCrossesBelowLevel` | Level -3 a 0 (paso 0.1) |

### 4. Timeframe, símbolos y horarios

- **Timeframe:** H1.
- **Instrumento recomendado:** Índices, metales y cruces de JPY. En un solo símbolo el resultado depende de pocas tendencias: validar en varios mercados.
- **Horario:** H1 con la ventana original 01:30-23:30 (evita el rollover); mantiene posiciones de 1 a 5 días.

### 5. Salidas y gestión del riesgo

SL 2-4 ATR(14-100) de H1; **trailing 2,5-5 ATR como salida principal (80 %)**; objetivo raro y lejano (4-10 ATR, 30 %); salida por regla (50 %). Acierto esperado 30-40 %. Riesgo 1 %.

### 6. Filtros y ranking

| Archivo | Fitness | Filtros |
|---|---|---|
| `Estrategia_Build_ConfigInicial_H1_BUY__TrendFollowing_H1_BUY` | Weighted: ReturnDDRatio (peso 2, max), StagnationPct (peso 1, min) | NumberOfTrades(IS) >= 260; ReturnDDRatio(IS) >= 3.5; WinningPct(IS) >= 30; ProfitFactor(IS) >= 1.3; AvgBarsInTrade(IS) >= 5; NetProfit(OOS) > 0; NumberOfTrades(OOS) >= 80 |
| `Estrategia_Retest_ConfigInicial_H1_BUY__TrendFollowing_H1_BUY` | Weighted: ReturnDDRatio (peso 2, max), StagnationPct (peso 1, min) | NetProfit(OOS) > 0; ProfitFactor(OOS) >= 1.05; ReturnDDRatio(Full) >= 5.25; NumberOfTrades(Full) >= 490; NumberOfTrades(OOS) >= 140; DrawdownPct(Full) <= 25 |
| `Ventaja_Build_ConfigInicial_H1_BUY__TrendFollowing_H1_BUY` | Weighted: SQN (peso 2, max), StagnationPct (peso 1, min) | NumberOfTrades(IS) >= 260; ReturnDDRatio(IS) >= 1.75; WinningPct(IS) >= 30; ProfitFactor(IS) >= 1.15; AvgBarsInTrade(IS) >= 5; NetProfit(OOS) > 0; NumberOfTrades(OOS) >= 80 |
| `Ventaja_Retest_ConfigInicial_H1_BUY__TrendFollowing_H1_BUY` | Weighted: SQN (peso 2, max), StagnationPct (peso 1, min) | NetProfit(OOS) > 0; ProfitFactor(Full) >= 1.1; NumberOfTrades(Full) >= 490; NumberOfTrades(OOS) >= 140 |

Justificación: El talón de Aquiles del TF son las rachas planas largas: StagnationPct las penaliza. El mínimo de operaciones sale de la densidad del estilo (50/año) multiplicada por los años de cada tramo; el acierto y el Ret/DD se adaptan al estilo. Los archivos SELL usan exactamente los mismos filtros.

### 7. Motor y robustez

- **Builder:** población 25 × 4 islas, 30 generaciones, cruce 80 %, mutación 30 %, migración 10 % cada 10, reinicio por estancamiento a 15.
- **Retest:** activo; precisión 2 (tick real + spread personalizado); 3 condiciones. What-if quita las 2 mejores operaciones: mide la dependencia de outliers (esperable en TF, pero no puede volverse perdedor).
- **Monte Carlo:** activo; 500 sims; OHLC ±10 % ATR(14), desliz. 0-0.5, spread 2-4, vela de inicio. Acepta: NetProfit(Full) >= 0; DrawdownPct(Full) <= 175% de DrawdownPct[main].
- **Manipulación MC:** activo; orden de operaciones 'resampling', saltar 10 %.
- **SPP:** activo; 5000 tests, ±30 %, 6 pasos; ≥90 % rentables.
- **What-if:** activo; ExcludeTradesWithBiggestPl, ExcludeTradesWithLowestPl.

### 8. Riesgos conocidos, sobreoptimización y mitigación

Riesgos propios del estilo: Win rate bajo (30-40 %) y rachas perdedoras largas; dependencia de pocas tendencias.

1. Pocas operaciones ganadoras explican todo el beneficio: what-if sin las 2 mejores y 2 peores.
2. Rachas planas largas: `StagnationPct` en la fitness.
3. En un solo símbolo el resultado depende de pocas tendencias: validar en cesta.

### 9. Plan de validación

1. `Ventaja_Build…TrendFollowing_H1` (salida 12 h-3 días) → `Ventaja_Retest…`.
2. `Estrategia_Build…` → `Estrategia_Retest…TrendFollowing_H1`.
3. Retest en 5+ mercados no correlacionados.
4. Walk-Forward Matrix y comprobación de rachas perdedoras máximas frente a tu tolerancia.

---

## Range

**Trading de rango (reversión a la media en régimen lateral)** · timeframe `H1`

**Archivos del kit** (todos *no validados en SQX*; tabla completa de cambios en `docs/cambios/`):

| Rol | BUY | SELL |
|---|---|---|
| EB | [`Estrategia_Build_ConfigInicial_H1_BUY__Range_H1_BUY.cfx`](cambios/Estrategia_Build_ConfigInicial_H1_BUY__Range_H1_BUY.md) | [`Estrategia_Build_ConfigInicial_H1_BUY__Range_H1_SELL.cfx`](cambios/Estrategia_Build_ConfigInicial_H1_BUY__Range_H1_SELL.md) |
| ER | [`Estrategia_Retest_ConfigInicial_H1_BUY__Range_H1_BUY.cfx`](cambios/Estrategia_Retest_ConfigInicial_H1_BUY__Range_H1_BUY.md) | [`Estrategia_Retest_ConfigInicial_H1_BUY__Range_H1_SELL.cfx`](cambios/Estrategia_Retest_ConfigInicial_H1_BUY__Range_H1_SELL.md) |
| VB | [`Ventaja_Build_ConfigInicial_H1_BUY__Range_H1_BUY.cfx`](cambios/Ventaja_Build_ConfigInicial_H1_BUY__Range_H1_BUY.md) | [`Ventaja_Build_ConfigInicial_H1_BUY__Range_H1_SELL.cfx`](cambios/Ventaja_Build_ConfigInicial_H1_BUY__Range_H1_SELL.md) |
| VR | [`Ventaja_Retest_ConfigInicial_H1_BUY__Range_H1_BUY.cfx`](cambios/Ventaja_Retest_ConfigInicial_H1_BUY__Range_H1_BUY.md) | [`Ventaja_Retest_ConfigInicial_H1_BUY__Range_H1_SELL.cfx`](cambios/Ventaja_Retest_ConfigInicial_H1_BUY__Range_H1_SELL.md) |

**Operaciones mínimas exigidas** (60/año): Builder IS ≥ 320, OOS 2019-2020 ≥ 100 (≈420 en 7.3 años de construcción); Retest periodo completo ≥ 580 y holdout 2021-2024 ≥ 170.

### 1. Tesis

Cuando la tendencia es débil (ADX bajo, eficiencia de Kaufman baja) los excesos respecto a la media se corrigen: se compra el exceso bajista (o se vende el alcista en SELL) y se sale en la media con objetivo corto.

### 2. Cambios respecto al original

#### 2.a Builder de estrategia completa (`Estrategia_Build`)

| Parámetro | Original | Nuevo | Justificación |
|---|---|---|---|
| Timeframe | H1 | H1 | Sin cambio. |
| Periodo de datos | 2013.09.30 – 2020.12.31 | 2013.09.30 – 2020.12.31 | Sin cambio. |
| Tramo OOS | sin OOS | 2019.01.01 – 2020.12.31 | Validación dentro del Builder: el original filtraba sólo sobre IS. |
| Deslizamiento (pips) | 0 | 0.3 | El original usa 0. |
| Modo de generación | template (plantilla externa .sqx) | simple | El original dependía de una plantilla .sqx no incluida; en modo simple el archivo es autónomo (docs/04 §A.3 para volver a plantilla). |
| Condiciones de entrada | 0–0 | 1–3 | Nivel + 1-2 filtros como máximo; más condiciones = más grados de libertad. |
| Periodos de indicadores | 4–200 | 5–60 | 5-60 velas H1: la reversión a la media es un fenómeno de corto plazo. |
| Desplazamiento (shift) | 1–1 | 1–1 | Sin cambio. |
| Tipos de salida (mín–máx) | 1–5 | 2–4 | SL obligatorio + salidas propias del estilo (el original pedía hasta 5 con 3 disponibles). |
| Tipos de orden | EnterAtMarket (w1) | EnterAtMarket (w1), EnterAtLimit (w3, válida 1-5 velas) | Límite bajo la banda/mínimo (sobre la banda/máximo en SELL): se opera el exceso, no la ruptura. |
| Stop loss | obligatorio=true; 1-3 × ATR(20-100) | obligatorio=true; 1.5-3 × ATR(14-60) | Objetivo corto obligatorio (PT 40-120 % del SL) y alta tasa de acierto; salida temporal: si no revierte en 5-30 h la tesis falló. |
| Profit target | obligatorio=true; 2-5 × ATR(20-100); PT=100-500 % del SL | obligatorio=true; 0.8-2 × ATR(14-60); PT=40-120 % del SL | Objetivo corto obligatorio (PT 40-120 % del SL) y alta tasa de acierto; salida temporal: si no revierte en 5-30 h la tesis falló. |
| Trailing stop | sí (50 %), fijo 50-100 pips, 1-5 ATR | no | Objetivo corto obligatorio (PT 40-120 % del SL) y alta tasa de acierto; salida temporal: si no revierte en 5-30 h la tesis falló. |
| Break-even | no | no | Sin cambio. |
| Salida temporal | no | sí (50 %), 5-30 velas | Objetivo corto obligatorio (PT 40-120 % del SL) y alta tasa de acierto; salida temporal: si no revierte en 5-30 h la tesis falló. |
| Salida por regla | no | sí (50 %) | Objetivo corto obligatorio (PT 40-120 % del SL) y alta tasa de acierto; salida temporal: si no revierte en 5-30 h la tesis falló. |
| Ventana de señales | 01:30-23:30 | 01:30-09:30 | Sesión asiática: menor deriva direccional en FX. |
| Cierres forzados | no diario; no viernes | no diario; no viernes | Sin cambio. |
| Máx. operaciones/día | 0 (sin límite) | 2 | Evita promediar en tendencia. |
| Distancia máx. orden | no | 1 % | 1 %. |
| Bloques activos | 146 señales / 29 indicadores / 29 stop-limit | 47 señales / 48 indicadores / 36 stop-limit | Núcleo: reentrada en bandas tras exceso, osciladores restringidos a sobreventa (sobrecompra en SELL) y filtros de régimen lateral; órdenes límite en la banda/extremo. Los rangos 0-100 originales permitían 'comprar en sobrecompra'. |
| Gestión monetaria | FixedAmount: riesgo 100 por operación | FixedAmount: riesgo 75 por operación | Riesgo fijo 0.75 % (no compuesto: Ret/DD comparable en el tiempo). |
| Fitness | type="ReturnDDRatio" | Weighted: ProfitFactor (peso 1, max), ReturnDDRatio (peso 2, max) | PF alto es imprescindible en reversión (pérdidas medias > ganancias medias). |
| Filtros (Ranking) | AvgBarsInTrade(IS) >= 2; ReturnDDRatio(IS) >= 8; NumberOfTrades(IS) >= 300; WinningPct(IS) >= 40 | NumberOfTrades(IS) >= 320; ReturnDDRatio(IS) >= 4; WinningPct(IS) >= 55; ProfitFactor(IS) >= 1.25; AvgBarsInTrade(IS) >= 2; NetProfit(OOS) > 0; NumberOfTrades(OOS) >= 100 | Umbrales del estilo + exigencia OOS. |
| Filtro población inicial | ReturnDDRatio(IS) >= 5; AvgBarsInTrade(IS) >= 2; NumberOfTrades(IS) >= 250; WinningPct(IS) >= 35 | NumberOfTrades(IS) >= 100 | Sólo nº mínimo de operaciones (recomendación de SQX): con filtros de rentabilidad la población inicial puede tardar horas/días y el Builder no guarda nada mientras tanto. |
| Motor genético | población 5 × 5 islas, 10 generaciones, cruce 46 %, mutación 35 %, migración 6 % cada 5, reinicio por estancamiento a 30 | población 25 × 4 islas, 30 generaciones, cruce 80 %, mutación 30 %, migración 10 % cada 10, reinicio por estancamiento a 15 | 80-100 individuos por generación (el original 25-75) y 30 generaciones (el original 10, insuficiente para que la evolución actúe). |
| Calibración de indicadores | false | true | Recalibra los rangos de valores de indicadores y de rangos stop/limit (±5000 por defecto) para el símbolo y timeframe antes de construir. |

#### 2.b Builder de test de ventaja (`Ventaja_Build`)

| Parámetro | Original | Nuevo | Justificación |
|---|---|---|---|
| Timeframe | H1 | H1 | Sin cambio. |
| Periodo de datos | 2013.09.30 – 2020.12.31 | 2013.09.30 – 2020.12.31 | Sin cambio. |
| Tramo OOS | sin OOS | 2019.01.01 – 2020.12.31 | Validación dentro del Builder: el original filtraba sólo sobre IS. |
| Deslizamiento (pips) | 0 | 0.3 | El original usa 0. |
| Modo de generación | simple | simple | Sin cambio. |
| Condiciones de entrada | 1–3 | 1–3 | Sin cambio. |
| Periodos de indicadores | 4–200 | 5–60 | 5-60 velas H1: la reversión a la media es un fenómeno de corto plazo. |
| Desplazamiento (shift) | 1–1 | 1–1 | Sin cambio. |
| Tipos de salida (mín–máx) | 1–5 | 1–1 | Sólo la salida temporal (test de ventaja). |
| Tipos de orden | EnterAtMarket (w1) | EnterAtMarket (w1), EnterAtLimit (w3, válida 1-5 velas) | Límite bajo la banda/mínimo (sobre la banda/máximo en SELL): se opera el exceso, no la ruptura. |
| Stop loss | obligatorio=false; sin ATR | obligatorio=false; sin ATR | Sin cambio. |
| Profit target | obligatorio=false; sin ATR | obligatorio=false; sin ATR | Sin cambio. |
| Trailing stop | no | no | Sin cambio. |
| Break-even | no | no | Sin cambio. |
| Salida temporal | sí (50 %), 2-15 velas | sí (100 %), 3-24 velas | Test de ventaja: salida por tiempo 3-24 h. |
| Salida por regla | no | no | Sin cambio. |
| Ventana de señales | 01:30-23:30 | 01:30-09:30 | Sesión asiática: menor deriva direccional en FX. |
| Cierres forzados | no diario; no viernes | no diario; no viernes | Sin cambio. |
| Máx. operaciones/día | 0 (sin límite) | 2 | Evita promediar en tendencia. |
| Distancia máx. orden | no | 1 % | 1 %. |
| Bloques activos | 146 señales / 29 indicadores / 29 stop-limit | 47 señales / 48 indicadores / 36 stop-limit | Núcleo: reentrada en bandas tras exceso, osciladores restringidos a sobreventa (sobrecompra en SELL) y filtros de régimen lateral; órdenes límite en la banda/extremo. Los rangos 0-100 originales permitían 'comprar en sobrecompra'. |
| Gestión monetaria | FixedSize: 1 lote | FixedSize: 1 lote | Sin cambio. |
| Fitness | Weighted: Stagnation (peso 1, min) | Weighted: SQN (peso 2, max), StagnationPct (peso 1, min) | SQN mide la calidad estadística de la entrada; el original optimizaba sólo 'Stagnation', que ignora el beneficio. |
| Filtros (Ranking) | AvgBarsInTrade(IS) >= 2; ReturnDDRatio(IS) >= 4; NumberOfTrades(IS) >= 300; WinningPct(IS) >= 40 | NumberOfTrades(IS) >= 320; ReturnDDRatio(IS) >= 2; WinningPct(IS) >= 50; ProfitFactor(IS) >= 1.15; AvgBarsInTrade(IS) >= 2; NetProfit(OOS) > 0; NumberOfTrades(OOS) >= 100 | Umbrales del estilo + exigencia OOS. Test de ventaja: Ret/DD a la mitad y PF ≥1,15. |
| Filtro población inicial | ReturnDDRatio(IS) >= 2; AvgBarsInTrade(IS) >= 2; NumberOfTrades(IS) >= 250; WinningPct(IS) >= 35 | NumberOfTrades(IS) >= 100 | Sólo nº mínimo de operaciones (recomendación de SQX): con filtros de rentabilidad la población inicial puede tardar horas/días y el Builder no guarda nada mientras tanto. |
| Motor genético | población 15 × 5 islas, 10 generaciones, cruce 46 %, mutación 35 %, migración 6 % cada 5, reinicio por estancamiento a 30 | población 25 × 4 islas, 30 generaciones, cruce 80 %, mutación 30 %, migración 10 % cada 10, reinicio por estancamiento a 15 | 80-100 individuos por generación (el original 25-75) y 30 generaciones (el original 10, insuficiente para que la evolución actúe). |
| Calibración de indicadores | false | true | Recalibra los rangos de valores de indicadores y de rangos stop/limit (±5000 por defecto) para el símbolo y timeframe antes de construir. |

#### 2.c Retesters (`Estrategia_Retest` / `Ventaja_Retest`)

| Parámetro | Original | Nuevo | Justificación |
|---|---|---|---|
| Timeframe | H1 | H1 | Sin cambio. |
| Periodo / OOS | 2013.09.30 – 2024.07.22; OOS 2021.01.01 – 2024.07.22 | 2013.09.30 – 2024.07.22; OOS 2021.01.01 – 2024.07.22 | Sin cambio. |
| Deslizamiento | 0 | 0.3 | El original usa 0. |
| Ventana de señales | 01:30-23:30 | 01:30-09:30 | Idéntica al Builder: si difiere, el Retest no reproduce lo construido. |
| Cierres forzados | no diario; no viernes | no diario; no viernes | Sin cambio. |
| Gestión monetaria | FixedAmount: riesgo 100 por operación | FixedAmount: riesgo 75 por operación | Igual que el Builder correspondiente. |
| Fitness | type="ReturnDDRatio" | Weighted: ProfitFactor (peso 1, max), ReturnDDRatio (peso 2, max) | Igual que el Builder correspondiente. |
| Filtros (Ranking) | (ninguna activa) | NetProfit(OOS) > 0; ProfitFactor(OOS) >= 1.1; ReturnDDRatio(Full) >= 6; NumberOfTrades(Full) >= 580; NumberOfTrades(OOS) >= 170; DrawdownPct(Full) <= 20 | El original no filtraba nada (todas use=false) ni borraba fallidas. |
| Mayor precisión | activo; precisión 2 (tick real + spread personalizado); 1 condiciones | activo; precisión 2 (tick real + spread personalizado); 3 condiciones | Se activan también las condiciones de nº de operaciones y DD. |
| Monte Carlo retest | activo; 1000 sims; OHLC ±10 % ATR(14), spread 1-3. Acepta: NetProfit(IS) >= 0 | activo; 500 sims; OHLC ±10 % ATR(14), desliz. 0-0.5, spread 2-4. Acepta: NetProfit(Full) >= 0; DrawdownPct(Full) <= 150% de DrawdownPct[main] | Spread desde el base hasta 2-4x, deslizamiento, percentil 95 (no el peor caso) y control del DD. |
| Monte Carlo manipulación | no; orden de operaciones 'exact', saltar 10 % | activo; orden de operaciones 'resampling', saltar 10 % | Barato; 'resampling' y referencia corregida (el original comparaba MC contra MC). |
| SPP / perfil de optimización | activo; 15000 tests, ±20 %, 6 pasos; ≥95 % rentables | activo; 5000 tests, ±20 %, 6 pasos; ≥85 % rentables | Tests y exigencia ajustados al coste de cómputo y a la sensibilidad del estilo. |
| What-if | no; ExcludePctTradesWithBiggestPl, ExcludePctTradesWithLowestPl | activo; ExcludePctTradesWithBiggestPl, ExcludePctTradesWithLowestPl | Quitar el 5 % de extremos: el estilo no debe depender de outliers. |

Diferencias del `Ventaja_Retest` respecto al anterior:

- **Gestión monetaria:** FixedSize: 1 lote
- **Fitness:** Weighted: SQN (peso 2, max), StagnationPct (peso 1, min)
- **Filtros (Ranking):** NetProfit(OOS) > 0; ProfitFactor(Full) >= 1.1; NumberOfTrades(Full) >= 580; NumberOfTrades(OOS) >= 170

### 3. Indicadores y bloques seleccionados

Criterio general: Núcleo: reentrada en bandas tras exceso, osciladores restringidos a sobreventa (sobrecompra en SELL) y filtros de régimen lateral; órdenes límite en la banda/extremo. Los rangos 0-100 originales permitían 'comprar en sobrecompra'.

Recuento: **47 señales, 48 indicadores y 36 niveles/rangos stop-limit** (el original: 146 / 29 / 29, todos con peso 1 y sin relación con la tesis). Las familias con peso ≥ 2 son el núcleo del estilo; las de peso 1 son filtros auxiliares que amplían la variedad de estrategias sin cambiar la tesis. Se excluyen siempre los bloques con niveles absolutos dependientes del precio. La columna SELL muestra el bloque espejo que se activa en el kit de ventas.

#### Señales

| Familia (peso) | Qué mide | Por qué en este estilo | Bloques BUY | Espejo SELL |
|---|---|---|---|---|
| rev_bandas (6) | Exceso fuera de la banda inferior y reentrada (reversión a la media). | Núcleo: exceso fuera de banda y reentrada. | `BBBarOpensAboveDownAfterOpenBelow`, `BBBarClosesBelowDown`, `BBBarOpensBelowDown`, `BBBarClosesAboveDown`, `KCBarOpensAboveLowerAfterOpenBelow`, `KCBarClosesBelowLower`, `KCBarOpensBelowLower`, `KCBarClosesAboveLower` | `BBBarOpensBelowUpAfterOpenAbove`, `BBBarClosesAboveUp`, `BBBarOpensAboveUp`, `BBBarClosesBelowUp`, `KCBarOpensBelowUpperAfterOpenAbove`, `KCBarClosesAboveUpper`, `KCBarOpensAboveUpper`, `KCBarClosesBelowUpper` |
| sobreventa (3) | Osciladores en zona de sobreventa (RSI 15-40, estocástico 10-30, WPR -95…-75, CCI -200…-80…). | Identificar el exceso que se espera que revierta. | `RSICrossUp`, `RSILower`, `StochSlowDCrossUp`, `StochFastKCrossUp`, `StochSlowDLower`, `WPRCrossUp`, `WPRLower`, `CCICrossUp`, `CCILower`, `LaguerreRSICrossUP`, `DEMCrossUp`, `DEMLower`, `QQEValue1CrossAbove`, `QQEValue1Lower`, `SchaffTrendCycleCrossesAboveLevel`, `SchaffTrendCycleBelowLevel` | `RSICrossDown`, `RSIHigher`, `StochSlowDCrossDown`, `StochFastKCrossDown`, `StochSlowDHigher`, `WPRCrossDown`, `WPRHigher`, `CCICrossDown`, `CCIHigher`, `LaguerreRSICrossDown`, `DEMCrossDown`, `DEMHigher`, `QQEValue1CrossBelow`, `QQEValue1Higher`, `SchaffTrendCycleCrossesBelowLevel`, `SchaffTrendCycleAboveLevel` |
| lateral (4) | ADX bajo/decreciente, eficiencia de Kaufman baja, SuperTrend en rango: no hay tendencia. | Imprescindible: la reversión sólo funciona sin tendencia. | `ADXLower`, `ADXFalling`, `ADXChangesDown`, `ADXCrossDown`, `KERbelowLevel`, `SuperTrendInRange` | igual (neutral) |
| falsa_ruptura (3) | Recuperación por encima del mínimo de N velas tras perforarlo (trampa bajista). | Recuperación tras perforar el extremo del rango. | `BarOpensAboveLowestAfterOpenBelow` | `BarOpensBelowHighestAfterOpenAbove` |
| vol_contraccion (1) | ATR/desviación típica/bandas cerrándose: compresión previa a un movimiento. | Filtro auxiliar: amplía la variedad. | `ATRFalling`, `ATRChangesDown`, `StdDevFalling`, `StdDevChangesDown`, `BBUpperFalling`, `BBLowerRising`, `KCUpperFalling`, `KCLowerRising` | igual (neutral) |
| velas (1) | Patrones de vela de giro alcista (envolvente, martillo, pauta penetrante, doji) y fractal. | Filtro auxiliar: amplía la variedad. | `BullishEngulfing`, `Hammer`, `PiercingLine`, `Doji`, `IsBullishFractal` | `BearishEngulfing`, `ShootingStar`, `DarkCloud`, `Doji`, `IsBearishFractal` |
| tiempo_intradia (1) | Franja horaria (hora mayor/menor que) y excluir un día de la semana. | Filtro auxiliar: amplía la variedad. | `BarHourIsBigger`, `BarHourIsSmaller`, `BarDayOfWeekIsNot` | igual (neutral) |

#### Indicadores

| Familia (peso) | Qué mide | Por qué en este estilo | Bloques BUY | Espejo SELL |
|---|---|---|---|---|
| bandas (3) | Bandas de Bollinger y canal de Keltner. | Bandas que delimitan el rango. | `BollingerBands`, `KeltnerChannel` | igual (neutral) |
| medias (2) | Medias móviles (SMA, EMA, LWMA, SMMA, TEMA, Hull, KAMA) y regresión lineal. | Centro del rango (objetivo/regla de salida). | `SMA`, `EMA`, `LWMA`, `SMMA`, `TEMA`, `HullMovingAverage`, `KAMA`, `LinearRegression` | igual (neutral) |
| niv_canal (2) | Máximo/mínimo de N velas. | Extremos del rango. | `Highest`, `Lowest` | `Lowest`, `Highest` |
| niv_horario (1) | Máximo/mínimo de un rango horario y de la sesión (apertura/cierre de sesión). | Filtro auxiliar: amplía la variedad. | `HighestInRange`, `LowestInRange`, `SessionHigh`, `SessionLow`, `SessionOpen`, `SessionClose` | `LowestInRange`, `HighestInRange`, `SessionLow`, `SessionHigh`, `SessionOpen`, `SessionClose` |
| niv_diario (1) | Máximo/mínimo/apertura/cierre del día. | Filtro auxiliar: amplía la variedad. | `HighD`, `LowD`, `OpenD`, `CloseD` | `LowD`, `HighD`, `OpenD`, `CloseD` |
| precio (1) | Apertura, máximo, mínimo y cierre de la vela. | Filtro auxiliar: amplía la variedad. | `Close`, `Open`, `High`, `Low` | `Close`, `Open`, `Low`, `High` |
| osciladores (2) | RSI, estocástico, CCI, Williams %R, RSI de Laguerre y DeMarker como valores. | Valores de osciladores para comparar. | `RSI`, `Stochastic`, `CCI`, `WilliamsPR`, `LaguerreRSI`, `DeMarker` | igual (neutral) |
| fuerza_ind (1) | ADX, eficiencia de Kaufman, Aroon y Vortex como valores. | Filtro auxiliar: amplía la variedad. | `ADX`, `KaufmanEfficiencyRatio`, `Aroon`, `Vortex` | igual (neutral) |
| volat_ind (1) | ATR y rango verdadero (para comparaciones relativas). | Filtro auxiliar: amplía la variedad. | `ATR`, `TrueRange` | igual (neutral) |
| comparadores (1) | Mayor/menor, mayor o igual, cruces. | Filtro auxiliar: amplía la variedad. | `IsGreater`, `IsLower`, `IsGreaterOrEqual`, `IsLowerOrEqual`, `CrossesAbove`, `CrossesBelow` | `IsLower`, `IsGreater`, `IsLowerOrEqual`, `IsGreaterOrEqual`, `CrossesBelow`, `CrossesAbove` |
| secuencias (2) | N velas seguidas por encima/debajo, subiendo/bajando. | Agotamiento: N velas seguidas en contra. | `IsGreaterCount`, `IsLowerCount`, `IsRising`, `IsFalling` | `IsLowerCount`, `IsGreaterCount`, `IsFalling`, `IsRising` |

#### Niveles y rangos stop/limit

| Familia (peso) | Qué mide | Por qué en este estilo | Bloques BUY | Espejo SELL |
|---|---|---|---|---|
| stl_bandas (5) | Orden en Bollinger/Keltner. | Orden límite en la banda: se opera el exceso. | `BollingerBands`, `KeltnerChannel`, `MTKeltnerChannel` | igual (neutral) |
| stl_canal (2) | Orden en el máximo/mínimo de N velas. | Límite en el extremo de N velas. | `Highest`(w1), `Lowest`(w3) | `Lowest`, `Highest` |
| stl_vela (2) | Orden en el máximo/mínimo/apertura/cierre de una vela. | Límite en el extremo de la vela. | `High`(w1), `Low`(w3), `Open`, `Close` | `Low`, `High`, `Open`, `Close` |
| stl_medias (2) | Orden en una media móvil. | Límite en la media. | `SMA`, `EMA`, `LWMA`, `SMMA`, `TEMA`, `HullMovingAverage`, `KAMA`, `LinearRegression` | igual (neutral) |
| stl_diario (1) | Orden en niveles del día. | Filtro auxiliar: amplía la variedad. | `HighD`, `LowD`(w2), `OpenD`, `CloseD` | `LowD`, `HighD`, `OpenD`, `CloseD` |
| stl_horario (1) | Orden en el extremo de un rango horario o de sesión. | Filtro auxiliar: amplía la variedad. | `HighestInRange`, `LowestInRange`(w2), `SessionHigh`, `SessionLow`(w2), `SessionOpen` | `LowestInRange`, `HighestInRange`, `SessionLow`, `SessionHigh`, `SessionOpen` |
| stl_estructura (1) | Orden en fractales o pivotes. | Filtro auxiliar: amplía la variedad. | `Fractal`, `Pivots` | igual (neutral) |
| stl_rangos (2) | Desplazamiento de la orden: k·ATR, rango de vela, rango verdadero, mayor/menor rango, anchura de Bollinger. | Distancia de la orden límite. | `ATR`, `MTATR`, `BarRange`, `TrueRange`, `BiggestRange`, `SmallestRange`, `BBRange`, `BBWidthRatio` | igual (neutral) |

#### Rangos específicos (BUY → SELL)

| Bloque BUY | Rango BUY | Bloque SELL | Rango SELL |
|---|---|---|---|
| `RSICrossUp` | Level 15 a 40 (paso 5) | `RSICrossDown` | Level 60 a 85 (paso 5) |
| `RSILower` | Level 20 a 40 (paso 5) | `RSIHigher` | Level 60 a 80 (paso 5) |
| `StochSlowDCrossUp` | Level 10 a 30 (paso 5) | `StochSlowDCrossDown` | Level 70 a 90 (paso 5) |
| `StochFastKCrossUp` | Level 10 a 30 (paso 5) | `StochFastKCrossDown` | Level 70 a 90 (paso 5) |
| `StochSlowDLower` | Level 10 a 30 (paso 5) | `StochSlowDHigher` | Level 70 a 90 (paso 5) |
| `WPRCrossUp` | Level -95 a -75 (paso 5) | `WPRCrossDown` | Level -25 a -5 (paso 5) |
| `WPRLower` | Level -95 a -75 (paso 5) | `WPRHigher` | Level -25 a -5 (paso 5) |
| `CCICrossUp` | Level -200 a -80 (paso 10) | `CCICrossDown` | Level 80 a 200 (paso 10) |
| `CCILower` | Level -200 a -80 (paso 10) | `CCIHigher` | Level 80 a 200 (paso 10) |
| `LaguerreRSICrossUP` | Gamma 0.3 a 0.8 (paso 0.05); Level 0.05 a 0.3 (paso 0.05) | `LaguerreRSICrossDown` | Gamma 0.3 a 0.8 (paso 0.05); Level 0.7 a 0.95 (paso 0.05) |
| `DEMCrossUp` | Level 0.1 a 0.3 (paso 0.05) | `DEMCrossDown` | Level 0.7 a 0.9 (paso 0.05) |
| `DEMLower` | Level 0.1 a 0.3 (paso 0.05) | `DEMHigher` | Level 0.7 a 0.9 (paso 0.05) |
| `QQEValue1CrossAbove` | Level 20 a 40 (paso 5) | `QQEValue1CrossBelow` | Level 60 a 80 (paso 5) |
| `QQEValue1Lower` | Level 20 a 40 (paso 5) | `QQEValue1Higher` | Level 60 a 80 (paso 5) |
| `SchaffTrendCycleCrossesAboveLevel` | Level 5 a 25 (paso 5) | `SchaffTrendCycleCrossesBelowLevel` | Level 75 a 95 (paso 5) |
| `SchaffTrendCycleBelowLevel` | Level 5 a 25 (paso 5) | `SchaffTrendCycleAboveLevel` | Level 75 a 95 (paso 5) |
| `ADXLower` | Level 15 a 30 (paso 5) | `ADXLower` | Level 15 a 30 (paso 5) |
| `ADXCrossDown` | Level 20 a 30 (paso 5) | `ADXCrossDown` | Level 20 a 30 (paso 5) |
| `KERbelowLevel` | Level 0.1 a 0.4 (paso 0.05) | `KERbelowLevel` | Level 0.1 a 0.4 (paso 0.05) |
| `SuperTrendInRange` | ATR Mult 1.5 a 5 (paso 0.5) | `SuperTrendInRange` | ATR Mult 1.5 a 5 (paso 0.5) |
| `Indicators.HighestInRange` | Time From 0 a 300 (paso 100); Time To 700 a 1000 (paso 100) | `Indicators.LowestInRange` | Time From 0 a 300 (paso 100); Time To 700 a 1000 (paso 100) |
| `Stop/Limit Price Levels.HighestInRange` | Time From 0 a 300 (paso 100); Time To 700 a 1000 (paso 100) | `Stop/Limit Price Levels.LowestInRange` | Time From 0 a 300 (paso 100); Time To 700 a 1000 (paso 100) |
| `Prices.SessionHigh` | Start Hours 1 a 3 (paso 1); Start Minutes 0 a 0 (paso 1); End Hours 8 a 10 (paso 1); End Minutes 0 a 0 (paso 1) | `Prices.SessionLow` | Start Hours 1 a 3 (paso 1); Start Minutes 0 a 0 (paso 1); End Hours 8 a 10 (paso 1); End Minutes 0 a 0 (paso 1) |
| `Stop/Limit Price Levels.SessionHigh` | Start Hours 1 a 3 (paso 1); Start Minutes 0 a 0 (paso 1); End Hours 8 a 10 (paso 1); End Minutes 0 a 0 (paso 1) | `Stop/Limit Price Levels.SessionLow` | Start Hours 1 a 3 (paso 1); Start Minutes 0 a 0 (paso 1); End Hours 8 a 10 (paso 1); End Minutes 0 a 0 (paso 1) |
| `Prices.SessionOpen` | Start Hours 1 a 3 (paso 1); Start Minutes 0 a 0 (paso 1) | `Prices.SessionOpen` | Start Hours 1 a 3 (paso 1); Start Minutes 0 a 0 (paso 1) |
| `Stop/Limit Price Levels.SessionOpen` | Start Hours 1 a 3 (paso 1); Start Minutes 0 a 0 (paso 1) | `Stop/Limit Price Levels.SessionOpen` | Start Hours 1 a 3 (paso 1); Start Minutes 0 a 0 (paso 1) |
| `Prices.SessionClose` | End Hours 8 a 10 (paso 1); End Minutes 0 a 0 (paso 1) | `Prices.SessionClose` | End Hours 8 a 10 (paso 1); End Minutes 0 a 0 (paso 1) |
| `BarHourIsBigger` | Hour 1 a 4 (paso 1) | `BarHourIsBigger` | Hour 1 a 4 (paso 1) |
| `BarHourIsSmaller` | Hour 5 a 10 (paso 1) | `BarHourIsSmaller` | Hour 5 a 10 (paso 1) |

### 4. Timeframe, símbolos y horarios

- **Timeframe:** H1.
- **Instrumento recomendado:** EURCHF, EURGBP, AUDNZD, USDCAD en sesión asiática o índices en rango. GBPJPY es tendencial y mal candidato: usar sólo como prueba.
- **Horario:** Entradas 01:30-09:30 servidor (sesión asiática, menor deriva direccional en FX). Fuera de esa franja no se abren operaciones nuevas.

### 5. Salidas y gestión del riesgo

SL 1,5-3 ATR(14-60) obligatorio; objetivo 0,8-2 ATR obligatorio con PT = 40-120 % del SL; salida temporal 5-30 h (50 %) y salida por regla (50 %); sin trailing. Acierto ≥55 %. Riesgo 0,75 %; máximo 2 entradas/día.

### 6. Filtros y ranking

| Archivo | Fitness | Filtros |
|---|---|---|
| `Estrategia_Build_ConfigInicial_H1_BUY__Range_H1_BUY` | Weighted: ProfitFactor (peso 1, max), ReturnDDRatio (peso 2, max) | NumberOfTrades(IS) >= 320; ReturnDDRatio(IS) >= 4; WinningPct(IS) >= 55; ProfitFactor(IS) >= 1.25; AvgBarsInTrade(IS) >= 2; NetProfit(OOS) > 0; NumberOfTrades(OOS) >= 100 |
| `Estrategia_Retest_ConfigInicial_H1_BUY__Range_H1_BUY` | Weighted: ProfitFactor (peso 1, max), ReturnDDRatio (peso 2, max) | NetProfit(OOS) > 0; ProfitFactor(OOS) >= 1.1; ReturnDDRatio(Full) >= 6; NumberOfTrades(Full) >= 580; NumberOfTrades(OOS) >= 170; DrawdownPct(Full) <= 20 |
| `Ventaja_Build_ConfigInicial_H1_BUY__Range_H1_BUY` | Weighted: SQN (peso 2, max), StagnationPct (peso 1, min) | NumberOfTrades(IS) >= 320; ReturnDDRatio(IS) >= 2; WinningPct(IS) >= 50; ProfitFactor(IS) >= 1.15; AvgBarsInTrade(IS) >= 2; NetProfit(OOS) > 0; NumberOfTrades(OOS) >= 100 |
| `Ventaja_Retest_ConfigInicial_H1_BUY__Range_H1_BUY` | Weighted: SQN (peso 2, max), StagnationPct (peso 1, min) | NetProfit(OOS) > 0; ProfitFactor(Full) >= 1.1; NumberOfTrades(Full) >= 580; NumberOfTrades(OOS) >= 170 |

Justificación: PF alto es imprescindible en reversión (pérdidas medias > ganancias medias). El mínimo de operaciones sale de la densidad del estilo (60/año) multiplicada por los años de cada tramo; el acierto y el Ret/DD se adaptan al estilo. Los archivos SELL usan exactamente los mismos filtros.

### 7. Motor y robustez

- **Builder:** población 25 × 4 islas, 30 generaciones, cruce 80 %, mutación 30 %, migración 10 % cada 10, reinicio por estancamiento a 15.
- **Retest:** activo; precisión 2 (tick real + spread personalizado); 3 condiciones. What-if excluye el 5 % de mejores y peores: una reversión sana no depende de outliers.
- **Monte Carlo:** activo; 500 sims; OHLC ±10 % ATR(14), desliz. 0-0.5, spread 2-4. Acepta: NetProfit(Full) >= 0; DrawdownPct(Full) <= 150% de DrawdownPct[main].
- **Manipulación MC:** activo; orden de operaciones 'resampling', saltar 10 %.
- **SPP:** activo; 5000 tests, ±20 %, 6 pasos; ≥85 % rentables.
- **What-if:** activo; ExcludePctTradesWithBiggestPl, ExcludePctTradesWithLowestPl.

### 8. Riesgos conocidos, sobreoptimización y mitigación

Riesgos propios del estilo: Pérdida grande cuando el rango se rompe (cola izquierda); el SL es imprescindible.

1. Cola izquierda: cuando el rango se rompe, una pérdida borra muchas ganancias. SL obligatorio y what-if excluyendo el 5 % de extremos.
2. Cambio de régimen (un par lateral durante años puede entrar en tendencia): análisis año a año.
3. Umbrales de osciladores y de ADX/KER: rangos acotados + SPP.

### 9. Plan de validación

1. `Ventaja_Build…Range_H1` (salida 3-24 h) → `Ventaja_Retest…`.
2. `Estrategia_Build…` → `Estrategia_Retest…Range_H1`.
3. Cambiar el símbolo a un par de rango (EURCHF, EURGBP, AUDNZD) y repetir: GBPJPY es mal candidato.
4. Revisar periodos de ruptura de régimen conocidos (p. ej. enero 2015 en EURCHF).

---

## PriceAction

**Acción del precio (patrones de vela en niveles)** · timeframe `H1`

**Archivos del kit** (todos *no validados en SQX*; tabla completa de cambios en `docs/cambios/`):

| Rol | BUY | SELL |
|---|---|---|
| EB | [`Estrategia_Build_ConfigInicial_H1_BUY__PriceAction_H1_BUY.cfx`](cambios/Estrategia_Build_ConfigInicial_H1_BUY__PriceAction_H1_BUY.md) | [`Estrategia_Build_ConfigInicial_H1_BUY__PriceAction_H1_SELL.cfx`](cambios/Estrategia_Build_ConfigInicial_H1_BUY__PriceAction_H1_SELL.md) |
| ER | [`Estrategia_Retest_ConfigInicial_H1_BUY__PriceAction_H1_BUY.cfx`](cambios/Estrategia_Retest_ConfigInicial_H1_BUY__PriceAction_H1_BUY.md) | [`Estrategia_Retest_ConfigInicial_H1_BUY__PriceAction_H1_SELL.cfx`](cambios/Estrategia_Retest_ConfigInicial_H1_BUY__PriceAction_H1_SELL.md) |
| VB | [`Ventaja_Build_ConfigInicial_H1_BUY__PriceAction_H1_BUY.cfx`](cambios/Ventaja_Build_ConfigInicial_H1_BUY__PriceAction_H1_BUY.md) | [`Ventaja_Build_ConfigInicial_H1_BUY__PriceAction_H1_SELL.cfx`](cambios/Ventaja_Build_ConfigInicial_H1_BUY__PriceAction_H1_SELL.md) |
| VR | [`Ventaja_Retest_ConfigInicial_H1_BUY__PriceAction_H1_BUY.cfx`](cambios/Ventaja_Retest_ConfigInicial_H1_BUY__PriceAction_H1_BUY.md) | [`Ventaja_Retest_ConfigInicial_H1_BUY__PriceAction_H1_SELL.cfx`](cambios/Ventaja_Retest_ConfigInicial_H1_BUY__PriceAction_H1_SELL.md) |

**Operaciones mínimas exigidas** (60/año): Builder IS ≥ 320, OOS 2019-2020 ≥ 100 (≈420 en 7.3 años de construcción); Retest periodo completo ≥ 580 y holdout 2021-2024 ≥ 170.

### 1. Tesis

Patrones de rechazo/absorción (envolvente, martillo, pauta penetrante, fractal y sus equivalentes bajistas en SELL) en niveles relevantes señalan desequilibrios de órdenes; se entra con stop sobre el extremo de la vela señal.

### 2. Cambios respecto al original

#### 2.a Builder de estrategia completa (`Estrategia_Build`)

| Parámetro | Original | Nuevo | Justificación |
|---|---|---|---|
| Timeframe | H1 | H1 | Sin cambio. |
| Periodo de datos | 2013.09.30 – 2020.12.31 | 2013.09.30 – 2020.12.31 | Sin cambio. |
| Tramo OOS | sin OOS | 2019.01.01 – 2020.12.31 | Validación dentro del Builder: el original filtraba sólo sobre IS. |
| Deslizamiento (pips) | 0 | 0.3 | El original usa 0. |
| Modo de generación | template (plantilla externa .sqx) | simple | El original dependía de una plantilla .sqx no incluida; en modo simple el archivo es autónomo (docs/04 §A.3 para volver a plantilla). |
| Condiciones de entrada | 0–0 | 1–3 | Nivel + 1-2 filtros como máximo; más condiciones = más grados de libertad. |
| Periodos de indicadores | 4–200 | 2–50 | Periodos 2-50 (estructura reciente); desplazamiento 1-3 para patrones de 2-3 velas. |
| Desplazamiento (shift) | 1–1 | 1–3 | Patrones de 2-3 velas. |
| Tipos de salida (mín–máx) | 1–5 | 2–4 | SL obligatorio + salidas propias del estilo (el original pedía hasta 5 con 3 disponibles). |
| Tipos de orden | EnterAtMarket (w1) | EnterAtMarket (w1), EnterAtStop (w3, válida 1-3 velas), EnterAtLimit (w1, válida 1-3 velas) | Stop sobre el extremo de la vela señal (confirmación) o límite en retroceso. |
| Stop loss | obligatorio=true; 1-3 × ATR(20-100) | obligatorio=true; 1-2.5 × ATR(14-50) | R:R 1,5-3 sobre el riesgo de la vela; break-even tras 1-2 ATR. |
| Profit target | obligatorio=true; 2-5 × ATR(20-100); PT=100-500 % del SL | obligatorio=true; 1.5-4 × ATR(14-50); PT=150-300 % del SL | R:R 1,5-3 sobre el riesgo de la vela; break-even tras 1-2 ATR. |
| Trailing stop | sí (50 %), fijo 50-100 pips, 1-5 ATR | no | R:R 1,5-3 sobre el riesgo de la vela; break-even tras 1-2 ATR. |
| Break-even | no | sí (50 %), 1-2 ATR | R:R 1,5-3 sobre el riesgo de la vela; break-even tras 1-2 ATR. |
| Salida temporal | no | sí (30 %), 5-30 velas | R:R 1,5-3 sobre el riesgo de la vela; break-even tras 1-2 ATR. |
| Salida por regla | no | sí (30 %) | R:R 1,5-3 sobre el riesgo de la vela; break-even tras 1-2 ATR. |
| Ventana de señales | 01:30-23:30 | 01:30-23:30 | Sin cambio. |
| Cierres forzados | no diario; no viernes | no diario; no viernes | Sin cambio. |
| Máx. operaciones/día | 0 (sin límite) | 2 | Evita encadenar señales en el mismo nivel. |
| Distancia máx. orden | no | 1 % | 1 %. |
| Bloques activos | 146 señales / 29 indicadores / 29 stop-limit | 33 señales / 37 indicadores / 32 stop-limit | Núcleo: velas de giro y falsas rupturas, precio puro, Heikin-Ashi y estructura (niveles diarios/semanales, fractales); ATR sólo como normalizador. Sin osciladores ni medias. |
| Gestión monetaria | FixedAmount: riesgo 100 por operación | FixedAmount: riesgo 100 por operación | Sin cambio. |
| Fitness | type="ReturnDDRatio" | Weighted: ReturnDDRatio (peso 2, max), SQN (peso 1, max) | Ret/DD + SQN (consistencia por operación). |
| Filtros (Ranking) | AvgBarsInTrade(IS) >= 2; ReturnDDRatio(IS) >= 8; NumberOfTrades(IS) >= 300; WinningPct(IS) >= 40 | NumberOfTrades(IS) >= 320; ReturnDDRatio(IS) >= 4; WinningPct(IS) >= 40; ProfitFactor(IS) >= 1.3; AvgBarsInTrade(IS) >= 2; NetProfit(OOS) > 0; NumberOfTrades(OOS) >= 100 | Umbrales del estilo + exigencia OOS. |
| Filtro población inicial | ReturnDDRatio(IS) >= 5; AvgBarsInTrade(IS) >= 2; NumberOfTrades(IS) >= 250; WinningPct(IS) >= 35 | NumberOfTrades(IS) >= 100 | Sólo nº mínimo de operaciones (recomendación de SQX): con filtros de rentabilidad la población inicial puede tardar horas/días y el Builder no guarda nada mientras tanto. |
| Motor genético | población 5 × 5 islas, 10 generaciones, cruce 46 %, mutación 35 %, migración 6 % cada 5, reinicio por estancamiento a 30 | población 25 × 4 islas, 30 generaciones, cruce 80 %, mutación 30 %, migración 10 % cada 10, reinicio por estancamiento a 15 | 80-100 individuos por generación (el original 25-75) y 30 generaciones (el original 10, insuficiente para que la evolución actúe). |
| Calibración de indicadores | false | true | Recalibra los rangos de valores de indicadores y de rangos stop/limit (±5000 por defecto) para el símbolo y timeframe antes de construir. |

#### 2.b Builder de test de ventaja (`Ventaja_Build`)

| Parámetro | Original | Nuevo | Justificación |
|---|---|---|---|
| Timeframe | H1 | H1 | Sin cambio. |
| Periodo de datos | 2013.09.30 – 2020.12.31 | 2013.09.30 – 2020.12.31 | Sin cambio. |
| Tramo OOS | sin OOS | 2019.01.01 – 2020.12.31 | Validación dentro del Builder: el original filtraba sólo sobre IS. |
| Deslizamiento (pips) | 0 | 0.3 | El original usa 0. |
| Modo de generación | simple | simple | Sin cambio. |
| Condiciones de entrada | 1–3 | 1–3 | Sin cambio. |
| Periodos de indicadores | 4–200 | 2–50 | Periodos 2-50 (estructura reciente); desplazamiento 1-3 para patrones de 2-3 velas. |
| Desplazamiento (shift) | 1–1 | 1–3 | Patrones de 2-3 velas. |
| Tipos de salida (mín–máx) | 1–5 | 1–1 | Sólo la salida temporal (test de ventaja). |
| Tipos de orden | EnterAtMarket (w1) | EnterAtMarket (w1), EnterAtStop (w3, válida 1-3 velas), EnterAtLimit (w1, válida 1-3 velas) | Stop sobre el extremo de la vela señal (confirmación) o límite en retroceso. |
| Stop loss | obligatorio=false; sin ATR | obligatorio=false; sin ATR | Sin cambio. |
| Profit target | obligatorio=false; sin ATR | obligatorio=false; sin ATR | Sin cambio. |
| Trailing stop | no | no | Sin cambio. |
| Break-even | no | no | Sin cambio. |
| Salida temporal | sí (50 %), 2-15 velas | sí (100 %), 3-24 velas | Test de ventaja: salida por tiempo 3-24 h. |
| Salida por regla | no | no | Sin cambio. |
| Ventana de señales | 01:30-23:30 | 01:30-23:30 | Sin cambio. |
| Cierres forzados | no diario; no viernes | no diario; no viernes | Sin cambio. |
| Máx. operaciones/día | 0 (sin límite) | 2 | Evita encadenar señales en el mismo nivel. |
| Distancia máx. orden | no | 1 % | 1 %. |
| Bloques activos | 146 señales / 29 indicadores / 29 stop-limit | 33 señales / 37 indicadores / 32 stop-limit | Núcleo: velas de giro y falsas rupturas, precio puro, Heikin-Ashi y estructura (niveles diarios/semanales, fractales); ATR sólo como normalizador. Sin osciladores ni medias. |
| Gestión monetaria | FixedSize: 1 lote | FixedSize: 1 lote | Sin cambio. |
| Fitness | Weighted: Stagnation (peso 1, min) | Weighted: SQN (peso 2, max), StagnationPct (peso 1, min) | SQN mide la calidad estadística de la entrada; el original optimizaba sólo 'Stagnation', que ignora el beneficio. |
| Filtros (Ranking) | AvgBarsInTrade(IS) >= 2; ReturnDDRatio(IS) >= 4; NumberOfTrades(IS) >= 300; WinningPct(IS) >= 40 | NumberOfTrades(IS) >= 320; ReturnDDRatio(IS) >= 2; WinningPct(IS) >= 35; ProfitFactor(IS) >= 1.15; AvgBarsInTrade(IS) >= 2; NetProfit(OOS) > 0; NumberOfTrades(OOS) >= 100 | Umbrales del estilo + exigencia OOS. Test de ventaja: Ret/DD a la mitad y PF ≥1,15. |
| Filtro población inicial | ReturnDDRatio(IS) >= 2; AvgBarsInTrade(IS) >= 2; NumberOfTrades(IS) >= 250; WinningPct(IS) >= 35 | NumberOfTrades(IS) >= 100 | Sólo nº mínimo de operaciones (recomendación de SQX): con filtros de rentabilidad la población inicial puede tardar horas/días y el Builder no guarda nada mientras tanto. |
| Motor genético | población 15 × 5 islas, 10 generaciones, cruce 46 %, mutación 35 %, migración 6 % cada 5, reinicio por estancamiento a 30 | población 25 × 4 islas, 30 generaciones, cruce 80 %, mutación 30 %, migración 10 % cada 10, reinicio por estancamiento a 15 | 80-100 individuos por generación (el original 25-75) y 30 generaciones (el original 10, insuficiente para que la evolución actúe). |
| Calibración de indicadores | false | true | Recalibra los rangos de valores de indicadores y de rangos stop/limit (±5000 por defecto) para el símbolo y timeframe antes de construir. |

#### 2.c Retesters (`Estrategia_Retest` / `Ventaja_Retest`)

| Parámetro | Original | Nuevo | Justificación |
|---|---|---|---|
| Timeframe | H1 | H1 | Sin cambio. |
| Periodo / OOS | 2013.09.30 – 2024.07.22; OOS 2021.01.01 – 2024.07.22 | 2013.09.30 – 2024.07.22; OOS 2021.01.01 – 2024.07.22 | Sin cambio. |
| Deslizamiento | 0 | 0.3 | El original usa 0. |
| Ventana de señales | 01:30-23:30 | 01:30-23:30 | Sin cambio. |
| Cierres forzados | no diario; no viernes | no diario; no viernes | Sin cambio. |
| Gestión monetaria | FixedAmount: riesgo 100 por operación | FixedAmount: riesgo 100 por operación | Sin cambio. |
| Fitness | type="ReturnDDRatio" | Weighted: ReturnDDRatio (peso 2, max), SQN (peso 1, max) | Igual que el Builder correspondiente. |
| Filtros (Ranking) | (ninguna activa) | NetProfit(OOS) > 0; ProfitFactor(OOS) >= 1.1; ReturnDDRatio(Full) >= 6; NumberOfTrades(Full) >= 580; NumberOfTrades(OOS) >= 170; DrawdownPct(Full) <= 20 | El original no filtraba nada (todas use=false) ni borraba fallidas. |
| Mayor precisión | activo; precisión 2 (tick real + spread personalizado); 1 condiciones | activo; precisión 2 (tick real + spread personalizado); 3 condiciones | Se activan también las condiciones de nº de operaciones y DD. |
| Monte Carlo retest | activo; 1000 sims; OHLC ±10 % ATR(14), spread 1-3. Acepta: NetProfit(IS) >= 0 | activo; 500 sims; OHLC ±10 % ATR(14), desliz. 0-0.5, spread 2-4. Acepta: NetProfit(Full) >= 0; DrawdownPct(Full) <= 150% de DrawdownPct[main] | Spread desde el base hasta 2-4x, deslizamiento, percentil 95 (no el peor caso) y control del DD. |
| Monte Carlo manipulación | no; orden de operaciones 'exact', saltar 10 % | activo; orden de operaciones 'resampling', saltar 10 % | Barato; 'resampling' y referencia corregida (el original comparaba MC contra MC). |
| SPP / perfil de optimización | activo; 15000 tests, ±20 %, 6 pasos; ≥95 % rentables | activo; 5000 tests, ±20 %, 6 pasos; ≥85 % rentables | Tests y exigencia ajustados al coste de cómputo y a la sensibilidad del estilo. |
| What-if | no; ExcludePctTradesWithBiggestPl, ExcludePctTradesWithLowestPl | activo; ExcludePctTradesWithBiggestPl, ExcludePctTradesWithLowestPl | Quitar el 5 % de extremos: el estilo no debe depender de outliers. |

Diferencias del `Ventaja_Retest` respecto al anterior:

- **Gestión monetaria:** FixedSize: 1 lote
- **Fitness:** Weighted: SQN (peso 2, max), StagnationPct (peso 1, min)
- **Filtros (Ranking):** NetProfit(OOS) > 0; ProfitFactor(Full) >= 1.1; NumberOfTrades(Full) >= 580; NumberOfTrades(OOS) >= 170

### 3. Indicadores y bloques seleccionados

Criterio general: Núcleo: velas de giro y falsas rupturas, precio puro, Heikin-Ashi y estructura (niveles diarios/semanales, fractales); ATR sólo como normalizador. Sin osciladores ni medias.

Recuento: **33 señales, 37 indicadores y 32 niveles/rangos stop-limit** (el original: 146 / 29 / 29, todos con peso 1 y sin relación con la tesis). Las familias con peso ≥ 2 son el núcleo del estilo; las de peso 1 son filtros auxiliares que amplían la variedad de estrategias sin cambiar la tesis. Se excluyen siempre los bloques con niveles absolutos dependientes del precio. La columna SELL muestra el bloque espejo que se activa en el kit de ventas.

#### Señales

| Familia (peso) | Qué mide | Por qué en este estilo | Bloques BUY | Espejo SELL |
|---|---|---|---|---|
| velas (8) | Patrones de vela de giro alcista (envolvente, martillo, pauta penetrante, doji) y fractal. | Núcleo: patrones de rechazo y absorción. | `BullishEngulfing`, `Hammer`, `PiercingLine`, `Doji`(w2), `IsBullishFractal` | `BearishEngulfing`, `ShootingStar`, `DarkCloud`, `Doji`, `IsBearishFractal` |
| falsa_ruptura (4) | Recuperación por encima del mínimo de N velas tras perforarlo (trampa bajista). | Trampa: perforación y recuperación. | `BarOpensAboveLowestAfterOpenBelow` | `BarOpensBelowHighestAfterOpenAbove` |
| rup_canal (3) | Apertura por encima del máximo de N velas tras abrir por debajo (ruptura Donchian confirmada). | Ruptura de estructura reciente. | `BarOpensAboveHighestAfterOpenBelow` | `BarOpensBelowLowestAfterOpenAbove` |
| rup_bandas (1) | Apertura/cierre fuera de la banda superior de Bollinger o Keltner. | Filtro auxiliar: amplía la variedad. | `BBBarOpensAboveUpAfterOpenBelow`, `BBBarClosesAboveUp`, `BBBarOpensAboveUp`, `KCBarOpensAboveUpperAfterOpenBelow`, `KCBarClosesAboveUpper`, `KCBarOpensAboveUpper` | `BBBarOpensBelowDownAfterOpenAbove`, `BBBarClosesBelowDown`, `BBBarOpensBelowDown`, `KCBarOpensBelowLowerAfterOpenAbove`, `KCBarClosesBelowLower`, `KCBarOpensBelowLower` |
| vol_expansion (1) | ATR/desviación típica/bandas abriéndose: entra volatilidad. | Filtro auxiliar: amplía la variedad. | `ATRRising`, `ATRChangesUp`, `StdDevRising`, `StdDevChangesUp`, `BBUpperRising`, `BBLowerFalling`, `KCUpperRising`, `KCLowerFalling` | igual (neutral) |
| vol_contraccion (1) | ATR/desviación típica/bandas cerrándose: compresión previa a un movimiento. | Filtro auxiliar: amplía la variedad. | `ATRFalling`, `ATRChangesDown`, `StdDevFalling`, `StdDevChangesDown`, `BBUpperFalling`, `BBLowerRising`, `KCUpperFalling`, `KCLowerRising` | igual (neutral) |
| tiempo_intradia (1) | Franja horaria (hora mayor/menor que) y excluir un día de la semana. | Filtro auxiliar: amplía la variedad. | `BarHourIsBigger`, `BarHourIsSmaller`, `BarDayOfWeekIsNot` | igual (neutral) |
| tiempo_calendario (1) | Excluir un día de la semana o un mes. | Filtro auxiliar: amplía la variedad. | `BarDayOfWeekIsNot`, `BarMonthIsNot` | igual (neutral) |

#### Indicadores

| Familia (peso) | Qué mide | Por qué en este estilo | Bloques BUY | Espejo SELL |
|---|---|---|---|---|
| precio (3) | Apertura, máximo, mínimo y cierre de la vela. | OHLC: estructura pura. | `Close`, `Open`, `High`, `Low` | `Close`, `Open`, `Low`, `High` |
| heiken (2) | Velas Heikin-Ashi (precio suavizado). | Heikin-Ashi: estructura suavizada. | `HeikenAshiOpen`, `HeikenAshiClose`, `HeikenAshiHigh`, `HeikenAshiLow` | `HeikenAshiOpen`, `HeikenAshiClose`, `HeikenAshiLow`, `HeikenAshiHigh` |
| niv_diario (2) | Máximo/mínimo/apertura/cierre del día. | Contexto: niveles del día. | `HighD`, `LowD`, `OpenD`, `CloseD` | `LowD`, `HighD`, `OpenD`, `CloseD` |
| niv_semanal (1) | Máximo/mínimo/apertura/cierre de la semana. | Filtro auxiliar: amplía la variedad. | `HighW`, `LowW`, `OpenW`, `CloseW` | `LowW`, `HighW`, `OpenW`, `CloseW` |
| niv_horario (1) | Máximo/mínimo de un rango horario y de la sesión (apertura/cierre de sesión). | Filtro auxiliar: amplía la variedad. | `HighestInRange`, `LowestInRange`, `SessionHigh`, `SessionLow`, `SessionOpen`, `SessionClose` | `LowestInRange`, `HighestInRange`, `SessionLow`, `SessionHigh`, `SessionOpen`, `SessionClose` |
| niv_canal (2) | Máximo/mínimo de N velas. | Extremos recientes. | `Highest`, `Lowest` | `Lowest`, `Highest` |
| estructura (2) | Fractales (máximos/mínimos locales). | Fractales. | `Fractal` | igual (neutral) |
| volat_ind (1) | ATR y rango verdadero (para comparaciones relativas). | Filtro auxiliar: amplía la variedad. | `ATR`, `TrueRange` | igual (neutral) |
| comparadores (2) | Mayor/menor, mayor o igual, cruces. | Comparaciones de precio. | `IsGreater`, `IsLower`, `IsGreaterOrEqual`, `IsLowerOrEqual`, `CrossesAbove`, `CrossesBelow` | `IsLower`, `IsGreater`, `IsLowerOrEqual`, `IsGreaterOrEqual`, `CrossesBelow`, `CrossesAbove` |
| secuencias (2) | N velas seguidas por encima/debajo, subiendo/bajando. | Secuencias de velas (máximos crecientes…). | `IsGreaterCount`, `IsLowerCount`, `IsRising`, `IsFalling` | `IsLowerCount`, `IsGreaterCount`, `IsFalling`, `IsRising` |

#### Niveles y rangos stop/limit

| Familia (peso) | Qué mide | Por qué en este estilo | Bloques BUY | Espejo SELL |
|---|---|---|---|---|
| stl_vela (5) | Orden en el máximo/mínimo/apertura/cierre de una vela. | Stop sobre el extremo de la vela señal: la confirmación clásica. | `High`, `Low`(w1), `Open`, `Close` | `Low`, `High`, `Open`, `Close` |
| stl_canal (2) | Orden en el máximo/mínimo de N velas. | Stop en extremo reciente. | `Highest`, `Lowest`(w1) | `Lowest`, `Highest` |
| stl_diario (2) | Orden en niveles del día. | Stop en nivel diario. | `HighD`, `LowD`(w1), `OpenD`, `CloseD` | `LowD`, `HighD`, `OpenD`, `CloseD` |
| stl_semanal (1) | Orden en niveles de la semana. | Filtro auxiliar: amplía la variedad. | `HighW`, `LowW`, `OpenW` | `LowW`, `HighW`, `OpenW` |
| stl_horario (1) | Orden en el extremo de un rango horario o de sesión. | Filtro auxiliar: amplía la variedad. | `HighestInRange`, `LowestInRange`, `SessionHigh`, `SessionLow`, `SessionOpen` | `LowestInRange`, `HighestInRange`, `SessionLow`, `SessionHigh`, `SessionOpen` |
| stl_estructura (2) | Orden en fractales o pivotes. | Stop en fractal. | `Fractal`, `Pivots` | igual (neutral) |
| stl_heiken (1) | Orden en niveles Heikin-Ashi. | Filtro auxiliar: amplía la variedad. | `HeikenAshiOpen`, `HeikenAshiClose`, `HeikenAshiHigh`, `HeikenAshiLow` | `HeikenAshiOpen`, `HeikenAshiClose`, `HeikenAshiLow`, `HeikenAshiHigh` |
| stl_rangos (2) | Desplazamiento de la orden: k·ATR, rango de vela, rango verdadero, mayor/menor rango, anchura de Bollinger. | Margen en rango de vela/ATR. | `ATR`, `MTATR`, `BarRange`, `TrueRange`, `BiggestRange`, `SmallestRange`, `BBRange`, `BBWidthRatio` | igual (neutral) |

#### Rangos específicos (BUY → SELL)

| Bloque BUY | Rango BUY | Bloque SELL | Rango SELL |
|---|---|---|---|
| `Indicators.HighestInRange` | Time From 0 a 300 (paso 100); Time To 700 a 1000 (paso 100) | `Indicators.LowestInRange` | Time From 0 a 300 (paso 100); Time To 700 a 1000 (paso 100) |
| `Stop/Limit Price Levels.HighestInRange` | Time From 0 a 300 (paso 100); Time To 700 a 1000 (paso 100) | `Stop/Limit Price Levels.LowestInRange` | Time From 0 a 300 (paso 100); Time To 700 a 1000 (paso 100) |
| `Prices.SessionHigh` | Start Hours 1 a 3 (paso 1); Start Minutes 0 a 0 (paso 1); End Hours 8 a 10 (paso 1); End Minutes 0 a 0 (paso 1) | `Prices.SessionLow` | Start Hours 1 a 3 (paso 1); Start Minutes 0 a 0 (paso 1); End Hours 8 a 10 (paso 1); End Minutes 0 a 0 (paso 1) |
| `Stop/Limit Price Levels.SessionHigh` | Start Hours 1 a 3 (paso 1); Start Minutes 0 a 0 (paso 1); End Hours 8 a 10 (paso 1); End Minutes 0 a 0 (paso 1) | `Stop/Limit Price Levels.SessionLow` | Start Hours 1 a 3 (paso 1); Start Minutes 0 a 0 (paso 1); End Hours 8 a 10 (paso 1); End Minutes 0 a 0 (paso 1) |
| `Prices.SessionOpen` | Start Hours 1 a 3 (paso 1); Start Minutes 0 a 0 (paso 1) | `Prices.SessionOpen` | Start Hours 1 a 3 (paso 1); Start Minutes 0 a 0 (paso 1) |
| `Stop/Limit Price Levels.SessionOpen` | Start Hours 1 a 3 (paso 1); Start Minutes 0 a 0 (paso 1) | `Stop/Limit Price Levels.SessionOpen` | Start Hours 1 a 3 (paso 1); Start Minutes 0 a 0 (paso 1) |
| `Prices.SessionClose` | End Hours 8 a 10 (paso 1); End Minutes 0 a 0 (paso 1) | `Prices.SessionClose` | End Hours 8 a 10 (paso 1); End Minutes 0 a 0 (paso 1) |

### 4. Timeframe, símbolos y horarios

- **Timeframe:** H1.
- **Instrumento recomendado:** Cualquier mercado líquido; mejor en índices y mayores. GBPJPY apto.
- **Horario:** Entradas 01:30-23:30 servidor (la ventana del original: evita el rollover). El rango 'asiático' de los bloques de sesión es 01:00-03:00 → 08:00-10:00.

### 5. Salidas y gestión del riesgo

SL 1-2,5 ATR(14-50); objetivo 1,5-4 ATR con PT = 150-300 % del SL; break-even 1-2 ATR (50 %); salida temporal 5-30 h (30 %); regla (30 %). Riesgo 1 %; 2 entradas/día.

### 6. Filtros y ranking

| Archivo | Fitness | Filtros |
|---|---|---|
| `Estrategia_Build_ConfigInicial_H1_BUY__PriceAction_H1_BUY` | Weighted: ReturnDDRatio (peso 2, max), SQN (peso 1, max) | NumberOfTrades(IS) >= 320; ReturnDDRatio(IS) >= 4; WinningPct(IS) >= 40; ProfitFactor(IS) >= 1.3; AvgBarsInTrade(IS) >= 2; NetProfit(OOS) > 0; NumberOfTrades(OOS) >= 100 |
| `Estrategia_Retest_ConfigInicial_H1_BUY__PriceAction_H1_BUY` | Weighted: ReturnDDRatio (peso 2, max), SQN (peso 1, max) | NetProfit(OOS) > 0; ProfitFactor(OOS) >= 1.1; ReturnDDRatio(Full) >= 6; NumberOfTrades(Full) >= 580; NumberOfTrades(OOS) >= 170; DrawdownPct(Full) <= 20 |
| `Ventaja_Build_ConfigInicial_H1_BUY__PriceAction_H1_BUY` | Weighted: SQN (peso 2, max), StagnationPct (peso 1, min) | NumberOfTrades(IS) >= 320; ReturnDDRatio(IS) >= 2; WinningPct(IS) >= 35; ProfitFactor(IS) >= 1.15; AvgBarsInTrade(IS) >= 2; NetProfit(OOS) > 0; NumberOfTrades(OOS) >= 100 |
| `Ventaja_Retest_ConfigInicial_H1_BUY__PriceAction_H1_BUY` | Weighted: SQN (peso 2, max), StagnationPct (peso 1, min) | NetProfit(OOS) > 0; ProfitFactor(Full) >= 1.1; NumberOfTrades(Full) >= 580; NumberOfTrades(OOS) >= 170 |

Justificación: Ret/DD + SQN (consistencia por operación). El mínimo de operaciones sale de la densidad del estilo (60/año) multiplicada por los años de cada tramo; el acierto y el Ret/DD se adaptan al estilo. Los archivos SELL usan exactamente los mismos filtros.

### 7. Motor y robustez

- **Builder:** población 25 × 4 islas, 30 generaciones, cruce 80 %, mutación 30 %, migración 10 % cada 10, reinicio por estancamiento a 15.
- **Retest:** activo; precisión 2 (tick real + spread personalizado); 3 condiciones. Igual que el original + what-if de outliers.
- **Monte Carlo:** activo; 500 sims; OHLC ±10 % ATR(14), desliz. 0-0.5, spread 2-4. Acepta: NetProfit(Full) >= 0; DrawdownPct(Full) <= 150% de DrawdownPct[main].
- **Manipulación MC:** activo; orden de operaciones 'resampling', saltar 10 %.
- **SPP:** activo; 5000 tests, ±20 %, 6 pasos; ≥85 % rentables.
- **What-if:** activo; ExcludePctTradesWithBiggestPl, ExcludePctTradesWithLowestPl.

### 8. Riesgos conocidos, sobreoptimización y mitigación

Riesgos propios del estilo: Los patrones de vela tienen poca ventaja aislada; el sesgo de minería de datos es alto.

1. Los patrones de vela tienen ventaja aislada pequeña y hay muchísimas combinaciones (desplazamiento 1-3): riesgo alto de minería de datos.
2. Los patrones dependen del OHLC exacto del bróker: el MC de OHLC (±10 % ATR) es aquí especialmente relevante.
3. Se excluyen los patrones bajistas que el original permitía como entrada larga.

### 9. Plan de validación

1. `Ventaja_Build…PriceAction_H1` (salida 3-24 h) → `Ventaja_Retest…`.
2. `Estrategia_Build…` → `Estrategia_Retest…PriceAction_H1`.
3. Retest con datos de otro proveedor/bróker (el OHLC cambia ligeramente).
4. Retest en otros mercados.

---

## NewsProxy

**Noticias (APROXIMACIÓN horaria: ventana de datos de EE. UU.)** · timeframe `M15`

> **Viabilidad:** News trading real **no es viable de forma nativa** en SQX (sin calendario económico). Esta ficha es una aproximación horaria. Alternativas: (a) indicador personalizado en Java que lea un CSV de eventos (requiere programación y reimplementarlo en la plataforma; MT5 tiene calendario nativo en MQL5); (b) usar las noticias sólo como filtro de 'no operar' en el EA.

**Archivos del kit** (todos *no validados en SQX*; tabla completa de cambios en `docs/cambios/`):

| Rol | BUY | SELL |
|---|---|---|
| EB | [`Estrategia_Build_ConfigInicial_H1_BUY__NewsProxy_M15_BUY.cfx`](cambios/Estrategia_Build_ConfigInicial_H1_BUY__NewsProxy_M15_BUY.md) | [`Estrategia_Build_ConfigInicial_H1_BUY__NewsProxy_M15_SELL.cfx`](cambios/Estrategia_Build_ConfigInicial_H1_BUY__NewsProxy_M15_SELL.md) |
| ER | [`Estrategia_Retest_ConfigInicial_H1_BUY__NewsProxy_M15_BUY.cfx`](cambios/Estrategia_Retest_ConfigInicial_H1_BUY__NewsProxy_M15_BUY.md) | [`Estrategia_Retest_ConfigInicial_H1_BUY__NewsProxy_M15_SELL.cfx`](cambios/Estrategia_Retest_ConfigInicial_H1_BUY__NewsProxy_M15_SELL.md) |
| VB | [`Ventaja_Build_ConfigInicial_H1_BUY__NewsProxy_M15_BUY.cfx`](cambios/Ventaja_Build_ConfigInicial_H1_BUY__NewsProxy_M15_BUY.md) | [`Ventaja_Build_ConfigInicial_H1_BUY__NewsProxy_M15_SELL.cfx`](cambios/Ventaja_Build_ConfigInicial_H1_BUY__NewsProxy_M15_SELL.md) |
| VR | [`Ventaja_Retest_ConfigInicial_H1_BUY__NewsProxy_M15_BUY.cfx`](cambios/Ventaja_Retest_ConfigInicial_H1_BUY__NewsProxy_M15_BUY.md) | [`Ventaja_Retest_ConfigInicial_H1_BUY__NewsProxy_M15_SELL.cfx`](cambios/Ventaja_Retest_ConfigInicial_H1_BUY__NewsProxy_M15_SELL.md) |

**Operaciones mínimas exigidas** (60/año): Builder IS ≥ 210, OOS 2019-2020 ≥ 70 (≈280 en 5.0 años de construcción); Retest periodo completo ≥ 580 y holdout 2021-2024 ≥ 170.

### 1. Tesis

Las publicaciones macro programadas de EE. UU. (8:30 ET = 15:30 servidor) provocan una expansión de volatilidad; se opera la ruptura del rango previo dentro de esa ventana. NO es news trading real: SQX no tiene calendario económico; la estrategia opera la ventana todos los días, haya o no noticia.

### 2. Cambios respecto al original

#### 2.a Builder de estrategia completa (`Estrategia_Build`)

| Parámetro | Original | Nuevo | Justificación |
|---|---|---|---|
| Timeframe | H1 | M15 | Horizonte típico del estilo (M15). |
| Periodo de datos | 2013.09.30 – 2020.12.31 | 2016.01.04 – 2020.12.31 | M5/M15: 5 años dan miles de operaciones y reducen el cómputo; 2021-2024 sigue reservado (S4). |
| Tramo OOS | sin OOS | 2019.07.01 – 2020.12.31 | Validación dentro del Builder: el original filtraba sólo sobre IS. |
| Deslizamiento (pips) | 0 | 1.5 | En publicaciones el deslizamiento real es de varios pips; 1,5 pips es el mínimo prudente. |
| Modo de generación | template (plantilla externa .sqx) | simple | El original dependía de una plantilla .sqx no incluida; en modo simple el archivo es autónomo (docs/04 §A.3 para volver a plantilla). |
| Condiciones de entrada | 0–0 | 1–3 | Nivel + 1-2 filtros como máximo; más condiciones = más grados de libertad. |
| Periodos de indicadores | 4–200 | 4–48 | 4-48 velas M15 (1-12 h): contexto del día de la publicación. |
| Desplazamiento (shift) | 1–1 | 1–1 | Sin cambio. |
| Tipos de salida (mín–máx) | 1–5 | 2–4 | SL obligatorio + salidas propias del estilo (el original pedía hasta 5 con 3 disponibles). |
| Tipos de orden | EnterAtMarket (w1) | EnterAtMarket (w1), EnterAtStop (w3, válida 1-4 velas) | Stop sobre el rango pre-dato (bajo él en SELL), caduca en 15-60 min. |
| Stop loss | obligatorio=true; 1-3 × ATR(20-100) | obligatorio=true; 1-2 × ATR(10-40) | El impulso de una noticia dura minutos/horas: salida temporal 30 min-4 h. |
| Profit target | obligatorio=true; 2-5 × ATR(20-100); PT=100-500 % del SL | obligatorio=false; 1.5-4 × ATR(10-40) | El impulso de una noticia dura minutos/horas: salida temporal 30 min-4 h. |
| Trailing stop | sí (50 %), fijo 50-100 pips, 1-5 ATR | no | El impulso de una noticia dura minutos/horas: salida temporal 30 min-4 h. |
| Break-even | no | sí (50 %), 0.5-1.5 ATR | El impulso de una noticia dura minutos/horas: salida temporal 30 min-4 h. |
| Salida temporal | no | sí (70 %), 2-16 velas | El impulso de una noticia dura minutos/horas: salida temporal 30 min-4 h. |
| Salida por regla | no | no | Sin cambio. |
| Ventana de señales | 01:30-23:30 | 15:00-17:00 | Incluye datos de las 10:00 ET (17:00 servidor). |
| Cierres forzados | no diario; no viernes | diario 22:00; viernes 21:00 | Sin exposición nocturna. |
| Máx. operaciones/día | 0 (sin límite) | 1 | Una reacción por día. |
| Distancia máx. orden | no | 0.5 % | 0,5 %. |
| Bloques activos | 146 señales / 29 indicadores / 29 stop-limit | 54 señales / 38 indicadores / 26 stop-limit | Núcleo: rango previo a la publicación (12:00-15:00 → 15:00/15:30), filtros de hora/día y expansión de volatilidad y de volumen de ticks; órdenes stop sobre el rango pre-dato. |
| Gestión monetaria | FixedAmount: riesgo 100 por operación | FixedAmount: riesgo 50 por operación | Riesgo fijo 0.5 % (no compuesto: Ret/DD comparable en el tiempo). |
| Fitness | type="ReturnDDRatio" | Weighted: ProfitFactor (peso 1, max), ReturnDDRatio (peso 2, max) | Operaciones con mucha varianza: PF + Ret/DD. |
| Filtros (Ranking) | AvgBarsInTrade(IS) >= 2; ReturnDDRatio(IS) >= 8; NumberOfTrades(IS) >= 300; WinningPct(IS) >= 40 | NumberOfTrades(IS) >= 210; ReturnDDRatio(IS) >= 3; WinningPct(IS) >= 35; ProfitFactor(IS) >= 1.3; AvgBarsInTrade(IS) >= 2; NetProfit(OOS) > 0; NumberOfTrades(OOS) >= 70 | Umbrales del estilo + exigencia OOS. |
| Filtro población inicial | ReturnDDRatio(IS) >= 5; AvgBarsInTrade(IS) >= 2; NumberOfTrades(IS) >= 250; WinningPct(IS) >= 35 | NumberOfTrades(IS) >= 60 | Sólo nº mínimo de operaciones (recomendación de SQX): con filtros de rentabilidad la población inicial puede tardar horas/días y el Builder no guarda nada mientras tanto. |
| Motor genético | población 5 × 5 islas, 10 generaciones, cruce 46 %, mutación 35 %, migración 6 % cada 5, reinicio por estancamiento a 30 | población 20 × 4 islas, 30 generaciones, cruce 80 %, mutación 30 %, migración 10 % cada 10, reinicio por estancamiento a 15 | 80-100 individuos por generación (el original 25-75) y 30 generaciones (el original 10, insuficiente para que la evolución actúe). |
| Calibración de indicadores | false | true | Recalibra los rangos de valores de indicadores y de rangos stop/limit (±5000 por defecto) para el símbolo y timeframe antes de construir. |

#### 2.b Builder de test de ventaja (`Ventaja_Build`)

| Parámetro | Original | Nuevo | Justificación |
|---|---|---|---|
| Timeframe | H1 | M15 | Horizonte típico del estilo (M15). |
| Periodo de datos | 2013.09.30 – 2020.12.31 | 2016.01.04 – 2020.12.31 | M5/M15: 5 años dan miles de operaciones y reducen el cómputo; 2021-2024 sigue reservado (S4). |
| Tramo OOS | sin OOS | 2019.07.01 – 2020.12.31 | Validación dentro del Builder: el original filtraba sólo sobre IS. |
| Deslizamiento (pips) | 0 | 1.5 | En publicaciones el deslizamiento real es de varios pips; 1,5 pips es el mínimo prudente. |
| Modo de generación | simple | simple | Sin cambio. |
| Condiciones de entrada | 1–3 | 1–3 | Sin cambio. |
| Periodos de indicadores | 4–200 | 4–48 | 4-48 velas M15 (1-12 h): contexto del día de la publicación. |
| Desplazamiento (shift) | 1–1 | 1–1 | Sin cambio. |
| Tipos de salida (mín–máx) | 1–5 | 1–1 | Sólo la salida temporal (test de ventaja). |
| Tipos de orden | EnterAtMarket (w1) | EnterAtMarket (w1), EnterAtStop (w3, válida 1-4 velas) | Stop sobre el rango pre-dato (bajo él en SELL), caduca en 15-60 min. |
| Stop loss | obligatorio=false; sin ATR | obligatorio=false; sin ATR | Sin cambio. |
| Profit target | obligatorio=false; sin ATR | obligatorio=false; sin ATR | Sin cambio. |
| Trailing stop | no | no | Sin cambio. |
| Break-even | no | no | Sin cambio. |
| Salida temporal | sí (50 %), 2-15 velas | sí (100 %), 2-12 velas | Test de ventaja: salida por tiempo 30 min-3 h. |
| Salida por regla | no | no | Sin cambio. |
| Ventana de señales | 01:30-23:30 | 15:00-17:00 | Incluye datos de las 10:00 ET (17:00 servidor). |
| Cierres forzados | no diario; no viernes | diario 22:00; viernes 21:00 | Sin exposición nocturna. |
| Máx. operaciones/día | 0 (sin límite) | 1 | Una reacción por día. |
| Distancia máx. orden | no | 0.5 % | 0,5 %. |
| Bloques activos | 146 señales / 29 indicadores / 29 stop-limit | 54 señales / 38 indicadores / 26 stop-limit | Núcleo: rango previo a la publicación (12:00-15:00 → 15:00/15:30), filtros de hora/día y expansión de volatilidad y de volumen de ticks; órdenes stop sobre el rango pre-dato. |
| Gestión monetaria | FixedSize: 1 lote | FixedSize: 1 lote | Sin cambio. |
| Fitness | Weighted: Stagnation (peso 1, min) | Weighted: SQN (peso 2, max), StagnationPct (peso 1, min) | SQN mide la calidad estadística de la entrada; el original optimizaba sólo 'Stagnation', que ignora el beneficio. |
| Filtros (Ranking) | AvgBarsInTrade(IS) >= 2; ReturnDDRatio(IS) >= 4; NumberOfTrades(IS) >= 300; WinningPct(IS) >= 40 | NumberOfTrades(IS) >= 210; ReturnDDRatio(IS) >= 1.5; WinningPct(IS) >= 30; ProfitFactor(IS) >= 1.15; AvgBarsInTrade(IS) >= 2; NetProfit(OOS) > 0; NumberOfTrades(OOS) >= 70 | Umbrales del estilo + exigencia OOS. Test de ventaja: Ret/DD a la mitad y PF ≥1,15. |
| Filtro población inicial | ReturnDDRatio(IS) >= 2; AvgBarsInTrade(IS) >= 2; NumberOfTrades(IS) >= 250; WinningPct(IS) >= 35 | NumberOfTrades(IS) >= 60 | Sólo nº mínimo de operaciones (recomendación de SQX): con filtros de rentabilidad la población inicial puede tardar horas/días y el Builder no guarda nada mientras tanto. |
| Motor genético | población 15 × 5 islas, 10 generaciones, cruce 46 %, mutación 35 %, migración 6 % cada 5, reinicio por estancamiento a 30 | población 20 × 4 islas, 30 generaciones, cruce 80 %, mutación 30 %, migración 10 % cada 10, reinicio por estancamiento a 15 | 80-100 individuos por generación (el original 25-75) y 30 generaciones (el original 10, insuficiente para que la evolución actúe). |
| Calibración de indicadores | false | true | Recalibra los rangos de valores de indicadores y de rangos stop/limit (±5000 por defecto) para el símbolo y timeframe antes de construir. |

#### 2.c Retesters (`Estrategia_Retest` / `Ventaja_Retest`)

| Parámetro | Original | Nuevo | Justificación |
|---|---|---|---|
| Timeframe | H1 | M15 | Debe coincidir con el Builder del estilo. |
| Periodo / OOS | 2013.09.30 – 2024.07.22; OOS 2021.01.01 – 2024.07.22 | 2013.09.30 – 2024.07.22; OOS 2021.01.01 – 2024.07.22 | Sin cambio. |
| Deslizamiento | 0 | 1.5 | En publicaciones el deslizamiento real es de varios pips; 1,5 pips es el mínimo prudente. |
| Ventana de señales | 01:30-23:30 | 15:00-17:00 | Idéntica al Builder: si difiere, el Retest no reproduce lo construido. |
| Cierres forzados | no diario; no viernes | diario 22:00; viernes 21:00 | Idénticos al Builder. |
| Gestión monetaria | FixedAmount: riesgo 100 por operación | FixedAmount: riesgo 50 por operación | Igual que el Builder correspondiente. |
| Fitness | type="ReturnDDRatio" | Weighted: ProfitFactor (peso 1, max), ReturnDDRatio (peso 2, max) | Igual que el Builder correspondiente. |
| Filtros (Ranking) | (ninguna activa) | NetProfit(OOS) > 0; ProfitFactor(OOS) >= 1.05; ReturnDDRatio(Full) >= 4.5; NumberOfTrades(Full) >= 580; NumberOfTrades(OOS) >= 170; DrawdownPct(Full) <= 20 | El original no filtraba nada (todas use=false) ni borraba fallidas. |
| Mayor precisión | activo; precisión 2 (tick real + spread personalizado); 1 condiciones | activo; precisión 3 (tick real + spread real); 3 condiciones | Spread aleatorio hasta 4x y deslizamiento hasta 3 pips: así es una publicación real. |
| Monte Carlo retest | activo; 1000 sims; OHLC ±10 % ATR(14), spread 1-3. Acepta: NetProfit(IS) >= 0 | activo; 200 sims; OHLC ±10 % ATR(14), desliz. 0-3, spread 2-8. Acepta: NetProfit(Full) >= 0; DrawdownPct(Full) <= 150% de DrawdownPct[main] | Spread desde el base hasta 2-4x, deslizamiento, percentil 95 (no el peor caso) y control del DD. |
| Monte Carlo manipulación | no; orden de operaciones 'exact', saltar 10 % | activo; orden de operaciones 'resampling', saltar 10 % | Barato; 'resampling' y referencia corregida (el original comparaba MC contra MC). |
| SPP / perfil de optimización | activo; 15000 tests, ±20 %, 6 pasos; ≥95 % rentables | activo; 1500 tests, ±20 %, 6 pasos; ≥80 % rentables | Tests y exigencia ajustados al coste de cómputo y a la sensibilidad del estilo. |
| What-if | no; ExcludePctTradesWithBiggestPl, ExcludePctTradesWithLowestPl | activo; ExcludePctTradesWithBiggestPl, ExcludePctTradesWithLowestPl | Quitar el 5 % de extremos: el estilo no debe depender de outliers. |

Diferencias del `Ventaja_Retest` respecto al anterior:

- **Gestión monetaria:** FixedSize: 1 lote
- **Fitness:** Weighted: SQN (peso 2, max), StagnationPct (peso 1, min)
- **Filtros (Ranking):** NetProfit(OOS) > 0; ProfitFactor(Full) >= 1.1; NumberOfTrades(Full) >= 580; NumberOfTrades(OOS) >= 170

### 3. Indicadores y bloques seleccionados

Criterio general: Núcleo: rango previo a la publicación (12:00-15:00 → 15:00/15:30), filtros de hora/día y expansión de volatilidad y de volumen de ticks; órdenes stop sobre el rango pre-dato.

Recuento: **54 señales, 38 indicadores y 26 niveles/rangos stop-limit** (el original: 146 / 29 / 29, todos con peso 1 y sin relación con la tesis). Las familias con peso ≥ 2 son el núcleo del estilo; las de peso 1 son filtros auxiliares que amplían la variedad de estrategias sin cambiar la tesis. Se excluyen siempre los bloques con niveles absolutos dependientes del precio. La columna SELL muestra el bloque espejo que se activa en el kit de ventas.

#### Señales

| Familia (peso) | Qué mide | Por qué en este estilo | Bloques BUY | Espejo SELL |
|---|---|---|---|---|
| tiempo_hora (3) | Hora exacta y día concreto (muy restrictivos: sólo donde la hora es la tesis). | Núcleo del estilo. | `BarHourIs`, `BarDayOfWeekIs` | igual (neutral) |
| tiempo_intradia (2) | Franja horaria (hora mayor/menor que) y excluir un día de la semana. | Aproximación al calendario: hora (15-16) y día de la semana. | `BarHourIsBigger`, `BarHourIsSmaller`, `BarDayOfWeekIsNot` | igual (neutral) |
| vol_expansion (4) | ATR/desviación típica/bandas abriéndose: entra volatilidad. | La publicación se manifiesta como expansión súbita de rango. | `ATRRising`, `ATRChangesUp`, `StdDevRising`, `StdDevChangesUp`, `BBUpperRising`, `BBLowerFalling`, `KCUpperRising`, `KCLowerFalling` | igual (neutral) |
| vol_tick (2) | Volumen de ticks creciente (en FX es actividad, no volumen real). | Pico de actividad en la publicación. | `VolumeRising`, `AvgVolumeRising` | igual (neutral) |
| rup_canal (6) | Apertura por encima del máximo de N velas tras abrir por debajo (ruptura Donchian confirmada). | Ruptura del rango previo. | `BarOpensAboveHighestAfterOpenBelow` | `BarOpensBelowLowestAfterOpenAbove` |
| rup_bandas (2) | Apertura/cierre fuera de la banda superior de Bollinger o Keltner. | Ruptura de bandas. | `BBBarOpensAboveUpAfterOpenBelow`, `BBBarClosesAboveUp`, `BBBarOpensAboveUp`, `KCBarOpensAboveUpperAfterOpenBelow`, `KCBarClosesAboveUpper`, `KCBarOpensAboveUpper` | `BBBarOpensBelowDownAfterOpenAbove`, `BBBarClosesBelowDown`, `BBBarOpensBelowDown`, `KCBarOpensBelowLowerAfterOpenAbove`, `KCBarClosesBelowLower`, `KCBarOpensBelowLower` |
| mom_direccion (1) | Osciladores y momentum girando o subiendo (RSI, estocástico, MACD, OSMA, QQE, Reflex, ROC, CCI, WPR, DeMarker…), sin niveles absolutos. | Filtro auxiliar: amplía la variedad. | `RSIRising`, `RSIChangesUp`, `LaguerreRSIRising`, `LaguerreRSIChangesUP`, `StochSlowDRising`, `StochSlowDChangesUp`, `StochFastKUp`, `MomRising`, `MomChangesUp`, `MACDMainRising`, `MACDMainChangesUp`, `MACDMainCrossAboveSignal`, `MACDMainHigherSignal`, `MACDSignalRising`, `OSMARising`, `OSMAChangesUp`, `AWORising`, `AWOChangesUp`, `QQEValue1Rising`, `QQEValue1CrossAboveValue2`, `QQEValue1HigherValue2`, `QQEValue2Rising`, `ReflexRising`, `ReflexChangesDirectionUP`, `FastReflexCrossUPSlowReflex`, `ROCRising`, `CCIRising`, `CCIChangesUp`, `WPRRising`, `WPRChangesUp`, `DEMRising`, `DEMChangesUp` | `RSIFalling`, `RSIChangesDown`, `LaguerreRSIFalling`, `LaguerreRSIChangesDown`, `StochSlowDFalling`, `StochSlowDChangesDown`, `StochFastKDown`, `MomFalling`, `MomChangesDown`, `MACDMainFalling`, `MACDMainChangesDown`, `MACDMainCrossBelowSignal`, `MACDMainLowerSignal`, `MACDSignalFalling`, `OSMAFalling`, `OSMAChangesDown`, `AWOFalling`, `AWOChangesDown`, `QQEValue1Falling`, `QQEValue1CrossBelowValue2`, `QQEValue1LowerValue2`, `QQEValue2Falling`, `ReflexFalling`, `ReflexChangesDirectionDown`, `FastReflexCrossDownSlowReflex`, `ROCFalling`, `CCIFalling`, `CCIChangesDown`, `WPRFalling`, `WPRChangesDown`, `DEMFalling`, `DEMChangesDown` |

#### Indicadores

| Familia (peso) | Qué mide | Por qué en este estilo | Bloques BUY | Espejo SELL |
|---|---|---|---|---|
| niv_horario (4) | Máximo/mínimo de un rango horario y de la sesión (apertura/cierre de sesión). | Rango 12:00-15:00 → 15:00/15:30 (pre-dato). | `HighestInRange`, `LowestInRange`(w2), `SessionHigh`, `SessionLow`(w2), `SessionOpen`, `SessionClose` | `LowestInRange`, `HighestInRange`, `SessionLow`, `SessionHigh`, `SessionOpen`, `SessionClose` |
| niv_canal (2) | Máximo/mínimo de N velas. | Extremos recientes. | `Highest`, `Lowest` | `Lowest`, `Highest` |
| niv_diario (1) | Máximo/mínimo/apertura/cierre del día. | Filtro auxiliar: amplía la variedad. | `HighD`, `LowD`, `OpenD`, `CloseD` | `LowD`, `HighD`, `OpenD`, `CloseD` |
| precio (1) | Apertura, máximo, mínimo y cierre de la vela. | Filtro auxiliar: amplía la variedad. | `Close`, `Open`, `High`, `Low` | `Close`, `Open`, `Low`, `High` |
| volat_ind (2) | ATR y rango verdadero (para comparaciones relativas). | ATR/rango verdadero para medir la expansión. | `ATR`, `TrueRange` | igual (neutral) |
| bandas (1) | Bandas de Bollinger y canal de Keltner. | Filtro auxiliar: amplía la variedad. | `BollingerBands`, `KeltnerChannel` | igual (neutral) |
| medias (1) | Medias móviles (SMA, EMA, LWMA, SMMA, TEMA, Hull, KAMA) y regresión lineal. | Filtro auxiliar: amplía la variedad. | `SMA`, `EMA`, `LWMA`, `SMMA`, `TEMA`, `HullMovingAverage`, `KAMA`, `LinearRegression` | igual (neutral) |
| comparadores (1) | Mayor/menor, mayor o igual, cruces. | Filtro auxiliar: amplía la variedad. | `IsGreater`, `IsLower`, `IsGreaterOrEqual`, `IsLowerOrEqual`, `CrossesAbove`, `CrossesBelow` | `IsLower`, `IsGreater`, `IsLowerOrEqual`, `IsGreaterOrEqual`, `CrossesBelow`, `CrossesAbove` |
| secuencias (1) | N velas seguidas por encima/debajo, subiendo/bajando. | Filtro auxiliar: amplía la variedad. | `IsGreaterCount`, `IsLowerCount`, `IsRising`, `IsFalling` | `IsLowerCount`, `IsGreaterCount`, `IsFalling`, `IsRising` |

#### Niveles y rangos stop/limit

| Familia (peso) | Qué mide | Por qué en este estilo | Bloques BUY | Espejo SELL |
|---|---|---|---|---|
| stl_horario (5) | Orden en el extremo de un rango horario o de sesión. | Stop sobre el rango pre-dato. | `HighestInRange`, `LowestInRange`(w1), `SessionHigh`, `SessionLow`(w1), `SessionOpen` | `LowestInRange`, `HighestInRange`, `SessionLow`, `SessionHigh`, `SessionOpen` |
| stl_canal (2) | Orden en el máximo/mínimo de N velas. | Stop en extremo reciente. | `Highest`, `Lowest`(w1) | `Lowest`, `Highest` |
| stl_vela (2) | Orden en el máximo/mínimo/apertura/cierre de una vela. | Stop en la vela previa. | `High`, `Low`(w1), `Open`, `Close` | `Low`, `High`, `Open`, `Close` |
| stl_diario (1) | Orden en niveles del día. | Filtro auxiliar: amplía la variedad. | `HighD`, `LowD`, `OpenD`, `CloseD` | `LowD`, `HighD`, `OpenD`, `CloseD` |
| stl_bandas (1) | Orden en Bollinger/Keltner. | Filtro auxiliar: amplía la variedad. | `BollingerBands`, `KeltnerChannel`, `MTKeltnerChannel` | igual (neutral) |
| stl_rangos (3) | Desplazamiento de la orden: k·ATR, rango de vela, rango verdadero, mayor/menor rango, anchura de Bollinger. | Margen para evitar el primer pico. | `ATR`, `MTATR`, `BarRange`, `TrueRange`, `BiggestRange`, `SmallestRange`, `BBRange`, `BBWidthRatio` | igual (neutral) |

#### Rangos específicos (BUY → SELL)

| Bloque BUY | Rango BUY | Bloque SELL | Rango SELL |
|---|---|---|---|
| `Indicators.HighestInRange` | Time From 1200 a 1500 (paso 100); Time To 1500 a 1530 (paso 30) | `Indicators.LowestInRange` | Time From 1200 a 1500 (paso 100); Time To 1500 a 1530 (paso 30) |
| `Stop/Limit Price Levels.HighestInRange` | Time From 1200 a 1500 (paso 100); Time To 1500 a 1530 (paso 30) | `Stop/Limit Price Levels.LowestInRange` | Time From 1200 a 1500 (paso 100); Time To 1500 a 1530 (paso 30) |
| `Prices.SessionHigh` | Start Hours 12 a 14 (paso 1); Start Minutes 0 a 0 (paso 1); End Hours 15 a 15 (paso 1); End Minutes 0 a 0 (paso 1) | `Prices.SessionLow` | Start Hours 12 a 14 (paso 1); Start Minutes 0 a 0 (paso 1); End Hours 15 a 15 (paso 1); End Minutes 0 a 0 (paso 1) |
| `Stop/Limit Price Levels.SessionHigh` | Start Hours 12 a 14 (paso 1); Start Minutes 0 a 0 (paso 1); End Hours 15 a 15 (paso 1); End Minutes 0 a 0 (paso 1) | `Stop/Limit Price Levels.SessionLow` | Start Hours 12 a 14 (paso 1); Start Minutes 0 a 0 (paso 1); End Hours 15 a 15 (paso 1); End Minutes 0 a 0 (paso 1) |
| `Prices.SessionOpen` | Start Hours 12 a 14 (paso 1); Start Minutes 0 a 0 (paso 1) | `Prices.SessionOpen` | Start Hours 12 a 14 (paso 1); Start Minutes 0 a 0 (paso 1) |
| `Stop/Limit Price Levels.SessionOpen` | Start Hours 12 a 14 (paso 1); Start Minutes 0 a 0 (paso 1) | `Stop/Limit Price Levels.SessionOpen` | Start Hours 12 a 14 (paso 1); Start Minutes 0 a 0 (paso 1) |
| `Prices.SessionClose` | End Hours 15 a 15 (paso 1); End Minutes 0 a 0 (paso 1) | `Prices.SessionClose` | End Hours 15 a 15 (paso 1); End Minutes 0 a 0 (paso 1) |
| `BarHourIs` | Hour 15 a 16 (paso 1) | `BarHourIs` | Hour 15 a 16 (paso 1) |
| `BarHourIsBigger` | Hour 14 a 16 (paso 1) | `BarHourIsBigger` | Hour 14 a 16 (paso 1) |
| `BarHourIsSmaller` | Hour 16 a 18 (paso 1) | `BarHourIsSmaller` | Hour 16 a 18 (paso 1) |

### 4. Timeframe, símbolos y horarios

- **Timeframe:** M15.
- **Instrumento recomendado:** EURUSD/USDJPY/oro/US30 (reaccionan a datos de EE. UU.). Exige datos tick con spread real.
- **Horario:** Rango pre-dato 12:00-15:00 → 15:00/15:30; señales 15:00-17:00 servidor (8:00-10:00 ET con la convención S5); `BarHourIs` 15-16; cierre 22:00 (viernes 21:00); una operación/día.

### 5. Salidas y gestión del riesgo

SL 1-2 ATR(10-40) de M15; objetivo opcional 1,5-4 ATR; break-even 0,5-1,5 ATR (50 %); salida temporal 2-16 velas = 30 min-4 h (70 %). Riesgo 0,5 %.

### 6. Filtros y ranking

| Archivo | Fitness | Filtros |
|---|---|---|
| `Estrategia_Build_ConfigInicial_H1_BUY__NewsProxy_M15_BUY` | Weighted: ProfitFactor (peso 1, max), ReturnDDRatio (peso 2, max) | NumberOfTrades(IS) >= 210; ReturnDDRatio(IS) >= 3; WinningPct(IS) >= 35; ProfitFactor(IS) >= 1.3; AvgBarsInTrade(IS) >= 2; NetProfit(OOS) > 0; NumberOfTrades(OOS) >= 70 |
| `Estrategia_Retest_ConfigInicial_H1_BUY__NewsProxy_M15_BUY` | Weighted: ProfitFactor (peso 1, max), ReturnDDRatio (peso 2, max) | NetProfit(OOS) > 0; ProfitFactor(OOS) >= 1.05; ReturnDDRatio(Full) >= 4.5; NumberOfTrades(Full) >= 580; NumberOfTrades(OOS) >= 170; DrawdownPct(Full) <= 20 |
| `Ventaja_Build_ConfigInicial_H1_BUY__NewsProxy_M15_BUY` | Weighted: SQN (peso 2, max), StagnationPct (peso 1, min) | NumberOfTrades(IS) >= 210; ReturnDDRatio(IS) >= 1.5; WinningPct(IS) >= 30; ProfitFactor(IS) >= 1.15; AvgBarsInTrade(IS) >= 2; NetProfit(OOS) > 0; NumberOfTrades(OOS) >= 70 |
| `Ventaja_Retest_ConfigInicial_H1_BUY__NewsProxy_M15_BUY` | Weighted: SQN (peso 2, max), StagnationPct (peso 1, min) | NetProfit(OOS) > 0; ProfitFactor(Full) >= 1.1; NumberOfTrades(Full) >= 580; NumberOfTrades(OOS) >= 170 |

Justificación: Operaciones con mucha varianza: PF + Ret/DD. El mínimo de operaciones sale de la densidad del estilo (60/año) multiplicada por los años de cada tramo; el acierto y el Ret/DD se adaptan al estilo. Los archivos SELL usan exactamente los mismos filtros.

### 7. Motor y robustez

- **Builder:** población 20 × 4 islas, 30 generaciones, cruce 80 %, mutación 30 %, migración 10 % cada 10, reinicio por estancamiento a 15.
- **Retest:** activo; precisión 3 (tick real + spread real); 3 condiciones. Spread aleatorio hasta 4x y deslizamiento hasta 3 pips: así es una publicación real.
- **Monte Carlo:** activo; 200 sims; OHLC ±10 % ATR(14), desliz. 0-3, spread 2-8. Acepta: NetProfit(Full) >= 0; DrawdownPct(Full) <= 150% de DrawdownPct[main].
- **Manipulación MC:** activo; orden de operaciones 'resampling', saltar 10 %.
- **SPP:** activo; 1500 tests, ±20 %, 6 pasos; ≥80 % rentables.
- **What-if:** activo; ExcludePctTradesWithBiggestPl, ExcludePctTradesWithLowestPl.

### 8. Riesgos conocidos, sobreoptimización y mitigación

Riesgos propios del estilo: No distingue días con/sin noticia; horario DST; spreads y deslizamiento reales muy superiores a los de datos M1; requotes.

1. La estrategia opera la ventana TODOS los días: el resultado mezcla días con dato y sin dato.
2. Las horas de publicación cambian con el DST de EE. UU. frente al de la UE (marzo/noviembre).
3. El spread y el deslizamiento de una publicación real no están en datos M1: MC de spread hasta 8 pips y deslizamiento hasta 3 pips + precisión 3.

### 9. Plan de validación

1. `Ventaja_Build…NewsProxy_M15` → `Ventaja_Retest…`.
2. `Estrategia_Build…` → `Estrategia_Retest…NewsProxy_M15`.
3. **Validación clave fuera de SQX**: exporta las operaciones (CSV) y crúzalas con un calendario histórico; compara el resultado en días con dato de alto impacto frente a días sin dato. Si no hay diferencia, la estrategia no es de noticias: es una ruptura horaria.
4. Demo durante varias publicaciones (NFP, IPC) midiendo el deslizamiento real.

---

