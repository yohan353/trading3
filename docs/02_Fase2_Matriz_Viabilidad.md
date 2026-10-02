# Fase 2 — Matriz de viabilidad [archivo × estilo]

## Criterios

- **Viable (V):** la arquitectura del archivo encaja con el estilo; basta reparametrizar (timeframe, rangos, umbrales).
- **Viable con cambios (VC):** hace falta un cambio estructural (tipos de orden, lógica de salida, horario, datos
  adicionales) o hay una advertencia que condiciona el resultado.
- **No viable (NV):** SQX no puede representar el estilo de forma fiel; se propone la alternativa más cercana.

Cambio transversal (no depende del estilo): `Estrategia_Build` usa una plantilla `.sqx` que no se ha recibido. Todas
sus versiones pasan a modo `simple` (autónomo); el modo plantilla sigue siendo posible siguiendo docs/04 §A.3.

### Horizonte y costes por estilo

| Estilo | Timeframe elegido | Mantenimiento típico | Operaciones/año esperables | Coste (spread 2 pips GBPJPY) / ATR del TF (B, orden de magnitud) | Sensibilidad a costes |
|---|---|---|---|---|---|
| Scalping | M5 | 15 min – 3 h | 200-600 | ≈ 20-40 % del ATR(M5) | **Extrema** |
| Day Trading | M15 | 1 – 10 h, plano al cierre | 80-200 | ≈ 13-20 % del ATR(M15) | Alta |
| Swing | H4 | 2 – 10 días | 20-60 | ≈ 3 % del ATR(H4) | Baja (swap relevante) |
| Position | D1 | 1 – 12 meses | 4-10 | ≈ 1-2 % del ATR(D1) | Muy baja (swap dominante) |
| Trend Following | H4 | 1 – 6 semanas | 15-40 | ≈ 3 % | Baja |
| Range | H1 | 3 – 30 h | 40-120 | ≈ 6-10 % del ATR(H1) | Media |
| Price Action | H1 | 3 – 30 h | 40-120 | ≈ 6-10 % | Media |
| Noticias (proxy) | M15 | 30 min – 4 h | 100-250 | spread y deslizamiento reales ×3-×10 en la publicación | **Extrema** |

(Los ATR de GBPJPY 2013-2024 se han estimado por orden de magnitud: M5 ≈ 5-10 pips, M15 ≈ 10-15, H1 ≈ 20-35, H4 ≈ 50-80,
D1 ≈ 100-150. Compruébalos con tus datos; la conclusión cualitativa no cambia.)

## Matriz

| Archivo \ Estilo | Scalping | Day Trading | Swing | Position | Trend Following | Range | Price Action | Noticias |
|---|---|---|---|---|---|---|---|---|
| **Estrategia_Build** (Builder estrategia) | VC ¹ | VC ² | V | VC ⁴ | V | VC ⁶ | VC ⁷ | NV → VC (proxy) ⁸ |
| **Estrategia_Retest** (Retester estrategia) | VC ¹ | V | V | VC ⁴ | V | V | V | VC (proxy) ⁸ |
| **Ventaja_Build** (Builder test de ventaja) | VC ¹ | VC ² | V | VC ⁴ | VC ⁵ | VC ⁶ | VC ⁷ | NV → VC (proxy) ⁸ |
| **Ventaja_Retest** (Retester test de ventaja) | VC ¹ | V | V | VC ⁴ | V | V | V | VC (proxy) ⁸ |

### Motivos

1. **Scalping.** SQX trabaja con barras (mínimo M1 para construir); el scalping de segundos/ticks (libro de órdenes,
   latencia, cola de órdenes) **no es representable** → alternativa más cercana: micro-rupturas en **M5** durante la
   sesión líquida. Exige: datos **tick con spread real** para el Retest (precisión 3), instrumento con spread bruto muy
   bajo (EURUSD, US500), deslizamiento modelado y estrés de costes. Con GBPJPY y 2 pips de spread el coste es 20-40 % del
   ATR de M5: aunque se configure, lo más probable es no encontrar nada robusto. Los Retest se adaptan cambiando la
   precisión y el estrés de spread/deslizamiento; el test de ventaja sigue teniendo sentido (salida 15 min-2 h), pero
   con costes reales incluidos o dará falsos positivos.
