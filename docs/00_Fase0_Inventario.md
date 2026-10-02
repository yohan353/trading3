# Fase 0 — Inspección y validación de los archivos recibidos

Convención usada en todo el análisis:

- **(A) Explícito**: valor leído literalmente en el archivo (se cita el nodo/atributo).
- **(B) Deducido**: inferencia, con grado de confianza *alta / media / baja*.
- **(C) No determinable**: no se puede saber con lo recibido.

## a) Inventario

| # | Archivo (nombre recibido) | Ext. | Tamaño `.cfx` | Contenido | Fecha interna del ZIP | `Task@type` | Módulo SQX | `Task@version` |
|---|---|---|---|---|---|---|---|---|
| 1 | `Estrategia_Build_ConfigInicial_H1_BUY.cfx` (recibido como `b00cf192-…`) | .cfx | 37.319 B | `config.xml` 1.840.169 B | 2024-11-14 06:52 | `Build` | **Builder** | `140.2099` |
| 2 | `Estrategia_Retest_ConfigInicial_H1_BUY.cfx` (`22aac16f-…`) | .cfx | 5.318 B | `config.xml` 47.926 B | 2024-11-13 20:57 | `Retest` | **Retester** | `140.2099` |
| 3 | `Ventaja_Build_ConfigInicial_H1_BUY.cfx` (`9b056dd2-…`) | .cfx | 37.078 B | `config.xml` 1.797.825 B | 2024-11-13 20:52 | `Build` | **Builder** | `140.2099` |
| 4 | `Ventaja_Retest_ConfigInicial_H1_BUY.cfx` (`e8a78540-…`) | .cfx | 6.063 B | `config.xml` 55.934 B | 2024-11-13 20:58 | `Retest` | **Retester** | `140.2099` |

Los prefijos hexadecimales (`b00cf192-` etc.) los añadió la subida de archivos; no forman parte del nombre original.

**No hay ningún archivo de Optimizer ni de Cross Check independiente.** El Walk-Forward (WFO/WFM) y el resto de
pruebas existen sólo como *cross checks* dentro de los cuatro archivos. Por tanto no se puede adaptar un "Optimizer"
original; donde el plan de validación lo necesita, se describe cómo configurarlo a mano (docs/04 §A.4).

## b) Formato real y legibilidad

| Comprobación | Resultado |
|---|---|
| Formato | ZIP (PKZIP 2.0, *deflate*) con **una única entrada `config.xml`**. No es XML plano. |
| Integridad ZIP | `unzip -t`: sin errores de CRC en los 4 archivos. Directorio central completo → no truncados. |
| XML | Bien formado en los 4 (parser estricto). Raíz `<Task>`, cierre `</Task>` presente. Sin declaración `<?xml?>`. |
| Codificación | UTF-8. Un único carácter no ASCII: "Formación" en una ruta del archivo 1. |
| Lectura completa | **Sí, los 4 se han leído íntegros** (15.545, 627, 15.643 y 722 nodos respectivamente). |
| Reescritura sin pérdida | Parsear y volver a serializar produce un XML canónicamente idéntico (C14N) en los 4 → los archivos derivados pueden generarse modificando sólo valores. |

## c) Archivos que no se pueden abrir o están incompletos

Ninguno está dañado ni truncado. Pero hay **una dependencia externa que impide reproducir el archivo 1**:

- `Estrategia_Build` usa `<StrategyType type="template" templateFile="C:\Users\<usuario>\Documents\StrategyQuant\00 - Temp\Formación\DOWJONES_H1_BUY\Template\Template_DOW_H1_BUY_1.8.4.sqx">` **(A)**.
  Esa plantilla `.sqx` **no viene dentro del `.cfx`**. Contiene la lógica de entrada (el *breakout* propiamente dicho),
  así que esa parte es **(C) no determinable**. El análisis del archivo 1 continúa, pero la lógica de entrada se marca
  como desconocida y las versiones nuevas no dependen de ella (ver Fase 3).
- El símbolo de datos `GBPJPY_M1_M1_UTCPlus02` (los 4 archivos) **no está definido** en la sección `Resources` de
  ningún archivo: debe existir con ese nombre exacto en tu *Data Manager* o SQX no podrá ejecutar las tareas.

## d) Coherencia con la build 144

| Observación | Tipo | Comentario |
|---|---|---|
| `Task@version="140.2099"` en los 4 archivos | (A) | **Son de la build 140, no de la 144.** La build 144 actual es la 144.2953 (mayo de 2026). |
| ¿Abre la 144 una configuración de la 140? | (B) media | SQX suele importar configuraciones de builds anteriores y completar con valores por defecto lo que falte, pero no está garantizado ni lo he podido comprobar sin SQX. |
| Bloques nuevos de 144 (p. ej. Volume Profile/TPO) | (B) alta | No aparecen en el catálogo de 472 bloques de estos archivos; en la 144 quedarán con su configuración por defecto (probablemente desactivados). |
| Funciones nuevas de 144 (Prop Firm Analysis, filtro de correlación…) | (B) alta | No existen en el XML; se usarán valores por defecto. |
| Métodos de MM distintos entre archivos | (A) | Los Retest incluyen `CryptoSizeByPrice` y los Builder no; `Ventaja_Build` no incluye `SimpleMartingaleMM` y `Estrategia_Build` sí (con un parámetro `Decimals` que los Retest no tienen). |
| Catálogo de objetivos de fitness distinto | (A) | `Ventaja_Retest` tiene 107 objetivos (incluye `VaR` y `CVaR`); `Ventaja_Build` tiene 105. |
| Interpretación de las dos filas anteriores | (B) media | Las plantillas se han ido copiando y editando en distintos momentos/módulos. No impide cargarlas, pero confirma que son configuraciones "heredadas", no generadas de cero. |
| `Estrategia_Retest` tiene `Task@templateFile="…\Ventaja_Retest_ConfigInicial_H1_BUY.cfx"` | (A) | (B) alta: el Retest de estrategia se creó a partir del de ventaja. |
| Dos nodos `<Databanks>` en cada Retest (uno con `retestSelected="true"`) | (A) | (B) media: duplicado escrito por SQX; inofensivo. |

**Nombres de parámetros**: todos los parámetros citados en este análisis existen literalmente en los archivos. Las
versiones nuevas **no introducen ningún nodo ni atributo** que no exista ya en alguno de los cuatro originales (lo
comprueba `tools/validar_cfx.py`).

## Otros hallazgos de la inspección

- Las rutas internas revelan el entorno del autor: dos perfiles de usuario de Windows distintos y una carpeta
  `00 - Temp\Formación\DOWJONES_H1_BUY` → **(B) alta: material de un curso de formación**, diseñado originalmente para el
  **Dow Jones (US30) en H1, sólo compras**. En el repositorio público se han ocultado los nombres de usuario.
- `Resources/Symbols` contiene definiciones de símbolos que **no se usan** en ningún *Setup* (US30 Dukascopy y EURUSD en
  `Estrategia_Build`; GBPUSD y EURUSD en `Ventaja_Build`): restos de configuraciones anteriores.
- Los `.cfx` originales **no se publican** en el repositorio (es público y son material de un tercero). El generador
  los lee de `originales/` (carpeta ignorada por git).

**Inventario entregado. Se continúa con la Fase 1.**
