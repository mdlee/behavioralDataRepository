"""One commentator id across 2015–2017 NFL pick files.

Reads the per-year ESPN tables in nfl-game-picks-irt and the 2017
Montgomery game rows, then writes datasets/wisdom-of-crowds/expert-nfl-picks/.
Assigns participant by sorting the canonical name. A single-token ESPN
name is replaced with the Montgomery full name only when that surname
is the last token of exactly one person in the 71. Two full names that
share a surname stay two people.

Topic columns are copied from the IRT question rows on gameId.
Does not write Mechanical Turk files or montgomery-lee-2021-nfl/.
"""

import csv
from pathlib import Path

ROOT = Path("/home/mdlee/Dropbox/GitHub/behavioralDataRepository")
IRT = ROOT / "datasets/wisdom-of-crowds/nfl-game-picks-irt"
GAMES = ROOT / "datasets/wisdom-of-crowds/montgomery-lee-2021-nfl-games"
OUT = ROOT / "datasets/wisdom-of-crowds/expert-nfl-picks"
YEARS = (2015, 2016, 2017)
TOPIC_FIELDS = (
    "topicId",
    "topic",
    "divisionTopicId",
    "divisionTopic",
    "conferenceTopicId",
    "conferenceTopic",
    "scopeTopicId",
    "scopeTopic",
    "homeConference",
    "homeDivision",
    "awayConference",
    "awayDivision",
)

# Seasons implied by the ESPN surnames and the 2017 full-name panel.
# Used to fail closed if a surname is merged with the wrong person.
EXPECTED_SEASONS = {
    "Mike Golic": {2015, 2016, 2017},
    "K.C. Joyner": {2015, 2016, 2017},
    "Seth Wickersham": {2015, 2016, 2017},
    "Caplan": {2015, 2016},
    "Hoge": {2015, 2016},
    "Jaworski": {2015, 2016},
    "Matt Bowen": {2016, 2017},
    "Dan Graziano": {2016, 2017},
    "Kevin Seifert": {2016, 2017},
    "Allen": {2015},
    "Carter": {2015},
    "Ditka": {2015},
    "Jackson": {2015},
    "Johnson": {2015},
    "Mortensen": {2015},
    "Schlereth": {2015},
    "Mike Clay": {2017},
    "Lisa Kerney": {2017},
    "Mina Kimes": {2017},
    "Louis Riddick": {2017},
    "Wingo": {2017},
}


def read_csv(path):
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return list(reader), list(reader.fieldnames)


def write_csv(path, fields, rows, line_ending):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fields,
            extrasaction="ignore",
            lineterminator=line_ending,
        )
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fields})


def canonical_espn_name(name, montgomery_names, by_last):
    """Full name when the surname matches one Montgomery person."""
    cleaned = " ".join(name.strip().split())
    if cleaned in montgomery_names:
        return cleaned
    if len(cleaned.split()) != 1:
        return cleaned
    hits = by_last.get(cleaned, [])
    if len(hits) > 1:
        raise ValueError(
            f"{cleaned} matches more than one Montgomery name {hits}; not merging"
        )
    if len(hits) == 1:
        return hits[0]
    return cleaned


def season_label(years):
    return ";".join(str(year) for year in sorted(years))


def correct_from_choice(choice, correct_option):
    if correct_option in ("1", "2") and choice in ("1", "2"):
        return "1" if choice == correct_option else "0"
    return ""


