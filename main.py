"""
Project: Major League Insights (MLI)
Author: Daniel Godoy
GitHub: https://github.com/DxGodoy-dev
Repository: https://github.com/DxGodoy-dev/Major-League-Insights-MLI
Version: 1.0
Description: Advanced data engine for MLB analytics and forecasting.
"""

import statsapi
import pandas as pd
from datetime import datetime
from pathlib import Path

# --- HELPER FUNCTIONS ---

def lookup_team(name):
    """Finds team ID and formal name using the MLB API."""
    candidates = statsapi.lookup_team(name)
    if not candidates:
        raise ValueError(f"No team found for '{name}'. Please check spelling.")
    
    for t in candidates:
        if t.get('abbreviation','').lower() == name.lower() \
        or t.get('name','').lower() == name.lower() \
        or t.get('teamName','').lower() == name.lower():
            return t['id'], t['name']

    return candidates[0]['id'], candidates[0]['name']

def fetch_season_schedule():
    """Fetches full season schedule up to today's date."""
    today = datetime.today()
    date_str = str(today.date())
    start_date = "2025-03-01" 
    
    raw = statsapi.schedule(start_date=start_date, end_date=date_str, sportId=1)
    
    records = []
    for g in raw:
        records.append({
            'game_id': g['game_id'],
            'date': g['game_date'][:10],
            'home_id': g['home_id'],
            'home_name': g['home_name'],
            'home_score': g['home_score'],
            'away_id': g['away_id'],
            'away_name': g['away_name'],
            'away_score': g['away_score'],
        })
    df = pd.DataFrame(records)
    df['date'] = pd.to_datetime(df['date'])
    return df, date_str

# --- ANALYSIS FUNCTIONS ---

def league_run_averages(df, t1_id, t2_id, t1_name, t2_name, windows=(None, 15, 10, 5)):
    """Calculates rolling average of total runs per game."""
    df = df.copy()
    df['total_runs'] = df['home_score'] + df['away_score']
    
    df_t1 = df[(df["home_id"] == t1_id) | (df["away_id"] == t1_id)]
    df_t2 = df[(df["home_id"] == t2_id) | (df["away_id"] == t2_id)]
    
    teams_data = [(df_t1, t1_name), (df_t2, t2_name)]
    full_results = []

    for d, t in teams_data:
        results = [f"{t}: "]
        for w in windows:
            if w is None:
                results.append(f"All: {d['total_runs'].mean():.2f}")
            else:
                results.append(f"L{w}: {d.tail(w)['total_runs'].mean():.2f}")
        full_results.append(results)
    return full_results

def team_run_averages(df, team_id, windows=(15, 10, 5)):
    """Calculates average runs scored by a specific team."""
    df_team = df[(df['home_id'] == team_id) | (df['away_id'] == team_id)].copy()
    df_team['runs_for'] = df_team.apply(
        lambda row: row['home_score'] if row['home_id'] == team_id else row['away_score'], axis=1
    )
    df_team = df_team.sort_values('date').reset_index(drop=True)
    return {f"Last {w}": df_team.tail(w)['runs_for'].mean() for w in windows}

def win_loss_record(df, team_id, windows=(15, 10, 5)):
    """Calculates W-L records for specified windows."""
    df_team = df[(df['home_id'] == team_id) | (df['away_id'] == team_id)].copy()
    df_team['runs_for'] = df_team.apply(
        lambda r: r['home_score'] if r['home_id'] == team_id else r['away_score'], axis=1
    )
    df_team['runs_against'] = df_team.apply(
        lambda r: r['away_score'] if r['home_id'] == team_id else r['home_score'], axis=1
    )
    
    records = {}
    for w in windows:
        sub = df_team.tail(w)
        wins = (sub['runs_for'] > sub['runs_against']).sum()
        losses = (sub['runs_for'] < sub['runs_against']).sum()
        records[f"Last {w}"] = (int(wins), int(losses))
    return records

