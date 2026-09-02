#!/usr/bin/env python3
"""Export BehavioralDataRepository (plus selected extras) to long-form CSVs."""

from __future__ import annotations

import csv
import re
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.io import loadmat

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "datasets"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from io_util import write_csv, write_dataframe, write_data_mat, to_camel, load_local_paths  # noqa: E402
from xlsx_sheets import read_xlsx  # noqa: E402

_src = load_local_paths()
BDR = _src.BDR
CC2 = _src.CC2
BB2 = _src.BB2


def load_struct(path: Path, var: str = "d"):
    return loadmat(str(path), squeeze_me=True, struct_as_record=False)[var]


def finite(x) -> bool:
    return np.isfinite(float(x))


def export_steyvers_bandit() -> dict:
    d = load_struct(BDR / "BanditProblems/SteyversLeeWagenmakers2009.mat")
    rows = []
    n_subj, n_games, n_trials = d.choices.shape
    for s in range(n_subj):
        for g in range(n_games):
            for t in range(n_trials):
                rows.append(
                    {
                        "participant": s + 1,
                        "game": g + 1,
                        "trial": t + 1,
                        "choice": int(d.choices[s, g, t]),
                        "reward": int(d.reward[s, g, t]),
                        "reward_rate_chosen": float(d.rewardRates[g, int(d.choices[s, g, t]) - 1]),
                    }
                )
    out = DATA / "sequential-choice/steyvers-lee-wagenmakers-2009-bandit"
    n = write_csv(out / "trials.csv", rows)
    rate_rows = []
    for g in range(d.rewardRates.shape[0]):
        rec = {"game": g + 1}
        for k in range(d.rewardRates.shape[1]):
            rec[f"reward_rate_arm{k+1}"] = float(d.rewardRates[g, k])
        rate_rows.append(rec)
    write_csv(out / "game_reward_rates.csv", rate_rows)
    write_data_mat(out)
    return {
        "id": "steyvers-lee-wagenmakers-2009-bandit",
        "n_rows": n,
        "n_participants": int(d.nSubjects),
    }


def export_lee_zhang_bandit() -> dict:
    zpath = BDR / "BanditProblems/LeeZhangMunroSteyvers2011.zip"
    env_map = {
        "A1-B1": "neutral",
        "A2-B4": "sparse",
        "A4-B2": "plentiful",
    }
    initials = []
    rows = []
    with tempfile.TemporaryDirectory() as tmp:
        with zipfile.ZipFile(zpath) as zf:
            zf.extractall(tmp)
        mats = sorted(Path(tmp).glob("*.mat"))
        for mat in mats:
            m = re.match(r"([a-z]{2})-(\d+)-S_(A\d-B\d)_dat\.mat", mat.name)
            if not m:
                continue
            init, length, env = m.group(1), int(m.group(2)), m.group(3)
            initials.append(init)
            S = loadmat(str(mat), squeeze_me=True, struct_as_record=False)
            actions, results = S["actions"], S["results"]
            g_dim, k_dim = actions.shape
            for g in range(g_dim):
                for t in range(k_dim):
                    rows.append(
                        {
                            "participant_code": init,
                            "horizon": length,
                            "environment": env_map[env],
                            "environment_code": env,
                            "game": g + 1,
                            "trial": t + 1,
                            "choice": int(actions[g, t]),
                            "reward": int(results[g, t]),
                        }
                    )
    codes = sorted(set(initials))
    code_to_id = {c: i + 1 for i, c in enumerate(codes)}
    for r in rows:
        r["participant"] = code_to_id[r.pop("participant_code")]
    out = DATA / "sequential-choice/lee-zhang-munro-steyvers-2011-bandit"
    n = write_csv(
        out / "trials.csv",
        rows,
        [
            "participant",
            "horizon",
            "environment",
            "environment_code",
            "game",
            "trial",
            "choice",
            "reward",
        ],
    )
    return {
        "id": "lee-zhang-munro-steyvers-2011-bandit",
        "n_rows": n,
        "n_participants": len(codes),
    }


