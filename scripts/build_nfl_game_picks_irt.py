"""Bennett-style IRT tables for 2017 Mechanical Turk NFL winner picks.

Writes the novice panel under datasets/wisdom-of-crowds/nfl-game-picks-irt/.
Commentators are not written here. They are in
datasets/wisdom-of-crowds/expert-nfl-picks/.

A gameId is the season plus away@home. The same 2017 game has the same
gameId here and in the commentator file, including the Dolphins–Buccaneers
game that was asked in week 1 and played in week 11.
"""

import csv
from collections import defaultdict
from pathlib import Path

import numpy as np
import scipy.io

ROOT = Path("/home/mdlee/Dropbox/GitHub/behavioralDataRepository")
OUT = ROOT / "datasets/wisdom-of-crowds/nfl-game-picks-irt"
ESPN_DIR = Path("/home/mdlee/Dropbox/Students/Lauren/LaurenMichaelShare/NFLPredictions")
MTURK_TRIALS = (
    ROOT
    / "datasets/wisdom-of-crowds/lee-danileiko-vi-2018-surprisingly-popular-nfl/trials.csv"
)
MTURK_PEOPLE = (
    ROOT
    / "datasets/wisdom-of-crowds/lee-danileiko-vi-2018-surprisingly-popular-nfl/participants.csv"
)

# Conference, division. Stable across 2015–2017.
DIVISION = {
    "Patriots": ("AFC", "East"),
    "Jets": ("AFC", "East"),
    "Bills": ("AFC", "East"),
    "Dolphins": ("AFC", "East"),
    "Bengals": ("AFC", "North"),
    "Steelers": ("AFC", "North"),
    "Ravens": ("AFC", "North"),
    "Browns": ("AFC", "North"),
    "Colts": ("AFC", "South"),
    "Titans": ("AFC", "South"),
    "Jaguars": ("AFC", "South"),
    "Texans": ("AFC", "South"),
    "Broncos": ("AFC", "West"),
    "Raiders": ("AFC", "West"),
    "Chargers": ("AFC", "West"),
    "Chiefs": ("AFC", "West"),
    "Redskins": ("NFC", "East"),
    "Cowboys": ("NFC", "East"),
    "Giants": ("NFC", "East"),
    "Eagles": ("NFC", "East"),
    "Packers": ("NFC", "North"),
    "Vikings": ("NFC", "North"),
    "Bears": ("NFC", "North"),
    "Lions": ("NFC", "North"),
    "Falcons": ("NFC", "South"),
    "Panthers": ("NFC", "South"),
    "Saints": ("NFC", "South"),
    "Buccaneers": ("NFC", "South"),
    "Cardinals": ("NFC", "West"),
    "Seahawks": ("NFC", "West"),
    "Rams": ("NFC", "West"),
    "49ers": ("NFC", "West"),
}

ABBREV = {
    "Patriots": "NE",
    "Jets": "NYJ",
    "Bills": "BUF",
    "Dolphins": "MIA",
    "Bengals": "CIN",
    "Steelers": "PIT",
    "Ravens": "BAL",
    "Browns": "CLE",
    "Colts": "IND",
    "Titans": "TEN",
    "Jaguars": "JAX",
    "Texans": "HOU",
    "Broncos": "DEN",
    "Raiders": "OAK",
    "Chargers": "LAC",
    "Chiefs": "KC",
    "Redskins": "WAS",
    "Cowboys": "DAL",
    "Giants": "NYG",
    "Eagles": "PHI",
    "Packers": "GB",
    "Vikings": "MIN",
    "Bears": "CHI",
    "Lions": "DET",
    "Falcons": "ATL",
    "Panthers": "CAR",
    "Saints": "NO",
    "Buccaneers": "TB",
    "Cardinals": "ARI",
    "Seahawks": "SEA",
    "Rams": "LAR",
    "49ers": "SF",
}

