"""Especificación de los 8 estilos objetivo (versión BUY; la SELL se deriva por espejo en familias.py).

Cada valor que se escribe en un .cfx sale de aquí y lleva su justificación. Las claves de bloques son las del
catálogo del propio archivo original (build 140.2099); validar_cfx.py comprueba que existen. Los horarios están en
hora del servidor de los datos (símbolo *_UTCPlus02).

Supuestos globales (ver docs/03, sección "Supuestos"):
* Símbolo: se conserva GBPJPY_M1_M1_UTCPlus02 (el que usan los 4 originales) para que los archivos carguen.
* Datos M1 disponibles de 2013.09.30 a 2024.07.22 (rango que usan los originales).
* Kits BUY (Market sides = long) y SELL (Market sides = short) con bloques espejados.
* Capital 10.000 y tolerancia de drawdown máxima del 20 % (25 % Position/Trend).

Revisión 2: paletas de bloques amplias (núcleo con peso alto + filtros a peso 1) y número mínimo de operaciones
calculado como densidad (operaciones/año) × años de cada tramo, con un mínimo equivalente al original (≈41/año).
"""

from sqx_cfx import SECONDS  # "09:30" -> segundos desde medianoche (formato de los Param de hora)
from familias import (P_FUERZA, P_LATERAL, P_MOMENTUM, P_SOBREVENTA, P_SUPERTREND, roc_params, ventana)

COMMON_WHY = {
    "simple": "El original dependía de una plantilla .sqx externa (Template_DOW_H1_BUY_1.8.4.sqx) que no viene "
              "en el .cfx; en modo 'simple' el archivo funciona por sí solo y la selección de bloques del "
              "estilo pasa a determinar la entrada. Para volver al flujo plantilla, ver docs/04 §A.3.",
}

# Rangos de fechas -------------------------------------------------------------------------
DATA_FULL = ("2013.09.30", "2024.07.22")          # rango de datos que usan los originales
HOLDOUT = ("2021.01.01", "2024.07.22")            # OOS final del Retest original (se conserva)
BUILD_STD = ("2013.09.30", "2020.12.31")          # periodo del Builder original
VALID_STD = ("2019.01.01", "2020.12.31")          # tramo de validación dentro del Builder
BUILD_FAST = ("2016.01.04", "2020.12.31")         # M5/M15: periodo más corto por coste de cómputo
VALID_FAST = ("2019.07.01", "2020.12.31")

L = "Stop/Limit Price Levels."
ASIA_RANGO = ((0, 300, 100), (700, 1000, 100))    # HighestInRange: desde 00-03 h hasta 07-10 h (horas enteras)
ASIA_SESION = ((1, 3, 1), (8, 10, 1))
PRE_US_RANGO = ((1200, 1500, 100), (1500, 1530, 30))
PRE_US_SESION = ((12, 14, 1), (15, 15, 1))


def P(*dicts):
    out = {}
    for d in dicts:
        out.update(d)
    return out


def S(name, title, tf, **kw):
    kw.update(name=name, title=title, tf=tf)
    return kw


