#!/usr/bin/env python3
"""Rename CSV files/columns to camelCase and write data.mat (struct d) in each folder."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "datasets"
sys.path.insert(0, str(Path(__file__).resolve().parent))
from io_util import camel_filename, to_camel, write_data_mat, _is_numeric_row  # noqa: E402


def convert_csv(path: Path) -> Path:
    dest = path.with_name(camel_filename(path.name))
    text = path.read_text(errors="replace")
    lines = text.splitlines()
    if not lines:
        if dest != path:
            path.rename(dest)
        return dest
    if _is_numeric_row(lines[0]):
        if dest != path:
            path.replace(dest)
        return dest
    df = pd.read_csv(path)
    df.columns = [to_camel(str(c)) for c in df.columns]
    df.to_csv(dest, index=False)
    if dest != path:
        path.unlink()
    return dest


def convert_catalog() -> None:
    path = ROOT / "CATALOG.csv"
    df = pd.read_csv(path)
    df.columns = [to_camel(str(c)) for c in df.columns]
    df.to_csv(path, index=False)


def replace_in_markdown() -> None:
    """Update backticked snake_case names in READMEs to camelCase."""
    for md in list(DATA.rglob("*.md")) + [ROOT / "README.md", ROOT / "scripts" / "README.md"]:
        text = md.read_text()
        orig = text

        def tick(match):
            inner = match.group(1)
            if "_" not in inner:
                return match.group(0)
            return f"`{to_camel(inner)}`"

        import re

        text = re.sub(r"`([^`]+)`", tick, text)
        # filenames mentioned without needing ticks already handled if ticked
        for old, new in [
            ("task_order.csv", "taskOrder.csv"),
            ("related_tasks.csv", "relatedTasks.csv"),
            ("problem_values.csv", "problemValues.csv"),
            ("game_reward_rates.csv", "gameRewardRates.csv"),
            ("condition_order.csv", "conditionOrder.csv"),
            ("cue_validities.csv", "cueValidities.csv"),
            ("study1_gain_loss.csv", "study1GainLoss.csv"),
            ("experiment1_training.csv", "experiment1Training.csv"),
            ("experiment1_testing.csv", "experiment1Testing.csv"),
            ("experiment2_training.csv", "experiment2Training.csv"),
            ("experiment2_testing.csv", "experiment2Testing.csv"),
            ("serial_position_counts.csv", "serialPositionCounts.csv"),
            ("murdock1962_wide.csv", "murdock1962Wide.csv"),
            ("continuous_osn.csv", "continuousOSN.csv"),
            ("study_test_osn.csv", "studyTestOSN.csv"),
            ("continuous_on.csv", "continuousON.csv"),
            ("study_test_on.csv", "studyTestON.csv"),
            ("CATALOG.csv", "CATALOG.csv"),
        ]:
            text = text.replace(old, new)
        if text != orig:
            md.write_text(text)


def main() -> None:
    convert_catalog()
    folders = sorted({p.parent for p in DATA.rglob("*.csv")})
    for folder in folders:
        for csv_path in sorted(folder.glob("*.csv")):
            convert_csv(csv_path)
        out = write_data_mat(folder)
        print(f"OK {folder.relative_to(ROOT)} -> {out.name}")
    replace_in_markdown()
    print("done")


if __name__ == "__main__":
    main()
