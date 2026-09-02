#!/usr/bin/env python3
"""Export de-identified bart, gasPrices, and fishPrices data.

Participant IDs are assigned from the union of student-ID keys across all three
tasks so the same person can be joined across folders. Keys never leave this
script.
"""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.io import loadmat

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "datasets"
sys.path.insert(0, str(Path(__file__).resolve().parent))
from io_util import write_csv, write_data_mat, load_local_paths  # noqa: E402
from xlsx_sheets import read_xlsx  # noqa: E402

TASKS = load_local_paths().TASKS


def excel_col(name: str) -> int:
    n = 0
    for ch in name:
        n = n * 26 + (ord(ch.upper()) - 64)
    return n - 1


def _as_float(x):
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return np.nan
    s = str(x).strip()
    if s == "":
        return np.nan
    try:
        return float(s)
    except ValueError:
        return np.nan


def _id_key(x):
    s = re.sub(r"\D", "", str(x).split(".")[0])
    return s[-8:] if len(s) >= 6 else None


def _assign_global_ids(groups: dict[str, list[dict]]) -> None:
    """Same non-null key → same anonymous integer across bart, gasPrices, and fishPrices."""
    keys = [s["key"] for sl in groups.values() for s in sl]
    mapping = {k: i + 1 for i, k in enumerate(sorted({k for k in keys if k}))}
    nxt = len(mapping) + 1
    for sl in groups.values():
        for s in sl:
            if s["key"] is None:
                s["participant"] = nxt
                nxt += 1
            else:
                s["participant"] = mapping[s["key"]]


def _add_session_numbers(sessions: list[dict]) -> None:
    session_n: dict[int, int] = {}
    for s in sessions:
        pid = s["participant"]
        session_n[pid] = session_n.get(pid, 0) + 1
        s["session"] = session_n[pid]


def collect_bart_sessions() -> list[dict]:
    sessions = []
    for quarter in ["W2023", "W2024", "F2025"]:
        d = loadmat(
            str(TASKS / "bart/data" / f"BART_{quarter}.mat"),
            squeeze_me=True,
            struct_as_record=False,
        )["d"]
        n = int(d.nParticipants)
        order = getattr(d, "order", None)
        part_ids = np.atleast_1d(d.partID)
        for i in range(n):
            sessions.append(
                {
                    "key": _id_key(part_ids[i] if i < len(part_ids) else None),
                    "quarter": quarter,
                    "d": d,
                    "i": i,
                    "order": order,
                }
            )
    return sessions


def write_bart(sessions: list[dict]) -> dict:
    out = DATA / "sequential-choice/bart"
    subscales = ["Ethical", "Financial", "Health/Safety", "Recreational", "Social"]
    trial_rows, dospert_rows = [], []
    for sess in sessions:
        d, i, quarter = sess["d"], sess["i"], sess["quarter"]
        order = sess["order"]
        rec = {
            "participant": sess["participant"],
            "quarter": quarter,
            "session": sess["session"],
            "adjusted_pumps": float(d.adjustedPumps[i]),
            "n_cashed": int(d.totalBanked[i]),
            "n_burst": int(d.totalBurst[i]),
            "dospert_perception": float(d.dospertPerception[i]),
        }
        for s, name in enumerate(subscales):
            rec[f"dospert_{name.split('/')[0].lower()}"] = float(d.subScaleScores[i, s])
        dospert_rows.append(rec)
        for j in range(int(d.nProblems)):
            pres = ""
            if order is not None:
                pres = int(order[i, j]) if np.isfinite(float(order[i, j])) else ""
            trial_rows.append(
                {
                    "participant": sess["participant"],
                    "quarter": quarter,
                    "session": sess["session"],
                    "problem": j + 1,
                    "presentation_order": pres,
                    "burst_point": int(d.burst[j]),
                    "n_pumps": int(d.y[i, j]),
                    "burst": int(d.didBurst[i, j]),
                }
            )
    n_t = write_csv(out / "trials.csv", trial_rows)
    write_csv(out / "participants.csv", dospert_rows)
    n_people = len({r["participant"] for r in dospert_rows})
    return {
        "id": "bart",
        "n_rows": n_t,
        "n_participants": n_people,
        "extra": f"sessions={len(sessions)}; unique people={n_people}",
    }


def _stop_choice(slice_vals, n_pos: int):
    for k, v in enumerate(slice_vals[:n_pos]):
        if _as_float(v) == 1:
            return k + 1
    return None


def _parse_qualtrics_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, header=0, skiprows=[1, 2])


