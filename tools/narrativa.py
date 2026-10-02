"""Texto de las fichas de diseño (Fase 3) que no se deriva automáticamente de los archivos."""

PREGUNTAS = [
    "**Instrumento y bróker reales.** Los originales mezclan una plantilla de US30 (Dow, costes de Darwinex: "
    "swap -7,67/+4,30 con triple swap en viernes, comisión 0,7) con datos de GBPJPY. ¿Sobre qué símbolo(s) "
    "vas a operar y cuáles son su spread típico, comisión por lote y swaps?",
    "**Datos disponibles en SQX.** ¿Desde qué año tienes M1 para cada símbolo? ¿Tienes datos tick con spread "
    "real (necesarios para la precisión 3 de Scalping y Noticias)? ¿El símbolo `*_UTCPlus02` es UTC+2 fijo o "
    "UTC+2/+3 con horario de verano de Nueva York?",
    "**Capital y riesgo.** ¿Capital inicial, riesgo por operación y drawdown máximo tolerable?",
    "**Dirección y plataforma.** ¿Sólo largos (como los originales \"BUY\") o también cortos? ¿Ejecutarás en "
    "MT4, MT5 u otra plataforma?",
    "**Noticias.** ¿Dispones de un calendario económico histórico (CSV) o de MT5 (que tiene calendario nativo)? "
    "¿Aceptas la aproximación por ventana horaria descrita en la Fase 2?",
]

SUPUESTOS = [
    ("S1", "Símbolo", "Se conserva `GBPJPY_M1_M1_UTCPlus02` en los 64 archivos para que carguen en tu instalación "
     "(es el único símbolo presente en los Setup de los 4 originales). Cada ficha indica el instrumento "
     "recomendado; cámbialo en *Data* antes de ejecutar."),
    ("S2", "Costes", "Se conservan los costes del original (spread 2, comisión SizeBased 0,7, swap -7,67/+4,30 "
     "triple viernes) porque no conozco tu bróker; **son incoherentes con GBPJPY** y deben corregirse "
     "(checklist, punto 3). Sólo se cambia el deslizamiento (0 → 0,3-1,5 según estilo)."),
    ("S3", "Datos", "M1 disponible de 2013.09.30 a 2024.07.22 (el rango que usan los originales)."),
    ("S4", "Partición temporal", "Se conserva la partición del autor: construcción hasta 2020.12.31 y OOS final "
     "2021.01.01-2024.07.22 en el Retest (nunca visto por el Builder). Se añade un tramo de validación dentro "
     "del Builder (2019-2020, o 2019.07-2020 en M5/M15)."),
    ("S5", "Horario del servidor", "UTC+2 en invierno / UTC+3 en verano siguiendo el cambio de hora de "
     "EE. UU. (convención \"cierre de Nueva York = 00:00\"). Con ella, 8:30 ET = 15:30 servidor todo el año."),
    ("S6", "Dirección", "Dos kits por estilo: BUY (*Market sides* = long, como los originales) y SELL (*Market sides* = short) con los bloques y niveles espejados. El valor `short` del XML es deducido (sólo hay `long` en los originales): verifica la dirección al importar."),
    ("S7", "Capital y riesgo", "10.000 de capital; riesgo fijo 0,5 % (alta frecuencia) o 1 % por operación; "
     "drawdown máximo tolerable 20 % (25 % en Position/Trend)."),
    ("S8", "Build", "Los archivos son de la build 140.2099. Se asume que la build 144 los importa (SQX suele "
     "mantener compatibilidad hacia atrás), pero **no está verificado**."),
]

