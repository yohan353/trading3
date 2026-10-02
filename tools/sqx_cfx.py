"""Lectura, modificación trazable y escritura de archivos .cfx de StrategyQuant X.

Un .cfx es un ZIP con una única entrada ``config.xml``. Este módulo:

* carga y guarda .cfx sin pérdida (la ida y vuelta es canónicamente idéntica, ver validar_cfx.py);
* ofrece un ``Patcher`` que aplica cambios sobre nodos que YA existen en el XML original y anota
  cada cambio (parámetro, valor original, valor nuevo, justificación) para generar las tablas de
  cambios de la Fase 3 directamente desde lo que se escribe en el archivo;
* sólo crea nodos copiando estructuras presentes en los propios archivos originales (condiciones de
  ranking, rango OOS, ranking ponderado), nunca nodos inventados.
"""

from __future__ import annotations

import copy
import io
import re
import zipfile
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path

ENTRY_NAME = "config.xml"

# Formato de columna que usan los propios archivos originales para cada métrica en condiciones.
COLUMN_FORMAT = {
    "ReturnDDRatio": "Decimal2",
    "AvgBarsInTrade": "Decimal2",
    "NumberOfTrades": "Integer",
    "WinningPct": "Decimal2Pct",
    "ProfitFactor": "Decimal2",
    "NetProfit": "Decimal2PL",
    "DrawdownPct": "Decimal2Pct",
    "Stagnation": "Integer",
    "StagnationPct": "Decimal2Pct",
}

SAMPLE = {"IS": "10", "OOS": "20", "FULL": "127"}

SECONDS = lambda hhmm: int(hhmm[:2]) * 3600 + int(hhmm[3:5]) * 60  # "09:30" -> 34200

_USER_PATH = re.compile(r"([A-Za-z]:\\Users\\)[^\\]+")


def fmt(value) -> str:
    """Números sin decimales espurios (1.0 -> "1"), resto tal cual."""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        return str(int(value)) if value.is_integer() else repr(value)
    return str(value)


def same_number(a, b) -> bool:
    try:
        return float(a) == float(b)
    except (TypeError, ValueError):
        return False


def redact(text: str) -> str:
    """Oculta el nombre de usuario de rutas Windows (el repositorio es público)."""
    return _USER_PATH.sub(r"\1<usuario>", str(text))


def load_cfx(path: Path) -> ET.Element:
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        if names != [ENTRY_NAME]:
            raise ValueError(f"{path}: se esperaba una sola entrada {ENTRY_NAME}, hay {names}")
        return ET.fromstring(z.read(ENTRY_NAME))


def to_xml_bytes(root: ET.Element) -> bytes:
    # Sin declaración XML, igual que los originales; UTF-8.
    return ET.tostring(root, encoding="unicode").encode("utf-8")


