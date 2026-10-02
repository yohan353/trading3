"""Genera docs/04_Fase4_Guia_Manual_y_Checklist.md.

Las tablas de valores por estilo se leen de los .cfx de configs/, de modo que la guía manual y los archivos
contienen exactamente los mismos valores.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sqx_cfx import load_cfx  # noqa: E402
from estilos import STYLES  # noqa: E402
from generar_cfx import ORIGINALS, cfx_name  # noqa: E402
import generar_fichas as F  # noqa: E402

BASE = Path(__file__).resolve().parent.parent


def o(r, key):
    return F.opt(r, key)


def opt_time(key):
    return lambda r: F.hhmm(o(r, key))


BUILD_FIELDS = [
    # (pestaña, campo UI aproximado, nodo XML, extractor)
    ("What to build", "Strategy type", "WhatToBuild/StrategyType@type", F.mode),
    ("What to build", "Trading direction", "WhatToBuild/MarketSides@type",
     lambda r: r.find("Settings/WhatToBuild/MarketSides").get("type")),
    ("What to build", "Entry conditions min–max", "RulesComplexity/Chart@min/maxConditions",
     lambda r: F.chart(r, "minConditions", "maxConditions")),
    ("What to build", "Exit conditions min–max", "Chart@min/maxExitConditions",
     lambda r: F.chart(r, "minExitConditions", "maxExitConditions")),
    ("What to build", "Exit types min–max", "Chart@min/maxExitTypes", lambda r: F.chart(r, "minExitTypes", "maxExitTypes")),
    ("What to build", "Indicator period min–max", "Chart@min/maxPeriod", lambda r: F.chart(r, "minPeriod", "maxPeriod")),
    ("What to build", "Shift min–max", "Chart@min/maxShift", lambda r: F.chart(r, "minShift", "maxShift")),
    ("What to build", "Stop Loss", "SLPTOptions/SL*", lambda r: F.slpt(r, "SL")),
    ("What to build", "Profit Target / Risk-Reward", "SLPTOptions/PT*, LimitSLPTRRR*", lambda r: F.slpt(r, "PT")),
    ("Genetic options", "Población / islas / generaciones / cruce / mutación / migración / estancamiento",
     "BuildMode/*", F.gen),
    ("Genetic options", "Initial population filters", "BuildMode/Conditions", F.init),
    ("Data", "Symbol", "Setup/Chart@symbol", lambda r: r.find("Settings/Data/Setups/Setup/Chart").get("symbol")),
    ("Data", "Timeframe", "Setup/Chart@timeframe", F.tf),
    ("Data", "Date from – to", "Setup@dateFrom/dateTo", F.dates),
    ("Data", "Out of sample", "OutOfSample/Range", F.oos),
    ("Data", "Precision", "Setup@testPrecision", lambda r: r.find("Settings/Data/Setups/Setup").get("testPrecision")),
    ("Data", "Spread / Slippage", "Chart@spread, Setup@slippage",
     lambda r: f"{r.find('Settings/Data/Setups/Setup/Chart').get('spread')} / {F.slip(r)}"),
    ("Trading options", "Limit signals to time range", "LimitTimeRange, SignalTimeRangeFrom/To, ExitAtEndOfRange", F.window),
    ("Trading options", "Exit at end of day / on Friday", "ExitAtEndOfDay/EODExitTime, ExitOnFriday/FridayExitTime", F.eod),
    ("Trading options", "Max trades per day", "MaxTradesPerDay", F.maxtr),
    ("Trading options", "Max distance from market", "MaxDistanceFromMarket/MaxDistancePct", F.maxdist),
    ("Trading options", "Reserved bars", "ReservedBars", lambda r: o(r, "ReservedBars")),
    ("Building blocks", "Order types", "Blocks/OrderTypes", F.orders),
    ("Building blocks", "Stop loss / Profit target", "ExitTypes StopLoss/ProfitTarget",
     lambda r: f"SL {F.exit_t(r, 'StopLoss.StopLoss')}; PT {F.exit_t(r, 'ProfitTarget.ProfitTarget')}"),
    ("Building blocks", "Trailing stop", "ExitTypes TrailingStop", lambda r: F.exit_t(r, "TrailingStop.TrailingStop")),
    ("Building blocks", "Move SL to BE", "ExitTypes MoveSL2BE", lambda r: F.exit_t(r, "MoveSL2BE.MoveSL2BE")),
    ("Building blocks", "Exit after bars", "ExitTypes ExitAfterBars", lambda r: F.exit_t(r, "ExitAfterBars.ExitAfterBars")),
    ("Building blocks", "Exit rule", "ExitTypes _ExitRule_", lambda r: F.exit_t(r, "_ExitRule_")),
    ("Building blocks", "Bloques activos (lista: docs/03 §3)", "BuildingBlocks", F.blocks),
    ("Money management", "Método", "MoneyManagement/Method", F.mm),
    ("Ranking", "Fitness", "FitnessCriteria/Ranking", F.fit),
    ("Ranking", "Filtering conditions", "Rankings/Conditions", F.filt),
]

RETEST_FIELDS = [
    ("Data", "Timeframe", "Setup/Chart@timeframe", F.tf),
    ("Data", "Date from – to / OOS", "Setup, OutOfSample", lambda r: f"{F.dates(r)}; OOS {F.oos(r)}"),
    ("Data", "Slippage", "Setup@slippage", F.slip),
    ("Trading options", "Ventana / cierres / máx. ops", "BuildTradingOptions",
     lambda r: f"{F.window(r)}; {F.eod(r)}; máx. {F.maxtr(r)}"),
    ("Money management", "Método", "MoneyManagement", F.mm),
    ("Ranking", "Fitness", "FitnessCriteria", F.fit),
    ("Ranking", "Filtering conditions", "Rankings/Conditions", F.filt),
    ("Cross checks", "Retest with higher precision", "RetestWithHigherPrecision", F.hp),
    ("Cross checks", "Monte Carlo retest", "MonteCarloRetest", F.mc),
    ("Cross checks", "Monte Carlo trades manipulation", "MonteCarloManipulation", F.mcm),
    ("Cross checks", "Optimization profile / SPP", "OptProfileSysParamPermutation", F.spp),
    ("Cross checks", "What if", "WhatIf", F.whatif),
]


def esc(s):
    return str(s).replace("|", "\\|")


def field_table(fields, kind):
    roots = {st["name"]: load_cfx(BASE / "configs" / st["name"] / f"{cfx_name(ORIGINALS[kind], st, 'BUY')}.cfx")
             for st in STYLES}
    L = ["| Pestaña › campo | Nodo XML | " + " | ".join(st["name"] for st in STYLES) + " |",
         "|---|---|" + "---|" * len(STYLES)]
    for tab, label, node, fn in fields:
        vals = [esc(fn(roots[st["name"]])) for st in STYLES]
        L.append(f"| **{tab}** › {label} | `{node}` | " + " | ".join(vals) + " |")
    return L


def main():
    L = ["# Fase 4 — Entregables D y E: archivos, guía de aplicación manual y lista de verificación", "",
         "## D) Qué se entrega", "",
         "> **Opción entregada: la GUÍA PASO A PASO de esta página es el entregable principal.** No puedo garantizar que",
         "> los `.cfx` abran sin errores en SQX **build 144**: los originales son de la build 140.2099 y no he podido",
         "> ejecutar SQX. Como apoyo se entregan además 64 archivos `.cfx` **experimentales, NO validados en SQX**,",
         "> generados modificando sólo valores de los originales (sin nodos ni atributos nuevos) y verificados",
         "> estáticamente (`docs/validacion/informe_validacion.md`). Si un archivo no carga o SQX avisa de algo,",
         "> aplica los valores a mano con las tablas de abajo, que contienen exactamente lo mismo que los archivos.", "",
         "Archivos: `configs/<Estilo>/<NombreOriginal>__<Estilo>_<TF>_<BUY|SELL>.cfx` (4 por estilo y dirección × 8 "
         "estilos × 2 direcciones = 64). Detalle de cada valor cambiado y su justificación: `docs/cambios/`.", "",
         "## A.1 Cargar un `.cfx` (vía rápida, experimental)", "",
         "1. Haz una copia de seguridad de tu proyecto y trabaja en un proyecto personalizado nuevo (p. ej. `Kit_<Estilo>`).",
         "2. Crea una tarea **Build** (para `*_Build_*`) o **Retest** (para `*_Retest_*`).",
         "3. En la tarea, usa la opción de **cargar configuración** (*Load settings/config*, icono de carpeta en la barra de "
         "ajustes; el nombre exacto puede variar en la build 144) y elige el `.cfx`.",
         "4. Si SQX muestra un aviso de versión o de símbolo no encontrado, **no lo ignores**: revisa la lista de "
         "verificación (E) y, si algo no cuadra, aplica los valores a mano (A.2).",
         "5. Recorre todas las pestañas comparando con las tablas de A.2 antes de pulsar *Start*.", "",
         "## A.2 Aplicación manual paso a paso", "",
         "Procedimiento (para cada estilo):", "",
         "1. Carga el **original** correspondiente (p. ej. `Ventaja_Build_ConfigInicial_H1_BUY.cfx`) en una tarea nueva.",
         "2. Recorre las pestañas en este orden: **What to build → Genetic options → Data → Trading options → Building "
         "blocks → Money management → Ranking → Cross checks**, fijando los valores de la columna de tu estilo.",
         "3. En **Building blocks**: desactiva todo (botón de deseleccionar categoría) y activa sólo los bloques de la "
         "tabla §3 de la ficha del estilo (docs/03), con sus pesos y rangos específicos. Haz lo mismo con *Order types* y "
         "*Exit types*.",
         "4. Guarda la configuración con el nombre `<Original>__<Estilo>_<TF>.cfx`.",
         "5. Repite para los otros 3 archivos del kit y verifica con la lista E.", "",
         "Los nombres de campo de la interfaz son aproximados (pueden variar entre builds); la columna *Nodo XML* da el "
         "nombre exacto del parámetro en el archivo.", "",
         "Las tablas muestran el kit **BUY**. El kit **SELL** es idéntico salvo dos cosas: (1) *What to build › Trading "
         "direction* = **Short only** (`MarketSides@type=\"short\"`); (2) en *Building blocks* se activa el bloque "
         "espejo de cada bloque direccional con su peso, y los niveles de osciladores se espejan (RSI/estocástico "
         "100−L, WPR −100−L, CCI y ROC −L, Laguerre/DeMarker 1−L). La lista exacta está en la columna *Espejo SELL* "
         "de cada ficha (docs/03 §3).", "",
         "### A.2.1 `Estrategia_Build` (estrategia completa)", ""]
    L += field_table(BUILD_FIELDS, "EB")
    L += ["", "### A.2.2 `Ventaja_Build` (test de ventaja de la entrada)", ""]
    L += field_table(BUILD_FIELDS, "VB")
    L += ["", "### A.2.3 `Estrategia_Retest`", ""]
    L += field_table(RETEST_FIELDS, "ER")
    L += ["", "### A.2.4 `Ventaja_Retest`", ""]
    L += field_table(RETEST_FIELDS, "VR")
    L += ["", "Valores que **no cambian** respecto al original en ningún estilo: símbolo, spread 2, comisión 0,7, swap "
          "(ver checklist punto 3), `testPrecision=1`, `MarketSides=long`, capital 10.000, `MaxStrategies=1000`, "
          "`DismissTooSimilarStrategies`, `AutomaticDismissal`, `ATMs` desactivado, cross checks desactivados en los "
          "Builders, `evaluateAll=false` y `DeleteFailedStrategies=false` en los Retest.", "",
          "## A.3 Volver al flujo con plantilla (fiel al original)", "",
          "El original construía la estrategia completa sobre una plantilla con la entrada fija. Para reproducirlo con "
          "cualquier estilo:", "",
          "1. Ejecuta `Ventaja_Build…<Estilo>` y `Ventaja_Retest…<Estilo>`; elige 1-3 entradas que pasen todos los cross "
          "checks y tengan OOS 2021-2024 positivo.",
          "2. Abre la estrategia en **AlgoWizard**, activa el modo plantilla y deja la entrada **fija** (condiciones y tipo "
          "de orden). Sustituye las salidas por los huecos aleatorios de salida que quieras que explore el Builder.",
          "3. Guarda como `Template_<Estilo>_<TF>_BUY.sqx`.",
          "4. En `Estrategia_Build…<Estilo>`: *What to build* → *Strategy from template* → elige la plantilla; pon "
          "*Entry conditions* 0–0 (como el original).",
          "5. Mantén el resto de la configuración del estilo (SL/PT, salidas, filtros, motor).", "",
          "## A.4 Walk-Forward Matrix en el Optimizer (no incluido en los originales)", "",
          "Recomendado para Day Trading, Swing, Trend Following y Range (no para Position: pocas operaciones por ventana).", "",
          "1. Crea una tarea **Optimizer** sobre las estrategias que superen `Estrategia_Retest`.",
          "2. Parámetros a optimizar: periodos de indicadores y parámetros de salida (los mismos que el SPP), ±20-30 %, "
          "5-10 pasos.",
          "3. Matriz: ejecuciones 5-15 y OOS 10-30 %; mismo símbolo, timeframe, costes y opciones de trading que el kit.",
          "4. Aceptación sugerida (la misma lógica que el WFM inactivo de los originales): ≥ 70 % de ejecuciones "
          "rentables, ninguna ejecución con > 50 % del beneficio total, DD por ejecución ≤ 25 %, y una zona de la "
          "matriz (no una celda aislada) que pase.", "",
          "## A.5 Si el Builder no genera ninguna estrategia", "",
          "Revisión 3 de los archivos: la causa principal era la **población inicial**. Las versiones anteriores pedían "
          "160-200 estrategias aleatorias que cumpliesen Ret/DD, % de acierto y 200-870 operaciones antes de empezar a "
          "evolucionar; SQX no guarda nada hasta completarla, así que podía pasar horas o días sin mostrar ninguna. "
          "Ahora la población inicial sólo exige un mínimo de operaciones, la calibración de indicadores está activa y "
          "se han quitado los filtros de calendario muy restrictivos. Si aun así no aparece nada:", "",
          "1. **Mira en qué fase está.** Si el progreso indica *initial population* / población inicial durante mucho "
          "tiempo, el filtro de *Genetic options › Initial population* sigue siendo demasiado estricto: déjalo sólo con "
          "nº de operaciones (o desactívalo).",
          "2. **Mira las estadísticas de rechazo** (generadas / aceptadas / rechazadas y motivo). Si casi todo se "
          "rechaza por *NumberOfTrades*, baja la densidad del estilo; si es por *Ret/DD* o *PF*, los costes del símbolo "
          "probablemente se comen la ventaja (típico de Scalping y NewsProxy con GBPJPY).",
          "3. **Calibra a mano**: *Building blocks › Calibrate* con el símbolo y timeframe ya puestos en *Data*. Comprueba "
          "que `ATR` ya no tiene rango −5000…5000.",
          "4. **Prueba de humo**: pon *Generation type* = generación aleatoria y quita temporalmente los filtros del "
          "*Ranking* salvo `NumberOfTrades`. Si en 10-15 minutos tampoco salen estrategias, el problema es de datos o de "
          "importación (símbolo, fechas, timeframe, dirección), no de los filtros.",
          "5. **Control con el original**: ejecuta el `Ventaja_Build_ConfigInicial_H1_BUY.cfx` original. Si tampoco "
          "genera nada, el problema está en los datos (`GBPJPY_M1_M1_UTCPlus02`, rango 2013-2020) y no en los archivos nuevos.",
          "6. **Empieza por un estilo de barras largas** (Swing H4, Trend H1, Range H1): Scalping y NewsProxy sobre "
          "GBPJPY con 2 pips de spread + deslizamiento casi nunca encuentran estrategias rentables (ver Fase 2).", "",
          "## E) Lista de verificación al importar", "",
          "### E.1 Para los 64 archivos", "",
          "1. **Versión:** SQX puede avisar de que el archivo es de la build 140.2099. Anota cualquier aviso; si dice que "
          "ignora o reinicia secciones, aplica esas secciones a mano (A.2).",
          "2. **Símbolo:** `Data` → el símbolo `GBPJPY_M1_M1_UTCPlus02` debe existir en tu *Data Manager*. Si usas otro "
          "instrumento (recomendado en Scalping, Range, Noticias), cámbialo aquí **y en los 4 archivos del kit**.",
          "3. **Costes:** spread, comisión (unidad y por lado/ida-vuelta) y swaps **de tu bróker**. Los heredados (swap "
          "-7,67/+4,30, triple **viernes**, comisión 0,7) son del US30 en Darwinex; para FX el triple swap es el "
          "**miércoles**.",
          "4. **Horario del servidor:** confirma si los datos son UTC+2 fijo o UTC+2/+3 con DST de Nueva York. Si no "
          "coincide con el supuesto S5, desplaza todas las horas (ventana de señales, cierres, rangos horarios de "
          "`HighestInRange`/`Session*`, `BarHour*`).",
          "5. **Fechas:** el rango del *Setup* debe estar dentro de tus datos; el OOS del Builder dentro del periodo de "
          "construcción; el OOS del Retest (2021.01.01-2024.07.22) **nunca** dentro del periodo de construcción.",
          "6. **Opciones de trading idénticas** entre el Builder y el Retest del mismo kit (ventana, cierres, máx. "
          "operaciones/día, distancia máxima).",
          "7. **Timeframe idéntico** en los 4 archivos del kit y en los *Setup* de *RetestOnAdditionalMarkets*.",
          "8. **Money management:** `FixedAmount` en `Estrategia_*` (riesgo en dinero coherente con tu capital) y "
          "`FixedSize 1` en `Ventaja_*`.",
          "9. **Fitness ponderada:** en *Ranking* deben aparecer exactamente los objetivos y pesos de la ficha (docs/03 §6).",
          "10. **Filtros:** revisa que las condiciones IS/OOS/Full aparecen con la muestra correcta (IS, OOS, *Full*).",
          "11. **Bases de datos:** Builder → salida `Results`; Retest → entrada y salida `Results`. Si encadenas Builder y "
          "Retest en un proyecto, apunta la entrada del Retest al banco de resultados del Builder.",
          "12. **Población inicial y calibración** (*Genetic options* y *Building blocks*): el filtro de población "
          "inicial debe tener sólo `NumberOfTrades`; la calibración antes de empezar debe estar activa.",
          "13. **No mezclar direcciones:** retestea las estrategias BUY con los Retest `_BUY` y las SELL con los `_SELL` "
          "(o en bancos de datos separados).", "",
          "### E.1b Sólo kits SELL", "",
          "- *What to build › Trading direction* debe mostrar **Short only**. `short` es el valor deducido del XML (los "
          "originales sólo traen `long`): si SQX lo ignora y muestra *Long only*, cámbialo a mano.",
          "- En *Building blocks* deben estar activos los bloques bajistas (p. ej. `BarOpensBelowLowestAfterOpenAbove`, "
          "`BearishEngulfing`, `RSICrossDown`) y desactivados sus equivalentes alcistas; los niveles stop de mayor peso "
          "son los mínimos (`Lowest`, `Low`, `LowestInRange`, `SessionLow`…).",
          "- **Swap corto**: el heredado (+4,30 triple viernes) es del US30; pon el swap corto real de tu bróker.",
          "- Un kit SELL sobre un activo con deriva alcista de largo plazo (índices) encontrará menos estrategias: es "
          "esperable, no un fallo de configuración.", "",
          "### E.2 Builders", "",
          "14. *What to build*: `Simple strategy` (o plantilla, si sigues A.3), dirección del kit, rangos de complejidad de "
          "la tabla A.2.",
          "15. *Building blocks*: nº de bloques activos = el de la tabla A.2 (p. ej. Scalping 93/48/40). Si la build 144 "
          "añade bloques nuevos, deben quedar **desactivados**.",
          "16. *Order types* y *Exit types*: sólo los de la tabla; en `Ventaja_*`, **únicamente** *Exit after bars*.",
          "17. Prueba corta: lanza el Builder 10-15 minutos y comprueba que se generan estrategias con el nº de operaciones "
          "esperado y que los rechazos no se deben a un filtro mal puesto (p. ej. todas descartadas por `NumberOfTrades`). "
          "Si casi todo se descarta por número de operaciones, baja la densidad del estilo en `tools/estilos.py` en vez "
          "de quitar el filtro.",
          "18. Abre 2-3 estrategias generadas y verifica a ojo que su lógica corresponde al estilo (p. ej. órdenes stop en "
          "el máximo del rango asiático en Day Trading BUY / en el mínimo en SELL, órdenes límite en Range).", "",
          "### E.3 Retesters", "",
          "19. **Datos tick:** *Retest with higher precision* usa precisión 2 (tick real + spread personalizado) o 3 "
          "(tick real + spread real, en Scalping y Noticias). Sin datos tick ese cross check fallará o no se ejecutará.",
          "20. Monte Carlo: nº de simulaciones, métodos (OHLC, spread, deslizamiento, vela de inicio) y condiciones al 95 %.",
          "21. Monte Carlo de manipulación: la condición de beneficio debe compararse contra el resultado **principal** "
          "(no contra otro Monte Carlo).",
          "22. SPP: nº de tests y % de rentables de la tabla; empieza con pocas estrategias (el coste es alto).",
          "23. *Retest on additional markets* sigue **desactivado**: configúralo con 1-3 símbolos reales relacionados si "
          "vas a usarlo (el original repetía GBPJPY).", "",
          "### E.4 Comprobaciones específicas por estilo", "",
          "| Estilo | Comprobar |", "|---|---|",
          "| Scalping | Instrumento de spread bruto bajo; datos tick con spread real; coste total < 15 % del ATR(M5); cierre al final de la ventana activo. |",
          "| Day Trading | Rango asiático en horas del servidor correctas; cierre diario 22:30 y viernes 21:30; órdenes stop activas. |",
          "| Swing | Swap real del instrumento (se mantienen noches y fines de semana); `RealisticGapsHandling=true`. |",
          "| Position | Mínimo 150 operaciones en 7,25 años (límite físico de un solo mercado con duraciones de semanas); ampliar datos a ≥15 años; sin filtro horario; retest multi-mercado. |",
          "| Trend Following | H1 (no H4); trailing activo con prob. 80 %; acierto mínimo 30 % (no 40 %); what-if de 2 mejores/peores. |",
          "| Range | Símbolo de rango (no GBPJPY); órdenes límite; PT obligatorio 40-120 % del SL; ventana 01:30-09:30. |",
          "| Price Action | Sólo patrones alcistas; desplazamiento 1-3; MC de OHLC activo. |",
          "| Noticias (proxy) | Ventana 15:00-17:00 = 8:00-10:00 ET con tu servidor; spread MC hasta 8 pips; precisión 3; cruzar después las operaciones con un calendario real. |", ""]
    out = BASE / "docs" / "04_Fase4_Guia_Manual_y_Checklist.md"
    out.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"OK {out.relative_to(BASE)} ({len(L)} líneas)")


if __name__ == "__main__":
    main()