# Por qué cada familia NÚCLEO (peso ≥ 2) encaja en el estilo; las de peso 1 son filtros auxiliares que amplían la
# variedad de estrategias sin cambiar la tesis.
CORE_WHY = {
    "Scalping": {
        "rup_canal": "La tesis es la micro-ruptura: define el nivel roto.",
        "rup_bandas": "Ruptura de bandas de volatilidad: variante de la misma tesis.",
        "vol_expansion": "Sin expansión de volatilidad la ruptura no cubre costes.",
        "niv_canal": "Máximos/mínimos recientes: el nivel que se rompe.",
        "niv_horario": "Extremos de la sesión asiática, que la apertura de Londres rompe.",
        "stl_canal": "Orden stop en el extremo de N velas: materializa la ruptura.",
        "stl_vela": "Stop sobre el extremo de la vela previa (micro-ruptura).",
        "stl_horario": "Stop en el extremo de la sesión asiática.",
        "stl_bandas": "Stop en la banda de volatilidad.",
        "stl_rangos": "Margen sobre el nivel para filtrar toques.",
    },
    "DayTrading": {
        "rup_canal": "Ruptura de canal intradía.", "rup_bandas": "Ruptura de bandas.",
        "vol_expansion": "La ruptura necesita expansión.",
        "tiempo_intradia": "Acotan la franja de entrada dentro de la ventana global.",
        "niv_horario": "Rango asiático y aperturas de sesión: los niveles clásicos intradía.",
        "niv_canal": "Extremos recientes.", "niv_diario": "Niveles del día anterior.",
        "stl_horario": "Stop en el extremo del rango asiático: el núcleo del estilo.",
        "stl_diario": "Stop en máximo/mínimo/apertura del día.", "stl_canal": "Stop en extremo de N velas.",
        "stl_vela": "Stop en la vela previa.", "stl_rangos": "Margen sobre el nivel.",
    },
    "Swing": {
        "rup_canal": "Ruptura de consolidaciones de varios días.", "rup_bandas": "Ruptura de bandas.",
        "rup_ichimoku": "Salida de la nube: ruptura de equilibrio de medio plazo.",
        "fuerza": "El swing a favor de un régimen con fuerza tiene más recorrido.",
        "niv_canal": "Máximos de N velas.", "niv_diario": "Niveles diarios.", "niv_semanal": "Niveles semanales.",
        "stl_canal": "Stop sobre el máximo de la consolidación.", "stl_diario": "Stop en niveles diarios.",
        "stl_semanal": "Stop en niveles semanales.", "stl_bandas": "Stop en la banda.",
        "stl_rangos": "Margen proporcional a la volatilidad.",
    },
    "Position": {
        "rup_canal": "Nuevos máximos de 20-250 días (momentum de series temporales).",
        "mom_nivel": "ROC en % y MACD/OSMA frente a cero: escalan a cualquier precio.",
        "tend_medias": "Pendiente de medias largas.", "tend_sistemas": "Sistemas de tendencia lentos.",
        "niv_canal": "Máximos de N días.", "niv_semanal": "Máximos semanales.", "niv_mensual": "Máximos mensuales.",
        "medias": "Medias largas para comparar.", "stl_canal": "Stop sobre máximo de N días.",
        "stl_semanal": "Stop sobre máximo semanal.", "stl_mensual": "Stop sobre máximo mensual.",
    },
    "TrendFollowing": {
        "tend_sistemas": "Núcleo: estimadores independientes de tendencia.",
        "tend_medias": "Pendiente y posición frente a medias.", "fuerza": "Sólo operar tendencias con fuerza.",
        "rup_canal": "Entrada por ruptura de canal (Donchian), la clásica del TF.",
        "rup_ichimoku": "Ruptura de la nube.", "medias": "Medias para comparar.", "sistemas": "SuperTrend/PSAR/Ichimoku.",
        "niv_canal": "Canales.", "stl_canal": "Stop sobre máximo reciente.", "stl_sistemas": "Stop en SuperTrend/PSAR.",
        "stl_rangos": "Margen en ATR.",
    },
    "Range": {
        "rev_bandas": "Núcleo: exceso fuera de banda y reentrada.",
        "sobreventa": "Identificar el exceso que se espera que revierta.",
        "lateral": "Imprescindible: la reversión sólo funciona sin tendencia.",
        "falsa_ruptura": "Recuperación tras perforar el extremo del rango.",
        "bandas": "Bandas que delimitan el rango.", "medias": "Centro del rango (objetivo/regla de salida).",
        "niv_canal": "Extremos del rango.", "osciladores": "Valores de osciladores para comparar.",
        "secuencias": "Agotamiento: N velas seguidas en contra.",
        "stl_bandas": "Orden límite en la banda: se opera el exceso.", "stl_canal": "Límite en el extremo de N velas.",
        "stl_vela": "Límite en el extremo de la vela.", "stl_medias": "Límite en la media.",
        "stl_rangos": "Distancia de la orden límite.",
    },
    "PriceAction": {
        "velas": "Núcleo: patrones de rechazo y absorción.", "falsa_ruptura": "Trampa: perforación y recuperación.",
        "rup_canal": "Ruptura de estructura reciente.", "precio": "OHLC: estructura pura.",
        "heiken": "Heikin-Ashi: estructura suavizada.", "niv_diario": "Contexto: niveles del día.",
        "niv_canal": "Extremos recientes.", "estructura": "Fractales.",
        "comparadores": "Comparaciones de precio.", "secuencias": "Secuencias de velas (máximos crecientes…).",
        "stl_vela": "Stop sobre el extremo de la vela señal: la confirmación clásica.",
        "stl_canal": "Stop en extremo reciente.", "stl_diario": "Stop en nivel diario.",
        "stl_estructura": "Stop en fractal.", "stl_rangos": "Margen en rango de vela/ATR.",
    },
    "NewsProxy": {
        "tiempo_intradia": "Aproximación al calendario: hora (15-16) y día de la semana.",
        "vol_expansion": "La publicación se manifiesta como expansión súbita de rango.",
        "vol_tick": "Pico de actividad en la publicación.", "rup_canal": "Ruptura del rango previo.",
        "rup_bandas": "Ruptura de bandas.", "niv_horario": "Rango 12:00-15:00 → 15:00/15:30 (pre-dato).",
        "niv_canal": "Extremos recientes.", "volat_ind": "ATR/rango verdadero para medir la expansión.",
        "stl_horario": "Stop sobre el rango pre-dato.", "stl_canal": "Stop en extremo reciente.",
        "stl_vela": "Stop en la vela previa.", "stl_rangos": "Margen para evitar el primer pico.",
    },
}

