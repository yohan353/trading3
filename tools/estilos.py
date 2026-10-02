"""Especificación de los 8 estilos objetivo.

Cada valor que se escribe en un .cfx sale de aquí y lleva su justificación. Las claves de bloques
son las del catálogo del propio archivo original (build 140.2099); validar_cfx.py comprueba que
existen. Los horarios están en hora del servidor de los datos (símbolo *_UTCPlus02).

Supuestos globales (ver docs/03, sección "Supuestos"):
* Símbolo: se conserva GBPJPY_M1_M1_UTCPlus02 (el que usan los 4 originales) para que los archivos
  carguen; cada ficha recomienda el instrumento más adecuado y la checklist obliga a revisar costes.
* Datos M1 disponibles de 2013.09.30 a 2024.07.22 (rango que usan los originales).
* Sólo largos (BUY), como los originales; la versión SELL se obtiene replicando el kit.
* Capital 10.000 y tolerancia de drawdown máxima del 20 %.
"""

from sqx_cfx import SECONDS  # "09:30" -> segundos desde medianoche (formato de los Param de hora)

COMMON_WHY = {
    "simple": "El original dependía de una plantilla .sqx externa (Template_DOW_H1_BUY_1.8.4.sqx) que no viene "
              "en el .cfx; en modo 'simple' el archivo funciona por sí solo y la selección de bloques del "
              "estilo pasa a determinar la entrada. Para volver al flujo plantilla, ver docs/04 §A.3.",
}

# Rangos de fechas -------------------------------------------------------------------------
DATA_FULL = ("2013.09.30", "2024.07.22")          # rango de datos que usan los originales
HOLDOUT = ("2021.01.01", "2024.07.22")            # OOS final del Retest original (se conserva)
BUILD_STD = ("2013.09.30", "2020.12.31")          # periodo del Builder original
VALID_STD = ("2019.01.01", "2020.12.31")          # nuevo tramo de validación dentro del Builder
BUILD_FAST = ("2016.01.04", "2020.12.31")         # M5/M15: periodo más corto por coste de cómputo
VALID_FAST = ("2019.07.01", "2020.12.31")

# Grupos de bloques reutilizables -----------------------------------------------------------
CMP = ["IsGreater", "IsLower", "CrossesAbove", "CrossesBelow"]
PRICES_BAR = ["Prices.Close", "Prices.Open", "Prices.High", "Prices.Low"]
PRICES_D = ["Prices.HighD", "Prices.LowD", "Prices.OpenD", "Prices.CloseD"]
SESSION_ASIA = {"Start Hours": (1, 3, 1), "Start Minutes": (0, 0, 1), "End Hours": (8, 10, 1), "End Minutes": (0, 0, 1)}
RANGE_ASIA = {"Time From": (0, 300, 100), "Time To": (700, 1000, 100)}
RANGE_PRE_US = {"Time From": (1200, 1500, 100), "Time To": (1500, 1530, 30)}


def S(name, title, tf, **kw):
    kw.update(name=name, title=title, tf=tf)
    return kw