def _write_problem_values(out: Path, blocks: list[tuple]) -> None:
    stim_rows = []
    for label, mat, var, npos in blocks:
        for p in range(mat.shape[0]):
            rec = {"stimulus_set": label, "variance": var, "problem": p + 1, "n_positions": npos}
            for t in range(npos):
                rec[f"value_{t+1}"] = float(mat[p, t])
            stim_rows.append(rec)
    write_csv(out / "problem_values.csv", stim_rows)


def _stopping_trial_rows(sessions: list[dict], n_pos: int) -> list[dict]:
    rows = []
    for sess in sessions:
        values = sess["values"]
        n_prob = values.shape[0]
        for j in range(n_prob):
            pos = int(sess["choices"][j])
            rec = {
                "participant": sess["participant"],
                "quarter": sess["quarter"],
                "session": sess["session"],
                "variance": sess["variance"],
                "problem": j + 1,
                "n_positions": n_pos,
                "choice_position": pos,
                "cost": float(values[j, pos - 1]),
            }
            for t in range(n_pos):
                rec[f"value_{t+1}"] = float(values[j, t])
            rows.append(rec)
    return rows


def collect_gas_sessions() -> list[dict]:
    stim_dir = TASKS / "optimalStopping/data"
    gas_hi = np.loadtxt(stim_dir / "gasHighVariance.csv", delimiter=",")
    gas_lo = np.loadtxt(stim_dir / "gasLowVariance.csv", delimiter=",")
    out = DATA / "sequential-choice/gasPrices"
    _write_problem_values(
        out,
        [
            ("high", gas_hi, "high", 10),
            ("low", gas_lo, "low", 10),
        ],
    )
    sessions = []
    n_pos, n_prob = 10, 20
    q0 = excel_col("T")
    for var, fname, values in [
        ("high", "optimalStoppingOne.csv", gas_hi),
        ("low", "optimalStoppingTwo.csv", gas_lo),
    ]:
        df = _parse_qualtrics_csv(stim_dir / fname)
        fin_col = next((c for c in df.columns if str(c).lower() == "finished"), None)
        if fin_col is not None:
            df = df[pd.to_numeric(df[fin_col], errors="coerce") == 1]
        for _, row in df.iterrows():
            choices = []
            ok = True
            for j in range(n_prob):
                sl = [row.iloc[q0 + j * n_pos + k] for k in range(n_pos)]
                ch = _stop_choice(sl, n_pos)
                if ch is None:
                    ok = False
                    break
                choices.append(ch)
            if not ok:
                continue
            sessions.append(
                {
                    "key": _id_key(row.iloc[excel_col("S")]),
                    "quarter": "W2023",
                    "variance": var,
                    "choices": choices,
                    "values": values,
                }
            )
    return sessions


def write_gas(sessions: list[dict]) -> dict:
    out = DATA / "sequential-choice/gasPrices"
    rows = _stopping_trial_rows(sessions, 10)
    n_t = write_csv(out / "trials.csv", rows)
    n_people = len({s["participant"] for s in sessions})
    n_hi = sum(1 for s in sessions if s["variance"] == "high")
    n_lo = sum(1 for s in sessions if s["variance"] == "low")
    return {
        "id": "gasPrices",
        "n_rows": n_t,
        "n_participants": n_people,
        "extra": f"W2023 high={n_hi} low={n_lo}",
    }


