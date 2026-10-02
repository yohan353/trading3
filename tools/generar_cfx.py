"""Genera las variantes por estilo de los 4 .cfx originales y sus tablas de cambios.

Uso:
    python tools/generar_cfx.py [--originales originales] [--salida configs] [--docs docs/cambios]

Los originales NO están en el repositorio (plantillas de un tercero). Copia en ``originales/``:
    Estrategia_Build_ConfigInicial_H1_BUY.cfx   Estrategia_Retest_ConfigInicial_H1_BUY.cfx
    Ventaja_Build_ConfigInicial_H1_BUY.cfx      Ventaja_Retest_ConfigInicial_H1_BUY.cfx
(se aceptan prefijos en el nombre, p. ej. "b00cf192-Estrategia_Build_...cfx").
"""

from __future__ import annotations

import argparse
import copy
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sqx_cfx import Patcher, load_cfx, save_cfx  # noqa: E402
from estilos import COMMON_WHY, SIDES, STYLES, min_trades  # noqa: E402
from familias import compose  # noqa: E402

ORIGINALS = {
    "EB": "Estrategia_Build_ConfigInicial_H1_BUY",
    "ER": "Estrategia_Retest_ConfigInicial_H1_BUY",
    "VB": "Ventaja_Build_ConfigInicial_H1_BUY",
    "VR": "Ventaja_Retest_ConfigInicial_H1_BUY",
}
KIND_LABEL = {"EB": "Builder de estrategia completa", "ER": "Retester de estrategia completa",
              "VB": "Builder de test de ventaja (entrada)", "VR": "Retester de test de ventaja"}


def cfx_name(base: str, st: dict, side: str) -> str:
    """<Original>__<Estilo>_<TF>_<BUY|SELL> (sin extensión)."""
    return f"{base}__{st['name']}_{st['tf']}_{side}"


def locate(dir_: Path, base: str) -> Path:
    hits = sorted(dir_.glob(f"*{base}.cfx"))
    if not hits:
        raise FileNotFoundError(f"No encuentro *{base}.cfx en {dir_}")
    return hits[0]


# =========================================================================== partes comunes
def patch_root(p: Patcher, new_name: str):
    p.set_attr(p.root, "templateFile", f"{new_name}.cfx", "Task", "Task@templateFile",
               "Ruta local del autor (C:\\Users\\<usuario>\\Desktop\\...) sustituida por el nombre del nuevo "
               "archivo: no aporta nada y expone el nombre de usuario de Windows.")


def patch_options(p: Patcher, st: dict):
    for key, (val, why) in st["options"].items():
        p.option(key, val, why)


def patch_setup(p: Patcher, setup: ET.Element, st: dict, dates=None, section="Data"):
    chart = setup.find("Chart")
    p.set_attr(chart, "timeframe", st["tf"], section, "Setup/Chart@timeframe",
               f"Timeframe del estilo {st['name']}.")
    p.set_attr(setup, "slippage", st["slippage"], section, "Setup@slippage", st["slippage_why"])
    if dates:
        p.set_attr(setup, "dateFrom", dates[0], section, "Setup@dateFrom", dates[2])
        p.set_attr(setup, "dateTo", dates[1], section, "Setup@dateTo", dates[2])


def patch_oos(p: Patcher, valid, why: str):
    oos = p.find("Settings/Data/OutOfSample")
    old = "; ".join(f"{r.get('dateFrom')}–{r.get('dateTo')}" for r in oos.findall("Range")) or "(sin OOS)"
    for r in list(oos.findall("Range")):
        oos.remove(r)
    if valid:
        ET.SubElement(oos, "Range", {"dateFrom": valid[0], "dateTo": valid[1]})
    p.mark_replaced(oos)
    new = "; ".join(f"{r.get('dateFrom')}–{r.get('dateTo')}" for r in oos.findall("Range")) or "(sin OOS)"
    p._log("Data", "OutOfSample/Range", old, new, why)


def patch_mm(p: Patcher, kind: str, st: dict):
    if kind in ("EB", "ER"):
        p.text("Settings/RiskMoneyManagement/MoneyManagement/Method[@type='FixedAmount']/Params/"
               "Param[@key='RiskedMoney']", st["risk"], "Money management",
               "FixedAmount · RiskedMoney",
               f"Riesgo fijo de {st['risk']} sobre 10.000 ({st['risk'] / 100:.2g} %). "
               + ("Estilos de alta frecuencia: 0,5 % para contener el drawdown en R."
                  if st["risk"] < 100 else "1 %, como el original."))