STYLES = [
    # =====================================================================================
    S("Scalping", "Scalping (micro-ruptura en sesión líquida)", "M5",
      tesis="En las aperturas de Londres y el solape Londres-Nueva York entra liquidez direccional; tras "
            "una micro-consolidación, la ruptura de su extremo tiende a continuar unas pocas velas. La "
            "ventaja es pequeña y sólo existe si el coste total (spread+comisión+deslizamiento) es una "
            "fracción pequeña del ATR de M5.",
      instrumento="EURUSD o índice US500/NAS100 con spread bruto ≤0,3 pips/0,5 pts + comisión. GBPJPY con "
                  "2 pips de spread NO es apto (coste ≈30 % del ATR de M5).",
      build_dates=BUILD_FAST, valid=VALID_FAST, slippage="0.5",
      slippage_why="El original usa 0; en M5 un deslizamiento de 0,5 pips por orden stop/mercado es "
                   "conservador-realista y cambia el signo de muchas estrategias.",
      density=300,
      options={
          "LimitTimeRange": ("true", "Sólo sesión líquida."),
          "SignalTimeRangeFrom": (SECONDS("09:00"), "09:00 servidor ≈ apertura de Londres (UTC+2)."),
          "SignalTimeRangeTo": (SECONDS("18:30"), "18:30 servidor ≈ final del solape Londres-NY."),
          "ExitAtEndOfRange": ("true", "Un scalper no arrastra posiciones fuera de su ventana."),
          "ExitAtEndOfDay": ("true", "Red de seguridad: nada abierto al cierre del día."),
          "EODExitTime": (SECONDS("21:00"), "Antes del rollover (spreads anchos)."),
          "ExitOnFriday": ("true", "Sin riesgo de gap de fin de semana."),
          "FridayExitTime": (SECONDS("20:00"), "Viernes tarde: liquidez decreciente."),
          "MaxTradesPerDay": ("6", "Permite varias operaciones/día sin sobre-operar en días de ruido."),
          "MaxDistanceFromMarket": ("true", "Evita órdenes stop lejos del precio."),
          "MaxDistancePct": ("0.3", "0,3 % ≈ 45 pips en GBPJPY; tope razonable para M5."),
          "ReservedBars": ("120", "≥ periodo máximo (100) para que los indicadores estén calculados."),
      },
      complexity=dict(entry=(1, 3), exit_cond=(1, 2), exit_types=(2, 4), period=(5, 100), shift=(1, 1)),
      complexity_why="Periodos 5-100 velas de M5 (25 min a 8 h): horizonte de micro-estructura; ≥100 no "
                     "aporta nada a un scalper y sobreajusta.",
      blocks=dict(
          signals=[("rup_canal", 10), ("rup_bandas", 4), ("vol_expansion", 2), ("vol_tick", 1), ("mom_direccion", 1),
                   ("mom_nivel", 1), ("tend_medias", 1), ("fuerza", 1), ("tiempo_intradia", 1)],
          indicators=[("niv_canal", 3), ("niv_horario", 2), ("niv_diario", 1), ("precio", 1), ("medias", 1),
                      ("bandas", 1), ("sistemas", 1), ("osciladores", 1), ("volat_ind", 1), ("comparadores", 1),
                      ("secuencias", 1)],
          stoplimit=[("stl_canal", 5), ("stl_vela", 3), ("stl_horario", 3), ("stl_diario", 1), ("stl_bandas", 2),
                     ("stl_medias", 1), ("stl_sistemas", 1), ("stl_estructura", 1), ("stl_rangos", 2)],
          pesos={"Indicators.Lowest": 1, "Indicators.LowestInRange": 1, "Prices.SessionLow": 1, L + "Lowest": 1,
                 L + "Low": 1, L + "LowestInRange": 1, L + "SessionLow": 1, L + "LowD": 1},
          params=P(P_MOMENTUM, P_FUERZA, P_SUPERTREND, roc_params(0, 1, 0.05),
                   ventana(*ASIA_RANGO, *ASIA_SESION, {"BarHourIs": {"Hour": (9, 18, 1)},
                                                       "BarHourIsBigger": {"Hour": (8, 12, 1)},
                                                       "BarHourIsSmaller": {"Hour": (12, 19, 1)}})),
      ),
      block_why="Núcleo: ruptura de canal/bandas y de los extremos de la sesión asiática (pesos 4-10, y órdenes "
                "stop en esos niveles, que son las que materializan la ruptura). Filtros a peso 1: expansión de "
                "volatilidad, momentum, tendencia corta, fuerza y hora. Sin bloques de nivel absoluto.",
      orders={"EnterAtStop": (True, 3), "EnterAtMarket": (True, 1), "EnterAtLimit": (False, 1)},
      bars_valid=(1, 3), orders_why="Orden stop en el nivel de ruptura: entra sólo si la ruptura ocurre; "
                                    "validez 1-3 velas (5-15 min) para no comprar rupturas viejas.",
      sltp=dict(sl=(1.0, 2.5, 14, 50), pt=(1.0, 3.0, 14, 50), pt_required=True, rrr=(80, 250)),
      exits=dict(pt=(True, 100), trailing=None, be=(True, 50, 0.5, 1.5), eab=(True, 50, 6, 36), rule=(True, 30)),
      exits_why="SL/PT en ATR de M5 (adaptativos); break-even rápido; salida temporal 30 min-3 h: la "
                "ventaja de un scalp se agota en pocas velas.",
      edge_eab=(3, 24), edge_why="Test de ventaja: salida pura por tiempo 15 min-2 h, sin SL/PT.",
      fitness={"SQN": 2, "ReturnDDRatio": 1},
      fitness_why="SQN premia expectativa consistente con muchas operaciones (lo propio de un scalper); "
                  "Ret/DD evita curvas con drawdowns profundos.",
      edge_fitness={"SQN": 2, "StagnationPct": 1},
      filt=dict(retdd=6, win=45, pf=1.25, avgbars=3, oos_pf=1.1),
      genetic=dict(pop=40, gens=30, islands=4),
      risk=50,
      retest=dict(precision=3, mc_sims=200, spread=(2, 4), slip=(0, 1), start_bar=False, spp_tests=1500,
                  spp_dist=20, spp_profit=80, whatif="pct5", dd_max=20, mc_dd_pct=150),
      retest_why="Precisión 3 (tick real con spread real): en M5 el spread variable decide el resultado.",
      riesgos="Sensibilidad extrema a costes y latencia; datos M1 con spread fijo sobreestiman; el "
              "deslizamiento real en aperturas es mayor que el modelado.",
      ),
    # =====================================================================================
    S("DayTrading", "Day Trading (ruptura del rango asiático)", "M15",
      tesis="El rango de la sesión asiática concentra órdenes en sus extremos; la apertura de Londres "
            "aporta el volumen que rompe uno de ellos y el movimiento tiende a extenderse durante la "
            "sesión europea. Se cierra todo al final del día: no se asume riesgo nocturno.",
      instrumento="GBPUSD/GBPJPY/EURJPY (rango asiático + apertura de Londres) o DAX/US30 con su "
                  "apertura de contado. GBPJPY es razonable aquí.",
      build_dates=BUILD_STD, valid=VALID_STD, slippage="0.3",
      slippage_why="El original usa 0; 0,3 pips por ejecución stop en apertura de Londres.",
      density=120,
      options={
          "LimitTimeRange": ("true", "Entradas sólo en Londres + NY temprano."),
          "SignalTimeRangeFrom": (SECONDS("09:00"), "Apertura de Londres (servidor UTC+2)."),
          "SignalTimeRangeTo": (SECONDS("19:00"), "Tras las 19:00 queda poco recorrido intradía."),
          "ExitAtEndOfDay": ("true", "Definición de day trading: plano al cierre."),
          "EODExitTime": (SECONDS("22:30"), "Antes del rollover de las 00:00 servidor."),
          "ExitOnFriday": ("true", "Sin exposición de fin de semana."),
          "FridayExitTime": (SECONDS("21:30"), "Viernes, cierre algo antes."),
          "MaxTradesPerDay": ("3", "La ruptura y hasta dos reintentos."),
          "MaxDistanceFromMarket": ("true", "Evita órdenes stop alejadas del precio."),
          "MaxDistancePct": ("0.6", "≈ 90 pips en GBPJPY: cubre rangos asiáticos amplios."),
          "ReservedBars": ("120", "≥ periodo máximo (100)."),
      },
      complexity=dict(entry=(1, 3), exit_cond=(1, 2), exit_types=(2, 4), period=(5, 100), shift=(1, 1)),
      complexity_why="5-100 velas de M15 = 1 h 15 min a 25 h: contexto intradía y del día anterior.",
      blocks=dict(
          signals=[("rup_canal", 8), ("rup_bandas", 3), ("rup_ichimoku", 1), ("vol_expansion", 2), ("vol_tick", 1),
                   ("mom_direccion", 1), ("mom_nivel", 1), ("tend_medias", 1), ("tend_sistemas", 1), ("fuerza", 1),
                   ("tiempo_intradia", 2)],
          indicators=[("niv_horario", 4), ("niv_canal", 2), ("niv_diario", 2), ("precio", 1), ("medias", 1),
                      ("bandas", 1), ("sistemas", 1), ("osciladores", 1), ("fuerza_ind", 1), ("volat_ind", 1),
                      ("comparadores", 1), ("secuencias", 1)],
          stoplimit=[("stl_horario", 5), ("stl_diario", 3), ("stl_canal", 2), ("stl_vela", 2), ("stl_bandas", 1),
                     ("stl_medias", 1), ("stl_sistemas", 1), ("stl_estructura", 1), ("stl_rangos", 2)],
          pesos={"Indicators.LowestInRange": 2, "Prices.SessionLow": 2, L + "LowestInRange": 1, L + "SessionLow": 1,
                 L + "LowD": 1, L + "Lowest": 1, L + "Low": 1},
          params=P(P_MOMENTUM, P_FUERZA, P_SUPERTREND, roc_params(0, 1, 0.05),
                   ventana(*ASIA_RANGO, *ASIA_SESION, {"BarHourIs": {"Hour": (9, 18, 1)},
                                                       "BarHourIsBigger": {"Hour": (8, 12, 1)},
                                                       "BarHourIsSmaller": {"Hour": (12, 19, 1)}}),
                   {"Prices.SessionOpen": {"Start Hours": (8, 10, 1), "Start Minutes": (0, 0, 1)},
                    L + "SessionOpen": {"Start Hours": (8, 10, 1), "Start Minutes": (0, 0, 1)}}),
      ),
      block_why="Núcleo: extremos del rango asiático (HighestInRange 00:00-03:00 → 07:00-10:00 en horas "
                "enteras; el original usaba paso 30 sobre HHMM, que genera horas inválidas como 0060), niveles "
                "del día anterior y aperturas de sesión, con órdenes stop en ellos. Filtros amplios a peso 1.",
      orders={"EnterAtStop": (True, 3), "EnterAtMarket": (True, 1), "EnterAtLimit": (False, 1)},
      bars_valid=(2, 8), orders_why="Stop en el extremo del rango; válida 30 min-2 h.",
      sltp=dict(sl=(1.0, 2.5, 14, 60), pt=(1.5, 4.0, 14, 60), pt_required=False, rrr=None),
      exits=dict(pt=(True, 50), trailing=(True, 30, 1.5, 3.0), be=(True, 30, 1.0, 2.0), eab=None, rule=(True, 30)),
      exits_why="SL en ATR; objetivo opcional porque el cierre de fin de día ya acota la operación.",
      edge_eab=(4, 24), edge_why="Test de ventaja: salida por tiempo 1-6 h + cierre de fin de día.",
      fitness={"ReturnDDRatio": 2, "StagnationPct": 1},
      fitness_why="Ret/DD como el original; StagnationPct penaliza meses planos (típico de rupturas "
                  "intradía en régimen de baja volatilidad).",
      edge_fitness={"SQN": 2, "StagnationPct": 1},
      filt=dict(retdd=5, win=40, pf=1.25, avgbars=2, oos_pf=1.1),
      genetic=dict(pop=40, gens=40, islands=4),
      risk=50,
      retest=dict(precision=2, mc_sims=300, spread=(2, 4), slip=(0, 0.5), start_bar=False, spp_tests=3000,
                  spp_dist=20, spp_profit=85, whatif="pct5", dd_max=20, mc_dd_pct=150),
      retest_why="Tick real con spread personalizado, como el original.",
      riesgos="Dependencia del horario del servidor (DST); rupturas falsas en días sin catalizador; "
              "sobreajuste de la ventana horaria.",
      ),
    # =====================================================================================
    S("Swing", "Swing Trading (ruptura de consolidación multi-día)", "H4",
      tesis="Tras una contracción de volatilidad, la ruptura del rango tiende a continuar durante 1-5 "
            "días en la dirección del régimen de fondo. Se mantiene la posición noches y fines de semana.",
      instrumento="Pares mayores y cruces líquidos, índices (US30/DAX) y oro. GBPJPY apto (swap "
                  "relevante: comprobar).",
      build_dates=BUILD_STD, valid=VALID_STD, slippage="0.3",
      slippage_why="El original usa 0; 0,3 pips es conservador en H4.",
      density=45,
      options={
          "LimitTimeRange": ("false", "En H4 la ventana 01:30-23:30 excluiría la vela de las 00:00 "
                                      "(1/6 de las señales) sin motivo de estilo."),
          "MaxTradesPerDay": ("2", "Swing: hasta dos entradas diarias."),
          "MaxDistanceFromMarket": ("true", "Evita stops lejanos."),
          "MaxDistancePct": ("2", "2 %: holgura para rupturas de rangos de varios días."),
          "ReservedBars": ("150", "≥ periodo máximo (120)."),
      },
      complexity=dict(entry=(1, 3), exit_cond=(1, 2), exit_types=(2, 4), period=(5, 120), shift=(1, 1)),
      complexity_why="5-120 velas H4 = 1-20 días: horizonte de swing.",
      blocks=dict(
          signals=[("rup_canal", 8), ("rup_bandas", 3), ("rup_ichimoku", 2), ("vol_expansion", 1),
                   ("vol_contraccion", 1), ("mom_direccion", 1), ("mom_nivel", 1), ("tend_medias", 1),
                   ("tend_sistemas", 1), ("fuerza", 2), ("tiempo_calendario", 1)],
          indicators=[("niv_canal", 3), ("niv_diario", 2), ("niv_semanal", 2), ("precio", 1), ("medias", 1),
                      ("bandas", 1), ("sistemas", 1), ("osciladores", 1), ("fuerza_ind", 1), ("volat_ind", 1),
                      ("estructura", 1), ("comparadores", 1), ("secuencias", 1)],
          stoplimit=[("stl_canal", 5), ("stl_diario", 2), ("stl_semanal", 2), ("stl_vela", 1), ("stl_bandas", 2),
                     ("stl_medias", 1), ("stl_sistemas", 1), ("stl_estructura", 1), ("stl_rangos", 2)],
          pesos={"Indicators.Lowest": 1, L + "Lowest": 1, L + "LowD": 1, L + "LowW": 1},
          params=P(P_MOMENTUM, P_FUERZA, P_SUPERTREND, roc_params(0, 3, 0.1)),
      ),
      block_why="Núcleo: ruptura de máximos de N velas/día/semana, bandas y nube de Ichimoku, con órdenes stop; "
                "filtros de régimen (ADX, KER, medias, sistemas de tendencia), volatilidad y calendario.",
      orders={"EnterAtStop": (True, 3), "EnterAtMarket": (True, 1), "EnterAtLimit": (False, 1)},
      bars_valid=(2, 6), orders_why="Stop válida 8-24 h.",
      sltp=dict(sl=(1.5, 3.5, 14, 100), pt=(2.0, 6.0, 14, 100), pt_required=False, rrr=None),
      exits=dict(pt=(True, 50), trailing=(True, 50, 2.0, 4.0), be=(True, 30, 1.0, 2.0), eab=(True, 40, 6, 30),
                 rule=(True, 30)),
      exits_why="Stop amplio en ATR, objetivo y trailing opcionales, salida temporal 1-5 días.",
      edge_eab=(6, 30), edge_why="Test de ventaja: salida por tiempo 1-5 días.",
      fitness={"ReturnDDRatio": 2, "Stability": 1},
      fitness_why="Ret/DD + estabilidad de la curva.",
      edge_fitness={"SQN": 2, "StagnationPct": 1},
      filt=dict(retdd=4, win=38, pf=1.3, avgbars=3, oos_pf=1.1),
      genetic=dict(pop=50, gens=40, islands=4),
      risk=100,
      retest=dict(precision=2, mc_sims=500, spread=(2, 4), slip=(0, 0.5), start_bar=True, spp_tests=5000,
                  spp_dist=20, spp_profit=85, whatif="top2", dd_max=20, mc_dd_pct=150),
      retest_why="Se añade aleatorizar la vela de inicio: el resultado no debe depender del punto de arranque.",
      riesgos="Gaps de fin de semana; swap; exposición nocturna.",
      ),
    # =====================================================================================
    S("Position", "Position Trading (momentum de medio-largo plazo)", "D1",
      tesis="El momentum de series temporales (rupturas de máximos de semanas/meses y pendiente de medias "
            "largas) es una de las anomalías más documentadas. Para obtener una muestra estadística útil en "
            "un solo mercado, las posiciones duran de 1 a 8 semanas (no meses).",
      instrumento="Índices (US500/US30/DAX), oro, y pares con tendencia macro. Recomendable ≥15 años de datos.",
      build_dates=BUILD_STD, valid=None, slippage="0.5",
      slippage_why="D1 entra a la apertura del día (a menudo tras gap): 0,5 pips conservador.",
      density=20,
      options={
          "LimitTimeRange": ("false", "Con velas D1 (apertura 00:00) la ventana 01:30-23:30 del original "
                                      "podría bloquear todas las señales."),
          "MaxTradesPerDay": ("1", "Position: una entrada como máximo."),
          "MaxDistanceFromMarket": ("true", "Tope de distancia para stops."),
          "MaxDistancePct": ("5", "5 %: rupturas de máximos de 20-250 días."),
          "ReservedBars": ("260", "≥ periodo máximo (250)."),
      },
      complexity=dict(entry=(1, 2), exit_cond=(1, 1), exit_types=(1, 3), period=(20, 250), shift=(1, 1)),
      complexity_why="20-250 días (1 mes-1 año). Máximo 2 condiciones: con ~20 operaciones/año cada grado "
                     "de libertad extra es sobreajuste casi seguro.",
      blocks=dict(
          signals=[("rup_canal", 8), ("rup_ichimoku", 1), ("mom_direccion", 1), ("mom_nivel", 2),
                   ("tend_medias", 2), ("tend_sistemas", 2), ("fuerza", 1), ("tiempo_calendario", 1)],
          indicators=[("niv_canal", 3), ("niv_semanal", 2), ("niv_mensual", 2), ("precio", 1), ("medias", 2),
                      ("sistemas", 1), ("osciladores", 1), ("fuerza_ind", 1), ("volat_ind", 1), ("comparadores", 1),
                      ("secuencias", 1)],
          stoplimit=[("stl_canal", 4), ("stl_semanal", 2), ("stl_mensual", 2), ("stl_vela", 1), ("stl_medias", 1),
                     ("stl_sistemas", 1), ("stl_rangos", 1)],
          pesos={"Indicators.Lowest": 1, L + "Lowest": 1, L + "LowW": 1, L + "LowM": 1},
          params=P(P_MOMENTUM, P_FUERZA, P_SUPERTREND, roc_params(0, 15, 1)),
      ),
      block_why="Núcleo: nuevos máximos de 20-250 días, semanales y mensuales; momentum sin niveles absolutos "
                "(ROC en %, MACD/OSMA frente a cero) y tendencia de medias/sistemas.",
      orders={"EnterAtMarket": (True, 2), "EnterAtStop": (True, 2), "EnterAtLimit": (False, 1)},
      bars_valid=(1, 5), orders_why="A mercado o con stop sobre el máximo, válida 1-5 días.",
      sltp=dict(sl=(2.5, 5.0, 20, 100), pt=(6.0, 12.0, 20, 100), pt_required=False, rrr=None),
      exits=dict(pt=(False, 30), trailing=(True, 70, 2.5, 5.0), be=None, eab=(True, 30, 10, 40), rule=(True, 50)),
      exits_why="Sin objetivo (dejar correr); trailing de 2,5-5 ATR como salida principal; salida por "
                "regla y temporal de 2-8 semanas.",
      edge_eab=(5, 40), edge_why="Test de ventaja: salida por tiempo 1-8 semanas.",
      fitness={"ReturnDDRatio": 2, "Stability": 1},
      fitness_why="Ret/DD + estabilidad; SQN es poco fiable con <200 operaciones.",
      edge_fitness={"ProfitFactor": 2, "StagnationPct": 1},
      filt=dict(retdd=3, win=33, pf=1.4, avgbars=4, oos_pf=None),
      genetic=dict(pop=50, gens=30, islands=4),
      risk=100,
      retest=dict(precision=2, mc_sims=500, spread=(2, 4), slip=(0, 1), start_bar=True, spp_tests=8000,
                  spp_dist=30, spp_profit=90, whatif="top2", dd_max=25, mc_dd_pct=175),
      retest_why="SPP ±30 %: con periodos largos la superficie debe ser lisa; exigencia 90 %.",
      riesgos="Muestra limitada; dependencia de pocas operaciones grandes; swap acumulado; cambio de régimen macro.",
      ),
    # =====================================================================================
    S("TrendFollowing", "Seguimiento de tendencia (multi-filtro con trailing)", "H1",
      tesis="Las tendencias persisten más de lo que predice un paseo aleatorio (reacción lenta a la "
            "información, flujos institucionales). Se entra cuando varios filtros de tendencia coinciden "
            "y se sale por trailing: pocas ganancias grandes pagan muchas pérdidas pequeñas. En H1 para "
            "tener una muestra de cientos de operaciones (tendencias de 1-5 días).",
      instrumento="Índices, metales y cruces de JPY. En un solo símbolo el resultado depende de pocas "
                  "tendencias: validar en varios mercados.",
      build_dates=BUILD_STD, valid=VALID_STD, slippage="0.3",
      slippage_why="El original usa 0.",
      density=50,
      options={
          "MaxTradesPerDay": ("2", "Hasta dos entradas diarias."),
          "MaxDistanceFromMarket": ("true", "Tope para órdenes stop."),
          "MaxDistancePct": ("2", "2 %: rupturas de canales largos en H1."),
          "ReservedBars": ("260", "≥ periodo máximo (250)."),
      },
      complexity=dict(entry=(1, 3), exit_cond=(1, 2), exit_types=(2, 4), period=(10, 250), shift=(1, 1)),
      complexity_why="10-250 velas H1 = 10 h a 10 días.",
      blocks=dict(
          signals=[("tend_sistemas", 4), ("tend_medias", 2), ("fuerza", 3), ("rup_canal", 6), ("rup_ichimoku", 2),
                   ("rup_bandas", 1), ("mom_direccion", 1), ("mom_nivel", 1), ("vol_expansion", 1)],
          indicators=[("medias", 2), ("sistemas", 2), ("niv_canal", 2), ("niv_diario", 1), ("precio", 1),
                      ("bandas", 1), ("fuerza_ind", 1), ("osciladores", 1), ("volat_ind", 1), ("comparadores", 1),
                      ("secuencias", 1)],
          stoplimit=[("stl_canal", 4), ("stl_sistemas", 2), ("stl_medias", 1), ("stl_bandas", 1), ("stl_vela", 1),
                     ("stl_diario", 1), ("stl_rangos", 2)],
          pesos={"Indicators.Lowest": 1, L + "Lowest": 1},
          params=P(P_MOMENTUM, P_FUERZA, P_SUPERTREND, roc_params(0, 3, 0.1)),
      ),
      block_why="Núcleo: sistemas y medias de tendencia, fuerza (ADX/KER) y ruptura de canal; sin osciladores "
                "de sobrecompra/sobreventa (contradicen la tesis).",
      orders={"EnterAtMarket": (True, 2), "EnterAtStop": (True, 2), "EnterAtLimit": (False, 1)},
      bars_valid=(1, 4), orders_why="A mercado con confirmación o stop sobre máximo reciente.",
      sltp=dict(sl=(2.0, 4.0, 14, 100), pt=(4.0, 10.0, 14, 100), pt_required=False, rrr=None),
      exits=dict(pt=(True, 30), trailing=(True, 80, 2.5, 5.0), be=None, eab=None, rule=(True, 50)),
      exits_why="El trailing (prob. 80 %) es la salida natural; objetivo raro y lejano.",
      edge_eab=(12, 72), edge_why="Test de ventaja: salida por tiempo 12 h-3 días.",
      fitness={"ReturnDDRatio": 2, "StagnationPct": 1},
      fitness_why="El talón de Aquiles del TF son las rachas planas largas: StagnationPct las penaliza.",
      edge_fitness={"SQN": 2, "StagnationPct": 1},
      filt=dict(retdd=3.5, win=30, pf=1.3, avgbars=5, oos_pf=1.05),
      genetic=dict(pop=50, gens=40, islands=4),
      risk=100,
      retest=dict(precision=2, mc_sims=500, spread=(2, 4), slip=(0, 0.5), start_bar=True, spp_tests=5000,
                  spp_dist=30, spp_profit=90, whatif="top2", dd_max=25, mc_dd_pct=175),
      retest_why="What-if quita las 2 mejores operaciones: mide la dependencia de outliers (esperable "
                 "en TF, pero no puede volverse perdedor).",
      riesgos="Win rate bajo (30-40 %) y rachas perdedoras largas; dependencia de pocas tendencias.",
      ),
    # =====================================================================================
    S("Range", "Trading de rango (reversión a la media en régimen lateral)", "H1",
      tesis="Cuando la tendencia es débil (ADX bajo, eficiencia de Kaufman baja) los excesos respecto a "
            "la media se corrigen: se compra el exceso bajista (o se vende el alcista en SELL) y se sale "
            "en la media con objetivo corto.",
      instrumento="EURCHF, EURGBP, AUDNZD, USDCAD en sesión asiática o índices en rango. GBPJPY es "
                  "tendencial y mal candidato: usar sólo como prueba.",
      build_dates=BUILD_STD, valid=VALID_STD, slippage="0.3",
      slippage_why="El original usa 0.",
      density=60,
      options={
          "LimitTimeRange": ("true", "Ventana de baja direccionalidad."),
          "SignalTimeRangeFrom": (SECONDS("01:30"), "Igual que el original: evita rollover."),
          "SignalTimeRangeTo": (SECONDS("09:30"), "Sesión asiática: menor deriva direccional en FX."),
          "MaxTradesPerDay": ("2", "Evita promediar en tendencia."),
          "MaxDistanceFromMarket": ("true", "Las órdenes límite lejanas casi nunca se ejecutan."),
          "MaxDistancePct": ("1", "1 %."),
          "ReservedBars": ("80", "≥ periodo máximo (60)."),
      },
      complexity=dict(entry=(1, 3), exit_cond=(1, 2), exit_types=(2, 4), period=(5, 60), shift=(1, 1)),
      complexity_why="5-60 velas H1: la reversión a la media es un fenómeno de corto plazo.",
      blocks=dict(
          signals=[("rev_bandas", 6), ("sobreventa", 3), ("lateral", 4), ("falsa_ruptura", 3),
                   ("vol_contraccion", 1), ("velas", 1), ("tiempo_intradia", 1)],
          indicators=[("bandas", 3), ("medias", 2), ("niv_canal", 2), ("niv_horario", 1), ("niv_diario", 1),
                      ("precio", 1), ("osciladores", 2), ("fuerza_ind", 1), ("volat_ind", 1), ("comparadores", 1),
                      ("secuencias", 2)],
          stoplimit=[("stl_bandas", 5), ("stl_canal", 2), ("stl_vela", 2), ("stl_medias", 2), ("stl_diario", 1),
                     ("stl_horario", 1), ("stl_estructura", 1), ("stl_rangos", 2)],
          pesos={L + "Lowest": 3, L + "Highest": 1, L + "Low": 3, L + "High": 1, L + "LowD": 2, L + "HighD": 1,
                 L + "LowestInRange": 2, L + "HighestInRange": 1, L + "SessionLow": 2, L + "SessionHigh": 1,
                 "Doji": 1},
          params=P(P_SOBREVENTA, P_LATERAL, P_SUPERTREND,
                   ventana(*ASIA_RANGO, *ASIA_SESION, {"BarHourIs": {"Hour": (1, 9, 1)},
                                                       "BarHourIsBigger": {"Hour": (1, 4, 1)},
                                                       "BarHourIsSmaller": {"Hour": (5, 10, 1)}})),
      ),
      block_why="Núcleo: reentrada en bandas tras exceso, osciladores restringidos a sobreventa (sobrecompra en "
                "SELL) y filtros de régimen lateral; órdenes límite en la banda/extremo. Los rangos 0-100 "
                "originales permitían 'comprar en sobrecompra'.",
      orders={"EnterAtLimit": (True, 3), "EnterAtMarket": (True, 1), "EnterAtStop": (False, 1)},
      bars_valid=(1, 5), orders_why="Límite bajo la banda/mínimo (sobre la banda/máximo en SELL): se opera el "
                                    "exceso, no la ruptura.",
      sltp=dict(sl=(1.5, 3.0, 14, 60), pt=(0.8, 2.0, 14, 60), pt_required=True, rrr=(40, 120)),
      exits=dict(pt=(True, 100), trailing=None, be=None, eab=(True, 50, 5, 30), rule=(True, 50)),
      exits_why="Objetivo corto obligatorio (PT 40-120 % del SL) y alta tasa de acierto; salida "
                "temporal: si no revierte en 5-30 h la tesis falló.",
      edge_eab=(3, 24), edge_why="Test de ventaja: salida por tiempo 3-24 h.",
      fitness={"ReturnDDRatio": 2, "ProfitFactor": 1},
      fitness_why="PF alto es imprescindible en reversión (pérdidas medias > ganancias medias).",
      edge_fitness={"SQN": 2, "StagnationPct": 1},
      filt=dict(retdd=4, win=55, pf=1.25, avgbars=2, oos_pf=1.1),
      genetic=dict(pop=40, gens=40, islands=4),
      risk=75,
      retest=dict(precision=2, mc_sims=500, spread=(2, 4), slip=(0, 0.5), start_bar=False, spp_tests=5000,
                  spp_dist=20, spp_profit=85, whatif="pct5", dd_max=20, mc_dd_pct=150),
      retest_why="What-if excluye el 5 % de mejores y peores: una reversión sana no depende de outliers.",
      riesgos="Pérdida grande cuando el rango se rompe (cola izquierda); el SL es imprescindible.",
      ),
    # =====================================================================================
    S("PriceAction", "Acción del precio (patrones de vela en niveles)", "H1",
      tesis="Patrones de rechazo/absorción (envolvente, martillo, pauta penetrante, fractal y sus "
            "equivalentes bajistas en SELL) en niveles relevantes señalan desequilibrios de órdenes; se "
            "entra con stop sobre el extremo de la vela señal.",
      instrumento="Cualquier mercado líquido; mejor en índices y mayores. GBPJPY apto.",
      build_dates=BUILD_STD, valid=VALID_STD, slippage="0.3",
      slippage_why="El original usa 0.",
      density=60,
      options={
          "MaxTradesPerDay": ("2", "Evita encadenar señales en el mismo nivel."),
          "MaxDistanceFromMarket": ("true", "Tope para stops."),
          "MaxDistancePct": ("1", "1 %."),
          "ReservedBars": ("60", "≥ periodo máximo (50)."),
      },
      complexity=dict(entry=(1, 3), exit_cond=(1, 2), exit_types=(2, 4), period=(2, 50), shift=(1, 3)),
      complexity_why="Periodos 2-50 (estructura reciente); desplazamiento 1-3 para patrones de 2-3 velas.",
      blocks=dict(
          signals=[("velas", 8), ("falsa_ruptura", 4), ("rup_canal", 3), ("rup_bandas", 1), ("vol_expansion", 1),
                   ("vol_contraccion", 1), ("tiempo_intradia", 1), ("tiempo_calendario", 1)],
          indicators=[("precio", 3), ("heiken", 2), ("niv_diario", 2), ("niv_semanal", 1), ("niv_horario", 1),
                      ("niv_canal", 2), ("estructura", 2), ("volat_ind", 1), ("comparadores", 2), ("secuencias", 2)],
          stoplimit=[("stl_vela", 5), ("stl_canal", 2), ("stl_diario", 2), ("stl_semanal", 1), ("stl_horario", 1),
                     ("stl_estructura", 2), ("stl_heiken", 1), ("stl_rangos", 2)],
          pesos={"Doji": 2, L + "Low": 1, L + "Lowest": 1, L + "LowD": 1, L + "LowW": 1, L + "LowestInRange": 1,
                 L + "SessionLow": 1},
          params=ventana(*ASIA_RANGO, *ASIA_SESION, None),
      ),
      block_why="Núcleo: velas de giro y falsas rupturas, precio puro, Heikin-Ashi y estructura (niveles "
                "diarios/semanales, fractales); ATR sólo como normalizador. Sin osciladores ni medias.",
      orders={"EnterAtStop": (True, 3), "EnterAtLimit": (True, 1), "EnterAtMarket": (True, 1)},
      bars_valid=(1, 3), orders_why="Stop sobre el extremo de la vela señal (confirmación) o límite en retroceso.",
      sltp=dict(sl=(1.0, 2.5, 14, 50), pt=(1.5, 4.0, 14, 50), pt_required=True, rrr=(150, 300)),
      exits=dict(pt=(True, 100), trailing=None, be=(True, 50, 1.0, 2.0), eab=(True, 30, 5, 30), rule=(True, 30)),
      exits_why="R:R 1,5-3 sobre el riesgo de la vela; break-even tras 1-2 ATR.",
      edge_eab=(3, 24), edge_why="Test de ventaja: salida por tiempo 3-24 h.",
      fitness={"ReturnDDRatio": 2, "SQN": 1},
      fitness_why="Ret/DD + SQN (consistencia por operación).",
      edge_fitness={"SQN": 2, "StagnationPct": 1},
      filt=dict(retdd=4, win=40, pf=1.3, avgbars=2, oos_pf=1.1),
      genetic=dict(pop=40, gens=40, islands=4),
      risk=100,
      retest=dict(precision=2, mc_sims=500, spread=(2, 4), slip=(0, 0.5), start_bar=False, spp_tests=5000,
                  spp_dist=20, spp_profit=85, whatif="pct5", dd_max=20, mc_dd_pct=150),
      retest_why="Igual que el original + what-if de outliers.",
      riesgos="Los patrones de vela tienen poca ventaja aislada; el sesgo de minería de datos es alto.",
      ),
    # =====================================================================================
    S("NewsProxy", "Noticias (APROXIMACIÓN horaria: ventana de datos de EE. UU.)", "M15",
      tesis="Las publicaciones macro programadas de EE. UU. (8:30 ET = 15:30 servidor) provocan una "
            "expansión de volatilidad; se opera la ruptura del rango previo dentro de esa ventana. NO "
            "es news trading real: SQX no tiene calendario económico; la estrategia opera la ventana "
            "todos los días, haya o no noticia.",
      instrumento="EURUSD/USDJPY/oro/US30 (reaccionan a datos de EE. UU.). Exige datos tick con spread real.",
      build_dates=BUILD_FAST, valid=VALID_FAST, slippage="1.5",
      slippage_why="En publicaciones el deslizamiento real es de varios pips; 1,5 pips es el mínimo prudente.",
      density=60,
      options={
          "LimitTimeRange": ("true", "Ventana de publicación."),
          "SignalTimeRangeFrom": (SECONDS("15:00"), "Media hora antes de las 15:30 (8:30 ET)."),
          "SignalTimeRangeTo": (SECONDS("17:00"), "Incluye datos de las 10:00 ET (17:00 servidor)."),
          "ExitAtEndOfDay": ("true", "Sin exposición nocturna."),
          "EODExitTime": (SECONDS("22:00"), "Antes del rollover."),
          "ExitOnFriday": ("true", "El NFP cae en viernes: no arrastrar al fin de semana."),
          "FridayExitTime": (SECONDS("21:00"), "Viernes."),
          "MaxTradesPerDay": ("1", "Una reacción por día."),
          "MaxDistanceFromMarket": ("true", "Tope para stops."),
          "MaxDistancePct": ("0.5", "0,5 %."),
          "ReservedBars": ("60", "≥ periodo máximo (48)."),
      },
      complexity=dict(entry=(1, 3), exit_cond=(1, 1), exit_types=(2, 4), period=(4, 48), shift=(1, 1)),
      complexity_why="4-48 velas M15 (1-12 h): contexto del día de la publicación.",
      blocks=dict(
          signals=[("tiempo_intradia", 4), ("vol_expansion", 4), ("vol_tick", 2), ("rup_canal", 6), ("rup_bandas", 2),
                   ("mom_direccion", 1)],
          indicators=[("niv_horario", 4), ("niv_canal", 2), ("niv_diario", 1), ("precio", 1), ("volat_ind", 2),
                      ("bandas", 1), ("medias", 1), ("comparadores", 1), ("secuencias", 1)],
          stoplimit=[("stl_horario", 5), ("stl_canal", 2), ("stl_vela", 2), ("stl_diario", 1), ("stl_bandas", 1),
                     ("stl_rangos", 3)],
          pesos={"Indicators.LowestInRange": 2, "Prices.SessionLow": 2, L + "LowestInRange": 1, L + "SessionLow": 1,
                 L + "Lowest": 1, L + "Low": 1, L + "LowD": 1},
          params=ventana(*PRE_US_RANGO, *PRE_US_SESION, {"BarHourIs": {"Hour": (15, 16, 1)},
                                                         "BarHourIsBigger": {"Hour": (14, 16, 1)},
                                                         "BarHourIsSmaller": {"Hour": (16, 18, 1)}}),
      ),
      block_why="Núcleo: rango previo a la publicación (12:00-15:00 → 15:00/15:30), filtros de hora/día y "
                "expansión de volatilidad y de volumen de ticks; órdenes stop sobre el rango pre-dato.",
      orders={"EnterAtStop": (True, 3), "EnterAtMarket": (True, 1), "EnterAtLimit": (False, 1)},
      bars_valid=(1, 4), orders_why="Stop sobre el rango pre-dato (bajo él en SELL), caduca en 15-60 min.",
      sltp=dict(sl=(1.0, 2.0, 10, 40), pt=(1.5, 4.0, 10, 40), pt_required=False, rrr=None),
      exits=dict(pt=(True, 50), trailing=None, be=(True, 50, 0.5, 1.5), eab=(True, 70, 2, 16), rule=None),
      exits_why="El impulso de una noticia dura minutos/horas: salida temporal 30 min-4 h.",
      edge_eab=(2, 12), edge_why="Test de ventaja: salida por tiempo 30 min-3 h.",
      fitness={"ReturnDDRatio": 2, "ProfitFactor": 1},
      fitness_why="Operaciones con mucha varianza: PF + Ret/DD.",
      edge_fitness={"SQN": 2, "StagnationPct": 1},
      filt=dict(retdd=3, win=35, pf=1.3, avgbars=2, oos_pf=1.05),
      genetic=dict(pop=40, gens=30, islands=4),
      risk=50,
      retest=dict(precision=3, mc_sims=200, spread=(2, 8), slip=(0, 3), start_bar=False, spp_tests=1500,
                  spp_dist=20, spp_profit=80, whatif="pct5", dd_max=20, mc_dd_pct=150),
      retest_why="Spread aleatorio hasta 4x y deslizamiento hasta 3 pips: así es una publicación real.",
      riesgos="No distingue días con/sin noticia; horario DST; spreads y deslizamiento reales muy "
              "superiores a los de datos M1; requotes.",
      ),
]