FULL = {
    "Patriots": "New England Patriots",
    "Jets": "New York Jets",
    "Bills": "Buffalo Bills",
    "Dolphins": "Miami Dolphins",
    "Bengals": "Cincinnati Bengals",
    "Steelers": "Pittsburgh Steelers",
    "Ravens": "Baltimore Ravens",
    "Browns": "Cleveland Browns",
    "Colts": "Indianapolis Colts",
    "Titans": "Tennessee Titans",
    "Jaguars": "Jacksonville Jaguars",
    "Texans": "Houston Texans",
    "Broncos": "Denver Broncos",
    "Raiders": "Oakland Raiders",
    "Chiefs": "Kansas City Chiefs",
    "Redskins": "Washington Redskins",
    "Cowboys": "Dallas Cowboys",
    "Giants": "New York Giants",
    "Eagles": "Philadelphia Eagles",
    "Packers": "Green Bay Packers",
    "Vikings": "Minnesota Vikings",
    "Bears": "Chicago Bears",
    "Lions": "Detroit Lions",
    "Falcons": "Atlanta Falcons",
    "Panthers": "Carolina Panthers",
    "Saints": "New Orleans Saints",
    "Buccaneers": "Tampa Bay Buccaneers",
    "Cardinals": "Arizona Cardinals",
    "Seahawks": "Seattle Seahawks",
    "49ers": "San Francisco 49ers",
}

SHORT_FROM_FULL = {v: k for k, v in FULL.items()}
SHORT_FROM_FULL["Los Angeles Chargers"] = "Chargers"
SHORT_FROM_FULL["San Diego Chargers"] = "Chargers"
SHORT_FROM_FULL["Los Angeles Rams"] = "Rams"
SHORT_FROM_FULL["St. Louis Rams"] = "Rams"

TOPIC_ID = {
    "AFC East": 1,
    "AFC North": 2,
    "AFC South": 3,
    "AFC West": 4,
    "NFC East": 5,
    "NFC North": 6,
    "NFC South": 7,
    "NFC West": 8,
    "AFC": 9,
    "NFC": 10,
    "Interconference": 11,
}
DIVISION_TOPIC_ID = {
    "AFC East": 1,
    "AFC North": 2,
    "AFC South": 3,
    "AFC West": 4,
    "NFC East": 5,
    "NFC North": 6,
    "NFC South": 7,
    "NFC West": 8,
    "Cross-division": 9,
}
CONFERENCE_TOPIC_ID = {"AFC": 1, "NFC": 2, "Interconference": 3}
SCOPE_TOPIC_ID = {"Divisional": 1, "Conference": 2, "Interconference": 3}

QUESTION_FIELDS = [
    "questionId",
    "gameId",
    "season",
    "askedWeek",
    "playedWeek",
    "topicId",
    "topic",
    "divisionTopicId",
    "divisionTopic",
    "conferenceTopicId",
    "conferenceTopic",
    "scopeTopicId",
    "scopeTopic",
    "questionText",
    "option1",
    "option2",
    "correctOption",
    "homeTeam",
    "awayTeam",
    "homeConference",
    "homeDivision",
    "awayConference",
    "awayDivision",
    "homeWins",
    "homeLosses",
    "awayWins",
    "awayLosses",
    "tie",
]
TRIAL_FIELDS = [
    "participant",
    "experiment",
    "itemBank",
    "design",
    "condition",
    "source",
    "askedWeek",
    "question",
    "questionId",
    "gameId",
    "topicId",
    "topic",
    "divisionTopicId",
    "divisionTopic",
    "conferenceTopicId",
    "conferenceTopic",
    "scopeTopicId",
    "scopeTopic",
    "answered",
    "choice",
    "correct",
    "confidence",
    "meta",
]
PERSON_FIELDS = [
    "participant",
    "experiment",
    "itemBank",
    "design",
    "condition",
    "source",
    "name",
    "askedWeek",
    "knowledge",
]
BANK_FIELDS = [
    "itemBank",
    "question",
    "questionId",
    "gameId",
    "topicId",
    "topic",
]


def full_name(short, season):
    if short == "Rams":
        return "St. Louis Rams" if season == 2015 else "Los Angeles Rams"
    if short == "Chargers":
        return "San Diego Chargers" if season < 2017 else "Los Angeles Chargers"
    return FULL[short]


def division_label(short):
    conference, division = DIVISION[short]
    return conference, f"{conference} {division}"


