#!/usr/bin/env python3
"""Export de-identified course judgment tasks.

percentageEstimation, generalKnowledgeEstimation, metaCognition, and ranking.
Anonymous participant IDs match bart / gasPrices / fishPrices when the same
person already has an ID. Student IDs are used only to build that map and are
not written.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from export_bart import (  # noqa: E402
    _assign_global_ids,
    _id_key,
    collect_bart_sessions,
    collect_fish_sessions,
    collect_gas_sessions,
    excel_col,
)
from io_util import load_local_paths, write_csv, write_data_mat  # noqa: E402
from xlsx_sheets import read_xlsx  # noqa: E402

TASKS = load_local_paths().TASKS
DATA = ROOT / "datasets" / "judgment-and-estimation"

PCT_F2025 = [
    ("left handed", 11),
    ("extra rib", 8),
    ("plant life in ocean", 85),
    ("cats asleep", 66),
    ("bones in feet", 25),
    ("Brazil coverage", 50),
    ("women candles", 96),
    ("China toys", 70),
    ("rice staple", 50),
    ("water expands", 9),
    ("carrot fat", 0),
    ("food waste", 27),
    ("oxygen brain", 25),
    ("cucumber water", 96),
    ("jellyfish", 95),
    ("US McDonalds", 7),
    ("countries north equator", 75),
    ("body carbon hydrogen nitrogen", 90),
    ("US land government", 32),
    ("R-rated movies", 55),
    ("body atom replacement", 98),
    ("broken bone", 44),
    ("almond chocolate manufacturers", 40),
    ("US adults sun is star", 45),
    ("lightning men", 80),
]
PCT_W2023 = [
    ("have a household income over $1 million", 0),
    ("are transgender", 1),
    ("have a household income over $500K", 1),
    ("are Muslim", 1),
    ("are Native American", 1),
    ("are Jewish", 2),
    ("live in New York City", 3),
    ("are gay or lesbian", 3),
    ("are atheists", 3),
    ("are bisexual", 4),
    ("are members of a union", 4),
    ("are vegan or vegetarian", 5),
    ("are Asian", 6),
    ("are a military veteran", 6),
    ("live in Texas", 9),
    ("are left handed", 11),
    ("live in California", 12),
    ("are Black", 12),
    ("have an advanced degree", 12),
    ("are first generation immigrants", 14),
    ("are Hispanic", 17),
    ("are Catholic", 22),
    ("own a gun", 32),
    ("have at least a college degree", 33),
    ("have a household income over $100K", 34),
    ("have a passport", 37),
    ("are Democrats", 42),
    ("are obese", 42),
    ("are Republicans", 47),
    ("are married", 51),
    ("have at least one child", 57),
    ("voted in the 2020 election", 62),
    ("have a household income over $50K", 62),
    ("are White", 64),
    ("own a house", 65),
    ("have a pet", 67),
    ("are Christian", 70),
    ("have read a book in the past year", 77),
    ("have a household income over $25K", 82),
    ("have a driver's license", 83),
    ("own a smartphone", 85),
    ("have flown on a plane", 88),
    ("own a car", 88),
    ("have at least a high school degree", 89),
]

GK_F2025_LABELS = [
    "Coachella",
    "In-n-Out",
    "Golden Gate",
    "Harry Potter",
    "Game of Thrones",
    "Avatar",
    "Obamacare",
    "Beyonce Lemonade",
    "Hollywood Sign",
    "Starbucks",
]
GK_F2025_TRUTH = [1999, 1948, 1937, 2001, 2011, 2009, 2010, 2016, 1923, 1971]
GK_F2025_ANCHOR1 = [2010, 1930, 1960, 1985, 2020, 2000, 2015, 2010, 1950, 1950]
GK_F2025_ANCHOR2 = [1980, 1970, 1890, 2020, 2000, 2020, 2005, 2023, 1850, 2003]

GK_W2024_LABELS = [
    "Thriller",
    "Internet",
    "Disneyland",
    "Great Depression",
    "iPhone",
    "Firefox",
    "Youtube",
    "McDonald's",
    "Revolutionary War",
    "Reagan",
    "Pixar",
]
GK_W2024_TRUTH = [1983, 1983, 1955, 1929, 2007, 2004, 2005, 1955, 1775, 1981, 1995]
GK_W2024_ANCHOR1 = [1970, 1990, 1920, 1950, 1990, 2010, 1990, 1980, 1730, 2000, 1990]
GK_W2024_ANCHOR2 = [1990, 1960, 1980, 1910, 2010, 1970, 2010, 1920, 1820, 1960, 2000]

GK_W2023_LABELS = [
    "Irvine population",
    "Harry Potter release",
    "Airplane capacity",
    "George Bush Age",
    "Redwood height",
    "Domino's Sales",
    "Venti latte",
    "Lord of the Rings pages",
    "Celtic titles",
    "Moon distance",
]
GK_W2023_TRUTH = [309031, 1997, 853, 94, 853, 1500000, 4.15, 1178, 17, 50000]
GK_W2023_ANCHOR1 = [1000000, 1980, 5000, 70, 1000, 1000, 8.50, 100, 40, 100]
GK_W2023_ANCHOR2 = [10000, 2010, 100, 100, 100, 10000000, 1.50, 5000, 5, 1000000]
LO_WORDS = {"younger", "shorter", "less", "closer", "fewer", "before"}
HI_WORDS = {"older", "taller", "more", "further", "after", "greater"}

META_TRUTH = [
    2, 2, 1, 1, 2, 1, 2, 2, 2, 1, 1, 1, 2, 1, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2,
    2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 1, 1, 2, 2, 2, 1, 2, 2, 2, 1, 2, 1,
]


def _num(x):
    if x is None or (isinstance(x, float) and pd.isna(x)):
        return None
    s = str(x).strip()
    if s == "" or s.lower() == "nan":
        return None
    try:
        return float(s)
    except ValueError:
        return None


def _qualtrics(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, header=0, skiprows=[1, 2])


def _find_col(columns, *needles: str) -> int | None:
    for i, c in enumerate(columns):
        s = str(c).lower()
        if all(n in s for n in needles):
            return i
    return None


def _existing_id_map() -> dict[str, int]:
    # Gas/fish collectors also rewrite stimulus CSVs. Suppress that while
    # recovering the anonymous-ID map.
    import export_bart as eb

    real = eb.write_csv
    eb.write_csv = lambda *a, **k: 0
    try:
        groups = {
            "bart": collect_bart_sessions(),
            "gas": collect_gas_sessions(),
            "fish": collect_fish_sessions(),
        }
    finally:
        eb.write_csv = real
    _assign_global_ids(groups)
    mapping = {}
    for sl in groups.values():
        for s in sl:
            if s["key"]:
                mapping[s["key"]] = s["participant"]
    return mapping


class IdBook:
    def __init__(self, existing: dict[str, int]):
        self.map = dict(existing)
        self._next = (max(existing.values()) + 1) if existing else 1
        self._pending: dict[str, int] = {}

    def freeze_new(self, keys: list[str | None]) -> None:
        fresh = sorted({k for k in keys if k and k not in self.map and k not in self._pending})
        for k in fresh:
            self._pending[k] = self._next
            self._next += 1
        self.map.update(self._pending)
        self._pending.clear()

    def pid(self, key: str | None) -> int | None:
        if not key:
            return None
        return self.map.get(key)


def _sessionize(rows: list[dict], quarter_key="quarter") -> None:
    seen: dict[tuple, int] = {}
    for r in rows:
        k = (r["participant"], r.get(quarter_key))
        # session assigned per participant within quarter at first row of that person
    # assign on unique (participant, quarter) in appearance order, then stamp
    order = []
    counts: dict[int, int] = {}
    stamped = {}
    for r in rows:
        key = (r["participant"], r.get(quarter_key), r.get("condition", ""))
        if key not in stamped:
            pid = r["participant"]
            counts[pid] = counts.get(pid, 0) + 1
            stamped[key] = counts[pid]
            order.append(key)
        r["session"] = stamped[key]


def _xlsx_rows(path: Path):
    book = read_xlsx(str(path))
    return book["Raw Data"]


def _header_index(header, needle: str) -> int:
    needle = needle.lower()
    for i, c in enumerate(header):
        if needle in str(c).lower():
            return i
    raise KeyError(needle)


def _completed_consented(table, id_i, consent_i):
    out = []
    for r in table[1:]:
        if id_i >= len(r) or consent_i >= len(r):
            continue
        status = str(r[1]).strip() if len(r) > 1 else ""
        if status and status not in ("Completed", "1", "1.0"):
            # QuestionPro uses Completed; allow blank status
            if status not in ("", "Started") and status != "Completed":
                continue
        if status == "Started":
            continue
        if str(r[consent_i]).strip() not in ("1", "1.0"):
            continue
        key = _id_key(r[id_i])
        if not key:
            continue
        out.append((key, r))
    return out


def collect_percentage(book: IdBook) -> list[dict]:
    rows = []
    base = TASKS / "percentageEstimation/data"

    df = _qualtrics(base / "proportion+estimation_January+25,+2023_10.32.csv")
    id_i = excel_col("S")
    q0 = excel_col("T")
    fin = pd.to_numeric(df["Finished"], errors="coerce") == 1
    keys = []
    pending = []
    for _, row in df.loc[fin].iterrows():
        key = _id_key(row.iloc[id_i])
        if not key:
            continue
        vals = [_num(row.iloc[q0 + j]) for j in range(len(PCT_W2023))]
        if any(v is None for v in vals):
            continue
        keys.append(key)
        pending.append((key, vals))
    book.freeze_new(keys)
    for key, vals in pending:
        pid = book.pid(key)
        for j, (lab, truth) in enumerate(PCT_W2023):
            rows.append(
                {
                    "participant": pid,
                    "quarter": "W2023",
                    "condition": "single",
                    "question": j + 1,
                    "questionLabel": lab,
                    "truth": truth,
                    "estimate": vals[j],
                }
            )

    df = _qualtrics(base / "proportion+estimation_W2024_January+25,+2024_16.09.csv")
    consent_i = excel_col("N")
    id_i = _find_col(df.columns, "student") or excel_col("S")
    q0 = excel_col("O")
    keys, pending = [], []
    for _, row in df.iterrows():
        if _num(row.iloc[consent_i]) != 1:
            continue
        key = _id_key(row.iloc[id_i])
        if not key:
            continue
        vals = [_num(row.iloc[q0 + j]) for j in range(len(PCT_F2025))]
        if any(v is None for v in vals):
            continue
        keys.append(key)
        pending.append((key, vals))
    book.freeze_new(keys)
    for key, vals in pending:
        pid = book.pid(key)
        for j, (lab, truth) in enumerate(PCT_F2025):
            rows.append(
                {
                    "participant": pid,
                    "quarter": "W2024",
                    "condition": "single",
                    "question": j + 1,
                    "questionLabel": lab,
                    "truth": truth,
                    "estimate": vals[j],
                }
            )

    for fname, cond in (
        ("percentageEstimationF2025_1.xlsx", "form1"),
        ("percentageEstimationF2025_2.xlsx", "form2"),
    ):
        table = _xlsx_rows(base / fname)
        header = table[0]
        id_i = _header_index(header, "student id")
        consent_i = _header_index(header, "do you give consent")
        q0 = _header_index(header, "left handed")
        people = _completed_consented(table, id_i, consent_i)
        book.freeze_new([k for k, _ in people])
        for key, r in people:
            vals = [_num(r[q0 + j]) if q0 + j < len(r) else None for j in range(len(PCT_F2025))]
            if any(v is None for v in vals):
                continue
            pid = book.pid(key)
            for j, (lab, truth) in enumerate(PCT_F2025):
                rows.append(
                    {
                        "participant": pid,
                        "quarter": "F2025",
                        "condition": cond,
                        "question": j + 1,
                        "questionLabel": lab,
                        "truth": truth,
                        "estimate": vals[j],
                    }
                )
    _sessionize(rows)
    return rows


def _gk_pair_rows(pid, quarter, condition, labels, truth, anchors, hilo, estimates):
    out = []
    for j, lab in enumerate(labels):
        out.append(
            {
                "participant": pid,
                "quarter": quarter,
                "condition": condition,
                "question": j + 1,
                "questionLabel": lab,
                "truth": truth[j],
                "anchor": "" if anchors is None else anchors[j],
                "highOrLow": "" if hilo is None else hilo[j],
                "estimate": estimates[j],
            }
        )
    return out


def _code_hilo(raw):
    if raw is None:
        return ""
    s = str(raw).strip().lower()
    if s in LO_WORDS:
        return 2
    if s in HI_WORDS:
        return 1
    n = _num(raw)
    if n is None:
        return ""
    return int(n) if n == int(n) else n


def collect_gk(book: IdBook) -> list[dict]:
    rows = []
    base = TASKS / "generalKnowledgeEstimation/data"

    specs = [
        (
            "estimationOne_January+25,+2023_10.29.csv",
            "W2023",
            "anchor1",
            GK_W2023_LABELS,
            GK_W2023_TRUTH,
            GK_W2023_ANCHOR1,
            excel_col("T"),
            True,
            10 - 3,
        ),
        (
            "estimationTwo_January+25,+2023_10.30.csv",
            "W2023",
            "anchor2",
            GK_W2023_LABELS,
            GK_W2023_TRUTH,
            GK_W2023_ANCHOR2,
            excel_col("T"),
            True,
            4 - 3,
        ),
    ]
    # MATLAB startRow is 1-indexed into readtable body (file row = startRow+1).
    # After skiprows [1,2], iloc 0 is file row 4. MATLAB startRow 7 means file row 8
    # for the first file (10-3=7 → file row 8). Convert: pandas index = startRow - 3
    # because file row = matlab_start+1 and pandas0 = file row 4, so index = startRow+1-4 = startRow-3.
    for fname, quarter, cond, labels, truth, anchors, q0, paired, start_row in specs:
        df = _qualtrics(base / fname)
        id_i = excel_col("S")
        index0 = start_row - 3
        if index0 < 0:
            index0 = 0
        sub = df.iloc[index0:]
        if "Finished" in sub.columns:
            sub = sub[pd.to_numeric(sub["Finished"], errors="coerce") == 1]
        keys, pending = [], []
        for _, row in sub.iterrows():
            key = _id_key(row.iloc[id_i])
            if not key:
                continue
            hilo, est = [], []
            ok = True
            for j in range(len(labels)):
                if paired:
                    h = _code_hilo(row.iloc[q0 + 2 * j])
                    e = _num(row.iloc[q0 + 2 * j + 1])
                else:
                    h, e = "", _num(row.iloc[q0 + j])
                if e is None:
                    ok = False
                    break
                hilo.append(h)
                est.append(e)
            if not ok:
                continue
            keys.append(key)
            pending.append((key, hilo, est))
        book.freeze_new(keys)
        for key, hilo, est in pending:
            rows.extend(
                _gk_pair_rows(book.pid(key), quarter, cond, labels, truth, anchors, hilo, est)
            )

    w2024 = [
        ("estimationTwo_W2024_January+24,+2024_12.43.csv", "anchor1", GK_W2024_ANCHOR1, True),
        ("estimationThree_W2024_January+24,+2024_12.42.csv", "anchor2", GK_W2024_ANCHOR2, True),
        ("estimationOne_W2024_January+24,+2024_12.42.csv", "noAnchor", None, False),
    ]
    for fname, cond, anchors, paired in w2024:
        df = _qualtrics(base / fname)
        consent_i = excel_col("N")
        id_i = _find_col(df.columns, "student") or excel_col("S")
        q0 = excel_col("O")
        keys, pending = [], []
        for _, row in df.iterrows():
            if _num(row.iloc[consent_i]) != 1:
                continue
            key = _id_key(row.iloc[id_i])
            if not key:
                continue
            hilo, est, ok = [], [], True
            for j in range(len(GK_W2024_LABELS)):
                if paired:
                    h = _code_hilo(row.iloc[q0 + 2 * j])
                    e = _num(row.iloc[q0 + 2 * j + 1])
                else:
                    h, e = "", _num(row.iloc[q0 + j])
                if e is None:
                    ok = False
                    break
                hilo.append(h)
                est.append(e)
            if not ok:
                continue
            keys.append(key)
            pending.append((key, hilo, est))
        book.freeze_new(keys)
        for key, hilo, est in pending:
            rows.extend(
                _gk_pair_rows(
                    book.pid(key),
                    "W2024",
                    cond,
                    GK_W2024_LABELS,
                    GK_W2024_TRUTH,
                    anchors if anchors is not None else [""] * len(GK_W2024_LABELS),
                    hilo if paired else [""] * len(est),
                    est,
                )
            )

    f2025 = [
        ("anchorF2025-anchor1.xlsx", "anchor1", GK_F2025_ANCHOR1, True),
        ("anchorF2025-anchor2.xlsx", "anchor2", GK_F2025_ANCHOR2, True),
        ("anchorF2025-none.xlsx", "noAnchor", None, False),
    ]
    for fname, cond, anchors, paired in f2025:
        table = _xlsx_rows(base / fname)
        header = table[0]
        id_i = _header_index(header, "student id")
        consent_i = _header_index(header, "do you give consent")
        if paired:
            q0 = _header_index(header, "before or after")
        else:
            q0 = _header_index(header, "what year")
        people = _completed_consented(table, id_i, consent_i)
        book.freeze_new([k for k, _ in people])
        for key, r in people:
            hilo, est, ok = [], [], True
            for j in range(len(GK_F2025_LABELS)):
                if paired:
                    h = _code_hilo(r[q0 + 2 * j])
                    e = _num(r[q0 + 2 * j + 1])
                else:
                    h, e = "", _num(r[q0 + j])
                if e is None:
                    ok = False
                    break
                hilo.append(h)
                est.append(e)
            if not ok:
                continue
            rows.extend(
                _gk_pair_rows(
                    book.pid(key),
                    "F2025",
                    cond,
                    GK_F2025_LABELS,
                    GK_F2025_TRUTH,
                    anchors if anchors is not None else [""] * len(GK_F2025_LABELS),
                    hilo,
                    est,
                )
            )
    _sessionize(rows)
    return rows


def collect_meta(book: IdBook) -> list[dict]:
    rows = []
    base = TASKS / "metaCognition/data"

    df = _qualtrics(base / "metaCognition_January+25,+2023_10.30.csv")
    id_i = excel_col("S")
    q0 = excel_col("T")
    # MATLAB startRow = 6 (7-1) on readtable → pandas index 6-3 = 3
    sub = df.iloc[3:]
    if "Finished" in sub.columns:
        sub = sub[pd.to_numeric(sub["Finished"], errors="coerce") == 1]
    keys, pending = [], []
    for _, row in sub.iterrows():
        key = _id_key(row.iloc[id_i])
        if not key:
            continue
        answers, metas, ok = [], [], True
        for j in range(50):
            raw = str(row.iloc[q0 + 2 * j]).strip().lower()
            if raw in ("yes", "true", "1", "1.0"):
                a = 1
            elif raw in ("no", "false", "2", "2.0"):
                a = 2
            else:
                ok = False
                break
            m = _num(row.iloc[q0 + 2 * j + 1])
            answers.append(a)
            metas.append("" if m is None else m)
        if not ok:
            continue
        keys.append(key)
        pending.append((key, answers, metas))
    book.freeze_new(keys)
    for key, answers, metas in pending:
        pid = book.pid(key)
        for j in range(50):
            rows.append(
                {
                    "participant": pid,
                    "quarter": "W2023",
                    "question": j + 1,
                    "truth": META_TRUTH[j],
                    "answer": answers[j],
                    "confidence": metas[j],
                    "correct": int(answers[j] == META_TRUTH[j]),
                }
            )

    df = _qualtrics(base / "metaCognition_W2024_January+22,+2024_16.37.csv")
    consent_i = excel_col("N")
    id_i = _find_col(df.columns, "student") or excel_col("S")
    q0 = excel_col("O")
    keys, pending = [], []
    for _, row in df.iterrows():
        if _num(row.iloc[consent_i]) != 1:
            continue
        key = _id_key(row.iloc[id_i])
        if not key:
            continue
        answers, metas, ok = [], [], True
        for j in range(50):
            a = _num(row.iloc[q0 + 2 * j])
            if a not in (1, 2, 1.0, 2.0):
                ok = False
                break
            answers.append(int(a))
            m = _num(row.iloc[q0 + 2 * j + 1])
            metas.append("" if m is None else m)
        if not ok:
            continue
        keys.append(key)
        pending.append((key, answers, metas))
    book.freeze_new(keys)
    for key, answers, metas in pending:
        pid = book.pid(key)
        for j in range(50):
            rows.append(
                {
                    "participant": pid,
                    "quarter": "W2024",
                    "question": j + 1,
                    "truth": META_TRUTH[j],
                    "answer": answers[j],
                    "confidence": metas[j],
                    "correct": int(answers[j] == META_TRUTH[j]),
                }
            )

    table = _xlsx_rows(base / "metaCognitionF2025.xlsx")
    header = table[0]
    id_i = _header_index(header, "student id")
    consent_i = _header_index(header, "do you give consent")
    q0 = _header_index(header, "state capital")
    labels = []
    for j in range(50):
        lab = str(header[q0 + 2 * j])
        lab = lab.replace("Is ", "").replace(" the state capital of ", ", ").replace("?", "")
        labels.append(lab)
    people = _completed_consented(table, id_i, consent_i)
    book.freeze_new([k for k, _ in people])
    for key, r in people:
        answers, metas, ok = [], [], True
        for j in range(50):
            a = _num(r[q0 + 2 * j])
            if a not in (1, 2, 1.0, 2.0):
                ok = False
                break
            answers.append(int(a))
            m = _num(r[q0 + 2 * j + 1]) if q0 + 2 * j + 1 < len(r) else None
            metas.append("" if m is None else m)
        if not ok:
            continue
        pid = book.pid(key)
        for j in range(50):
            rows.append(
                {
                    "participant": pid,
                    "quarter": "F2025",
                    "question": j + 1,
                    "questionLabel": labels[j],
                    "truth": META_TRUTH[j],
                    "answer": answers[j],
                    "confidence": metas[j],
                    "correct": int(answers[j] == META_TRUTH[j]),
                }
            )
    _sessionize(rows)
    return rows


RANK_TRUTH = {
    "us city": [
        "New York",
        "Los Angeles",
        "Chicago",
        "Houston",
        "Phoenix",
        "Philadelphia",
        "San Antonio",
        "San Diego",
        "Dallas",
        "San Jose",
    ],
    "world city": [
        "Tokyo",
        "Delhi",
        "Shanghai",
        "Sao Paulo",
        "Mexico City",
        "Mumbai",
        "Dhaka",
        "New York",
        "Buenos Aires",
        "Kolkata",
    ],
    "country population": [
        "China",
        "India",
        "United States",
        "Indonesia",
        "Pakistan",
        "Nigeria",
        "Brazil",
        "Bangladesh",
        "Russia",
        "Japan",
    ],
    "european": [
        "London",
        "Berlin",
        "Madrid",
        "Rome",
        "Paris",
        "Bucharest",
        "Hamburg",
        "Warsaw",
        "Budapest",
        "Vienna",
    ],
    "west to east": [
        "Oregon",
        "Utah",
        "Nebraska",
        "Iowa",
        "Alabama",
        "Ohio",
        "Virginia",
        "Delaware",
        "Connecticut",
        "Maine",
    ],
    "landmass": [
        "Russia",
        "Canada",
        "China",
        "United States",
        "Brazil",
        "Australia",
        "India",
        "Argentina",
        "Kazakhstan",
        "Sudan",
    ],
    "river": [
        "Nile",
        "Amazon",
        "Yangtze",
        "Mississippi",
        "Ob-Irtysh",
        "Yenisey-Angara",
        "Yellow River",
        "Congo",
        "Parana",
        "Mekong",
    ],
    "holiday": [
        "New Year",
        "Martin Luther King",
        "Presidents",
        "Memorial",
        "Independence",
        "Labor",
        "Indigenous",
        "Columbus",
        "Halloween",
        "Veterans",
        "Thanksgiving",
    ],
}


def _truth_rank(stimulus: str, item: str):
    s = stimulus.lower()
    for key, order in RANK_TRUTH.items():
        if key in s:
            for i, name in enumerate(order):
                if name.lower() in item.lower() or item.lower() in name.lower():
                    return i + 1
    return ""


def _split_rank_list(cell) -> list[str]:
    s = str(cell).strip()
    if not s or s.lower() == "nan":
        return []
    if "," not in s:
        return []
    return [p.strip() for p in s.split(",") if p.strip()]


def collect_ranking(book: IdBook) -> list[dict]:
    rows = []
    base = TASKS / "ranking/data"
    files = [
        (base / "wisdomOfDiverseCrowd_January+25,+2023_10.27.csv", "W2023"),
        (base / "wisdomOfDiverseCrowd_W2024_January+22,+2024_15.47.csv", "W2024"),
    ]
    for path, quarter in files:
        df = _qualtrics(path)
        id_i = _find_col(df.columns, "student", "id")
        if id_i is None:
            id_i = excel_col("S")
        group_cols = [i for i, c in enumerate(df.columns) if "GROUP" in str(c)]
        if "Finished" in df.columns:
            df = df[pd.to_numeric(df["Finished"], errors="coerce") == 1]
        consent_i = _find_col(df.columns, "consent")
        keys = []
        pending = []
        for _, row in df.iterrows():
            if consent_i is not None and _num(row.iloc[consent_i]) not in (1, 1.0):
                # keep rows when the column exists but is the credit question not 0/1
                val = str(row.iloc[consent_i]).strip()
                if val in ("2", "2.0", "0", "0.0"):
                    continue
            key = _id_key(row.iloc[id_i])
            if not key:
                continue
            sets = []
            for i in group_cols:
                items = _split_rank_list(row.iloc[i])
                if items:
                    sets.append((str(df.columns[i]), items))
            if not sets:
                continue
            keys.append(key)
            pending.append((key, sets))
        book.freeze_new(keys)
        for key, sets in pending:
            pid = book.pid(key)
            for set_name, items in sets:
                for rank, item in enumerate(items, start=1):
                    rows.append(
                        {
                            "participant": pid,
                            "quarter": quarter,
                            "stimulusSet": set_name.replace("_", " "),
                            "item": item,
                            "rank": rank,
                            "truthRank": _truth_rank(set_name, item),
                        }
                    )

    table = _xlsx_rows(base / "rankingF2025.xlsx")
    header, itemrow = table[0], table[1]
    id_i = _header_index(header, "student id")
    consent_i = _header_index(header, "do you give consent")
    # blocks of 10 starting at each "Rank" header
    starts = [i for i, c in enumerate(header) if str(c).lower().startswith("rank")]
    people = _completed_consented(table, id_i, consent_i)
    book.freeze_new([k for k, _ in people])
    for key, r in people:
        pid = book.pid(key)
        for s in starts:
            set_name = str(header[s]).split("Rank")[-1].strip()
            set_name = " ".join(set_name.split())[:80]
            for j in range(10):
                if s + j >= len(itemrow):
                    break
                item = str(itemrow[s + j]).strip()
                if not item:
                    continue
                val = _num(r[s + j]) if s + j < len(r) else None
                if val is None or val <= 0:
                    continue
                rows.append(
                    {
                        "participant": pid,
                        "quarter": "F2025",
                        "stimulusSet": set_name,
                        "item": item,
                        "rank": int(val),
                        "truthRank": _truth_rank(set_name, item),
                    }
                )
    _sessionize(rows)
    return rows


def _summarize(name, rows):
    people = {r["participant"] for r in rows}
    print(f"OK {name}: rows={len(rows)} people={len(people)} quarters={sorted({r['quarter'] for r in rows})}")
    return len(rows), len(people)


def main() -> None:
    book = IdBook(_existing_id_map())
    pct = collect_percentage(book)
    gk = collect_gk(book)
    meta = collect_meta(book)
    rank = collect_ranking(book)
    jobs = [
        ("percentageEstimation", pct),
        ("generalKnowledgeEstimation", gk),
        ("metaCognition", meta),
        ("ranking", rank),
    ]
    # overlap with previously assigned IDs
    old_max_probe = max(_existing_id_map().values())
    for name, rows in jobs:
        out = DATA / name
        n, p = _summarize(name, rows)
        write_csv(out / "trials.csv", rows)
        write_data_mat(out)
        print(f"  wrote {out} n={n} people={p}; existing-id ceiling was {old_max_probe}")


if __name__ == "__main__":
    main()
