import streamlit as st
import pandas as pd
import mysql.connector

# Connect to MySQL 
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="YourNewPassword123!",
    database="cricbuzz"
)

# Dictionary of queries 
queries = {
    # Q1: Venues in India
    "Venues in India": """
        SELECT * 
        FROM Venues
        WHERE country = 'India';
    """,

    # Q2: Matches in last 30 days
    "Recent Matches (last 30 days)": """
        SELECT m.match_id,
               t1.team_name AS team1,
               t2.team_name AS team2,
               CONCAT(v.venue_name, ', ', v.city) AS venue,
               m.match_date
        FROM Matches m
        JOIN Teams t1 ON m.team1_id = t1.team_id
        JOIN Teams t2 ON m.team2_id = t2.team_id
        JOIN Venues v ON m.venue_id = v.venue_id
        WHERE m.match_date >= (CURDATE() - INTERVAL 30 DAY)
        ORDER BY m.match_date DESC;
    """,

    # Q3: Top 10 players by runs/average/hundreds
    "Top 10 Players by Runs & Averages": """
        SELECT p.player_name,
               SUM(ms.runs) AS total_runs,
               ROUND(AVG(NULLIF(ms.runs, 0)), 2) AS batting_average,
               SUM(CASE WHEN ms.runs >= 100 THEN 1 ELSE 0 END) AS hundreds
        FROM MatchStats ms
        JOIN Players p ON p.player_id = ms.player_id
        GROUP BY p.player_id, p.player_name
        ORDER BY total_runs DESC
        LIMIT 10;
    """,

    # Q4: Venues with capacity > 50k
    "Venues with capacity > 50k": """
        SELECT venue_name, city, country, capacity
        FROM Venues
        WHERE capacity > 50000
        ORDER BY capacity DESC;
    """,

    # Q5: Total wins by team (winner_id)
    "Total Wins by Team": """
        SELECT t.team_name, COUNT(m.match_id) AS total_wins
        FROM Matches m
        JOIN Teams t ON m.winner_id = t.team_id
        WHERE m.winner_id IS NOT NULL
        GROUP BY t.team_name
        ORDER BY total_wins DESC;
    """,

    # Q6: Player role distribution
    "Player Roles Count": """
        SELECT role, COUNT(*) AS total_players
        FROM Players
        GROUP BY role
        ORDER BY total_players DESC;
    """,

    # Q7: Series in 2024
    "Series in 2024": """
        SELECT series_name, host_country, match_type, start_date, total_matches
        FROM Series
        WHERE YEAR(start_date) = 2024;
    """,

    # Q8: All-rounders with 1000+ runs and 50+ wickets
    "All-Rounders with 1000+ Runs and 50+ Wickets": """
        SELECT p.player_name,
               SUM(ms.runs) AS total_runs,
               SUM(ms.wickets) AS total_wickets
        FROM Players p
        JOIN MatchStats ms ON p.player_id = ms.player_id
        WHERE p.role = 'All-Rounder'
        GROUP BY p.player_id
        HAVING total_runs > 1000 AND total_wickets > 50;
    """,

    # Q9: Match descriptions
    "Match Descriptions": """
        SELECT match_id, match_desc
        FROM Matches;
    """,

    # Q10: Player performance by format
    "Player Runs by Format": """
        SELECT p.player_name,
               SUM(CASE WHEN m.match_format = 'Test' THEN ms.runs ELSE 0 END) AS Test_runs,
               SUM(CASE WHEN m.match_format = 'ODI' THEN ms.runs ELSE 0 END) AS ODI_runs,
               SUM(CASE WHEN m.match_format = 'T20I' THEN ms.runs ELSE 0 END) AS T20I_runs,
               ROUND(SUM(ms.runs) / COUNT(ms.match_id), 2) AS overall_batting_average
        FROM Players p
        JOIN MatchStats ms ON p.player_id = ms.player_id
        JOIN Matches m ON ms.match_id = m.match_id
        GROUP BY p.player_id, p.player_name
        HAVING COUNT(DISTINCT m.match_format) >= 2
        ORDER BY overall_batting_average DESC;
    """,

    # Q11: Home vs Away Wins
    "Home vs Away Wins": """
        SELECT t.team_name,
               SUM(CASE WHEN t.country = v.country THEN 1 ELSE 0 END) AS home_wins,
               SUM(CASE WHEN t.country != v.country THEN 1 ELSE 0 END) AS away_wins
        FROM Matches m
        JOIN Teams t ON m.winner_id = t.team_id
        JOIN Venues v ON m.venue_id = v.venue_id
        GROUP BY t.team_id, t.team_name
        ORDER BY home_wins DESC, away_wins DESC;
    """,

    # Q12: Partnerships with 100+ runs
    "100+ Partnerships": """
        SELECT p1.player_name AS batsman1,
               p2.player_name AS batsman2,
               (ms1.runs + ms2.runs) AS partnership_runs,
               ms1.match_id AS match_id
        FROM MatchStats ms1
        JOIN MatchStats ms2 
          ON ms1.match_id = ms2.match_id
         AND ms1.batting_position = ms2.batting_position - 1
        JOIN Players p1 ON ms1.player_id = p1.player_id
        JOIN Players p2 ON ms2.player_id = p2.player_id
        WHERE (ms1.runs + ms2.runs) >= 100
        ORDER BY partnership_runs DESC;
    """,

    # Q13: Bowlers Economy by Venue
    "Bowler Economy by Venue (3+ matches)": """
        SELECT p.player_name,
               v.venue_name,
               COUNT(ms.match_id) AS matches_played,
               SUM(ms.wickets) AS total_wickets,
               ROUND(SUM(ms.runs)/SUM(ms.overs), 2) AS avg_economy_rate
        FROM MatchStats ms
        JOIN Players p ON ms.player_id = p.player_id
        JOIN Matches m ON ms.match_id = m.match_id
        JOIN Venues v ON m.venue_id = v.venue_id
        WHERE p.role = 'Bowler' AND ms.overs >= 4
        GROUP BY p.player_id, v.venue_id
        HAVING COUNT(ms.match_id) >= 3
        ORDER BY avg_economy_rate ASC;
    """,

    # Q14: Close match performance
    "Player Performance in Close Matches": """
        SELECT p.player_name,
               ROUND(AVG(ms.runs), 2) AS avg_runs_in_close_matches,
               COUNT(ms.match_id) AS total_close_matches_played,
               SUM(CASE WHEN m.winner_id = p.team_id THEN 1 ELSE 0 END) AS close_matches_won
        FROM MatchStats ms
        JOIN Players p ON ms.player_id = p.player_id
        JOIN Matches m ON ms.match_id = m.match_id
        WHERE ms.is_close_match = 1
        GROUP BY p.player_id, p.player_name
        HAVING total_close_matches_played > 0
        ORDER BY avg_runs_in_close_matches DESC;
    """,

    # Q15: Strike Rate by Year (since 2020)
    "Player Strike Rate by Year": """
        SELECT p.player_name,
               YEAR(m.match_date) AS match_year,
               COUNT(ms.match_id) AS matches_played,
               ROUND(AVG(ms.runs), 2) AS avg_runs_per_match,
               ROUND(SUM(ms.runs) / SUM(NULLIF(ms.balls_faced,0)) * 100, 2) AS avg_strike_rate
        FROM MatchStats ms
        JOIN Players p ON ms.player_id = p.player_id
        JOIN Matches m ON ms.match_id = m.match_id
        WHERE m.match_date >= '2020-01-01'
        GROUP BY p.player_id, match_year
        HAVING matches_played >= 5
        ORDER BY p.player_name, match_year;
    """,

    # Q16: Toss impact
    "Toss Decision Impact": """
        SELECT toss_decision,
               COUNT(*) AS total_matches,
               SUM(CASE WHEN toss_winner_id = winner_id THEN 1 ELSE 0 END) AS matches_won_by_toss_winner,
               ROUND(SUM(CASE WHEN toss_winner_id = winner_id THEN 1 ELSE 0 END) / COUNT(*) * 100, 2) AS win_percentage
        FROM Matches
        WHERE toss_winner_id IS NOT NULL AND winner_id IS NOT NULL
        GROUP BY toss_decision;
    """,

    # Q17: Bowling workload (ODI & T20)
    "Bowling Workload (ODI & T20)": """
        SELECT p.player_name,
               SUM(ms.runs) / SUM(ms.overs_bowled) AS economy_rate,
               SUM(ms.wickets) AS total_wickets,
               COUNT(DISTINCT ms.match_id) AS matches_played,
               SUM(ms.overs_bowled) / COUNT(DISTINCT ms.match_id) AS avg_overs_per_match
        FROM MatchStats ms
        JOIN Players p ON ms.player_id = p.player_id
        JOIN Matches m ON ms.match_id = m.match_id
        WHERE ms.match_format IN ('ODI', 'T20')
        GROUP BY p.player_id, p.player_name
        HAVING COUNT(DISTINCT ms.match_id) >= 10;
    
    """,
        # Q18: Highest Wicket Takers
    "Top 10 Bowlers by Wickets": """
        SELECT p.player_name,
               SUM(ms.wickets) AS total_wickets,
               ROUND(SUM(ms.runs) / NULLIF(SUM(ms.wickets), 0), 2) AS bowling_average
        FROM MatchStats ms
        JOIN Players p ON ms.player_id = p.player_id
        GROUP BY p.player_id, p.player_name
        ORDER BY total_wickets DESC
        LIMIT 10;
    """,

    # Q19: Player of the Match Awards
    "Most Player of the Match Awards": """
        SELECT p.player_name,
               COUNT(*) AS awards
        FROM Matches m
        JOIN Players p ON m.player_of_match = p.player_id
        GROUP BY p.player_id, p.player_name
        ORDER BY awards DESC
        LIMIT 10;
    """,

    # Q20: Teams Head-to-Head
    "Head-to-Head Records": """
        SELECT t1.team_name AS team1,
               t2.team_name AS team2,
               COUNT(m.match_id) AS total_matches,
               SUM(CASE WHEN m.winner_id = t1.team_id THEN 1 ELSE 0 END) AS team1_wins,
               SUM(CASE WHEN m.winner_id = t2.team_id THEN 1 ELSE 0 END) AS team2_wins
        FROM Matches m
        JOIN Teams t1 ON m.team1_id = t1.team_id
        JOIN Teams t2 ON m.team2_id = t2.team_id
        GROUP BY t1.team_name, t2.team_name
        HAVING total_matches > 0
        ORDER BY total_matches DESC;
    """,

    # Q21: Batting Average by Batting Position
    "Batting Average by Position": """
        SELECT ms.batting_position,
               ROUND(AVG(ms.runs), 2) AS avg_runs,
               COUNT(ms.match_id) AS innings_played
        FROM MatchStats ms
        GROUP BY ms.batting_position
        ORDER BY ms.batting_position;
    """,

    # Q22: Team Performance by Year
    "Team Wins by Year": """
        SELECT t.team_name,
               YEAR(m.match_date) AS match_year,
               COUNT(m.match_id) AS matches_played,
               SUM(CASE WHEN m.winner_id = t.team_id THEN 1 ELSE 0 END) AS wins
        FROM Matches m
        JOIN Teams t ON m.team1_id = t.team_id OR m.team2_id = t.team_id
        GROUP BY t.team_name, match_year
        ORDER BY match_year DESC, wins DESC;
    """,

    # Q23: Fastest 50s (<=30 balls)
    "Fastest Fifties": """
        SELECT p.player_name,
               ms.match_id,
               ms.runs,
               ms.balls_faced
        FROM MatchStats ms
        JOIN Players p ON ms.player_id = p.player_id
        WHERE ms.runs >= 50 AND ms.balls_faced <= 30
        ORDER BY ms.balls_faced ASC
        LIMIT 10;
    """,

    # Q24: Duck Count (0 runs)
    "Players with Most Ducks": """
        SELECT p.player_name,
               COUNT(*) AS ducks
        FROM MatchStats ms
        JOIN Players p ON ms.player_id = p.player_id
        WHERE ms.runs = 0
        GROUP BY p.player_id, p.player_name
        ORDER BY ducks DESC
        LIMIT 10;
    """,

    # Q25: Consistent Performers (30+ avg, 1000+ runs)
    "Consistent Run Scorers": """
        SELECT p.player_name,
               SUM(ms.runs) AS total_runs,
               ROUND(AVG(NULLIF(ms.runs,0)), 2) AS batting_average,
               COUNT(ms.match_id) AS innings
        FROM MatchStats ms
        JOIN Players p ON ms.player_id = p.player_id
        GROUP BY p.player_id, p.player_name
        HAVING total_runs >= 1000 AND batting_average >= 30
        ORDER BY batting_average DESC, total_runs DESC;
    """

    

    
}


# Streamlit UI
st.title("🏏 Cricbuzz LiveStats - SQL Dashboard")

choice = st.selectbox("Select a query to run:", list(queries.keys()))

if st.button("Run Query"):
    df = pd.read_sql(queries[choice], conn)
    st.dataframe(df)