def topic_fields(home, away):
    home_conf, home_div = division_label(home)
    away_conf, away_div = division_label(away)
    if home_div == away_div:
        division_topic = home_div
        scope = "Divisional"
    else:
        division_topic = "Cross-division"
        scope = None
    if home_conf == away_conf:
        conference_topic = home_conf
        if scope is None:
            scope = "Conference"
    else:
        conference_topic = "Interconference"
        scope = "Interconference"
    # Divisional games keep the division name. Other games use the conference
    # matchup, so one topic column carries both kinds of expertise.
    topic = division_topic if scope == "Divisional" else conference_topic
    return {
        "topicId": TOPIC_ID[topic],
        "topic": topic,
        "divisionTopicId": DIVISION_TOPIC_ID[division_topic],
        "divisionTopic": division_topic,
        "conferenceTopicId": CONFERENCE_TOPIC_ID[conference_topic],
        "conferenceTopic": conference_topic,
        "scopeTopicId": SCOPE_TOPIC_ID[scope],
        "scopeTopic": scope,
        "homeConference": home_conf,
        "homeDivision": home_div,
        "awayConference": away_conf,
        "awayDivision": away_div,
    }


def game_id(season, away, home):
    return f"{season}-{ABBREV[away]}@{ABBREV[home]}"


def blank(value):
    return "" if value is None else str(value)


def write_csv(path, fields, rows):
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: blank(row.get(key)) for key in fields})


def entering_record(win):
    """Wins and losses before each week. win is (team, week) with 1, 0, or nan."""
    n_teams, n_weeks = win.shape
    wins = np.zeros((n_teams, n_weeks), dtype=int)
    losses = np.zeros((n_teams, n_weeks), dtype=int)
    for week in range(1, n_weeks):
        prior = win[:, :week]
        wins[:, week] = np.nansum(prior == 1, axis=1)
        losses[:, week] = np.nansum(prior == 0, axis=1)
    return wins, losses


def corrected_results(win, game, scores, win_home, n_games):
    """Winner from winHome, not the point total.

    Five 2017 49ers home games store the home score as 49, and the win
    vector marks both teams as losing. winHome still says the home team
    lost. Ties (equal scores) are neither a win nor a loss; the source
    win vector had counted each tie as a loss for both teams.
    """
    corrected = np.array(win, dtype=float, copy=True)
    for week, n_week in enumerate(n_games):
        for slot in range(n_week):
            away_i = int(game[week, slot, 0]) - 1
            home_i = int(game[week, slot, 1]) - 1
            away_score = float(scores[week, slot, 0])
            home_score = float(scores[week, slot, 1])
            home_won = float(win_home[week, slot])
            if away_score == home_score:
                corrected[away_i, week] = np.nan
                corrected[home_i, week] = np.nan
            elif home_won == 1:
                corrected[home_i, week] = 1
                corrected[away_i, week] = 0
            elif home_won == 0:
                corrected[home_i, week] = 0
                corrected[away_i, week] = 1
            else:
                raise ValueError(f"winHome {home_won} at week {week + 1} slot {slot + 1}")
    return corrected


def official_2017():
    """Final 2017 regular-season scores. The expert MATLAB file stores 49 as the
    49ers' points in every 49ers game, so winners for that season come from here.
    """
    path = OUT / "nfl2017-regular-season.csv"
    short_from_espn = {abbr: name for name, abbr in ABBREV.items()}
    short_from_espn["WSH"] = "Redskins"
    games = []
    with path.open() as handle:
        for row in csv.DictReader(handle):
            games.append(
                {
                    "playedWeek": int(row["week"]),
                    "away": short_from_espn[row["away"]],
                    "home": short_from_espn[row["home"]],
                    "awayScore": int(row["awayScore"]),
                    "homeScore": int(row["homeScore"]),
                }
            )
    return games


def entering_from_results(results, week):
    wins = defaultdict(int)
    losses = defaultdict(int)
    for game in results:
        if game["playedWeek"] >= week:
            continue
        if game["homeScore"] == game["awayScore"]:
            continue
        if game["homeScore"] > game["awayScore"]:
            wins[game["home"]] += 1
            losses[game["away"]] += 1
        else:
            wins[game["away"]] += 1
            losses[game["home"]] += 1
    return wins, losses


