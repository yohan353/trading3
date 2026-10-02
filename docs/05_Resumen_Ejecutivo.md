# Resumen ejecutivo

**Qué son los archivos.** Cuatro configuraciones de StrategyQuant X de la **build 140.2099** (no 144), en formato ZIP
con un `config.xml` legible y completo: dos **Builders** y dos **Retesters** que forman un flujo en dos etapas de un
curso de formación diseñado para **US30 H1, sólo compras**: (1) `Ventaja_Build` busca entradas con ventaja usando sólo
una salida por tiempo; (2) `Ventaja_Retest` las valida; (3) `Estrategia_Build` construye SL/PT/trailing sobre una
**plantilla `.sqx` externa que no se ha recibido**; (4) `Estrategia_Retest` valida con el periodo 2021-2024 nunca visto.

**Hallazgos principales**

1. **La lógica de breakout no está en lo recibido.** En `Estrategia_Build` vive en la plantilla externa (no
   reproducible); en `Ventaja_Build` no se impone: 146 señales genéricas con el mismo peso, sólo órdenes a mercado, y
   apenas un 8-11 % de las señales son rupturas.
2. **Costes incorrectos:** los datos son de GBPJPY pero swap, triple swap (viernes) y comisión son del US30 en
   Darwinex; deslizamiento 0 en los cuatro archivos.
3. **Motor genético inoperante:** población 5-15, 10 generaciones, migración nula en la práctica y reinicio por
   estancamiento inalcanzable → búsqueda casi aleatoria.
4. **Validación incompleta:** los Builders no tienen OOS (filtran y puntúan sobre la misma muestra) y los Retest no
   filtran nada ni borran las fallidas; hay errores en condiciones inactivas (MC contra MC, muestras mezcladas en SPP,
   "mercado adicional" = el mismo GBPJPY).
5. **Ruido estructural:** bloques con niveles absolutos dependientes de la escala de precio, osciladores sin restringir y
   patrones bajistas como entrada larga.
6. **Aciertos a conservar:** arquitectura ventaja → estrategia, *holdout* 2021-2024, SL en ATR con riesgo fijo no
   compuesto, ventana anti-rollover, retest con tick real, Monte Carlo de OHLC y SPP.

**Viabilidad (32 combinaciones × BUY/SELL).** Todas configurables. Swing y Trend Following (en H1) encajan casi
directamente; Day Trading, Range y Price Action requieren cambios estructurales (órdenes stop/límite, cierres, paleta de
bloques); Position queda **condicionado a más datos** y a un límite físico de ~20 operaciones/año por mercado; Scalping
sólo como **aproximación en M5** (el de ticks no es representable) y News Trading sólo como **aproximación horaria**
(SQX no tiene calendario económico).

**Revisión 2 de los archivos:** (1) paletas amplias de 26-119 señales, 37-52 indicadores y 26-40 niveles stop/limit por
estilo (núcleo con peso alto + filtros a peso 1, sin bloques de nivel absoluto); (2) mínimo de operaciones por densidad
(≥41/año como el original; 45-300/año según estilo, salvo Position 20/año) en IS, OOS y Retest; (3) kits **SELL** con
`Market sides = short` y bloques/niveles espejados.

**Qué se entrega**

| Entregable | Dónde | Estado |
|---|---|---|
| A) Análisis por archivo | `docs/00_*`, `docs/01_*` | Completo |
| B) Matriz de viabilidad | `docs/02_*` | Completo |
| C) 8 fichas de diseño (64 configuraciones) | `docs/03_*` | Completo, con preguntas y supuestos explícitos |
| D) **Guía manual paso a paso** (opción principal) | `docs/04_*` §A | Completo |
| D) 64 `.cfx` **experimentales, no validados en SQX** (32 BUY + 32 SELL) | `configs/` + `docs/cambios/` | Validación estática superada (`docs/validacion/`) |
| E) Lista de verificación | `docs/04_*` §E | Completo |
| Herramientas para regenerar todo | `tools/` | Reproducible |

**Riesgos que no desaparecen con ninguna configuración:** sesgo de minería de datos (miles de candidatas probadas),
costes reales distintos de los modelados, cambio de régimen de mercado y dependencia del horario del servidor.
**Ninguna de estas configuraciones garantiza rentabilidad**; sólo aumentan la probabilidad de descartar estrategias frágiles.

**Siguientes pasos recomendados**

1. Responder a las 5 preguntas de docs/03 (instrumento/bróker, datos tick y zona horaria, capital/DD, dirección/
   plataforma, calendario de noticias) y ajustar `tools/estilos.py` en consecuencia.
2. Corregir símbolo y costes en los kits que vayas a usar (checklist E.1, puntos 2-4).
3. Empezar por el kit **Swing** (el más cercano al original), BUY y SELL: cargarlo, verificarlo con la checklist (en SELL,
   comprobar que la dirección es *Short only*) y hacer una prueba corta de 15 minutos.
4. Ejecutar siempre primero **Ventaja_Build → Ventaja_Retest**; si no hay entradas con ventaja robusta, no pasar a
   construir salidas.
5. Para las supervivientes: `Estrategia_Build → Estrategia_Retest`, Walk-Forward Matrix en el Optimizer (docs/04 §A.4)
   y retest en otros mercados.
6. Antes de dinero real: demo/forward de 2-3 meses (intradía) o 6-12 meses (swing/position), comparando deslizamiento y
   spread reales con los modelados.
