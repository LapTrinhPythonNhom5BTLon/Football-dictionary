import sqlite3
import pandas as pd
import numpy as np
from tabulate import tabulate

conn = sqlite3.connect("players.db")
df = pd.read_sql_query("SELECT * FROM players", conn)
conn.close()

non_numeric = ["player", "team", "nationality", "position"]

for col in df.columns:
    if col not in non_numeric:
        df[col] = pd.to_numeric(df[col], errors='coerce')

df = df.dropna(axis=1, how='all')

numeric_cols = df.select_dtypes(include=np.number).columns
team_stats = df.groupby("team")[numeric_cols].agg(['median', 'mean', 'std'])

team_stats.columns = ['_'.join(col) for col in team_stats.columns]

team_stats.to_csv("team_statistics.csv", index=True)

print("✔ Đã tạo file team_statistics.csv")


best_teams = {}

for col in numeric_cols:
    if col in ["minutes", "games", "goals", "assists"]:
        series = df.groupby("team")[col].sum()
    else:
        series = df.groupby("team")[col].mean()

    if col in ["cards_red", "cards_yellow"]:
        best_teams[col] = series.idxmin()
    else:
        best_teams[col] = series.idxmax()

best_df = pd.DataFrame(list(best_teams.items()), columns=["Chi_so", "Doi_tot_nhat"])
best_df.to_csv("best_team_each_metric.csv", index=False)

print("Đã tạo file best_team_each_metric.csv")

df_norm = df.copy()
df_norm[numeric_cols] = (df[numeric_cols] - df[numeric_cols].mean()) / df[numeric_cols].std()
df_norm = df_norm.fillna(0)

negative_cols = ["cards_red", "cards_yellow"]
for col in negative_cols:
    if col in df_norm.columns:
        df_norm[col] *= -1

weights = {
    "goals": 2,
    "assists": 1.5,
    "goals_per90": 2,
    "cards_red": -2,
    "cards_yellow": -1
}

team_score = pd.Series(0, index=df["team"].unique())

for col in numeric_cols:
    w = weights.get(col, 1)
    team_score += df_norm.groupby("team")[col].mean() * w

best_team_overall = team_score.idxmax()

print("\n BẢNG THỐNG KÊ THEO ĐỘI:\n")
print(tabulate(team_stats.reset_index(), headers="keys", tablefmt="grid"))

print("\n ĐỘI TỐT NHẤT THEO TỪNG CHỈ SỐ:\n")
print(tabulate(best_df, headers="keys", tablefmt="grid"))

ranking_df = team_score.sort_values(ascending=False).reset_index()
ranking_df.columns = ["Team", "Score"]

print("\n BXH PHONG ĐỘ TỔNG THỂ:\n")
print(tabulate(ranking_df, headers="keys", tablefmt="grid"))

print("\n Đội có phong độ tốt nhất:", best_team_overall)

print("\n Số cầu thủ mỗi đội:")
print(df["team"].value_counts())