def load_espn(season):
    path = ESPN_DIR / f"Data_NFL{season}.mat"
    data = scipy.io.loadmat(path, squeeze_me=True, struct_as_record=False)["d"]
    shorts = [str(name) for name in np.atleast_1d(data.shortTeamNames)]
    if season == 2017:
        names = [str(name) for name in np.atleast_1d(data.espnExpertNames)]
        game = data.games
        picks = data.picks
    else:
        names = [str(name) for name in np.atleast_1d(data.expertNames)]
        game = data.game
        picks = data.expertPick
    expert_index = [i for i, name in enumerate(names) if name != "Pick'em"]
    experts = [names[i] for i in expert_index]
    n_games = [int(n) for n in np.atleast_1d(data.nGames)]
    official = official_2017() if season == 2017 else None
    official_by_pair = {(row["away"], row["home"]): row for row in official} if official else {}
    if season == 2017:
        wins_by_week = {week: entering_from_results(official, week) for week in range(1, 18)}
    else:
        win = corrected_results(data.win, game, data.scores, data.winHome, n_games)
        win_before, loss_before = entering_record(win)
    games = []
    for week, n_week in enumerate(n_games, start=1):
        for slot in range(1, n_week + 1):
            away_i = int(game[week - 1, slot - 1, 0]) - 1
            home_i = int(game[week - 1, slot - 1, 1]) - 1
            away = shorts[away_i]
            home = shorts[home_i]
            away_score = float(data.scores[week - 1, slot - 1, 0])
            home_score = float(data.scores[week - 1, slot - 1, 1])
            home_won = float(data.winHome[week - 1, slot - 1])
            played_week = week
            if season == 2017:
                official_game = official_by_pair[(away, home)]
                played_week = official_game["playedWeek"]
                if official_game["homeScore"] > official_game["awayScore"]:
                    correct_option = 1
                    tie = 0
                elif official_game["awayScore"] > official_game["homeScore"]:
                    correct_option = 2
                    tie = 0
                else:
                    correct_option = None
                    tie = 1
                week_wins, week_losses = wins_by_week[week]
                home_wins = week_wins[home]
                home_losses = week_losses[home]
                away_wins = week_wins[away]
                away_losses = week_losses[away]
            else:
                if away_score == home_score:
                    correct_option = None
                    tie = 1
                elif home_won == 1:
                    correct_option = 1
                    tie = 0
                elif home_won == 0:
                    correct_option = 2
                    tie = 0
                else:
                    raise ValueError(f"{season} week {week} slot {slot} winHome {home_won}")
                home_wins = int(win_before[home_i, week - 1])
                home_losses = int(loss_before[home_i, week - 1])
                away_wins = int(win_before[away_i, week - 1])
                away_losses = int(loss_before[away_i, week - 1])
            expert_choice = {}
            for name, index in zip(experts, expert_index):
                picked = int(picks[week - 1, slot - 1, index]) - 1
                if picked == home_i:
                    expert_choice[name] = 1
                elif picked == away_i:
                    expert_choice[name] = 2
                else:
                    raise ValueError(f"{season} W{week} {name} picked a team not in the game")
            games.append(
                {
                    "season": season,
                    "askedWeek": week,
                    "playedWeek": played_week,
                    "slot": slot,
                    "home": home,
                    "away": away,
                    "homeIndex": home_i,
                    "awayIndex": away_i,
                    "correctOption": correct_option,
                    "tie": tie,
                    "homeWins": home_wins,
                    "homeLosses": home_losses,
                    "awayWins": away_wins,
                    "awayLosses": away_losses,
                    "expertChoice": expert_choice,
                }
            )
    return experts, games


def question_row(question_id, game):
    season = game["season"]
    home = game["home"]
    away = game["away"]
    home_name = full_name(home, season)
    away_name = full_name(away, season)
    topics = topic_fields(home, away)
    row = {
        "questionId": question_id,
        "gameId": game_id(season, away, home),
        "season": season,
        "askedWeek": game["askedWeek"],
        "playedWeek": game["playedWeek"],
        "questionText": f"Which team will win? {home_name} (home) or {away_name} (away)?",
        "option1": home_name,
        "option2": away_name,
        "correctOption": game["correctOption"],
        "homeTeam": home_name,
        "awayTeam": away_name,
        "homeWins": game["homeWins"],
        "homeLosses": game["homeLosses"],
        "awayWins": game["awayWins"],
        "awayLosses": game["awayLosses"],
        "tie": game["tie"],
    }
    row.update(topics)
    return row


def trial_from_choice(person, game_row, choice, confidence, meta):
    correct = ""
    if game_row["correctOption"] in (1, 2) and choice in (1, 2):
        correct = 1 if choice == game_row["correctOption"] else 0
    week = game_row["askedWeek"]
    source = person["source"]
    item_bank = f"week{int(week):02d}" if source == "participant" else "season"
    return {
        "participant": person["participant"],
        "experiment": person["experiment"],
        "itemBank": item_bank,
        "design": "assigned",
        "condition": source,
        "source": source,
        "askedWeek": week,
        "question": game_row["question"],
        "questionId": game_row["questionId"],
        "gameId": game_row["gameId"],
        "topicId": game_row["topicId"],
        "topic": game_row["topic"],
        "divisionTopicId": game_row["divisionTopicId"],
        "divisionTopic": game_row["divisionTopic"],
        "conferenceTopicId": game_row["conferenceTopicId"],
        "conferenceTopic": game_row["conferenceTopic"],
        "scopeTopicId": game_row["scopeTopicId"],
        "scopeTopic": game_row["scopeTopic"],
        "answered": 1 if choice in (1, 2) else 0,
        "choice": choice if choice in (1, 2) else "",
        "correct": correct,
        "confidence": confidence,
        "meta": meta,
    }