def stabilize_expert_ids():
    espn_people = {}
    espn_trials = {}
    questions = {}
    banks = {}
    for year in YEARS:
        espn_people[year], _ = read_csv(IRT / f"participants-experts-{year}.csv")
        espn_trials[year], trial_fields = read_csv(IRT / f"trials-experts-{year}.csv")
        questions[year], question_fields = read_csv(IRT / f"questions-experts-{year}.csv")
        banks[year], bank_fields = read_csv(IRT / f"itemBank-experts-{year}.csv")
        if [row["gameId"] for row in questions[year]] != [row["gameId"] for row in banks[year]]:
            raise ValueError(f"{year} question and item bank gameIds differ")
        if [row["questionId"] for row in questions[year]] != [row["questionId"] for row in banks[year]]:
            raise ValueError(f"{year} questionIds differ between questions and item bank")

    mont_people, _ = read_csv(GAMES / "participants.csv")
    mont_trials, mont_trial_fields = read_csv(GAMES / "trials.csv")
    montgomery_names = []
    for row in mont_people:
        name = " ".join(row["name"].strip().split())
        if name in montgomery_names:
            raise ValueError(f"duplicate Montgomery name {name}")
        montgomery_names.append(name)
    by_last = {}
    for name in montgomery_names:
        token = name.split()[-1]
        by_last.setdefault(token, []).append(name)

    seasons = {name: set() for name in montgomery_names}
    linked_from = {}
    for year, rows in espn_people.items():
        seen = set()
        for row in rows:
            canonical = canonical_espn_name(row["name"], set(montgomery_names), by_last)
            if canonical in seen:
                raise ValueError(f"{year} has two rows for {canonical}")
            seen.add(canonical)
            seasons.setdefault(canonical, set()).add(year)
            linked_from.setdefault(canonical, row["name"])
    for name in montgomery_names:
        seasons[name].add(2017)

    for name, expected in EXPECTED_SEASONS.items():
        if seasons.get(name) != expected:
            raise ValueError(f"{name} seasons {seasons.get(name)} != {expected}")

    ordered = sorted(seasons, key=str.casefold)
    id_of = {name: str(index) for index, name in enumerate(ordered, start=1)}
    if len(id_of) != 82:
        raise ValueError(f"expected 82 experts, found {len(id_of)}")

    # Per-year ESPN files keep local question ids. Only participant changes,
    # and the stored name becomes the canonical one.
    year_id_map = {}
    for year, rows in espn_people.items():
        for row in rows:
            canonical = canonical_espn_name(row["name"], set(montgomery_names), by_last)
            year_id_map[(year, row["participant"])] = id_of[canonical]
            row["participant"] = id_of[canonical]
            row["name"] = canonical
        rows.sort(key=lambda row: int(row["participant"]))
        for row in espn_trials[year]:
            row["participant"] = year_id_map[(year, row["participant"])]

    qid_of = {}
    next_qid = 1
    combined_questions = []
    combined_bank = []
    for year in YEARS:
        for question, bank in zip(questions[year], banks[year]):
            old = question["questionId"]
            if (year, old) in qid_of:
                raise ValueError(f"duplicate questionId {old} in {year}")
            qid_of[(year, old)] = str(next_qid)
            qid_of[(year, question["gameId"])] = str(next_qid)
            new_question = dict(question)
            new_question["questionId"] = str(next_qid)
            combined_questions.append(new_question)
            new_bank = dict(bank)
            new_bank["questionId"] = str(next_qid)
            combined_bank.append(new_bank)
            next_qid += 1
    if len({row["gameId"] for row in combined_questions}) != len(combined_questions):
        raise ValueError("gameId collision in combined questions")
    if len({row["questionId"] for row in combined_questions}) != len(combined_questions):
        raise ValueError("questionId collision in combined questions")

    question_by_game = {row["gameId"]: row for row in combined_questions if row["season"] == "2017"}
    slot_by_game = {bank["gameId"]: bank["question"] for bank in banks[2017]}
    name_of = {id_of[name]: name for name in ordered}

    def retarget_espn(year, trial):
        row = dict(trial)
        row["questionId"] = qid_of[(year, trial["questionId"])]
        if qid_of[(year, trial["gameId"])] != row["questionId"]:
            raise ValueError(f"{trial['gameId']} questionId does not match gameId")
        return row

    espn_2017 = {}
    for trial in espn_trials[2017]:
        row = retarget_espn(2017, trial)
        key = (row["participant"], row["gameId"])
        if key in espn_2017:
            raise ValueError(f"duplicate ESPN trial {key}")
        espn_2017[key] = row

    # Current Montgomery participant value, whether it is still 1–71 or
    # already the stable id, joins the name. The local 1–71 index is kept
    # in montgomeryParticipant when that column is already present.
    name_by_current = {}
    local_by_name = {}
    for row in mont_people:
        name = " ".join(row["name"].strip().split())
        name_by_current[row["participant"]] = name
        local = row.get("montgomeryParticipant") or row["participant"]
        local_by_name[name] = local
        row["name"] = name
        row["participant"] = id_of[name]
        row["montgomeryParticipant"] = local
        row["panel"] = "expert"
        row["season"] = "2017"

    template_by_game = {}
    for row in espn_2017.values():
        template_by_game.setdefault(row["gameId"], row)

    mont_2017 = {}
    for trial in mont_trials:
        name = name_by_current[trial["participant"]]
        local = trial.get("montgomeryParticipant") or local_by_name[name]
        game_id = trial["gameId"]
        question = question_by_game[game_id]
        choice = trial["prediction"]
        template = template_by_game[game_id]
        row = dict(template)
        row["participant"] = id_of[name]
        row["experiment"] = "2017"
        row["itemBank"] = "season"
        row["design"] = "assigned"
        row["condition"] = "expert"
        row["source"] = "expert"
        row["askedWeek"] = question["askedWeek"]
        row["question"] = slot_by_game[game_id]
        row["questionId"] = question["questionId"]
        row["gameId"] = game_id
        row["answered"] = "1"
        row["choice"] = choice
        row["correct"] = correct_from_choice(choice, question["correctOption"])
        row["confidence"] = ""
        row["meta"] = ""
        key = (row["participant"], game_id)
        if key in mont_2017:
            raise ValueError(f"duplicate Montgomery trial {key}")
        mont_2017[key] = row
        trial["participant"] = id_of[name]
        trial["montgomeryParticipant"] = local

    disagreements = []
    combined_trials = []
    for year in (2015, 2016):
        for trial in espn_trials[year]:
            row = retarget_espn(year, trial)
            row["pickSource"] = "espn"
            combined_trials.append(row)

    for key in sorted(set(espn_2017) | set(mont_2017), key=lambda item: (item[1], int(item[0]))):
        espn_row = espn_2017.get(key)
        mont_row = mont_2017.get(key)
        if espn_row and mont_row:
            if espn_row["choice"] == mont_row["choice"]:
                if espn_row["correct"] != mont_row["correct"]:
                    raise ValueError(f"same pick, different correct on {key}")
                kept = dict(espn_row)
                kept["pickSource"] = "both"
                combined_trials.append(kept)
            else:
                espn_copy = dict(espn_row)
                mont_copy = dict(mont_row)
                espn_copy["pickSource"] = "espn"
                mont_copy["pickSource"] = "montgomery"
                combined_trials.append(espn_copy)
                combined_trials.append(mont_copy)
                disagreements.append(
                    {
                        "participant": key[0],
                        "name": name_of[key[0]],
                        "gameId": key[1],
                        "espnChoice": espn_row["choice"],
                        "montgomeryChoice": mont_row["choice"],
                        "option1": question_by_game[key[1]]["option1"],
                        "option2": question_by_game[key[1]]["option2"],
                        "correctOption": question_by_game[key[1]]["correctOption"],
                    }
                )
        elif espn_row:
            row = dict(espn_row)
            row["pickSource"] = "espn"
            combined_trials.append(row)
        else:
            row = dict(mont_row)
            row["pickSource"] = "montgomery"
            combined_trials.append(row)

    combined_trials.sort(
        key=lambda row: (
            int(row["experiment"]),
            int(row["questionId"]),
            int(row["participant"]),
            row["pickSource"],
        )
    )

    question_for_game = {row["gameId"]: row for row in combined_questions}
    for row in combined_trials:
        question = question_for_game[row["gameId"]]
        for field in TOPIC_FIELDS:
            if field in row and row[field] != question[field]:
                raise ValueError(
                    f"{row['gameId']} {field} is {row[field]!r} on the trial and {question[field]!r} on the question"
                )
            row[field] = question[field]

    people_rows = []
    for name in ordered:
        years = seasons[name]
        label = season_label(years)
        people_rows.append(
            {
                "participant": id_of[name],
                "name": name,
                "season2015": "1" if 2015 in years else "0",
                "season2016": "1" if 2016 in years else "0",
                "season2017": "1" if 2017 in years else "0",
                "seasons": label,
            }
        )

    person_fields = [
        "participant",
        "name",
        "season2015",
        "season2016",
        "season2017",
        "seasons",
    ]
    combined_trial_fields = []
    for field in trial_fields:
        combined_trial_fields.append(field)
        if field == "scopeTopic":
            combined_trial_fields.extend(
                ["homeConference", "homeDivision", "awayConference", "awayDivision"]
            )
    combined_trial_fields.append("pickSource")
    OUT.mkdir(parents=True, exist_ok=True)
    write_csv(OUT / "participants.csv", person_fields, people_rows, "\n")
    write_csv(OUT / "trials.csv", combined_trial_fields, combined_trials, "\n")
    write_csv(OUT / "questions.csv", question_fields, combined_questions, "\n")
    write_csv(OUT / "itemBank.csv", bank_fields, combined_bank, "\n")

    by_year = {year: 0 for year in YEARS}
    sources = {}
    for row in combined_trials:
        by_year[int(row["experiment"])] += 1
        sources[row["pickSource"]] = sources.get(row["pickSource"], 0) + 1
    if by_year != {2015: 3328, 2016: 2304, 2017: 18423}:
        raise ValueError(f"unexpected trials by year {by_year}")
    if len(combined_trials) != 24055:
        raise ValueError(f"unexpected trial count {len(combined_trials)}")
    if len(disagreements) != 8:
        raise ValueError(f"expected 8 disagreements, found {len(disagreements)}")
    paired = {(row["participant"], row["gameId"]) for row in combined_trials}
    # Disagreements are the only person-game with two rows.
    if len(combined_trials) - len(paired) != len(disagreements):
        raise ValueError("person-game duplicates are not exactly the disagreements")

    multi = [
        (int(id_of[name]), name, season_label(seasons[name]))
        for name in ordered
        if len(seasons[name]) > 1
    ]
    return {
        "nExperts": len(ordered),
        "ids": [(int(id_of[name]), name, season_label(seasons[name])) for name in ordered],
        "multiYear": multi,
        "trialsByYear": by_year,
        "pickSource": sources,
        "disagreements": disagreements,
        "nQuestions": len(combined_questions),
    }


if __name__ == "__main__":
    summary = stabilize_expert_ids()
    print("experts", summary["nExperts"])
    print("trials", summary["trialsByYear"], "sources", summary["pickSource"])
    print("questions", summary["nQuestions"])
    print("multi-year")
    for row in summary["multiYear"]:
        print(f"  {row[0]}\t{row[1]}\t{row[2]}")
    print("disagreements")
    for row in summary["disagreements"]:
        print(
            f"  {row['participant']} {row['name']} {row['gameId']} "
            f"espn={row['espnChoice']} montgomery={row['montgomeryChoice']} "
            f"option1={row['option1']} option2={row['option2']} correct={row['correctOption']}"
        )