def patch_notes(p: Patcher, st: dict, kind: str, orig: str, side: str):
    note = (f"<b>{st['title']} – {KIND_LABEL[kind]} – {side}</b><div>Derivado de {orig} (build 140.2099). "
            f"Timeframe {st['tf']}. Ver docs/03 (ficha {st['name']}) y docs/04 (checklist).</div>"
            "<div>NO VALIDADO EN SQX: revisar símbolo, costes, horario del servidor e importación.</div>")
    p.text("Settings/Notes", note, "Notes", "Notes", "Descripción del estilo y advertencias.")


def fitness(p: Patcher, tpl: ET.Element, goals: dict, why: str):
    parent = p.find("Settings/Rankings/FitnessCriteria/Settings")
    p.weighted_fitness(parent, tpl, goals, "Ranking", why)


# =========================================================================== Builder
def patch_builder(p: Patcher, st: dict, kind: str, weighted_tpl: ET.Element, new_name: str, orig: str, side: str):
    E = kind == "EB"
    patch_root(p, new_name)
    patch_options(p, st)
    if side == "SELL":
        p.attr("Settings/WhatToBuild/MarketSides", "type", "short", "What to build", "MarketSides@type",
               "Kit SELL: sólo ventas. Sin simetría, SQX usa los bloques tal cual, por eso se activan los "
               "equivalentes bajistas (espejo) en Building blocks.")

    # --- What to build
    stype = p.find("Settings/WhatToBuild/StrategyType")
    if E:
        p.set_attr(stype, "type", "simple", "What to build", "StrategyType@type", COMMON_WHY["simple"])
        p.set_attr(stype, "templateFile", "SQ3StrategyTemplateExample.sq4", "What to build",
                   "StrategyType@templateFile", "Valor por defecto (el mismo que Ventaja_Build); en modo "
                   "'simple' no se usa.")
    ch = p.find("Settings/WhatToBuild/RulesComplexity/Chart")
    cx = st["complexity"]
    sec = "What to build · complejidad"
    p.set_attr(ch, "minConditions", cx["entry"][0], sec, "Chart@minConditions",
               "Entrada generada por el Builder." if E else "Igual que el original (1-3) salvo estilos de pocas operaciones.")
    p.set_attr(ch, "maxConditions", cx["entry"][1], sec, "Chart@maxConditions", st["complexity_why"])
    if E:
        p.set_attr(ch, "minExitConditions", cx["exit_cond"][0], sec, "Chart@minExitConditions",
                   "Condiciones de la regla de salida (sólo si _ExitRule_ está activo).")
        p.set_attr(ch, "maxExitConditions", cx["exit_cond"][1], sec, "Chart@maxExitConditions",
                   "Máximo 1-2: una salida por regla sencilla es más robusta.")
        p.set_attr(ch, "minExitTypes", cx["exit_types"][0], sec, "Chart@minExitTypes",
                   "Al menos SL + otra salida." if cx["exit_types"][0] > 1 else "SL obligatorio basta.")
        p.set_attr(ch, "maxExitTypes", cx["exit_types"][1], sec, "Chart@maxExitTypes",
                   "El original pedía hasta 5 con sólo 3 tipos activos.")
    else:
        p.set_attr(ch, "minExitTypes", 1, sec, "Chart@minExitTypes", "Test de ventaja: una única salida (tiempo).")
        p.set_attr(ch, "maxExitTypes", 1, sec, "Chart@maxExitTypes",
                   "Test de ventaja: sólo salida temporal, para medir la entrada aislada.")
    p.set_attr(ch, "minPeriod", cx["period"][0], sec, "Chart@minPeriod", st["complexity_why"])
    p.set_attr(ch, "maxPeriod", cx["period"][1], sec, "Chart@maxPeriod", st["complexity_why"])
    p.set_attr(ch, "minShift", cx["shift"][0], sec, "Chart@minShift", "Siempre vela cerrada (sin mirar el futuro).")
    p.set_attr(ch, "maxShift", cx["shift"][1], sec, "Chart@maxShift",
               "Patrones de 2-3 velas." if cx["shift"][1] > 1 else "Como el original.")

    # --- SL/PT (sólo estrategia completa)
    if E:
        sl, pt = st["sltp"]["sl"], st["sltp"]["pt"]
        b = "Settings/WhatToBuild/SLPTOptions/"
        sec = "What to build · SL/PT"
        p.text(b + "SLRequired", "true", sec, "SLRequired", "SL obligatorio en todos los estilos.")
        p.text(b + "SLATR", "true", sec, "SLATR", "SL en múltiplos de ATR: se adapta al timeframe y al símbolo.")
        p.text(b + "MinSLATRMultiple", sl[0], sec, "MinSLATRMultiple", f"Rango de SL del estilo: {sl[0]}-{sl[1]} ATR.")
        p.text(b + "MaxSLATRMultiple", sl[1], sec, "MaxSLATRMultiple", f"Rango de SL del estilo: {sl[0]}-{sl[1]} ATR.")
        p.text(b + "MinSLATRPeriod", sl[2], sec, "MinSLATRPeriod", f"ATR({sl[2]}-{sl[3]}) en velas {st['tf']}.")
        p.text(b + "MaxSLATRPeriod", sl[3], sec, "MaxSLATRPeriod", f"ATR({sl[2]}-{sl[3]}) en velas {st['tf']}.")
        p.text(b + "PTRequired", "true" if st["sltp"]["pt_required"] else "false", sec, "PTRequired",
               "Objetivo obligatorio (estilo de objetivo corto)." if st["sltp"]["pt_required"]
               else "Objetivo opcional: el estilo sale por trailing/tiempo/fin de día.")
        p.text(b + "PTATR", "true", sec, "PTATR", "PT en múltiplos de ATR.")
        p.text(b + "MinPTATRMultiple", pt[0], sec, "MinPTATRMultiple", f"Rango de PT: {pt[0]}-{pt[1]} ATR.")
        p.text(b + "MaxPTATRMultiple", pt[1], sec, "MaxPTATRMultiple", f"Rango de PT: {pt[0]}-{pt[1]} ATR.")
        p.text(b + "MinPTATRPeriod", pt[2], sec, "MinPTATRPeriod", f"ATR({pt[2]}-{pt[3]}).")
        p.text(b + "MaxPTATRPeriod", pt[3], sec, "MaxPTATRPeriod", f"ATR({pt[2]}-{pt[3]}).")
        rrr = st["sltp"]["rrr"]
        p.text(b + "LimitSLPTRRR", "true" if rrr else "false", sec, "LimitSLPTRRR",
               "PT expresado como % del SL (ver Fase 1: con SL/PT en ATR SQX puede no respetarlo)."
               if rrr else "Sin límite R:R: el PT es opcional y la salida principal es otra.")
        if rrr:
            p.text(b + "LimitSLPTRRRFrom", rrr[0], sec, "LimitSLPTRRRFrom", f"PT = {rrr[0]}-{rrr[1]} % del SL.")
            p.text(b + "LimitSLPTRRRTo", rrr[1], sec, "LimitSLPTRRRTo", f"PT = {rrr[0]}-{rrr[1]} % del SL.")

    # --- Motor genético
    g = st["genetic"]
    b = "Settings/WhatToBuild/BuildMode/"
    sec = "Genetic options"
    p.text(b + "PopulationSize", g["pop"], sec, "PopulationSize",
           f"{g['pop']} por isla × {g['islands']} islas = {g['pop'] * g['islands']} por generación: más diversidad que el "
           "original (5-15) sin que la población inicial tarde horas en completarse.")
    p.text(b + "MaxGenerations", g["gens"], sec, "MaxGenerations",
           "Con 10 generaciones la evolución apenas actúa (y el reinicio por estancamiento a 30 nunca saltaba).")
    p.text(b + "Islands", g["islands"], sec, "Islands", "4 islas: diversidad suficiente con menos coste.")
    p.text(b + "CrossoverProbability", 80, sec, "CrossoverProbability",
           "46 % es bajo para un AG; 70-90 % es lo habitual (supuesto de práctica general, no de SQX).")
    p.text(b + "MutationProbability", 30, sec, "MutationProbability", "Algo menor para no destruir buenas soluciones.")
    p.text(b + "MigrationModulo", 10, sec, "MigrationModulo", "Migrar cada 10 generaciones (con 30-40 generaciones).")
    p.text(b + "MigrationRate", 10, sec, "MigrationRate",
           "6 % de 5 individuos = 0,3: la migración original era nula en la práctica.")
    p.attr(b + "EvoRestartOnStagnation", "generations", 15, sec, "EvoRestartOnStagnation@generations",
           "Debe ser menor que MaxGenerations para poder actuar.")

    # --- Filtros de población inicial y finales
    f = st["filt"]
    mt = min_trades(st)
    tr = mt["is"]
    if E:
        rd, wn, pf, ab = f["retdd"], f["win"], f["pf"], f["avgbars"]
    else:
        rd, wn, ab = round(f["retdd"] / 2, 2), max(30, f["win"] - 5), f["avgbars"]
        pf = 1.3 if st["name"] == "Position" else 1.15
    init = [("NumberOfTrades", ">=", int(round(tr * 0.3 / 10.0)) * 10, "IS")]
    p.replace_conditions(p.find(b + "Conditions"), init, "main", sec, "BuildMode/Conditions (población inicial)",
                         "SÓLO nº mínimo de operaciones (30 % del mínimo final), como recomienda SQX. La población "
                         "inicial no se guarda en el banco y SQX genera aleatorias hasta completarla: con 80-100 "
                         "individuos y filtros de rentabilidad (Ret/DD, acierto) el Builder puede pasar horas o días "
                         "sin producir nada. La exigencia de calidad está en los filtros del Ranking.")
    final = [("NumberOfTrades", ">=", tr, "IS"), ("ReturnDDRatio", ">=", rd, "IS"),
             ("WinningPct", ">=", wn, "IS"), ("ProfitFactor", ">=", pf, "IS"),
             ("AvgBarsInTrade", ">=", ab, "IS")]
    if st["valid"]:
        final.append(("NetProfit", ">", 0, "OOS"))
        final.append(("NumberOfTrades", ">=", mt["oos"], "OOS"))
    p.replace_conditions(p.find("Settings/Rankings/Conditions"), final, "main", "Ranking",
                         "Rankings/Conditions (filtros)",
                         f"Mínimo de operaciones = {mt['per_year']}/año × años de cada tramo (el original exigía "
                         "300 en 7,25 años ≈ 41/año; ningún estilo baja de esa densidad salvo Position) + "
                         "umbrales del estilo + exigencia en el tramo de validación OOS, que el original no tenía."
                         + ("" if E else " Test de ventaja: Ret/DD a la mitad, PF mínimo 1,15."))
    fitness(p, weighted_tpl, st["fitness"] if E else st["edge_fitness"],
            st["fitness_why"] if E else "SQN mide la calidad estadística de la entrada (expectativa/desviación·√N); "
            "el original optimizaba sólo 'Stagnation', que ignora el beneficio.")

    # --- MM y datos
    patch_mm(p, kind, st)
    bd = st["build_dates"]
    patch_setup(p, p.find("Settings/Data/Setups/Setup"), st,
                (bd[0], bd[1], "Periodo de construcción; 2021-2024 queda reservado como OOS final del Retest."
                 if bd[0] == "2013.09.30" else "M5/M15: 5 años bastan en operaciones y reducen el cómputo."))
    patch_oos(p, st["valid"], "Nuevo tramo de validación dentro del Builder (el original no tenía OOS y "
              "filtraba sólo sobre IS)." if st["valid"] else
              "Sin OOS en el Builder: con ~20 operaciones/año un tramo de 2 años (≈40) es poco informativo; la "
              "validación se hace en el Retest (2021-2024).")
    for s in p.findall("Settings/CrossChecks/RetestOnAdditionalMarkets/Settings/Setups/Setup"):
        p.set_attr(s.find("Chart"), "timeframe", st["tf"], "Cross checks", "RetestOnAdditionalMarkets/Setup@timeframe",
                   "Coherencia si se activa (sigue desactivado).")

    # --- Bloques
    p.attr("Settings/Blocks/Calibration", "calibrateBeforeStart", "true", "Building blocks",
           "Calibration@calibrateBeforeStart",
           "Recalibra antes de empezar los rangos de valores de los indicadores (p. ej. ATR y rangos de órdenes "
           "stop/limit, que traen ±5000 por defecto) con el símbolo y timeframe de Data. Sin ello, al cambiar de H1 a "
           "M5/M15/H4/D1 las comparaciones con números y los desplazamientos de órdenes stop/limit no tienen sentido.")
    patch_blocks(p, st, side)
    patch_order_types(p, st, kind)
    patch_exit_types(p, st, kind)
    patch_notes(p, st, kind, orig, side)