def export_guan_battery() -> dict:
    """One folder per task; participant IDs 1–56 are the same person across folders."""
    bandit_dir = DATA / "sequential-choice/guan-et-al-2020-bandit"
    bart_dir = DATA / "sequential-choice/guan-et-al-2020-bart"
    stop_dir = DATA / "sequential-choice/guan-et-al-2020-optimal-stopping"
    gamble_dir = DATA / "risky-gamble-choice/guan-et-al-2020-described-gambles"

    d = load_struct(BDR / "RiskPropensity/banditGuanEtAl2020.mat")
    bandit_rows = []
    nsubj, nprob, ncond, _ = d.decisions.shape
    ntrial = np.atleast_1d(d.ntrial).astype(int)
    cond_names = [
        "horizon8_neutral",
        "horizon8_plentiful",
        "horizon16_neutral",
        "horizon16_plentiful",
    ]
    for s in range(nsubj):
        for c in range(ncond):
            k = int(ntrial[c])
            for p in range(nprob):
                for t in range(k):
                    ch = d.decisions[s, p, c, t]
                    if not finite(ch):
                        continue
                    bandit_rows.append(
                        {
                            "participant": s + 1,
                            "condition": cond_names[c],
                            "condition_index": c,
                            "problem": p + 1,
                            "trial": t + 1,
                            "horizon": k,
                            "p_left": float(d.stimuli[s, p, c, 0]),
                            "p_right": float(d.stimuli[s, p, c, 1]),
                            "choice_right": int(ch),
                            "reward": int(d.rewardChosen[s, p, c, t])
                            if finite(d.rewardChosen[s, p, c, t])
                            else "",
                            "reward_left": int(d.rewardLeft[s, p, c, t])
                            if finite(d.rewardLeft[s, p, c, t])
                            else "",
                            "reward_right": int(d.rewardRight[s, p, c, t])
                            if finite(d.rewardRight[s, p, c, t])
                            else "",
                            "problem_order": int(d.order[s, p, c]) if finite(d.order[s, p, c]) else "",
                        }
                    )
    n_bandit = write_csv(bandit_dir / "trials.csv", bandit_rows)

    d = load_struct(BDR / "RiskPropensity/BARTGuanEtAl2020.mat")
    bart_rows = []
    nsubj, nprob, ncond, _ = d.decisions.shape
    bart_cond = ["p_burst_0.1", "p_burst_0.2"]
    for s in range(nsubj):
        for c in range(ncond):
            for p in range(nprob):
                bart_rows.append(
                    {
                        "participant": s + 1,
                        "condition": bart_cond[c],
                        "condition_index": c,
                        "problem": p + 1,
                        "burst_point": int(d.stimuli[s, p, c]),
                        "burst": int(d.decisions[s, p, c, 0]),
                        "n_pumps": int(d.decisions[s, p, c, 1]),
                        "problem_order": int(d.order[s, p, c]) if finite(d.order[s, p, c]) else "",
                    }
                )
    n_bart = write_csv(bart_dir / "trials.csv", bart_rows)

    d = load_struct(BDR / "RiskPropensity/optimalStoppingGuanEtAl2020.mat")
    stop_rows = []
    nsubj, nprob, ncond = d.decisions.shape
    nstim = np.atleast_1d(d.nstim).astype(int)
    stop_cond = [
        "length4_neutral",
        "length4_plentiful",
        "length8_neutral",
        "length8_plentiful",
    ]
    for s in range(nsubj):
        for c in range(ncond):
            L = int(nstim[c])
            for p in range(nprob):
                rec = {
                    "participant": s + 1,
                    "condition": stop_cond[c],
                    "condition_index": c,
                    "problem": p + 1,
                    "sequence_length": L,
                    "choice_position": int(d.decisions[s, p, c]),
                    "problem_order": int(d.order[s, p, c]) if finite(d.order[s, p, c]) else "",
                }
                for t in range(L):
                    rec[f"value_{t+1}"] = float(d.stimuli[s, p, c, t])
                stop_rows.append(rec)
    n_stop = write_csv(stop_dir / "trials.csv", stop_rows)

    d = load_struct(BDR / "RiskPropensity/decisionTasksGeneral.mat")
    names = [str(x) for x in np.atleast_1d(d.taskNames)]
    order_rows = []
    for s in range(int(d.nsubj)):
        rec = {"participant": s + 1}
        for j, name in enumerate(names):
            rec[f"task_{j+1}"] = names[int(d.taskOrder[s, j]) - 1]
            rec[f"task_{j+1}_code"] = int(d.taskOrder[s, j])
        order_rows.append(rec)
    for dest in (bandit_dir, bart_dir, stop_dir, gamble_dir):
        write_csv(dest / "task_order.csv", order_rows)

    return {
        "id": "guan-et-al-2020",
        "n_rows": n_bandit + n_bart + n_stop,
        "n_participants": nsubj,
        "extra": f"bandit={n_bandit}; bart={n_bart}; stopping={n_stop}",
    }


