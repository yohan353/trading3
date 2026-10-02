"""Familias de bloques (versión BUY), espejo BUY→SELL y rangos de niveles.

Cada estilo se compone de familias con un peso. El peso alto en la familia "núcleo" mantiene la tesis del estilo; las
familias auxiliares (peso 1) amplían la paleta de filtros, que es lo que permite al Builder encontrar más variedad y
más operaciones. Se excluyen de forma deliberada los bloques con niveles ABSOLUTOS dependientes de la escala de precio
(ATRHigher/Lower/Cross, StdDevHigher/Lower/Cross, MACDMainHigher/Lower/CrossAbove/Below con nivel, Mom/AWO/BEP/BUP con
nivel, BullsPower/BearsPower, FixedPips): en GBPJPY o US30 son siempre verdaderos o siempre falsos.

La versión SELL no se basa en que SQX "invierta" reglas: con *Market sides* = short y sin simetría, el Builder usa los
bloques tal cual, así que hay que activar los bloques bajistas equivalentes (espejo) y espejar sus niveles.
"""

from __future__ import annotations

# ------------------------------------------------------------------------------------------------- señales (BUY)
SIG = {
    "rup_canal": ["BarOpensAboveHighestAfterOpenBelow"],
    "rup_bandas": ["BBBarOpensAboveUpAfterOpenBelow", "BBBarClosesAboveUp", "BBBarOpensAboveUp",
                   "KCBarOpensAboveUpperAfterOpenBelow", "KCBarClosesAboveUpper", "KCBarOpensAboveUpper"],
    "rup_ichimoku": ["IchimokuKumoBreakoutBullish", "IchimokuKijunSenCrossBullish", "IchimokuSenkouSpanCrossBullish",
                     "IchimokuTenkanKijunCrossBullish"],
    "falsa_ruptura": ["BarOpensAboveLowestAfterOpenBelow"],
    "vol_expansion": ["ATRRising", "ATRChangesUp", "StdDevRising", "StdDevChangesUp", "BBUpperRising", "BBLowerFalling",
                      "KCUpperRising", "KCLowerFalling"],
    "vol_contraccion": ["ATRFalling", "ATRChangesDown", "StdDevFalling", "StdDevChangesDown", "BBUpperFalling",
                        "BBLowerRising", "KCUpperFalling", "KCLowerRising"],
    "vol_tick": ["VolumeRising", "AvgVolumeRising"],
    "mom_direccion": ["RSIRising", "RSIChangesUp", "LaguerreRSIRising", "LaguerreRSIChangesUP", "StochSlowDRising",
                      "StochSlowDChangesUp", "StochFastKUp", "MomRising", "MomChangesUp", "MACDMainRising",
                      "MACDMainChangesUp", "MACDMainCrossAboveSignal", "MACDMainHigherSignal", "MACDSignalRising",
                      "OSMARising", "OSMAChangesUp", "AWORising", "AWOChangesUp", "QQEValue1Rising",
                      "QQEValue1CrossAboveValue2", "QQEValue1HigherValue2", "QQEValue2Rising", "ReflexRising",
                      "ReflexChangesDirectionUP", "FastReflexCrossUPSlowReflex", "ROCRising", "CCIRising",
                      "CCIChangesUp", "WPRRising", "WPRChangesUp", "DEMRising", "DEMChangesUp"],
    "mom_nivel": ["RSIHigher", "RSICrossUp", "LaguerreRSICrossUP", "StochSlowDHigher", "StochSlowDCrossUp", "CCIHigher",
                  "CCICrossUp", "WPRHigher", "WPRCrossUp", "QQEValue1Higher", "QQEValue1CrossAbove", "MACDMainHigherZero",
                  "MACDMainCrossAboveZero", "OSMAHigherZero", "OSMACrossZeroUp", "ROCAboveLevel", "ROCCrossesAboveLevel",
                  "SchaffTrendCycleAboveLevel", "SchaffTrendCycleCrossesAboveLevel"],
    "sobreventa": ["RSICrossUp", "RSILower", "StochSlowDCrossUp", "StochFastKCrossUp", "StochSlowDLower", "WPRCrossUp",
                   "WPRLower", "CCICrossUp", "CCILower", "LaguerreRSICrossUP", "DEMCrossUp", "DEMLower",
                   "QQEValue1CrossAbove", "QQEValue1Lower", "SchaffTrendCycleCrossesAboveLevel",
                   "SchaffTrendCycleBelowLevel"],
    "tend_medias": ["MARising", "MABarClosesAbove", "MABarOpensAbove", "MABarOpensAboveAfterOpenBelow", "LinRegRising",
                    "LinRegBarClosesAbove", "LinRegBarOpensAbove", "LinRegBarOpensAboveAfterOpenBelow", "HMARising",
                    "HMAChangesUP", "FasterHMAIsAboveSlowerHMA", "KAMARising", "FastKAMAAboveSlowKAMA",
                    "BarClosesAboveKAMA", "IsUptrend"],
    "tend_sistemas": ["SuperTrendUPTrend", "BarClosesAboveSuperTrend", "PSARBarLower", "VortexUptrend",
                      "VortexChangesTrendUP", "GannHiLoUPTrend", "AroonCrossesAbove", "WoodiesTrendUP",
                      "WoodiesCCIZeroLineBreakUP", "DIPlusRising", "DIPlusChangesUp", "DICrossUp", "DIPlusHigher",
                      "DIMinusFalling", "DIMinusChangesDown"],
    "fuerza": ["ADXRising", "ADXChangesUp", "ADXHigher", "ADXCrossUp", "KERaboveLevel"],
    "lateral": ["ADXLower", "ADXFalling", "ADXChangesDown", "ADXCrossDown", "KERbelowLevel", "SuperTrendInRange"],
    "rev_bandas": ["BBBarOpensAboveDownAfterOpenBelow", "BBBarClosesBelowDown", "BBBarOpensBelowDown",
                   "BBBarClosesAboveDown", "KCBarOpensAboveLowerAfterOpenBelow", "KCBarClosesBelowLower",
                   "KCBarOpensBelowLower", "KCBarClosesAboveLower"],
    "velas": ["BullishEngulfing", "Hammer", "PiercingLine", "Doji", "IsBullishFractal"],
    "tiempo_intradia": ["BarHourIs", "BarHourIsBigger", "BarHourIsSmaller", "BarDayOfWeekIs", "BarDayOfWeekIsNot"],
    "tiempo_calendario": ["BarDayOfWeekIs", "BarDayOfWeekIsNot", "BarMonthIs", "BarMonthIsNot",
                          "IsMonthFirstTradingDay", "IsMonthLastTradingDay"],
}

