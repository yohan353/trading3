# Plantillas SQX de breakout: ingeniería inversa y adaptación a 8 estilos

Análisis de cuatro configuraciones de **StrategyQuant X** (Builder y Retester, build 140.2099) diseñadas para
estrategias de ruptura en H1 sólo compras, y su adaptación a Scalping, Day Trading, Swing, Position, Trend Following,
Range, Price Action y Noticias (aproximación horaria).

Empieza por el **[resumen ejecutivo](docs/05_Resumen_Ejecutivo.md)**.

## Documentos (por fases)

| Fase | Documento | Contenido |
|---|---|---|
| 0 | [docs/00_Fase0_Inventario.md](docs/00_Fase0_Inventario.md) | Inventario, formato, legibilidad, coherencia con la build 144 |
| 1 | [docs/01_Fase1_Ingenieria_Inversa.md](docs/01_Fase1_Ingenieria_Inversa.md) | Deconstrucción de cada archivo (A explícito / B deducido / C no determinable), errores y malas prácticas |
| 2 | [docs/02_Fase2_Matriz_Viabilidad.md](docs/02_Fase2_Matriz_Viabilidad.md) | Matriz archivo × estilo con motivos y alternativas |
| 3 | [docs/03_Fase3_Fichas_Diseno.md](docs/03_Fase3_Fichas_Diseno.md) | Preguntas, supuestos y una ficha por estilo (tesis, cambios, bloques, salidas, filtros, motor, riesgos, validación) |
| 4 | [docs/04_Fase4_Guia_Manual_y_Checklist.md](docs/04_Fase4_Guia_Manual_y_Checklist.md) | **Guía manual paso a paso (entregable principal)** y lista de verificación al importar |
| — | [docs/cambios/](docs/cambios/) | Tabla de cambios (original → nuevo → justificación) de cada uno de los 32 archivos |
| — | [docs/validacion/informe_validacion.md](docs/validacion/informe_validacion.md) | Validación estática de los 32 archivos |

## Archivos de configuración

`configs/<Estilo>/<NombreOriginal>__<Estilo>_<TF>.cfx` — 4 por estilo (Builder y Retester de *ventaja* y de
*estrategia*). **Son experimentales y no se han abierto en SQX**: se generaron modificando sólo valores de los
originales y superan una validación estática (estructura, catálogo de bloques, rangos, fechas), pero eso no garantiza
que la build 144 los importe sin avisos. Si alguno falla, aplica los valores a mano con la guía de la Fase 4.

## Regenerar

Los `.cfx` originales **no están en este repositorio** (público; material de un tercero). Cópialos en `originales/`
(`Estrategia_Build_…`, `Estrategia_Retest_…`, `Ventaja_Build_…`, `Ventaja_Retest_ConfigInicial_H1_BUY.cfx`) y ejecuta:

```bash
bash tools/regenerar_todo.sh
```

| Script | Función |
|---|---|
| `tools/estilos.py` | Especificación de cada estilo con la justificación de cada valor (editar aquí los supuestos) |
| `tools/generar_cfx.py` | Aplica los estilos a los originales, escribe `configs/` y `docs/cambios/`; falla si algún cambio no queda registrado |
| `tools/validar_cfx.py` | Validación estática e informe |
| `tools/generar_fichas.py`, `tools/generar_guia.py` | Generan las Fases 3 y 4 leyendo los `.cfx` resultantes |

Requiere sólo Python 3.9+ (biblioteca estándar).

## Aviso

Nada de este material promete rentabilidad. Los resultados dependen de los datos, los costes reales y la validación
fuera de muestra.