def patch_blocks(p: Patcher, st: dict, side: str):
    sig, ind, stl, params = compose(st["blocks"], side)
    wanted = {**sig, **ind, **stl}
    blocks = {b.get("key"): b for b in p.findall("Settings/Blocks/BuildingBlocks/Block")}
    missing = [k for k in wanted if k not in blocks]
    if missing:
        raise KeyError(f"Bloques inexistentes en el catálogo: {missing}")
    for cat in ("signals", "indicators", "stopLimitBlocks"):
        old_on = sorted(k for k, b in blocks.items() if b.get("category") == cat and b.get("use") == "true")
        for k, b in blocks.items():
            if b.get("category") != cat:
                continue
            use = "true" if k in wanted else "false"
            if b.get("use") != use:
                b.set("use", use)
                p.touched.add((id(b), "use"))
            w = str(wanted.get(k, 1))
            if b.get("weight") != w:
                b.set("weight", w)
                p.touched.add((id(b), "weight"))
        new_on = sorted(k for k, b in blocks.items() if b.get("category") == cat and b.get("use") == "true")
        p._log("Building blocks", f"Bloques activos · {cat}", f"{len(old_on)} activos",
               f"{len(new_on)} activos: " + ", ".join(f"{k}(w{wanted[k]})" for k in new_on),
               st["block_why"] + (" Versión SELL: bloques y niveles espejados." if side == "SELL" else ""))
    for k, ranges in params.items():
        p.block_params(blocks[k], ranges, "Rango acotado al estilo (ver ficha)"
                       + (" y espejado para SELL." if side == "SELL" else "."))


