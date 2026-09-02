"""Shared CSV/MATLAB naming: camelCase columns and a single struct d."""

from __future__ import annotations

import csv
import importlib.util
import re
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.io import savemat


def load_local_paths():
    """Load gitignored local/paths.py (source locations for rebuilds)."""
    root = Path(__file__).resolve().parents[1]
    path_file = root / "local" / "paths.py"
    if not path_file.is_file():
        raise SystemExit(f"Missing {path_file} (gitignored maintainer file).")
    spec = importlib.util.spec_from_file_location("local_paths", path_file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


FILE_STEMS = {
    "game_reward_rates": "gameRewardRates",
    "task_order": "taskOrder",
    "related_tasks": "relatedTasks",
    "problem_values": "problemValues",
    "condition_order": "conditionOrder",
    "cue_validities": "cueValidities",
    "study1_gain_loss": "study1GainLoss",
    "experiment1_training": "experiment1Training",
    "experiment1_testing": "experiment1Testing",
    "experiment2_training": "experiment2Training",
    "experiment2_testing": "experiment2Testing",
    "serial_position_counts": "serialPositionCounts",
    "murdock1962_wide": "murdock1962Wide",
    "continuous_osn": "continuousOSN",
    "study_test_osn": "studyTestOSN",
    "continuous_on": "continuousON",
    "study_test_on": "studyTestON",
    "source_id": "sourceId",
}

ACRONYMS = {"osn": "OSN", "on": "ON"}


def to_camel(name: str) -> str:
    name = str(name).strip()
    if not name:
        return name
    if name in FILE_STEMS:
        return FILE_STEMS[name]
    if name == "condtype":
        return "condType"
    if "_" not in name and "-" not in name:
        if name and name[0].isupper() and len(name) > 1 and name[1:].islower():
            return name[0].lower() + name[1:]
        return name
    parts = [p for p in re.split(r"[_\-]+", name) if p]
    if not parts:
        return name

    def piece(part: str, i: int) -> str:
        low = part.lower()
        if low in ACRONYMS and i > 0:
            return ACRONYMS[low]
        if part.isupper() and not part.isdigit():
            return part
        if part.isdigit():
            return part
        if i == 0:
            return part[0].lower() + part[1:]
        return part[0].upper() + part[1:]

    return "".join(piece(p, i) for i, p in enumerate(parts))


def camel_filename(name: str) -> str:
    path = Path(name)
    return f"{to_camel(path.stem)}{path.suffix}"


def _camel_row(row: dict) -> dict:
    return {to_camel(k): v for k, v in row.items()}


def write_csv(path: Path, rows: list[dict], fieldnames: list[str] | None = None) -> int:
    path = path.with_name(camel_filename(path.name))
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("")
        return 0
    rows = [_camel_row(r) for r in rows]
    fieldnames = [to_camel(c) for c in (fieldnames or list(rows[0].keys()))]
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    return len(rows)


def write_dataframe(path: Path, df: pd.DataFrame, *, header: bool = True) -> None:
    path = path.with_name(camel_filename(path.name))
    path.parent.mkdir(parents=True, exist_ok=True)
    if header:
        df = df.rename(columns={c: to_camel(str(c)) for c in df.columns})
    df.to_csv(path, index=False, header=header)


def _is_numeric_row(line: str) -> bool:
    cells = [c.strip() for c in line.split(",")]
    if not cells or cells == [""]:
        return False

    def ok(c: str) -> bool:
        if c == "":
            return True
        try:
            float(c)
            return True
        except ValueError:
            return False

    return all(ok(c) for c in cells)


def _series_to_mat(s: pd.Series):
    if pd.api.types.is_numeric_dtype(s):
        return np.asarray(pd.to_numeric(s, errors="coerce"), dtype=float)
    vals = s.where(s.notna(), "").astype(str).replace({"nan": "", "None": ""})
    return np.array(vals.to_list(), dtype=object)


def _df_to_struct(df: pd.DataFrame) -> dict:
    return {str(c): _series_to_mat(df[c]) for c in df.columns}


def write_data_mat(folder: Path) -> Path:
    """Write data.mat with a single struct d. Extra source .mat files are removed."""
    csvs = sorted(p for p in folder.glob("*.csv") if p.name != "CATALOG.csv")
    d: dict = {}
    named = []
    for path in csvs:
        first = path.read_text(errors="replace").splitlines()
        if not first:
            continue
        headerless = _is_numeric_row(first[0])
        if headerless:
            arr = np.loadtxt(path, delimiter=",")
            d[to_camel(path.stem)] = np.atleast_2d(arr)
        else:
            df = pd.read_csv(path)
            df.columns = [to_camel(str(c)) for c in df.columns]
            named.append((to_camel(path.stem), df))
    if len(named) == 1 and not any(k for k in d if k not in {named[0][0]}):
        # one named table and no headerless matrices: fields live on d
        d.update(_df_to_struct(named[0][1]))
    else:
        for stem, df in named:
            d[stem] = _df_to_struct(df)
    out = folder / "data.mat"
    savemat(str(out), {"d": d}, do_compression=True, oned_as="column")
    for mat in folder.glob("*.mat"):
        if mat.name != "data.mat":
            mat.unlink()
    return out
