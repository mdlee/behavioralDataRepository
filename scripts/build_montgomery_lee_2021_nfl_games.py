"""Game-level recode of Montgomery & Lee (2021) NFL experts.

Writes datasets/wisdom-of-crowds/montgomery-lee-2021-nfl-games/.

The published heuristic files stay in montgomery-lee-2021-nfl/. This
script does not modify that folder. Novices are not written: every
novice team pick in the Montgomery table is already a Lee, Danileiko,
and Vi (2018) trial.

Experts are the 71 commentators retained by parseData_2.m (the bot
"Pickwatch Fan Picks" is left out). Participant numbers match
expertPredictions.csv. option1, option2, and the within-week game
number follow the Danileiko survey for the same week and the same two
teams. gameId is 2017-away@home, the same key as nfl-game-picks-irt.
montgomeryGame is the season-long id in expertPredictions.csv.
"""

import csv
from pathlib import Path

ROOT = Path("/home/mdlee/Dropbox/GitHub/behavioralDataRepository")
OUT = ROOT / "datasets/wisdom-of-crowds/montgomery-lee-2021-nfl-games"
EXPERT_CSV = Path(
    "/home/mdlee/Dropbox/Students/Lauren/LaurenMichaelShare/"
    "mdlHeuristicNFL/heuristicNFL/nfl_data2017.csv"
)
NOVICE_CSV = Path(
    "/home/mdlee/Dropbox/Students/Lauren/LaurenMichaelShare/"
    "mdlHeuristicNFL/heuristicNFL/nfl_novice_data2017.csv"
)
HEURISTIC = (
    ROOT / "datasets/wisdom-of-crowds/montgomery-lee-2021-nfl/expertPredictions.csv"
)
DANILEIKO = (
    ROOT
    / "datasets/wisdom-of-crowds/lee-danileiko-vi-2018-surprisingly-popular-nfl/trials.csv"
)
SCORES = ROOT / "datasets/wisdom-of-crowds/nfl-game-picks-irt/nfl2017-regular-season.csv"

# Order in parseData_2.m. Index + 1 is the participant id in expertPredictions.csv.
EXPERT_LIST = [
    2, 3, 4, 5, 6, 7, 8, 9, 10, 13, 15, 16, 18, 19, 20, 21, 25, 26, 32,
    33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 45, 46, 48, 49, 50, 52, 53,
    55, 56, 57, 58, 60, 62, 63, 65, 69, 71, 72, 73, 74, 75, 76, 77, 78, 80,
    81, 87, 88, 89, 91, 92, 97, 98, 99, 100, 101, 102, 104, 107, 112, 114,
]

# Spelling that does not match either team after case and space cleanup.
# Applied only when the corrected name is one of the two teams in the game.
ALIASES = {
    "new yorks giants": "New York Giants",
    "arizona cardinas": "Arizona Cardinals",
    "arizona carindlas": "Arizona Cardinals",
    "washington football": "Washington Redskins",
    "the washington redskins": "Washington Redskins",
    "seattle sawhawks": "Seattle Seahawks",
    "seattle seahawls": "Seattle Seahawks",
    "bufallo bills": "Buffalo Bills",
}

ABBREV = {
    "Arizona Cardinals": "ARI",
    "Atlanta Falcons": "ATL",
    "Baltimore Ravens": "BAL",
    "Buffalo Bills": "BUF",
    "Carolina Panthers": "CAR",
    "Chicago Bears": "CHI",
    "Cincinnati Bengals": "CIN",
    "Cleveland Browns": "CLE",
    "Dallas Cowboys": "DAL",
    "Denver Broncos": "DEN",
    "Detroit Lions": "DET",
    "Green Bay Packers": "GB",
    "Houston Texans": "HOU",
    "Indianapolis Colts": "IND",
    "Jacksonville Jaguars": "JAX",
    "Kansas City Chiefs": "KC",
    "Los Angeles Chargers": "LAC",
    "Los Angeles Rams": "LAR",
    "Miami Dolphins": "MIA",
    "Minnesota Vikings": "MIN",
    "New England Patriots": "NE",
    "New Orleans Saints": "NO",
    "New York Giants": "NYG",
    "New York Jets": "NYJ",
    "Oakland Raiders": "OAK",
    "Philadelphia Eagles": "PHI",
    "Pittsburgh Steelers": "PIT",
    "San Francisco 49ers": "SF",
    "Seattle Seahawks": "SEA",
    "Tampa Bay Buccaneers": "TB",
    "Tennessee Titans": "TEN",
    "Washington Redskins": "WAS",
}