# ------------------------------------------------------------------------------------------------- indicadores
IND = {
    "niv_canal": ["Indicators.Highest", "Indicators.Lowest"],
    "niv_horario": ["Indicators.HighestInRange", "Indicators.LowestInRange", "Prices.SessionHigh", "Prices.SessionLow",
                    "Prices.SessionOpen", "Prices.SessionClose"],
    "niv_diario": ["Prices.HighD", "Prices.LowD", "Prices.OpenD", "Prices.CloseD"],
    "niv_semanal": ["Prices.HighW", "Prices.LowW", "Prices.OpenW", "Prices.CloseW"],
    "niv_mensual": ["Prices.HighM", "Prices.LowM", "Prices.OpenM", "Prices.CloseM"],
    "precio": ["Prices.Close", "Prices.Open", "Prices.High", "Prices.Low"],
    "heiken": ["Prices.HeikenAshiOpen", "Prices.HeikenAshiClose", "Prices.HeikenAshiHigh", "Prices.HeikenAshiLow"],
    "medias": ["Indicators.SMA", "Indicators.EMA", "Indicators.LWMA", "Indicators.SMMA", "Indicators.TEMA",
               "Indicators.HullMovingAverage", "Indicators.KAMA", "Indicators.LinearRegression"],
    "bandas": ["Indicators.BollingerBands", "Indicators.KeltnerChannel"],
    "sistemas": ["Indicators.SuperTrend", "Indicators.ParabolicSAR", "Indicators.Ichimoku", "Indicators.GannHiLo"],
    "osciladores": ["Indicators.RSI", "Indicators.Stochastic", "Indicators.CCI", "Indicators.WilliamsPR",
                    "Indicators.LaguerreRSI", "Indicators.DeMarker"],
    "fuerza_ind": ["Indicators.ADX", "Indicators.KaufmanEfficiencyRatio", "Indicators.Aroon", "Indicators.Vortex"],
    "volat_ind": ["Indicators.ATR", "Indicators.TrueRange"],
    "estructura": ["Indicators.Fractal"],
    "comparadores": ["IsGreater", "IsLower", "IsGreaterOrEqual", "IsLowerOrEqual", "CrossesAbove", "CrossesBelow"],
    "secuencias": ["IsGreaterCount", "IsLowerCount", "IsRising", "IsFalling"],
}

