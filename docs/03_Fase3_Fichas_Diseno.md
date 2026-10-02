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
| S1 | Símbolo | Se conserva `GBPJPY_M1_M1_UTCPlus02` en los 32 archivos para que carguen en tu instalación (es el único símbolo presente en los Setup de los 4 originales). Cada ficha indica el instrumento recomendado; cámbialo en *Data* antes de ejecutar. |
| S2 | Costes | Se conservan los costes del original (spread 2, comisión SizeBased 0,7, swap -7,67/+4,30 triple viernes) porque no conozco tu bróker; **son incoherentes con GBPJPY** y deben corregirse (checklist, punto 3). Sólo se cambia el deslizamiento (0 → 0,3-1,5 según estilo). |
| S3 | Datos | M1 disponible de 2013.09.30 a 2024.07.22 (el rango que usan los originales). |
| S4 | Partición temporal | Se conserva la partición del autor: construcción hasta 2020.12.31 y OOS final 2021.01.01-2024.07.22 en el Retest (nunca visto por el Builder). Se añade un tramo de validación dentro del Builder (2019-2020, o 2019.07-2020 en M5/M15). |
| S5 | Horario del servidor | UTC+2 en invierno / UTC+3 en verano siguiendo el cambio de hora de EE. UU. (convención "cierre de Nueva York = 00:00"). Con ella, 8:30 ET = 15:30 servidor todo el año. |
| S6 | Dirección | Sólo largos, como los originales; el kit SELL se obtiene replicando con *Market sides* = short. |
| S7 | Capital y riesgo | 10.000 de capital; riesgo fijo 0,5 % (alta frecuencia) o 1 % por operación; drawdown máximo tolerable 20 % (25 % en Position/Trend). |
| S8 | Build | Los archivos son de la build 140.2099. Se asume que la build 144 los importa (SQX suele mantener compatibilidad hacia atrás), pero **no está verificado**. |

## Estructura común de cada kit

Cada estilo conserva la arquitectura de dos etapas del autor, que es su principal acierto:

1. **`Ventaja_Build`** busca *entradas* con ventaja usando sólo una salida temporal y tamaño fijo (sin SL/PT), para medir la entrada aislada.
2. **`Ventaja_Retest`** comprueba la robustez de esa ventaja (tick real, Monte Carlo, SPP, OOS 2021-2024).
3. **`Estrategia_Build`** genera la estrategia completa (entrada + SL/PT/trailing/salidas) con riesgo fijo. *Cambio metodológico*: el original usaba una plantilla externa con la entrada fija; los nuevos están en modo `simple` para funcionar sin ese archivo (docs/04 §A.3 explica cómo volver al modo plantilla).
4. **`Estrategia_Retest`** valida la estrategia completa con los mismos tests y el holdout 2021-2024.