TRIAL_FIELDS = [
    "participant",
    "week",
    "game",
    "option1",
    "option2",
    "prediction",
    "confidence",
    "meta",
    "truth",
    "correct",
    "gameId",
    "montgomeryGame",
]
PERSON_FIELDS = ["participant", "panel", "season", "name"]


def norm(text):
    return " ".join(text.strip().lower().split())


def resolve_pick(raw, home, away, predhome):
    """Return home or away when the recorded winner names one of them.

    If the winner string names neither team, predhome still decides:
    1 is the source home team and 0 is the source away team. That is how
    the published home-team heuristic codes the pick.
    """
    key = norm(raw)
    hits = [team for team in (home, away) if norm(team) == key]
    if len(hits) == 1:
        return hits[0]
    mapped = ALIASES.get(key)
    if mapped in (home, away):
        return mapped
    if predhome == "1":
        return home
    if predhome == "0":
        return away
    return None


def load_scores():
    """(away abbrev, home abbrev) -> (played week, away score, home score).

    The score file writes Washington as WSH. gameId uses WAS, matching
    nfl-game-picks-irt.
    """
    games = {}
    with SCORES.open(newline="") as handle:
        for row in csv.DictReader(handle):
            away = "WAS" if row["away"] == "WSH" else row["away"]
            home = "WAS" if row["home"] == "WSH" else row["home"]
            key = (away, home)
            if key in games:
                raise ValueError(f"duplicate score row {key}")
            games[key] = (int(row["week"]), int(row["awayScore"]), int(row["homeScore"]))
    return games


def load_danileiko():
    """(week, frozenset of team names) -> (game, option1, option2, truth)."""
    games = {}
    with DANILEIKO.open(newline="") as handle:
        for row in csv.DictReader(handle):
            key = (int(row["week"]), frozenset((row["option1"], row["option2"])))
            info = (int(row["game"]), row["option1"], row["option2"], row["truth"])
            previous = games.get(key)
            if previous is None:
                games[key] = info
            elif previous[:3] != info[:3]:
                raise ValueError(f"Danileiko slot conflict {key}")
    return games


def load_experts():
    rows = []
    with EXPERT_CSV.open(newline="") as handle:
        for row in csv.DictReader(handle):
            if row["personid"] in ("", "NA") or row["weekid"] in ("", "NA"):
                continue
            rows.append(row)
    return rows


def montgomery_game_index(rows):
    """Season-long game id: sorted unique week*100+game, as in parseData_2.m."""
    keys = sorted({int(row["weekid"]) * 100 + int(row["gameid"]) for row in rows})
    return {key: index + 1 for index, key in enumerate(keys)}


def check_novices_are_danileiko():
    """Every Montgomery novice pick is already in the Danileiko trials."""
    danileiko = {}
    with DANILEIKO.open(newline="") as handle:
        for row in csv.DictReader(handle):
            picked = row["option1"] if row["prediction"] == "1" else row["option2"]
            key = (
                int(row["participant"]),
                int(row["week"]),
                frozenset((row["option1"], row["option2"])),
            )
            danileiko[key] = picked
    same = missing = 0
    with NOVICE_CSV.open(newline="") as handle:
        for row in csv.DictReader(handle):
            key = (
                int(row["personid"]),
                int(row["weekid"]),
                frozenset((row["home"], row["away"])),
            )
            if key not in danileiko:
                missing += 1
                continue
            if norm(row["predwinner"]) == norm(danileiko[key]):
                same += 1
            else:
                raise ValueError(f"novice pick differs from Danileiko {key}")
    if same != 25600 or missing != 0:
        raise ValueError(f"novice overlap same={same} missing={missing}")
    return same, len(danileiko)