# ------------------------------------------------------------------------------------------------- niveles stop/limit
_L = "Stop/Limit Price Levels."
_R = "Stop/Limit Price Ranges."
STL = {
    "stl_canal": [_L + "Highest", _L + "Lowest"],
    "stl_vela": [_L + "High", _L + "Low", _L + "Open", _L + "Close"],
    "stl_horario": [_L + "HighestInRange", _L + "LowestInRange", _L + "SessionHigh", _L + "SessionLow", _L + "SessionOpen"],
    "stl_diario": [_L + "HighD", _L + "LowD", _L + "OpenD", _L + "CloseD"],
    "stl_semanal": [_L + "HighW", _L + "LowW", _L + "OpenW"],
    "stl_mensual": [_L + "HighM", _L + "LowM"],
    "stl_bandas": [_L + "BollingerBands", _L + "KeltnerChannel", _L + "MTKeltnerChannel"],
    "stl_medias": [_L + "SMA", _L + "EMA", _L + "LWMA", _L + "SMMA", _L + "TEMA", _L + "HullMovingAverage", _L + "KAMA",
                   _L + "LinearRegression"],
    "stl_sistemas": [_L + "SuperTrend", _L + "ParabolicSAR", _L + "Ichimoku", _L + "GannHiLo"],
    "stl_estructura": [_L + "Fractal", _L + "Pivots"],
    "stl_heiken": [_L + "HeikenAshiOpen", _L + "HeikenAshiClose", _L + "HeikenAshiHigh", _L + "HeikenAshiLow"],
    "stl_rangos": [_R + "ATR", _R + "MTATR", _R + "BarRange", _R + "TrueRange", _R + "BiggestRange", _R + "SmallestRange",
                   _R + "BBRange", _R + "BBWidthRatio"],
}

