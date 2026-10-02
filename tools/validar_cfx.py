"""Validación estática de los .cfx generados (no sustituye a abrirlos en SQX).

Comprueba, para cada archivo de configs/:
 1. ZIP válido con una única entrada config.xml y XML bien formado.
 2. Mismo tipo de tarea y misma versión que su original.
 3. Estructura: cada ruta de nodo y cada atributo existe en alguno de los 4 originales
    (no hay nodos ni atributos inventados).
 4. Catálogo de bloques idéntico al original (mismas claves, ninguna añadida ni eliminada).
 5. Coherencia de valores: rangos min<=max, pasos >0, probabilidades 0-100, horas 0-86399,
    fechas válidas y OOS dentro del periodo, al menos una orden de entrada y una señal activas,
    fitness ponderado con algún objetivo, columnas y comparadores de condiciones conocidos.
 6. Sin rutas con nombre de usuario de Windows.
 7. Ida y vuelta: los originales se reescriben sin pérdida (C14N idéntico).

Uso: python tools/validar_cfx.py [--originales originales] [--configs configs] [--informe docs/validacion/informe_validacion.md]
"""

from __future__ import annotations

import argparse
import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sqx_cfx import COLUMN_FORMAT, load_cfx, to_xml_bytes  # noqa: E402
from generar_cfx import ORIGINALS, locate  # noqa: E402

SENTINEL = re.compile(r"^-10000\d\d$")
COMPARATORS = {">", ">=", "<", "<=", "==", "!="}
KNOWN_COLUMNS = set(COLUMN_FORMAT) | {"Drawdown", "WFPctOfProfitableRuns", "WFMaxProfitByRunInPct",
                                      "WFMinTradesInRun", "WFMaxPctDDbyRun"}


def paths(e: ET.Element, prefix="") -> dict[str, set]:
    out: dict[str, set] = {}
    p = f"{prefix}/{e.tag}"
    out.setdefault(p, set()).update(e.attrib)
    for c in e:
        for k, v in paths(c, p).items():
            out.setdefault(k, set()).update(v)
    return out


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def check(root: ET.Element, orig: ET.Element, allowed: dict, name: str) -> list[str]:
    err = []
    if root.tag != "Task" or root.get("type") != orig.get("type") or root.get("version") != orig.get("version"):
        err.append("tipo/versión de tarea distintos del original")
    for p, attrs in paths(root).items():
        if p not in allowed:
            err.append(f"ruta de nodo desconocida: {p}")
        elif not attrs <= allowed[p]:
            err.append(f"atributos desconocidos en {p}: {sorted(attrs - allowed[p])}")
    raw = to_xml_bytes(root).decode("utf-8")
    if re.search(r"[A-Za-z]:\\Users\\(?!<usuario>)", raw):
        err.append("contiene una ruta C:\\Users\\<nombre>")

    is_build = root.get("type") == "Build"
    if is_build:
        ko = {b.get("key") for b in orig.iter("Block") if b.get("category") in ("signals", "indicators", "stopLimitBlocks")}
        kn = {b.get("key") for b in root.iter("Block") if b.get("category") in ("signals", "indicators", "stopLimitBlocks")}
        if ko != kn:
            err.append(f"catálogo de bloques distinto: +{sorted(kn - ko)} -{sorted(ko - kn)}")
        used = [b for b in root.find("Settings/Blocks/BuildingBlocks") if b.get("use") == "true"]
        if not any(b.get("category") == "signals" for b in used) and not any(
                b.get("category") == "indicators" for b in used):
            err.append("ningún bloque de entrada activo")
        ots = [b for b in root.find("Settings/Blocks/OrderTypes") if b.get("use") == "true"]
        if not ots:
            err.append("ningún tipo de orden activo")
        if any(b.get("key") in ("EnterAtStop", "EnterAtLimit") for b in ots) and not any(
                b.get("category") == "stopLimitBlocks" for b in used):
            err.append("órdenes stop/limit activas sin bloques de nivel de precio")
        ch = root.find("Settings/WhatToBuild/RulesComplexity/Chart")
        for a, b in (("minConditions", "maxConditions"), ("minExitConditions", "maxExitConditions"),
                     ("minExitTypes", "maxExitTypes"), ("minPeriod", "maxPeriod"), ("minShift", "maxShift")):
            if num(ch.get(a)) > num(ch.get(b)):
                err.append(f"RulesComplexity {a} > {b}")
        st = root.find("Settings/WhatToBuild/StrategyType")
        if st.get("type") == "simple" and num(ch.get("maxConditions")) < 1:
            err.append("modo simple sin condiciones de entrada")
        ets = [b for b in root.find("Settings/Blocks/ExitTypes") if b.get("use") == "true"]
        if len(ets) < num(ch.get("minExitTypes")):
            err.append(f"minExitTypes={ch.get('minExitTypes')} pero sólo {len(ets)} tipos de salida activos")
        for b in root.iter("Block"):
            pr = b.get("probability")
            if pr is not None and not 0 <= num(pr) <= 100:
                err.append(f"probabilidad fuera de rango en {b.get('key')}")
        slpt = root.find("Settings/WhatToBuild/SLPTOptions")
        for a, b in (("MinSLATRMultiple", "MaxSLATRMultiple"), ("MinPTATRMultiple", "MaxPTATRMultiple"),
                     ("MinSLATRPeriod", "MaxSLATRPeriod"), ("MinPTATRPeriod", "MaxPTATRPeriod"),
                     ("LimitSLPTRRRFrom", "LimitSLPTRRRTo")):
            if num(slpt.find(a).text) > num(slpt.find(b).text):
                err.append(f"SLPTOptions {a} > {b}")
        bm = root.find("Settings/WhatToBuild/BuildMode")
        if num(bm.find("EvoRestartOnStagnation").get("generations")) >= num(bm.find("MaxGenerations").text):
            err.append("EvoRestartOnStagnation >= MaxGenerations (nunca actuaría)")

    # parámetros aleatorios
    for prm in root.iter("Param"):
        mn, mx, stp = prm.get("minValue"), prm.get("maxValue"), prm.get("step")
        if num(mn) is not None and num(mx) is not None and not (SENTINEL.match(mn) or SENTINEL.match(mx)):
            if num(mn) > num(mx):
                err.append(f"Param {prm.get('name')} min>max ({mn}>{mx})")
            if num(stp) is not None and num(stp) <= 0:
                err.append(f"Param {prm.get('name')} step<=0")
    # horas de Trading options
    for prm in root.findall("Settings/Options/BuildTradingOptions/Params/Param"):
        if prm.get("key").endswith("Time") or prm.get("key").startswith("SignalTimeRange"):
            if not 0 <= num(prm.text) <= 86399:
                err.append(f"hora fuera de rango en {prm.get('key')}")
    # fechas
    fmt = "%Y.%m.%d"
    setup = root.find("Settings/Data/Setups/Setup")
    d0, d1 = (datetime.strptime(setup.get(a), fmt) for a in ("dateFrom", "dateTo"))
    if d0 >= d1:
        err.append("dateFrom >= dateTo")
    for r in root.findall("Settings/Data/OutOfSample/Range"):
        r0, r1 = (datetime.strptime(r.get(a), fmt) for a in ("dateFrom", "dateTo"))
        if not (d0 < r0 < r1 <= d1):
            err.append(f"rango OOS {r.get('dateFrom')}-{r.get('dateTo')} fuera del periodo")
    # condiciones
    for c in root.iter("Condition"):
        cmp_ = c.find("Comparator").get("value")
        if cmp_ not in COMPARATORS:
            err.append(f"comparador desconocido {cmp_}")
        lv = c.find("Left-Side/Column-Value")
        if lv is not None and lv.get("column") not in KNOWN_COLUMNS:
            err.append(f"columna desconocida {lv.get('column')}")
    # fitness
    rk = root.find("Settings/Rankings/FitnessCriteria/Settings/Ranking")
    if rk.get("type") == "Weighted" and not any(g.get("use") == "true" for g in rk.findall("Goal")):
        err.append("fitness ponderado sin objetivos")
    return err