def bank_rows(questions, source):
    rows = []
    for question in questions:
        week = question["askedWeek"]
        item_bank = f"week{int(week):02d}" if source == "participant" else "season"
        rows.append(
            {
                "itemBank": item_bank,
                "question": question["question"],
                "questionId": question["questionId"],
                "gameId": question["gameId"],
                "topicId": question["topicId"],
                "topic": question["topic"],
            }
        )
    return rows


def export_experts(season, experts, games):
    questions = []
    by_week_slot = {}
    for question_id, game in enumerate(games, start=1):
        row = question_row(question_id, game)
        row["question"] = game["slot"]
        row["source"] = "expert"
        questions.append(row)
        by_week_slot[(game["askedWeek"], game["slot"])] = row
    people = []
    for participant, name in enumerate(experts, start=1):
        people.append(
            {
                "participant": participant,
                "experiment": str(season),
                "itemBank": "season",
                "design": "assigned",
                "condition": "expert",
                "source": "expert",
                "name": name,
                "askedWeek": "",
                "knowledge": "",
            }
        )
    name_to_id = {person["name"]: person["participant"] for person in people}
    trials = []
    for game, question in zip(games, questions):
        for name, choice in game["expertChoice"].items():
            person = {
                "participant": name_to_id[name],
                "experiment": str(season),
                "source": "expert",
            }
            trials.append(trial_from_choice(person, question, choice, "", ""))
    # Commentator rows are published in expert-nfl-picks/, not as per-year files here.
    return questions, trials, people


def load_mturk_rows():
    with MTURK_TRIALS.open() as handle:
        trials = list(csv.DictReader(handle))
    with MTURK_PEOPLE.open() as handle:
        people = list(csv.DictReader(handle))
    return trials, people


def match_mturk_game(asked_week, option1, option2, espn_games):
    short1 = SHORT_FROM_FULL[option1]
    short2 = SHORT_FROM_FULL[option2]
    same_week = [
        game
        for game in espn_games
        if game["askedWeek"] == asked_week and {game["home"], game["away"]} == {short1, short2}
    ]
    if len(same_week) == 1:
        return same_week[0], "same-week"
    if len(same_week) > 1:
        raise ValueError(f"Two ESPN games for {option1} vs {option2} in week {asked_week}")
    any_week = [
        game for game in espn_games if {game["home"], game["away"]} == {short1, short2}
    ]
    if len(any_week) == 1:
        return any_week[0], "rescheduled"
    raise ValueError(
        f"No unique ESPN game for week {asked_week} {option1} vs {option2} ({len(any_week)} season matches)"
    )