def export_mount_stopping() -> dict:
    d = load_struct(BDR / "OptimalStoppingProblems/MountLee2003.mat")
    lengths = np.atleast_1d(d.problemLengths).astype(int)
    rows = []
    part_rows = []
    ravens = np.atleast_1d(d.ravens)
    for s in range(int(d.nSubjects)):
        part_rows.append({"participant": s + 1, "ravens": int(ravens[s])})
        for ti, L in enumerate(lengths):
            values = d.values[ti]
            decision = d.decision[ti]
            conf = d.confidence[ti]
            order = d.order[ti]
            nprob = decision.shape[1]
            for p in range(nprob):
                rec = {
                    "participant": s + 1,
                    "problem_length": int(L),
                    "problem": p + 1,
                    "choice_position": int(decision[s, p]),
                    "confidence": int(conf[s, p]),
                    "presentation_order": int(order[s, p]),
                }
                for t in range(int(L)):
                    rec[f"value_{t+1}"] = float(values[p, t])
                rows.append(rec)
    out = DATA / "sequential-choice/mount-2003-optimal-stopping"
    n = write_csv(out / "trials.csv", rows)
    write_csv(out / "participants.csv", part_rows)
    return {"id": "mount-2003-optimal-stopping", "n_rows": n, "n_participants": int(d.nSubjects)}


def export_stillman() -> dict:
    src = CC2 / "raw/stillmanEtAl.csv"
    out = DATA / "risky-gamble-choice/stillman-et-al-mixed-gambles"
    out.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(src)
    write_dataframe(out / "trials.csv", df)
    mixed = df[(df["study"] == "study_1") & (df["gamble_type"] == "gain_loss")]
    write_dataframe(out / "study1_gain_loss.csv", mixed)
    return {
        "id": "stillman-et-al-mixed-gambles",
        "n_rows": len(df),
        "n_participants": int(df["subject"].nunique()),
        "extra": f"study1_gain_loss={len(mixed)} rows, {mixed['subject'].nunique()} people",
    }


def _lee_cummins_block(pattern: str, n_subj: int, test_name: str) -> tuple[list[dict], list[dict]]:
    raw = BDR / "DecisionMaking/raw"
    train, test = [], []
    for i in range(1, n_subj + 1):
        path = raw / pattern.format(i)
        m = loadmat(str(path), squeeze_me=True, struct_as_record=False)
        alldec = m.get("alldec")
        testdec = m.get("testdec")
        if alldec is not None and not np.isscalar(alldec):
            arr = np.atleast_2d(alldec)
            for j, row in enumerate(arr):
                train.append(
                    {
                        "participant": i,
                        "trial": j + 1,
                        "decision": int(row[0]),
                        "left_stimulus": int(row[1]),
                        "right_stimulus": int(row[2]),
                        "rt": float(row[3]),
                        "accuracy": int(row[4]),
                    }
                )
        if testdec is not None and not np.isscalar(testdec):
            arr = np.atleast_2d(testdec)
            for j, row in enumerate(arr):
                test.append(
                    {
                        "participant": i,
                        "trial": j + 1,
                        "decision": int(row[0]),
                        "left_stimulus": int(row[1]),
                        "right_stimulus": int(row[2]),
                        "rt": float(row[3]),
                        test_name: int(row[4]),
                    }
                )
    return train, test


