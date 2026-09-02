#!/usr/bin/env python3
"""Export the Lee & Stark (2023) Behaviormetrika MST extract.

21 people, study–test old/new and old/similar/new. Source IDs are dropped.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from scipy.io import loadmat

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "datasets/working-memory-recognition/lee-stark-2023-mst"
sys.path.insert(0, str(Path(__file__).resolve().parent))
from io_util import write_csv, write_data_mat, load_local_paths  # noqa: E402

SRC = Path(load_local_paths().LEE_STARK_MST)

OSN = {1: "old", 2: "new", 3: "similar"}
ON = {1: "old", 2: "new"}


def nan_num(x):
    if x is None or (isinstance(x, (float, np.floating)) and not np.isfinite(x)):
        return ""
    return x


def item_type(truth: int, lure: int) -> str:
    if lure:
        return "lure"
    if truth == 1:
        return "target"
    return "foil"


def rows_for(d, suffix: str, labels: dict[int, str]) -> list[dict]:
    n = getattr(d, f"trial{suffix}").size
    rows = []
    for i in range(n):
        truth = int(getattr(d, f"truth{suffix}")[i])
        lure = int(getattr(d, f"lure{suffix}")[i])
        dec_raw = getattr(d, f"decision{suffix}")[i]
        missing = not np.isfinite(float(dec_raw))
        dec = "" if missing else int(dec_raw)
        rows.append(
            {
                "participant": int(getattr(d, f"participant{suffix}")[i]),
                "trial": int(getattr(d, f"trial{suffix}")[i]),
                "stimulus": int(getattr(d, f"stimulus{suffix}")[i]),
                "item_type": item_type(truth, lure),
                "lure_bin": int(getattr(d, f"lureBin{suffix}")[i]),
                "lure": lure,
                "truth": truth,
                "truth_label": labels[truth],
                "decision": dec,
                "decision_label": "" if missing else labels.get(int(dec), ""),
                "correct": "" if missing else int(getattr(d, f"correct{suffix}")[i]),
                "study_position": nan_num(getattr(d, f"study{suffix}")[i]),
                "gap": nan_num(getattr(d, f"gap{suffix}")[i]),
            }
        )
    return rows


def main() -> None:
    d = loadmat(str(SRC), squeeze_me=True, struct_as_record=False)["d"]
    on = rows_for(d, "ON", ON)
    osn = rows_for(d, "OSN", OSN)
    OUT.mkdir(parents=True, exist_ok=True)
    n_on = write_csv(OUT / "study_test_on.csv", on)
    n_osn = write_csv(OUT / "study_test_osn.csv", osn)
    write_data_mat(OUT)
    n_people = len({r["participant"] for r in on})
    print(f"OK lee-stark-2023-mst people={n_people} on={n_on} osn={n_osn}")


if __name__ == "__main__":
    main()