# ------------------------------------------------------------------------------------------------- espejo BUY -> SELL
_PAIRS = [
    ("BarOpensAboveHighestAfterOpenBelow", "BarOpensBelowLowestAfterOpenAbove"),
    ("BarOpensAboveLowestAfterOpenBelow", "BarOpensBelowHighestAfterOpenAbove"),
    ("BBBarOpensAboveUpAfterOpenBelow", "BBBarOpensBelowDownAfterOpenAbove"),
    ("BBBarClosesAboveUp", "BBBarClosesBelowDown"),
    ("BBBarOpensAboveUp", "BBBarOpensBelowDown"),
    ("BBBarOpensAboveDownAfterOpenBelow", "BBBarOpensBelowUpAfterOpenAbove"),
    ("BBBarClosesAboveDown", "BBBarClosesBelowUp"),
    ("KCBarOpensAboveUpperAfterOpenBelow", "KCBarOpensBelowLowerAfterOpenAbove"),
    ("KCBarClosesAboveUpper", "KCBarClosesBelowLower"),
    ("KCBarOpensAboveUpper", "KCBarOpensBelowLower"),
    ("KCBarOpensAboveLowerAfterOpenBelow", "KCBarOpensBelowUpperAfterOpenAbove"),
    ("KCBarClosesAboveLower", "KCBarClosesBelowUpper"),
    ("IchimokuKumoBreakoutBullish", "IchimokuKumoBreakoutBearish"),
    ("IchimokuKijunSenCrossBullish", "IchimokuKijunSenCrossBearish"),
    ("IchimokuSenkouSpanCrossBullish", "IchimokuSenkouSpanCrossBearish"),
    ("IchimokuTenkanKijunCrossBullish", "IchimokuTenkanKijunCrossBearish"),
    ("RSIRising", "RSIFalling"), ("RSIChangesUp", "RSIChangesDown"), ("RSIHigher", "RSILower"),
    ("RSICrossUp", "RSICrossDown"),
    ("LaguerreRSIRising", "LaguerreRSIFalling"), ("LaguerreRSIChangesUP", "LaguerreRSIChangesDown"),
    ("LaguerreRSICrossUP", "LaguerreRSICrossDown"),
    ("StochSlowDRising", "StochSlowDFalling"), ("StochSlowDChangesUp", "StochSlowDChangesDown"),
    ("StochSlowDHigher", "StochSlowDLower"), ("StochSlowDCrossUp", "StochSlowDCrossDown"),
    ("StochFastKUp", "StochFastKDown"), ("StochFastKCrossUp", "StochFastKCrossDown"),
    ("MomRising", "MomFalling"), ("MomChangesUp", "MomChangesDown"),
    ("MACDMainRising", "MACDMainFalling"), ("MACDMainChangesUp", "MACDMainChangesDown"),
    ("MACDMainCrossAboveSignal", "MACDMainCrossBelowSignal"), ("MACDMainHigherSignal", "MACDMainLowerSignal"),
    ("MACDSignalRising", "MACDSignalFalling"), ("MACDMainHigherZero", "MACDMainLowerZero"),
    ("MACDMainCrossAboveZero", "MACDMainCrossBelowZero"),
    ("OSMARising", "OSMAFalling"), ("OSMAChangesUp", "OSMAChangesDown"), ("OSMAHigherZero", "OSMALowerZero"),
    ("OSMACrossZeroUp", "OSMACrossZeroDown"),
    ("AWORising", "AWOFalling"), ("AWOChangesUp", "AWOChangesDown"),
    ("QQEValue1Rising", "QQEValue1Falling"), ("QQEValue1CrossAboveValue2", "QQEValue1CrossBelowValue2"),
    ("QQEValue1HigherValue2", "QQEValue1LowerValue2"), ("QQEValue2Rising", "QQEValue2Falling"),
    ("QQEValue1Higher", "QQEValue1Lower"), ("QQEValue1CrossAbove", "QQEValue1CrossBelow"),
    ("ReflexRising", "ReflexFalling"), ("ReflexChangesDirectionUP", "ReflexChangesDirectionDown"),
    ("FastReflexCrossUPSlowReflex", "FastReflexCrossDownSlowReflex"),
    ("ROCRising", "ROCFalling"), ("ROCAboveLevel", "ROCBelowLevel"), ("ROCCrossesAboveLevel", "ROCCrossesBelowLevel"),
    ("CCIRising", "CCIFalling"), ("CCIChangesUp", "CCIChangesDown"), ("CCIHigher", "CCILower"),
    ("CCICrossUp", "CCICrossDown"),
    ("WPRRising", "WPRFalling"), ("WPRChangesUp", "WPRChangesDown"), ("WPRHigher", "WPRLower"),
    ("WPRCrossUp", "WPRCrossDown"),
    ("DEMRising", "DEMFalling"), ("DEMChangesUp", "DEMChangesDown"), ("DEMHigher", "DEMLower"),
    ("DEMCrossUp", "DEMCrossDown"),
    ("SchaffTrendCycleAboveLevel", "SchaffTrendCycleBelowLevel"),
    ("SchaffTrendCycleCrossesAboveLevel", "SchaffTrendCycleCrossesBelowLevel"),
    ("MARising", "MAFalling"), ("MABarClosesAbove", "MABarClosesBelow"), ("MABarOpensAbove", "MABarOpensBelow"),
    ("MABarOpensAboveAfterOpenBelow", "MABarOpensBelowAfterOpenAbove"),
    ("LinRegRising", "LinRegFalling"), ("LinRegBarClosesAbove", "LinRegBarClosesBelow"),
    ("LinRegBarOpensAbove", "LinRegBarOpensBelow"),
    ("LinRegBarOpensAboveAfterOpenBelow", "LinRegBarOpensBelowAfterOpenAbove"),
    ("HMARising", "HMAFalling"), ("HMAChangesUP", "HMAChangesDown"),
    ("FasterHMAIsAboveSlowerHMA", "FasterHMAIsBelowSlowerHMA"),
    ("KAMARising", "KAMAFalling"), ("FastKAMAAboveSlowKAMA", "FastKAMABelowSlowKAMA"),
    ("BarClosesAboveKAMA", "BarClosesBelowKAMA"), ("IsUptrend", "IsDowntrend"),
    ("SuperTrendUPTrend", "SuperTrendDownTrend"), ("BarClosesAboveSuperTrend", "BarClosesBelowSuperTrend"),
    ("PSARBarLower", "PSARBarHigher"), ("VortexUptrend", "VortexDowntrend"),
    ("VortexChangesTrendUP", "VortexChangesTrendDown"), ("GannHiLoUPTrend", "GannHiLoDownTrend"),
    ("AroonCrossesAbove", "AroonCrossesBelow"), ("WoodiesTrendUP", "WoodiesTrendDown"),
    ("WoodiesCCIZeroLineBreakUP", "WoodiesCCIZeroLineBreakDown"),
    ("DIPlusRising", "DIMinusRising"), ("DIPlusChangesUp", "DIMinusChangesUp"), ("DICrossUp", "DICrossDown"),
    ("DIPlusHigher", "DIPlusLower"), ("DIMinusFalling", "DIPlusFalling"), ("DIMinusChangesDown", "DIPlusChangesDown"),
    ("BullishEngulfing", "BearishEngulfing"), ("Hammer", "ShootingStar"), ("PiercingLine", "DarkCloud"),
    ("IsBullishFractal", "IsBearishFractal"),
    # indicadores / niveles: se intercambian (si ambos están, se intercambian los pesos)
    ("Indicators.Highest", "Indicators.Lowest"), ("Indicators.HighestInRange", "Indicators.LowestInRange"),
    ("Prices.SessionHigh", "Prices.SessionLow"), ("Prices.HighD", "Prices.LowD"), ("Prices.HighW", "Prices.LowW"),
    ("Prices.HighM", "Prices.LowM"), ("Prices.High", "Prices.Low"), ("Prices.HeikenAshiHigh", "Prices.HeikenAshiLow"),
    ("IsGreater", "IsLower"), ("IsGreaterOrEqual", "IsLowerOrEqual"), ("CrossesAbove", "CrossesBelow"),
    ("IsGreaterCount", "IsLowerCount"), ("IsRising", "IsFalling"),
    (_L + "Highest", _L + "Lowest"), (_L + "High", _L + "Low"), (_L + "HighestInRange", _L + "LowestInRange"),
    (_L + "SessionHigh", _L + "SessionLow"), (_L + "HighD", _L + "LowD"), (_L + "HighW", _L + "LowW"),
    (_L + "HighM", _L + "LowM"), (_L + "HeikenAshiHigh", _L + "HeikenAshiLow"),
]
MIRROR: dict[str, str] = {}
for a, b in _PAIRS:
    MIRROR[a], MIRROR[b] = b, a


