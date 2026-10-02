"""Genera docs/03_Fase3_Fichas_Diseno.md.

Las tablas "original → nuevo" se leen de los XML original y generado (no se copian a mano), así que la
ficha refleja exactamente lo que contiene cada .cfx de configs/.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sqx_cfx import Patcher, load_cfx  # noqa: E402
from estilos import STYLES  # noqa: E402
from generar_cfx import ORIGINALS, cfx_name, locate  # noqa: E402
from estilos import min_trades  # noqa: E402
from familias import FAMILIA_DESC, IND, SIG, STL, compose, mirror_key  # noqa: E402
from narrativa import CORE_WHY, NARR, PREGUNTAS, SUPUESTOS  # noqa: E402

BASE = Path(__file__).resolve().parent.parent


def hhmm(sec: str) -> str:
    s = int(float(sec))
    return f"{s // 3600:02d}:{(s % 3600) // 60:02d}"


def opt(r, key):
    return r.find(f"Settings/Options/BuildTradingOptions/Params/Param[@key='{key}']").text


# ----------------------------------------------------------------------------- extractores
def tf(r): return r.find("Settings/Data/Setups/Setup/Chart").get("timeframe")
def dates(r):
    s = r.find("Settings/Data/Setups/Setup")
    return f"{s.get('dateFrom')} – {s.get('dateTo')}"
def oos(r): return "; ".join(f"{x.get('dateFrom')} – {x.get('dateTo')}" for x in r.findall("Settings/Data/OutOfSample/Range")) or "sin OOS"
def slip(r): return r.find("Settings/Data/Setups/Setup").get("slippage")
def mode(r):
    s = r.find("Settings/WhatToBuild/StrategyType")
    return s.get("type") + (" (plantilla externa .sqx)" if s.get("type") == "template" else "")
def chart(r, a, b):
    c = r.find("Settings/WhatToBuild/RulesComplexity/Chart")
    return f"{c.get(a)}–{c.get(b)}"
def orders(r):
    out = []
    for b in r.find("Settings/Blocks/OrderTypes"):
        if b.get("use") == "true":
            bv = b.find("Generated/Param[@key='#BarsValid#']")
            out.append(b.get("key") + f" (w{b.get('weight')}" + (f", válida {bv.get('minValue')}-{bv.get('maxValue')} velas)" if bv is not None else ")"))
    return ", ".join(out)
def slpt(r, which):
    o = r.find("Settings/WhatToBuild/SLPTOptions")
    req = o.find(f"{which}Required").text
    if o.find(f"{which}ATR").text != "true":
        return f"obligatorio={req}; sin ATR"
    s = (f"obligatorio={req}; {o.find(f'Min{which}ATRMultiple').text}-{o.find(f'Max{which}ATRMultiple').text} × "
         f"ATR({o.find(f'Min{which}ATRPeriod').text}-{o.find(f'Max{which}ATRPeriod').text})")
    if which == "PT" and o.find("LimitSLPTRRR").text == "true":
        s += f"; PT={o.find('LimitSLPTRRRFrom').text}-{o.find('LimitSLPTRRRTo').text} % del SL"
    return s
def exit_t(r, key):
    b = r.find(f"Settings/Blocks/ExitTypes/Block[@key='{key}']")
    if b.get("use") != "true":
        return "no"
    s = f"sí ({b.get('probability')} %)"
    p = b.find("Value/Generated/Param[@key='#ExitAfterBars#']")
    if p is not None:
        s += f", {p.get('minValue')}-{p.get('maxValue')} velas"
    for v in b.findall("Value"):
        if v.get("key", "").endswith("ATRBasedValue") and v.get("use") == "true":
            pv = v.find("Generated/Param[@key='#Value#']")
            if pv is not None and not pv.get("minValue").startswith("-10000"):
                s += f", {pv.get('minValue')}-{pv.get('maxValue')} ATR"
        if v.get("key", "").endswith("FixedValue") and v.get("use") == "true" and key.startswith(("Trailing", "MoveSL")):
            pv = v.find("Generated/Param[@key='#Value#']")
            s += f", fijo {pv.get('minValue')}-{pv.get('maxValue')} pips"
    return s
def window(r):
    if opt(r, "LimitTimeRange") != "true":
        return "sin ventana"
    s = f"{hhmm(opt(r, 'SignalTimeRangeFrom'))}-{hhmm(opt(r, 'SignalTimeRangeTo'))}"
    return s + (" + cierre al final" if opt(r, "ExitAtEndOfRange") == "true" else "")
def eod(r):
    a = f"diario {hhmm(opt(r, 'EODExitTime'))}" if opt(r, "ExitAtEndOfDay") == "true" else "no diario"
    b = f"viernes {hhmm(opt(r, 'FridayExitTime'))}" if opt(r, "ExitOnFriday") == "true" else "no viernes"
    return f"{a}; {b}"
def maxtr(r): return opt(r, "MaxTradesPerDay") + (" (sin límite)" if opt(r, "MaxTradesPerDay") == "0" else "")
def maxdist(r): return f"{opt(r, 'MaxDistancePct')} %" if opt(r, "MaxDistanceFromMarket") == "true" else "no"
def blocks(r):
    bb = r.find("Settings/Blocks/BuildingBlocks")
    c = {k: 0 for k in ("signals", "indicators", "stopLimitBlocks")}
    for b in bb:
        if b.get("use") == "true":
            c[b.get("category")] += 1
    return f"{c['signals']} señales / {c['indicators']} indicadores / {c['stopLimitBlocks']} stop-limit"
def mm(r):
    for m in r.find("Settings/RiskMoneyManagement/MoneyManagement").findall("Method"):
        if m.get("use") == "true":
            ps = {p.get("key"): p.text for p in m.find("Params")}
            if m.get("type") == "FixedAmount":
                return f"FixedAmount: riesgo {ps['RiskedMoney']} por operación"
            if m.get("type") == "FixedSize":
                return f"FixedSize: {ps['Size']} lote"
            return m.get("type")
def fit(r): return Patcher.describe_ranking(r.find("Settings/Rankings/FitnessCriteria/Settings/Ranking"))
def filt(r): return Patcher.describe_conditions(r.find("Settings/Rankings/Conditions"))
def init(r): return Patcher.describe_conditions(r.find("Settings/WhatToBuild/BuildMode/Conditions"))
def gen(r):
    b = r.find("Settings/WhatToBuild/BuildMode")
    g = lambda t: b.find(t).text
    return (f"población {g('PopulationSize')} × {g('Islands')} islas, {g('MaxGenerations')} generaciones, "
            f"cruce {g('CrossoverProbability')} %, mutación {g('MutationProbability')} %, migración "
            f"{g('MigrationRate')} % cada {g('MigrationModulo')}, reinicio por estancamiento a "
            f"{b.find('EvoRestartOnStagnation').get('generations')}")
def cc(r, name): return "activo" if r.find(f"Settings/CrossChecks/{name}").get("use") == "true" else "no"
def hp(r):
    x = r.find("Settings/CrossChecks/RetestWithHigherPrecision")
    pr = {"1": "M1 simulado", "2": "tick real + spread personalizado", "3": "tick real + spread real"}
    n = sum(1 for c in x.iter("Condition") if c.get("use") == "true")
    return f"{'activo' if x.get('use') == 'true' else 'no'}; precisión {x.find('Settings/Precision').text} ({pr.get(x.find('Settings/Precision').text, '?')}); {n} condiciones"
def g(x):
    try:
        return f"{float(x):g}"
    except (TypeError, ValueError):
        return x


def mc(r):
    x = r.find("Settings/CrossChecks/MonteCarloRetest")
    ms = []
    for m in x.find("Settings/Methods"):
        if m.get("use") == "true":
            ps = {p.get("key"): p.text for p in m.find("Params")}
            if m.get("type") == "RandomizeSpread":
                ms.append(f"spread {g(ps['Min'])}-{g(ps['Max'])}")
            elif m.get("type") == "RandomizeSlippage":
                ms.append(f"desliz. {g(ps['Min'])}-{g(ps['Max'])}")
            elif m.get("type") == "RandomizeHistoryDataOHLC":
                ms.append(f"OHLC ±{ps['MaxChange']} % ATR({ps['ATRPeriod']})")
            elif m.get("type") == "RandomizeStartingBar":
                ms.append("vela de inicio")
            else:
                ms.append(m.get("type"))
    acc = Patcher.describe_conditions(x.find("AcceptanceSettings/Conditions"))
    return f"{'activo' if x.get('use') == 'true' else 'no'}; {x.find('Settings/NumberOfSimulations').text} sims; " + ", ".join(ms) + f". Acepta: {acc}"
def mcm(r):
    x = r.find("Settings/CrossChecks/MonteCarloManipulation")
    meth = x.find("Settings/Methods/Method[@type='RandomizeTradesOrder']/Params/Param").text
    return f"{'activo' if x.get('use') == 'true' else 'no'}; orden de operaciones '{meth}', saltar 10 %"
def spp(r):
    x = r.find("Settings/CrossChecks/OptProfileSysParamPermutation")
    s = x.find("Settings")
    return (f"{'activo' if x.get('use') == 'true' else 'no'}; {s.find('MaxTests').text} tests, ±{s.find('DistributionUp').text} %, "
            f"{s.find('Steps').text} pasos; ≥{x.find('AcceptanceSettings/ProfitOptPct').text} % rentables")
def whatif(r):
    x = r.find("Settings/CrossChecks/WhatIf")
    ms = [m.get("type") for m in x.find("Settings/Methods") if m.get("use") == "true"]
    return f"{'activo' if x.get('use') == 'true' else 'no'}; " + ", ".join(ms)


def _o(st, key):
    return st["options"].get(key, ("", ""))[1]


def _exit_why(st, kind, what):
    if kind == "VB":
        return st["edge_why"] if what == "time" else "Test de ventaja: sin SL/PT ni otras salidas, para aislar la entrada."
    return st["exits_why"]


# (etiqueta, extractor, justificación(st, narr, kind))
BUILD_ROWS = [
    ("Timeframe", tf, lambda st, n, k: f"Horizonte típico del estilo ({st['tf']})."),
    ("Periodo de datos", dates, lambda st, n, k: "Construcción hasta 2020; 2021-2024 reservado para el Retest (S4)."
     if st["build_dates"][0] == "2013.09.30" else "M5/M15: 5 años dan miles de operaciones y reducen el cómputo; "
     "2021-2024 sigue reservado (S4)."),
    ("Tramo OOS", oos, lambda st, n, k: "Validación dentro del Builder: el original filtraba sólo sobre IS."
     if st["valid"] else "Sin OOS en el Builder: con ~8 operaciones/año 2 años no informan; se valida en el Retest."),
    ("Deslizamiento (pips)", slip, lambda st, n, k: st["slippage_why"]),
    ("Modo de generación", mode, lambda st, n, k: "El original dependía de una plantilla .sqx no incluida; en modo "
     "simple el archivo es autónomo (docs/04 §A.3 para volver a plantilla)." if k == "EB" else ""),
    ("Condiciones de entrada", lambda r: chart(r, "minConditions", "maxConditions"),
     lambda st, n, k: "Nivel + 1-2 filtros como máximo; más condiciones = más grados de libertad."
     + (" Position: máx. 2 por la muestra pequeña." if st["name"] == "Position" else "")),
    ("Periodos de indicadores", lambda r: chart(r, "minPeriod", "maxPeriod"), lambda st, n, k: st["complexity_why"]),
    ("Desplazamiento (shift)", lambda r: chart(r, "minShift", "maxShift"),
     lambda st, n, k: "Patrones de 2-3 velas." if st["complexity"]["shift"][1] > 1 else "Vela cerrada."),
    ("Tipos de salida (mín–máx)", lambda r: chart(r, "minExitTypes", "maxExitTypes"),
     lambda st, n, k: "Sólo la salida temporal (test de ventaja)." if k == "VB" else
     "SL obligatorio + salidas propias del estilo (el original pedía hasta 5 con 3 disponibles)."),
    ("Tipos de orden", orders, lambda st, n, k: st["orders_why"]),
    ("Stop loss", lambda r: slpt(r, "SL"), lambda st, n, k: _exit_why(st, k, "sl")),
    ("Profit target", lambda r: slpt(r, "PT"), lambda st, n, k: _exit_why(st, k, "pt")),
    ("Trailing stop", lambda r: exit_t(r, "TrailingStop.TrailingStop"), lambda st, n, k: _exit_why(st, k, "ts")),
    ("Break-even", lambda r: exit_t(r, "MoveSL2BE.MoveSL2BE"), lambda st, n, k: _exit_why(st, k, "be")),
    ("Salida temporal", lambda r: exit_t(r, "ExitAfterBars.ExitAfterBars"), lambda st, n, k: _exit_why(st, k, "time")),
    ("Salida por regla", lambda r: exit_t(r, "_ExitRule_"), lambda st, n, k: _exit_why(st, k, "rule")),
    ("Ventana de señales", window, lambda st, n, k: _o(st, "SignalTimeRangeTo") or _o(st, "LimitTimeRange")),
    ("Cierres forzados", eod, lambda st, n, k: _o(st, "ExitAtEndOfDay") or "El estilo mantiene posiciones."),
    ("Máx. operaciones/día", maxtr, lambda st, n, k: _o(st, "MaxTradesPerDay")),
    ("Distancia máx. orden", maxdist, lambda st, n, k: _o(st, "MaxDistancePct")),
    ("Bloques activos", blocks, lambda st, n, k: st["block_why"]),
    ("Gestión monetaria", mm, lambda st, n, k: "Tamaño fijo: el test de ventaja compara entradas, no capital."
     if k == "VB" else f"Riesgo fijo {st['risk'] / 100:g} % (no compuesto: Ret/DD comparable en el tiempo)."),
    ("Fitness", fit, lambda st, n, k: st["fitness_why"] if k == "EB" else
     "SQN mide la calidad estadística de la entrada; el original optimizaba sólo 'Stagnation', que ignora el beneficio."),
    ("Filtros (Ranking)", filt, lambda st, n, k: "Umbrales del estilo + exigencia OOS."
     + (" Test de ventaja: Ret/DD a la mitad y PF ≥1,15." if k == "VB" else "")),
    ("Filtro población inicial", init, lambda st, n, k: "Misma proporción que el autor (≈60 % Ret/DD, ≈83 % "
     "operaciones, -5 puntos de acierto)."),
    ("Motor genético", gen, lambda st, n, k: "Población y generaciones del original insuficientes para que la "
     "evolución actúe (Fase 1 §6)."),
]
RETEST_ROWS = [
    ("Timeframe", tf, lambda st, n, k: "Debe coincidir con el Builder del estilo."),
    ("Periodo / OOS", lambda r: f"{dates(r)}; OOS {oos(r)}", lambda st, n, k: "Holdout del autor conservado."),
    ("Deslizamiento", slip, lambda st, n, k: st["slippage_why"]),
    ("Ventana de señales", window, lambda st, n, k: "Idéntica al Builder: si difiere, el Retest no reproduce lo construido."),
    ("Cierres forzados", eod, lambda st, n, k: "Idénticos al Builder."),
    ("Gestión monetaria", mm, lambda st, n, k: "Igual que el Builder correspondiente."),
    ("Fitness", fit, lambda st, n, k: "Igual que el Builder correspondiente."),
    ("Filtros (Ranking)", filt, lambda st, n, k: "El original no filtraba nada (todas use=false) ni borraba fallidas."),
    ("Mayor precisión", hp, lambda st, n, k: st["retest_why"] if st["retest"]["precision"] == 3 else
     "Se activan también las condiciones de nº de operaciones y DD."),
    ("Monte Carlo retest", mc, lambda st, n, k: "Spread desde el base hasta 2-4x, deslizamiento, percentil 95 "
     "(no el peor caso) y control del DD."),
    ("Monte Carlo manipulación", mcm, lambda st, n, k: "Barato; 'resampling' y referencia corregida (el original "
     "comparaba MC contra MC)."),
    ("SPP / perfil de optimización", spp, lambda st, n, k: "Tests y exigencia ajustados al coste de cómputo y a la "
     "sensibilidad del estilo."),
    ("What-if", whatif, lambda st, n, k: "Quitar 2 mejores/peores (estilos de outliers)." if st["retest"]["whatif"]
     == "top2" else "Quitar el 5 % de extremos: el estilo no debe depender de outliers."),
]


def esc(s): return str(s).replace("|", "\\|")


def table(rows, orig, new, st, narr, kind):
    out = ["| Parámetro | Original | Nuevo | Justificación |", "|---|---|---|---|"]
    for label, fn, why_fn in rows:
        try:
            o = fn(orig)
        except Exception:  # noqa: BLE001
            o = "—"
        n = fn(new)
        why = "Sin cambio." if o == n else why_fn(st, narr, kind)
        out.append(f"| {label} | {esc(o)} | {esc(n)} | {esc(why)} |")
    return out


def ficha(st, origs) -> list[str]:
    n = st["name"]
    narr = NARR[n]
    files = {k: BASE / "configs" / n / f"{cfx_name(v, st, 'BUY')}.cfx" for k, v in ORIGINALS.items()}
    files_sell = {k: BASE / "configs" / n / f"{cfx_name(v, st, 'SELL')}.cfx" for k, v in ORIGINALS.items()}
    new = {k: load_cfx(p) for k, p in files.items()}
    mt = min_trades(st)
    L = [f"## {n}", "", f"**{st['title']}** · timeframe `{st['tf']}`", ""]
    if narr["alternativa"]:
        L += [f"> **Viabilidad:** {narr['alternativa']}", ""]
    L += ["**Archivos del kit** (todos *no validados en SQX*; tabla completa de cambios en `docs/cambios/`):", "",
          "| Rol | BUY | SELL |", "|---|---|---|"]
    for k in ORIGINALS:
        b, sl = files[k], files_sell[k]
        L.append(f"| {k} | [`{b.name}`](cambios/{b.stem}.md) | [`{sl.name}`](cambios/{sl.stem}.md) |")
    L += ["", f"**Operaciones mínimas exigidas** ({mt['per_year']}/año): Builder IS ≥ {mt['is']}"
          + (f", OOS 2019-2020 ≥ {mt['oos']}" if mt["oos"] else "")
          + f" (≈{mt['is'] + mt['oos']} en {mt['build_total_years']:.1f} años de construcción); Retest periodo "
          f"completo ≥ {mt['full']} y holdout 2021-2024 ≥ {mt['holdout']}."]
    L += ["", "### 1. Tesis", "", st["tesis"], "",
          "### 2. Cambios respecto al original", "",
          "#### 2.a Builder de estrategia completa (`Estrategia_Build`)", ""]
    L += table(BUILD_ROWS, origs["EB"], new["EB"], st, narr, "EB")
    L += ["", "#### 2.b Builder de test de ventaja (`Ventaja_Build`)", ""]
    L += table(BUILD_ROWS, origs["VB"], new["VB"], st, narr, "VB")
    L += ["", "#### 2.c Retesters (`Estrategia_Retest` / `Ventaja_Retest`)", ""]
    L += table(RETEST_ROWS, origs["ER"], new["ER"], st, narr, "ER")
    L += ["", "Diferencias del `Ventaja_Retest` respecto al anterior:", ""]
    for label, fn, _w in RETEST_ROWS:
        if fn(new["ER"]) != fn(new["VR"]):
            L.append(f"- **{label}:** {esc(fn(new['VR']))}")
    sig, ind, stl, params = compose(st["blocks"], "BUY")
    sig_s, ind_s, stl_s, params_s = compose(st["blocks"], "SELL")
    L += ["", "### 3. Indicadores y bloques seleccionados", "",
          f"Criterio general: {st['block_why']}", "",
          f"Recuento: **{len(sig)} señales, {len(ind)} indicadores y {len(stl)} niveles/rangos stop-limit** "
          "(el original: 146 / 29 / 29, todos con peso 1 y sin relación con la tesis). Las familias con peso ≥ 2 "
          "son el núcleo del estilo; las de peso 1 son filtros auxiliares que amplían la variedad de estrategias "
          "sin cambiar la tesis. Se excluyen siempre los bloques con niveles absolutos dependientes del precio. "
          "La columna SELL muestra el bloque espejo que se activa en el kit de ventas.", ""]
    for cat, fams, d, d_s in (("Señales", SIG, sig, sig_s), ("Indicadores", IND, ind, ind_s),
                              ("Niveles y rangos stop/limit", STL, stl, stl_s)):
        L += [f"#### {cat}", "", "| Familia (peso) | Qué mide | Por qué en este estilo | Bloques BUY | Espejo SELL |",
              "|---|---|---|---|---|"]
        spec = st["blocks"]["signals" if fams is SIG else "indicators" if fams is IND else "stoplimit"]
        for fam, w in spec:
            keys = fams[fam]
            buy = ", ".join(f"`{k.split('.')[-1]}`" + (f"(w{d[k]})" if d[k] != w else "") for k in keys)
            mir = [mirror_key(k) for k in keys]
            sell = "igual (neutral)" if mir == keys else ", ".join(f"`{m.split('.')[-1]}`" for m in mir)
            why = CORE_WHY[n].get(fam) if w >= 2 else None
            why = why or ("Núcleo del estilo." if w >= 2 else "Filtro auxiliar: amplía la variedad.")
            L.append(f"| {fam} ({w}) | {FAMILIA_DESC[fam]} | {why} | {buy} | {sell} |")
        L.append("")
    L += ["#### Rangos específicos (BUY → SELL)", "", "| Bloque BUY | Rango BUY | Bloque SELL | Rango SELL |",
          "|---|---|---|---|"]
    fmt_r = lambda ps: "; ".join(f"{p} {a} a {b} (paso {c})" for p, (a, b, c) in ps.items())
    seen = set()
    for k, ps in params.items():
        m = mirror_key(k)
        if (k, m) in seen or (m, k) in seen:
            continue
        seen.add((k, m))
        L.append(f"| `{k}` | {fmt_r(ps)} | `{m}` | {fmt_r(params_s[m])} |")
    L += ["", "### 4. Timeframe, símbolos y horarios", "",
          f"- **Timeframe:** {st['tf']}.",
          f"- **Instrumento recomendado:** {st['instrumento']}",
          f"- **Horario:** {narr['horario']}", "",
          "### 5. Salidas y gestión del riesgo", "", narr["salidas"], "",
          "### 6. Filtros y ranking", "",
          "| Archivo | Fitness | Filtros |", "|---|---|---|"]
    for k in ORIGINALS:
        L.append(f"| `{files[k].stem}` | {esc(fit(new[k]))} | {esc(filt(new[k]))} |")
    L += ["", f"Justificación: {st['fitness_why']} El mínimo de operaciones sale de la densidad del estilo "
          f"({mt['per_year']}/año) multiplicada por los años de cada tramo; el acierto y el Ret/DD se adaptan al "
          "estilo. Los archivos SELL usan exactamente los mismos filtros.", "",
          "### 7. Motor y robustez", "",
          f"- **Builder:** {gen(new['EB'])}.",
          f"- **Retest:** {hp(new['ER'])}. {st['retest_why']}",
          f"- **Monte Carlo:** {mc(new['ER'])}.",
          f"- **Manipulación MC:** {mcm(new['ER'])}.",
          f"- **SPP:** {spp(new['ER'])}.",
          f"- **What-if:** {whatif(new['ER'])}.", "",
          "### 8. Riesgos conocidos, sobreoptimización y mitigación", "",
          f"Riesgos propios del estilo: {st['riesgos']}", ""]
    L += [f"{i}. {t}" for i, t in enumerate(narr["sobreajuste"], 1)]
    L += ["", "### 9. Plan de validación", ""]
    L += [f"{i}. {t}" for i, t in enumerate(narr["validacion"], 1)]
    L += ["", "---", ""]
    return L


def main():
    origs = {k: load_cfx(locate(BASE / "originales", v)) for k, v in ORIGINALS.items()}
    L = ["# Fase 3 — Fichas de diseño por estilo", "",
         "Documento generado por `tools/generar_fichas.py`: las tablas \"Original → Nuevo\" se leen de los XML, "
         "por lo que coinciden con los `.cfx` de `configs/`. El detalle exhaustivo (cada valor modificado) está "
         "en `docs/cambios/`.", "",
         "## Preguntas abiertas (máximo 5)", "",
         "Se formulan antes de diseñar; al no tener respuesta se continúa con los supuestos de la tabla "
         "siguiente. Cualquier respuesta distinta se traslada cambiando `tools/estilos.py` y regenerando.", ""]
    L += [f"{i}. {q}" for i, q in enumerate(PREGUNTAS, 1)]
    L += ["", "## Supuestos explícitos", "", "| Id | Tema | Supuesto |", "|---|---|---|"]
    L += [f"| {a} | {b} | {c} |" for a, b, c in SUPUESTOS]
    L += ["", "## Estructura común de cada kit", "",
          "Cada estilo tiene **dos kits idénticos salvo la dirección**: BUY (`Market sides` = long) y SELL "
          "(`Market sides` = short, bloques y niveles espejados). Cada kit conserva la arquitectura de dos etapas "
          "del autor, que es su principal acierto:", "",
          "1. **`Ventaja_Build`** busca *entradas* con ventaja usando sólo una salida temporal y tamaño fijo "
          "(sin SL/PT), para medir la entrada aislada.",
          "2. **`Ventaja_Retest`** comprueba la robustez de esa ventaja (tick real, Monte Carlo, SPP, OOS 2021-2024).",
          "3. **`Estrategia_Build`** genera la estrategia completa (entrada + SL/PT/trailing/salidas) con riesgo "
          "fijo. *Cambio metodológico*: el original usaba una plantilla externa con la entrada fija; los nuevos "
          "están en modo `simple` para funcionar sin ese archivo (docs/04 §A.3 explica cómo volver al modo plantilla).",
          "4. **`Estrategia_Retest`** valida la estrategia completa con los mismos tests y el holdout 2021-2024.", "",
          "Índice: " + " · ".join(f"[{s['name']}](#{s['name'].lower()})" for s in STYLES), "", "---", ""]
    for st in STYLES:
        L += ficha(st, origs)
    out = BASE / "docs" / "03_Fase3_Fichas_Diseno.md"
    out.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"OK {out.relative_to(BASE)} ({len(L)} líneas)")


if __name__ == "__main__":
    main()
