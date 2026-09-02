#!/usr/bin/env python3
"""Export Stark lab mnemonic similarity task (MST) trial data to CSV.

Stimulus images are not copied. Filenames identify items in the standard MST sets.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.io import loadmat

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "datasets/working-memory-recognition/stark-mst"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from io_util import write_csv, write_data_mat, load_local_paths  # noqa: E402

_src = load_local_paths()
STARK = _src.STARK
MANUEL = _src.MANUEL

OSN = {1: "old", 2: "new", 3: "similar"}
ON = {1: "old", 2: "new"}


def load_d(path: Path):
    return loadmat(str(path), squeeze_me=True, struct_as_record=False)["d"]


def stem(name: str) -> str:
    s = str(name).replace("\\", "/")
    s = re.sub(r"\.jpe?g$", "", s, flags=re.I)
    return s


def stimulus_set(name: str) -> str:
    m = re.search(r"Set\s*([A-Za-z0-9]+)", str(name), re.I)
    return m.group(1) if m else ""


def sessions(trials: np.ndarray) -> list[int]:
    out = []
    sess, prev = 1, 0
    for t in trials:
        t = int(t)
        if prev and t < prev:
            sess += 1
        out.append(sess)
        prev = t
    return out


def lags_within_person(stimuli: list[str]) -> list[str]:
    first: dict[str, int] = {}
    lags: list[str] = []
    for i, s in enumerate(stimuli):
        base = stem(s).rsplit("/", 1)[-1]
        if not base:
            lags.append("")
            continue
        key, suffix = base[:-1], base[-1]
        if suffix == "a":
            if key not in first:
                first[key] = i
                lags.append("")
            else:
                lags.append(str(i - first[key]))
        elif suffix == "b" and key in first:
            lags.append(str(i - first[key]))
        else:
            lags.append("")
    return lags


def nan_num(x):
    if x is None or (isinstance(x, (float, np.floating)) and not np.isfinite(x)):
        return ""
    return x


def assign_participants(source_ids: list[int]) -> dict[int, int]:
    uniq = sorted(set(int(x) for x in source_ids))
    return {sid: i + 1 for i, sid in enumerate(uniq)}


def rows_from_exp2_cont(path: Path) -> list[dict]:
    df = pd.read_csv(path)
    rows = []
    for sid, g in df.groupby("sid", sort=True):
        g = g.sort_values("trial")
        stims = [stem(x) for x in g["stimulus"]]
        lag = lags_within_person(stims)
        for i, (_, r) in enumerate(g.iterrows()):
            truth = int(r["truth"])
            dec = int(r["resp"])
            rows.append(
                {
                    "source_id": int(sid),
                    "session": 1,
                    "trial": int(r["trial"]),
                    "stimulus": stims[i],
                    "stimulus_set": str(int(r["set"])) if pd.notna(r["set"]) else stimulus_set(stims[i]),
                    "item_type": str(r["type"]),
                    "lure_bin": int(r["lureBin"]),
                    "lure": 1 if str(r["type"]) == "lure" else 0,
                    "truth": truth,
                    "truth_label": OSN[truth],
                    "decision": dec,
                    "decision_label": OSN.get(dec, ""),
                    "correct": int(bool(r["correct"])),
                    "rt_ms": int(r["rt"]) if pd.notna(r["rt"]) else "",
                    "lag": lag[i],
                    "study_position": "",
                    "gap": "",
                }
            )
    return rows


def rows_from_exp2_mstt(path: Path) -> list[dict]:
    df = pd.read_csv(path)
    type_map = {"TR": "target", "TF": "foil", "TL": "lure"}
    rows = []
    for sid, g in df.groupby("sid", sort=True):
        g = g.sort_values("trial")
        sess = sessions(g["trial"].to_numpy())
        for i, (_, r) in enumerate(g.iterrows()):
            truth = int(r["truth"])
            raw_dec = r["resp"]
            missing = pd.isna(r["response"]) or int(raw_dec) == 0 or int(r["rt"]) < 0
            dec = "" if missing else int(raw_dec)
            rows.append(
                {
                    "source_id": int(sid),
                    "session": sess[i],
                    "trial": int(r["trial"]),
                    "stimulus": stem(r["stimulus"]),
                    "stimulus_set": str(int(r["set"])) if pd.notna(r["set"]) else "",
                    "item_type": type_map.get(str(r["type"]), str(r["type"])),
                    "lure_bin": int(r["lureBin"]),
                    "lure": 1 if str(r["type"]) == "TL" else 0,
                    "truth": truth,
                    "truth_label": OSN[truth],
                    "decision": dec,
                    "decision_label": "" if dec == "" else OSN.get(int(dec), ""),
                    "correct": "" if missing else int(bool(r["correct"])),
                    "rt_ms": "" if missing else int(r["rt"]),
                    "lag": "",
                    "study_position": "",
                    "gap": "",
                }
            )
    return rows


def rows_from_mstt_mat(path: Path, labels: dict[int, str]) -> list[dict]:
    d = load_d(path)
    n = d.trial.size
    rows = []
    by_person: dict[int, list[int]] = {}
    for i in range(n):
        sid = int(d.participantID[i])
        by_person.setdefault(sid, []).append(i)
    for sid in sorted(by_person):
        idxs = by_person[sid]
        trials = np.array([d.trial[i] for i in idxs])
        sess = sessions(trials)
        for k, i in enumerate(idxs):
            truth = int(d.truth[i])
            lure = int(d.lure[i])
            if lure:
                item_type = "lure"
            elif truth == 1:
                item_type = "target"
            else:
                item_type = "foil"
            dec_raw = d.decision[i]
            missing = not np.isfinite(float(dec_raw))
            dec = "" if missing else int(dec_raw)
            study = getattr(d, "study", None)
            gap = getattr(d, "gap", None)
            rt = getattr(d, "rt", None)
            stim = stem(d.stimulusFull[i])
            rows.append(
                {
                    "source_id": sid,
                    "session": sess[k],
                    "trial": int(d.trial[i]),
                    "stimulus": stim,
                    "stimulus_set": stimulus_set(stim),
                    "item_type": item_type,
                    "lure_bin": int(d.lureBin[i]),
                    "lure": lure,
                    "truth": truth,
                    "truth_label": labels[truth],
                    "decision": dec,
                    "decision_label": "" if dec == "" else labels.get(int(dec), ""),
                    "correct": "" if missing else int(d.correct[i]),
                    "rt_ms": "" if missing or rt is None else float(rt[i]),
                    "lag": "",
                    "study_position": "" if study is None else nan_num(study[i]),
                    "gap": "" if gap is None else nan_num(gap[i]),
                }
            )
    return rows


def rows_from_cont_on(path: Path) -> list[dict]:
    d = load_d(path)
    n = d.trial.size
    rows = []
    by_person: dict[int, list[int]] = {}
    for i in range(n):
        by_person.setdefault(int(d.participantID[i]), []).append(i)
    for sid in sorted(by_person):
        idxs = by_person[sid]
        stims = [stem(d.stimulusFull[i]) for i in idxs]
        lag = lags_within_person(stims)
        for k, i in enumerate(idxs):
            truth = int(d.truth[i])
            lure = int(d.lure[i])
            if lure:
                item_type = "lure"
            elif truth == 1:
                item_type = "target"
            else:
                item_type = "foil"
            dec = int(d.decision[i])
            rows.append(
                {
                    "source_id": sid,
                    "session": 1,
                    "trial": int(d.trial[i]),
                    "stimulus": stims[k],
                    "stimulus_set": stimulus_set(stims[k]),
                    "item_type": item_type,
                    "lure_bin": int(d.lureBin[i]),
                    "lure": lure,
                    "truth": truth,
                    "truth_label": ON[truth],
                    "decision": dec,
                    "decision_label": ON.get(dec, ""),
                    "correct": int(d.correct[i]),
                    "rt_ms": "",
                    "lag": lag[k] if lag[k] else nan_num(d.lag[i]),
                    "study_position": "",
                    "gap": "",
                }
            )
    return rows


FIELDS = [
    "participant",
    "source_id",
    "session",
    "trial",
    "stimulus",
    "stimulus_set",
    "item_type",
    "lure_bin",
    "lure",
    "truth",
    "truth_label",
    "decision",
    "decision_label",
    "correct",
    "rt_ms",
    "lag",
    "study_position",
    "gap",
]


def add_participant(rows: list[dict], id_map: dict[int, int]) -> list[dict]:
    for r in rows:
        r["participant"] = id_map[int(r["source_id"])]
    return rows


def main() -> None:
    cont_osn = rows_from_exp2_cont(STARK / "Exp2_cont.csv")
    study_osn_exp2 = rows_from_exp2_mstt(STARK / "Exp2_mstt.csv")
    study_osn_mat = rows_from_mstt_mat(MANUEL / "msttDataOSNrt.mat", OSN)
    exp2_ids = {r["source_id"] for r in study_osn_exp2}
    study_osn = study_osn_exp2 + [r for r in study_osn_mat if r["source_id"] not in exp2_ids]
    cont_on = rows_from_cont_on(STARK / "contmstDataON.mat")
    study_on = rows_from_mstt_mat(MANUEL / "msttDataONrt.mat", ON)

    all_ids = []
    for block in (cont_osn, study_osn, cont_on, study_on):
        all_ids.extend(r["source_id"] for r in block)
    id_map = assign_participants(all_ids)

    OUT.mkdir(parents=True, exist_ok=True)
    n1 = write_csv(OUT / "continuous_osn.csv", add_participant(cont_osn, id_map), FIELDS)
    n2 = write_csv(OUT / "study_test_osn.csv", add_participant(study_osn, id_map), FIELDS)
    n3 = write_csv(OUT / "continuous_on.csv", add_participant(cont_on, id_map), FIELDS)
    n4 = write_csv(OUT / "study_test_on.csv", add_participant(study_on, id_map), FIELDS)

    def n_people(rows):
        return len({r["participant"] for r in rows})

    print(
        f"continuous_osn {n1} rows {n_people(cont_osn)} people; "
        f"study_test_osn {n2} rows {n_people(study_osn)} people; "
        f"continuous_on {n3} rows {n_people(cont_on)} people; "
        f"study_test_on {n4} rows {n_people(study_on)} people; "
        f"unique people {len(id_map)}"
    )
    write_data_mat(OUT)


if __name__ == "__main__":
    main()