def mirror_key(k: str) -> str:
    return MIRROR.get(k, k)


# Espejo de niveles de osciladores: rango (a, b) en BUY -> rango equivalente en SELL
def _mirror_range(prefix_fn, a, b):
    x, y = prefix_fn(a), prefix_fn(b)
    return (min(x, y), max(x, y))


def mirror_param(key_buy: str, pname: str, rng: tuple):
    a, b, step = rng
    if pname != "Level":
        return rng
    k = key_buy
    if k.startswith(("RSI", "Stoch", "QQE", "Schaff")):
        f = lambda v: round(100 - v, 6)
    elif k.startswith("WPR"):
        f = lambda v: round(-100 - v, 6)
    elif k.startswith(("CCI", "ROC")):
        f = lambda v: round(-v, 6)
    elif k.startswith(("LaguerreRSI", "DEM")):
        f = lambda v: round(1 - v, 6)
    else:  # ADX, KER… son neutrales
        return rng
    lo, hi = _mirror_range(f, a, b)
    return (lo, hi, step)


# ------------------------------------------------------------------------------------------------- rangos (BUY)
# Zona de momentum (continuación) y zona de sobreventa (reversión); niveles de régimen.
P_MOMENTUM = {
    "RSIHigher": {"Level": (50, 70, 5)}, "RSICrossUp": {"Level": (50, 70, 5)},
    "LaguerreRSICrossUP": {"Gamma": (0.3, 0.8, 0.05), "Level": (0.4, 0.85, 0.05)},
    "StochSlowDHigher": {"Level": (50, 80, 5)}, "StochSlowDCrossUp": {"Level": (50, 80, 5)},
    "CCIHigher": {"Level": (0, 150, 10)}, "CCICrossUp": {"Level": (0, 150, 10)},
    "WPRHigher": {"Level": (-50, -20, 5)}, "WPRCrossUp": {"Level": (-50, -20, 5)},
    "QQEValue1Higher": {"Level": (50, 70, 5)}, "QQEValue1CrossAbove": {"Level": (50, 70, 5)},
    "SchaffTrendCycleAboveLevel": {"Level": (50, 90, 5)},
    "SchaffTrendCycleCrossesAboveLevel": {"Level": (25, 75, 5)},
}
P_SOBREVENTA = {
    "RSICrossUp": {"Level": (15, 40, 5)}, "RSILower": {"Level": (20, 40, 5)},
    "StochSlowDCrossUp": {"Level": (10, 30, 5)}, "StochFastKCrossUp": {"Level": (10, 30, 5)},
    "StochSlowDLower": {"Level": (10, 30, 5)},
    "WPRCrossUp": {"Level": (-95, -75, 5)}, "WPRLower": {"Level": (-95, -75, 5)},
    "CCICrossUp": {"Level": (-200, -80, 10)}, "CCILower": {"Level": (-200, -80, 10)},
    "LaguerreRSICrossUP": {"Gamma": (0.3, 0.8, 0.05), "Level": (0.05, 0.3, 0.05)},
    "DEMCrossUp": {"Level": (0.1, 0.3, 0.05)}, "DEMLower": {"Level": (0.1, 0.3, 0.05)},
    "QQEValue1CrossAbove": {"Level": (20, 40, 5)}, "QQEValue1Lower": {"Level": (20, 40, 5)},
    "SchaffTrendCycleCrossesAboveLevel": {"Level": (5, 25, 5)}, "SchaffTrendCycleBelowLevel": {"Level": (5, 25, 5)},
}
P_FUERZA = {"ADXHigher": {"Level": (20, 40, 5)}, "ADXCrossUp": {"Level": (20, 35, 5)},
            "KERaboveLevel": {"Level": (0.3, 0.7, 0.05)}}