def h2h_stats(df, team1_id, team2_id, windows=(10, 5)):
    """Analyzes Head-to-Head performance trends."""
    mask = ((df.home_id == team1_id) & (df.away_id == team2_id)) | \
            ((df.home_id == team2_id) & (df.away_id == team1_id))
    
    df_h2h = df[mask].copy().sort_values('date').reset_index(drop=True)
    df_h2h['total_runs'] = df_h2h['home_score'] + df_h2h['away_score']
    
    def get_runs(sub, tid):
        return sub.apply(lambda r: r['home_score'] if r['home_id'] == tid else r['away_score'], axis=1)

    results_h2h, avg_t1, avg_t2, wl_t1, wl_t2 = [], [], [], [], []
    for w in windows:
        sub = df_h2h.tail(w)
        results_h2h.append(f"L{w}: {sub['total_runs'].mean():.2f}")
        r1, r2 = get_runs(sub, team1_id), get_runs(sub, team2_id)
        avg_t1.append(f"L{w}: {r1.mean():.2f}")
        avg_t2.append(f"L{w}: {r2.mean():.2f}")
        wl_t1.append(f"L{w}: {(r1 > r2).sum()}-{(r1 < r2).sum()}")
        wl_t2.append(f"L{w}: {(r2 > r1).sum()}-{(r2 < r1).sum()}")

    return results_h2h, avg_t1, avg_t2, wl_t1, wl_t2

# --- MAIN ENGINE ---

def main():
    print(f"\n[Major League Insights] Starting analysis...")
    df, date_str = fetch_season_schedule()
    
    project_root = Path(__file__).parent
    output_path = project_root / "reports" / f"MLB_Matches_{date_str}"
    output_path.mkdir(parents=True, exist_ok=True)

    current_games = df[df.date == date_str].copy().reset_index(drop=True)
    
    if current_games.empty:
        print(f"No games scheduled for {date_str}.")
        return

    for _, row in current_games.iterrows():
        t1, t2 = row['home_name'], row['away_name']
        t1_id, t1_name = lookup_team(t1)
        t2_id, t2_name = lookup_team(t2)
        
        file_path = output_path / f"{t1_name} vs {t2_name}.txt"

        hist_mask = (df.home_score != df.away_score) & \
                    ((df.home_id == t1_id) | (df.away_id == t1_id) | 
                    (df.home_id == t2_id) | (df.away_id == t2_id))
        df_final = df[hist_mask].copy().sort_values('date')

        with open(file_path, "w", encoding="utf-8") as f:
            f.write("="*60 + "\n")
            f.write(f" MAJOR LEAGUE INSIGHTS: {t1_name.upper()} vs {t2_name.upper()} \n")
            f.write("="*60 + "\n\n")
            
            f.write("--- LEAGUE RUN AVERAGES (TOTAL) ---\n")
            for p in league_run_averages(df_final, t1_id, t2_id, t1_name, t2_name):
                f.write(f"{p[0].ljust(20)} | " + " | ".join(p[1:]) + "\n")
            
            f.write(f"\n--- RUNS SCORED BY TEAM ---\n")
            f.write(f"{t1_name.ljust(20)}: ")
            f.write(" | ".join([f"{k}: {v:.2f}" for k, v in team_run_averages(df_final, t1_id).items()]) + "\n")
            f.write(f"{t2_name.ljust(20)}: ")
            f.write(" | ".join([f"{k}: {v:.2f}" for k, v in team_run_averages(df_final, t2_id).items()]) + "\n")

            f.write(f"\n--- HEAD-TO-HEAD (H2H) HISTORY ---\n")
            h2h_res, a1, a2, w1, w2 = h2h_stats(df_final, t1_id, t2_id)
            f.write(f"Combined Total Avg  : {', '.join(h2h_res)}\n")
            f.write(f"{t1_name.ljust(20)} Avg : {', '.join(a1)}\n")
            f.write(f"{t2_name.ljust(20)} Avg : {', '.join(a2)}\n")
            f.write(f"{t1_name.ljust(20)} W-L : {', '.join(w1)}\n")
            f.write(f"{t2_name.ljust(20)} W-L : {', '.join(w2)}\n")

            f.write(f"\n--- OVERALL SEASON RECORD (W-L) ---\n")
            wl1, wl2 = win_loss_record(df_final, t1_id), win_loss_record(df_final, t2_id)
            f.write(f"{t1_name.ljust(20)}: " + " | ".join([f"{k}: {w}-{l}" for k, (w, l) in wl1.items()]) + "\n")
            f.write(f"{t2_name.ljust(20)}: " + " | ".join([f"{k}: {w}-{l}" for k, (w, l) in wl2.items()]) + "\n")
            
            f.write("\n" + "="*60 + "\n")
            f.write(f" Report generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} \n")
            f.write("="*60 + "\n")

    print(f"Analysis complete. Reports saved in: {output_path.absolute()}")

if __name__ == "__main__":
    main()