def export_participants(espn_2017):
    raw_trials, raw_people = load_mturk_rows()
    slate = {}
    for row in raw_trials:
        key = (int(row["week"]), int(row["game"]))
        slate.setdefault(key, (row["option1"], row["option2"], row["truth"]))
    questions_by_key = {}
    rescheduled = []
    for key in sorted(slate):
        asked_week, slot = key
        option1, option2, truth = slate[key]
        espn, how = match_mturk_game(asked_week, option1, option2, espn_2017)
        if how == "rescheduled":
            rescheduled.append((asked_week, espn["playedWeek"], option1, option2, espn["home"], espn["away"]))
        game = dict(espn)
        game["askedWeek"] = asked_week
        game["season"] = 2017
        if asked_week != game["playedWeek"]:
            week_wins, week_losses = entering_from_results(official_2017(), asked_week)
            game["homeWins"] = week_wins[game["home"]]
            game["homeLosses"] = week_losses[game["home"]]
            game["awayWins"] = week_wins[game["away"]]
            game["awayLosses"] = week_losses[game["away"]]
        questions_by_key[key] = game
        if truth != "":
            mturk_home_won = truth == "1"
            # truth is coded for the survey order, which is checked below
            survey_correct = 1 if mturk_home_won else 2
            # Hold the survey coding; real correctOption comes from ESPN scores.
            game["surveyCorrectOption"] = survey_correct
            game["surveyOption1"] = option1
        else:
            game["surveyCorrectOption"] = None
            game["surveyOption1"] = option1

    questions = []
    winner_disagreements = []
    for question_id, key in enumerate(sorted(questions_by_key), start=1):
        game = questions_by_key[key]
        row = question_row(question_id, game)
        row["question"] = key[1]
        row["source"] = "participant"
        # Survey option 1 should be the home team. Check, do not assume later.
        if full_name(game["home"], 2017) != game["surveyOption1"]:
            raise ValueError(
                f"Week {game['askedWeek']} game {key[1]}: survey option1 is {game['surveyOption1']}, ESPN home is {full_name(game['home'], 2017)}"
            )
        if game["surveyCorrectOption"] is not None and game["correctOption"] != game["surveyCorrectOption"]:
            winner_disagreements.append(
                (row["gameId"], row["askedWeek"], game["correctOption"], game["surveyCorrectOption"])
            )
        questions.append(row)
        questions_by_key[key] = row

    people = []
    for row in raw_people:
        week = int(row["week"])
        people.append(
            {
                "participant": int(row["participant"]),
                "experiment": "2017",
                "itemBank": f"week{week:02d}",
                "design": "assigned",
                "condition": "participant",
                "source": "participant",
                "name": "",
                "askedWeek": week,
                "knowledge": row["knowledge"],
            }
        )
    trials = []
    for row in raw_trials:
        key = (int(row["week"]), int(row["game"]))
        question = questions_by_key[key]
        choice = int(row["prediction"]) if row["prediction"] != "" else None
        person = {"participant": int(row["participant"]), "experiment": "2017", "source": "participant"}
        trials.append(trial_from_choice(person, question, choice, row["confidence"], row["meta"]))

    stem = "participants-2017"
    write_csv(OUT / f"questions-{stem}.csv", QUESTION_FIELDS, questions)
    write_csv(OUT / f"trials-{stem}.csv", TRIAL_FIELDS, trials)
    write_csv(OUT / f"participants-{stem}.csv", PERSON_FIELDS, people)
    write_csv(OUT / f"itemBank-{stem}.csv", BANK_FIELDS, bank_rows(questions, "participant"))
    return questions, trials, people, rescheduled, winner_disagreements


def topic_counts(questions):
    counts = defaultdict(int)
    for question in questions:
        counts[question["topic"]] += 1
    return dict(sorted(counts.items(), key=lambda item: (-item[1], item[0])))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    summary = []
    expert_questions = {}
    for season in (2015, 2016, 2017):
        experts, games = load_espn(season)
        questions, trials, people = export_experts(season, experts, games)
        expert_questions[season] = questions
        ids = [row["gameId"] for row in questions]
        summary.append(
            f"{season} experts: {len(people)} people, {len(questions)} games, {len(trials)} trials, "
            f"unique gameId {len(set(ids))}, ties {sum(row['tie'] == 1 for row in questions)}, "
            f"topics {topic_counts(questions)}"
        )
        if len(ids) != len(set(ids)):
            raise ValueError(f"Duplicate gameId in {season}")
    q17, t17, p17, rescheduled, winner_disagreements = export_participants(load_espn(2017)[1])
    expert_ids = {row["gameId"] for row in expert_questions[2017]}
    participant_ids = {row["gameId"] for row in q17}
    summary.append(
        f"2017 participants: {len(p17)} people, {len(q17)} games, {len(t17)} trials, "
        f"topics {topic_counts(q17)}"
    )
    summary.append(
        f"2017 gameId overlap: {len(expert_ids & participant_ids)} shared, "
        f"expert only {sorted(expert_ids - participant_ids)}, "
        f"participant only {sorted(participant_ids - expert_ids)}"
    )
    summary.append(f"rescheduled: {rescheduled}")
    summary.append(f"survey truth disagreed with final score on {len(winner_disagreements)} games: {winner_disagreements}")
    week_mismatch = [
        (row["gameId"], row["askedWeek"], row["playedWeek"])
        for row in q17
        if int(row["askedWeek"]) != int(row["playedWeek"])
    ]
    summary.append(f"participant askedWeek != playedWeek: {week_mismatch}")
    print("\n".join(summary))


if __name__ == "__main__":
    main()