def save_cfx(root: ET.Element, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr(ENTRY_NAME, to_xml_bytes(root))
    path.write_bytes(buf.getvalue())


@dataclass
class Change:
    section: str
    label: str
    old: str
    new: str
    why: str


@dataclass
class Patcher:
    root: ET.Element
    changes: list[Change] = field(default_factory=list)
    touched: set = field(default_factory=set)  # (id(elem), attr|'#text') modificados
    replaced: set = field(default_factory=set)  # id(elem) de subárboles reconstruidos

    # ------------------------------------------------------------------ utilidades básicas
    def find(self, xpath: str) -> ET.Element:
        e = self.root.find(xpath)
        if e is None:
            raise KeyError(f"No existe el nodo {xpath!r}")
        return e

    def findall(self, xpath: str) -> list[ET.Element]:
        return self.root.findall(xpath)

    def _log(self, section, label, old, new, why):
        if str(old) != str(new):
            self.changes.append(Change(section, label, redact(old), redact(new), why))

    def set_attr(self, elem: ET.Element, attr: str, value, section: str, label: str, why: str):
        if attr not in elem.attrib:
            raise KeyError(f"El atributo {attr!r} no existe en <{elem.tag}> ({label})")
        old = elem.get(attr)
        value = fmt(value)
        if same_number(old, value):
            return
        if old != value:
            elem.set(attr, value)
            self.touched.add((id(elem), attr))
        self._log(section, label, old, value, why)

    def set_text(self, elem: ET.Element, value, section: str, label: str, why: str):
        old = (elem.text or "").strip()
        value = fmt(value)
        if same_number(old, value):
            return
        if old != value:
            elem.text = value
            self.touched.add((id(elem), "#text"))
        self._log(section, label, old, value, why)

    def attr(self, xpath, attr, value, section, label, why):
        self.set_attr(self.find(xpath), attr, value, section, label, why)

    def text(self, xpath, value, section, label, why):
        self.set_text(self.find(xpath), value, section, label, why)

    def mark_replaced(self, elem: ET.Element):
        self.replaced.add(id(elem))

    # ------------------------------------------------------------------ Trading options
    def option(self, key: str, value, why: str):
        p = self.find(f"Settings/Options/BuildTradingOptions/Params/Param[@key='{key}']")
        self.set_text(p, value, "Trading options", f"Param key=\"{key}\"", why)

    # ------------------------------------------------------------------ Condiciones
    @staticmethod
    def make_condition(column: str, comparator: str, value, sample: str, result_type: str) -> ET.Element:
        """Construye una <Condition> con la misma forma exacta que usan los originales."""
        c = ET.Element("Condition", {"use": "true"})
        ls = ET.SubElement(c, "Left-Side", {"valueType": "column"})
        ET.SubElement(
            ls,
            "Column-Value",
            {
                "column": column,
                "columnType": "0",
                "format": COLUMN_FORMAT[column],
                "resultType": result_type,
                "direction": "0",
                "sampleType": SAMPLE[sample],
                "plType": "10",
                "confidenceLevel": "50",
                "market": "1",
                "subresult": "30",
                "pctRatio": "0",
                "class": column,
            },
        )
        ET.SubElement(c, "Comparator", {"value": comparator})
        rs = ET.SubElement(c, "Right-Side", {"valueType": "numeric"})
        ET.SubElement(rs, "Numeric-Value", {"value": fmt(value)})
        return c

    @staticmethod
    def describe_conditions(container: ET.Element) -> str:
        out = []
        for c in container.findall("Condition"):
            if c.get("use") != "true":
                continue
            lv = c.find("Left-Side/Column-Value")
            comp = c.find("Comparator").get("value")
            rs = c.find("Right-Side")
            if rs.get("valueType") == "numeric":
                rv = rs.find("Numeric-Value").get("value")
            else:
                rc = rs.find("Column-Value")
                rv = f"{rc.get('pctRatio')}% de {rc.get('column')}[{rc.get('resultType')}]"
            sample = {"10": "IS", "20": "OOS", "127": "Full"}.get(lv.get("sampleType"), lv.get("sampleType"))
            out.append(f"{lv.get('column')}({sample}) {comp} {rv}")
        return "; ".join(out) if out else "(ninguna activa)"

    def replace_conditions(self, container: ET.Element, conds: list[tuple], result_type: str,
                           section: str, label: str, why: str):
        """conds: lista de (columna, comparador, valor, muestra)."""
        old = self.describe_conditions(container)
        for c in list(container.findall("Condition")):
            container.remove(c)
        for col, comp, val, sample in conds:
            container.append(self.make_condition(col, comp, val, sample, result_type))
        self.mark_replaced(container)
        self._log(section, label, old, self.describe_conditions(container), why)

    # ------------------------------------------------------------------ Fitness ponderado
    def weighted_fitness(self, ranking_parent: ET.Element, weighted_template: ET.Element,
                         goals: dict[str, float], section: str, why: str):
        """Sustituye el <Ranking> por el formato 'Weighted' copiado de un original y activa objetivos."""
        old_r = ranking_parent.find("Ranking")
        old_desc = self.describe_ranking(old_r)
        new_r = copy.deepcopy(weighted_template)
        known = {g.get("type") for g in new_r.findall("Goal")}
        for k in goals:
            if k not in known:
                raise KeyError(f"Objetivo de fitness desconocido: {k}")
        for g in new_r.findall("Goal"):
            if g.get("type") in goals:
                g.set("use", "true")
                g.set("weight", fmt(goals[g.get("type")]))
            else:
                g.set("use", "false")
                g.set("weight", "1")
        idx = list(ranking_parent).index(old_r)
        ranking_parent.remove(old_r)
        ranking_parent.insert(idx, new_r)
        self.mark_replaced(new_r)
        self._log(section, "FitnessCriteria/Settings/Ranking", old_desc, self.describe_ranking(new_r), why)

    @staticmethod
    def describe_ranking(r: ET.Element) -> str:
        if r.get("type") != "Weighted":
            return f"type=\"{r.get('type')}\""
        gs = []
        for g in r.findall("Goal"):
            if g.get("use") == "true":
                vt = {"1": "max", "2": "min", "3": "objetivo"}.get(g.get("valueType"), g.get("valueType"))
                gs.append(f"{g.get('type')} (peso {g.get('weight')}, {vt})")
        return "Weighted: " + ", ".join(gs)

    # ------------------------------------------------------------------ Bloques
    def block_params(self, block: ET.Element, ranges: dict[str, tuple], why: str):
        """Fija min/max/step de parámetros aleatorios (Generated y conjuntos Predefined)."""
        for pname, (mn, mx, st) in ranges.items():
            hits = 0
            for p in block.iter("Param"):
                if p.get("name") == pname and p.get("generation") == "random" and "minValue" in p.attrib:
                    old = f"{p.get('minValue')}..{p.get('maxValue')}/{p.get('step')}"
                    p.set("minValue", fmt(mn))
                    p.set("maxValue", fmt(mx))
                    p.set("step", fmt(st))
                    for a in ("minValue", "maxValue", "step"):
                        self.touched.add((id(p), a))
                    hits += 1
            if not hits:
                raise KeyError(f"El bloque {block.get('key')} no tiene parámetro aleatorio {pname!r}")
            self._log("Building blocks", f"{block.get('key')} · {pname}", old, f"{fmt(mn)}..{fmt(mx)}/{fmt(st)}", why)
