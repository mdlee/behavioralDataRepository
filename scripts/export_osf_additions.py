#!/usr/bin/env python3
"""Export OSF/GitHub additions into existing dataset families."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.io import loadmat

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "datasets"
sys.path.insert(0, str(Path(__file__).resolve().parent))
from io_util import load_local_paths, write_csv, write_data_mat  # noqa: E402
from xlsx_sheets import read_xlsx  # noqa: E402

_src = load_local_paths()
SRC = Path(getattr(_src, "SOURCES", ROOT / "local" / "sources"))


def load_d(path: Path):
    return loadmat(str(path), squeeze_me=True, struct_as_record=False)["d"]


def finite(x) -> bool:
    try:
        return np.isfinite(float(x))
    except (TypeError, ValueError):
        return False


def as_str(x) -> str:
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return ""
    return str(x).strip()


def export_airline() -> dict:
    d = load_d(SRC / "airline/data/cheapAirTicket.mat")
    labels = [as_str(x) for x in np.atleast_1d(d.optionLabs)]
    values = np.atleast_2d(d.values)
    out = DATA / "sequential-choice/lee-chong-2024-airline-tickets"
    env_rows = []
    for i, lab in enumerate(labels):
        env_rows.append(
            {
                "position": i + 1,
                "label": lab,
                "mean": float(d.environment[i, 0]),
                "sd": float(d.environment[i, 1]),
                "optimal_threshold": float(d.optimalThresholds[i]),
            }
        )
    write_csv(out / "positions.csv", env_rows)
    problem_rows = []
    for p in range(int(d.nProblems)):
        rec = {
            "problem": p + 1,
            "min_position": int(d.minChoice[p]),
            "min_price": int(d.minValue[p]),
            "optimal_position": int(d.optChoice[p]),
            "optimal_price": int(d.optValue[p]),
        }
        for t in range(int(d.nPositions)):
            rec[f"value_{t+1}"] = int(values[p, t])
        problem_rows.append(rec)
    write_csv(out / "problem_values.csv", problem_rows)
    trial_rows = []
    for s in range(int(d.nParticipants)):
        for p in range(int(d.nProblems)):
            pos = int(d.decision[s, p])
            rec = {
                "participant": s + 1,
                "problem": p + 1,
                "problem_order": int(d.order[s, p]),
                "choice_position": pos,
                "cost": int(d.decisionValue[s, p]),
            }
            for t in range(int(d.nPositions)):
                rec[f"value_{t+1}"] = int(values[p, t])
            trial_rows.append(rec)
    n = write_csv(out / "trials.csv", trial_rows)
    part_rows = []
    for s in range(int(d.nParticipants)):
        part_rows.append(
            {
                "participant": s + 1,
                "age": int(d.age[s]) if finite(d.age[s]) else "",
                "gender": as_str(d.gender[s]),
            }
        )
    write_csv(out / "participants.csv", part_rows)
    write_data_mat(out)
    return {"id": "lee-chong-2024-airline-tickets", "n_rows": n, "n_participants": int(d.nParticipants)}


def export_mate() -> dict:
    d = load_d(SRC / "mate/MateChoiceApril1st.mat")
    out = DATA / "sequential-choice/lee-courey-2021-mate-selection"
    env_names = [as_str(x) for x in np.atleast_1d(d.environmentNames)]
    ages = [int(x) for x in np.atleast_1d(d.ages)]
    values = np.array(d.values)
    pos_rows = []
    for e, name in enumerate(env_names):
        dist = np.atleast_2d(d.environmentDistributions[e])
        thr = np.atleast_1d(d.optimalThresholds[e])
        for t in range(int(d.nPositions)):
            pos_rows.append(
                {
                    "environment": name,
                    "position": t + 1,
                    "age_label": ages[t],
                    "distribution_mode": float(dist[t, 0]),
                    "distribution_sd": float(dist[t, 1]),
                    "optimal_threshold": float(thr[t]),
                }
            )
    write_csv(out / "positions.csv", pos_rows)
    problem_rows = []
    for e, name in enumerate(env_names):
        for p in range(int(d.nProblems)):
            rec = {
                "environment": name,
                "problem": p + 1,
                "max_position": int(d.maxChoice[p, e]),
                "optimal_position": int(d.optChoice[p, e]),
            }
            for t in range(int(d.nPositions)):
                rec[f"value_{t+1}"] = int(values[p, t, e])
            problem_rows.append(rec)
    write_csv(out / "problem_values.csv", problem_rows)
    trial_rows = []
    for s in range(int(d.nSubjects)):
        for e, name in enumerate(env_names):
            for p in range(int(d.nProblems)):
                ch = d.decision[s, p, e]
                if not finite(ch):
                    continue
                pos = int(ch)
                rec = {
                    "participant": s + 1,
                    "environment": name,
                    "problem": p + 1,
                    "problem_order": int(d.order[s, p, e]),
                    "choice_position": pos,
                    "value": int(values[p, pos - 1, e]),
                }
                for t in range(int(d.nPositions)):
                    rec[f"value_{t+1}"] = int(values[p, t, e])
                trial_rows.append(rec)
    n = write_csv(out / "trials.csv", trial_rows)
    part_rows = []
    for s in range(int(d.nSubjects)):
        part_rows.append(
            {
                "participant": s + 1,
                "gender": int(d.gender[s]),
                "environment_order": int(d.environmentOrder[s]),
            }
        )
    write_csv(out / "participants.csv", part_rows)
    write_data_mat(out)
    n_people = len({r["participant"] for r in trial_rows})
    return {"id": "lee-courey-2021-mate-selection", "n_rows": n, "n_participants": n_people}


def _cue_long(environment: str, item: str, criterion, cue_labs, cue_vals, extra=None):
    rows = []
    for j, lab in enumerate(cue_labs):
        rec = {
            "environment": environment,
            "item": as_str(item),
            "criterion": criterion,
            "cue": as_str(lab),
            "cue_value": int(cue_vals[j]) if finite(cue_vals[j]) else "",
        }
        if extra:
            rec.update(extra)
        rows.append(rec)
    return rows


def export_ttb() -> dict:
    out = DATA / "cue-based-multi-attribute/lee-blanco-bo-2016-take-the-best"
    new = np.atleast_1d(load_d(SRC / "ttb/NewEnvironments.mat"))
    rows = []
    for env in new:
        cues = [as_str(x) for x in np.atleast_1d(env.cueLabs)]
        items = np.atleast_1d(env.itemLabs)
        m = np.atleast_2d(env.m)
        k = np.atleast_1d(env.k)
        for i, item in enumerate(items):
            rows.extend(_cue_long(as_str(env.name), item, float(k[i]), cues, m[i]))
    n_new = write_csv(out / "new_environments.csv", rows)

    xlsx_map = {
        "United States": SRC / "ttb/USCities.xlsx",
        "United Kingdom": SRC / "ttb/UKCities.xlsx",
        "Italy": SRC / "ttb/ItalianCities.xlsx",
        "Germany": SRC / "ttb/GermanCities.xlsx",
    }
    ch_rows = []
    for env_name, path in xlsx_map.items():
        sheets = read_xlsx(str(path))
        for year, table in sheets.items():
            if not table:
                continue
            header = table[0]
            cue_idx = [j for j, h in enumerate(header[2:], start=2) if as_str(h)]
            cue_labs = [as_str(header[j]) for j in cue_idx]
            for row in table[1:]:
                item = as_str(row[0] if row else "")
                if not item:
                    continue
                crit = pd.to_numeric(row[1] if len(row) > 1 else "", errors="coerce")
                cues = [pd.to_numeric(row[j] if j < len(row) else "", errors="coerce") for j in cue_idx]
                ch_rows.extend(
                    _cue_long(
                        env_name,
                        item,
                        float(crit) if pd.notna(crit) else "",
                        cue_labs,
                        cues,
                        extra={"year": int(year) if str(year).isdigit() else year},
                    )
                )
    n_ch = write_csv(out / "changing_environments.csv", ch_rows)
    write_data_mat(out)
    return {
        "id": "lee-blanco-bo-2016-take-the-best",
        "n_rows": n_new + n_ch,
        "n_participants": None,
        "extra": f"new={n_new}; changing={n_ch}",
    }


def export_walsh_gluck() -> dict:
    d = load_d(SRC / "walshgluck/WalshGluck2016Data.mat")
    out = DATA / "cue-based-multi-attribute/lee-gluck-walsh-2019-switching"
    cond_names = [as_str(x).lower() for x in np.atleast_1d(d.conditionNames)]
    report_names = [as_str(x) for x in np.atleast_1d(d.reportNames)]
    n_subj, n_trials, n_cues = int(d.nSubjects), int(d.nTrials), int(d.nCues)
    cue_rows = []
    for c in range(n_cues):
        cue_rows.append(
            {
                "cue": c + 1,
                "validity": float(d.validity[c]),
                "log_odds": float(d.logodds[c]),
            }
        )
    write_csv(out / "cues.csv", cue_rows)
    layout_rows = []
    for s in range(n_subj):
        for alt in range(2):
            for slot in range(n_cues):
                layout_rows.append(
                    {
                        "participant": s + 1,
                        "alternative": alt + 1,
                        "slot": slot + 1,
                        "cue": int(d.layout[slot, alt, s]),
                    }
                )
    write_csv(out / "layouts.csv", layout_rows)
    trial_rows, search_rows, report_rows = [], [], []
    for s in range(n_subj):
        cond = cond_names[int(d.condition[s]) - 1]
        for t in range(n_trials):
            if not finite(d.decision[s, t]):
                continue
            trial_rows.append(
                {
                    "participant": s + 1,
                    "trial": int(d.trial[s, t]),
                    "condition": cond,
                    "decision": int(d.decision[s, t]),
                    "reward": int(d.reward[s, t]),
                    "correct": int(d.correct[s, t]),
                    "trial_start_sec": float(d.startTime[s, t]) if finite(d.startTime[s, t]) else "",
                }
            )
            for alt in range(2):
                for c in range(n_cues):
                    so = d.search[c, alt, s, t]
                    if not finite(so):
                        continue
                    search_rows.append(
                        {
                            "participant": s + 1,
                            "trial": int(d.trial[s, t]),
                            "alternative": alt + 1,
                            "cue": c + 1,
                            "present": int(d.stimulus[c, alt, s, t]),
                            "search_order_within": int(so),
                            "search_order_all": int(d.searchAll[c, alt, s, t])
                            if finite(d.searchAll[c, alt, s, t])
                            else "",
                            "search_time": float(d.searchTime[c, alt, s, t])
                            if finite(d.searchTime[c, alt, s, t])
                            else "",
                        }
                    )
        if s < d.report.shape[0]:
            for t in range(n_trials):
                nrep = int(d.nSubjectReports[s, t]) if finite(d.nSubjectReports[s, t]) else 0
                for k in range(min(nrep, d.report.shape[2])):
                    code = int(d.report[s, t, k])
                    if code <= 0:
                        continue
                    report_rows.append(
                        {
                            "participant": s + 1,
                            "trial": t + 1,
                            "report_index": k + 1,
                            "report": report_names[code - 1] if 0 < code <= len(report_names) else code,
                        }
                    )
    n = write_csv(out / "trials.csv", trial_rows)
    write_csv(out / "searches.csv", search_rows)
    write_csv(out / "reports.csv", report_rows)
    write_data_mat(out)
    return {
        "id": "lee-gluck-walsh-2019-switching",
        "n_rows": n,
        "n_participants": n_subj,
        "extra": f"searches={len(search_rows)}; reports={len(report_rows)}",
    }


def _nback_trials(d, *, participant_ids, n_blocks_field="nBlocks") -> list[dict]:
    dec = np.array(d.decision, dtype=float)
    truth = np.array(d.truth, dtype=float)
    state = np.array(d.state, dtype=float)
    stim = np.array(d.stim, dtype=float)
    face = getattr(d, "face", None)
    rows = []
    n_subj, n_trials, n_blocks = dec.shape
    n_blocks_vec = np.atleast_1d(getattr(d, n_blocks_field))
    for s in range(n_subj):
        pid = participant_ids[s]
        blocks = int(n_blocks_vec[s]) if s < len(n_blocks_vec) and finite(n_blocks_vec[s]) else n_blocks
        for b in range(min(blocks, n_blocks)):
            for t in range(n_trials):
                if not finite(dec[s, t, b]):
                    continue
                rec = {
                    "participant": pid,
                    "block": b + 1,
                    "trial": t + 1,
                    "stimulus": int(stim[s, t, b]) if finite(stim[s, t, b]) else "",
                    "trial_type": int(state[s, t, b]) if finite(state[s, t, b]) else "",
                    "decision": int(dec[s, t, b]),
                    "truth": int(truth[s, t, b]) if finite(truth[s, t, b]) else "",
                }
                if face is not None:
                    rec["face"] = int(face[s, t, b]) if finite(face[s, t, b]) else ""
                rows.append(rec)
    return rows


def export_nback() -> dict:
    out = DATA / "working-memory-recognition/lee-mistry-menon-2022-nback"
    sd = load_d(SRC / "nback/data/StelterDegner2018.mat")
    sd_rows = _nback_trials(sd, participant_ids=list(range(1, int(sd.nSubjects) + 1)))
    n1 = write_csv(out / "stelter_degner.csv", sd_rows)
    hcp = load_d(SRC / "nback/data/humanConnectomeProject.mat")
    n_h = int(hcp.nSubjects)
    hcp_rows = _nback_trials(hcp, participant_ids=list(range(1, n_h + 1)))
    n2 = write_csv(out / "human_connectome.csv", hcp_rows)
    part_rows = []
    for s in range(n_h):
        part_rows.append(
            {
                "participant": s + 1,
                "n_blocks": int(hcp.nBlocks[s]),
                "penn_matrices": float(hcp.pennMatrices[s]) if finite(hcp.pennMatrices[s]) else "",
                "list_sort": float(hcp.listSort[s]) if finite(hcp.listSort[s]) else "",
                "card_sort": float(hcp.cardSort[s]) if finite(hcp.cardSort[s]) else "",
            }
        )
    write_csv(out / "human_connectome_participants.csv", part_rows)
    write_data_mat(out)
    return {
        "id": "lee-mistry-menon-2022-nback",
        "n_rows": n1 + n2,
        "n_participants": int(sd.nSubjects) + n_h,
        "extra": f"stelter={n1} people={int(sd.nSubjects)}; hcp={n2} people={n_h}",
    }


def export_recognition_validity() -> dict:
    src = SRC / "recogval"
    out = DATA / "working-memory-recognition/lee-doering-carr-2019-recognition-validity"
    domains = [
        ("actors", "Actors"),
        ("airplanes", "Airplanes"),
        ("athletes", "Athletes"),
        ("cities", "Cities"),
        ("companies", "Companies"),
        ("hotels", "Hotels"),
        ("marchMadness2016", "MarchMadness2016"),
    ]
    n = 0
    people = set()
    for stem, prefix in domains:
        stim = pd.read_csv(src / f"{prefix}StimulusData.csv", header=None, encoding="latin-1")
        stim_rows = []
        crit = pd.to_numeric(stim[1], errors="coerce")
        for i, row in stim.iterrows():
            stim_rows.append({"item": i + 1, "name": as_str(row[0]), "criterion": crit.iloc[i]})
        write_csv(out / f"{stem}_stimuli.csv", stim_rows)
        beh = pd.read_csv(src / f"{prefix}BehavioralData.csv", header=None)
        varied_choice = set(beh[3].unique()) - {1}
        trial_rows = []
        for _, r in beh.iterrows():
            ia, ib = int(r[1]), int(r[2])
            ca = crit.iloc[ia - 1]
            cb = crit.iloc[ib - 1]
            rec = {
                "participant": int(r[0]),
                "item_a": ia,
                "item_b": ib,
                "recognized_a": int(r[4]),
                "recognized_b": int(r[5]),
                "a_larger": 1 if pd.notna(ca) and pd.notna(cb) and ca > cb else 0,
            }
            if varied_choice:
                if int(r[3]) == 1:
                    rec["choice_a"] = 1
                elif int(r[3]) == 2:
                    rec["choice_a"] = 0
                else:
                    rec["choice_a"] = ""
            trial_rows.append(rec)
            people.add(int(r[0]))
        n += write_csv(out / f"{stem}_trials.csv", trial_rows)
    write_data_mat(out)
    return {
        "id": "lee-doering-carr-2019-recognition-validity",
        "n_rows": n,
        "n_participants": len(people),
        "extra": "participant IDs shared across domains where they overlap",
    }


def export_nfl() -> dict:
    out = DATA / "judgment-and-estimation/montgomery-lee-2021-nfl"
    expert = load_d(SRC / "nfl/expertNFL2017.mat")
    names = [as_str(x) for x in np.atleast_1d(expert.heuristic)]
    e_rows = []
    for h, name in enumerate(names):
        y = np.atleast_1d(expert.y[h])
        truth = np.atleast_1d(expert.truth[h])
        correct = np.atleast_1d(expert.correct[h])
        game = np.atleast_1d(expert.game[h])
        who = np.atleast_1d(expert.expert[h])
        for i in range(len(y)):
            e_rows.append(
                {
                    "heuristic": name,
                    "participant": int(who[i]),
                    "game": int(game[i]),
                    "prediction": int(y[i]),
                    "truth": int(truth[i]),
                    "correct": int(correct[i]),
                }
            )
    n1 = write_csv(out / "expert_predictions.csv", e_rows)
    novice = load_d(SRC / "nfl/noviceNFL2017.mat")
    n_rows = []
    n_names = [as_str(x) for x in np.atleast_1d(novice.heuristic)]
    for h, name in enumerate(n_names):
        y = np.atleast_1d(novice.y[h])
        truth = np.atleast_1d(novice.truth[h])
        correct = np.atleast_1d(novice.correct[h])
        game = np.atleast_1d(novice.game[h])
        who = np.atleast_1d(novice.novice[h])
        n_use = min(len(y), len(who), len(game), len(truth), len(correct))
        for i in range(n_use):
            n_rows.append(
                {
                    "heuristic": name,
                    "participant": int(who[i]),
                    "game": int(game[i]),
                    "prediction": int(y[i]),
                    "truth": int(truth[i]),
                    "correct": int(correct[i]),
                }
            )
    n2 = write_csv(out / "novice_predictions.csv", n_rows)
    write_data_mat(out)
    n_exp = len({r["participant"] for r in e_rows})
    n_nov = len({r["participant"] for r in n_rows})
    return {
        "id": "montgomery-lee-2021-nfl",
        "n_rows": n1 + n2,
        "n_participants": n_exp + n_nov,
        "extra": f"expert_rows={n1} experts={n_exp}; novice_rows={n2} novices={n_nov}",
    }


def export_crowd() -> dict:
    out = DATA / "judgment-and-estimation/lee-lee-2017-crowd-majority"
    files = {
        "afl_games.csv": "AFL games.csv",
        "cancer_diagnosis.csv": "Cancer diagnosis.csv",
        "duration_perception.csv": "Duration perception.csv",
        "esp.csv": "ESP.csv",
        "fantasy_football.csv": "Fantasy football.csv",
        "march_madness.csv": "March Madness.csv",
        "nfl_games.csv": "NFL games.csv",
        "roulette.csv": "Roulette.csv",
        "trivia_questions.csv": "Trivia questions.csv",
    }
    n = 0
    for dest, src_name in files.items():
        df = pd.read_csv(SRC / "crowd" / src_name)
        df.columns = [c.strip() for c in df.columns]
        rows = df.to_dict(orient="records")
        n += write_csv(out / dest, rows)
    write_data_mat(out)
    return {"id": "lee-lee-2017-crowd-majority", "n_rows": n, "n_participants": None}


def export_probability() -> dict:
    out = DATA / "judgment-and-estimation/lee-danileiko-2014-probability-estimates"
    gk = read_xlsx(str(SRC / "probs/GenKnowledgeProbs.xlsx"))["Sheet1"]
    gk_rows = []
    for q, row in enumerate(gk[1:], start=1):
        if not as_str(row[0]):
            continue
        truth = pd.to_numeric(row[1], errors="coerce")
        responses = row[3:]
        for s, val in enumerate(responses, start=1):
            if as_str(val) == "" and s > 145:
                break
            est = pd.to_numeric(val, errors="coerce")
            if pd.isna(est) and as_str(val) == "":
                continue
            gk_rows.append(
                {
                    "participant": s,
                    "question": q,
                    "question_text": as_str(row[0]),
                    "truth": float(truth) if pd.notna(truth) else "",
                    "estimate": float(est) if pd.notna(est) else "",
                }
            )
    n1 = write_csv(out / "general_knowledge.csv", gk_rows)
    soccer = read_xlsx(str(SRC / "probs/SoccerProbs.xlsx"))["Mechanical Turk"]
    sc_rows = []
    for q, row in enumerate(soccer[1:], start=1):
        if not as_str(row[0]):
            continue
        truth = pd.to_numeric(row[1], errors="coerce")
        responses = row[2:]
        for s, val in enumerate(responses, start=1):
            est = pd.to_numeric(val, errors="coerce")
            if pd.isna(est) and as_str(val) == "":
                continue
            sc_rows.append(
                {
                    "participant": s,
                    "question": q,
                    "question_text": as_str(row[0]),
                    "truth": float(truth) if pd.notna(truth) else "",
                    "estimate": float(est) if pd.notna(est) else "",
                }
            )
    n2 = write_csv(out / "soccer.csv", sc_rows)
    write_data_mat(out)
    n_gk = len({r["participant"] for r in gk_rows})
    n_sc = len({r["participant"] for r in sc_rows})
    return {
        "id": "lee-danileiko-2014-probability-estimates",
        "n_rows": n1 + n2,
        "n_participants": n_gk + n_sc,
        "extra": f"general_knowledge={n1} people={n_gk}; soccer={n2} people={n_sc}",
    }


def export_beliefs() -> dict:
    out = DATA / "judgment-and-estimation/lee-ke-thurstonian-beliefs"
    files = {
        "nba_players": "BestNBAPlayers_310423rankOnly.mat",
        "presidents": "BestPresidentsInPast50Years_518292rankOnly.mat",
        "months": "MonthsOfYear_1242079rankOnly.mat",
        "worst_places": "WorstPlacesToLiveInTheUS_935607rankOnly.mat",
    }
    n = 0
    n_people = 0
    for stem, name in files.items():
        d = load_d(SRC / "beliefs/data" / name)
        items = [as_str(x) for x in np.atleast_1d(d.uItem)]
        ranked = np.atleast_2d(np.array(d.ranked, dtype=float))
        write_csv(out / f"{stem}_items.csv", [{"item": i + 1, "name": lab} for i, lab in enumerate(items)])
        rows = []
        for s in range(ranked.shape[0]):
            for i in range(ranked.shape[1]):
                if not finite(ranked[s, i]):
                    continue
                rows.append(
                    {
                        "participant": s + 1,
                        "item": i + 1,
                        "name": items[i],
                        "rank": int(ranked[s, i]),
                    }
                )
        n += write_csv(out / f"{stem}.csv", rows)
        n_people += ranked.shape[0]
    write_data_mat(out)
    return {
        "id": "lee-ke-thurstonian-beliefs",
        "n_rows": n,
        "n_participants": n_people,
        "extra": "participant IDs restart in each domain file",
    }


def main() -> None:
    if not SRC.exists():
        raise SystemExit(f"Missing {SRC} (gitignored source download).")
    for fn in (
        export_airline,
        export_mate,
        export_ttb,
        export_walsh_gluck,
        export_nback,
        export_recognition_validity,
        export_nfl,
        export_crowd,
        export_probability,
        export_beliefs,
    ):
        info = fn()
        print(
            f"OK {info['id']}: rows={info['n_rows']} n={info.get('n_participants')} {info.get('extra', '')}"
        )


if __name__ == "__main__":
    main()