def export_lee_cummins() -> dict:
    out = DATA / "cue-based-multi-attribute/lee-cummins-2004"
    t1, e1 = _lee_cummins_block("gasexp-p{}.mat", 40, "confidence")
    t2, e2 = _lee_cummins_block("gasexp2-p{}.mat", 20, "confidence")
    n = 0
    n += write_csv(out / "experiment1_training.csv", t1)
    n += write_csv(out / "experiment1_testing.csv", e1)
    n += write_csv(out / "experiment2_training.csv", t2)
    n += write_csv(out / "experiment2_testing.csv", e2)
    missing = sorted({i for i in range(1, 41)} - {r["participant"] for r in t1})
    extra = "Exp1 n=40 (testing); Exp2 n=20"
    if missing:
        extra += f"; Exp1 training missing for participant(s) {missing}"
    return {"id": "lee-cummins-2004", "n_rows": n, "n_participants": 60, "extra": extra}


def export_lee_dry() -> dict:
    files = sorted((BDR / "DecisionMaking/raw/Model_Exp2").glob("P*.mat"))
    thresholds = [50, 60, 70, 80, 90, 100]
    rows = []
    order_rows = []
    pid = 0
    for f in files:
        data = loadmat(str(f), squeeze_me=True, struct_as_record=False)["data"]
        if float(data[0, 0]) != 1:
            continue
        pid += 1
        order = data[1, :6].astype(int)
        order_rows.append(
            {"participant": pid, **{f"position_{i+1}": int(order[i]) for i in range(6)}}
        )
        trials = data[2:, :]
        for c in range(6):
            sl = trials[c * 50 : (c + 1) * 50]
            pres = int(np.where(order == (c + 1))[0][0]) + 1
            for t in range(50):
                advice, truth, p1, p2, decision, conf, rt = sl[t]
                rows.append(
                    {
                        "participant": pid,
                        "condition": c + 1,
                        "advice_threshold_percent": thresholds[c],
                        "presentation_position": pres,
                        "trial": t + 1,
                        "advice": int(advice),
                        "truth": int(truth),
                        "p_left": float(p1),
                        "p_right": float(p2),
                        "decision": int(decision),
                        "confidence": int(conf),
                        "accuracy": int(truth == decision),
                        "rt": float(rt),
                    }
                )
    out = DATA / "cue-based-multi-attribute/lee-dry-2006"
    n = write_csv(out / "trials.csv", rows)
    write_csv(out / "condition_order.csv", order_rows)
    return {"id": "lee-dry-2006", "n_rows": n, "n_participants": pid}


def export_bergert() -> dict:
    B = loadmat(
        str(BB2 / "HeuristicDecisionMaking/Old/BergertNosofsky.mat"),
        squeeze_me=True,
        struct_as_record=False,
    )
    m, p, y, v, x = B["m"], B["p"], B["y"], B["v"], B["x"]
    out = DATA / "cue-based-multi-attribute/bergert-nosofsky-2007"
    cue_rows = []
    for i in range(m.shape[0]):
        rec = {"alternative": i + 1}
        for c in range(m.shape[1]):
            rec[f"cue_{c+1}"] = int(m[i, c])
        cue_rows.append(rec)
    write_csv(out / "alternatives.csv", cue_rows)
    write_csv(
        out / "cue_validities.csv",
        [
            {
                "cue": c + 1,
                "validity": float(v[c]),
                "log_odds_weight": float(x[c]),
            }
            for c in range(len(v))
        ],
    )
    problem_rows = []
    for q in range(p.shape[0]):
        problem_rows.append(
            {
                "problem": q + 1,
                "alternative_A": int(p[q, 0]),
                "alternative_B": int(p[q, 1]),
            }
        )
    write_csv(out / "problems.csv", problem_rows)
    trial_rows = []
    for s in range(y.shape[0]):
        for q in range(y.shape[1]):
            trial_rows.append(
                {
                    "participant": s + 1,
                    "problem": q + 1,
                    "choice": int(y[s, q]),
                    "alternative_A": int(p[q, 0]),
                    "alternative_B": int(p[q, 1]),
                }
            )
    n = write_csv(out / "trials.csv", trial_rows)
    return {"id": "bergert-nosofsky-2007", "n_rows": n, "n_participants": int(y.shape[0])}