def main(argv=None):
    base = Path(__file__).resolve().parent.parent
    ap = argparse.ArgumentParser()
    ap.add_argument("--originales", type=Path, default=base / "originales")
    ap.add_argument("--configs", type=Path, default=base / "configs")
    ap.add_argument("--informe", type=Path, default=base / "docs" / "validacion" / "informe_validacion.md")
    a = ap.parse_args(argv)

    origs = {k: load_cfx(locate(a.originales, v)) for k, v in ORIGINALS.items()}
    allowed: dict[str, set] = {}
    for o in origs.values():
        for k, v in paths(o).items():
            allowed.setdefault(k, set()).update(v)

    lines = ["# Informe de validación estática", "",
             "Generado por `tools/validar_cfx.py`. Una validación estática **no garantiza** que SQX build 144 "
             "abra los archivos sin avisos: sólo que son ZIP/XML válidos, con la misma estructura, atributos y "
             "catálogo de bloques que los originales build 140.2099 y con valores coherentes.", "",
             "## Ida y vuelta de los originales", "", "| Original | C14N idéntico tras reescribir |", "|---|---|"]
    total_err = 0
    for k, v in ORIGINALS.items():
        p = locate(a.originales, v)
        with zipfile.ZipFile(p) as z:
            raw = z.read("config.xml").decode("utf-8")
        same = ET.canonicalize(raw) == ET.canonicalize(to_xml_bytes(origs[k]).decode("utf-8"))
        total_err += 0 if same else 1
        lines.append(f"| {v}.cfx | {'sí' if same else '**NO**'} |")

    lines += ["", "## Archivos generados", "", "| Archivo | Tamaño ZIP | Resultado |", "|---|---|---|"]
    files = sorted(a.configs.glob("*/*.cfx"))
    for f in files:
        kind = next(k for k, v in ORIGINALS.items() if f.name.startswith(v + "__"))
        try:
            with zipfile.ZipFile(f) as z:
                if z.namelist() != ["config.xml"] or z.testzip() is not None:
                    raise ValueError("ZIP inesperado")
            root = load_cfx(f)
            errs = check(root, origs[kind], allowed, f.name)
        except Exception as ex:  # noqa: BLE001
            errs = [f"no se puede leer: {ex}"]
        total_err += len(errs)
        res = "OK" if not errs else "<br>".join(errs)
        lines.append(f"| `{f.relative_to(a.configs)}` | {f.stat().st_size:,} B | {res} |")
        print(("OK   " if not errs else "FAIL ") + f.name + ("" if not errs else "\n   " + "\n   ".join(errs)))
    lines += ["", f"**Total: {len(files)} archivos, {total_err} errores.**", ""]
    a.informe.parent.mkdir(parents=True, exist_ok=True)
    a.informe.write_text("\n".join(lines), encoding="utf-8")
    print(f"\n{len(files)} archivos, {total_err} errores -> {a.informe}")
    return 1 if total_err else 0


if __name__ == "__main__":
    sys.exit(main())