STYLE_BY_NAME = {s["name"]: s for s in STYLES}
SIDES = ("BUY", "SELL")


# ----------------------------------------------------------------------------------------- operaciones mínimas
def _years(a: str, b: str) -> float:
    from datetime import date
    y0, m0, d0 = map(int, a.split("."))
    y1, m1, d1 = map(int, b.split("."))
    return (date(y1, m1, d1) - date(y0, m0, d0)).days / 365.25


def _r10(x: float) -> int:
    return int(round(x / 10.0)) * 10


def min_trades(st: dict) -> dict:
    """Mínimos de operaciones derivados de la densidad (operaciones/año) del estilo.

    Builder: IS = densidad × años IS; OOS (validación) = 80 % de lo proporcional.
    Retest: periodo completo = 90 % de lo proporcional (10,8 años); holdout 2021-2024 = 80 %.
    """
    dens = st["density"]
    b0, b1 = st["build_dates"]
    if st["valid"]:
        is_years = _years(b0, st["valid"][0])
        oos_years = _years(*st["valid"])
    else:
        is_years, oos_years = _years(b0, b1), 0.0
    return {
        "is": _r10(dens * is_years),
        "oos": _r10(dens * oos_years * 0.8) if oos_years else 0,
        "full": _r10(dens * _years(*DATA_FULL) * 0.9),
        "holdout": _r10(dens * _years(*HOLDOUT) * 0.8),
        "per_year": dens,
        "build_total_years": _years(b0, b1),
    }