def export_childers() -> dict:
    src = CC2 / "raw/childers"
    out = DATA / "working-memory-recognition/childers-recognition-sat"
    presentation_map = {1: "new", 2: "studied_once", 3: "studied_three_times"}
    freq_map = {1: "high", 2: "low", 3: "very_low"}
    cond_map = {1: "speed", 2: "accuracy"}
    resp_map = {1: "old", 2: "new"}
    rows = []
    for age, fname in [("older", "recognition.older.data"), ("young", "recognition.young.data")]:
        raw = np.loadtxt(src / fname)
        for r in raw:
            subj, pres, freq, cond, resp, rt = r
            resp_i = int(resp)
            status = presentation_map[int(pres)]
            truth = "new" if int(pres) == 1 else "old"
            decision = resp_map.get(resp_i, "no_response")
            correct = "" if resp_i not in (1, 2) else int(decision == truth)
            rows.append(
                {
                    "age_group": age,
                    "participant": int(subj),
                    "presentation": status,
                    "word_frequency": freq_map[int(freq)],
                    "instruction": cond_map[int(cond)],
                    "decision": decision,
                    "truth": truth,
                    "correct": correct,
                    "rt_ms": float(rt),
                }
            )
    n = write_csv(out / "trials.csv", rows)
    shutil.copy2(src / "README_recognition", out / "source_readme.txt")
    n_old = len({r["participant"] for r in rows if r["age_group"] == "older"})
    n_young = len({r["participant"] for r in rows if r["age_group"] == "young"})
    return {
        "id": "childers-recognition-sat",
        "n_rows": n,
        "n_participants": n_old + n_young,
        "extra": f"older={n_old}; young={n_young}",
    }


def export_kannan() -> dict:
    src = CC2 / "raw/kannan/long_data.csv"
    out = DATA / "working-memory-recognition/kannan-conditioned-recognition"
    df = pd.read_csv(src)
    out.mkdir(parents=True, exist_ok=True)
    write_dataframe(out / "trials.csv", df)
    return {
        "id": "kannan-conditioned-recognition",
        "n_rows": len(df),
        "n_participants": int(df["Subject"].nunique()),
    }


def export_murdock() -> dict:
    src = BB2 / "Simple/murdock1962.csv"
    raw = np.loadtxt(src, delimiter=",")
    rows = []
    for row in raw:
        length_rate = float(row[0])
        length = int(length_rate)
        rate = round(length_rate - length, 1)
        for pos, count in enumerate(row[1:], start=1):
            if pos > length:
                continue
            rows.append(
                {
                    "list_length": length,
                    "presentation_rate_sec": rate,
                    "serial_position": pos,
                    "recall_count": int(count),
                }
            )
    out = DATA / "working-memory-recognition/murdock-1962-free-recall"
    n = write_csv(out / "serial_position_counts.csv", rows)
    shutil.copy2(src, out / "murdock1962_wide.csv")
    return {"id": "murdock-1962-free-recall", "n_rows": n, "n_participants": None}


def export_number() -> dict:
    """Give-N and fast-cards in separate folders; participant IDs match."""
    src = BDR / "NumberDevelopment"
    pairs = [
        (
            "LeeSarnecka2011_giveN_long.csv",
            DATA / "judgment-and-estimation/lee-sarnecka-2011-give-n",
        ),
        (
            "LeeSarnecka2011_fastCards_long.csv",
            DATA / "judgment-and-estimation/lee-sarnecka-2011-fast-cards",
        ),
    ]
    n = 0
    n_part = None
    for name, out in pairs:
        df = pd.read_csv(src / name, skipinitialspace=True)
        out.mkdir(parents=True, exist_ok=True)
        write_dataframe(out / "trials.csv", df)
        n += len(df)
        n_part = int(df["participant"].nunique())
    return {
        "id": "lee-sarnecka-2011",
        "n_rows": n,
        "n_participants": n_part,
    }


