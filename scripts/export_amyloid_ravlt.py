#!/usr/bin/env python3
"""Export de-identified RAVLT recognition counts (amyloid groups).

This is the 200-person extract used in Twelve Angry Models, not the larger
clinical table with demographics or identifiers.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "datasets/working-memory-recognition/ravlt-amyloid"
sys.path.insert(0, str(Path(__file__).resolve().parent))
from io_util import write_csv, write_data_mat, load_local_paths  # noqa: E402

SRC = load_local_paths().AMYLOID_CSV


def main() -> None:
    df = pd.read_csv(SRC)
    df.columns = [c.strip() for c in df.columns]
    status = {1: "negative", 2: "positive"}
    rows = []
    for i, r in df.iterrows():
        rows.append(
            {
                "participant": i + 1,
                "amyloid_status": status[int(r["group"])],
                "hits": int(r["hit"]),
                "misses": int(r["miss"]),
                "false_alarms": int(r["fa"]),
                "correct_rejections": int(r["cr"]),
                "n_old": 15,
                "n_new": 15,
            }
        )
    n = write_csv(OUT / "counts.csv", rows)
    write_data_mat(OUT)
    n_neg = sum(1 for r in rows if r["amyloid_status"] == "negative")
    n_pos = sum(1 for r in rows if r["amyloid_status"] == "positive")
    print(f"OK ravlt-amyloid rows={n} negative={n_neg} positive={n_pos}")


if __name__ == "__main__":
    main()