2. **Day Trading.** Encaja muy bien con la ruptura (rango asiático/apertura de Londres) pero exige cambios
   estructurales en el Builder: órdenes **stop** en el nivel (el original sólo entra a mercado), cierre obligatorio al
   final del día (`ExitAtEndOfDay`), rangos horarios en horas válidas, M15. Los Retest sólo cambian timeframe/opciones.
3. **Swing.** El estilo más cercano al original (H1 con SL/PT en ATR y mantenimiento de horas a días): basta pasar a
   H4 y reparametrizar.
4. **Position.** Técnicamente representable (D1, salidas por trailing/tiempo), pero con los datos 2013-2024 un sistema
   de meses hace 40-90 operaciones: estadística insuficiente para un Builder genético (riesgo de minería de datos
   extremo) y para el Monte Carlo de manipulación. Viable **si se amplían los datos (≥15-20 años) y se valida en varios
   mercados**. El swap pasa a ser una parte principal del resultado (y el del original es incorrecto).
5. **Trend Following (test de ventaja).** El Builder y los Retest encajan (H4, trailing). Pero el test de ventaja con
   **salida a tiempo fijo trunca la cola derecha**, que es justo donde está la ventaja del seguimiento de tendencia:
   puede rechazar entradas válidas. Se compensa alargando la salida temporal (2-10 días) y, si hace falta, con un test
   alternativo de ventaja con trailing como única salida.
6. **Range.** Es la lógica opuesta a la del original (reversión, no ruptura): órdenes **límite**, objetivo corto
   obligatorio, osciladores restringidos a sobreventa y filtros de régimen lateral. GBPJPY es tendencial: el símbolo
   debería cambiarse (EURCHF/EURGBP/AUDNZD). Los Retest sólo cambian el what-if (exclusión de extremos).
7. **Price Action.** Requiere sustituir casi toda la paleta de bloques (sólo velas, precio y estructura, sin
   indicadores salvo ATR como normalizador) y permitir desplazamiento 1-3 para patrones de varias velas.
8. **Noticias.** SQX **no incluye calendario económico** ni datos de eventos, y sus datos M1 no reflejan el spread ni el
   deslizamiento reales de una publicación → **news trading real: no viable de forma nativa**. Alternativa más cercana
   (entregada como *NewsProxy*): ruptura del rango previo dentro de la **ventana horaria de los datos de EE. UU.**
   (8:30 ET = 15:30 servidor con la convención S5), con filtros de hora/día y expansión de volatilidad.

   **Qué se pierde con la aproximación horaria:**
   - Qué días hay publicación y su importancia (la estrategia opera la ventana todos los días).
   - La sorpresa (dato frente a consenso), que es lo que mueve el precio.
   - Horarios irregulares: FOMC (14:00 ET), festivos, cambios de fecha, y el desfase de 1-3 semanas entre el cambio de
     hora de EE. UU. y el europeo.
   - El ensanchamiento real del spread, el deslizamiento y los huecos de liquidez (sólo se aproximan por Monte Carlo).

   **Alternativas más fieles (fuera de lo entregado):** (a) indicador/bloque personalizado en Java que lea un CSV de
   eventos (requiere programación en SQX y reimplementarlo en la plataforma de ejecución; MQL5 dispone de funciones de
   calendario económico); (b) construir sin noticias y usar el calendario sólo como filtro de "no operar" en el EA.

## Módulo frente a estilo

- **Builder:** útil en los 8 estilos (en Noticias, como proxy).
- **Retester:** útil en los 8; los cambios son de parámetros (precisión, estrés de costes, umbrales).
- **Optimizer:** no se recibió ningún archivo de Optimizer. El Walk-Forward Matrix es especialmente importante en Day
  Trading, Swing, Trend y Range; se describe cómo configurarlo a mano en docs/04 §A.4. En Position no es fiable
  (pocas operaciones por ventana) y se sustituye por SPP + multi-mercado.

## Conclusión de la fase

Las 32 combinaciones se pueden configurar en SQX; ninguna se descarta, pero dos se entregan **explícitamente como
aproximaciones** (Scalping en M5 y Noticias por ventana horaria) y una (Position) queda **condicionada a disponer de más
datos**. Antes de diseñar se formulan las preguntas abiertas y los supuestos (docs/03, al inicio).