def export_tsp() -> dict:
    tsp = load_struct(BDR / "TSPs/ChronicleEtAl2008.mat", "tsp")
    out = DATA / "sequential-choice/chronicle-et-al-2008-tsp"
    coord_rows = []
    for size, coords in ((30, tsp.coords30), (40, tsp.coords40)):
        for p, xy in enumerate(coords):
            for k, (x, y) in enumerate(xy):
                coord_rows.append(
                    {
                        "problem_size": size,
                        "problem": p + 1,
                        "point": k + 1,
                        "x": float(x),
                        "y": float(y),
                    }
                )
    write_csv(out / "coordinates.csv", coord_rows)
    tour_rows = []
    for size, tours in ((30, tsp.tours30), (40, tsp.tours40)):
        npts, nprob, nsubj = tours.shape
        for s in range(nsubj):
            for p in range(nprob):
                for k in range(npts):
                    tour_rows.append(
                        {
                            "participant": s + 1,
                            "problem_size": size,
                            "problem": p + 1,
                            "step": k + 1,
                            "point": int(tours[k, p, s]),
                        }
                    )
    n = write_csv(out / "tours.csv", tour_rows)

    v = loadmat(str(BDR / "TSPs/VickersEtAl2001.mat"), squeeze_me=True, struct_as_record=False)["tsp"]
    vout = DATA / "sequential-choice/vickers-et-al-2001-tsp"
    v_coord, v_tour = [], []
    for pi, item in enumerate(np.atleast_1d(v)):
        xy = np.atleast_2d(item.coords)
        for k, (x, y) in enumerate(xy):
            v_coord.append(
                {
                    "problem": pi + 1,
                    "n_points": int(item.nPoints),
                    "n_hull": int(item.nHull),
                    "point": k + 1,
                    "x": float(x),
                    "y": float(y),
                }
            )
        tours = np.atleast_2d(item.tours)
        ids = np.atleast_1d(item.subjectIDs)
        for s in range(tours.shape[0]):
            for k in range(tours.shape[1]):
                v_tour.append(
                    {
                        "problem": pi + 1,
                        "participant": int(ids[s]) if s < len(ids) else s + 1,
                        "step": k + 1,
                        "point": int(tours[s, k]),
                    }
                )
    write_csv(vout / "coordinates.csv", v_coord)
    nv = write_csv(vout / "tours.csv", v_tour)
    return {
        "id": "tsp",
        "n_rows": n + nv,
        "n_participants": int(tsp.nSubjects),
        "extra": f"chronicle_tours={n}; vickers_tours={nv}",
    }