def patch_order_types(p: Patcher, st: dict, kind: str):
    sec = "Order types"
    eab = st["edge_eab"] if kind == "VB" else (st["exits"]["eab"][2:] if st["exits"]["eab"] else None)
    for key, (use, w) in st["orders"].items():
        b = p.find(f"Settings/Blocks/OrderTypes/Block[@key='{key}']")
        p.set_attr(b, "use", "true" if use else "false", sec, f"{key}@use", st["orders_why"])
        p.set_attr(b, "weight", w, sec, f"{key}@weight", "Peso relativo entre tipos de orden.")
        bv = b.find("Generated/Param[@key='#BarsValid#']")
        if bv is not None and use:
            p.set_attr(bv, "minValue", st["bars_valid"][0], sec, f"{key} · BarsValid min", st["orders_why"])
            p.set_attr(bv, "maxValue", st["bars_valid"][1], sec, f"{key} · BarsValid max", st["orders_why"])
        ea = b.find("Generated/Param[@key='#ExitAfterBars.ExitAfterBars#']")
        if eab and use:
            p.set_attr(ea, "minValue", eab[0], sec, f"{key} · ExitAfterBars min",
                       "Alineado con el rango de ExitTypes para eliminar la ambigüedad del original (5-20 vs 2-15).")
            p.set_attr(ea, "maxValue", eab[1], sec, f"{key} · ExitAfterBars max",
                       "Alineado con el rango de ExitTypes.")