STYLES = [
    # =====================================================================================
    S("Scalping", "Scalping (micro-ruptura en sesión líquida)", "M5",
      tesis="En las aperturas de Londres y el solape Londres-Nueva York entra liquidez direccional; tras "
            "una micro-consolidación, la ruptura de su máximo tiende a continuar unas pocas velas. La "
            "ventaja es pequeña y sólo existe si el coste total (spread+comisión+deslizamiento) es una "
            "fracción pequeña del ATR de M5.",
      instrumento="EURUSD o índice US500/NAS100 con spread bruto ≤0,3 pips/0,5 pts + comisión. GBPJPY con "
                  "2 pips de spread NO es apto (coste ≈30 % del ATR de M5).",
      build_dates=BUILD_FAST, valid=VALID_FAST, slippage="0.5",
      slippage_why="El original usa 0; en M5 un deslizamiento de 0,5 pips por orden stop/mercado es "
                   "conservador-realista y cambia el signo de muchas estrategias.",
      options={
          "LimitTimeRange": ("true", "Sólo sesión líquida."),
          "SignalTimeRangeFrom": (SECONDS("09:00"), "09:00 servidor ≈ apertura de Londres (UTC+2)."),
          "SignalTimeRangeTo": (SECONDS("18:30"), "18:30 servidor ≈ final del solape Londres-NY."),
          "ExitAtEndOfRange": ("true", "Un scalper no arrastra posiciones fuera de su ventana."),
          "ExitAtEndOfDay": ("true", "Red de seguridad: nada abierto al cierre del día."),
          "EODExitTime": (SECONDS("21:00"), "Antes del rollover (spreads anchos)."),
          "ExitOnFriday": ("true", "Sin riesgo de gap de fin de semana."),
          "FridayExitTime": (SECONDS("20:00"), "Viernes tarde: liquidez decreciente."),
          "MaxTradesPerDay": ("4", "Limita sobre-operar en días de ruido."),
          "MaxDistanceFromMarket": ("true", "Evita órdenes stop lejos del precio."),
          "MaxDistancePct": ("0.3", "0,3 % ≈ 45 pips en GBPJPY; tope razonable para M5."),
          "ReservedBars": ("120", "≥ periodo máximo (100) para que los indicadores estén calculados."),
      },
      complexity=dict(entry=(1, 3), exit_cond=(1, 2), exit_types=(2, 4), period=(5, 100), shift=(1, 1)),
      complexity_why="Periodos 5-100 velas de M5 (25 min a 8 h): horizonte de micro-estructura; ≥100 no "
                     "aporta nada a un scalper y sobreajusta.",
      signals={"BarOpensAboveHighestAfterOpenBelow": 3, "BBBarOpensAboveUpAfterOpenBelow": 2,
               "BBBarClosesAboveUp": 1, "KCBarOpensAboveUpperAfterOpenBelow": 2, "KCBarClosesAboveUpper": 1,
               "ATRRising": 1, "ATRChangesUp": 1, "StdDevRising": 1, "LaguerreRSICrossUP": 1,
               "RSICrossUp": 1, "ADXRising": 1, "MARising": 1},
      indicators={"Indicators.Highest": 2, "Indicators.Lowest": 1, "Indicators.ATR": 1, "Indicators.EMA": 1,
                  "Indicators.BollingerBands": 1, "Indicators.KeltnerChannel": 1, "Prices.SessionHigh": 2,
                  "Prices.SessionLow": 1, **{k: 1 for k in PRICES_BAR}, **{k: 1 for k in CMP}, "IsGreaterCount": 1},
      stoplimit={"Stop/Limit Price Levels.Highest": 3, "Stop/Limit Price Levels.High": 2,
                 "Stop/Limit Price Levels.BollingerBands": 1, "Stop/Limit Price Levels.KeltnerChannel": 1,
                 "Stop/Limit Price Levels.SessionHigh": 2, "Stop/Limit Price Ranges.ATR": 2,
                 "Stop/Limit Price Ranges.BarRange": 1, "Stop/Limit Price Ranges.SmallestRange": 1},
      block_params={
          "Prices.SessionHigh": SESSION_ASIA, "Prices.SessionLow": SESSION_ASIA,
          "Stop/Limit Price Levels.SessionHigh": SESSION_ASIA,
          "LaguerreRSICrossUP": {"Gamma": (0.3, 0.8, 0.05), "Level": (0.4, 0.85, 0.05)},
          "RSICrossUp": {"Level": (50, 70, 5)},
      },
      block_why="Bloques de ruptura de rango corto (Donchian, Bollinger, Keltner, máximo de sesión asiática) "
                "+ confirmación de expansión de volatilidad sin niveles absolutos (dependientes de precio).",
      orders={"EnterAtStop": (True, 2), "EnterAtMarket": (True, 1), "EnterAtLimit": (False, 1)},
      bars_valid=(1, 3), orders_why="Orden stop por encima del máximo: entra sólo si la ruptura ocurre; "
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
      filt=dict(trades=1000, retdd=6, win=45, pf=1.25, avgbars=3, oos_pf=1.1),
      genetic=dict(pop=30, gens=30, islands=4),
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
      options={
          "LimitTimeRange": ("true", "Entradas sólo en Londres + NY temprano."),
          "SignalTimeRangeFrom": (SECONDS("09:00"), "Apertura de Londres (servidor UTC+2)."),
          "SignalTimeRangeTo": (SECONDS("19:00"), "Tras las 19:00 queda poco recorrido intradía."),
          "ExitAtEndOfDay": ("true", "Definición de day trading: plano al cierre."),
          "EODExitTime": (SECONDS("22:30"), "Antes del rollover de las 00:00 servidor."),
          "ExitOnFriday": ("true", "Sin exposición de fin de semana."),
          "FridayExitTime": (SECONDS("21:30"), "Viernes, cierre algo antes."),
          "MaxTradesPerDay": ("2", "Una ruptura y, como mucho, un reintento."),
          "MaxDistanceFromMarket": ("true", "Evita órdenes stop alejadas del precio."),
          "MaxDistancePct": ("0.6", "≈ 90 pips en GBPJPY: cubre rangos asiáticos amplios."),
          "ReservedBars": ("120", "≥ periodo máximo (100)."),
      },
      complexity=dict(entry=(1, 3), exit_cond=(1, 2), exit_types=(2, 4), period=(5, 100), shift=(1, 1)),
      complexity_why="5-100 velas de M15 = 1 h 15 min a 25 h: contexto intradía y del día anterior.",
      signals={"BarOpensAboveHighestAfterOpenBelow": 2, "BBBarOpensAboveUpAfterOpenBelow": 1,
               "KCBarOpensAboveUpperAfterOpenBelow": 1, "ADXRising": 1, "ADXHigher": 1, "ATRRising": 1,
               "MARising": 1, "MABarClosesAbove": 1, "LinRegRising": 1, "BarHourIsBigger": 1,
               "BarHourIsSmaller": 1},
      indicators={"Indicators.HighestInRange": 3, "Indicators.LowestInRange": 2, "Indicators.Highest": 1,
                  "Indicators.Lowest": 1, "Indicators.ATR": 1, "Indicators.EMA": 1, "Prices.SessionHigh": 2,
                  "Prices.SessionLow": 1, "Prices.SessionOpen": 1, **{k: 1 for k in PRICES_BAR},
                  **{k: 1 for k in PRICES_D}, **{k: 1 for k in CMP}},
      stoplimit={"Stop/Limit Price Levels.HighestInRange": 3, "Stop/Limit Price Levels.SessionHigh": 2,
                 "Stop/Limit Price Levels.HighD": 1, "Stop/Limit Price Levels.Highest": 1,
                 "Stop/Limit Price Levels.OpenD": 1, "Stop/Limit Price Ranges.ATR": 2,
                 "Stop/Limit Price Ranges.BarRange": 1},
      block_params={
          "Indicators.HighestInRange": RANGE_ASIA, "Indicators.LowestInRange": RANGE_ASIA,
          "Stop/Limit Price Levels.HighestInRange": RANGE_ASIA,
          "Prices.SessionHigh": SESSION_ASIA, "Prices.SessionLow": SESSION_ASIA,
          "Stop/Limit Price Levels.SessionHigh": SESSION_ASIA,
          "Prices.SessionOpen": {"Start Hours": (9, 10, 1), "Start Minutes": (0, 0, 1)},
          "ADXHigher": {"Level": (20, 40, 5)},
          "BarHourIsBigger": {"Hour": (8, 12, 1)}, "BarHourIsSmaller": {"Hour": (12, 19, 1)},
      },
      block_why="El nivel roto es el máximo del rango asiático (HighestInRange 00:00-03:00 → 07:00-10:00, "
                "en horas enteras: el rango original 0-2359 con paso 30 generaba horas HHMM inválidas como "
                "0060) y los niveles del día anterior.",
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
      filt=dict(trades=500, retdd=5, win=40, pf=1.25, avgbars=2, oos_pf=1.1),
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
      tesis="Tras una contracción de volatilidad de varios días, la ruptura del rango tiende a "
            "continuar durante 2-10 días en la dirección del régimen de fondo. Se mantiene la posición "
            "noches y fines de semana.",
      instrumento="Pares mayores y cruces líquidos, índices (US30/DAX) y oro. GBPJPY apto (swap "
                  "relevante: comprobar).",
      build_dates=BUILD_STD, valid=VALID_STD, slippage="0.3",
      slippage_why="El original usa 0; 0,3 pips es conservador en H4.",
      options={
          "LimitTimeRange": ("false", "En H4 la ventana 01:30-23:30 excluiría la vela de las 00:00 "
                                      "(1/6 de las señales) sin motivo de estilo."),
          "MaxTradesPerDay": ("1", "Swing: como mucho una entrada diaria."),
          "MaxDistanceFromMarket": ("true", "Evita stops lejanos."),
          "MaxDistancePct": ("2", "2 %: holgura para rupturas de rangos de varios días."),
          "ReservedBars": ("150", "≥ periodo máximo (120)."),
      },
      complexity=dict(entry=(1, 3), exit_cond=(1, 2), exit_types=(2, 4), period=(5, 120), shift=(1, 1)),
      complexity_why="5-120 velas H4 = 1-20 días: horizonte de swing.",
      signals={"BarOpensAboveHighestAfterOpenBelow": 3, "BBBarOpensAboveUpAfterOpenBelow": 1,
               "KCBarOpensAboveUpperAfterOpenBelow": 1, "IchimokuKumoBreakoutBullish": 1, "ADXRising": 1,
               "ADXHigher": 1, "MARising": 1, "MABarClosesAbove": 1, "RSIHigher": 1, "ATRRising": 1,
               "BBUpperRising": 1, "SuperTrendUPTrend": 1, "LinRegRising": 1, "KERaboveLevel": 1},
      indicators={"Indicators.Highest": 2, "Indicators.Lowest": 1, "Indicators.ATR": 1, "Indicators.SMA": 1,
                  "Indicators.EMA": 1, "Indicators.BollingerBands": 1, "Indicators.KeltnerChannel": 1,
                  **{k: 1 for k in PRICES_BAR}, "Prices.HighD": 1, "Prices.LowD": 1, "Prices.HighW": 1,
                  "Prices.LowW": 1, **{k: 1 for k in CMP}, "IsGreaterCount": 1},
      stoplimit={"Stop/Limit Price Levels.Highest": 3, "Stop/Limit Price Levels.HighD": 1,
                 "Stop/Limit Price Levels.HighW": 1, "Stop/Limit Price Levels.BollingerBands": 1,
                 "Stop/Limit Price Levels.KeltnerChannel": 1, "Stop/Limit Price Levels.High": 1,
                 "Stop/Limit Price Ranges.ATR": 2, "Stop/Limit Price Ranges.BarRange": 1,
                 "Stop/Limit Price Ranges.BBRange": 1},
      block_params={"ADXHigher": {"Level": (20, 40, 5)}, "RSIHigher": {"Level": (50, 70, 5)},
                    "KERaboveLevel": {"Level": (0.2, 0.6, 0.05)}},
      block_why="Ruptura de máximos de N días (Donchian/Bollinger/Keltner/Kumo) filtrada por régimen "
                "(ADX, pendiente de medias, eficiencia de Kaufman).",
      orders={"EnterAtStop": (True, 2), "EnterAtMarket": (True, 1), "EnterAtLimit": (False, 1)},
      bars_valid=(2, 6), orders_why="Stop válida 8-24 h.",
      sltp=dict(sl=(1.5, 3.5, 14, 100), pt=(2.0, 6.0, 14, 100), pt_required=False, rrr=None),
      exits=dict(pt=(True, 50), trailing=(True, 50, 2.0, 4.0), be=(True, 30, 1.0, 2.0), eab=(True, 30, 10, 40),
                 rule=(True, 30)),
      exits_why="Stop amplio en ATR, objetivo y trailing opcionales, salida temporal 2-7 días.",
      edge_eab=(6, 30), edge_why="Test de ventaja: salida por tiempo 1-5 días.",
      fitness={"ReturnDDRatio": 2, "Stability": 1},
      fitness_why="Ret/DD + estabilidad de la curva: un swing con 30 operaciones/año necesita curvas regulares.",
      edge_fitness={"SQN": 2, "StagnationPct": 1},
      filt=dict(trades=150, retdd=4, win=38, pf=1.3, avgbars=3, oos_pf=1.1),
      genetic=dict(pop=50, gens=40, islands=4),
      risk=100,
      retest=dict(precision=2, mc_sims=500, spread=(2, 4), slip=(0, 0.5), start_bar=True, spp_tests=5000,
                  spp_dist=20, spp_profit=85, whatif="top2", dd_max=20, mc_dd_pct=150),
      retest_why="Se añade aleatorizar la vela de inicio: con pocas operaciones el punto de arranque importa.",
      riesgos="Gaps de fin de semana; swap; pocas operaciones por año → estadística débil.",
      ),
    # =====================================================================================
    S("Position", "Position Trading (momentum de largo plazo)", "D1",
      tesis="El momentum de series temporales a 3-12 meses (rupturas de máximos de largo plazo y "
            "pendiente de medias largas) es una de las anomalías más documentadas; se captura con "
            "pocas operaciones, stops amplios y sin objetivo fijo.",
      instrumento="Índices (US500/US30/DAX), oro, y pares con tendencia macro. Necesita ≥15-20 años de "
                  "datos: con 2013-2024 el número de operaciones es insuficiente (ver Fase 2).",
      build_dates=BUILD_STD, valid=None, slippage="0.5",
      slippage_why="D1 entra a la apertura del día (a menudo tras gap): 0,5 pips conservador.",
      options={
          "LimitTimeRange": ("false", "Con velas D1 (apertura 00:00) la ventana 01:30-23:30 del original "
                                      "podría bloquear todas las señales."),
          "MaxTradesPerDay": ("1", "Position: una entrada como máximo."),
          "MaxDistanceFromMarket": ("true", "Tope de distancia para stops."),
          "MaxDistancePct": ("5", "5 %: rupturas de máximos de 20-250 días."),
          "ReservedBars": ("260", "≥ periodo máximo (250)."),
      },
      complexity=dict(entry=(1, 2), exit_cond=(1, 1), exit_types=(1, 3), period=(20, 250), shift=(1, 1)),
      complexity_why="20-250 días (1 mes-1 año). Máximo 2 condiciones: con ~8 operaciones/año cada "
                     "grado de libertad extra es sobreajuste casi seguro.",
      signals={"BarOpensAboveHighestAfterOpenBelow": 3, "MARising": 2, "MABarClosesAbove": 2,
               "MACDMainHigherZero": 1, "MACDMainCrossAboveZero": 1, "ROCAboveLevel": 2, "ROCRising": 1,
               "ADXHigher": 1, "SuperTrendUPTrend": 1, "KAMARising": 1, "IchimokuKumoBreakoutBullish": 1,
               "LinRegRising": 1},
      indicators={"Indicators.Highest": 2, "Indicators.Lowest": 1, "Indicators.SMA": 2, "Indicators.EMA": 1,
                  "Indicators.ATR": 1, "Prices.Close": 1, "Prices.High": 1, "Prices.Low": 1,
                  "Prices.HighW": 1, "Prices.LowW": 1, "Prices.CloseW": 1, "Prices.HighM": 1, "Prices.LowM": 1,
                  **{k: 1 for k in CMP}},
      stoplimit={"Stop/Limit Price Levels.Highest": 2, "Stop/Limit Price Levels.HighW": 1,
                 "Stop/Limit Price Levels.HighM": 1, "Stop/Limit Price Levels.High": 1,
                 "Stop/Limit Price Ranges.ATR": 1},
      block_params={"ROCAboveLevel": {"Level": (0, 15, 1)}, "ADXHigher": {"Level": (20, 40, 5)}},
      block_why="Momentum sin niveles absolutos (ROC en %, MACD vs 0, medias, máximos de 20-250 días). "
                "Se eliminan osciladores: no aportan nada a un horizonte de meses.",
      orders={"EnterAtMarket": (True, 2), "EnterAtStop": (True, 1), "EnterAtLimit": (False, 1)},
      bars_valid=(1, 5), orders_why="Mayoritariamente a mercado; stop opcional válido 1-5 días.",
      sltp=dict(sl=(2.5, 6.0, 20, 100), pt=(6.0, 12.0, 20, 100), pt_required=False, rrr=None),
      exits=dict(pt=(False, 30), trailing=(True, 70, 3.0, 6.0), be=None, eab=(True, 30, 60, 250), rule=(True, 50)),
      exits_why="Sin objetivo (dejar correr); trailing de 3-6 ATR como salida principal; salida por "
                "regla (p. ej. cierre bajo media) y temporal 3-12 meses.",
      edge_eab=(20, 120), edge_why="Test de ventaja: salida por tiempo 1-6 meses.",
      fitness={"ReturnDDRatio": 2, "Stability": 1},
      fitness_why="Ret/DD + estabilidad; SQN es poco fiable con <100 operaciones.",
      edge_fitness={"ProfitFactor": 2, "StagnationPct": 1},
      filt=dict(trades=40, retdd=3, win=30, pf=1.5, avgbars=5, oos_pf=None),
      genetic=dict(pop=50, gens=30, islands=4),
      risk=100,
      retest=dict(precision=2, mc_sims=500, spread=(2, 4), slip=(0, 1), start_bar=True, spp_tests=8000,
                  spp_dist=30, spp_profit=90, whatif="top2", dd_max=25, mc_dd_pct=175),
      retest_why="SPP ±30 %: con periodos largos la superficie debe ser lisa; exigencia 90 %.",
      riesgos="Muestra pequeña; dependencia de pocas operaciones grandes; swap acumulado; "
              "cambio de régimen macro.",
      ),
    # =====================================================================================
    S("TrendFollowing", "Seguimiento de tendencia (multi-filtro con trailing)", "H4",
      tesis="Las tendencias persisten más de lo que predice un paseo aleatorio (reacción lenta a la "
            "información, flujos institucionales). Se entra cuando varios filtros de tendencia coinciden "
            "y se sale por trailing: pocas ganancias grandes pagan muchas pérdidas pequeñas.",
      instrumento="Cesta diversificada (índices, metales, JPY-cruces). En un solo símbolo el resultado "
                  "depende de 2-3 tendencias: validar en varios mercados.",
      build_dates=BUILD_STD, valid=VALID_STD, slippage="0.3",
      slippage_why="El original usa 0.",
      options={
          "LimitTimeRange": ("false", "Igual que Swing: en H4 la ventana del original sesga señales."),
          "MaxTradesPerDay": ("1", "Una entrada diaria como máximo."),
          "MaxDistanceFromMarket": ("true", "Tope para órdenes stop."),
          "MaxDistancePct": ("3", "3 %: rupturas de canales largos."),
          "ReservedBars": ("220", "≥ periodo máximo (200)."),
      },
      complexity=dict(entry=(1, 3), exit_cond=(1, 2), exit_types=(2, 4), period=(10, 200), shift=(1, 1)),
      complexity_why="10-200 velas H4 = 2-33 días.",
      signals={"SuperTrendUPTrend": 2, "BarClosesAboveSuperTrend": 2, "IchimokuKumoBreakoutBullish": 1,
               "IchimokuTenkanKijunCrossBullish": 1, "ADXHigher": 2, "ADXRising": 1, "DICrossUp": 1,
               "MACDMainCrossAboveSignal": 1, "MACDMainHigherZero": 1, "MARising": 1, "MABarClosesAbove": 1,
               "FasterHMAIsAboveSlowerHMA": 1, "FastKAMAAboveSlowKAMA": 1, "AroonCrossesAbove": 1,
               "VortexUptrend": 1, "GannHiLoUPTrend": 1, "PSARBarLower": 1,
               "BarOpensAboveHighestAfterOpenBelow": 2, "KERaboveLevel": 1},
      indicators={"Indicators.SMA": 1, "Indicators.EMA": 1, "Indicators.Highest": 2, "Indicators.Lowest": 1,
                  "Indicators.ATR": 1, "Indicators.SuperTrend": 1, "Indicators.KAMA": 1,
                  "Indicators.HullMovingAverage": 1, "Prices.Close": 1, "Prices.High": 1, "Prices.Low": 1,
                  **{k: 1 for k in CMP}},
      stoplimit={"Stop/Limit Price Levels.Highest": 2, "Stop/Limit Price Levels.SuperTrend": 1,
                 "Stop/Limit Price Levels.KeltnerChannel": 1, "Stop/Limit Price Levels.High": 1,
                 "Stop/Limit Price Ranges.ATR": 1},
      block_params={"ADXHigher": {"Level": (20, 40, 5)}, "KERaboveLevel": {"Level": (0.3, 0.7, 0.05)},
                    "SuperTrendUPTrend": {"ATR Mult": (1.5, 5, 0.5)},
                    "BarClosesAboveSuperTrend": {"ATR Mult": (1.5, 5, 0.5)},
                    "Indicators.SuperTrend": {"ATR Mult": (1.5, 5, 0.5)},
                    "Stop/Limit Price Levels.SuperTrend": {"ATR Mult": (1.5, 5, 0.5)}},
      block_why="Sólo filtros de dirección/fuerza de tendencia; sin osciladores de sobrecompra/sobreventa "
                "(contradicen la tesis).",
      orders={"EnterAtMarket": (True, 2), "EnterAtStop": (True, 1), "EnterAtLimit": (False, 1)},
      bars_valid=(1, 4), orders_why="A mercado con confirmación o stop sobre máximo reciente.",
      sltp=dict(sl=(2.0, 4.0, 14, 100), pt=(4.0, 10.0, 14, 100), pt_required=False, rrr=None),
      exits=dict(pt=(True, 30), trailing=(True, 80, 2.5, 5.0), be=None, eab=None, rule=(True, 50)),
      exits_why="El trailing (prob. 80 %) es la salida natural; objetivo raro y lejano.",
      edge_eab=(12, 60), edge_why="Test de ventaja: salida por tiempo 2-10 días.",
      fitness={"ReturnDDRatio": 2, "StagnationPct": 1},
      fitness_why="El talón de Aquiles del TF son las rachas planas largas: StagnationPct las penaliza.",
      edge_fitness={"SQN": 2, "StagnationPct": 1},
      filt=dict(trades=100, retdd=3.5, win=30, pf=1.4, avgbars=5, oos_pf=1.05),
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
            "la media se corrigen: se compra el exceso bajista y se sale en la media con objetivo corto.",
      instrumento="EURCHF, EURGBP, AUDNZD, USDCAD en sesión asiática o índices en rango. GBPJPY es "
                  "tendencial y mal candidato: usar sólo como prueba.",
      build_dates=BUILD_STD, valid=VALID_STD, slippage="0.3",
      slippage_why="El original usa 0.",
      options={
          "LimitTimeRange": ("true", "Ventana de baja direccionalidad."),
          "SignalTimeRangeFrom": (SECONDS("01:30"), "Igual que el original: evita rollover."),
          "SignalTimeRangeTo": (SECONDS("09:30"), "Sesión asiática: menor drift direccional en FX."),
          "MaxTradesPerDay": ("2", "Evita promediar a la baja en tendencia."),
          "MaxDistanceFromMarket": ("true", "Las órdenes límite lejanas casi nunca se ejecutan."),
          "MaxDistancePct": ("1", "1 %."),
          "ReservedBars": ("80", "≥ periodo máximo (60)."),
      },
      complexity=dict(entry=(1, 3), exit_cond=(1, 2), exit_types=(2, 4), period=(5, 60), shift=(1, 1)),
      complexity_why="5-60 velas H1: la reversión a la media es un fenómeno de corto plazo.",
      signals={"BBBarOpensAboveDownAfterOpenBelow": 2, "BBBarClosesBelowDown": 1,
               "KCBarOpensAboveLowerAfterOpenBelow": 2, "KCBarClosesBelowLower": 1, "RSICrossUp": 1,
               "RSILower": 1, "StochSlowDCrossUp": 1, "StochFastKCrossUp": 1, "WPRCrossUp": 1, "CCICrossUp": 1,
               "LaguerreRSICrossUP": 1, "DEMCrossUp": 1, "ADXLower": 2, "ADXFalling": 1, "KERbelowLevel": 2,
               "BarOpensAboveLowestAfterOpenBelow": 1},
      indicators={"Indicators.BollingerBands": 1, "Indicators.KeltnerChannel": 1, "Indicators.SMA": 1,
                  "Indicators.EMA": 1, "Indicators.Lowest": 1, "Indicators.Highest": 1, "Indicators.RSI": 1,
                  "Indicators.Stochastic": 1, "Indicators.WilliamsPR": 1, "Indicators.CCI": 1,
                  "Prices.Close": 1, "Prices.Low": 1, "Prices.Open": 1, **{k: 1 for k in CMP}, "IsLowerCount": 1},
      stoplimit={"Stop/Limit Price Levels.BollingerBands": 2, "Stop/Limit Price Levels.KeltnerChannel": 2,
                 "Stop/Limit Price Levels.Lowest": 1, "Stop/Limit Price Levels.Low": 1,
                 "Stop/Limit Price Levels.SMA": 1, "Stop/Limit Price Levels.EMA": 1,
                 "Stop/Limit Price Ranges.ATR": 2, "Stop/Limit Price Ranges.BarRange": 1,
                 "Stop/Limit Price Ranges.BBRange": 1},
      block_params={"RSICrossUp": {"Level": (15, 40, 5)}, "RSILower": {"Level": (20, 40, 5)},
                    "StochSlowDCrossUp": {"Level": (10, 30, 5)}, "StochFastKCrossUp": {"Level": (10, 30, 5)},
                    "WPRCrossUp": {"Level": (-95, -75, 5)}, "CCICrossUp": {"Level": (-150, -80, 5)},
                    "LaguerreRSICrossUP": {"Level": (0.05, 0.3, 0.05)}, "DEMCrossUp": {"Level": (0.1, 0.3, 0.1)},
                    "ADXLower": {"Level": (15, 30, 5)}, "KERbelowLevel": {"Level": (0.1, 0.4, 0.05)}},
      block_why="Osciladores sólo en zona de sobreventa (sus rangos 0-100 originales permitían 'comprar "
                "en sobrecompra'); filtros de régimen lateral (ADX bajo, KER bajo).",
      orders={"EnterAtLimit": (True, 2), "EnterAtMarket": (True, 1), "EnterAtStop": (False, 1)},
      bars_valid=(1, 5), orders_why="Límite bajo la banda/mínimo: se compra el exceso, no la ruptura.",
      sltp=dict(sl=(1.5, 3.0, 14, 60), pt=(0.8, 2.0, 14, 60), pt_required=True, rrr=(40, 120)),
      exits=dict(pt=(True, 100), trailing=None, be=None, eab=(True, 50, 5, 30), rule=(True, 50)),
      exits_why="Objetivo corto obligatorio (PT 40-120 % del SL) y alta tasa de acierto; salida "
                "temporal: si no revierte en 5-30 h la tesis falló.",
      edge_eab=(3, 24), edge_why="Test de ventaja: salida por tiempo 3-24 h.",
      fitness={"ReturnDDRatio": 2, "ProfitFactor": 1},
      fitness_why="PF alto es imprescindible en reversión (pérdidas medias > ganancias medias).",
      edge_fitness={"SQN": 2, "StagnationPct": 1},
      filt=dict(trades=250, retdd=4, win=55, pf=1.25, avgbars=2, oos_pf=1.1),
      genetic=dict(pop=40, gens=40, islands=4),
      risk=75,
      retest=dict(precision=2, mc_sims=500, spread=(2, 4), slip=(0, 0.5), start_bar=False, spp_tests=5000,
                  spp_dist=20, spp_profit=85, whatif="pct5", dd_max=20, mc_dd_pct=150),
      retest_why="What-if excluye el 5 % de mejores y peores: una reversión sana no depende de outliers.",
      riesgos="Pérdida grande cuando el rango se rompe (cola izquierda); el SL es imprescindible.",
      ),
    # =====================================================================================
    S("PriceAction", "Acción del precio (patrones de vela en niveles)", "H1",
      tesis="Patrones de rechazo/absorción (envolvente, martillo, pauta penetrante, fractal) en niveles "
            "relevantes (mínimos recientes, máximo/mínimo del día anterior) señalan desequilibrios de "
            "órdenes; se entra con stop sobre el máximo de la vela señal.",
      instrumento="Cualquier mercado líquido; mejor en índices y mayores. GBPJPY apto.",
      build_dates=BUILD_STD, valid=VALID_STD, slippage="0.3",
      slippage_why="El original usa 0.",
      options={
          "MaxTradesPerDay": ("2", "Evita encadenar señales en el mismo nivel."),
          "MaxDistanceFromMarket": ("true", "Tope para stops."),
          "MaxDistancePct": ("1", "1 %."),
          "ReservedBars": ("60", "≥ periodo máximo (50)."),
      },
      complexity=dict(entry=(1, 3), exit_cond=(1, 2), exit_types=(2, 4), period=(2, 50), shift=(1, 3)),
      complexity_why="Periodos 2-50 (estructura reciente); desplazamiento 1-3 para patrones de 2-3 velas.",
      signals={"BullishEngulfing": 2, "Hammer": 2, "PiercingLine": 2, "Doji": 1, "IsBullishFractal": 1,
               "BarOpensAboveHighestAfterOpenBelow": 1, "BarOpensAboveLowestAfterOpenBelow": 2},
      indicators={**{k: 2 for k in PRICES_BAR}, **{k: 1 for k in PRICES_D}, "Prices.HighW": 1, "Prices.LowW": 1,
                  "Prices.HeikenAshiOpen": 1, "Prices.HeikenAshiClose": 1, "Prices.HeikenAshiHigh": 1,
                  "Prices.HeikenAshiLow": 1, "Prices.SessionHigh": 1, "Prices.SessionLow": 1,
                  "Indicators.Highest": 1, "Indicators.Lowest": 1, "Indicators.Fractal": 1,
                  "Indicators.TrueRange": 1, "Indicators.ATR": 1, **{k: 1 for k in CMP},
                  "IsGreaterCount": 1, "IsLowerCount": 1, "IsRising": 1, "IsFalling": 1},
      stoplimit={"Stop/Limit Price Levels.High": 3, "Stop/Limit Price Levels.Low": 1,
                 "Stop/Limit Price Levels.Highest": 1, "Stop/Limit Price Levels.HighD": 1,
                 "Stop/Limit Price Levels.OpenD": 1, "Stop/Limit Price Levels.Fractal": 1,
                 "Stop/Limit Price Ranges.BarRange": 2, "Stop/Limit Price Ranges.ATR": 1,
                 "Stop/Limit Price Ranges.SmallestRange": 1},
      block_params={"Prices.SessionHigh": SESSION_ASIA, "Prices.SessionLow": SESSION_ASIA},
      block_why="Sólo precio, velas y estructura; ATR únicamente como normalizador. Se excluyen patrones "
                "bajistas (el original los usaba como entrada larga, incoherente).",
      orders={"EnterAtStop": (True, 2), "EnterAtLimit": (True, 1), "EnterAtMarket": (True, 1)},
      bars_valid=(1, 3), orders_why="Stop sobre el máximo de la vela señal (confirmación) o límite en retroceso.",
      sltp=dict(sl=(1.0, 2.5, 14, 50), pt=(1.5, 4.0, 14, 50), pt_required=True, rrr=(150, 300)),
      exits=dict(pt=(True, 100), trailing=None, be=(True, 50, 1.0, 2.0), eab=(True, 30, 5, 30), rule=(True, 30)),
      exits_why="R:R 1,5-3 sobre el riesgo de la vela; break-even tras 1-2 ATR.",
      edge_eab=(3, 24), edge_why="Test de ventaja: salida por tiempo 3-24 h.",
      fitness={"ReturnDDRatio": 2, "SQN": 1},
      fitness_why="Ret/DD + SQN (consistencia por operación).",
      edge_fitness={"SQN": 2, "StagnationPct": 1},
      filt=dict(trades=200, retdd=4, win=40, pf=1.3, avgbars=2, oos_pf=1.1),
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
      signals={"BarHourIs": 2, "BarDayOfWeekIs": 1, "ATRRising": 2, "ATRChangesUp": 1, "StdDevRising": 1,
               "BarOpensAboveHighestAfterOpenBelow": 2, "BBBarOpensAboveUpAfterOpenBelow": 1,
               "KCBarOpensAboveUpperAfterOpenBelow": 1},
      indicators={"Indicators.HighestInRange": 3, "Indicators.LowestInRange": 1, "Indicators.Highest": 1,
                  "Indicators.Lowest": 1, "Indicators.ATR": 1, "Indicators.TrueRange": 1,
                  **{k: 1 for k in PRICES_BAR}, **{k: 1 for k in CMP}},
      stoplimit={"Stop/Limit Price Levels.HighestInRange": 3, "Stop/Limit Price Levels.High": 1,
                 "Stop/Limit Price Levels.Highest": 1, "Stop/Limit Price Ranges.ATR": 2,
                 "Stop/Limit Price Ranges.TrueRange": 1, "Stop/Limit Price Ranges.BarRange": 1},
      block_params={"Indicators.HighestInRange": RANGE_PRE_US, "Indicators.LowestInRange": RANGE_PRE_US,
                    "Stop/Limit Price Levels.HighestInRange": RANGE_PRE_US, "BarHourIs": {"Hour": (15, 16, 1)}},
      block_why="Rango previo a la publicación (12:00-15:00 → 15:00/15:30) y filtros de hora/día; "
                "expansión de volatilidad como confirmación.",
      orders={"EnterAtStop": (True, 3), "EnterAtMarket": (True, 1), "EnterAtLimit": (False, 1)},
      bars_valid=(1, 4), orders_why="Stop sobre el rango pre-dato, caduca en 15-60 min.",
      sltp=dict(sl=(1.0, 2.0, 10, 40), pt=(1.5, 4.0, 10, 40), pt_required=False, rrr=None),
      exits=dict(pt=(True, 50), trailing=None, be=(True, 50, 0.5, 1.5), eab=(True, 70, 2, 16), rule=None),
      exits_why="El impulso de una noticia dura minutos/horas: salida temporal 30 min-4 h.",
      edge_eab=(2, 12), edge_why="Test de ventaja: salida por tiempo 30 min-3 h.",
      fitness={"ReturnDDRatio": 2, "ProfitFactor": 1},
      fitness_why="Pocas operaciones con mucha varianza: PF + Ret/DD.",
      edge_fitness={"SQN": 2, "StagnationPct": 1},
      filt=dict(trades=250, retdd=3, win=35, pf=1.3, avgbars=2, oos_pf=1.05),
      genetic=dict(pop=30, gens=30, islands=4),
      risk=50,
      retest=dict(precision=3, mc_sims=200, spread=(2, 8), slip=(0, 3), start_bar=False, spp_tests=1500,
                  spp_dist=20, spp_profit=80, whatif="pct5", dd_max=20, mc_dd_pct=150),
      retest_why="Spread aleatorio hasta 4x y deslizamiento hasta 3 pips: así es una publicación real.",
      riesgos="No distingue días con/sin noticia; horario DST; spreads y deslizamiento reales muy "
              "superiores a los de datos M1; requotes.",
      ),
]

STYLE_BY_NAME = {s["name"]: s for s in STYLES}