P_LATERAL = {"ADXLower": {"Level": (15, 30, 5)}, "ADXCrossDown": {"Level": (20, 30, 5)},
             "KERbelowLevel": {"Level": (0.1, 0.4, 0.05)}}
P_SUPERTREND = {k: {"ATR Mult": (1.5, 5, 0.5)} for k in ("SuperTrendUPTrend", "BarClosesAboveSuperTrend",
                                                          "SuperTrendInRange", "Indicators.SuperTrend",
                                                          _L + "SuperTrend")}


def roc_params(lo, hi, step):
    return {"ROCAboveLevel": {"Level": (lo, hi, step)}, "ROCCrossesAboveLevel": {"Level": (lo, hi, step)}}


def ventana(rango_desde, rango_hasta, sesion_ini, sesion_fin, horas):
    """Parámetros horarios: rango HighestInRange (HHMM, horas enteras), sesiones y filtros de hora."""
    rng = {"Time From": rango_desde, "Time To": rango_hasta}
    ses = {"Start Hours": sesion_ini, "Start Minutes": (0, 0, 1), "End Hours": sesion_fin, "End Minutes": (0, 0, 1)}
    out = {k: rng for k in ("Indicators.HighestInRange", "Indicators.LowestInRange",
                            _L + "HighestInRange", _L + "LowestInRange")}
    out.update({k: ses for k in ("Prices.SessionHigh", "Prices.SessionLow", _L + "SessionHigh", _L + "SessionLow")})
    out["Prices.SessionOpen"] = out[_L + "SessionOpen"] = {"Start Hours": sesion_ini, "Start Minutes": (0, 0, 1)}
    out["Prices.SessionClose"] = {"End Hours": sesion_fin, "End Minutes": (0, 0, 1)}
    if horas:
        out.update(horas)
    return out