def _exit_block(p, key):
    return p.find(f"Settings/Blocks/ExitTypes/Block[@key='{key}']")


def _atr_value(p, blk, rng, label, why):
    for v in blk.findall("Value"):
        k = v.get("key")
        if k.endswith("FixedValue"):
            p.set_attr(v, "use", "false", "Exit types", f"{label} · {k.split('.')[-1]}",
                       "Valores fijos en pips no son trasladables entre timeframes/símbolos.")
        elif k.endswith("PctValue"):
            p.set_attr(v, "use", "false", "Exit types", f"{label} · PctValue",
                       "Coherencia con SLPTOptions (SLPercent/PTPercent = false).")
        elif k.endswith("ATRBasedValue"):
            p.set_attr(v, "use", "true", "Exit types", f"{label} · ATRBasedValue", "Salidas en ATR.")
            if rng:
                val = v.find("Generated/Param[@key='#Value#']")
                if not val.get("minValue").startswith("-10000"):
                    p.set_attr(val, "minValue", rng[0], "Exit types", f"{label} · ATR mult. min", why)
                    p.set_attr(val, "maxValue", rng[1], "Exit types", f"{label} · ATR mult. max", why)


def patch_exit_types(p: Patcher, st: dict, kind: str):
    sec = "Exit types"
    if kind == "VB":
        b = _exit_block(p, "ExitAfterBars.ExitAfterBars")
        p.set_attr(b, "use", "true", sec, "ExitAfterBars@use", st["edge_why"])
        p.set_attr(b, "probability", 100, sec, "ExitAfterBars@probability",
                   "Explícito: es la única salida (el original ponía 50 y dependía de minExitTypes=1).")
        prm = b.find("Value/Generated/Param[@key='#ExitAfterBars#']")
        p.set_attr(prm, "minValue", st["edge_eab"][0], sec, "ExitAfterBars min", st["edge_why"])
        p.set_attr(prm, "maxValue", st["edge_eab"][1], sec, "ExitAfterBars max", st["edge_why"])
        return
    ex = st["exits"]
    why = st["exits_why"]
    b = _exit_block(p, "StopLoss.StopLoss")
    p.set_attr(b, "use", "true", sec, "StopLoss@use", "SL siempre.")
    p.set_attr(b, "probability", 100, sec, "StopLoss@probability", "SL siempre.")
    _atr_value(p, b, None, "StopLoss", why)
    b = _exit_block(p, "ProfitTarget.ProfitTarget")
    p.set_attr(b, "use", "true" if ex["pt"][0] else "false", sec, "ProfitTarget@use", why)
    p.set_attr(b, "probability", 100 if st["sltp"]["pt_required"] else ex["pt"][1], sec,
               "ProfitTarget@probability", why)
    _atr_value(p, b, None, "ProfitTarget", why)
    b = _exit_block(p, "TrailingStop.TrailingStop")
    if ex["trailing"]:
        p.set_attr(b, "use", "true", sec, "TrailingStop@use", why)
        p.set_attr(b, "probability", ex["trailing"][1], sec, "TrailingStop@probability", why)
        _atr_value(p, b, ex["trailing"][2:], "TrailingStop", why)
    else:
        p.set_attr(b, "use", "false", sec, "TrailingStop@use", "El estilo no usa trailing.")
    b = _exit_block(p, "MoveSL2BE.MoveSL2BE")
    if ex["be"]:
        p.set_attr(b, "use", "true", sec, "MoveSL2BE@use", why)
        p.set_attr(b, "probability", ex["be"][1], sec, "MoveSL2BE@probability", why)
        _atr_value(p, b, ex["be"][2:], "MoveSL2BE", why)
    b = _exit_block(p, "ExitAfterBars.ExitAfterBars")
    if ex["eab"]:
        p.set_attr(b, "use", "true", sec, "ExitAfterBars@use", why)
        p.set_attr(b, "probability", ex["eab"][1], sec, "ExitAfterBars@probability", why)
        prm = b.find("Value/Generated/Param[@key='#ExitAfterBars#']")
        p.set_attr(prm, "minValue", ex["eab"][2], sec, "ExitAfterBars min", why)
        p.set_attr(prm, "maxValue", ex["eab"][3], sec, "ExitAfterBars max", why)
    b = _exit_block(p, "_ExitRule_")
    if ex["rule"]:
        p.set_attr(b, "use", "true", sec, "_ExitRule_@use", "Salida por condición (cierre bajo media, "
                   "oscilador en zona neutra...) coherente con el estilo.")
        p.set_attr(b, "probability", ex["rule"][1], sec, "_ExitRule_@probability", why)


