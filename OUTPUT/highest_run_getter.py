"""
Highest Run Getter + ODI Average
among the 8 Australian batters – using odi_international.csv
"""

import pandas as pd

CSV_PATH = r"D:\AUS BATTER ANALYSIS\DATA\odi_international.csv"

AUS_BATTERS = [
    'MR Marsh', 'TM Head', 'AT Carey', 'M Labuschagne',
    'C Green', 'JP Inglis', 'MT Renshaw', 'C Connolly',
]

# ── Load & filter ──────────────────────────────────────────────
print("Loading international ODI data ...")
df = pd.read_csv(CSV_PATH, low_memory=False)
print(f"Total rows: {len(df):,}\n")

aus_df = df[
    df['batter'].isin(AUS_BATTERS) &
    (df['batting_team'] == 'Australia')
].copy()

# ── Aggregate stats ────────────────────────────────────────────
summary = aus_df.groupby('batter').agg(
    Total_Runs  = ('runs_batter', 'sum'),
    Dismissals  = ('wicket',      'sum'),
    Balls_Faced = ('wides',       lambda x: (x == 0).sum()),
    Matches     = ('match_id',    'nunique'),
).reset_index()

# Batting Average = Runs / Dismissals (N/O if never dismissed)
summary['Average'] = (
    summary['Total_Runs'] / summary['Dismissals'].replace(0, float('nan'))
).round(2)

# Strike Rate
summary['Strike_Rate'] = (
    summary['Total_Runs'] / summary['Balls_Faced'] * 100
).round(2)

# Sort by runs
summary = summary.sort_values('Total_Runs', ascending=False).reset_index(drop=True)
summary.index += 1

# ── Print leaderboard ──────────────────────────────────────────
print("=" * 70)
print("  Australian Batters – International ODI Stats")
print("=" * 70)
print(f"{'Rk':<4} {'Batter':<18} {'Mat':>4} {'Runs':>6} "
      f"{'Balls':>6} {'Out':>5} {'Avg':>7} {'SR':>7}")
print("-" * 70)

for rank, row in summary.iterrows():
    avg = f"{row['Average']:.2f}" if str(row['Average']) != 'nan' else "N/O"
    tag = "  <<< HIGHEST" if rank == 1 else ""
    print(f"{rank:<4} {row['batter']:<18} {int(row['Matches']):>4} "
          f"{int(row['Total_Runs']):>6} {int(row['Balls_Faced']):>6} "
          f"{int(row['Dismissals']):>5} {avg:>7} {row['Strike_Rate']:>7}{tag}")

print("=" * 70)

# ── Winner card ────────────────────────────────────────────────
top = summary.iloc[0]
avg_top = f"{top['Average']:.2f}" if str(top['Average']) != 'nan' else "N/O"

print(f"\n[HIGHEST RUN GETTER]")
print(f"  Batter       : {top['batter']}")
print(f"  Total Runs   : {int(top['Total_Runs'])}")
print(f"  Matches      : {int(top['Matches'])}")
print(f"  Batting Avg  : {avg_top}")
print(f"  Strike Rate  : {top['Strike_Rate']}")