def compose(spec: dict, side: str):
    """spec = {'signals': [(familia, peso)], 'indicators': [...], 'stoplimit': [...], 'pesos': {clave: peso},
    'params': {clave: {param: (min,max,step)}}}. Devuelve (signals, indicators, stoplimit, params) para BUY o SELL."""
    out = []
    for cat, fams in (("signals", SIG), ("indicators", IND), ("stoplimit", STL)):
        d: dict[str, int] = {}
        for fam, w in spec[cat]:
            for k in fams[fam]:
                d[k] = max(d.get(k, 0), w)
        for k, w in spec.get("pesos", {}).items():
            if k in d:
                d[k] = w
        out.append(d)
    params = {k: v for k, v in spec.get("params", {}).items()
              if any(k in d for d in out)}
    if side == "SELL":
        out = [{mirror_key(k): w for k, w in d.items()} for d in out]
        params = {mirror_key(k): {p: mirror_param(k, p, r) for p, r in v.items()} for k, v in params.items()}
    return out[0], out[1], out[2], params


# ------------------------------------------------------------------------------------------------- descripciones
FAMILIA_DESC = {
    "rup_canal": "Apertura por encima del máximo de N velas tras abrir por debajo (ruptura Donchian confirmada).",
    "rup_bandas": "Apertura/cierre fuera de la banda superior de Bollinger o Keltner.",
    "rup_ichimoku": "Salida de la nube y cruces alcistas de Ichimoku.",
    "falsa_ruptura": "Recuperación por encima del mínimo de N velas tras perforarlo (trampa bajista).",
    "vol_expansion": "ATR/desviación típica/bandas abriéndose: entra volatilidad.",
    "vol_contraccion": "ATR/desviación típica/bandas cerrándose: compresión previa a un movimiento.",
    "vol_tick": "Volumen de ticks creciente (en FX es actividad, no volumen real).",
    "mom_direccion": "Osciladores y momentum girando o subiendo (RSI, estocástico, MACD, OSMA, QQE, Reflex, ROC, CCI, "
                     "WPR, DeMarker…), sin niveles absolutos.",
    "mom_nivel": "Osciladores en zona de fuerza (RSI 50-70, estocástico 50-80, CCI 0-150…) y MACD/OSMA/ROC por "
                 "encima de cero.",
    "sobreventa": "Osciladores en zona de sobreventa (RSI 15-40, estocástico 10-30, WPR -95…-75, CCI -200…-80…).",
    "tend_medias": "Pendiente y posición del precio respecto a medias (simple, Hull, KAMA, regresión lineal).",
    "tend_sistemas": "Sistemas de tendencia: SuperTrend, PSAR, Vortex, Gann HiLo, Aroon, DMI, Woodies.",
    "fuerza": "ADX creciente o alto y eficiencia de Kaufman alta: hay tendencia.",
    "lateral": "ADX bajo/decreciente, eficiencia de Kaufman baja, SuperTrend en rango: no hay tendencia.",
    "rev_bandas": "Exceso fuera de la banda inferior y reentrada (reversión a la media).",
    "velas": "Patrones de vela de giro alcista (envolvente, martillo, pauta penetrante, doji) y fractal.",
    "tiempo_intradia": "Hora y día de la semana de la vela.",
    "tiempo_calendario": "Día de la semana, mes y primer/último día de mes.",
    "niv_canal": "Máximo/mínimo de N velas.",
    "niv_horario": "Máximo/mínimo de un rango horario y de la sesión (apertura/cierre de sesión).",
    "niv_diario": "Máximo/mínimo/apertura/cierre del día.",
    "niv_semanal": "Máximo/mínimo/apertura/cierre de la semana.",
    "niv_mensual": "Máximo/mínimo/apertura/cierre del mes.",
    "precio": "Apertura, máximo, mínimo y cierre de la vela.",
    "heiken": "Velas Heikin-Ashi (precio suavizado).",
    "medias": "Medias móviles (SMA, EMA, LWMA, SMMA, TEMA, Hull, KAMA) y regresión lineal.",
    "bandas": "Bandas de Bollinger y canal de Keltner.",
    "sistemas": "SuperTrend, Parabolic SAR, Ichimoku y Gann HiLo como valores.",
    "osciladores": "RSI, estocástico, CCI, Williams %R, RSI de Laguerre y DeMarker como valores.",
    "fuerza_ind": "ADX, eficiencia de Kaufman, Aroon y Vortex como valores.",
    "volat_ind": "ATR y rango verdadero (para comparaciones relativas).",
    "estructura": "Fractales (máximos/mínimos locales).",
    "comparadores": "Mayor/menor, mayor o igual, cruces.",
    "secuencias": "N velas seguidas por encima/debajo, subiendo/bajando.",
    "stl_canal": "Orden en el máximo/mínimo de N velas.",
    "stl_vela": "Orden en el máximo/mínimo/apertura/cierre de una vela.",
    "stl_horario": "Orden en el extremo de un rango horario o de sesión.",
    "stl_diario": "Orden en niveles del día.",
    "stl_semanal": "Orden en niveles de la semana.",
    "stl_mensual": "Orden en niveles del mes.",
    "stl_bandas": "Orden en Bollinger/Keltner.",
    "stl_medias": "Orden en una media móvil.",
    "stl_sistemas": "Orden en SuperTrend, PSAR, Ichimoku o Gann HiLo.",
    "stl_estructura": "Orden en fractales o pivotes.",
    "stl_heiken": "Orden en niveles Heikin-Ashi.",
    "stl_rangos": "Desplazamiento de la orden: k·ATR, rango de vela, rango verdadero, mayor/menor rango, anchura de Bollinger.",
}
