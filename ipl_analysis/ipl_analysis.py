import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

df = pd.read_csv("ipl_2008_to_2025.csv")
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df['Season'] = df['Date'].dt.year1
conn = sqlite3.connect("ipl_analysis.db")
df.to_sql("matches", conn, if_exists="replace", index=False)

def save_and_show(fig, name):
    path = f"{name}.png"
    fig.savefig(path, bbox_inches='tight')
    print(f"✅ Plot saved as: {path}")
    plt.show()
    plt.close(fig)

def team_win_percentage():
    wins = df['Match_Winner'].value_counts()
    matches = df['Teams'].str.split(' vs ').explode().value_counts()
    win_pct = (wins / matches * 100).dropna().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(12,6))
    win_pct.plot(kind='bar', color='skyblue', ax=ax)
    ax.set_title("Team‑wise Win Percentage")
    ax.set_ylabel("Win Percentage")
    save_and_show(fig, "team_win_percentage")

def matches_per_season():
    counts = df['Season'].value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(12,6))
    counts.plot(kind='bar', color='lightgreen', ax=ax)
    ax.set_title("Matches Per Season")
    ax.set_ylabel("Number of Matches")
    save_and_show(fig, "matches_per_season")

def toss_win_impact():
    df['Toss_Win_Impact'] = df['Toss_Winner'] == df['Match_Winner']
    counts = df['Toss_Win_Impact'].value_counts()
    labels = ['Toss Loss -> Match Win', 'Toss Win -> Match Win']
    fig, ax = plt.subplots()
    counts.plot.pie(autopct='%1.1f%%', labels=labels, ax=ax)
    ax.set_ylabel('')
    ax.set_title("Impact of Toss on Match Win")
    save_and_show(fig, "toss_win_impact")

def top_venues():
    venue_counts = df['Venue'].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(12,6))
    venue_counts.plot(kind='bar', color='orange', ax=ax)
    ax.set_title("Top 10 Most Frequent IPL Venues")
    ax.set_ylabel("Match Count")
    save_and_show(fig, "top_venues")

def player_of_match():
    top_players = df['Player_of_Match'].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(12,6))
    top_players.plot(kind='bar', color='purple', ax=ax)
    ax.set_title("Top 10 Players of the Match")
    ax.set_ylabel("Count")
    save_and_show(fig, "player_of_match")

def team_performance_trend():
    performance = df.groupby(['Season', 'Match_Winner']).size().unstack().fillna(0)
    top_teams = performance.sum().sort_values(ascending=False).head(5).index
    fig, ax = plt.subplots(figsize=(12,6))
    performance[top_teams].plot(ax=ax, marker='o')
    ax.set_title("Top 5 Teams Performance Over Seasons")
    ax.set_ylabel("Number of Wins")
    save_and_show(fig, "team_performance_trend")

def win_type_distribution():
    win_types = df['Win_Type'].value_counts()
    fig, ax = plt.subplots()
    win_types.plot.pie(autopct='%1.1f%%', ax=ax)
    ax.set_ylabel('')
    ax.set_title("Win Type Distribution")
    save_and_show(fig, "win_type_distribution")

def avg_win_margin():
    avg_runs = df[df['Win_Type'] == 'runs']['Win_Margin'].mean()
    avg_wkts = df[df['Win_Type'] == 'wickets']['Win_Margin'].mean()
    margins = pd.Series({'Runs': avg_runs, 'Wickets': avg_wkts})
    fig, ax = plt.subplots()
    margins.plot(kind='bar', ax=ax, color=['blue', 'green'])
    ax.set_title("Average Win Margin")
    ax.set_ylabel("Margin")
    save_and_show(fig, "avg_win_margin")

def high_powerplay():
    high_pp = df[df['Powerplay_Scores'] > 70]
    counts = high_pp['Teams'].value_counts().head(5)
    fig, ax = plt.subplots()
    counts.plot(kind='bar', color='red', ax=ax)
    ax.set_title("Top 5 Teams With Powerplays >70")
    ax.set_ylabel("Count")
    save_and_show(fig, "high_powerplay_teams")

def death_overs_analysis():
    fig, ax = plt.subplots()
    df['Death_Overs_Scores'].plot.hist(bins=20, color='darkred', ax=ax)
    ax.set_title("Death Overs Score Distribution")
    ax.set_xlabel("Runs in Death Overs")
    save_and_show(fig, "death_overs_distribution")

menu_options = {
    "1": team_win_percentage,
    "2": matches_per_season,
    "3": toss_win_impact,
    "4": top_venues,
    "5": player_of_match,
    "6": team_performance_trend,
    "7": win_type_distribution,
    "8": avg_win_margin,
    "9": high_powerplay,
    "10": death_overs_analysis
}

def run_menu():
    while True:
        print("""
--- IPL Analysis Menu ---
1. Team Win Percentage
2. Matches Per Season
3. Toss Win Impact
4. Top 10 IPL Venues
5. Top 10 Player of the Match Awards
6. Team Performance Trend Over Seasons
7. Win Type Distribution
8. Average Win Margin
9. High Powerplay Scores
10. Death Overs Score Distribution
0. Exit
""")
        choice = input("Enter option number: ").strip()
        if choice == "0":
            print("✅ Exiting program.")
            break
        elif choice in menu_options:
            menu_options[choice]()
        else:
            print("❌ Invalid input. Please choose a number from 0–10.")

if __name__ == "__main__":
    run_menu()
