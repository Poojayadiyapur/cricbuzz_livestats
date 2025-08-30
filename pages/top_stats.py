import streamlit as st
import pandas as pd
import sys
import os
import mysql.connector

# Import connection from utils 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

st.title("📊 Top Player Stats - Cricbuzz Live")

# Get MySQL connection 
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="YourNewPassword123!",  
    database="fufu"
)

#  Top Stats queries 
queries = {
    "🏏 Most Runs": """
        SELECT p.player_name, SUM(ps.runs) AS total_runs
        FROM player_stats ps
        JOIN players p ON ps.player_id = p.player_id
        GROUP BY p.player_name
        ORDER BY total_runs DESC
        LIMIT 10;
    """,
    "🎯 Most Wickets": """
        SELECT p.player_name, SUM(ps.wickets) AS total_wickets
        FROM player_stats ps
        JOIN players p ON ps.player_id = p.player_id
        GROUP BY p.player_name
        ORDER BY total_wickets DESC
        LIMIT 10;
    """,
    "🔥 Highest Individual Score": """
        SELECT p.player_name, MAX(ps.runs) AS highest_score
        FROM player_stats ps
        JOIN players p ON ps.player_id = p.player_id
        GROUP BY p.player_name
        ORDER BY highest_score DESC
        LIMIT 10;
    """,
    "⚡ Best Bowling Figures": """
        SELECT p.player_name,
               MAX(ps.wickets) AS best_wickets,
               MIN(ps.runs) AS least_runs_conceded
        FROM player_stats ps
        JOIN players p ON ps.player_id = p.player_id
        GROUP BY p.player_name
        ORDER BY best_wickets DESC, least_runs_conceded ASC
        LIMIT 10;
    """,
    "💯 Centuries (100s)": """
        SELECT p.player_name, COUNT(*) AS hundreds
        FROM player_stats ps
        JOIN players p ON ps.player_id = p.player_id
        WHERE ps.runs >= 100
        GROUP BY p.player_name
        ORDER BY hundreds DESC
        LIMIT 10;
    """
}

# Show all stats
for title, query in queries.items():
    st.subheader(title)
    df = pd.read_sql(query, conn)
    st.dataframe(df)

# Close 
conn.close()