# =========================================================================== Retest
def patch_retest(p: Patcher, st: dict, kind: str, weighted_tpl: ET.Element, new_name: str, orig: str, side: str):
    E = kind == "ER"
    r, f = st["retest"], st["filt"]
    mt = min_trades(st)
    patch_root(p, new_name)
    patch_options(p, st)
    patch_mm(p, kind, st)
    patch_setup(p, p.find("Settings/Data/Setups/Setup"), st)
    for i, s in enumerate(p.findall("Settings/CrossChecks/RetestOnAdditionalMarkets/Settings/Setups/Setup"), 1):
        p.set_attr(s.find("Chart"), "timeframe", st["tf"], "Cross checks",
                   f"RetestOnAdditionalMarkets/Setup[{i}]@timeframe",
                   "Coherencia si se activa (sigue desactivado: el original repetía GBPJPY como 'mercado adicional').")

    # --- Ranking y filtros (el original los tenía todos desactivados)
    fitness(p, weighted_tpl, st["fitness"] if E else st["edge_fitness"], "Mismo criterio que el Builder del estilo.")
    if E:
        conds = [("NetProfit", ">", 0, "OOS")]
        if f["oos_pf"]:
            conds.append(("ProfitFactor", ">=", f["oos_pf"], "OOS"))
        conds += [("ReturnDDRatio", ">=", round(f["retdd"] * 1.5, 2), "FULL"),
                  ("NumberOfTrades", ">=", mt["full"], "FULL"),
                  ("NumberOfTrades", ">=", mt["holdout"], "OOS"),
                  ("DrawdownPct", "<=", r["dd_max"], "FULL")]
    else:
        conds = [("NetProfit", ">", 0, "OOS"),
                 ("ProfitFactor", ">=", 1.2 if st["name"] == "Position" else 1.1, "FULL"),
                 ("NumberOfTrades", ">=", mt["full"], "FULL"),
                 ("NumberOfTrades", ">=", mt["holdout"], "OOS")]
    p.replace_conditions(p.find("Settings/Rankings/Conditions"), conds, "portfolio", "Ranking",
                         "Rankings/Conditions (filtros)",
                         "El original no filtraba nada en el Retest (todas use=false) y no borraba fallidos: "
                         "se exige OOS 2021-2024 positivo y métricas del periodo completo acordes al estilo.")

    # --- Cross checks
    cc = "Settings/CrossChecks/"
    sec = "Cross checks"
    p.text(cc + "RetestWithHigherPrecision/Settings/Precision", r["precision"], sec, "HigherPrecision/Precision",
           st["retest_why"] if r["precision"] == 3 else "Tick real con spread personalizado (como el original).")
    for c in p.findall(cc + "RetestWithHigherPrecision/AcceptanceSettings/Conditions/Condition"):
        col = c.find("Left-Side/Column-Value").get("column")
        p.set_attr(c, "use", "true", sec, f"HigherPrecision · condición {col}",
                   "Activada: además del OOS ≥ 0, el nº de operaciones y el DD no deben degradarse con tick real.")

    mc = cc + "MonteCarloRetest/Settings/Methods/"
    p.text(mc + "Method[@type='RandomizeSpread']/Params/Param[@key='Min']", r["spread"][0], sec,
           "MC · RandomizeSpread Min", "Desde el spread base (el original bajaba a 1, optimista).")
    p.text(mc + "Method[@type='RandomizeSpread']/Params/Param[@key='Max']", r["spread"][1], sec,
           "MC · RandomizeSpread Max", "Hasta 2x-4x el spread base según el estilo.")
    p.attr(mc + "Method[@type='RandomizeSlippage']", "use", "true", sec, "MC · RandomizeSlippage@use",
           "El original no estresaba el deslizamiento.")
    p.text(mc + "Method[@type='RandomizeSlippage']/Params/Param[@key='Min']", r["slip"][0], sec,
           "MC · RandomizeSlippage Min", "Rango de deslizamiento del estilo (pips).")
    p.text(mc + "Method[@type='RandomizeSlippage']/Params/Param[@key='Max']", r["slip"][1], sec,
           "MC · RandomizeSlippage Max", "Rango de deslizamiento del estilo (pips).")
    if r["start_bar"]:
        p.attr(mc + "Method[@type='RandomizeStartingBar']", "use", "true", sec, "MC · RandomizeStartingBar@use",
               "Con pocas operaciones el resultado no debe depender de la vela de inicio.")
    p.text(cc + "MonteCarloRetest/Settings/NumberOfSimulations", r["mc_sims"], sec, "MC · NumberOfSimulations",
           "1000 simulaciones con backtest completo es muy costoso; 200-500 bastan para percentiles 95 %.")
    conds = p.findall(cc + "MonteCarloRetest/AcceptanceSettings/Conditions/Condition")
    lv = conds[0].find("Left-Side/Column-Value")
    p.set_attr(lv, "confidenceLevel", 95, sec, "MC · NetProfit nivel de confianza",
               "100 = el peor de N simulaciones: depende de N y de un único caso extremo; 95 es estable.")
    p.set_attr(lv, "sampleType", 127, sec, "MC · NetProfit muestra", "Muestra completa (MCUseFullSample=true).")
    p.set_attr(conds[1], "use", "true", sec, "MC · condición DrawdownPct@use",
               "Activada: el DD al 95 % no debe dispararse respecto al original.")
    p.set_attr(conds[1].find("Left-Side/Column-Value"), "confidenceLevel", 95, sec, "MC · DD nivel de confianza",
               "Coherente con la condición de beneficio.")
    p.set_attr(conds[1].find("Right-Side/Column-Value"), "pctRatio", r["mc_dd_pct"], sec, "MC · DD % del original",
               f"DD al 95 % ≤ {r['mc_dd_pct']} % del DD original (200 % del original es demasiado permisivo).")

    mm = cc + "MonteCarloManipulation"
    p.attr(mm, "use", "true", sec, "MonteCarloManipulation@use", "Barato (no re-ejecuta backtest) y mide el "
           "riesgo de secuencia.")
    p.text(mm + "/Settings/Methods/Method[@type='RandomizeTradesOrder']/Params/Param[@key='Method']", "resampling",
           sec, "MCManip · RandomizeTradesOrder Method",
           "'exact' sólo permuta (el beneficio neto no cambia); 'resampling' (bootstrap) varía beneficio y DD.")
    rs = p.find(mm + "/AcceptanceSettings/Conditions/Condition/Right-Side/Column-Value")
    p.set_attr(rs, "resultType", "main", sec, "MCManip · referencia de la condición NetProfit",
               "Error del original: comparaba MC contra MC (resultType=MonteCarloManipulation); debe ser el "
               "resultado principal.")
    p.set_attr(rs, "confidenceLevel", 50, sec, "MCManip · nivel de la referencia",
               "La referencia pasa a ser el backtest principal, que no tiene percentiles; 50 es el valor neutro "
               "que usan el resto de condiciones.")

    spp = cc + "OptProfileSysParamPermutation/"
    p.text(spp + "Settings/MaxTests", r["spp_tests"], sec, "SPP · MaxTests",
           "15.000 backtests por estrategia es desproporcionado en M5/M15; se ajusta por estilo.")
    p.text(spp + "Settings/DistributionUp", r["spp_dist"], sec, "SPP · DistributionUp", "±% alrededor del valor.")
    p.text(spp + "Settings/DistributionDown", r["spp_dist"], sec, "SPP · DistributionDown", "±% alrededor del valor.")
    p.text(spp + "AcceptanceSettings/ProfitOptPct", r["spp_profit"], sec, "SPP · ProfitOptPct",
           "% de permutaciones rentables exigido; 95 % penaliza en exceso a estilos sensibles a costes.")
    for c in p.findall(spp + "AcceptanceSettings/Conditions/Condition"):
        lv = c.find("Left-Side/Column-Value")
        if lv.get("sampleType") != "127":
            p.set_attr(lv, "sampleType", 127, sec,
                       f"SPP · {lv.get('column')} (pctRatio {lv.get('pctRatio')}) muestra (izq.)",
                       "Inconsistencia del original: comparaba IS (10) contra el original en muestra completa (127).")

    wi = cc + "WhatIf"
    p.attr(wi, "use", "true", sec, "WhatIf@use", "Mide la dependencia de operaciones extremas.")
    if r["whatif"] == "top2":
        for t, u in (("ExcludePctTradesWithBiggestPl", "false"), ("ExcludePctTradesWithLowestPl", "false"),
                     ("ExcludeTradesWithBiggestPl", "true"), ("ExcludeTradesWithLowestPl", "true")):
            p.attr(f"{wi}/Settings/Methods/Method[@type='{t}']", "use", u, sec, f"WhatIf · {t}@use",
                   "Estilo de pocas ganancias grandes: se quitan las 2 mejores y 2 peores (no el 5 %, que "
                   "por diseño destruiría cualquier sistema tendencial).")

    patch_notes(p, st, kind, orig, side)