def export_wisdom() -> dict:
    out = DATA / "judgment-and-estimation/lee-zhang-shi-2011-price-is-right"
    out.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(BDR / "WisdomOfTheCrowd/LeeZhangShi2011.csv")
    df["Episode"] = df["Episode"].ffill().astype(int)
    truth = pd.to_numeric(df["Truth"], errors="coerce")
    df["Truth"] = [
        "allOverbid" if pd.isna(v) else int(v) if float(v) == int(v) else v for v in truth
    ]
    write_dataframe(out / "bids.csv", df)

    d = load_struct(BDR / "WisdomOfTheCrowd/LeeShi2010.mat")
    wout = DATA / "judgment-and-estimation/lee-shi-2010-small-group-woc"
    est_rows = []
    names = [str(x) for x in np.atleast_1d(d.productName)]
    for set_i in range(int(d.nSets)):
        truth = np.atleast_1d(d.truthIndividual[set_i])
        prod_idx = np.atleast_1d(d.productIndividual[set_i]).astype(int)
        indiv = np.atleast_2d(d.individual[set_i])
        for j in range(indiv.shape[1]):
            for i in range(indiv.shape[0]):
                pi = int(prod_idx[i]) - 1
                est_rows.append(
                    {
                        "condition": "individual",
                        "stimulus_set": set_i + 1,
                        "trial": i + 1,
                        "participant": j + 1,
                        "product": names[pi] if 0 <= pi < len(names) else "",
                        "estimate": float(indiv[i, j]),
                        "truth": float(truth[i]),
                    }
                )
        primed = np.atleast_2d(d.primedIndividual[set_i])
        for j in range(primed.shape[1]):
            for i in range(primed.shape[0]):
                pi = int(prod_idx[i]) - 1
                est_rows.append(
                    {
                        "condition": "primed_individual",
                        "stimulus_set": set_i + 1,
                        "trial": i + 1,
                        "participant": j + 1,
                        "product": names[pi] if 0 <= pi < len(names) else "",
                        "estimate": float(primed[i, j]),
                        "truth": float(truth[i]),
                    }
                )
    for g in range(int(d.nCooperativeGroups)):
        indiv = np.atleast_2d(d.cooperativeIndividual[g])
        consensus = np.atleast_1d(d.cooperativeConsensus[g])
        truth = np.atleast_1d(d.truthCooperativeGroup[g])
        prod_idx = np.atleast_1d(d.productConsensus[g]).astype(int)
        for j in range(indiv.shape[1]):
            for i in range(indiv.shape[0]):
                pi = int(prod_idx[i]) - 1
                est_rows.append(
                    {
                        "condition": "cooperative_individual",
                        "group": g + 1,
                        "trial": i + 1,
                        "participant": j + 1,
                        "product": names[pi] if 0 <= pi < len(names) else "",
                        "estimate": float(indiv[i, j]),
                        "truth": float(truth[i]),
                        "group_consensus": float(consensus[i]),
                    }
                )
    for g in range(int(d.nCompetitiveGroups)):
        indiv = np.atleast_2d(d.competitiveIndividual[g])
        truth = np.atleast_1d(d.truthCompetitiveGroup[g])
        for j in range(indiv.shape[1]):
            for i in range(indiv.shape[0]):
                val = indiv[i, j]
                if not finite(val):
                    continue
                est_rows.append(
                    {
                        "condition": "competitive_individual",
                        "group": g + 1,
                        "trial": i + 1,
                        "participant": j + 1,
                        "estimate": float(val),
                        "truth": float(truth[i]) if finite(truth[i]) else "",
                    }
                )
    n = write_csv(wout / "estimates.csv", est_rows)

    sheets = read_xlsx(str(BDR / "WisdomOfTheCrowd/LeeSteversMiller2014.xlsx"))
    rout = DATA / "judgment-and-estimation/lee-steyvers-miller-2014-rankings"
    rout.mkdir(parents=True, exist_ok=True)
    n_rank = 0
    for name, table in sheets.items():
        path = rout / f"{to_camel(re.sub(r'[^A-Za-z0-9]+', '_', name).strip('_'))}.csv"
        with path.open("w", newline="") as f:
            w = csv.writer(f)
            w.writerows(table)
        n_rank += max(0, len(table) - 1)
    return {
        "id": "wisdom-of-crowd",
        "n_rows": n + len(df) + n_rank,
        "n_participants": None,
        "extra": f"small_group_estimates={n}; rankings_body_rows~={n_rank}",
    }


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    exporters = [
        export_steyvers_bandit,
        export_lee_zhang_bandit,
        export_guan_battery,
        export_mount_stopping,
        export_stillman,
        export_lee_cummins,
        export_lee_dry,
        export_bergert,
        export_childers,
        export_kannan,
        export_murdock,
        export_number,
        export_tsp,
        export_wisdom,
    ]
    catalog = []
    for fn in exporters:
        info = fn()
        catalog.append(info)
        print(f"OK {info['id']}: rows={info['n_rows']} n={info.get('n_participants')} {info.get('extra','')}")
    for folder in sorted({p.parent for p in DATA.rglob("*.csv")}):
        write_data_mat(folder)
        print(f"OK data.mat {folder.relative_to(ROOT)}")
    print("done")


if __name__ == "__main__":
    main()