Índice: [Scalping](#scalping) · [DayTrading](#daytrading) · [Swing](#swing) · [Position](#position) · [TrendFollowing](#trendfollowing) · [Range](#range) · [PriceAction](#priceaction) · [NewsProxy](#newsproxy)

---

## Scalping

**Scalping (micro-ruptura en sesión líquida)** · timeframe `M5`

> **Viabilidad:** Scalping de ticks/segundos (libro de órdenes, latencia) **no es viable en SQX**: el motor trabaja con barras (mínimo M1). Esta ficha es la alternativa más cercana (M5). Si no tienes datos tick con spread real ni spreads brutos ≤0,3 pips, usa la ficha Day Trading.

**Archivos del kit** (todos *no validados en SQX*):

- `configs/Scalping/Estrategia_Build_ConfigInicial_H1_BUY__Scalping_M5.cfx` — tabla completa de cambios: [`docs/cambios/Estrategia_Build_ConfigInicial_H1_BUY__Scalping_M5.md`](cambios/Estrategia_Build_ConfigInicial_H1_BUY__Scalping_M5.md)
- `configs/Scalping/Estrategia_Retest_ConfigInicial_H1_BUY__Scalping_M5.cfx` — tabla completa de cambios: [`docs/cambios/Estrategia_Retest_ConfigInicial_H1_BUY__Scalping_M5.md`](cambios/Estrategia_Retest_ConfigInicial_H1_BUY__Scalping_M5.md)
- `configs/Scalping/Ventaja_Build_ConfigInicial_H1_BUY__Scalping_M5.cfx` — tabla completa de cambios: [`docs/cambios/Ventaja_Build_ConfigInicial_H1_BUY__Scalping_M5.md`](cambios/Ventaja_Build_ConfigInicial_H1_BUY__Scalping_M5.md)
- `configs/Scalping/Ventaja_Retest_ConfigInicial_H1_BUY__Scalping_M5.cfx` — tabla completa de cambios: [`docs/cambios/Ventaja_Retest_ConfigInicial_H1_BUY__Scalping_M5.md`](cambios/Ventaja_Retest_ConfigInicial_H1_BUY__Scalping_M5.md)

### 1. Tesis

En las aperturas de Londres y el solape Londres-Nueva York entra liquidez direccional; tras una micro-consolidación, la ruptura de su máximo tiende a continuar unas pocas velas. La ventaja es pequeña y sólo existe si el coste total (spread+comisión+deslizamiento) es una fracción pequeña del ATR de M5.

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
| Tipos de orden | EnterAtMarket (w1) | EnterAtMarket (w1), EnterAtStop (w2, válida 1-3 velas) | Orden stop por encima del máximo: entra sólo si la ruptura ocurre; validez 1-3 velas (5-15 min) para no comprar rupturas viejas. |
| Stop loss | obligatorio=true; 1-3 × ATR(20-100) | obligatorio=true; 1-2.5 × ATR(14-50) | SL/PT en ATR de M5 (adaptativos); break-even rápido; salida temporal 30 min-3 h: la ventaja de un scalp se agota en pocas velas. |
| Profit target | obligatorio=true; 2-5 × ATR(20-100); PT=100-500 % del SL | obligatorio=true; 1-3 × ATR(14-50); PT=80-250 % del SL | SL/PT en ATR de M5 (adaptativos); break-even rápido; salida temporal 30 min-3 h: la ventaja de un scalp se agota en pocas velas. |
| Trailing stop | sí (50 %), fijo 50-100 pips, 1-5 ATR | no | SL/PT en ATR de M5 (adaptativos); break-even rápido; salida temporal 30 min-3 h: la ventaja de un scalp se agota en pocas velas. |
| Break-even | no | sí (50 %), 0.5-1.5 ATR | SL/PT en ATR de M5 (adaptativos); break-even rápido; salida temporal 30 min-3 h: la ventaja de un scalp se agota en pocas velas. |
| Salida temporal | no | sí (50 %), 6-36 velas | SL/PT en ATR de M5 (adaptativos); break-even rápido; salida temporal 30 min-3 h: la ventaja de un scalp se agota en pocas velas. |
| Salida por regla | no | sí (30 %) | SL/PT en ATR de M5 (adaptativos); break-even rápido; salida temporal 30 min-3 h: la ventaja de un scalp se agota en pocas velas. |
| Ventana de señales | 01:30-23:30 | 09:00-18:30 + cierre al final | 18:30 servidor ≈ final del solape Londres-NY. |
| Cierres forzados | no diario; no viernes | diario 21:00; viernes 20:00 | Red de seguridad: nada abierto al cierre del día. |
| Máx. operaciones/día | 0 (sin límite) | 4 | Limita sobre-operar en días de ruido. |
| Distancia máx. orden | no | 0.3 % | 0,3 % ≈ 45 pips en GBPJPY; tope razonable para M5. |
| Bloques activos | 146 señales / 29 indicadores / 29 stop-limit | 12 señales / 17 indicadores / 8 stop-limit | Bloques de ruptura de rango corto (Donchian, Bollinger, Keltner, máximo de sesión asiática) + confirmación de expansión de volatilidad sin niveles absolutos (dependientes de precio). |
| Gestión monetaria | FixedAmount: riesgo 100 por operación | FixedAmount: riesgo 50 por operación | Riesgo fijo 0.5 % (no compuesto: Ret/DD comparable en el tiempo). |
| Fitness | type="ReturnDDRatio" | Weighted: ReturnDDRatio (peso 1, max), SQN (peso 2, max) | SQN premia expectativa consistente con muchas operaciones (lo propio de un scalper); Ret/DD evita curvas con drawdowns profundos. |
| Filtros (Ranking) | AvgBarsInTrade(IS) >= 2; ReturnDDRatio(IS) >= 8; NumberOfTrades(IS) >= 300; WinningPct(IS) >= 40 | NumberOfTrades(IS) >= 1000; ReturnDDRatio(IS) >= 6; WinningPct(IS) >= 45; ProfitFactor(IS) >= 1.25; AvgBarsInTrade(IS) >= 3; NetProfit(OOS) > 0; ProfitFactor(OOS) >= 1.1 | Umbrales del estilo + exigencia OOS. |
| Filtro población inicial | ReturnDDRatio(IS) >= 5; AvgBarsInTrade(IS) >= 2; NumberOfTrades(IS) >= 250; WinningPct(IS) >= 35 | ReturnDDRatio(IS) >= 3.75; AvgBarsInTrade(IS) >= 3; NumberOfTrades(IS) >= 830; WinningPct(IS) >= 40 | Misma proporción que el autor (≈60 % Ret/DD, ≈83 % operaciones, -5 puntos de acierto). |
| Motor genético | población 5 × 5 islas, 10 generaciones, cruce 46 %, mutación 35 %, migración 6 % cada 5, reinicio por estancamiento a 30 | población 30 × 4 islas, 30 generaciones, cruce 80 %, mutación 30 %, migración 10 % cada 10, reinicio por estancamiento a 15 | Población y generaciones del original insuficientes para que la evolución actúe (Fase 1 §6). |

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
| Tipos de orden | EnterAtMarket (w1) | EnterAtMarket (w1), EnterAtStop (w2, válida 1-3 velas) | Orden stop por encima del máximo: entra sólo si la ruptura ocurre; validez 1-3 velas (5-15 min) para no comprar rupturas viejas. |
| Stop loss | obligatorio=false; sin ATR | obligatorio=false; sin ATR | Sin cambio. |
| Profit target | obligatorio=false; sin ATR | obligatorio=false; sin ATR | Sin cambio. |
| Trailing stop | no | no | Sin cambio. |
| Break-even | no | no | Sin cambio. |
| Salida temporal | sí (50 %), 2-15 velas | sí (100 %), 3-24 velas | Test de ventaja: salida pura por tiempo 15 min-2 h, sin SL/PT. |
| Salida por regla | no | no | Sin cambio. |
| Ventana de señales | 01:30-23:30 | 09:00-18:30 + cierre al final | 18:30 servidor ≈ final del solape Londres-NY. |
| Cierres forzados | no diario; no viernes | diario 21:00; viernes 20:00 | Red de seguridad: nada abierto al cierre del día. |
| Máx. operaciones/día | 0 (sin límite) | 4 | Limita sobre-operar en días de ruido. |
| Distancia máx. orden | no | 0.3 % | 0,3 % ≈ 45 pips en GBPJPY; tope razonable para M5. |
| Bloques activos | 146 señales / 29 indicadores / 29 stop-limit | 12 señales / 17 indicadores / 8 stop-limit | Bloques de ruptura de rango corto (Donchian, Bollinger, Keltner, máximo de sesión asiática) + confirmación de expansión de volatilidad sin niveles absolutos (dependientes de precio). |
| Gestión monetaria | FixedSize: 1 lote | FixedSize: 1 lote | Sin cambio. |
| Fitness | Weighted: Stagnation (peso 1, min) | Weighted: SQN (peso 2, max), StagnationPct (peso 1, min) | SQN mide la calidad estadística de la entrada; el original optimizaba sólo 'Stagnation', que ignora el beneficio. |
| Filtros (Ranking) | AvgBarsInTrade(IS) >= 2; ReturnDDRatio(IS) >= 4; NumberOfTrades(IS) >= 300; WinningPct(IS) >= 40 | NumberOfTrades(IS) >= 1000; ReturnDDRatio(IS) >= 3; WinningPct(IS) >= 40; ProfitFactor(IS) >= 1.15; AvgBarsInTrade(IS) >= 3; NetProfit(OOS) > 0 | Umbrales del estilo + exigencia OOS. Test de ventaja: Ret/DD a la mitad y PF ≥1,15. |
| Filtro población inicial | ReturnDDRatio(IS) >= 2; AvgBarsInTrade(IS) >= 2; NumberOfTrades(IS) >= 250; WinningPct(IS) >= 35 | ReturnDDRatio(IS) >= 1.5; AvgBarsInTrade(IS) >= 3; NumberOfTrades(IS) >= 830; WinningPct(IS) >= 35 | Misma proporción que el autor (≈60 % Ret/DD, ≈83 % operaciones, -5 puntos de acierto). |
| Motor genético | población 15 × 5 islas, 10 generaciones, cruce 46 %, mutación 35 %, migración 6 % cada 5, reinicio por estancamiento a 30 | población 30 × 4 islas, 30 generaciones, cruce 80 %, mutación 30 %, migración 10 % cada 10, reinicio por estancamiento a 15 | Población y generaciones del original insuficientes para que la evolución actúe (Fase 1 §6). |

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
| Filtros (Ranking) | (ninguna activa) | NetProfit(OOS) > 0; ProfitFactor(OOS) >= 1.1; ReturnDDRatio(Full) >= 9; NumberOfTrades(Full) >= 1500; DrawdownPct(Full) <= 20 | El original no filtraba nada (todas use=false) ni borraba fallidas. |
| Mayor precisión | activo; precisión 2 (tick real + spread personalizado); 1 condiciones | activo; precisión 3 (tick real + spread real); 3 condiciones | Precisión 3 (tick real con spread real): en M5 el spread variable decide el resultado. |
| Monte Carlo retest | activo; 1000 sims; OHLC ±10 % ATR(14), spread 1-3. Acepta: NetProfit(IS) >= 0 | activo; 200 sims; OHLC ±10 % ATR(14), desliz. 0-1, spread 2-4. Acepta: NetProfit(Full) >= 0; DrawdownPct(Full) <= 150% de DrawdownPct[main] | Spread desde el base hasta 2-4x, deslizamiento, percentil 95 (no el peor caso) y control del DD. |
| Monte Carlo manipulación | no; orden de operaciones 'exact', saltar 10 % | activo; orden de operaciones 'resampling', saltar 10 % | Barato; 'resampling' y referencia corregida (el original comparaba MC contra MC). |
| SPP / perfil de optimización | activo; 15000 tests, ±20 %, 6 pasos; ≥95 % rentables | activo; 1500 tests, ±20 %, 6 pasos; ≥80 % rentables | Tests y exigencia ajustados al coste de cómputo y a la sensibilidad del estilo. |
| What-if | no; ExcludePctTradesWithBiggestPl, ExcludePctTradesWithLowestPl | activo; ExcludePctTradesWithBiggestPl, ExcludePctTradesWithLowestPl | Quitar el 5 % de extremos: el estilo no debe depender de outliers. |

Diferencias del `Ventaja_Retest` respecto al anterior:

- **Gestión monetaria:** FixedSize: 1 lote
- **Fitness:** Weighted: SQN (peso 2, max), StagnationPct (peso 1, min)
- **Filtros (Ranking):** NetProfit(OOS) > 0; ProfitFactor(Full) >= 1.1; NumberOfTrades(Full) >= 1500

### 3. Indicadores y bloques seleccionados

Criterio general: Bloques de ruptura de rango corto (Donchian, Bollinger, Keltner, máximo de sesión asiática) + confirmación de expansión de volatilidad sin niveles absolutos (dependientes de precio). El original activaba 146 señales + 29 indicadores + 29 niveles stop/limit genéricos con peso 1; aquí sólo los coherentes con la tesis, con peso mayor en los centrales (w2-w3).

| Bloque | Peso | Familia | Qué mide | Por qué en este estilo | Rango específico |
|---|---|---|---|---|---|
| `BarOpensAboveHighestAfterOpenBelow` | 3 | Ruptura de nivel | La vela abre por encima del máximo de N velas tras abrir por debajo (ruptura Donchian confirmada en apertura). | La tesis es la micro-ruptura: estos bloques definen el nivel roto. | global del estilo |
| `BBBarOpensAboveUpAfterOpenBelow` | 2 | Ruptura de nivel | Cruce de apertura por encima de la banda superior de Bollinger. | La tesis es la micro-ruptura: estos bloques definen el nivel roto. | global del estilo |
| `KCBarOpensAboveUpperAfterOpenBelow` | 2 | Ruptura de nivel | Cruce de apertura por encima de la banda superior de Keltner (ATR). | La tesis es la micro-ruptura: estos bloques definen el nivel roto. | global del estilo |
| `BBBarClosesAboveUp` | 1 | Ruptura de nivel | Cierre por encima de la banda superior de Bollinger. | La tesis es la micro-ruptura: estos bloques definen el nivel roto. | global del estilo |
| `KCBarClosesAboveUpper` | 1 | Ruptura de nivel | Cierre por encima de la banda superior de Keltner. | La tesis es la micro-ruptura: estos bloques definen el nivel roto. | global del estilo |
| `LaguerreRSICrossUP` | 1 | Oscilador | RSI de Laguerre (0-1, poco retardo) cruza al alza un nivel. | Sólo como filtro de momentum (niveles 50-70 / 0,4-0,85), nunca como sobreventa. | Gamma 0.3 a 0.8 (paso 0.05); Level 0.4 a 0.85 (paso 0.05) |
| `RSICrossUp` | 1 | Oscilador | RSI cruza hacia arriba un nivel. | Sólo como filtro de momentum (niveles 50-70 / 0,4-0,85), nunca como sobreventa. | Level 50 a 70 (paso 5) |
| `ADXRising` | 1 | Tendencia | ADX creciente: la tendencia gana fuerza. | Filtro de dirección de muy corto plazo. | global del estilo |
| `Indicators.EMA` | 1 | Tendencia | Media exponencial. | Filtro de dirección de muy corto plazo. | global del estilo |
| `MARising` | 1 | Tendencia | Media móvil con pendiente positiva. | Filtro de dirección de muy corto plazo. | global del estilo |
| `ATRChangesUp` | 1 | Volatilidad | El ATR cambia de dirección al alza. | Sin expansión de volatilidad la ruptura no cubre costes; confirman que entra flujo. | global del estilo |
| `ATRRising` | 1 | Volatilidad | ATR creciente: expansión de volatilidad (sin nivel absoluto). | Sin expansión de volatilidad la ruptura no cubre costes; confirman que entra flujo. | global del estilo |
| `Indicators.ATR` | 1 | Volatilidad | ATR: rango medio verdadero. | Sin expansión de volatilidad la ruptura no cubre costes; confirman que entra flujo. | global del estilo |
| `StdDevRising` | 1 | Volatilidad | Desviación típica creciente. | Sin expansión de volatilidad la ruptura no cubre costes; confirman que entra flujo. | global del estilo |
| `Indicators.Highest` | 2 | Nivel de referencia | Máximo de N velas (canal Donchian). | Máximos/mínimos de N velas y de la sesión asiática: los niveles que la apertura de Londres rompe. | global del estilo |
| `Prices.SessionHigh` | 2 | Nivel de referencia | Máximo de una sesión horaria configurable. | Máximos/mínimos de N velas y de la sesión asiática: los niveles que la apertura de Londres rompe. | Start Hours 1 a 3 (paso 1); Start Minutes 0 a 0 (paso 1); End Hours 8 a 10 (paso 1); End Minutes 0 a 0 (paso 1) |
| `Indicators.BollingerBands` | 1 | Nivel de referencia | Bandas de Bollinger (media ± k·desviación). | Máximos/mínimos de N velas y de la sesión asiática: los niveles que la apertura de Londres rompe. | global del estilo |
| `Indicators.KeltnerChannel` | 1 | Nivel de referencia | Canal de Keltner (media ± k·ATR). | Máximos/mínimos de N velas y de la sesión asiática: los niveles que la apertura de Londres rompe. | global del estilo |
| `Indicators.Lowest` | 1 | Nivel de referencia | Mínimo de N velas. | Máximos/mínimos de N velas y de la sesión asiática: los niveles que la apertura de Londres rompe. | global del estilo |
| `Prices.SessionLow` | 1 | Nivel de referencia | Mínimo de una sesión horaria configurable. | Máximos/mínimos de N velas y de la sesión asiática: los niveles que la apertura de Londres rompe. | Start Hours 1 a 3 (paso 1); Start Minutes 0 a 0 (paso 1); End Hours 8 a 10 (paso 1); End Minutes 0 a 0 (paso 1) |
| `Prices.Close` | 1 | Precio | Cierre. | Comparaciones de precio con los niveles. | global del estilo |
| `Prices.High` | 1 | Precio | Máximo. | Comparaciones de precio con los niveles. | global del estilo |
| `Prices.Low` | 1 | Precio | Mínimo. | Comparaciones de precio con los niveles. | global del estilo |
| `Prices.Open` | 1 | Precio | Apertura. | Comparaciones de precio con los niveles. | global del estilo |
| `CrossesAbove` | 1 | Comparador | A cruza B al alza. | Construyen 'precio cruza/está sobre nivel'. | global del estilo |
| `CrossesBelow` | 1 | Comparador | A cruza B a la baja. | Construyen 'precio cruza/está sobre nivel'. | global del estilo |
| `IsGreater` | 1 | Comparador | A > B. | Construyen 'precio cruza/está sobre nivel'. | global del estilo |
| `IsGreaterCount` | 1 | Comparador | A > B durante N velas seguidas. | Construyen 'precio cruza/está sobre nivel'. | global del estilo |
| `IsLower` | 1 | Comparador | A < B. | Construyen 'precio cruza/está sobre nivel'. | global del estilo |
| `Stop/Limit Price Levels.Highest` | 3 | Precio de orden stop/limit | Precio de la orden = máximo de N velas. | Dónde se coloca la orden stop de ruptura. | global del estilo |
| `Stop/Limit Price Levels.High` | 2 | Precio de orden stop/limit | Precio de la orden = máximo de una vela (vela señal). | Dónde se coloca la orden stop de ruptura. | global del estilo |
| `Stop/Limit Price Levels.SessionHigh` | 2 | Precio de orden stop/limit | Precio = máximo de sesión. | Dónde se coloca la orden stop de ruptura. | Start Hours 1 a 3 (paso 1); Start Minutes 0 a 0 (paso 1); End Hours 8 a 10 (paso 1); End Minutes 0 a 0 (paso 1) |
| `Stop/Limit Price Levels.BollingerBands` | 1 | Precio de orden stop/limit | Precio = banda de Bollinger. | Dónde se coloca la orden stop de ruptura. | global del estilo |
| `Stop/Limit Price Levels.KeltnerChannel` | 1 | Precio de orden stop/limit | Precio = banda de Keltner. | Dónde se coloca la orden stop de ruptura. | global del estilo |
| `Stop/Limit Price Ranges.ATR` | 2 | Desplazamiento de orden | Desplazamiento del precio de la orden = k·ATR. | Margen por encima del nivel para filtrar toques. | global del estilo |
| `Stop/Limit Price Ranges.BarRange` | 1 | Desplazamiento de orden | Desplazamiento = k·rango de la vela. | Margen por encima del nivel para filtrar toques. | global del estilo |
| `Stop/Limit Price Ranges.SmallestRange` | 1 | Desplazamiento de orden | Desplazamiento = k·rango mínimo de N velas (contracción). | Margen por encima del nivel para filtrar toques. | global del estilo |

### 4. Timeframe, símbolos y horarios

- **Timeframe:** M5.
- **Instrumento recomendado:** EURUSD o índice US500/NAS100 con spread bruto ≤0,3 pips/0,5 pts + comisión. GBPJPY con 2 pips de spread NO es apto (coste ≈30 % del ATR de M5).
- **Horario:** Señales 09:00-18:30 servidor (apertura de Londres + solape con Nueva York); cierre forzado al final de la ventana (`ExitAtEndOfRange`), a las 21:00 y los viernes a las 20:00. Se evita 23:00-01:30 (rollover, spreads anchos). El rango 'asiático' de los bloques de sesión es 01:00-03:00 → 08:00-10:00.

### 5. Salidas y gestión del riesgo

SL 1-2,5 ATR(14-50) de M5 (≈6-25 pips en EURUSD), PT 1-3 ATR con PT = 80-250 % del SL, break-even a 0,5-1,5 ATR (50 % de las estrategias), salida temporal 6-36 velas (30 min-3 h) y regla de salida opcional. Riesgo 0,5 % por operación y máximo 4 operaciones/día (≤2 % de riesgo diario).

### 6. Filtros y ranking

| Archivo | Fitness | Filtros |
|---|---|---|
| `Estrategia_Build_ConfigInicial_H1_BUY__Scalping_M5` | Weighted: ReturnDDRatio (peso 1, max), SQN (peso 2, max) | NumberOfTrades(IS) >= 1000; ReturnDDRatio(IS) >= 6; WinningPct(IS) >= 45; ProfitFactor(IS) >= 1.25; AvgBarsInTrade(IS) >= 3; NetProfit(OOS) > 0; ProfitFactor(OOS) >= 1.1 |
| `Estrategia_Retest_ConfigInicial_H1_BUY__Scalping_M5` | Weighted: ReturnDDRatio (peso 1, max), SQN (peso 2, max) | NetProfit(OOS) > 0; ProfitFactor(OOS) >= 1.1; ReturnDDRatio(Full) >= 9; NumberOfTrades(Full) >= 1500; DrawdownPct(Full) <= 20 |
| `Ventaja_Build_ConfigInicial_H1_BUY__Scalping_M5` | Weighted: SQN (peso 2, max), StagnationPct (peso 1, min) | NumberOfTrades(IS) >= 1000; ReturnDDRatio(IS) >= 3; WinningPct(IS) >= 40; ProfitFactor(IS) >= 1.15; AvgBarsInTrade(IS) >= 3; NetProfit(OOS) > 0 |
| `Ventaja_Retest_ConfigInicial_H1_BUY__Scalping_M5` | Weighted: SQN (peso 2, max), StagnationPct (peso 1, min) | NetProfit(OOS) > 0; ProfitFactor(Full) >= 1.1; NumberOfTrades(Full) >= 1500 |

Justificación: SQN premia expectativa consistente con muchas operaciones (lo propio de un scalper); Ret/DD evita curvas con drawdowns profundos. Los umbrales reflejan la frecuencia y el acierto típicos del estilo (no se usa el 40 % de acierto ni las 300 operaciones del original para todos).

### 7. Motor y robustez

- **Builder:** población 30 × 4 islas, 30 generaciones, cruce 80 %, mutación 30 %, migración 10 % cada 10, reinicio por estancamiento a 15.
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

**Archivos del kit** (todos *no validados en SQX*):

- `configs/DayTrading/Estrategia_Build_ConfigInicial_H1_BUY__DayTrading_M15.cfx` — tabla completa de cambios: [`docs/cambios/Estrategia_Build_ConfigInicial_H1_BUY__DayTrading_M15.md`](cambios/Estrategia_Build_ConfigInicial_H1_BUY__DayTrading_M15.md)
- `configs/DayTrading/Estrategia_Retest_ConfigInicial_H1_BUY__DayTrading_M15.cfx` — tabla completa de cambios: [`docs/cambios/Estrategia_Retest_ConfigInicial_H1_BUY__DayTrading_M15.md`](cambios/Estrategia_Retest_ConfigInicial_H1_BUY__DayTrading_M15.md)
- `configs/DayTrading/Ventaja_Build_ConfigInicial_H1_BUY__DayTrading_M15.cfx` — tabla completa de cambios: [`docs/cambios/Ventaja_Build_ConfigInicial_H1_BUY__DayTrading_M15.md`](cambios/Ventaja_Build_ConfigInicial_H1_BUY__DayTrading_M15.md)
- `configs/DayTrading/Ventaja_Retest_ConfigInicial_H1_BUY__DayTrading_M15.cfx` — tabla completa de cambios: [`docs/cambios/Ventaja_Retest_ConfigInicial_H1_BUY__DayTrading_M15.md`](cambios/Ventaja_Retest_ConfigInicial_H1_BUY__DayTrading_M15.md)

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
| Máx. operaciones/día | 0 (sin límite) | 2 | Una ruptura y, como mucho, un reintento. |
| Distancia máx. orden | no | 0.6 % | ≈ 90 pips en GBPJPY: cubre rangos asiáticos amplios. |
| Bloques activos | 146 señales / 29 indicadores / 29 stop-limit | 11 señales / 21 indicadores / 7 stop-limit | El nivel roto es el máximo del rango asiático (HighestInRange 00:00-03:00 → 07:00-10:00, en horas enteras: el rango original 0-2359 con paso 30 generaba horas HHMM inválidas como 0060) y los niveles del día anterior. |
| Gestión monetaria | FixedAmount: riesgo 100 por operación | FixedAmount: riesgo 50 por operación | Riesgo fijo 0.5 % (no compuesto: Ret/DD comparable en el tiempo). |
| Fitness | type="ReturnDDRatio" | Weighted: ReturnDDRatio (peso 2, max), StagnationPct (peso 1, min) | Ret/DD como el original; StagnationPct penaliza meses planos (típico de rupturas intradía en régimen de baja volatilidad). |
| Filtros (Ranking) | AvgBarsInTrade(IS) >= 2; ReturnDDRatio(IS) >= 8; NumberOfTrades(IS) >= 300; WinningPct(IS) >= 40 | NumberOfTrades(IS) >= 500; ReturnDDRatio(IS) >= 5; WinningPct(IS) >= 40; ProfitFactor(IS) >= 1.25; AvgBarsInTrade(IS) >= 2; NetProfit(OOS) > 0; ProfitFactor(OOS) >= 1.1 | Umbrales del estilo + exigencia OOS. |
| Filtro población inicial | ReturnDDRatio(IS) >= 5; AvgBarsInTrade(IS) >= 2; NumberOfTrades(IS) >= 250; WinningPct(IS) >= 35 | ReturnDDRatio(IS) >= 3.12; AvgBarsInTrade(IS) >= 2; NumberOfTrades(IS) >= 415; WinningPct(IS) >= 35 | Misma proporción que el autor (≈60 % Ret/DD, ≈83 % operaciones, -5 puntos de acierto). |
| Motor genético | población 5 × 5 islas, 10 generaciones, cruce 46 %, mutación 35 %, migración 6 % cada 5, reinicio por estancamiento a 30 | población 40 × 4 islas, 40 generaciones, cruce 80 %, mutación 30 %, migración 10 % cada 10, reinicio por estancamiento a 15 | Población y generaciones del original insuficientes para que la evolución actúe (Fase 1 §6). |

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
| Máx. operaciones/día | 0 (sin límite) | 2 | Una ruptura y, como mucho, un reintento. |
| Distancia máx. orden | no | 0.6 % | ≈ 90 pips en GBPJPY: cubre rangos asiáticos amplios. |
| Bloques activos | 146 señales / 29 indicadores / 29 stop-limit | 11 señales / 21 indicadores / 7 stop-limit | El nivel roto es el máximo del rango asiático (HighestInRange 00:00-03:00 → 07:00-10:00, en horas enteras: el rango original 0-2359 con paso 30 generaba horas HHMM inválidas como 0060) y los niveles del día anterior. |
| Gestión monetaria | FixedSize: 1 lote | FixedSize: 1 lote | Sin cambio. |
| Fitness | Weighted: Stagnation (peso 1, min) | Weighted: SQN (peso 2, max), StagnationPct (peso 1, min) | SQN mide la calidad estadística de la entrada; el original optimizaba sólo 'Stagnation', que ignora el beneficio. |
| Filtros (Ranking) | AvgBarsInTrade(IS) >= 2; ReturnDDRatio(IS) >= 4; NumberOfTrades(IS) >= 300; WinningPct(IS) >= 40 | NumberOfTrades(IS) >= 500; ReturnDDRatio(IS) >= 2.5; WinningPct(IS) >= 35; ProfitFactor(IS) >= 1.15; AvgBarsInTrade(IS) >= 2; NetProfit(OOS) > 0 | Umbrales del estilo + exigencia OOS. Test de ventaja: Ret/DD a la mitad y PF ≥1,15. |
| Filtro población inicial | ReturnDDRatio(IS) >= 2; AvgBarsInTrade(IS) >= 2; NumberOfTrades(IS) >= 250; WinningPct(IS) >= 35 | ReturnDDRatio(IS) >= 1.25; AvgBarsInTrade(IS) >= 2; NumberOfTrades(IS) >= 415; WinningPct(IS) >= 30 | Misma proporción que el autor (≈60 % Ret/DD, ≈83 % operaciones, -5 puntos de acierto). |
| Motor genético | población 15 × 5 islas, 10 generaciones, cruce 46 %, mutación 35 %, migración 6 % cada 5, reinicio por estancamiento a 30 | población 40 × 4 islas, 40 generaciones, cruce 80 %, mutación 30 %, migración 10 % cada 10, reinicio por estancamiento a 15 | Población y generaciones del original insuficientes para que la evolución actúe (Fase 1 §6). |

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
| Filtros (Ranking) | (ninguna activa) | NetProfit(OOS) > 0; ProfitFactor(OOS) >= 1.1; ReturnDDRatio(Full) >= 7.5; NumberOfTrades(Full) >= 750; DrawdownPct(Full) <= 20 | El original no filtraba nada (todas use=false) ni borraba fallidas. |
| Mayor precisión | activo; precisión 2 (tick real + spread personalizado); 1 condiciones | activo; precisión 2 (tick real + spread personalizado); 3 condiciones | Se activan también las condiciones de nº de operaciones y DD. |
| Monte Carlo retest | activo; 1000 sims; OHLC ±10 % ATR(14), spread 1-3. Acepta: NetProfit(IS) >= 0 | activo; 300 sims; OHLC ±10 % ATR(14), desliz. 0-0.5, spread 2-4. Acepta: NetProfit(Full) >= 0; DrawdownPct(Full) <= 150% de DrawdownPct[main] | Spread desde el base hasta 2-4x, deslizamiento, percentil 95 (no el peor caso) y control del DD. |
| Monte Carlo manipulación | no; orden de operaciones 'exact', saltar 10 % | activo; orden de operaciones 'resampling', saltar 10 % | Barato; 'resampling' y referencia corregida (el original comparaba MC contra MC). |
| SPP / perfil de optimización | activo; 15000 tests, ±20 %, 6 pasos; ≥95 % rentables | activo; 3000 tests, ±20 %, 6 pasos; ≥85 % rentables | Tests y exigencia ajustados al coste de cómputo y a la sensibilidad del estilo. |
| What-if | no; ExcludePctTradesWithBiggestPl, ExcludePctTradesWithLowestPl | activo; ExcludePctTradesWithBiggestPl, ExcludePctTradesWithLowestPl | Quitar el 5 % de extremos: el estilo no debe depender de outliers. |

Diferencias del `Ventaja_Retest` respecto al anterior:

- **Gestión monetaria:** FixedSize: 1 lote
- **Fitness:** Weighted: SQN (peso 2, max), StagnationPct (peso 1, min)
- **Filtros (Ranking):** NetProfit(OOS) > 0; ProfitFactor(Full) >= 1.1; NumberOfTrades(Full) >= 750

### 3. Indicadores y bloques seleccionados

Criterio general: El nivel roto es el máximo del rango asiático (HighestInRange 00:00-03:00 → 07:00-10:00, en horas enteras: el rango original 0-2359 con paso 30 generaba horas HHMM inválidas como 0060) y los niveles del día anterior. El original activaba 146 señales + 29 indicadores + 29 niveles stop/limit genéricos con peso 1; aquí sólo los coherentes con la tesis, con peso mayor en los centrales (w2-w3).

| Bloque | Peso | Familia | Qué mide | Por qué en este estilo | Rango específico |
|---|---|---|---|---|---|
| `BarOpensAboveHighestAfterOpenBelow` | 2 | Ruptura de nivel | La vela abre por encima del máximo de N velas tras abrir por debajo (ruptura Donchian confirmada en apertura). | Rupturas de canal confirmadas en apertura. | global del estilo |
| `BBBarOpensAboveUpAfterOpenBelow` | 1 | Ruptura de nivel | Cruce de apertura por encima de la banda superior de Bollinger. | Rupturas de canal confirmadas en apertura. | global del estilo |
| `KCBarOpensAboveUpperAfterOpenBelow` | 1 | Ruptura de nivel | Cruce de apertura por encima de la banda superior de Keltner (ATR). | Rupturas de canal confirmadas en apertura. | global del estilo |
| `ADXHigher` | 1 | Tendencia | ADX por encima de un nivel: tendencia con fuerza. | Sesgo direccional intradía (ADX, pendientes). | Level 20 a 40 (paso 5) |
| `ADXRising` | 1 | Tendencia | ADX creciente: la tendencia gana fuerza. | Sesgo direccional intradía (ADX, pendientes). | global del estilo |
| `Indicators.EMA` | 1 | Tendencia | Media exponencial. | Sesgo direccional intradía (ADX, pendientes). | global del estilo |
| `LinRegRising` | 1 | Tendencia | Regresión lineal con pendiente positiva. | Sesgo direccional intradía (ADX, pendientes). | global del estilo |
| `MABarClosesAbove` | 1 | Tendencia | Cierre por encima de una media móvil. | Sesgo direccional intradía (ADX, pendientes). | global del estilo |
| `MARising` | 1 | Tendencia | Media móvil con pendiente positiva. | Sesgo direccional intradía (ADX, pendientes). | global del estilo |
| `ATRRising` | 1 | Volatilidad | ATR creciente: expansión de volatilidad (sin nivel absoluto). | La ruptura necesita expansión. | global del estilo |
| `Indicators.ATR` | 1 | Volatilidad | ATR: rango medio verdadero. | La ruptura necesita expansión. | global del estilo |
| `BarHourIsBigger` | 1 | Tiempo | Hora de la vela posterior a H. | Permiten al Builder acotar la franja de entrada dentro de la ventana global. | Hour 8 a 12 (paso 1) |
| `BarHourIsSmaller` | 1 | Tiempo | Hora de la vela anterior a H. | Permiten al Builder acotar la franja de entrada dentro de la ventana global. | Hour 12 a 19 (paso 1) |
| `Indicators.HighestInRange` | 3 | Nivel de referencia | Máximo entre dos horas del día (rango horario, p. ej. asiático). | Rango asiático, niveles del día anterior y aperturas de sesión: los niveles clásicos intradía. | Time From 0 a 300 (paso 100); Time To 700 a 1000 (paso 100) |
| `Indicators.LowestInRange` | 2 | Nivel de referencia | Mínimo entre dos horas del día. | Rango asiático, niveles del día anterior y aperturas de sesión: los niveles clásicos intradía. | Time From 0 a 300 (paso 100); Time To 700 a 1000 (paso 100) |
| `Prices.SessionHigh` | 2 | Nivel de referencia | Máximo de una sesión horaria configurable. | Rango asiático, niveles del día anterior y aperturas de sesión: los niveles clásicos intradía. | Start Hours 1 a 3 (paso 1); Start Minutes 0 a 0 (paso 1); End Hours 8 a 10 (paso 1); End Minutes 0 a 0 (paso 1) |
| `Indicators.Highest` | 1 | Nivel de referencia | Máximo de N velas (canal Donchian). | Rango asiático, niveles del día anterior y aperturas de sesión: los niveles clásicos intradía. | global del estilo |
| `Indicators.Lowest` | 1 | Nivel de referencia | Mínimo de N velas. | Rango asiático, niveles del día anterior y aperturas de sesión: los niveles clásicos intradía. | global del estilo |
| `Prices.CloseD` | 1 | Nivel de referencia | Cierre del día anterior. | Rango asiático, niveles del día anterior y aperturas de sesión: los niveles clásicos intradía. | global del estilo |
| `Prices.HighD` | 1 | Nivel de referencia | Máximo del día anterior. | Rango asiático, niveles del día anterior y aperturas de sesión: los niveles clásicos intradía. | global del estilo |
| `Prices.LowD` | 1 | Nivel de referencia | Mínimo del día anterior. | Rango asiático, niveles del día anterior y aperturas de sesión: los niveles clásicos intradía. | global del estilo |
| `Prices.OpenD` | 1 | Nivel de referencia | Apertura diaria. | Rango asiático, niveles del día anterior y aperturas de sesión: los niveles clásicos intradía. | global del estilo |
| `Prices.SessionLow` | 1 | Nivel de referencia | Mínimo de una sesión horaria configurable. | Rango asiático, niveles del día anterior y aperturas de sesión: los niveles clásicos intradía. | Start Hours 1 a 3 (paso 1); Start Minutes 0 a 0 (paso 1); End Hours 8 a 10 (paso 1); End Minutes 0 a 0 (paso 1) |
| `Prices.SessionOpen` | 1 | Nivel de referencia | Apertura de una sesión horaria configurable. | Rango asiático, niveles del día anterior y aperturas de sesión: los niveles clásicos intradía. | Start Hours 9 a 10 (paso 1); Start Minutes 0 a 0 (paso 1) |
| `Prices.Close` | 1 | Precio | Cierre. | Comparaciones con los niveles. | global del estilo |
| `Prices.High` | 1 | Precio | Máximo. | Comparaciones con los niveles. | global del estilo |
| `Prices.Low` | 1 | Precio | Mínimo. | Comparaciones con los niveles. | global del estilo |
| `Prices.Open` | 1 | Precio | Apertura. | Comparaciones con los niveles. | global del estilo |
| `CrossesAbove` | 1 | Comparador | A cruza B al alza. | Construyen las condiciones de ruptura. | global del estilo |
| `CrossesBelow` | 1 | Comparador | A cruza B a la baja. | Construyen las condiciones de ruptura. | global del estilo |
| `IsGreater` | 1 | Comparador | A > B. | Construyen las condiciones de ruptura. | global del estilo |
| `IsLower` | 1 | Comparador | A < B. | Construyen las condiciones de ruptura. | global del estilo |
| `Stop/Limit Price Levels.HighestInRange` | 3 | Precio de orden stop/limit | Precio = máximo de un rango horario. | Orden stop en el extremo del rango asiático/día anterior. | Time From 0 a 300 (paso 100); Time To 700 a 1000 (paso 100) |
| `Stop/Limit Price Levels.SessionHigh` | 2 | Precio de orden stop/limit | Precio = máximo de sesión. | Orden stop en el extremo del rango asiático/día anterior. | Start Hours 1 a 3 (paso 1); Start Minutes 0 a 0 (paso 1); End Hours 8 a 10 (paso 1); End Minutes 0 a 0 (paso 1) |
| `Stop/Limit Price Levels.HighD` | 1 | Precio de orden stop/limit | Precio = máximo del día anterior. | Orden stop en el extremo del rango asiático/día anterior. | global del estilo |
| `Stop/Limit Price Levels.Highest` | 1 | Precio de orden stop/limit | Precio de la orden = máximo de N velas. | Orden stop en el extremo del rango asiático/día anterior. | global del estilo |
| `Stop/Limit Price Levels.OpenD` | 1 | Precio de orden stop/limit | Precio = apertura diaria. | Orden stop en el extremo del rango asiático/día anterior. | global del estilo |
| `Stop/Limit Price Ranges.ATR` | 2 | Desplazamiento de orden | Desplazamiento del precio de la orden = k·ATR. | Margen sobre el nivel. | global del estilo |
| `Stop/Limit Price Ranges.BarRange` | 1 | Desplazamiento de orden | Desplazamiento = k·rango de la vela. | Margen sobre el nivel. | global del estilo |

### 4. Timeframe, símbolos y horarios

- **Timeframe:** M15.
- **Instrumento recomendado:** GBPUSD/GBPJPY/EURJPY (rango asiático + apertura de Londres) o DAX/US30 con su apertura de contado. GBPJPY es razonable aquí.
- **Horario:** Rango asiático: inicio entre 00:00 y 03:00, fin entre 07:00 y 10:00 (horas enteras). Entradas 09:00-19:00 servidor; cierre de todo a las 22:30 (viernes 21:30); máximo 2 operaciones/día.

### 5. Salidas y gestión del riesgo

SL 1-2,5 ATR(14-60) de M15; objetivo opcional 1,5-4 ATR (50 %); trailing 1,5-3 ATR (30 %); break-even 1-2 ATR (30 %); regla de salida (30 %); cierre de fin de día siempre. Riesgo 0,5 %.

### 6. Filtros y ranking

| Archivo | Fitness | Filtros |
|---|---|---|
| `Estrategia_Build_ConfigInicial_H1_BUY__DayTrading_M15` | Weighted: ReturnDDRatio (peso 2, max), StagnationPct (peso 1, min) | NumberOfTrades(IS) >= 500; ReturnDDRatio(IS) >= 5; WinningPct(IS) >= 40; ProfitFactor(IS) >= 1.25; AvgBarsInTrade(IS) >= 2; NetProfit(OOS) > 0; ProfitFactor(OOS) >= 1.1 |
| `Estrategia_Retest_ConfigInicial_H1_BUY__DayTrading_M15` | Weighted: ReturnDDRatio (peso 2, max), StagnationPct (peso 1, min) | NetProfit(OOS) > 0; ProfitFactor(OOS) >= 1.1; ReturnDDRatio(Full) >= 7.5; NumberOfTrades(Full) >= 750; DrawdownPct(Full) <= 20 |
| `Ventaja_Build_ConfigInicial_H1_BUY__DayTrading_M15` | Weighted: SQN (peso 2, max), StagnationPct (peso 1, min) | NumberOfTrades(IS) >= 500; ReturnDDRatio(IS) >= 2.5; WinningPct(IS) >= 35; ProfitFactor(IS) >= 1.15; AvgBarsInTrade(IS) >= 2; NetProfit(OOS) > 0 |
| `Ventaja_Retest_ConfigInicial_H1_BUY__DayTrading_M15` | Weighted: SQN (peso 2, max), StagnationPct (peso 1, min) | NetProfit(OOS) > 0; ProfitFactor(Full) >= 1.1; NumberOfTrades(Full) >= 750 |

Justificación: Ret/DD como el original; StagnationPct penaliza meses planos (típico de rupturas intradía en régimen de baja volatilidad). Los umbrales reflejan la frecuencia y el acierto típicos del estilo (no se usa el 40 % de acierto ni las 300 operaciones del original para todos).

### 7. Motor y robustez

- **Builder:** población 40 × 4 islas, 40 generaciones, cruce 80 %, mutación 30 %, migración 10 % cada 10, reinicio por estancamiento a 15.
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

**Archivos del kit** (todos *no validados en SQX*):

- `configs/Swing/Estrategia_Build_ConfigInicial_H1_BUY__Swing_H4.cfx` — tabla completa de cambios: [`docs/cambios/Estrategia_Build_ConfigInicial_H1_BUY__Swing_H4.md`](cambios/Estrategia_Build_ConfigInicial_H1_BUY__Swing_H4.md)
- `configs/Swing/Estrategia_Retest_ConfigInicial_H1_BUY__Swing_H4.cfx` — tabla completa de cambios: [`docs/cambios/Estrategia_Retest_ConfigInicial_H1_BUY__Swing_H4.md`](cambios/Estrategia_Retest_ConfigInicial_H1_BUY__Swing_H4.md)
- `configs/Swing/Ventaja_Build_ConfigInicial_H1_BUY__Swing_H4.cfx` — tabla completa de cambios: [`docs/cambios/Ventaja_Build_ConfigInicial_H1_BUY__Swing_H4.md`](cambios/Ventaja_Build_ConfigInicial_H1_BUY__Swing_H4.md)
- `configs/Swing/Ventaja_Retest_ConfigInicial_H1_BUY__Swing_H4.cfx` — tabla completa de cambios: [`docs/cambios/Ventaja_Retest_ConfigInicial_H1_BUY__Swing_H4.md`](cambios/Ventaja_Retest_ConfigInicial_H1_BUY__Swing_H4.md)

### 1. Tesis

Tras una contracción de volatilidad de varios días, la ruptura del rango tiende a continuar durante 2-10 días en la dirección del régimen de fondo. Se mantiene la posición noches y fines de semana.

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
| Tipos de orden | EnterAtMarket (w1) | EnterAtMarket (w1), EnterAtStop (w2, válida 2-6 velas) | Stop válida 8-24 h. |
| Stop loss | obligatorio=true; 1-3 × ATR(20-100) | obligatorio=true; 1.5-3.5 × ATR(14-100) | Stop amplio en ATR, objetivo y trailing opcionales, salida temporal 2-7 días. |
| Profit target | obligatorio=true; 2-5 × ATR(20-100); PT=100-500 % del SL | obligatorio=false; 2-6 × ATR(14-100) | Stop amplio en ATR, objetivo y trailing opcionales, salida temporal 2-7 días. |
| Trailing stop | sí (50 %), fijo 50-100 pips, 1-5 ATR | sí (50 %), 2-4 ATR | Stop amplio en ATR, objetivo y trailing opcionales, salida temporal 2-7 días. |
| Break-even | no | sí (30 %), 1-2 ATR | Stop amplio en ATR, objetivo y trailing opcionales, salida temporal 2-7 días. |
| Salida temporal | no | sí (30 %), 10-40 velas | Stop amplio en ATR, objetivo y trailing opcionales, salida temporal 2-7 días. |
| Salida por regla | no | sí (30 %) | Stop amplio en ATR, objetivo y trailing opcionales, salida temporal 2-7 días. |
| Ventana de señales | 01:30-23:30 | sin ventana | En H4 la ventana 01:30-23:30 excluiría la vela de las 00:00 (1/6 de las señales) sin motivo de estilo. |
| Cierres forzados | no diario; no viernes | no diario; no viernes | Sin cambio. |
| Máx. operaciones/día | 0 (sin límite) | 1 | Swing: como mucho una entrada diaria. |
| Distancia máx. orden | no | 2 % | 2 %: holgura para rupturas de rangos de varios días. |
| Bloques activos | 146 señales / 29 indicadores / 29 stop-limit | 14 señales / 20 indicadores / 9 stop-limit | Ruptura de máximos de N días (Donchian/Bollinger/Keltner/Kumo) filtrada por régimen (ADX, pendiente de medias, eficiencia de Kaufman). |
| Gestión monetaria | FixedAmount: riesgo 100 por operación | FixedAmount: riesgo 100 por operación | Sin cambio. |
| Fitness | type="ReturnDDRatio" | Weighted: ReturnDDRatio (peso 2, max), Stability (peso 1, max) | Ret/DD + estabilidad de la curva: un swing con 30 operaciones/año necesita curvas regulares. |
| Filtros (Ranking) | AvgBarsInTrade(IS) >= 2; ReturnDDRatio(IS) >= 8; NumberOfTrades(IS) >= 300; WinningPct(IS) >= 40 | NumberOfTrades(IS) >= 150; ReturnDDRatio(IS) >= 4; WinningPct(IS) >= 38; ProfitFactor(IS) >= 1.3; AvgBarsInTrade(IS) >= 3; NetProfit(OOS) > 0; ProfitFactor(OOS) >= 1.1 | Umbrales del estilo + exigencia OOS. |
| Filtro población inicial | ReturnDDRatio(IS) >= 5; AvgBarsInTrade(IS) >= 2; NumberOfTrades(IS) >= 250; WinningPct(IS) >= 35 | ReturnDDRatio(IS) >= 2.5; AvgBarsInTrade(IS) >= 3; NumberOfTrades(IS) >= 124; WinningPct(IS) >= 33 | Misma proporción que el autor (≈60 % Ret/DD, ≈83 % operaciones, -5 puntos de acierto). |
| Motor genético | población 5 × 5 islas, 10 generaciones, cruce 46 %, mutación 35 %, migración 6 % cada 5, reinicio por estancamiento a 30 | población 50 × 4 islas, 40 generaciones, cruce 80 %, mutación 30 %, migración 10 % cada 10, reinicio por estancamiento a 15 | Población y generaciones del original insuficientes para que la evolución actúe (Fase 1 §6). |

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
| Tipos de orden | EnterAtMarket (w1) | EnterAtMarket (w1), EnterAtStop (w2, válida 2-6 velas) | Stop válida 8-24 h. |
| Stop loss | obligatorio=false; sin ATR | obligatorio=false; sin ATR | Sin cambio. |
| Profit target | obligatorio=false; sin ATR | obligatorio=false; sin ATR | Sin cambio. |
| Trailing stop | no | no | Sin cambio. |
| Break-even | no | no | Sin cambio. |
| Salida temporal | sí (50 %), 2-15 velas | sí (100 %), 6-30 velas | Test de ventaja: salida por tiempo 1-5 días. |
| Salida por regla | no | no | Sin cambio. |
| Ventana de señales | 01:30-23:30 | sin ventana | En H4 la ventana 01:30-23:30 excluiría la vela de las 00:00 (1/6 de las señales) sin motivo de estilo. |
| Cierres forzados | no diario; no viernes | no diario; no viernes | Sin cambio. |
| Máx. operaciones/día | 0 (sin límite) | 1 | Swing: como mucho una entrada diaria. |
| Distancia máx. orden | no | 2 % | 2 %: holgura para rupturas de rangos de varios días. |
| Bloques activos | 146 señales / 29 indicadores / 29 stop-limit | 14 señales / 20 indicadores / 9 stop-limit | Ruptura de máximos de N días (Donchian/Bollinger/Keltner/Kumo) filtrada por régimen (ADX, pendiente de medias, eficiencia de Kaufman). |
| Gestión monetaria | FixedSize: 1 lote | FixedSize: 1 lote | Sin cambio. |
| Fitness | Weighted: Stagnation (peso 1, min) | Weighted: SQN (peso 2, max), StagnationPct (peso 1, min) | SQN mide la calidad estadística de la entrada; el original optimizaba sólo 'Stagnation', que ignora el beneficio. |
| Filtros (Ranking) | AvgBarsInTrade(IS) >= 2; ReturnDDRatio(IS) >= 4; NumberOfTrades(IS) >= 300; WinningPct(IS) >= 40 | NumberOfTrades(IS) >= 150; ReturnDDRatio(IS) >= 2; WinningPct(IS) >= 33; ProfitFactor(IS) >= 1.15; AvgBarsInTrade(IS) >= 3; NetProfit(OOS) > 0 | Umbrales del estilo + exigencia OOS. Test de ventaja: Ret/DD a la mitad y PF ≥1,15. |
| Filtro población inicial | ReturnDDRatio(IS) >= 2; AvgBarsInTrade(IS) >= 2; NumberOfTrades(IS) >= 250; WinningPct(IS) >= 35 | ReturnDDRatio(IS) >= 1; AvgBarsInTrade(IS) >= 3; NumberOfTrades(IS) >= 124; WinningPct(IS) >= 28 | Misma proporción que el autor (≈60 % Ret/DD, ≈83 % operaciones, -5 puntos de acierto). |
| Motor genético | población 15 × 5 islas, 10 generaciones, cruce 46 %, mutación 35 %, migración 6 % cada 5, reinicio por estancamiento a 30 | población 50 × 4 islas, 40 generaciones, cruce 80 %, mutación 30 %, migración 10 % cada 10, reinicio por estancamiento a 15 | Población y generaciones del original insuficientes para que la evolución actúe (Fase 1 §6). |

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
| Filtros (Ranking) | (ninguna activa) | NetProfit(OOS) > 0; ProfitFactor(OOS) >= 1.1; ReturnDDRatio(Full) >= 6; NumberOfTrades(Full) >= 225; DrawdownPct(Full) <= 20 | El original no filtraba nada (todas use=false) ni borraba fallidas. |
| Mayor precisión | activo; precisión 2 (tick real + spread personalizado); 1 condiciones | activo; precisión 2 (tick real + spread personalizado); 3 condiciones | Se activan también las condiciones de nº de operaciones y DD. |
| Monte Carlo retest | activo; 1000 sims; OHLC ±10 % ATR(14), spread 1-3. Acepta: NetProfit(IS) >= 0 | activo; 500 sims; OHLC ±10 % ATR(14), desliz. 0-0.5, spread 2-4, vela de inicio. Acepta: NetProfit(Full) >= 0; DrawdownPct(Full) <= 150% de DrawdownPct[main] | Spread desde el base hasta 2-4x, deslizamiento, percentil 95 (no el peor caso) y control del DD. |
| Monte Carlo manipulación | no; orden de operaciones 'exact', saltar 10 % | activo; orden de operaciones 'resampling', saltar 10 % | Barato; 'resampling' y referencia corregida (el original comparaba MC contra MC). |
| SPP / perfil de optimización | activo; 15000 tests, ±20 %, 6 pasos; ≥95 % rentables | activo; 5000 tests, ±20 %, 6 pasos; ≥85 % rentables | Tests y exigencia ajustados al coste de cómputo y a la sensibilidad del estilo. |
| What-if | no; ExcludePctTradesWithBiggestPl, ExcludePctTradesWithLowestPl | activo; ExcludeTradesWithBiggestPl, ExcludeTradesWithLowestPl | Quitar 2 mejores/peores (estilos de outliers). |

Diferencias del `Ventaja_Retest` respecto al anterior:

- **Gestión monetaria:** FixedSize: 1 lote
- **Fitness:** Weighted: SQN (peso 2, max), StagnationPct (peso 1, min)
- **Filtros (Ranking):** NetProfit(OOS) > 0; ProfitFactor(Full) >= 1.1; NumberOfTrades(Full) >= 225

### 3. Indicadores y bloques seleccionados

Criterio general: Ruptura de máximos de N días (Donchian/Bollinger/Keltner/Kumo) filtrada por régimen (ADX, pendiente de medias, eficiencia de Kaufman). El original activaba 146 señales + 29 indicadores + 29 niveles stop/limit genéricos con peso 1; aquí sólo los coherentes con la tesis, con peso mayor en los centrales (w2-w3).

| Bloque | Peso | Familia | Qué mide | Por qué en este estilo | Rango específico |
|---|---|---|---|---|---|
| `BarOpensAboveHighestAfterOpenBelow` | 3 | Ruptura de nivel | La vela abre por encima del máximo de N velas tras abrir por debajo (ruptura Donchian confirmada en apertura). | Ruptura de consolidaciones de varios días. | global del estilo |
| `BBBarOpensAboveUpAfterOpenBelow` | 1 | Ruptura de nivel | Cruce de apertura por encima de la banda superior de Bollinger. | Ruptura de consolidaciones de varios días. | global del estilo |
| `IchimokuKumoBreakoutBullish` | 1 | Ruptura de nivel | El precio sale por encima de la nube de Ichimoku. | Ruptura de consolidaciones de varios días. | global del estilo |
| `KCBarOpensAboveUpperAfterOpenBelow` | 1 | Ruptura de nivel | Cruce de apertura por encima de la banda superior de Keltner (ATR). | Ruptura de consolidaciones de varios días. | global del estilo |
| `RSIHigher` | 1 | Momentum | RSI por encima de un nivel (fuerza relativa). | Fuerza relativa (RSI > 50-70) como confirmación, no como sobrecompra. | Level 50 a 70 (paso 5) |
| `ADXHigher` | 1 | Tendencia | ADX por encima de un nivel: tendencia con fuerza. | El swing a favor del régimen de fondo tiene más recorrido. | Level 20 a 40 (paso 5) |
| `ADXRising` | 1 | Tendencia | ADX creciente: la tendencia gana fuerza. | El swing a favor del régimen de fondo tiene más recorrido. | global del estilo |
| `Indicators.EMA` | 1 | Tendencia | Media exponencial. | El swing a favor del régimen de fondo tiene más recorrido. | global del estilo |
| `Indicators.SMA` | 1 | Tendencia | Media simple. | El swing a favor del régimen de fondo tiene más recorrido. | global del estilo |
| `KERaboveLevel` | 1 | Tendencia | Ratio de eficiencia de Kaufman alto: movimiento direccional limpio. | El swing a favor del régimen de fondo tiene más recorrido. | Level 0.2 a 0.6 (paso 0.05) |
| `LinRegRising` | 1 | Tendencia | Regresión lineal con pendiente positiva. | El swing a favor del régimen de fondo tiene más recorrido. | global del estilo |
| `MABarClosesAbove` | 1 | Tendencia | Cierre por encima de una media móvil. | El swing a favor del régimen de fondo tiene más recorrido. | global del estilo |
| `MARising` | 1 | Tendencia | Media móvil con pendiente positiva. | El swing a favor del régimen de fondo tiene más recorrido. | global del estilo |
| `SuperTrendUPTrend` | 1 | Tendencia | SuperTrend en modo alcista. | El swing a favor del régimen de fondo tiene más recorrido. | global del estilo |
| `ATRRising` | 1 | Volatilidad | ATR creciente: expansión de volatilidad (sin nivel absoluto). | Contracción → expansión. | global del estilo |
| `BBUpperRising` | 1 | Volatilidad | Banda superior de Bollinger subiendo (expansión). | Contracción → expansión. | global del estilo |
| `Indicators.ATR` | 1 | Volatilidad | ATR: rango medio verdadero. | Contracción → expansión. | global del estilo |
| `Indicators.Highest` | 2 | Nivel de referencia | Máximo de N velas (canal Donchian). | Máximos de N velas, del día y de la semana. | global del estilo |
| `Indicators.BollingerBands` | 1 | Nivel de referencia | Bandas de Bollinger (media ± k·desviación). | Máximos de N velas, del día y de la semana. | global del estilo |
| `Indicators.KeltnerChannel` | 1 | Nivel de referencia | Canal de Keltner (media ± k·ATR). | Máximos de N velas, del día y de la semana. | global del estilo |
| `Indicators.Lowest` | 1 | Nivel de referencia | Mínimo de N velas. | Máximos de N velas, del día y de la semana. | global del estilo |
| `Prices.HighD` | 1 | Nivel de referencia | Máximo del día anterior. | Máximos de N velas, del día y de la semana. | global del estilo |
| `Prices.HighW` | 1 | Nivel de referencia | Máximo semanal. | Máximos de N velas, del día y de la semana. | global del estilo |
| `Prices.LowD` | 1 | Nivel de referencia | Mínimo del día anterior. | Máximos de N velas, del día y de la semana. | global del estilo |
| `Prices.LowW` | 1 | Nivel de referencia | Mínimo semanal. | Máximos de N velas, del día y de la semana. | global del estilo |
| `Prices.Close` | 1 | Precio | Cierre. | Comparaciones con niveles. | global del estilo |
| `Prices.High` | 1 | Precio | Máximo. | Comparaciones con niveles. | global del estilo |
| `Prices.Low` | 1 | Precio | Mínimo. | Comparaciones con niveles. | global del estilo |
| `Prices.Open` | 1 | Precio | Apertura. | Comparaciones con niveles. | global del estilo |
| `CrossesAbove` | 1 | Comparador | A cruza B al alza. | Incluye 'N velas seguidas por encima' (persistencia). | global del estilo |
| `CrossesBelow` | 1 | Comparador | A cruza B a la baja. | Incluye 'N velas seguidas por encima' (persistencia). | global del estilo |
| `IsGreater` | 1 | Comparador | A > B. | Incluye 'N velas seguidas por encima' (persistencia). | global del estilo |
| `IsGreaterCount` | 1 | Comparador | A > B durante N velas seguidas. | Incluye 'N velas seguidas por encima' (persistencia). | global del estilo |
| `IsLower` | 1 | Comparador | A < B. | Incluye 'N velas seguidas por encima' (persistencia). | global del estilo |
| `Stop/Limit Price Levels.Highest` | 3 | Precio de orden stop/limit | Precio de la orden = máximo de N velas. | Stop sobre el máximo de la consolidación. | global del estilo |
| `Stop/Limit Price Levels.BollingerBands` | 1 | Precio de orden stop/limit | Precio = banda de Bollinger. | Stop sobre el máximo de la consolidación. | global del estilo |
| `Stop/Limit Price Levels.High` | 1 | Precio de orden stop/limit | Precio de la orden = máximo de una vela (vela señal). | Stop sobre el máximo de la consolidación. | global del estilo |
| `Stop/Limit Price Levels.HighD` | 1 | Precio de orden stop/limit | Precio = máximo del día anterior. | Stop sobre el máximo de la consolidación. | global del estilo |
| `Stop/Limit Price Levels.HighW` | 1 | Precio de orden stop/limit | Precio = máximo semanal. | Stop sobre el máximo de la consolidación. | global del estilo |
| `Stop/Limit Price Levels.KeltnerChannel` | 1 | Precio de orden stop/limit | Precio = banda de Keltner. | Stop sobre el máximo de la consolidación. | global del estilo |
| `Stop/Limit Price Ranges.ATR` | 2 | Desplazamiento de orden | Desplazamiento del precio de la orden = k·ATR. | Margen proporcional a la volatilidad. | global del estilo |
| `Stop/Limit Price Ranges.BBRange` | 1 | Desplazamiento de orden | Desplazamiento = k·anchura de Bollinger. | Margen proporcional a la volatilidad. | global del estilo |
| `Stop/Limit Price Ranges.BarRange` | 1 | Desplazamiento de orden | Desplazamiento = k·rango de la vela. | Margen proporcional a la volatilidad. | global del estilo |

### 4. Timeframe, símbolos y horarios

- **Timeframe:** H4.
- **Instrumento recomendado:** Pares mayores y cruces líquidos, índices (US30/DAX) y oro. GBPJPY apto (swap relevante: comprobar).
- **Horario:** H4 sin filtro horario (en H4 la ventana 01:30-23:30 del original eliminaría la vela de las 00:00). Mantiene posiciones de noche y fin de semana (`RealisticGapsHandling` = true se conserva para simular gaps).

### 5. Salidas y gestión del riesgo

SL 1,5-3,5 ATR(14-100) de H4; objetivo opcional 2-6 ATR; trailing 2-4 ATR (50 %); break-even (30 %); salida temporal 10-40 velas = 2-7 días (30 %). Riesgo 1 %; 1 entrada/día.

### 6. Filtros y ranking

| Archivo | Fitness | Filtros |
|---|---|---|
| `Estrategia_Build_ConfigInicial_H1_BUY__Swing_H4` | Weighted: ReturnDDRatio (peso 2, max), Stability (peso 1, max) | NumberOfTrades(IS) >= 150; ReturnDDRatio(IS) >= 4; WinningPct(IS) >= 38; ProfitFactor(IS) >= 1.3; AvgBarsInTrade(IS) >= 3; NetProfit(OOS) > 0; ProfitFactor(OOS) >= 1.1 |
| `Estrategia_Retest_ConfigInicial_H1_BUY__Swing_H4` | Weighted: ReturnDDRatio (peso 2, max), Stability (peso 1, max) | NetProfit(OOS) > 0; ProfitFactor(OOS) >= 1.1; ReturnDDRatio(Full) >= 6; NumberOfTrades(Full) >= 225; DrawdownPct(Full) <= 20 |
| `Ventaja_Build_ConfigInicial_H1_BUY__Swing_H4` | Weighted: SQN (peso 2, max), StagnationPct (peso 1, min) | NumberOfTrades(IS) >= 150; ReturnDDRatio(IS) >= 2; WinningPct(IS) >= 33; ProfitFactor(IS) >= 1.15; AvgBarsInTrade(IS) >= 3; NetProfit(OOS) > 0 |
| `Ventaja_Retest_ConfigInicial_H1_BUY__Swing_H4` | Weighted: SQN (peso 2, max), StagnationPct (peso 1, min) | NetProfit(OOS) > 0; ProfitFactor(Full) >= 1.1; NumberOfTrades(Full) >= 225 |

Justificación: Ret/DD + estabilidad de la curva: un swing con 30 operaciones/año necesita curvas regulares. Los umbrales reflejan la frecuencia y el acierto típicos del estilo (no se usa el 40 % de acierto ni las 300 operaciones del original para todos).

### 7. Motor y robustez

- **Builder:** población 50 × 4 islas, 40 generaciones, cruce 80 %, mutación 30 %, migración 10 % cada 10, reinicio por estancamiento a 15.
- **Retest:** activo; precisión 2 (tick real + spread personalizado); 3 condiciones. Se añade aleatorizar la vela de inicio: con pocas operaciones el punto de arranque importa.
- **Monte Carlo:** activo; 500 sims; OHLC ±10 % ATR(14), desliz. 0-0.5, spread 2-4, vela de inicio. Acepta: NetProfit(Full) >= 0; DrawdownPct(Full) <= 150% de DrawdownPct[main].
- **Manipulación MC:** activo; orden de operaciones 'resampling', saltar 10 %.
- **SPP:** activo; 5000 tests, ±20 %, 6 pasos; ≥85 % rentables.
- **What-if:** activo; ExcludeTradesWithBiggestPl, ExcludeTradesWithLowestPl.

### 8. Riesgos conocidos, sobreoptimización y mitigación

Riesgos propios del estilo: Gaps de fin de semana; swap; pocas operaciones por año → estadística débil.

1. ~30 operaciones/año: la significación estadística es limitada. Mitigación: Stability en la fitness, OOS 2019-2020, holdout 2021-2024 y validación multi-mercado.
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

**Position Trading (momentum de largo plazo)** · timeframe `D1`

**Archivos del kit** (todos *no validados en SQX*):

- `configs/Position/Estrategia_Build_ConfigInicial_H1_BUY__Position_D1.cfx` — tabla completa de cambios: [`docs/cambios/Estrategia_Build_ConfigInicial_H1_BUY__Position_D1.md`](cambios/Estrategia_Build_ConfigInicial_H1_BUY__Position_D1.md)
- `configs/Position/Estrategia_Retest_ConfigInicial_H1_BUY__Position_D1.cfx` — tabla completa de cambios: [`docs/cambios/Estrategia_Retest_ConfigInicial_H1_BUY__Position_D1.md`](cambios/Estrategia_Retest_ConfigInicial_H1_BUY__Position_D1.md)
- `configs/Position/Ventaja_Build_ConfigInicial_H1_BUY__Position_D1.cfx` — tabla completa de cambios: [`docs/cambios/Ventaja_Build_ConfigInicial_H1_BUY__Position_D1.md`](cambios/Ventaja_Build_ConfigInicial_H1_BUY__Position_D1.md)
- `configs/Position/Ventaja_Retest_ConfigInicial_H1_BUY__Position_D1.cfx` — tabla completa de cambios: [`docs/cambios/Ventaja_Retest_ConfigInicial_H1_BUY__Position_D1.md`](cambios/Ventaja_Retest_ConfigInicial_H1_BUY__Position_D1.md)

### 1. Tesis

El momentum de series temporales a 3-12 meses (rupturas de máximos de largo plazo y pendiente de medias largas) es una de las anomalías más documentadas; se captura con pocas operaciones, stops amplios y sin objetivo fijo.

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
| Periodos de indicadores | 4–200 | 20–250 | 20-250 días (1 mes-1 año). Máximo 2 condiciones: con ~8 operaciones/año cada grado de libertad extra es sobreajuste casi seguro. |
| Desplazamiento (shift) | 1–1 | 1–1 | Sin cambio. |
| Tipos de salida (mín–máx) | 1–5 | 1–3 | SL obligatorio + salidas propias del estilo (el original pedía hasta 5 con 3 disponibles). |
| Tipos de orden | EnterAtMarket (w1) | EnterAtMarket (w2), EnterAtStop (w1, válida 1-5 velas) | Mayoritariamente a mercado; stop opcional válido 1-5 días. |
| Stop loss | obligatorio=true; 1-3 × ATR(20-100) | obligatorio=true; 2.5-6 × ATR(20-100) | Sin objetivo (dejar correr); trailing de 3-6 ATR como salida principal; salida por regla (p. ej. cierre bajo media) y temporal 3-12 meses. |
| Profit target | obligatorio=true; 2-5 × ATR(20-100); PT=100-500 % del SL | obligatorio=false; 6-12 × ATR(20-100) | Sin objetivo (dejar correr); trailing de 3-6 ATR como salida principal; salida por regla (p. ej. cierre bajo media) y temporal 3-12 meses. |
| Trailing stop | sí (50 %), fijo 50-100 pips, 1-5 ATR | sí (70 %), 3-6 ATR | Sin objetivo (dejar correr); trailing de 3-6 ATR como salida principal; salida por regla (p. ej. cierre bajo media) y temporal 3-12 meses. |
| Break-even | no | no | Sin cambio. |
| Salida temporal | no | sí (30 %), 60-250 velas | Sin objetivo (dejar correr); trailing de 3-6 ATR como salida principal; salida por regla (p. ej. cierre bajo media) y temporal 3-12 meses. |
| Salida por regla | no | sí (50 %) | Sin objetivo (dejar correr); trailing de 3-6 ATR como salida principal; salida por regla (p. ej. cierre bajo media) y temporal 3-12 meses. |
| Ventana de señales | 01:30-23:30 | sin ventana | Con velas D1 (apertura 00:00) la ventana 01:30-23:30 del original podría bloquear todas las señales. |
| Cierres forzados | no diario; no viernes | no diario; no viernes | Sin cambio. |
| Máx. operaciones/día | 0 (sin límite) | 1 | Position: una entrada como máximo. |
| Distancia máx. orden | no | 5 % | 5 %: rupturas de máximos de 20-250 días. |
| Bloques activos | 146 señales / 29 indicadores / 29 stop-limit | 12 señales / 17 indicadores / 5 stop-limit | Momentum sin niveles absolutos (ROC en %, MACD vs 0, medias, máximos de 20-250 días). Se eliminan osciladores: no aportan nada a un horizonte de meses. |
| Gestión monetaria | FixedAmount: riesgo 100 por operación | FixedAmount: riesgo 100 por operación | Sin cambio. |
| Fitness | type="ReturnDDRatio" | Weighted: ReturnDDRatio (peso 2, max), Stability (peso 1, max) | Ret/DD + estabilidad; SQN es poco fiable con <100 operaciones. |
| Filtros (Ranking) | AvgBarsInTrade(IS) >= 2; ReturnDDRatio(IS) >= 8; NumberOfTrades(IS) >= 300; WinningPct(IS) >= 40 | NumberOfTrades(IS) >= 40; ReturnDDRatio(IS) >= 3; WinningPct(IS) >= 30; ProfitFactor(IS) >= 1.5; AvgBarsInTrade(IS) >= 5 | Umbrales del estilo + exigencia OOS. |
| Filtro población inicial | ReturnDDRatio(IS) >= 5; AvgBarsInTrade(IS) >= 2; NumberOfTrades(IS) >= 250; WinningPct(IS) >= 35 | ReturnDDRatio(IS) >= 1.88; AvgBarsInTrade(IS) >= 5; NumberOfTrades(IS) >= 33; WinningPct(IS) >= 25 | Misma proporción que el autor (≈60 % Ret/DD, ≈83 % operaciones, -5 puntos de acierto). |
| Motor genético | población 5 × 5 islas, 10 generaciones, cruce 46 %, mutación 35 %, migración 6 % cada 5, reinicio por estancamiento a 30 | población 50 × 4 islas, 30 generaciones, cruce 80 %, mutación 30 %, migración 10 % cada 10, reinicio por estancamiento a 15 | Población y generaciones del original insuficientes para que la evolución actúe (Fase 1 §6). |

#### 2.b Builder de test de ventaja (`Ventaja_Build`)

| Parámetro | Original | Nuevo | Justificación |
|---|---|---|---|
| Timeframe | H1 | D1 | Horizonte típico del estilo (D1). |
| Periodo de datos | 2013.09.30 – 2020.12.31 | 2013.09.30 – 2020.12.31 | Sin cambio. |
| Tramo OOS | sin OOS | sin OOS | Sin cambio. |
| Deslizamiento (pips) | 0 | 0.5 | D1 entra a la apertura del día (a menudo tras gap): 0,5 pips conservador. |
| Modo de generación | simple | simple | Sin cambio. |
| Condiciones de entrada | 1–3 | 1–2 | Nivel + 1-2 filtros como máximo; más condiciones = más grados de libertad. Position: máx. 2 por la muestra pequeña. |
| Periodos de indicadores | 4–200 | 20–250 | 20-250 días (1 mes-1 año). Máximo 2 condiciones: con ~8 operaciones/año cada grado de libertad extra es sobreajuste casi seguro. |
| Desplazamiento (shift) | 1–1 | 1–1 | Sin cambio. |
| Tipos de salida (mín–máx) | 1–5 | 1–1 | Sólo la salida temporal (test de ventaja). |
| Tipos de orden | EnterAtMarket (w1) | EnterAtMarket (w2), EnterAtStop (w1, válida 1-5 velas) | Mayoritariamente a mercado; stop opcional válido 1-5 días. |
| Stop loss | obligatorio=false; sin ATR | obligatorio=false; sin ATR | Sin cambio. |
| Profit target | obligatorio=false; sin ATR | obligatorio=false; sin ATR | Sin cambio. |
| Trailing stop | no | no | Sin cambio. |
| Break-even | no | no | Sin cambio. |
| Salida temporal | sí (50 %), 2-15 velas | sí (100 %), 20-120 velas | Test de ventaja: salida por tiempo 1-6 meses. |
| Salida por regla | no | no | Sin cambio. |
| Ventana de señales | 01:30-23:30 | sin ventana | Con velas D1 (apertura 00:00) la ventana 01:30-23:30 del original podría bloquear todas las señales. |
| Cierres forzados | no diario; no viernes | no diario; no viernes | Sin cambio. |
| Máx. operaciones/día | 0 (sin límite) | 1 | Position: una entrada como máximo. |
| Distancia máx. orden | no | 5 % | 5 %: rupturas de máximos de 20-250 días. |
| Bloques activos | 146 señales / 29 indicadores / 29 stop-limit | 12 señales / 17 indicadores / 5 stop-limit | Momentum sin niveles absolutos (ROC en %, MACD vs 0, medias, máximos de 20-250 días). Se eliminan osciladores: no aportan nada a un horizonte de meses. |
| Gestión monetaria | FixedSize: 1 lote | FixedSize: 1 lote | Sin cambio. |
| Fitness | Weighted: Stagnation (peso 1, min) | Weighted: ProfitFactor (peso 2, max), StagnationPct (peso 1, min) | SQN mide la calidad estadística de la entrada; el original optimizaba sólo 'Stagnation', que ignora el beneficio. |
| Filtros (Ranking) | AvgBarsInTrade(IS) >= 2; ReturnDDRatio(IS) >= 4; NumberOfTrades(IS) >= 300; WinningPct(IS) >= 40 | NumberOfTrades(IS) >= 40; ReturnDDRatio(IS) >= 1.5; WinningPct(IS) >= 30; ProfitFactor(IS) >= 1.3; AvgBarsInTrade(IS) >= 5 | Umbrales del estilo + exigencia OOS. Test de ventaja: Ret/DD a la mitad y PF ≥1,15. |
| Filtro población inicial | ReturnDDRatio(IS) >= 2; AvgBarsInTrade(IS) >= 2; NumberOfTrades(IS) >= 250; WinningPct(IS) >= 35 | ReturnDDRatio(IS) >= 0.75; AvgBarsInTrade(IS) >= 5; NumberOfTrades(IS) >= 33; WinningPct(IS) >= 25 | Misma proporción que el autor (≈60 % Ret/DD, ≈83 % operaciones, -5 puntos de acierto). |
| Motor genético | población 15 × 5 islas, 10 generaciones, cruce 46 %, mutación 35 %, migración 6 % cada 5, reinicio por estancamiento a 30 | población 50 × 4 islas, 30 generaciones, cruce 80 %, mutación 30 %, migración 10 % cada 10, reinicio por estancamiento a 15 | Población y generaciones del original insuficientes para que la evolución actúe (Fase 1 §6). |

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
| Filtros (Ranking) | (ninguna activa) | NetProfit(OOS) > 0; ReturnDDRatio(Full) >= 4.5; NumberOfTrades(Full) >= 60; DrawdownPct(Full) <= 25 | El original no filtraba nada (todas use=false) ni borraba fallidas. |
| Mayor precisión | activo; precisión 2 (tick real + spread personalizado); 1 condiciones | activo; precisión 2 (tick real + spread personalizado); 3 condiciones | Se activan también las condiciones de nº de operaciones y DD. |
| Monte Carlo retest | activo; 1000 sims; OHLC ±10 % ATR(14), spread 1-3. Acepta: NetProfit(IS) >= 0 | activo; 500 sims; OHLC ±10 % ATR(14), desliz. 0-1, spread 2-4, vela de inicio. Acepta: NetProfit(Full) >= 0; DrawdownPct(Full) <= 175% de DrawdownPct[main] | Spread desde el base hasta 2-4x, deslizamiento, percentil 95 (no el peor caso) y control del DD. |
| Monte Carlo manipulación | no; orden de operaciones 'exact', saltar 10 % | activo; orden de operaciones 'resampling', saltar 10 % | Barato; 'resampling' y referencia corregida (el original comparaba MC contra MC). |
| SPP / perfil de optimización | activo; 15000 tests, ±20 %, 6 pasos; ≥95 % rentables | activo; 8000 tests, ±30 %, 6 pasos; ≥90 % rentables | Tests y exigencia ajustados al coste de cómputo y a la sensibilidad del estilo. |
| What-if | no; ExcludePctTradesWithBiggestPl, ExcludePctTradesWithLowestPl | activo; ExcludeTradesWithBiggestPl, ExcludeTradesWithLowestPl | Quitar 2 mejores/peores (estilos de outliers). |

Diferencias del `Ventaja_Retest` respecto al anterior:

- **Gestión monetaria:** FixedSize: 1 lote
- **Fitness:** Weighted: ProfitFactor (peso 2, max), StagnationPct (peso 1, min)
- **Filtros (Ranking):** NetProfit(OOS) > 0; ProfitFactor(Full) >= 1.2; NumberOfTrades(Full) >= 60

### 3. Indicadores y bloques seleccionados

Criterio general: Momentum sin niveles absolutos (ROC en %, MACD vs 0, medias, máximos de 20-250 días). Se eliminan osciladores: no aportan nada a un horizonte de meses. El original activaba 146 señales + 29 indicadores + 29 niveles stop/limit genéricos con peso 1; aquí sólo los coherentes con la tesis, con peso mayor en los centrales (w2-w3).

| Bloque | Peso | Familia | Qué mide | Por qué en este estilo | Rango específico |
|---|---|---|---|---|---|
| `BarOpensAboveHighestAfterOpenBelow` | 3 | Ruptura de nivel | La vela abre por encima del máximo de N velas tras abrir por debajo (ruptura Donchian confirmada en apertura). | Nuevos máximos de 20-250 días (momentum de series temporales). | global del estilo |
| `IchimokuKumoBreakoutBullish` | 1 | Ruptura de nivel | El precio sale por encima de la nube de Ichimoku. | Nuevos máximos de 20-250 días (momentum de series temporales). | global del estilo |
| `ROCAboveLevel` | 2 | Momentum | Rate of Change (%) por encima de un nivel: momentum de series temporales. | ROC en % y MACD frente a cero: escalan a cualquier precio. | Level 0 a 15 (paso 1) |
| `MACDMainCrossAboveZero` | 1 | Momentum | MACD cruza cero al alza. | ROC en % y MACD frente a cero: escalan a cualquier precio. | global del estilo |
| `MACDMainHigherZero` | 1 | Momentum | MACD por encima de cero (media rápida > lenta): independiente de la escala de precio. | ROC en % y MACD frente a cero: escalan a cualquier precio. | global del estilo |
| `ROCRising` | 1 | Momentum | ROC creciente. | ROC en % y MACD frente a cero: escalan a cualquier precio. | global del estilo |
| `Indicators.SMA` | 2 | Tendencia | Media simple. | Pendiente de medias largas. | global del estilo |
| `MABarClosesAbove` | 2 | Tendencia | Cierre por encima de una media móvil. | Pendiente de medias largas. | global del estilo |
| `MARising` | 2 | Tendencia | Media móvil con pendiente positiva. | Pendiente de medias largas. | global del estilo |
| `ADXHigher` | 1 | Tendencia | ADX por encima de un nivel: tendencia con fuerza. | Pendiente de medias largas. | Level 20 a 40 (paso 5) |
| `Indicators.EMA` | 1 | Tendencia | Media exponencial. | Pendiente de medias largas. | global del estilo |
| `KAMARising` | 1 | Tendencia | KAMA con pendiente positiva. | Pendiente de medias largas. | global del estilo |
| `LinRegRising` | 1 | Tendencia | Regresión lineal con pendiente positiva. | Pendiente de medias largas. | global del estilo |
| `SuperTrendUPTrend` | 1 | Tendencia | SuperTrend en modo alcista. | Pendiente de medias largas. | global del estilo |
| `Indicators.ATR` | 1 | Volatilidad | ATR: rango medio verdadero. | ATR sólo como normalizador. | global del estilo |
| `Indicators.Highest` | 2 | Nivel de referencia | Máximo de N velas (canal Donchian). | Máximos semanales/mensuales. | global del estilo |
| `Indicators.Lowest` | 1 | Nivel de referencia | Mínimo de N velas. | Máximos semanales/mensuales. | global del estilo |
| `Prices.CloseW` | 1 | Nivel de referencia | Cierre semanal. | Máximos semanales/mensuales. | global del estilo |
| `Prices.HighM` | 1 | Nivel de referencia | Máximo mensual. | Máximos semanales/mensuales. | global del estilo |
| `Prices.HighW` | 1 | Nivel de referencia | Máximo semanal. | Máximos semanales/mensuales. | global del estilo |
| `Prices.LowM` | 1 | Nivel de referencia | Mínimo mensual. | Máximos semanales/mensuales. | global del estilo |
| `Prices.LowW` | 1 | Nivel de referencia | Mínimo semanal. | Máximos semanales/mensuales. | global del estilo |
| `Prices.Close` | 1 | Precio | Cierre. | Comparaciones con medias y niveles. | global del estilo |
| `Prices.High` | 1 | Precio | Máximo. | Comparaciones con medias y niveles. | global del estilo |
| `Prices.Low` | 1 | Precio | Mínimo. | Comparaciones con medias y niveles. | global del estilo |
| `CrossesAbove` | 1 | Comparador | A cruza B al alza. | Condiciones simples. | global del estilo |
| `CrossesBelow` | 1 | Comparador | A cruza B a la baja. | Condiciones simples. | global del estilo |
| `IsGreater` | 1 | Comparador | A > B. | Condiciones simples. | global del estilo |
| `IsLower` | 1 | Comparador | A < B. | Condiciones simples. | global del estilo |
| `Stop/Limit Price Levels.Highest` | 2 | Precio de orden stop/limit | Precio de la orden = máximo de N velas. | Stop opcional sobre máximo. | global del estilo |
| `Stop/Limit Price Levels.High` | 1 | Precio de orden stop/limit | Precio de la orden = máximo de una vela (vela señal). | Stop opcional sobre máximo. | global del estilo |
| `Stop/Limit Price Levels.HighM` | 1 | Precio de orden stop/limit | Precio = máximo mensual. | Stop opcional sobre máximo. | global del estilo |
| `Stop/Limit Price Levels.HighW` | 1 | Precio de orden stop/limit | Precio = máximo semanal. | Stop opcional sobre máximo. | global del estilo |
| `Stop/Limit Price Ranges.ATR` | 1 | Desplazamiento de orden | Desplazamiento del precio de la orden = k·ATR. | Margen en ATR. | global del estilo |

### 4. Timeframe, símbolos y horarios

- **Timeframe:** D1.
- **Instrumento recomendado:** Índices (US500/US30/DAX), oro, y pares con tendencia macro. Necesita ≥15-20 años de datos: con 2013-2024 el número de operaciones es insuficiente (ver Fase 2).
- **Horario:** D1 sin filtro horario. Las posiciones duran de semanas a meses; el swap es un componente principal del resultado.

### 5. Salidas y gestión del riesgo

SL 2,5-6 ATR(20-100) diario obligatorio, **sin objetivo**, trailing 3-6 ATR (70 %), salida temporal 60-250 días (30 %) y salida por regla (50 %). Riesgo 1 %.

### 6. Filtros y ranking

| Archivo | Fitness | Filtros |
|---|---|---|
| `Estrategia_Build_ConfigInicial_H1_BUY__Position_D1` | Weighted: ReturnDDRatio (peso 2, max), Stability (peso 1, max) | NumberOfTrades(IS) >= 40; ReturnDDRatio(IS) >= 3; WinningPct(IS) >= 30; ProfitFactor(IS) >= 1.5; AvgBarsInTrade(IS) >= 5 |
| `Estrategia_Retest_ConfigInicial_H1_BUY__Position_D1` | Weighted: ReturnDDRatio (peso 2, max), Stability (peso 1, max) | NetProfit(OOS) > 0; ReturnDDRatio(Full) >= 4.5; NumberOfTrades(Full) >= 60; DrawdownPct(Full) <= 25 |
| `Ventaja_Build_ConfigInicial_H1_BUY__Position_D1` | Weighted: ProfitFactor (peso 2, max), StagnationPct (peso 1, min) | NumberOfTrades(IS) >= 40; ReturnDDRatio(IS) >= 1.5; WinningPct(IS) >= 30; ProfitFactor(IS) >= 1.3; AvgBarsInTrade(IS) >= 5 |
| `Ventaja_Retest_ConfigInicial_H1_BUY__Position_D1` | Weighted: ProfitFactor (peso 2, max), StagnationPct (peso 1, min) | NetProfit(OOS) > 0; ProfitFactor(Full) >= 1.2; NumberOfTrades(Full) >= 60 |

Justificación: Ret/DD + estabilidad; SQN es poco fiable con <100 operaciones. Los umbrales reflejan la frecuencia y el acierto típicos del estilo (no se usa el 40 % de acierto ni las 300 operaciones del original para todos).

### 7. Motor y robustez

- **Builder:** población 50 × 4 islas, 30 generaciones, cruce 80 %, mutación 30 %, migración 10 % cada 10, reinicio por estancamiento a 15.
- **Retest:** activo; precisión 2 (tick real + spread personalizado); 3 condiciones. SPP ±30 %: con periodos largos la superficie debe ser lisa; exigencia 90 %.
- **Monte Carlo:** activo; 500 sims; OHLC ±10 % ATR(14), desliz. 0-1, spread 2-4, vela de inicio. Acepta: NetProfit(Full) >= 0; DrawdownPct(Full) <= 175% de DrawdownPct[main].
- **Manipulación MC:** activo; orden de operaciones 'resampling', saltar 10 %.
- **SPP:** activo; 8000 tests, ±30 %, 6 pasos; ≥90 % rentables.
- **What-if:** activo; ExcludeTradesWithBiggestPl, ExcludeTradesWithLowestPl.

### 8. Riesgos conocidos, sobreoptimización y mitigación

Riesgos propios del estilo: Muestra pequeña; dependencia de pocas operaciones grandes; swap acumulado; cambio de régimen macro.

1. Con 2013-2024 (≈11 años) un sistema de meses hace 40-90 operaciones: elegir la mejor entre miles de candidatas con esa muestra es minería de datos casi pura. Máximo 2 condiciones de entrada.
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

**Seguimiento de tendencia (multi-filtro con trailing)** · timeframe `H4`

**Archivos del kit** (todos *no validados en SQX*):

- `configs/TrendFollowing/Estrategia_Build_ConfigInicial_H1_BUY__TrendFollowing_H4.cfx` — tabla completa de cambios: [`docs/cambios/Estrategia_Build_ConfigInicial_H1_BUY__TrendFollowing_H4.md`](cambios/Estrategia_Build_ConfigInicial_H1_BUY__TrendFollowing_H4.md)
- `configs/TrendFollowing/Estrategia_Retest_ConfigInicial_H1_BUY__TrendFollowing_H4.cfx` — tabla completa de cambios: [`docs/cambios/Estrategia_Retest_ConfigInicial_H1_BUY__TrendFollowing_H4.md`](cambios/Estrategia_Retest_ConfigInicial_H1_BUY__TrendFollowing_H4.md)
- `configs/TrendFollowing/Ventaja_Build_ConfigInicial_H1_BUY__TrendFollowing_H4.cfx` — tabla completa de cambios: [`docs/cambios/Ventaja_Build_ConfigInicial_H1_BUY__TrendFollowing_H4.md`](cambios/Ventaja_Build_ConfigInicial_H1_BUY__TrendFollowing_H4.md)
- `configs/TrendFollowing/Ventaja_Retest_ConfigInicial_H1_BUY__TrendFollowing_H4.cfx` — tabla completa de cambios: [`docs/cambios/Ventaja_Retest_ConfigInicial_H1_BUY__TrendFollowing_H4.md`](cambios/Ventaja_Retest_ConfigInicial_H1_BUY__TrendFollowing_H4.md)

### 1. Tesis

Las tendencias persisten más de lo que predice un paseo aleatorio (reacción lenta a la información, flujos institucionales). Se entra cuando varios filtros de tendencia coinciden y se sale por trailing: pocas ganancias grandes pagan muchas pérdidas pequeñas.

### 2. Cambios respecto al original

#### 2.a Builder de estrategia completa (`Estrategia_Build`)

| Parámetro | Original | Nuevo | Justificación |
|---|---|---|---|
| Timeframe | H1 | H4 | Horizonte típico del estilo (H4). |
| Periodo de datos | 2013.09.30 – 2020.12.31 | 2013.09.30 – 2020.12.31 | Sin cambio. |
| Tramo OOS | sin OOS | 2019.01.01 – 2020.12.31 | Validación dentro del Builder: el original filtraba sólo sobre IS. |
| Deslizamiento (pips) | 0 | 0.3 | El original usa 0. |
| Modo de generación | template (plantilla externa .sqx) | simple | El original dependía de una plantilla .sqx no incluida; en modo simple el archivo es autónomo (docs/04 §A.3 para volver a plantilla). |
| Condiciones de entrada | 0–0 | 1–3 | Nivel + 1-2 filtros como máximo; más condiciones = más grados de libertad. |
| Periodos de indicadores | 4–200 | 10–200 | 10-200 velas H4 = 2-33 días. |
| Desplazamiento (shift) | 1–1 | 1–1 | Sin cambio. |
| Tipos de salida (mín–máx) | 1–5 | 2–4 | SL obligatorio + salidas propias del estilo (el original pedía hasta 5 con 3 disponibles). |
| Tipos de orden | EnterAtMarket (w1) | EnterAtMarket (w2), EnterAtStop (w1, válida 1-4 velas) | A mercado con confirmación o stop sobre máximo reciente. |
| Stop loss | obligatorio=true; 1-3 × ATR(20-100) | obligatorio=true; 2-4 × ATR(14-100) | El trailing (prob. 80 %) es la salida natural; objetivo raro y lejano. |
| Profit target | obligatorio=true; 2-5 × ATR(20-100); PT=100-500 % del SL | obligatorio=false; 4-10 × ATR(14-100) | El trailing (prob. 80 %) es la salida natural; objetivo raro y lejano. |
| Trailing stop | sí (50 %), fijo 50-100 pips, 1-5 ATR | sí (80 %), 2.5-5 ATR | El trailing (prob. 80 %) es la salida natural; objetivo raro y lejano. |
| Break-even | no | no | Sin cambio. |
| Salida temporal | no | no | Sin cambio. |
| Salida por regla | no | sí (50 %) | El trailing (prob. 80 %) es la salida natural; objetivo raro y lejano. |
| Ventana de señales | 01:30-23:30 | sin ventana | Igual que Swing: en H4 la ventana del original sesga señales. |
| Cierres forzados | no diario; no viernes | no diario; no viernes | Sin cambio. |
| Máx. operaciones/día | 0 (sin límite) | 1 | Una entrada diaria como máximo. |
| Distancia máx. orden | no | 3 % | 3 %: rupturas de canales largos. |
| Bloques activos | 146 señales / 29 indicadores / 29 stop-limit | 19 señales / 15 indicadores / 5 stop-limit | Sólo filtros de dirección/fuerza de tendencia; sin osciladores de sobrecompra/sobreventa (contradicen la tesis). |
| Gestión monetaria | FixedAmount: riesgo 100 por operación | FixedAmount: riesgo 100 por operación | Sin cambio. |
| Fitness | type="ReturnDDRatio" | Weighted: ReturnDDRatio (peso 2, max), StagnationPct (peso 1, min) | El talón de Aquiles del TF son las rachas planas largas: StagnationPct las penaliza. |
| Filtros (Ranking) | AvgBarsInTrade(IS) >= 2; ReturnDDRatio(IS) >= 8; NumberOfTrades(IS) >= 300; WinningPct(IS) >= 40 | NumberOfTrades(IS) >= 100; ReturnDDRatio(IS) >= 3.5; WinningPct(IS) >= 30; ProfitFactor(IS) >= 1.4; AvgBarsInTrade(IS) >= 5; NetProfit(OOS) > 0; ProfitFactor(OOS) >= 1.05 | Umbrales del estilo + exigencia OOS. |
| Filtro población inicial | ReturnDDRatio(IS) >= 5; AvgBarsInTrade(IS) >= 2; NumberOfTrades(IS) >= 250; WinningPct(IS) >= 35 | ReturnDDRatio(IS) >= 2.19; AvgBarsInTrade(IS) >= 5; NumberOfTrades(IS) >= 83; WinningPct(IS) >= 25 | Misma proporción que el autor (≈60 % Ret/DD, ≈83 % operaciones, -5 puntos de acierto). |
| Motor genético | población 5 × 5 islas, 10 generaciones, cruce 46 %, mutación 35 %, migración 6 % cada 5, reinicio por estancamiento a 30 | población 50 × 4 islas, 40 generaciones, cruce 80 %, mutación 30 %, migración 10 % cada 10, reinicio por estancamiento a 15 | Población y generaciones del original insuficientes para que la evolución actúe (Fase 1 §6). |

#### 2.b Builder de test de ventaja (`Ventaja_Build`)

| Parámetro | Original | Nuevo | Justificación |
|---|---|---|---|
| Timeframe | H1 | H4 | Horizonte típico del estilo (H4). |
| Periodo de datos | 2013.09.30 – 2020.12.31 | 2013.09.30 – 2020.12.31 | Sin cambio. |
| Tramo OOS | sin OOS | 2019.01.01 – 2020.12.31 | Validación dentro del Builder: el original filtraba sólo sobre IS. |
| Deslizamiento (pips) | 0 | 0.3 | El original usa 0. |
| Modo de generación | simple | simple | Sin cambio. |
| Condiciones de entrada | 1–3 | 1–3 | Sin cambio. |
| Periodos de indicadores | 4–200 | 10–200 | 10-200 velas H4 = 2-33 días. |
| Desplazamiento (shift) | 1–1 | 1–1 | Sin cambio. |
| Tipos de salida (mín–máx) | 1–5 | 1–1 | Sólo la salida temporal (test de ventaja). |
| Tipos de orden | EnterAtMarket (w1) | EnterAtMarket (w2), EnterAtStop (w1, válida 1-4 velas) | A mercado con confirmación o stop sobre máximo reciente. |
| Stop loss | obligatorio=false; sin ATR | obligatorio=false; sin ATR | Sin cambio. |
| Profit target | obligatorio=false; sin ATR | obligatorio=false; sin ATR | Sin cambio. |
| Trailing stop | no | no | Sin cambio. |
| Break-even | no | no | Sin cambio. |
| Salida temporal | sí (50 %), 2-15 velas | sí (100 %), 12-60 velas | Test de ventaja: salida por tiempo 2-10 días. |
| Salida por regla | no | no | Sin cambio. |
| Ventana de señales | 01:30-23:30 | sin ventana | Igual que Swing: en H4 la ventana del original sesga señales. |
| Cierres forzados | no diario; no viernes | no diario; no viernes | Sin cambio. |
| Máx. operaciones/día | 0 (sin límite) | 1 | Una entrada diaria como máximo. |
| Distancia máx. orden | no | 3 % | 3 %: rupturas de canales largos. |
| Bloques activos | 146 señales / 29 indicadores / 29 stop-limit | 19 señales / 15 indicadores / 5 stop-limit | Sólo filtros de dirección/fuerza de tendencia; sin osciladores de sobrecompra/sobreventa (contradicen la tesis). |
| Gestión monetaria | FixedSize: 1 lote | FixedSize: 1 lote | Sin cambio. |
| Fitness | Weighted: Stagnation (peso 1, min) | Weighted: SQN (peso 2, max), StagnationPct (peso 1, min) | SQN mide la calidad estadística de la entrada; el original optimizaba sólo 'Stagnation', que ignora el beneficio. |
| Filtros (Ranking) | AvgBarsInTrade(IS) >= 2; ReturnDDRatio(IS) >= 4; NumberOfTrades(IS) >= 300; WinningPct(IS) >= 40 | NumberOfTrades(IS) >= 100; ReturnDDRatio(IS) >= 1.75; WinningPct(IS) >= 30; ProfitFactor(IS) >= 1.15; AvgBarsInTrade(IS) >= 5; NetProfit(OOS) > 0 | Umbrales del estilo + exigencia OOS. Test de ventaja: Ret/DD a la mitad y PF ≥1,15. |
| Filtro población inicial | ReturnDDRatio(IS) >= 2; AvgBarsInTrade(IS) >= 2; NumberOfTrades(IS) >= 250; WinningPct(IS) >= 35 | ReturnDDRatio(IS) >= 0.88; AvgBarsInTrade(IS) >= 5; NumberOfTrades(IS) >= 83; WinningPct(IS) >= 25 | Misma proporción que el autor (≈60 % Ret/DD, ≈83 % operaciones, -5 puntos de acierto). |
| Motor genético | población 15 × 5 islas, 10 generaciones, cruce 46 %, mutación 35 %, migración 6 % cada 5, reinicio por estancamiento a 30 | población 50 × 4 islas, 40 generaciones, cruce 80 %, mutación 30 %, migración 10 % cada 10, reinicio por estancamiento a 15 | Población y generaciones del original insuficientes para que la evolución actúe (Fase 1 §6). |

#### 2.c Retesters (`Estrategia_Retest` / `Ventaja_Retest`)

| Parámetro | Original | Nuevo | Justificación |
|---|---|---|---|
| Timeframe | H1 | H4 | Debe coincidir con el Builder del estilo. |
| Periodo / OOS | 2013.09.30 – 2024.07.22; OOS 2021.01.01 – 2024.07.22 | 2013.09.30 – 2024.07.22; OOS 2021.01.01 – 2024.07.22 | Sin cambio. |
| Deslizamiento | 0 | 0.3 | El original usa 0. |
| Ventana de señales | 01:30-23:30 | sin ventana | Idéntica al Builder: si difiere, el Retest no reproduce lo construido. |
| Cierres forzados | no diario; no viernes | no diario; no viernes | Sin cambio. |
| Gestión monetaria | FixedAmount: riesgo 100 por operación | FixedAmount: riesgo 100 por operación | Sin cambio. |
| Fitness | type="ReturnDDRatio" | Weighted: ReturnDDRatio (peso 2, max), StagnationPct (peso 1, min) | Igual que el Builder correspondiente. |
| Filtros (Ranking) | (ninguna activa) | NetProfit(OOS) > 0; ProfitFactor(OOS) >= 1.05; ReturnDDRatio(Full) >= 5.25; NumberOfTrades(Full) >= 150; DrawdownPct(Full) <= 25 | El original no filtraba nada (todas use=false) ni borraba fallidas. |
| Mayor precisión | activo; precisión 2 (tick real + spread personalizado); 1 condiciones | activo; precisión 2 (tick real + spread personalizado); 3 condiciones | Se activan también las condiciones de nº de operaciones y DD. |
| Monte Carlo retest | activo; 1000 sims; OHLC ±10 % ATR(14), spread 1-3. Acepta: NetProfit(IS) >= 0 | activo; 500 sims; OHLC ±10 % ATR(14), desliz. 0-0.5, spread 2-4, vela de inicio. Acepta: NetProfit(Full) >= 0; DrawdownPct(Full) <= 175% de DrawdownPct[main] | Spread desde el base hasta 2-4x, deslizamiento, percentil 95 (no el peor caso) y control del DD. |
| Monte Carlo manipulación | no; orden de operaciones 'exact', saltar 10 % | activo; orden de operaciones 'resampling', saltar 10 % | Barato; 'resampling' y referencia corregida (el original comparaba MC contra MC). |
| SPP / perfil de optimización | activo; 15000 tests, ±20 %, 6 pasos; ≥95 % rentables | activo; 5000 tests, ±30 %, 6 pasos; ≥90 % rentables | Tests y exigencia ajustados al coste de cómputo y a la sensibilidad del estilo. |
| What-if | no; ExcludePctTradesWithBiggestPl, ExcludePctTradesWithLowestPl | activo; ExcludeTradesWithBiggestPl, ExcludeTradesWithLowestPl | Quitar 2 mejores/peores (estilos de outliers). |

Diferencias del `Ventaja_Retest` respecto al anterior:

- **Gestión monetaria:** FixedSize: 1 lote
- **Fitness:** Weighted: SQN (peso 2, max), StagnationPct (peso 1, min)
- **Filtros (Ranking):** NetProfit(OOS) > 0; ProfitFactor(Full) >= 1.1; NumberOfTrades(Full) >= 150

### 3. Indicadores y bloques seleccionados

Criterio general: Sólo filtros de dirección/fuerza de tendencia; sin osciladores de sobrecompra/sobreventa (contradicen la tesis). El original activaba 146 señales + 29 indicadores + 29 niveles stop/limit genéricos con peso 1; aquí sólo los coherentes con la tesis, con peso mayor en los centrales (w2-w3).

| Bloque | Peso | Familia | Qué mide | Por qué en este estilo | Rango específico |
|---|---|---|---|---|---|
| `BarOpensAboveHighestAfterOpenBelow` | 2 | Ruptura de nivel | La vela abre por encima del máximo de N velas tras abrir por debajo (ruptura Donchian confirmada en apertura). | Entrada por ruptura de canal (Donchian/Kumo), la clásica del TF. | global del estilo |
| `IchimokuKumoBreakoutBullish` | 1 | Ruptura de nivel | El precio sale por encima de la nube de Ichimoku. | Entrada por ruptura de canal (Donchian/Kumo), la clásica del TF. | global del estilo |
| `MACDMainCrossAboveSignal` | 1 | Momentum | MACD cruza por encima de su señal. | Confirmación por momentum (MACD). | global del estilo |
| `MACDMainHigherZero` | 1 | Momentum | MACD por encima de cero (media rápida > lenta): independiente de la escala de precio. | Confirmación por momentum (MACD). | global del estilo |
| `ADXHigher` | 2 | Tendencia | ADX por encima de un nivel: tendencia con fuerza. | Núcleo del estilo: varios estimadores independientes de tendencia. | Level 20 a 40 (paso 5) |
| `BarClosesAboveSuperTrend` | 2 | Tendencia | Cierre por encima de la línea SuperTrend. | Núcleo del estilo: varios estimadores independientes de tendencia. | ATR Mult 1.5 a 5 (paso 0.5) |
| `SuperTrendUPTrend` | 2 | Tendencia | SuperTrend en modo alcista. | Núcleo del estilo: varios estimadores independientes de tendencia. | ATR Mult 1.5 a 5 (paso 0.5) |
| `ADXRising` | 1 | Tendencia | ADX creciente: la tendencia gana fuerza. | Núcleo del estilo: varios estimadores independientes de tendencia. | global del estilo |
| `AroonCrossesAbove` | 1 | Tendencia | Aroon Up cruza por encima de Aroon Down (deducido del nombre). | Núcleo del estilo: varios estimadores independientes de tendencia. | global del estilo |
| `DICrossUp` | 1 | Tendencia | DI+ cruza por encima de DI- (deducido del nombre). | Núcleo del estilo: varios estimadores independientes de tendencia. | global del estilo |
| `FastKAMAAboveSlowKAMA` | 1 | Tendencia | KAMA rápida por encima de la lenta (media adaptativa). | Núcleo del estilo: varios estimadores independientes de tendencia. | global del estilo |
| `FasterHMAIsAboveSlowerHMA` | 1 | Tendencia | Media de Hull rápida por encima de la lenta. | Núcleo del estilo: varios estimadores independientes de tendencia. | global del estilo |
| `GannHiLoUPTrend` | 1 | Tendencia | Gann HiLo activador en modo alcista. | Núcleo del estilo: varios estimadores independientes de tendencia. | global del estilo |
| `IchimokuTenkanKijunCrossBullish` | 1 | Tendencia | Cruce alcista Tenkan/Kijun de Ichimoku. | Núcleo del estilo: varios estimadores independientes de tendencia. | global del estilo |
| `Indicators.EMA` | 1 | Tendencia | Media exponencial. | Núcleo del estilo: varios estimadores independientes de tendencia. | global del estilo |
| `Indicators.HullMovingAverage` | 1 | Tendencia | Media de Hull. | Núcleo del estilo: varios estimadores independientes de tendencia. | global del estilo |
| `Indicators.KAMA` | 1 | Tendencia | Media adaptativa de Kaufman. | Núcleo del estilo: varios estimadores independientes de tendencia. | global del estilo |
| `Indicators.SMA` | 1 | Tendencia | Media simple. | Núcleo del estilo: varios estimadores independientes de tendencia. | global del estilo |
| `Indicators.SuperTrend` | 1 | Tendencia | Línea SuperTrend. | Núcleo del estilo: varios estimadores independientes de tendencia. | ATR Mult 1.5 a 5 (paso 0.5) |
| `KERaboveLevel` | 1 | Tendencia | Ratio de eficiencia de Kaufman alto: movimiento direccional limpio. | Núcleo del estilo: varios estimadores independientes de tendencia. | Level 0.3 a 0.7 (paso 0.05) |
| `MABarClosesAbove` | 1 | Tendencia | Cierre por encima de una media móvil. | Núcleo del estilo: varios estimadores independientes de tendencia. | global del estilo |
| `MARising` | 1 | Tendencia | Media móvil con pendiente positiva. | Núcleo del estilo: varios estimadores independientes de tendencia. | global del estilo |
| `PSARBarLower` | 1 | Tendencia | Parabolic SAR por debajo de la vela (deducido: régimen alcista). | Núcleo del estilo: varios estimadores independientes de tendencia. | global del estilo |
| `VortexUptrend` | 1 | Tendencia | Indicador Vortex en tendencia alcista. | Núcleo del estilo: varios estimadores independientes de tendencia. | global del estilo |
| `Indicators.ATR` | 1 | Volatilidad | ATR: rango medio verdadero. | ATR como normalizador. | global del estilo |
| `Indicators.Highest` | 2 | Nivel de referencia | Máximo de N velas (canal Donchian). | Canales para comparar. | global del estilo |
| `Indicators.Lowest` | 1 | Nivel de referencia | Mínimo de N velas. | Canales para comparar. | global del estilo |
| `Prices.Close` | 1 | Precio | Cierre. | Comparaciones. | global del estilo |
| `Prices.High` | 1 | Precio | Máximo. | Comparaciones. | global del estilo |
| `Prices.Low` | 1 | Precio | Mínimo. | Comparaciones. | global del estilo |
| `CrossesAbove` | 1 | Comparador | A cruza B al alza. | Condiciones simples. | global del estilo |
| `CrossesBelow` | 1 | Comparador | A cruza B a la baja. | Condiciones simples. | global del estilo |
| `IsGreater` | 1 | Comparador | A > B. | Condiciones simples. | global del estilo |
| `IsLower` | 1 | Comparador | A < B. | Condiciones simples. | global del estilo |
| `Stop/Limit Price Levels.Highest` | 2 | Precio de orden stop/limit | Precio de la orden = máximo de N velas. | Stop sobre máximo o SuperTrend. | global del estilo |
| `Stop/Limit Price Levels.High` | 1 | Precio de orden stop/limit | Precio de la orden = máximo de una vela (vela señal). | Stop sobre máximo o SuperTrend. | global del estilo |
| `Stop/Limit Price Levels.KeltnerChannel` | 1 | Precio de orden stop/limit | Precio = banda de Keltner. | Stop sobre máximo o SuperTrend. | global del estilo |
| `Stop/Limit Price Levels.SuperTrend` | 1 | Precio de orden stop/limit | Precio = línea SuperTrend. | Stop sobre máximo o SuperTrend. | ATR Mult 1.5 a 5 (paso 0.5) |
| `Stop/Limit Price Ranges.ATR` | 1 | Desplazamiento de orden | Desplazamiento del precio de la orden = k·ATR. | Margen en ATR. | global del estilo |

### 4. Timeframe, símbolos y horarios

- **Timeframe:** H4.
- **Instrumento recomendado:** Cesta diversificada (índices, metales, JPY-cruces). En un solo símbolo el resultado depende de 2-3 tendencias: validar en varios mercados.
- **Horario:** H4 sin filtro horario; mantiene posiciones días o semanas.

### 5. Salidas y gestión del riesgo

SL 2-4 ATR(14-100); **trailing 2,5-5 ATR como salida principal (80 %)**; objetivo raro y lejano (4-10 ATR, 30 %); salida por regla (50 %). Acierto esperado 30-40 %. Riesgo 1 %.

### 6. Filtros y ranking

| Archivo | Fitness | Filtros |
|---|---|---|
| `Estrategia_Build_ConfigInicial_H1_BUY__TrendFollowing_H4` | Weighted: ReturnDDRatio (peso 2, max), StagnationPct (peso 1, min) | NumberOfTrades(IS) >= 100; ReturnDDRatio(IS) >= 3.5; WinningPct(IS) >= 30; ProfitFactor(IS) >= 1.4; AvgBarsInTrade(IS) >= 5; NetProfit(OOS) > 0; ProfitFactor(OOS) >= 1.05 |
| `Estrategia_Retest_ConfigInicial_H1_BUY__TrendFollowing_H4` | Weighted: ReturnDDRatio (peso 2, max), StagnationPct (peso 1, min) | NetProfit(OOS) > 0; ProfitFactor(OOS) >= 1.05; ReturnDDRatio(Full) >= 5.25; NumberOfTrades(Full) >= 150; DrawdownPct(Full) <= 25 |
| `Ventaja_Build_ConfigInicial_H1_BUY__TrendFollowing_H4` | Weighted: SQN (peso 2, max), StagnationPct (peso 1, min) | NumberOfTrades(IS) >= 100; ReturnDDRatio(IS) >= 1.75; WinningPct(IS) >= 30; ProfitFactor(IS) >= 1.15; AvgBarsInTrade(IS) >= 5; NetProfit(OOS) > 0 |
| `Ventaja_Retest_ConfigInicial_H1_BUY__TrendFollowing_H4` | Weighted: SQN (peso 2, max), StagnationPct (peso 1, min) | NetProfit(OOS) > 0; ProfitFactor(Full) >= 1.1; NumberOfTrades(Full) >= 150 |

Justificación: El talón de Aquiles del TF son las rachas planas largas: StagnationPct las penaliza. Los umbrales reflejan la frecuencia y el acierto típicos del estilo (no se usa el 40 % de acierto ni las 300 operaciones del original para todos).

### 7. Motor y robustez

- **Builder:** población 50 × 4 islas, 40 generaciones, cruce 80 %, mutación 30 %, migración 10 % cada 10, reinicio por estancamiento a 15.
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

1. `Ventaja_Build…TrendFollowing_H4` (salida 2-10 días) → `Ventaja_Retest…`.
2. `Estrategia_Build…` → `Estrategia_Retest…TrendFollowing_H4`.
3. Retest en 5+ mercados no correlacionados.
4. Walk-Forward Matrix y comprobación de rachas perdedoras máximas frente a tu tolerancia.

---

## Range

**Trading de rango (reversión a la media en régimen lateral)** · timeframe `H1`

**Archivos del kit** (todos *no validados en SQX*):

- `configs/Range/Estrategia_Build_ConfigInicial_H1_BUY__Range_H1.cfx` — tabla completa de cambios: [`docs/cambios/Estrategia_Build_ConfigInicial_H1_BUY__Range_H1.md`](cambios/Estrategia_Build_ConfigInicial_H1_BUY__Range_H1.md)
- `configs/Range/Estrategia_Retest_ConfigInicial_H1_BUY__Range_H1.cfx` — tabla completa de cambios: [`docs/cambios/Estrategia_Retest_ConfigInicial_H1_BUY__Range_H1.md`](cambios/Estrategia_Retest_ConfigInicial_H1_BUY__Range_H1.md)
- `configs/Range/Ventaja_Build_ConfigInicial_H1_BUY__Range_H1.cfx` — tabla completa de cambios: [`docs/cambios/Ventaja_Build_ConfigInicial_H1_BUY__Range_H1.md`](cambios/Ventaja_Build_ConfigInicial_H1_BUY__Range_H1.md)
- `configs/Range/Ventaja_Retest_ConfigInicial_H1_BUY__Range_H1.cfx` — tabla completa de cambios: [`docs/cambios/Ventaja_Retest_ConfigInicial_H1_BUY__Range_H1.md`](cambios/Ventaja_Retest_ConfigInicial_H1_BUY__Range_H1.md)

### 1. Tesis

Cuando la tendencia es débil (ADX bajo, eficiencia de Kaufman baja) los excesos respecto a la media se corrigen: se compra el exceso bajista y se sale en la media con objetivo corto.

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
| Tipos de orden | EnterAtMarket (w1) | EnterAtMarket (w1), EnterAtLimit (w2, válida 1-5 velas) | Límite bajo la banda/mínimo: se compra el exceso, no la ruptura. |
| Stop loss | obligatorio=true; 1-3 × ATR(20-100) | obligatorio=true; 1.5-3 × ATR(14-60) | Objetivo corto obligatorio (PT 40-120 % del SL) y alta tasa de acierto; salida temporal: si no revierte en 5-30 h la tesis falló. |
| Profit target | obligatorio=true; 2-5 × ATR(20-100); PT=100-500 % del SL | obligatorio=true; 0.8-2 × ATR(14-60); PT=40-120 % del SL | Objetivo corto obligatorio (PT 40-120 % del SL) y alta tasa de acierto; salida temporal: si no revierte en 5-30 h la tesis falló. |
| Trailing stop | sí (50 %), fijo 50-100 pips, 1-5 ATR | no | Objetivo corto obligatorio (PT 40-120 % del SL) y alta tasa de acierto; salida temporal: si no revierte en 5-30 h la tesis falló. |
| Break-even | no | no | Sin cambio. |
| Salida temporal | no | sí (50 %), 5-30 velas | Objetivo corto obligatorio (PT 40-120 % del SL) y alta tasa de acierto; salida temporal: si no revierte en 5-30 h la tesis falló. |
| Salida por regla | no | sí (50 %) | Objetivo corto obligatorio (PT 40-120 % del SL) y alta tasa de acierto; salida temporal: si no revierte en 5-30 h la tesis falló. |
| Ventana de señales | 01:30-23:30 | 01:30-09:30 | Sesión asiática: menor drift direccional en FX. |
| Cierres forzados | no diario; no viernes | no diario; no viernes | Sin cambio. |
| Máx. operaciones/día | 0 (sin límite) | 2 | Evita promediar a la baja en tendencia. |
| Distancia máx. orden | no | 1 % | 1 %. |
| Bloques activos | 146 señales / 29 indicadores / 29 stop-limit | 16 señales / 18 indicadores / 9 stop-limit | Osciladores sólo en zona de sobreventa (sus rangos 0-100 originales permitían 'comprar en sobrecompra'); filtros de régimen lateral (ADX bajo, KER bajo). |
| Gestión monetaria | FixedAmount: riesgo 100 por operación | FixedAmount: riesgo 75 por operación | Riesgo fijo 0.75 % (no compuesto: Ret/DD comparable en el tiempo). |
| Fitness | type="ReturnDDRatio" | Weighted: ProfitFactor (peso 1, max), ReturnDDRatio (peso 2, max) | PF alto es imprescindible en reversión (pérdidas medias > ganancias medias). |
| Filtros (Ranking) | AvgBarsInTrade(IS) >= 2; ReturnDDRatio(IS) >= 8; NumberOfTrades(IS) >= 300; WinningPct(IS) >= 40 | NumberOfTrades(IS) >= 250; ReturnDDRatio(IS) >= 4; WinningPct(IS) >= 55; ProfitFactor(IS) >= 1.25; AvgBarsInTrade(IS) >= 2; NetProfit(OOS) > 0; ProfitFactor(OOS) >= 1.1 | Umbrales del estilo + exigencia OOS. |
| Filtro población inicial | ReturnDDRatio(IS) >= 5; AvgBarsInTrade(IS) >= 2; NumberOfTrades(IS) >= 250; WinningPct(IS) >= 35 | ReturnDDRatio(IS) >= 2.5; AvgBarsInTrade(IS) >= 2; NumberOfTrades(IS) >= 207; WinningPct(IS) >= 50 | Misma proporción que el autor (≈60 % Ret/DD, ≈83 % operaciones, -5 puntos de acierto). |
| Motor genético | población 5 × 5 islas, 10 generaciones, cruce 46 %, mutación 35 %, migración 6 % cada 5, reinicio por estancamiento a 30 | población 40 × 4 islas, 40 generaciones, cruce 80 %, mutación 30 %, migración 10 % cada 10, reinicio por estancamiento a 15 | Población y generaciones del original insuficientes para que la evolución actúe (Fase 1 §6). |

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
| Tipos de orden | EnterAtMarket (w1) | EnterAtMarket (w1), EnterAtLimit (w2, válida 1-5 velas) | Límite bajo la banda/mínimo: se compra el exceso, no la ruptura. |
| Stop loss | obligatorio=false; sin ATR | obligatorio=false; sin ATR | Sin cambio. |
| Profit target | obligatorio=false; sin ATR | obligatorio=false; sin ATR | Sin cambio. |
| Trailing stop | no | no | Sin cambio. |
| Break-even | no | no | Sin cambio. |
| Salida temporal | sí (50 %), 2-15 velas | sí (100 %), 3-24 velas | Test de ventaja: salida por tiempo 3-24 h. |
| Salida por regla | no | no | Sin cambio. |
| Ventana de señales | 01:30-23:30 | 01:30-09:30 | Sesión asiática: menor drift direccional en FX. |
| Cierres forzados | no diario; no viernes | no diario; no viernes | Sin cambio. |
| Máx. operaciones/día | 0 (sin límite) | 2 | Evita promediar a la baja en tendencia. |
| Distancia máx. orden | no | 1 % | 1 %. |
| Bloques activos | 146 señales / 29 indicadores / 29 stop-limit | 16 señales / 18 indicadores / 9 stop-limit | Osciladores sólo en zona de sobreventa (sus rangos 0-100 originales permitían 'comprar en sobrecompra'); filtros de régimen lateral (ADX bajo, KER bajo). |
| Gestión monetaria | FixedSize: 1 lote | FixedSize: 1 lote | Sin cambio. |
| Fitness | Weighted: Stagnation (peso 1, min) | Weighted: SQN (peso 2, max), StagnationPct (peso 1, min) | SQN mide la calidad estadística de la entrada; el original optimizaba sólo 'Stagnation', que ignora el beneficio. |
| Filtros (Ranking) | AvgBarsInTrade(IS) >= 2; ReturnDDRatio(IS) >= 4; NumberOfTrades(IS) >= 300; WinningPct(IS) >= 40 | NumberOfTrades(IS) >= 250; ReturnDDRatio(IS) >= 2; WinningPct(IS) >= 50; ProfitFactor(IS) >= 1.15; AvgBarsInTrade(IS) >= 2; NetProfit(OOS) > 0 | Umbrales del estilo + exigencia OOS. Test de ventaja: Ret/DD a la mitad y PF ≥1,15. |
| Filtro población inicial | ReturnDDRatio(IS) >= 2; AvgBarsInTrade(IS) >= 2; NumberOfTrades(IS) >= 250; WinningPct(IS) >= 35 | ReturnDDRatio(IS) >= 1; AvgBarsInTrade(IS) >= 2; NumberOfTrades(IS) >= 207; WinningPct(IS) >= 45 | Misma proporción que el autor (≈60 % Ret/DD, ≈83 % operaciones, -5 puntos de acierto). |
| Motor genético | población 15 × 5 islas, 10 generaciones, cruce 46 %, mutación 35 %, migración 6 % cada 5, reinicio por estancamiento a 30 | población 40 × 4 islas, 40 generaciones, cruce 80 %, mutación 30 %, migración 10 % cada 10, reinicio por estancamiento a 15 | Población y generaciones del original insuficientes para que la evolución actúe (Fase 1 §6). |

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
| Filtros (Ranking) | (ninguna activa) | NetProfit(OOS) > 0; ProfitFactor(OOS) >= 1.1; ReturnDDRatio(Full) >= 6; NumberOfTrades(Full) >= 375; DrawdownPct(Full) <= 20 | El original no filtraba nada (todas use=false) ni borraba fallidas. |
| Mayor precisión | activo; precisión 2 (tick real + spread personalizado); 1 condiciones | activo; precisión 2 (tick real + spread personalizado); 3 condiciones | Se activan también las condiciones de nº de operaciones y DD. |
| Monte Carlo retest | activo; 1000 sims; OHLC ±10 % ATR(14), spread 1-3. Acepta: NetProfit(IS) >= 0 | activo; 500 sims; OHLC ±10 % ATR(14), desliz. 0-0.5, spread 2-4. Acepta: NetProfit(Full) >= 0; DrawdownPct(Full) <= 150% de DrawdownPct[main] | Spread desde el base hasta 2-4x, deslizamiento, percentil 95 (no el peor caso) y control del DD. |
| Monte Carlo manipulación | no; orden de operaciones 'exact', saltar 10 % | activo; orden de operaciones 'resampling', saltar 10 % | Barato; 'resampling' y referencia corregida (el original comparaba MC contra MC). |
| SPP / perfil de optimización | activo; 15000 tests, ±20 %, 6 pasos; ≥95 % rentables | activo; 5000 tests, ±20 %, 6 pasos; ≥85 % rentables | Tests y exigencia ajustados al coste de cómputo y a la sensibilidad del estilo. |
| What-if | no; ExcludePctTradesWithBiggestPl, ExcludePctTradesWithLowestPl | activo; ExcludePctTradesWithBiggestPl, ExcludePctTradesWithLowestPl | Quitar el 5 % de extremos: el estilo no debe depender de outliers. |

Diferencias del `Ventaja_Retest` respecto al anterior:

- **Gestión monetaria:** FixedSize: 1 lote
- **Fitness:** Weighted: SQN (peso 2, max), StagnationPct (peso 1, min)
- **Filtros (Ranking):** NetProfit(OOS) > 0; ProfitFactor(Full) >= 1.1; NumberOfTrades(Full) >= 375

### 3. Indicadores y bloques seleccionados

Criterio general: Osciladores sólo en zona de sobreventa (sus rangos 0-100 originales permitían 'comprar en sobrecompra'); filtros de régimen lateral (ADX bajo, KER bajo). El original activaba 146 señales + 29 indicadores + 29 niveles stop/limit genéricos con peso 1; aquí sólo los coherentes con la tesis, con peso mayor en los centrales (w2-w3).

| Bloque | Peso | Familia | Qué mide | Por qué en este estilo | Rango específico |
|---|---|---|---|---|---|
| `BarOpensAboveLowestAfterOpenBelow` | 1 | Ruptura de nivel | Abre por encima del mínimo de N velas tras abrir por debajo: recuperación tras una falsa ruptura bajista. | Sólo la recuperación tras falsa ruptura bajista. | global del estilo |
| `BBBarOpensAboveDownAfterOpenBelow` | 2 | Reversión / sobreventa | Reentrada por encima de la banda inferior de Bollinger tras abrir por debajo. | Núcleo: identificar el exceso bajista que se espera que revierta. | global del estilo |
| `KCBarOpensAboveLowerAfterOpenBelow` | 2 | Reversión / sobreventa | Reentrada por encima de la banda inferior de Keltner. | Núcleo: identificar el exceso bajista que se espera que revierta. | global del estilo |
| `BBBarClosesBelowDown` | 1 | Reversión / sobreventa | Cierre por debajo de la banda inferior de Bollinger (exceso bajista). | Núcleo: identificar el exceso bajista que se espera que revierta. | global del estilo |
| `CCICrossUp` | 1 | Reversión / sobreventa | CCI cruza al alza un nivel. | Núcleo: identificar el exceso bajista que se espera que revierta. | Level -150 a -80 (paso 5) |
| `DEMCrossUp` | 1 | Reversión / sobreventa | DeMarker (0-1) cruza al alza un nivel. | Núcleo: identificar el exceso bajista que se espera que revierta. | Level 0.1 a 0.3 (paso 0.1) |
| `Indicators.CCI` | 1 | Reversión / sobreventa | CCI (valor). | Núcleo: identificar el exceso bajista que se espera que revierta. | global del estilo |
| `Indicators.RSI` | 1 | Reversión / sobreventa | RSI (valor). | Núcleo: identificar el exceso bajista que se espera que revierta. | global del estilo |
| `Indicators.Stochastic` | 1 | Reversión / sobreventa | Estocástico (valor). | Núcleo: identificar el exceso bajista que se espera que revierta. | global del estilo |
| `Indicators.WilliamsPR` | 1 | Reversión / sobreventa | Williams %R (valor). | Núcleo: identificar el exceso bajista que se espera que revierta. | global del estilo |
| `KCBarClosesBelowLower` | 1 | Reversión / sobreventa | Cierre por debajo de la banda inferior de Keltner. | Núcleo: identificar el exceso bajista que se espera que revierta. | global del estilo |
| `RSILower` | 1 | Reversión / sobreventa | RSI por debajo de un nivel. | Núcleo: identificar el exceso bajista que se espera que revierta. | Level 20 a 40 (paso 5) |
| `StochFastKCrossUp` | 1 | Reversión / sobreventa | %K rápido del estocástico cruza al alza un nivel. | Núcleo: identificar el exceso bajista que se espera que revierta. | Level 10 a 30 (paso 5) |
| `StochSlowDCrossUp` | 1 | Reversión / sobreventa | %D lento del estocástico cruza al alza un nivel. | Núcleo: identificar el exceso bajista que se espera que revierta. | Level 10 a 30 (paso 5) |
| `WPRCrossUp` | 1 | Reversión / sobreventa | Williams %R cruza al alza un nivel (escala -100..0). | Núcleo: identificar el exceso bajista que se espera que revierta. | Level -95 a -75 (paso 5) |
| `LaguerreRSICrossUP` | 1 | Oscilador | RSI de Laguerre (0-1, poco retardo) cruza al alza un nivel. | Restringido a zona de sobreventa. | Level 0.05 a 0.3 (paso 0.05) |
| `RSICrossUp` | 1 | Oscilador | RSI cruza hacia arriba un nivel. | Restringido a zona de sobreventa. | Level 15 a 40 (paso 5) |
| `ADXLower` | 2 | Régimen lateral | ADX por debajo de un nivel: tendencia débil. | Imprescindible: la reversión sólo funciona sin tendencia. | Level 15 a 30 (paso 5) |
| `KERbelowLevel` | 2 | Régimen lateral | Ratio de eficiencia de Kaufman bajo: movimiento errático, sin dirección. | Imprescindible: la reversión sólo funciona sin tendencia. | Level 0.1 a 0.4 (paso 0.05) |
| `ADXFalling` | 1 | Régimen lateral | ADX descendente: la tendencia pierde fuerza. | Imprescindible: la reversión sólo funciona sin tendencia. | global del estilo |
| `Indicators.EMA` | 1 | Tendencia | Media exponencial. | Medias como 'centro' del rango (objetivo/regla de salida). | global del estilo |
| `Indicators.SMA` | 1 | Tendencia | Media simple. | Medias como 'centro' del rango (objetivo/regla de salida). | global del estilo |
| `Indicators.BollingerBands` | 1 | Nivel de referencia | Bandas de Bollinger (media ± k·desviación). | Bandas y extremos que delimitan el rango. | global del estilo |
| `Indicators.Highest` | 1 | Nivel de referencia | Máximo de N velas (canal Donchian). | Bandas y extremos que delimitan el rango. | global del estilo |
| `Indicators.KeltnerChannel` | 1 | Nivel de referencia | Canal de Keltner (media ± k·ATR). | Bandas y extremos que delimitan el rango. | global del estilo |
| `Indicators.Lowest` | 1 | Nivel de referencia | Mínimo de N velas. | Bandas y extremos que delimitan el rango. | global del estilo |
| `Prices.Close` | 1 | Precio | Cierre. | Comparaciones con bandas. | global del estilo |
| `Prices.Low` | 1 | Precio | Mínimo. | Comparaciones con bandas. | global del estilo |
| `Prices.Open` | 1 | Precio | Apertura. | Comparaciones con bandas. | global del estilo |
| `CrossesAbove` | 1 | Comparador | A cruza B al alza. | Construyen 'precio frente a banda/media'; IsLowerCount mide agotamiento (N velas por debajo). | global del estilo |
| `CrossesBelow` | 1 | Comparador | A cruza B a la baja. | Construyen 'precio frente a banda/media'; IsLowerCount mide agotamiento (N velas por debajo). | global del estilo |
| `IsGreater` | 1 | Comparador | A > B. | Construyen 'precio frente a banda/media'; IsLowerCount mide agotamiento (N velas por debajo). | global del estilo |
| `IsLower` | 1 | Comparador | A < B. | Construyen 'precio frente a banda/media'; IsLowerCount mide agotamiento (N velas por debajo). | global del estilo |
| `IsLowerCount` | 1 | Comparador | A < B durante N velas seguidas. | Construyen 'precio frente a banda/media'; IsLowerCount mide agotamiento (N velas por debajo). | global del estilo |
| `Stop/Limit Price Levels.BollingerBands` | 2 | Precio de orden stop/limit | Precio = banda de Bollinger. | Orden límite en la banda/mínimo: se compra el exceso. | global del estilo |
| `Stop/Limit Price Levels.KeltnerChannel` | 2 | Precio de orden stop/limit | Precio = banda de Keltner. | Orden límite en la banda/mínimo: se compra el exceso. | global del estilo |
| `Stop/Limit Price Levels.EMA` | 1 | Precio de orden stop/limit | Precio = media exponencial. | Orden límite en la banda/mínimo: se compra el exceso. | global del estilo |
| `Stop/Limit Price Levels.Low` | 1 | Precio de orden stop/limit | Precio de la orden = mínimo de una vela. | Orden límite en la banda/mínimo: se compra el exceso. | global del estilo |
| `Stop/Limit Price Levels.Lowest` | 1 | Precio de orden stop/limit | Precio de la orden = mínimo de N velas. | Orden límite en la banda/mínimo: se compra el exceso. | global del estilo |
| `Stop/Limit Price Levels.SMA` | 1 | Precio de orden stop/limit | Precio = media simple. | Orden límite en la banda/mínimo: se compra el exceso. | global del estilo |
| `Stop/Limit Price Ranges.ATR` | 2 | Desplazamiento de orden | Desplazamiento del precio de la orden = k·ATR. | Distancia de la orden límite bajo el nivel. | global del estilo |
| `Stop/Limit Price Ranges.BBRange` | 1 | Desplazamiento de orden | Desplazamiento = k·anchura de Bollinger. | Distancia de la orden límite bajo el nivel. | global del estilo |
| `Stop/Limit Price Ranges.BarRange` | 1 | Desplazamiento de orden | Desplazamiento = k·rango de la vela. | Distancia de la orden límite bajo el nivel. | global del estilo |

### 4. Timeframe, símbolos y horarios

- **Timeframe:** H1.
- **Instrumento recomendado:** EURCHF, EURGBP, AUDNZD, USDCAD en sesión asiática o índices en rango. GBPJPY es tendencial y mal candidato: usar sólo como prueba.
- **Horario:** Entradas 01:30-09:30 servidor (sesión asiática, menor deriva direccional en FX). Fuera de esa franja no se abren operaciones nuevas.

### 5. Salidas y gestión del riesgo

SL 1,5-3 ATR(14-60) obligatorio; objetivo 0,8-2 ATR obligatorio con PT = 40-120 % del SL; salida temporal 5-30 h (50 %) y salida por regla (50 %); sin trailing. Acierto ≥55 %. Riesgo 0,75 %; máximo 2 entradas/día.

### 6. Filtros y ranking

| Archivo | Fitness | Filtros |
|---|---|---|
| `Estrategia_Build_ConfigInicial_H1_BUY__Range_H1` | Weighted: ProfitFactor (peso 1, max), ReturnDDRatio (peso 2, max) | NumberOfTrades(IS) >= 250; ReturnDDRatio(IS) >= 4; WinningPct(IS) >= 55; ProfitFactor(IS) >= 1.25; AvgBarsInTrade(IS) >= 2; NetProfit(OOS) > 0; ProfitFactor(OOS) >= 1.1 |
| `Estrategia_Retest_ConfigInicial_H1_BUY__Range_H1` | Weighted: ProfitFactor (peso 1, max), ReturnDDRatio (peso 2, max) | NetProfit(OOS) > 0; ProfitFactor(OOS) >= 1.1; ReturnDDRatio(Full) >= 6; NumberOfTrades(Full) >= 375; DrawdownPct(Full) <= 20 |
| `Ventaja_Build_ConfigInicial_H1_BUY__Range_H1` | Weighted: SQN (peso 2, max), StagnationPct (peso 1, min) | NumberOfTrades(IS) >= 250; ReturnDDRatio(IS) >= 2; WinningPct(IS) >= 50; ProfitFactor(IS) >= 1.15; AvgBarsInTrade(IS) >= 2; NetProfit(OOS) > 0 |
| `Ventaja_Retest_ConfigInicial_H1_BUY__Range_H1` | Weighted: SQN (peso 2, max), StagnationPct (peso 1, min) | NetProfit(OOS) > 0; ProfitFactor(Full) >= 1.1; NumberOfTrades(Full) >= 375 |

Justificación: PF alto es imprescindible en reversión (pérdidas medias > ganancias medias). Los umbrales reflejan la frecuencia y el acierto típicos del estilo (no se usa el 40 % de acierto ni las 300 operaciones del original para todos).

### 7. Motor y robustez

- **Builder:** población 40 × 4 islas, 40 generaciones, cruce 80 %, mutación 30 %, migración 10 % cada 10, reinicio por estancamiento a 15.
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

**Archivos del kit** (todos *no validados en SQX*):

- `configs/PriceAction/Estrategia_Build_ConfigInicial_H1_BUY__PriceAction_H1.cfx` — tabla completa de cambios: [`docs/cambios/Estrategia_Build_ConfigInicial_H1_BUY__PriceAction_H1.md`](cambios/Estrategia_Build_ConfigInicial_H1_BUY__PriceAction_H1.md)
- `configs/PriceAction/Estrategia_Retest_ConfigInicial_H1_BUY__PriceAction_H1.cfx` — tabla completa de cambios: [`docs/cambios/Estrategia_Retest_ConfigInicial_H1_BUY__PriceAction_H1.md`](cambios/Estrategia_Retest_ConfigInicial_H1_BUY__PriceAction_H1.md)
- `configs/PriceAction/Ventaja_Build_ConfigInicial_H1_BUY__PriceAction_H1.cfx` — tabla completa de cambios: [`docs/cambios/Ventaja_Build_ConfigInicial_H1_BUY__PriceAction_H1.md`](cambios/Ventaja_Build_ConfigInicial_H1_BUY__PriceAction_H1.md)
- `configs/PriceAction/Ventaja_Retest_ConfigInicial_H1_BUY__PriceAction_H1.cfx` — tabla completa de cambios: [`docs/cambios/Ventaja_Retest_ConfigInicial_H1_BUY__PriceAction_H1.md`](cambios/Ventaja_Retest_ConfigInicial_H1_BUY__PriceAction_H1.md)

### 1. Tesis

Patrones de rechazo/absorción (envolvente, martillo, pauta penetrante, fractal) en niveles relevantes (mínimos recientes, máximo/mínimo del día anterior) señalan desequilibrios de órdenes; se entra con stop sobre el máximo de la vela señal.

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
| Tipos de orden | EnterAtMarket (w1) | EnterAtMarket (w1), EnterAtStop (w2, válida 1-3 velas), EnterAtLimit (w1, válida 1-3 velas) | Stop sobre el máximo de la vela señal (confirmación) o límite en retroceso. |
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
| Bloques activos | 146 señales / 29 indicadores / 29 stop-limit | 7 señales / 29 indicadores / 9 stop-limit | Sólo precio, velas y estructura; ATR únicamente como normalizador. Se excluyen patrones bajistas (el original los usaba como entrada larga, incoherente). |
| Gestión monetaria | FixedAmount: riesgo 100 por operación | FixedAmount: riesgo 100 por operación | Sin cambio. |
| Fitness | type="ReturnDDRatio" | Weighted: ReturnDDRatio (peso 2, max), SQN (peso 1, max) | Ret/DD + SQN (consistencia por operación). |
| Filtros (Ranking) | AvgBarsInTrade(IS) >= 2; ReturnDDRatio(IS) >= 8; NumberOfTrades(IS) >= 300; WinningPct(IS) >= 40 | NumberOfTrades(IS) >= 200; ReturnDDRatio(IS) >= 4; WinningPct(IS) >= 40; ProfitFactor(IS) >= 1.3; AvgBarsInTrade(IS) >= 2; NetProfit(OOS) > 0; ProfitFactor(OOS) >= 1.1 | Umbrales del estilo + exigencia OOS. |
| Filtro población inicial | ReturnDDRatio(IS) >= 5; AvgBarsInTrade(IS) >= 2; NumberOfTrades(IS) >= 250; WinningPct(IS) >= 35 | ReturnDDRatio(IS) >= 2.5; AvgBarsInTrade(IS) >= 2; NumberOfTrades(IS) >= 166; WinningPct(IS) >= 35 | Misma proporción que el autor (≈60 % Ret/DD, ≈83 % operaciones, -5 puntos de acierto). |
| Motor genético | población 5 × 5 islas, 10 generaciones, cruce 46 %, mutación 35 %, migración 6 % cada 5, reinicio por estancamiento a 30 | población 40 × 4 islas, 40 generaciones, cruce 80 %, mutación 30 %, migración 10 % cada 10, reinicio por estancamiento a 15 | Población y generaciones del original insuficientes para que la evolución actúe (Fase 1 §6). |

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
| Tipos de orden | EnterAtMarket (w1) | EnterAtMarket (w1), EnterAtStop (w2, válida 1-3 velas), EnterAtLimit (w1, válida 1-3 velas) | Stop sobre el máximo de la vela señal (confirmación) o límite en retroceso. |
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
| Bloques activos | 146 señales / 29 indicadores / 29 stop-limit | 7 señales / 29 indicadores / 9 stop-limit | Sólo precio, velas y estructura; ATR únicamente como normalizador. Se excluyen patrones bajistas (el original los usaba como entrada larga, incoherente). |
| Gestión monetaria | FixedSize: 1 lote | FixedSize: 1 lote | Sin cambio. |
| Fitness | Weighted: Stagnation (peso 1, min) | Weighted: SQN (peso 2, max), StagnationPct (peso 1, min) | SQN mide la calidad estadística de la entrada; el original optimizaba sólo 'Stagnation', que ignora el beneficio. |
| Filtros (Ranking) | AvgBarsInTrade(IS) >= 2; ReturnDDRatio(IS) >= 4; NumberOfTrades(IS) >= 300; WinningPct(IS) >= 40 | NumberOfTrades(IS) >= 200; ReturnDDRatio(IS) >= 2; WinningPct(IS) >= 35; ProfitFactor(IS) >= 1.15; AvgBarsInTrade(IS) >= 2; NetProfit(OOS) > 0 | Umbrales del estilo + exigencia OOS. Test de ventaja: Ret/DD a la mitad y PF ≥1,15. |
| Filtro población inicial | ReturnDDRatio(IS) >= 2; AvgBarsInTrade(IS) >= 2; NumberOfTrades(IS) >= 250; WinningPct(IS) >= 35 | ReturnDDRatio(IS) >= 1; AvgBarsInTrade(IS) >= 2; NumberOfTrades(IS) >= 166; WinningPct(IS) >= 30 | Misma proporción que el autor (≈60 % Ret/DD, ≈83 % operaciones, -5 puntos de acierto). |
| Motor genético | población 15 × 5 islas, 10 generaciones, cruce 46 %, mutación 35 %, migración 6 % cada 5, reinicio por estancamiento a 30 | población 40 × 4 islas, 40 generaciones, cruce 80 %, mutación 30 %, migración 10 % cada 10, reinicio por estancamiento a 15 | Población y generaciones del original insuficientes para que la evolución actúe (Fase 1 §6). |

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
| Filtros (Ranking) | (ninguna activa) | NetProfit(OOS) > 0; ProfitFactor(OOS) >= 1.1; ReturnDDRatio(Full) >= 6; NumberOfTrades(Full) >= 300; DrawdownPct(Full) <= 20 | El original no filtraba nada (todas use=false) ni borraba fallidas. |
| Mayor precisión | activo; precisión 2 (tick real + spread personalizado); 1 condiciones | activo; precisión 2 (tick real + spread personalizado); 3 condiciones | Se activan también las condiciones de nº de operaciones y DD. |
| Monte Carlo retest | activo; 1000 sims; OHLC ±10 % ATR(14), spread 1-3. Acepta: NetProfit(IS) >= 0 | activo; 500 sims; OHLC ±10 % ATR(14), desliz. 0-0.5, spread 2-4. Acepta: NetProfit(Full) >= 0; DrawdownPct(Full) <= 150% de DrawdownPct[main] | Spread desde el base hasta 2-4x, deslizamiento, percentil 95 (no el peor caso) y control del DD. |
| Monte Carlo manipulación | no; orden de operaciones 'exact', saltar 10 % | activo; orden de operaciones 'resampling', saltar 10 % | Barato; 'resampling' y referencia corregida (el original comparaba MC contra MC). |
| SPP / perfil de optimización | activo; 15000 tests, ±20 %, 6 pasos; ≥95 % rentables | activo; 5000 tests, ±20 %, 6 pasos; ≥85 % rentables | Tests y exigencia ajustados al coste de cómputo y a la sensibilidad del estilo. |
| What-if | no; ExcludePctTradesWithBiggestPl, ExcludePctTradesWithLowestPl | activo; ExcludePctTradesWithBiggestPl, ExcludePctTradesWithLowestPl | Quitar el 5 % de extremos: el estilo no debe depender de outliers. |

Diferencias del `Ventaja_Retest` respecto al anterior:

- **Gestión monetaria:** FixedSize: 1 lote
- **Fitness:** Weighted: SQN (peso 2, max), StagnationPct (peso 1, min)
- **Filtros (Ranking):** NetProfit(OOS) > 0; ProfitFactor(Full) >= 1.1; NumberOfTrades(Full) >= 300

### 3. Indicadores y bloques seleccionados

Criterio general: Sólo precio, velas y estructura; ATR únicamente como normalizador. Se excluyen patrones bajistas (el original los usaba como entrada larga, incoherente). El original activaba 146 señales + 29 indicadores + 29 niveles stop/limit genéricos con peso 1; aquí sólo los coherentes con la tesis, con peso mayor en los centrales (w2-w3).

| Bloque | Peso | Familia | Qué mide | Por qué en este estilo | Rango específico |
|---|---|---|---|---|---|
| `BarOpensAboveLowestAfterOpenBelow` | 2 | Ruptura de nivel | Abre por encima del mínimo de N velas tras abrir por debajo: recuperación tras una falsa ruptura bajista. | Recuperación tras falsa ruptura / ruptura de máximos recientes. | global del estilo |
| `BarOpensAboveHighestAfterOpenBelow` | 1 | Ruptura de nivel | La vela abre por encima del máximo de N velas tras abrir por debajo (ruptura Donchian confirmada en apertura). | Recuperación tras falsa ruptura / ruptura de máximos recientes. | global del estilo |
| `Indicators.ATR` | 1 | Volatilidad | ATR: rango medio verdadero. | Sólo rango verdadero/ATR para normalizar tamaños de vela. | global del estilo |
| `Indicators.TrueRange` | 1 | Volatilidad | Rango verdadero de la vela. | Sólo rango verdadero/ATR para normalizar tamaños de vela. | global del estilo |
| `BullishEngulfing` | 2 | Patrón de vela | Envolvente alcista. | Núcleo: patrones de rechazo y absorción alcistas. | global del estilo |
| `Hammer` | 2 | Patrón de vela | Martillo (rechazo de mínimos). | Núcleo: patrones de rechazo y absorción alcistas. | global del estilo |
| `PiercingLine` | 2 | Patrón de vela | Pauta penetrante alcista. | Núcleo: patrones de rechazo y absorción alcistas. | global del estilo |
| `Doji` | 1 | Patrón de vela | Doji (indecisión; útil sólo en contexto). | Núcleo: patrones de rechazo y absorción alcistas. | global del estilo |
| `IsBullishFractal` | 1 | Patrón de vela | Fractal alcista de Williams (mínimo local confirmado). | Núcleo: patrones de rechazo y absorción alcistas. | global del estilo |
| `Indicators.Fractal` | 1 | Nivel de referencia | Último fractal (máximo/mínimo local). | Contexto: máximos/mínimos del día, semana, sesión y fractales. | global del estilo |
| `Indicators.Highest` | 1 | Nivel de referencia | Máximo de N velas (canal Donchian). | Contexto: máximos/mínimos del día, semana, sesión y fractales. | global del estilo |
| `Indicators.Lowest` | 1 | Nivel de referencia | Mínimo de N velas. | Contexto: máximos/mínimos del día, semana, sesión y fractales. | global del estilo |
| `Prices.CloseD` | 1 | Nivel de referencia | Cierre del día anterior. | Contexto: máximos/mínimos del día, semana, sesión y fractales. | global del estilo |
| `Prices.HighD` | 1 | Nivel de referencia | Máximo del día anterior. | Contexto: máximos/mínimos del día, semana, sesión y fractales. | global del estilo |
| `Prices.HighW` | 1 | Nivel de referencia | Máximo semanal. | Contexto: máximos/mínimos del día, semana, sesión y fractales. | global del estilo |
| `Prices.LowD` | 1 | Nivel de referencia | Mínimo del día anterior. | Contexto: máximos/mínimos del día, semana, sesión y fractales. | global del estilo |
| `Prices.LowW` | 1 | Nivel de referencia | Mínimo semanal. | Contexto: máximos/mínimos del día, semana, sesión y fractales. | global del estilo |
| `Prices.OpenD` | 1 | Nivel de referencia | Apertura diaria. | Contexto: máximos/mínimos del día, semana, sesión y fractales. | global del estilo |
| `Prices.SessionHigh` | 1 | Nivel de referencia | Máximo de una sesión horaria configurable. | Contexto: máximos/mínimos del día, semana, sesión y fractales. | Start Hours 1 a 3 (paso 1); Start Minutes 0 a 0 (paso 1); End Hours 8 a 10 (paso 1); End Minutes 0 a 0 (paso 1) |
| `Prices.SessionLow` | 1 | Nivel de referencia | Mínimo de una sesión horaria configurable. | Contexto: máximos/mínimos del día, semana, sesión y fractales. | Start Hours 1 a 3 (paso 1); Start Minutes 0 a 0 (paso 1); End Hours 8 a 10 (paso 1); End Minutes 0 a 0 (paso 1) |
| `Prices.Close` | 2 | Precio | Cierre. | OHLC y Heikin-Ashi: estructura pura. | global del estilo |
| `Prices.High` | 2 | Precio | Máximo. | OHLC y Heikin-Ashi: estructura pura. | global del estilo |
| `Prices.Low` | 2 | Precio | Mínimo. | OHLC y Heikin-Ashi: estructura pura. | global del estilo |
| `Prices.Open` | 2 | Precio | Apertura. | OHLC y Heikin-Ashi: estructura pura. | global del estilo |
| `Prices.HeikenAshiClose` | 1 | Precio | Cierre Heikin-Ashi. | OHLC y Heikin-Ashi: estructura pura. | global del estilo |
| `Prices.HeikenAshiHigh` | 1 | Precio | Máximo Heikin-Ashi. | OHLC y Heikin-Ashi: estructura pura. | global del estilo |
| `Prices.HeikenAshiLow` | 1 | Precio | Mínimo Heikin-Ashi. | OHLC y Heikin-Ashi: estructura pura. | global del estilo |
| `Prices.HeikenAshiOpen` | 1 | Precio | Apertura Heikin-Ashi (vela suavizada). | OHLC y Heikin-Ashi: estructura pura. | global del estilo |
| `CrossesAbove` | 1 | Comparador | A cruza B al alza. | Secuencias (N velas al alza/baja, máximos crecientes). | global del estilo |
| `CrossesBelow` | 1 | Comparador | A cruza B a la baja. | Secuencias (N velas al alza/baja, máximos crecientes). | global del estilo |
| `IsFalling` | 1 | Comparador | A baja durante N velas. | Secuencias (N velas al alza/baja, máximos crecientes). | global del estilo |
| `IsGreater` | 1 | Comparador | A > B. | Secuencias (N velas al alza/baja, máximos crecientes). | global del estilo |
| `IsGreaterCount` | 1 | Comparador | A > B durante N velas seguidas. | Secuencias (N velas al alza/baja, máximos crecientes). | global del estilo |
| `IsLower` | 1 | Comparador | A < B. | Secuencias (N velas al alza/baja, máximos crecientes). | global del estilo |
| `IsLowerCount` | 1 | Comparador | A < B durante N velas seguidas. | Secuencias (N velas al alza/baja, máximos crecientes). | global del estilo |
| `IsRising` | 1 | Comparador | A sube durante N velas. | Secuencias (N velas al alza/baja, máximos crecientes). | global del estilo |
| `Stop/Limit Price Levels.High` | 3 | Precio de orden stop/limit | Precio de la orden = máximo de una vela (vela señal). | Stop sobre el máximo de la vela señal (confirmación clásica). | global del estilo |
| `Stop/Limit Price Levels.Fractal` | 1 | Precio de orden stop/limit | Precio = último fractal. | Stop sobre el máximo de la vela señal (confirmación clásica). | global del estilo |
| `Stop/Limit Price Levels.HighD` | 1 | Precio de orden stop/limit | Precio = máximo del día anterior. | Stop sobre el máximo de la vela señal (confirmación clásica). | global del estilo |
| `Stop/Limit Price Levels.Highest` | 1 | Precio de orden stop/limit | Precio de la orden = máximo de N velas. | Stop sobre el máximo de la vela señal (confirmación clásica). | global del estilo |
| `Stop/Limit Price Levels.Low` | 1 | Precio de orden stop/limit | Precio de la orden = mínimo de una vela. | Stop sobre el máximo de la vela señal (confirmación clásica). | global del estilo |
| `Stop/Limit Price Levels.OpenD` | 1 | Precio de orden stop/limit | Precio = apertura diaria. | Stop sobre el máximo de la vela señal (confirmación clásica). | global del estilo |
| `Stop/Limit Price Ranges.BarRange` | 2 | Desplazamiento de orden | Desplazamiento = k·rango de la vela. | Margen en rango de vela/ATR. | global del estilo |
| `Stop/Limit Price Ranges.ATR` | 1 | Desplazamiento de orden | Desplazamiento del precio de la orden = k·ATR. | Margen en rango de vela/ATR. | global del estilo |
| `Stop/Limit Price Ranges.SmallestRange` | 1 | Desplazamiento de orden | Desplazamiento = k·rango mínimo de N velas (contracción). | Margen en rango de vela/ATR. | global del estilo |

### 4. Timeframe, símbolos y horarios

- **Timeframe:** H1.
- **Instrumento recomendado:** Cualquier mercado líquido; mejor en índices y mayores. GBPJPY apto.
- **Horario:** Entradas 01:30-23:30 servidor (la ventana del original: evita el rollover). El rango 'asiático' de los bloques de sesión es 01:00-03:00 → 08:00-10:00.

### 5. Salidas y gestión del riesgo

SL 1-2,5 ATR(14-50); objetivo 1,5-4 ATR con PT = 150-300 % del SL; break-even 1-2 ATR (50 %); salida temporal 5-30 h (30 %); regla (30 %). Riesgo 1 %; 2 entradas/día.

### 6. Filtros y ranking

| Archivo | Fitness | Filtros |
|---|---|---|
| `Estrategia_Build_ConfigInicial_H1_BUY__PriceAction_H1` | Weighted: ReturnDDRatio (peso 2, max), SQN (peso 1, max) | NumberOfTrades(IS) >= 200; ReturnDDRatio(IS) >= 4; WinningPct(IS) >= 40; ProfitFactor(IS) >= 1.3; AvgBarsInTrade(IS) >= 2; NetProfit(OOS) > 0; ProfitFactor(OOS) >= 1.1 |
| `Estrategia_Retest_ConfigInicial_H1_BUY__PriceAction_H1` | Weighted: ReturnDDRatio (peso 2, max), SQN (peso 1, max) | NetProfit(OOS) > 0; ProfitFactor(OOS) >= 1.1; ReturnDDRatio(Full) >= 6; NumberOfTrades(Full) >= 300; DrawdownPct(Full) <= 20 |
| `Ventaja_Build_ConfigInicial_H1_BUY__PriceAction_H1` | Weighted: SQN (peso 2, max), StagnationPct (peso 1, min) | NumberOfTrades(IS) >= 200; ReturnDDRatio(IS) >= 2; WinningPct(IS) >= 35; ProfitFactor(IS) >= 1.15; AvgBarsInTrade(IS) >= 2; NetProfit(OOS) > 0 |
| `Ventaja_Retest_ConfigInicial_H1_BUY__PriceAction_H1` | Weighted: SQN (peso 2, max), StagnationPct (peso 1, min) | NetProfit(OOS) > 0; ProfitFactor(Full) >= 1.1; NumberOfTrades(Full) >= 300 |

Justificación: Ret/DD + SQN (consistencia por operación). Los umbrales reflejan la frecuencia y el acierto típicos del estilo (no se usa el 40 % de acierto ni las 300 operaciones del original para todos).

### 7. Motor y robustez

- **Builder:** población 40 × 4 islas, 40 generaciones, cruce 80 %, mutación 30 %, migración 10 % cada 10, reinicio por estancamiento a 15.
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

**Archivos del kit** (todos *no validados en SQX*):

- `configs/NewsProxy/Estrategia_Build_ConfigInicial_H1_BUY__NewsProxy_M15.cfx` — tabla completa de cambios: [`docs/cambios/Estrategia_Build_ConfigInicial_H1_BUY__NewsProxy_M15.md`](cambios/Estrategia_Build_ConfigInicial_H1_BUY__NewsProxy_M15.md)
- `configs/NewsProxy/Estrategia_Retest_ConfigInicial_H1_BUY__NewsProxy_M15.cfx` — tabla completa de cambios: [`docs/cambios/Estrategia_Retest_ConfigInicial_H1_BUY__NewsProxy_M15.md`](cambios/Estrategia_Retest_ConfigInicial_H1_BUY__NewsProxy_M15.md)
- `configs/NewsProxy/Ventaja_Build_ConfigInicial_H1_BUY__NewsProxy_M15.cfx` — tabla completa de cambios: [`docs/cambios/Ventaja_Build_ConfigInicial_H1_BUY__NewsProxy_M15.md`](cambios/Ventaja_Build_ConfigInicial_H1_BUY__NewsProxy_M15.md)
- `configs/NewsProxy/Ventaja_Retest_ConfigInicial_H1_BUY__NewsProxy_M15.cfx` — tabla completa de cambios: [`docs/cambios/Ventaja_Retest_ConfigInicial_H1_BUY__NewsProxy_M15.md`](cambios/Ventaja_Retest_ConfigInicial_H1_BUY__NewsProxy_M15.md)

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
| Tipos de orden | EnterAtMarket (w1) | EnterAtMarket (w1), EnterAtStop (w3, válida 1-4 velas) | Stop sobre el rango pre-dato, caduca en 15-60 min. |
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
| Bloques activos | 146 señales / 29 indicadores / 29 stop-limit | 8 señales / 14 indicadores / 6 stop-limit | Rango previo a la publicación (12:00-15:00 → 15:00/15:30) y filtros de hora/día; expansión de volatilidad como confirmación. |
| Gestión monetaria | FixedAmount: riesgo 100 por operación | FixedAmount: riesgo 50 por operación | Riesgo fijo 0.5 % (no compuesto: Ret/DD comparable en el tiempo). |
| Fitness | type="ReturnDDRatio" | Weighted: ProfitFactor (peso 1, max), ReturnDDRatio (peso 2, max) | Pocas operaciones con mucha varianza: PF + Ret/DD. |
| Filtros (Ranking) | AvgBarsInTrade(IS) >= 2; ReturnDDRatio(IS) >= 8; NumberOfTrades(IS) >= 300; WinningPct(IS) >= 40 | NumberOfTrades(IS) >= 250; ReturnDDRatio(IS) >= 3; WinningPct(IS) >= 35; ProfitFactor(IS) >= 1.3; AvgBarsInTrade(IS) >= 2; NetProfit(OOS) > 0; ProfitFactor(OOS) >= 1.05 | Umbrales del estilo + exigencia OOS. |
| Filtro población inicial | ReturnDDRatio(IS) >= 5; AvgBarsInTrade(IS) >= 2; NumberOfTrades(IS) >= 250; WinningPct(IS) >= 35 | ReturnDDRatio(IS) >= 1.88; AvgBarsInTrade(IS) >= 2; NumberOfTrades(IS) >= 207; WinningPct(IS) >= 30 | Misma proporción que el autor (≈60 % Ret/DD, ≈83 % operaciones, -5 puntos de acierto). |
| Motor genético | población 5 × 5 islas, 10 generaciones, cruce 46 %, mutación 35 %, migración 6 % cada 5, reinicio por estancamiento a 30 | población 30 × 4 islas, 30 generaciones, cruce 80 %, mutación 30 %, migración 10 % cada 10, reinicio por estancamiento a 15 | Población y generaciones del original insuficientes para que la evolución actúe (Fase 1 §6). |

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
| Tipos de orden | EnterAtMarket (w1) | EnterAtMarket (w1), EnterAtStop (w3, válida 1-4 velas) | Stop sobre el rango pre-dato, caduca en 15-60 min. |
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
| Bloques activos | 146 señales / 29 indicadores / 29 stop-limit | 8 señales / 14 indicadores / 6 stop-limit | Rango previo a la publicación (12:00-15:00 → 15:00/15:30) y filtros de hora/día; expansión de volatilidad como confirmación. |
| Gestión monetaria | FixedSize: 1 lote | FixedSize: 1 lote | Sin cambio. |
| Fitness | Weighted: Stagnation (peso 1, min) | Weighted: SQN (peso 2, max), StagnationPct (peso 1, min) | SQN mide la calidad estadística de la entrada; el original optimizaba sólo 'Stagnation', que ignora el beneficio. |
| Filtros (Ranking) | AvgBarsInTrade(IS) >= 2; ReturnDDRatio(IS) >= 4; NumberOfTrades(IS) >= 300; WinningPct(IS) >= 40 | NumberOfTrades(IS) >= 250; ReturnDDRatio(IS) >= 1.5; WinningPct(IS) >= 30; ProfitFactor(IS) >= 1.15; AvgBarsInTrade(IS) >= 2; NetProfit(OOS) > 0 | Umbrales del estilo + exigencia OOS. Test de ventaja: Ret/DD a la mitad y PF ≥1,15. |
| Filtro población inicial | ReturnDDRatio(IS) >= 2; AvgBarsInTrade(IS) >= 2; NumberOfTrades(IS) >= 250; WinningPct(IS) >= 35 | ReturnDDRatio(IS) >= 0.75; AvgBarsInTrade(IS) >= 2; NumberOfTrades(IS) >= 207; WinningPct(IS) >= 25 | Misma proporción que el autor (≈60 % Ret/DD, ≈83 % operaciones, -5 puntos de acierto). |
| Motor genético | población 15 × 5 islas, 10 generaciones, cruce 46 %, mutación 35 %, migración 6 % cada 5, reinicio por estancamiento a 30 | población 30 × 4 islas, 30 generaciones, cruce 80 %, mutación 30 %, migración 10 % cada 10, reinicio por estancamiento a 15 | Población y generaciones del original insuficientes para que la evolución actúe (Fase 1 §6). |

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
| Filtros (Ranking) | (ninguna activa) | NetProfit(OOS) > 0; ProfitFactor(OOS) >= 1.05; ReturnDDRatio(Full) >= 4.5; NumberOfTrades(Full) >= 375; DrawdownPct(Full) <= 20 | El original no filtraba nada (todas use=false) ni borraba fallidas. |
| Mayor precisión | activo; precisión 2 (tick real + spread personalizado); 1 condiciones | activo; precisión 3 (tick real + spread real); 3 condiciones | Spread aleatorio hasta 4x y deslizamiento hasta 3 pips: así es una publicación real. |
| Monte Carlo retest | activo; 1000 sims; OHLC ±10 % ATR(14), spread 1-3. Acepta: NetProfit(IS) >= 0 | activo; 200 sims; OHLC ±10 % ATR(14), desliz. 0-3, spread 2-8. Acepta: NetProfit(Full) >= 0; DrawdownPct(Full) <= 150% de DrawdownPct[main] | Spread desde el base hasta 2-4x, deslizamiento, percentil 95 (no el peor caso) y control del DD. |
| Monte Carlo manipulación | no; orden de operaciones 'exact', saltar 10 % | activo; orden de operaciones 'resampling', saltar 10 % | Barato; 'resampling' y referencia corregida (el original comparaba MC contra MC). |
| SPP / perfil de optimización | activo; 15000 tests, ±20 %, 6 pasos; ≥95 % rentables | activo; 1500 tests, ±20 %, 6 pasos; ≥80 % rentables | Tests y exigencia ajustados al coste de cómputo y a la sensibilidad del estilo. |
| What-if | no; ExcludePctTradesWithBiggestPl, ExcludePctTradesWithLowestPl | activo; ExcludePctTradesWithBiggestPl, ExcludePctTradesWithLowestPl | Quitar el 5 % de extremos: el estilo no debe depender de outliers. |

Diferencias del `Ventaja_Retest` respecto al anterior:

- **Gestión monetaria:** FixedSize: 1 lote
- **Fitness:** Weighted: SQN (peso 2, max), StagnationPct (peso 1, min)
- **Filtros (Ranking):** NetProfit(OOS) > 0; ProfitFactor(Full) >= 1.1; NumberOfTrades(Full) >= 375

### 3. Indicadores y bloques seleccionados

Criterio general: Rango previo a la publicación (12:00-15:00 → 15:00/15:30) y filtros de hora/día; expansión de volatilidad como confirmación. El original activaba 146 señales + 29 indicadores + 29 niveles stop/limit genéricos con peso 1; aquí sólo los coherentes con la tesis, con peso mayor en los centrales (w2-w3).

| Bloque | Peso | Familia | Qué mide | Por qué en este estilo | Rango específico |
|---|---|---|---|---|---|
| `BarOpensAboveHighestAfterOpenBelow` | 2 | Ruptura de nivel | La vela abre por encima del máximo de N velas tras abrir por debajo (ruptura Donchian confirmada en apertura). | Ruptura del rango previo a la publicación. | global del estilo |
| `BBBarOpensAboveUpAfterOpenBelow` | 1 | Ruptura de nivel | Cruce de apertura por encima de la banda superior de Bollinger. | Ruptura del rango previo a la publicación. | global del estilo |
| `KCBarOpensAboveUpperAfterOpenBelow` | 1 | Ruptura de nivel | Cruce de apertura por encima de la banda superior de Keltner (ATR). | Ruptura del rango previo a la publicación. | global del estilo |
| `ATRRising` | 2 | Volatilidad | ATR creciente: expansión de volatilidad (sin nivel absoluto). | La publicación se manifiesta como expansión súbita de rango. | global del estilo |
| `ATRChangesUp` | 1 | Volatilidad | El ATR cambia de dirección al alza. | La publicación se manifiesta como expansión súbita de rango. | global del estilo |
| `Indicators.ATR` | 1 | Volatilidad | ATR: rango medio verdadero. | La publicación se manifiesta como expansión súbita de rango. | global del estilo |
| `Indicators.TrueRange` | 1 | Volatilidad | Rango verdadero de la vela. | La publicación se manifiesta como expansión súbita de rango. | global del estilo |
| `StdDevRising` | 1 | Volatilidad | Desviación típica creciente. | La publicación se manifiesta como expansión súbita de rango. | global del estilo |
| `BarHourIs` | 2 | Tiempo | La vela es de una hora concreta. | Aproximación al calendario: hora (15-16) y día de la semana. | Hour 15 a 16 (paso 1) |
| `BarDayOfWeekIs` | 1 | Tiempo | Día de la semana concreto. | Aproximación al calendario: hora (15-16) y día de la semana. | global del estilo |
| `Indicators.HighestInRange` | 3 | Nivel de referencia | Máximo entre dos horas del día (rango horario, p. ej. asiático). | Rango 12:00-15:00 → 15:00/15:30 (pre-dato). | Time From 1200 a 1500 (paso 100); Time To 1500 a 1530 (paso 30) |
| `Indicators.Highest` | 1 | Nivel de referencia | Máximo de N velas (canal Donchian). | Rango 12:00-15:00 → 15:00/15:30 (pre-dato). | global del estilo |
| `Indicators.Lowest` | 1 | Nivel de referencia | Mínimo de N velas. | Rango 12:00-15:00 → 15:00/15:30 (pre-dato). | global del estilo |
| `Indicators.LowestInRange` | 1 | Nivel de referencia | Mínimo entre dos horas del día. | Rango 12:00-15:00 → 15:00/15:30 (pre-dato). | Time From 1200 a 1500 (paso 100); Time To 1500 a 1530 (paso 30) |
| `Prices.Close` | 1 | Precio | Cierre. | Comparaciones. | global del estilo |
| `Prices.High` | 1 | Precio | Máximo. | Comparaciones. | global del estilo |
| `Prices.Low` | 1 | Precio | Mínimo. | Comparaciones. | global del estilo |
| `Prices.Open` | 1 | Precio | Apertura. | Comparaciones. | global del estilo |
| `CrossesAbove` | 1 | Comparador | A cruza B al alza. | Condiciones. | global del estilo |
| `CrossesBelow` | 1 | Comparador | A cruza B a la baja. | Condiciones. | global del estilo |
| `IsGreater` | 1 | Comparador | A > B. | Condiciones. | global del estilo |
| `IsLower` | 1 | Comparador | A < B. | Condiciones. | global del estilo |
| `Stop/Limit Price Levels.HighestInRange` | 3 | Precio de orden stop/limit | Precio = máximo de un rango horario. | Stop sobre el rango pre-dato. | Time From 1200 a 1500 (paso 100); Time To 1500 a 1530 (paso 30) |
| `Stop/Limit Price Levels.High` | 1 | Precio de orden stop/limit | Precio de la orden = máximo de una vela (vela señal). | Stop sobre el rango pre-dato. | global del estilo |
| `Stop/Limit Price Levels.Highest` | 1 | Precio de orden stop/limit | Precio de la orden = máximo de N velas. | Stop sobre el rango pre-dato. | global del estilo |
| `Stop/Limit Price Ranges.ATR` | 2 | Desplazamiento de orden | Desplazamiento del precio de la orden = k·ATR. | Margen en ATR/rango verdadero para evitar el primer pico. | global del estilo |
| `Stop/Limit Price Ranges.BarRange` | 1 | Desplazamiento de orden | Desplazamiento = k·rango de la vela. | Margen en ATR/rango verdadero para evitar el primer pico. | global del estilo |
| `Stop/Limit Price Ranges.TrueRange` | 1 | Desplazamiento de orden | Desplazamiento = k·rango verdadero. | Margen en ATR/rango verdadero para evitar el primer pico. | global del estilo |

### 4. Timeframe, símbolos y horarios

- **Timeframe:** M15.
- **Instrumento recomendado:** EURUSD/USDJPY/oro/US30 (reaccionan a datos de EE. UU.). Exige datos tick con spread real.
- **Horario:** Rango pre-dato 12:00-15:00 → 15:00/15:30; señales 15:00-17:00 servidor (8:00-10:00 ET con la convención S5); `BarHourIs` 15-16; cierre 22:00 (viernes 21:00); una operación/día.

### 5. Salidas y gestión del riesgo

SL 1-2 ATR(10-40) de M15; objetivo opcional 1,5-4 ATR; break-even 0,5-1,5 ATR (50 %); salida temporal 2-16 velas = 30 min-4 h (70 %). Riesgo 0,5 %.

### 6. Filtros y ranking

| Archivo | Fitness | Filtros |
|---|---|---|
| `Estrategia_Build_ConfigInicial_H1_BUY__NewsProxy_M15` | Weighted: ProfitFactor (peso 1, max), ReturnDDRatio (peso 2, max) | NumberOfTrades(IS) >= 250; ReturnDDRatio(IS) >= 3; WinningPct(IS) >= 35; ProfitFactor(IS) >= 1.3; AvgBarsInTrade(IS) >= 2; NetProfit(OOS) > 0; ProfitFactor(OOS) >= 1.05 |
| `Estrategia_Retest_ConfigInicial_H1_BUY__NewsProxy_M15` | Weighted: ProfitFactor (peso 1, max), ReturnDDRatio (peso 2, max) | NetProfit(OOS) > 0; ProfitFactor(OOS) >= 1.05; ReturnDDRatio(Full) >= 4.5; NumberOfTrades(Full) >= 375; DrawdownPct(Full) <= 20 |
| `Ventaja_Build_ConfigInicial_H1_BUY__NewsProxy_M15` | Weighted: SQN (peso 2, max), StagnationPct (peso 1, min) | NumberOfTrades(IS) >= 250; ReturnDDRatio(IS) >= 1.5; WinningPct(IS) >= 30; ProfitFactor(IS) >= 1.15; AvgBarsInTrade(IS) >= 2; NetProfit(OOS) > 0 |
| `Ventaja_Retest_ConfigInicial_H1_BUY__NewsProxy_M15` | Weighted: SQN (peso 2, max), StagnationPct (peso 1, min) | NetProfit(OOS) > 0; ProfitFactor(Full) >= 1.1; NumberOfTrades(Full) >= 375 |

Justificación: Pocas operaciones con mucha varianza: PF + Ret/DD. Los umbrales reflejan la frecuencia y el acierto típicos del estilo (no se usa el 40 % de acierto ni las 300 operaciones del original para todos).

### 7. Motor y robustez

- **Builder:** población 30 × 4 islas, 30 generaciones, cruce 80 %, mutación 30 %, migración 10 % cada 10, reinicio por estancamiento a 15.
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