NARR = {
    "Scalping": dict(
        horario="Señales 09:00-18:30 servidor (apertura de Londres + solape con Nueva York); cierre forzado al "
                "final de la ventana (`ExitAtEndOfRange`), a las 21:00 y los viernes a las 20:00. Se evita "
                "23:00-01:30 (rollover, spreads anchos). El rango 'asiático' de los bloques de sesión es "
                "01:00-03:00 → 08:00-10:00.",
        salidas="SL 1-2,5 ATR(14-50) de M5 (≈6-25 pips en EURUSD), PT 1-3 ATR con PT = 80-250 % del SL, "
                "break-even a 0,5-1,5 ATR (50 % de las estrategias), salida temporal 6-36 velas (30 min-3 h) "
                "y regla de salida opcional. Riesgo 0,5 % por operación y máximo 4 operaciones/día (≤2 % de "
                "riesgo diario).",
        sobreajuste=[
            "El ruido de microestructura en M5 es enorme: con miles de estrategias candidatas, algunas "
            "'ganarán' por azar. Mitigación: ≥1.000 operaciones en IS, OOS 2019.07-2020 y holdout 2021-2024.",
            "El Builder usa simulación M1: una orden stop y su SL dentro del mismo minuto son ambiguos. "
            "Mitigación: `AvgBarsInTrade ≥ 3` y Retest con tick real y spread real (precisión 3).",
            "Costes: un spread fijo de backtest infravalora la apertura de Londres. Mitigación: MC de spread "
            "2-4 pips y deslizamiento 0-1 pip; prueba manual con coste ×2.",
            "Ventana horaria y niveles de sesión son parámetros muy ajustables: SPP con 1.500 permutaciones y "
            "exigencia del 80 % de variantes rentables.",
        ],
        validacion=[
            "Ejecuta `Ventaja_Build…Scalping_M5` (salida sólo por tiempo). Si no aparecen entradas con SQN > 2 "
            "y OOS positivo **con costes reales**, detente: no hay ventaja que gestionar.",
            "Pasa las supervivientes por `Ventaja_Retest…Scalping_M5` (tick real, MC de spread y deslizamiento, SPP).",
            "Ejecuta `Estrategia_Build…Scalping_M5` (o, mejor, el flujo plantilla con la entrada ganadora, docs/04 §A.3).",
            "`Estrategia_Retest…Scalping_M5`: el holdout 2021-2024 debe ser positivo y el DD con tick real ≤130 % del original.",
            "Retest manual con spread ×2 y deslizamiento 1 pip: si el beneficio desaparece, la ventaja no es explotable.",
            "Retest en un segundo símbolo de la misma clase (EURUSD ↔ GBPUSD, US500 ↔ NAS100).",
            "Demo 2-3 meses registrando spread y deslizamiento reales y comparándolos con los modelados.",
        ],
        alternativa="Scalping de ticks/segundos (libro de órdenes, latencia) **no es viable en SQX**: el motor "
                    "trabaja con barras (mínimo M1). Esta ficha es la alternativa más cercana (M5). Si no "
                    "tienes datos tick con spread real ni spreads brutos ≤0,3 pips, usa la ficha Day Trading.",
    ),
    "DayTrading": dict(
        horario="Rango asiático: inicio entre 00:00 y 03:00, fin entre 07:00 y 10:00 (horas enteras). Entradas "
                "09:00-19:00 servidor; cierre de todo a las 22:30 (viernes 21:30); máximo 2 operaciones/día.",
        salidas="SL 1-2,5 ATR(14-60) de M15; objetivo opcional 1,5-4 ATR (50 %); trailing 1,5-3 ATR (30 %); "
                "break-even 1-2 ATR (30 %); regla de salida (30 %); cierre de fin de día siempre. Riesgo 0,5 %.",
        sobreajuste=[
            "Las horas del rango (Time From/To) son el parámetro más sobreajustable: se limitan a horas enteras y "
            "se someten a SPP; prueba manual desplazando el rango ±1 h.",
            "El cambio de hora (DST) desplaza 1 h las sesiones varias semanas al año si el servidor no sigue la "
            "convención de Nueva York: verifica la zona horaria del símbolo.",
            "Rupturas falsas en días sin catalizador: `ADXRising`/`ATRRising` como filtros y `StagnationPct` en "
            "la fitness.",
        ],
        validacion=[
            "`Ventaja_Build…DayTrading_M15` → entradas con ventaja (salida 1-6 h + cierre diario).",
            "`Ventaja_Retest…DayTrading_M15` → tick real, MC, SPP, what-if.",
            "`Estrategia_Build…` y `Estrategia_Retest…DayTrading_M15`.",
            "What-if 'ByDays' manual: ningún día de la semana debe concentrar el beneficio.",
            "Retest en GBPUSD/EURJPY (misma mecánica de sesión).",
            "Walk-Forward Matrix en el Optimizer (docs/04 §A.4) con 5-10 ventanas.",
        ],
        alternativa="",
    ),
    "Swing": dict(
        horario="H4 sin filtro horario (en H4 la ventana 01:30-23:30 del original eliminaría la vela de las "
                "00:00). Mantiene posiciones de noche y fin de semana (`RealisticGapsHandling` = true se "
                "conserva para simular gaps).",
        salidas="SL 1,5-3,5 ATR(14-100) de H4; objetivo opcional 2-6 ATR; trailing 2-4 ATR (50 %); break-even "
                "(30 %); salida temporal 6-30 velas = 1-5 días (40 %). Riesgo 1 %; hasta 2 entradas/día.",
        sobreajuste=[
            "≥45 operaciones/año exigidas (≈310 en 7,25 años): muestra suficiente, pero sigue siendo "
            "recomendable Stability en la fitness, OOS 2019-2020, holdout 2021-2024 y validación multi-mercado.",
            "Sensibilidad al punto de inicio: MC con vela de inicio aleatoria.",
            "Swap: el original aplica el swap del Dow; con GBPJPY el carry real cambia el resultado de un swing.",
        ],
        validacion=[
            "`Ventaja_Build…Swing_H4` (salida 1-5 días) → `Ventaja_Retest…Swing_H4`.",
            "`Estrategia_Build…` → `Estrategia_Retest…Swing_H4`.",
            "Retest en 3+ mercados (p. ej. GBPUSD, EURJPY, US30): ≥2 deben ser rentables.",
            "Walk-Forward Matrix (Optimizer) 5-10 ventanas, 20-30 % OOS.",
            "Revisar el resultado año a año: ningún año debe aportar >40 % del beneficio.",
        ],
        alternativa="",
    ),
    "Position": dict(
        horario="D1 sin filtro horario. Las posiciones duran de 1 a 8 semanas; el swap es un componente "
                "importante del resultado.",
        salidas="SL 2,5-5 ATR(20-100) diario obligatorio, **sin objetivo**, trailing 2,5-5 ATR (70 %), salida "
                "temporal 10-40 días (30 %) y salida por regla (50 %). Riesgo 1 %.",
        sobreajuste=[
            "Límite físico: con una sola posición abierta y duraciones de semanas, un mercado no da más de "
            "~20-25 operaciones/año. Se exige ese máximo razonable (≥150 en 7,25 años); 300 en 7 años sólo es "
            "posible acortando la duración (eso ya es Swing/Trend) o construyendo sobre varios mercados. "
            "Máximo 2 condiciones de entrada.",
            "Dependencia de 2-3 tendencias grandes: what-if sin las 2 mejores operaciones.",
            "Sin OOS en el Builder (no hay muestra suficiente): toda la validación recae en el Retest y en "
            "otros mercados.",
        ],
        validacion=[
            "**Requisito previo**: ampliar datos (Dukascopy ofrece M1 desde 2003 en mayores e índices) y repetir "
            "la construcción con ≥15 años.",
            "`Ventaja_Build…Position_D1` (salida 1-6 meses) → `Ventaja_Retest…`.",
            "`Estrategia_Build…` → `Estrategia_Retest…Position_D1`.",
            "Retest obligatorio en 5+ mercados con los mismos parámetros (el momentum es un fenómeno de cartera).",
            "SPP ±30 % y MC con vela de inicio aleatoria.",
            "Operar en demo/real con tamaño mínimo al menos 6-12 meses antes de escalar.",
        ],
        alternativa="",
    ),
    "TrendFollowing": dict(
        horario="H1 con la ventana original 01:30-23:30 (evita el rollover); mantiene posiciones de 1 a 5 días.",
        salidas="SL 2-4 ATR(14-100) de H1; **trailing 2,5-5 ATR como salida principal (80 %)**; objetivo raro y "
                "lejano (4-10 ATR, 30 %); salida por regla (50 %). Acierto esperado 30-40 %. Riesgo 1 %.",
        sobreajuste=[
            "Pocas operaciones ganadoras explican todo el beneficio: what-if sin las 2 mejores y 2 peores.",
            "Rachas planas largas: `StagnationPct` en la fitness.",
            "En un solo símbolo el resultado depende de pocas tendencias: validar en cesta.",
        ],
        validacion=[
            "`Ventaja_Build…TrendFollowing_H1` (salida 12 h-3 días) → `Ventaja_Retest…`.",
            "`Estrategia_Build…` → `Estrategia_Retest…TrendFollowing_H1`.",
            "Retest en 5+ mercados no correlacionados.",
            "Walk-Forward Matrix y comprobación de rachas perdedoras máximas frente a tu tolerancia.",
        ],
        alternativa="",
    ),
    "Range": dict(
        horario="Entradas 01:30-09:30 servidor (sesión asiática, menor deriva direccional en FX). Fuera de esa "
                "franja no se abren operaciones nuevas.",
        salidas="SL 1,5-3 ATR(14-60) obligatorio; objetivo 0,8-2 ATR obligatorio con PT = 40-120 % del SL; "
                "salida temporal 5-30 h (50 %) y salida por regla (50 %); sin trailing. Acierto ≥55 %. "
                "Riesgo 0,75 %; máximo 2 entradas/día.",
        sobreajuste=[
            "Cola izquierda: cuando el rango se rompe, una pérdida borra muchas ganancias. SL obligatorio y "
            "what-if excluyendo el 5 % de extremos.",
            "Cambio de régimen (un par lateral durante años puede entrar en tendencia): análisis año a año.",
            "Umbrales de osciladores y de ADX/KER: rangos acotados + SPP.",
        ],
        validacion=[
            "`Ventaja_Build…Range_H1` (salida 3-24 h) → `Ventaja_Retest…`.",
            "`Estrategia_Build…` → `Estrategia_Retest…Range_H1`.",
            "Cambiar el símbolo a un par de rango (EURCHF, EURGBP, AUDNZD) y repetir: GBPJPY es mal candidato.",
            "Revisar periodos de ruptura de régimen conocidos (p. ej. enero 2015 en EURCHF).",
        ],
        alternativa="",
    ),
    "PriceAction": dict(
        horario="Entradas 01:30-23:30 servidor (la ventana del original: evita el rollover). El rango "
                "'asiático' de los bloques de sesión es 01:00-03:00 → 08:00-10:00.",
        salidas="SL 1-2,5 ATR(14-50); objetivo 1,5-4 ATR con PT = 150-300 % del SL; break-even 1-2 ATR (50 %); "
                "salida temporal 5-30 h (30 %); regla (30 %). Riesgo 1 %; 2 entradas/día.",
        sobreajuste=[
            "Los patrones de vela tienen ventaja aislada pequeña y hay muchísimas combinaciones (desplazamiento "
            "1-3): riesgo alto de minería de datos.",
            "Los patrones dependen del OHLC exacto del bróker: el MC de OHLC (±10 % ATR) es aquí especialmente "
            "relevante.",
            "Se excluyen los patrones bajistas que el original permitía como entrada larga.",
        ],
        validacion=[
            "`Ventaja_Build…PriceAction_H1` (salida 3-24 h) → `Ventaja_Retest…`.",
            "`Estrategia_Build…` → `Estrategia_Retest…PriceAction_H1`.",
            "Retest con datos de otro proveedor/bróker (el OHLC cambia ligeramente).",
            "Retest en otros mercados.",
        ],
        alternativa="",
    ),
    "NewsProxy": dict(
        horario="Rango pre-dato 12:00-15:00 → 15:00/15:30; señales 15:00-17:00 servidor (8:00-10:00 ET con la "
                "convención S5); `BarHourIs` 15-16; cierre 22:00 (viernes 21:00); una operación/día.",
        salidas="SL 1-2 ATR(10-40) de M15; objetivo opcional 1,5-4 ATR; break-even 0,5-1,5 ATR (50 %); salida "
                "temporal 2-16 velas = 30 min-4 h (70 %). Riesgo 0,5 %.",
        sobreajuste=[
            "La estrategia opera la ventana TODOS los días: el resultado mezcla días con dato y sin dato.",
            "Las horas de publicación cambian con el DST de EE. UU. frente al de la UE (marzo/noviembre).",
            "El spread y el deslizamiento de una publicación real no están en datos M1: MC de spread hasta "
            "8 pips y deslizamiento hasta 3 pips + precisión 3.",
        ],
        validacion=[
            "`Ventaja_Build…NewsProxy_M15` → `Ventaja_Retest…`.",
            "`Estrategia_Build…` → `Estrategia_Retest…NewsProxy_M15`.",
            "**Validación clave fuera de SQX**: exporta las operaciones (CSV) y crúzalas con un calendario "
            "histórico; compara el resultado en días con dato de alto impacto frente a días sin dato. Si no hay "
            "diferencia, la estrategia no es de noticias: es una ruptura horaria.",
            "Demo durante varias publicaciones (NFP, IPC) midiendo el deslizamiento real.",
        ],
        alternativa="News trading real **no es viable de forma nativa** en SQX (sin calendario económico). Esta "
                    "ficha es una aproximación horaria. Alternativas: (a) indicador personalizado en Java que lea "
                    "un CSV de eventos (requiere programación y reimplementarlo en la plataforma; MT5 tiene "
                    "calendario nativo en MQL5); (b) usar las noticias sólo como filtro de 'no operar' en el EA.",
    ),
}
