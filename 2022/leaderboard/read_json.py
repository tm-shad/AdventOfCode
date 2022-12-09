# %% [markdown]
# ## 1.0 - Setup

# %%
import json
from pathlib import Path
import logging
import argparse

import pandas as pd


# %%
def get_day_result(df: pd.DataFrame, day: int) -> pd.DataFrame:
    cols = [
        col
        for col in df.filter(regex="^score_Q\d+\.\d+").columns
        if int(col.strip("score_Q").split(".")[0]) <= day
    ]

    return df[cols]


def load_data(json_file: str):
    # Load Data
    with open(json_file) as f:
        data_dict = json.load(f)

    df = pd.DataFrame(
        [
            (
                m["id"],
                m["name"],
                m["stars"],
                m["local_score"],
            )
            for m in data_dict["members"].values()
        ],
        columns=["id", "name", "stars", "local_score"],
    )
    df = df.set_index("id", drop=True)

    # Get Metadata
    max_days = max(
        [
            max(list(int(c) for c in m["completion_day_level"].keys()) + [0])
            for m in data_dict["members"].values()
        ]
    )
    questions_per_day = 2

    # Fix missing data
    df.name.replace(pd.NA, "Anon", inplace=True)

    # Extract per-question points
    for day in range(1, max_days + 1):
        for q in range(1, questions_per_day + 1):
            s = pd.Series(index=df.index, dtype=float)
            for m_id in df.index:
                try:
                    s[m_id] = data_dict["members"][str(m_id)]["completion_day_level"][
                        str(day)
                    ][str(q)]["get_star_ts"]
                except KeyError:
                    s[m_id] = pd.NA

            # sort and assign points
            df[f"time_Q{day}.{q}"] = s
            df[f"score_Q{day}.{q}"] = (
                s.sort_values().rank(ascending=False, na_option="keep", method="min")
                + s.isna().sum()
            )

    # Calculate Running Points
    for d in range(1, max_days + 1):
        df[f"Points day {d}"] = get_day_result(df, day=d).sum(axis=1)

    # Calculate Running Rank
    for d in range(1, max_days + 1):
        df[f"Rank day {d}"] = (
            df[f"Points day {d}"].sort_values(ascending=False).rank(ascending=False)
        )

    return df


df = load_data(r"C:\Users\Troy\Documents\Git Dev\AdventOfCode\2022\leaderboard.json")
df

# %% [markdown]
# ## 2.0 - Data Exploration

# %%
def day_change(df: pd.DataFrame, day: int):
    new_df = df[["name", f"Rank day {day-1}", f"Rank day {day}"]].copy()

    new_df["total points"] = get_day_result(df, day).sum(axis=1).astype(int)
    new_df["change"] = [
        "▲🟢"
        if r[f"Rank day {day-1}"] - r[f"Rank day {day}"] > 0
        else "▼🔴"
        if r[f"Rank day {day-1}"] - r[f"Rank day {day}"] < 0
        else "- "
        for _, r in new_df.iterrows()
    ]
    new_df["change #"] = [
        r[f"Rank day {day-1}"] - r[f"Rank day {day}"] for _, r in new_df.iterrows()
    ]

    # get point delta
    delta = get_day_result(df, day).sum(axis=1).astype(int) - get_day_result(
        df, day - 1
    ).sum(axis=1).astype(int)
    delta.iloc[0]

    # delta.loc[1511475]
    id = df[df.name.str.contains("Troy")].iloc[0].name

    new_df["point delta"] = delta - delta.loc[id]

    return new_df.sort_values(by=f"Rank day {day}")


# %%
DAY = 8
pd.set_option("display.max_rows", 500)
day_change(df, day=DAY)

# %%
df.insert(0, "Points day 0", 0)
me_id = df[df.name.str.contains("Troy")].iloc[0].name

for i, j in df.filter(regex="^(Points day)").items():
    day = i.split()[-1]
    df[f"Delta P day {day}"] = df[i] - df[i].loc[me_id]
df.sort_values(by="local_score", ascending=False).head(100).filter(
    regex="^(name|Delta P day )"
).set_index("name", drop=True).transpose().plot.line(legend=False, figsize=(20, 15))
