"""Minimal xlsx reader (shared strings + cell values) so we do not need openpyxl."""

from __future__ import annotations

import zipfile
from xml.etree import ElementTree as ET

NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
REL_NS = {
    "r": "http://schemas.openxmlformats.org/package/2006/relationships",
    "pr": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}


def _col_row(cell_ref: str) -> tuple[int, int]:
    letters = "".join(ch for ch in cell_ref if ch.isalpha())
    digits = "".join(ch for ch in cell_ref if ch.isdigit())
    col = 0
    for ch in letters:
        col = col * 26 + (ord(ch.upper()) - 64)
    return col - 1, int(digits) - 1


def _cell_text(cell: ET.Element, shared: list[str]) -> str:
    cell_type = cell.attrib.get("t")
    if cell_type == "s":
        v = cell.find("m:v", NS)
        if v is None or v.text is None:
            return ""
        return shared[int(v.text)]
    if cell_type == "inlineStr":
        texts = [t.text or "" for t in cell.findall(".//m:t", NS)]
        return "".join(texts)
    v = cell.find("m:v", NS)
    return "" if v is None or v.text is None else v.text


def read_xlsx(path: str) -> dict[str, list[list[str]]]:
    with zipfile.ZipFile(path) as zf:
        shared: list[str] = []
        if "xl/sharedStrings.xml" in zf.namelist():
            root = ET.fromstring(zf.read("xl/sharedStrings.xml"))
            for si in root.findall("m:si", NS):
                shared.append("".join(t.text or "" for t in si.findall(".//m:t", NS)))

        rels_root = ET.fromstring(zf.read("xl/_rels/workbook.xml.rels"))
        rels = {
            rel.attrib["Id"]: rel.attrib["Target"]
            for rel in rels_root.findall("r:Relationship", REL_NS)
        }

        wb = ET.fromstring(zf.read("xl/workbook.xml"))
        sheets: dict[str, list[list[str]]] = {}
        for sheet in wb.find("m:sheets", NS).findall("m:sheet", NS):
            name = sheet.attrib["name"]
            rid = sheet.attrib["{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"]
            target = rels[rid]
            if not target.startswith("xl/"):
                target = "xl/" + target.lstrip("/")
            root = ET.fromstring(zf.read(target))
            grid: dict[tuple[int, int], str] = {}
            max_r = max_c = -1
            for row in root.findall("m:sheetData/m:row", NS):
                for cell in row.findall("m:c", NS):
                    ref = cell.attrib.get("r")
                    if not ref:
                        continue
                    c, r = _col_row(ref)
                    grid[(r, c)] = _cell_text(cell, shared)
                    max_r = max(max_r, r)
                    max_c = max(max_c, c)
            table = []
            for r in range(max_r + 1):
                table.append([grid.get((r, c), "") for c in range(max_c + 1)])
            sheets[name] = table
        return sheets