def collect_fish_sessions() -> list[dict]:
    stim_dir = TASKS / "optimalStopping/data"
    fish_hi = np.loadtxt(stim_dir / "fishHighVariance.csv", delimiter=",")
    fish_lo = np.loadtxt(stim_dir / "fishLowVariance.csv", delimiter=",")
    f2025_shuffle = [10, 9, 20, 11, 12, 13, 16, 14, 15, 17, 1, 2, 3, 4, 6, 5, 7, 8, 19, 18]
    fish_hi_f2025 = fish_hi[[i - 1 for i in f2025_shuffle], :]
    out = DATA / "sequential-choice/fishPrices"
    _write_problem_values(
        out,
        [
            ("high_W2024", fish_hi, "high", 7),
            ("high_F2025", fish_hi_f2025, "high", 7),
            ("low", fish_lo, "low", 7),
        ],
    )
    sessions = []
    n_pos, n_prob = 7, 20

    for var, fname, values, row_slice, consent_letter, q_letter, id_col in [
        (
            "high",
            "optimalStoppingOne_W2024_January+22,+2024_15.50.csv",
            fish_hi,
            slice(0, 117),
            "N",
            "O",
            11,
        ),
        (
            "low",
            "optimalStoppingTwo_W2024_January+22,+2024_15.50.csv",
            fish_lo,
            slice(3, 77),
            "F",
            "O",
            11,
        ),
    ]:
        df = pd.read_csv(stim_dir / fname, header=0)
        sub = df.iloc[row_slice]
        keep = sub[pd.to_numeric(sub.iloc[:, excel_col(consent_letter)], errors="coerce") == 1]
        q0 = excel_col(q_letter)
        for _, row in keep.iterrows():
            choices = []
            ok = True
            for j in range(n_prob):
                sl = [row.iloc[q0 + j * n_pos + k] for k in range(n_pos)]
                ch = _stop_choice(sl, n_pos)
                if ch is None:
                    ok = False
                    break
                choices.append(ch)
            if not ok:
                continue
            sessions.append(
                {
                    "key": _id_key(row.iloc[id_col]),
                    "quarter": "W2024",
                    "variance": var,
                    "choices": choices,
                    "values": values,
                }
            )

    for var, fname, values, start_row in [
        ("high", "optimalStoppingF2025_1.xlsx", fish_hi_f2025, 16),
        ("low", "optimalStoppingF2025_2.xlsx", fish_lo, 9),
    ]:
        table = read_xlsx(str(stim_dir / fname))["Raw Data"]
        body = table[1:]
        consent_i, q0 = excel_col("GC"), excel_col("U")
        stride = n_pos + 1
        for ridx, row in enumerate(body, start=2):
            if ridx < start_row:
                continue
            if consent_i >= len(row) or _as_float(row[consent_i]) != 1:
                continue
            choices = []
            ok = True
            for j in range(n_prob):
                sl = row[q0 + j * stride : q0 + j * stride + n_pos]
                ch = _stop_choice(sl, n_pos)
                if ch is None:
                    ok = False
                    break
                choices.append(ch)
            if not ok:
                continue
            sessions.append(
                {
                    "key": _id_key(row[181] if len(row) > 181 else None),
                    "quarter": "F2025",
                    "variance": var,
                    "choices": choices,
                    "values": values,
                }
            )
    return sessions


def write_fish(sessions: list[dict]) -> dict:
    out = DATA / "sequential-choice/fishPrices"
    rows = _stopping_trial_rows(sessions, 7)
    n_t = write_csv(out / "trials.csv", rows)
    n_people = len({s["participant"] for s in sessions})
    by = {}
    for s in sessions:
        by[(s["quarter"], s["variance"])] = by.get((s["quarter"], s["variance"]), 0) + 1
    return {
        "id": "fishPrices",
        "n_rows": n_t,
        "n_participants": n_people,
        "extra": f"sessions={len(sessions)} unique={n_people} counts={by}",
    }


def write_related_tasks(groups: dict[str, list[dict]]) -> None:
    counts = {task: defaultdict(int) for task in groups}
    for task, sl in groups.items():
        for s in sl:
            counts[task][s["participant"]] += 1
    paths = {
        "bart": DATA / "sequential-choice/bart/related_tasks.csv",
        "gas": DATA / "sequential-choice/gasPrices/related_tasks.csv",
        "fish": DATA / "sequential-choice/fishPrices/related_tasks.csv",
    }
    for task, path in paths.items():
        pids = sorted({s["participant"] for s in groups[task]})
        rows = [
            {
                "participant": pid,
                "bart_sessions": counts["bart"][pid],
                "gasPrices_sessions": counts["gas"][pid],
                "fishPrices_sessions": counts["fish"][pid],
            }
            for pid in pids
        ]
        write_csv(path, rows)


def main() -> None:
    groups = {
        "bart": collect_bart_sessions(),
        "gas": collect_gas_sessions(),
        "fish": collect_fish_sessions(),
    }
    _assign_global_ids(groups)
    for sl in groups.values():
        _add_session_numbers(sl)
    for info in (write_bart(groups["bart"]), write_gas(groups["gas"]), write_fish(groups["fish"])):
        print(f"OK {info}")
    write_related_tasks(groups)
    for folder in (
        DATA / "sequential-choice/bart",
        DATA / "sequential-choice/gasPrices",
        DATA / "sequential-choice/fishPrices",
    ):
        write_data_mat(folder)
    bart_pids = {s["participant"] for s in groups["bart"]}
    gas_pids = {s["participant"] for s in groups["gas"]}
    fish_pids = {s["participant"] for s in groups["fish"]}
    print(
        f"OK related_tasks gas-with-bart={len(gas_pids & bart_pids)}/{len(gas_pids)} "
        f"fish-with-bart={len(fish_pids & bart_pids)}/{len(fish_pids)}"
    )


if __name__ == "__main__":
    main()