def check_home_heuristic(trials):
    """Every published home-team row picks the same team as the recode.

    The published truth flag follows the scrape's outcome string. Final
    scores disagree with that string on a few games, so truth and correct
    are not compared here.
    """
    published = {}
    with HEURISTIC.open(newline="") as handle:
        for row in csv.DictReader(handle):
            if row["heuristic"] != "home team":
                continue
            published[(int(row["participant"]), int(row["game"]))] = row["prediction"]
    found = {}
    for trial in trials:
        picked_home = (trial["prediction"] == "1") == trial["option1IsHome"]
        found[(int(trial["participant"]), int(trial["montgomeryGame"]))] = (
            "1" if picked_home else "0"
        )
    missing = set(published) - set(found)
    differ = [
        key
        for key in set(published) & set(found)
        if published[key] != found[key]
    ]
    if missing or differ:
        raise ValueError(
            f"home heuristic mismatch missing={len(missing)} differ={len(differ)}"
        )
    return len(published)


def build():
    if len(EXPERT_LIST) != 71 or len(set(EXPERT_LIST)) != 71:
        raise ValueError("expert list is not the 71 Montgomery experts")
    id_to_participant = {person_id: index + 1 for index, person_id in enumerate(EXPERT_LIST)}
    scores = load_scores()
    danileiko = load_danileiko()
    rows = load_experts()
    game_index = montgomery_game_index(
        [row for row in rows if int(row["personid"]) in id_to_participant]
    )
    if len(game_index) != 256:
        raise ValueError(f"expected 256 games, found {len(game_index)}")

    names = {}
    kept = []
    for row in rows:
        person_id = int(row["personid"])
        if person_id not in id_to_participant:
            continue
        names.setdefault(person_id, row["person"].strip())
        kept.append(row)

    schedule = {}
    for row in kept:
        key = (int(row["weekid"]), frozenset((row["home"], row["away"])))
        schedule.setdefault(key, (row["home"], row["away"], row["outcome"]))

    trials = []
    unmapped = []
    score_disagreements = []
    week_disagreements = []
    truth_vs_danileiko = []
    seen = set()
    for row in kept:
        home = row["home"]
        away = row["away"]
        week = int(row["weekid"])
        pick = resolve_pick(row["predwinner"], home, away, row["predhome"])
        if pick is None:
            unmapped.append(
                {
                    "person": row["person"],
                    "week": week,
                    "sourceGame": row["gameid"],
                    "home": home,
                    "away": away,
                    "predwinner": row["predwinner"],
                }
            )
            continue
        pair = (ABBREV[away], ABBREV[home])
        if pair not in scores:
            flipped = (ABBREV[home], ABBREV[away])
            if flipped not in scores:
                raise KeyError(pair)
            # Source home/away is reversed relative to the final-score file.
            pair = flipped
        played_week, away_score, home_score = scores[pair]
        game_id = f"2017-{pair[0]}@{pair[1]}"
        if played_week != week:
            week_disagreements.append((game_id, week, played_week))
        team_of = {ABBREV[home]: home, ABBREV[away]: away}
        if home_score > away_score:
            winner = team_of[pair[1]]
        elif away_score > home_score:
            winner = team_of[pair[0]]
        else:
            winner = None
        if winner is not None and row["outcome"] != winner:
            score_disagreements.append(
                (game_id, row["outcome"], winner, home_score, away_score)
            )
        survey = danileiko[(week, frozenset((home, away)))]
        game, option1, option2, danileiko_truth = survey
        if pick == option1:
            prediction = "1"
        elif pick == option2:
            prediction = "2"
        else:
            raise ValueError(f"pick {pick} not in {option1} / {option2}")
        if winner is None:
            truth = ""
            correct = ""
        else:
            truth = "1" if winner == option1 else "0"
            correct = "1" if pick == winner else "0"
        if truth != danileiko_truth:
            truth_vs_danileiko.append(
                (f"2017-{pair[0]}@{pair[1]}", week, game, danileiko_truth, truth)
            )
        participant = id_to_participant[int(row["personid"])]
        key = (participant, week, game)
        if key in seen:
            raise ValueError(f"duplicate trial {key}")
        seen.add(key)
        trials.append(
            {
                "participant": str(participant),
                "week": str(week),
                "game": str(game),
                "option1": option1,
                "option2": option2,
                "prediction": prediction,
                "confidence": "",
                "meta": "",
                "truth": truth,
                "correct": correct,
                "gameId": f"2017-{pair[0]}@{pair[1]}",
                "montgomeryGame": str(game_index[week * 100 + int(row["gameid"])]),
                "option1IsHome": option1 == home,
            }
        )

    home_rows = check_home_heuristic(trials)
    novice_same, danileiko_trials = check_novices_are_danileiko()

    people = []
    for person_id in EXPERT_LIST:
        people.append(
            {
                "participant": str(id_to_participant[person_id]),
                "panel": "expert",
                "season": "2017",
                "name": names[person_id],
            }
        )

    trials.sort(key=lambda trial: (int(trial["participant"]), int(trial["week"]), int(trial["game"])))
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / "trials.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=TRIAL_FIELDS, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(trials)
    with (OUT / "participants.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=PERSON_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(people)

    present = {(int(row["personid"]), int(row["weekid"]), int(row["gameid"])) for row in kept}
    schedule_slots = {(int(row["weekid"]), int(row["gameid"])) for row in kept}
    absent_slots = []
    for person_id in EXPERT_LIST:
        for week, source_game in schedule_slots:
            if (person_id, week, source_game) not in present:
                absent_slots.append((id_to_participant[person_id], names[person_id], week, source_game))
    games = {trial["gameId"] for trial in trials}
    bad_correct = 0
    for trial in trials:
        if trial["truth"] == "":
            if trial["correct"] != "":
                bad_correct += 1
            continue
        picked_option1 = trial["prediction"] == "1"
        option1_won = trial["truth"] == "1"
        expect = "1" if picked_option1 == option1_won else "0"
        if trial["correct"] != expect:
            bad_correct += 1
    if bad_correct:
        raise ValueError(f"{bad_correct} trials have correct inconsistent with the pick")
    print("experts", len(people))
    print("source rows for 71", len(kept))
    print("trials", len(trials))
    print("games", len(games))
    print("seasons", {2017})
    print("unmapped", len(unmapped))
    for item in unmapped:
        print("  UNMAPPED", item)
    print("absent person-games", len(absent_slots))
    for item in absent_slots:
        print("  ABSENT", item)
    print("score disagreements", sorted(set(score_disagreements)))
    print("asked vs played week", sorted(set(week_disagreements)))
    print("truth differs from Danileiko", sorted(set(truth_vs_danileiko)))
    print("home heuristic rows matched", home_rows)
    print("novice picks identical to Danileiko", novice_same, "of", danileiko_trials, "Danileiko trials")
    print("blank correct", sum(1 for trial in trials if trial["correct"] == ""))
    print("header", ",".join(TRIAL_FIELDS))
    # Spot-check week 1 Patriots-Chiefs: Chiefs won on the road.
    sample = [
        trial for trial in trials
        if trial["gameId"] == "2017-KC@NE" and trial["participant"] == "1"
    ]
    print("sample 2017-KC@NE participant 1", {k: sample[0][k] for k in TRIAL_FIELDS})


if __name__ == "__main__":
    build()