# =========================================================================== cobertura del registro
def diff_unlogged(orig: ET.Element, new: ET.Element, p: Patcher, path="Task") -> list[str]:
    """Toda diferencia entre original y nuevo debe estar registrada (touched/replaced)."""
    out = []
    if id(new) in p.replaced:
        return out
    for a in set(orig.attrib) | set(new.attrib):
        if orig.get(a) != new.get(a) and (id(new), a) not in p.touched:
            out.append(f"{path}@{a}: {orig.get(a)} -> {new.get(a)}")
    if (orig.text or "").strip() != (new.text or "").strip() and (id(new), "#text") not in p.touched:
        out.append(f"{path}#text")
    if len(orig) != len(new):
        out.append(f"{path}: nº de hijos {len(orig)} -> {len(new)}")
        return out
    for i, (co, cn) in enumerate(zip(orig, new)):
        out += diff_unlogged(co, cn, p, f"{path}/{cn.tag}[{i}]")
    return out


# =========================================================================== salida
def write_changes_md(path: Path, title: str, orig: str, st: dict, kind: str, changes, side: str):
    lines = [f"# {title}", "",
             f"*Original:* `{orig}.cfx` · *Estilo:* {st['title']} · *Timeframe:* {st['tf']} · "
             f"*Rol:* {KIND_LABEL[kind]} · *Dirección:* {side}", "",
             "Tabla generada automáticamente a partir de los cambios aplicados al XML (cada fila es un valor "
             "que difiere del original). Estado: **no validado en SQX** (ver docs/04).", "",
             "| Sección | Parámetro | Valor original | Valor nuevo | Justificación |",
             "|---|---|---|---|---|"]
    esc = lambda s: str(s).replace("|", "\\|").replace("\n", " ")
    for c in changes:
        lines.append(f"| {esc(c.section)} | `{esc(c.label)}` | {esc(c.old)} | {esc(c.new)} | {esc(c.why)} |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv=None):
    ap = argparse.ArgumentParser()
    root = Path(__file__).resolve().parent.parent
    ap.add_argument("--originales", type=Path, default=root / "originales")
    ap.add_argument("--salida", type=Path, default=root / "configs")
    ap.add_argument("--docs", type=Path, default=root / "docs" / "cambios")
    ap.add_argument("--estilo", action="append", help="Generar sólo estos estilos")
    a = ap.parse_args(argv)

    paths = {k: locate(a.originales, v) for k, v in ORIGINALS.items()}
    tpl_build = load_cfx(paths["VB"]).find("Settings/Rankings/FitnessCriteria/Settings/Ranking")
    tpl_retest = load_cfx(paths["VR"]).find("Settings/Rankings/FitnessCriteria/Settings/Ranking")
    a.docs.mkdir(parents=True, exist_ok=True)
    index = []
    errors = 0
    for st in STYLES:
        if a.estilo and st["name"] not in a.estilo:
            continue
        for side in SIDES:
            for kind, base in ORIGINALS.items():
                pristine = load_cfx(paths[kind])
                work = copy.deepcopy(pristine)
                p = Patcher(work)
                new_name = cfx_name(base, st, side)
                if kind in ("EB", "VB"):
                    patch_builder(p, st, kind, tpl_build, new_name, base, side)
                else:
                    patch_retest(p, st, kind, tpl_retest, new_name, base, side)
                unlogged = diff_unlogged(pristine, work, p)
                if unlogged:
                    errors += 1
                    print(f"[ERROR] {new_name}: cambios sin registrar:\n  " + "\n  ".join(unlogged[:20]))
                out = a.salida / st["name"] / f"{new_name}.cfx"
                save_cfx(work, out)
                write_changes_md(a.docs / f"{new_name}.md", new_name, base, st, kind, p.changes, side)
                index.append((st["name"], kind, out, len(p.changes)))
                print(f"OK {out.relative_to(root)}  ({len(p.changes)} cambios registrados)")
    print(f"\n{len(index)} archivos generados, {errors} con cambios sin registrar.")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
