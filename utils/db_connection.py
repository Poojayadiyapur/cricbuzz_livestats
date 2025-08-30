import requests
import pandas as pd
import sqlite3
import mysql.connector

# API 
url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/live"

headers = {
    "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com",
    "x-rapidapi-key": 'd796d360e4msh8060d58be8bed38p172e52jsn679a3df8b9d4'
}


# Fetch data
response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
else:
    print("Error:", response.status_code, response.text)
    exit()

# Extract matches
matches_list = []

for match_type in data['typeMatches']:
    for series in match_type['seriesMatches']:
        if 'seriesAdWrapper' in series:
            for match in series['seriesAdWrapper']['matches']:
                info = match.get('matchInfo', {})
                score = match.get('matchScore', {})

                team1 = info.get('team1', {}).get('teamName', 'N/A')
                team2 = info.get('team2', {}).get('teamName', 'N/A')
                status = info.get('status', 'N/A')
                match_format = info.get('matchFormat', 'N/A')

                # Scores
                team1_score = score.get('team1Score', {}).get('inngs1', {})
                team2_score = score.get('team2Score', {}).get('inngs1', {})

                matches_list.append({
                    "Team 1": team1,
                    "Team 2": team2,
                    "Status": status,
                    "Format": match_format,
                    "T1 Runs": team1_score.get('runs'),
                    "T1 Wkts": team1_score.get('wickets'),
                    "T1 Overs": team1_score.get('overs'),
                    "T2 Runs": team2_score.get('runs'),
                    "T2 Wkts": team2_score.get('wickets'),
                    "T2 Overs": team2_score.get('overs')
                })

# Save 
df = pd.DataFrame(matches_list)

conn = sqlite3.connect("cricbuzz.db")
df.to_sql("live_matches", conn, if_exists="replace", index=False)
conn.close()

print("✅ Data fetched and saved to cricbuzz.db")

import sqlite3

DB_PATH = "cricbuzz.db"

def get_connection():
    """Create and return SQLite DB connection."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    return conn
import streamlit as st
import pandas as pd
import sys, os
import sqlite3


DB_PATH = "cricbuzz.db"

def get_connection():
    """Create and return SQLite DB connection."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    return conn

st.title("🏏 Cricbuzz SQL Queries & Analytics")

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="YourNewPassword123!",
    database="cricbuzz"
)

queries = {
    "Live Matches (raw)": "SELECT * FROM live_matches;",
    "Top 5 Team Scores": """
        SELECT "Team 1" AS team, MAX("T1 Runs") AS runs FROM live_matches
        GROUP BY "Team 1"
        UNION
        SELECT "Team 2" AS team, MAX("T2 Runs") AS runs FROM live_matches
        GROUP BY "Team 2"
        ORDER BY runs DESC
        LIMIT 5;
    """,
    "Average Runs per Team": """
        SELECT "Team 1" AS team, AVG("T1 Runs") AS avg_runs
        FROM live_matches
        GROUP BY "Team 1"
        UNION
        SELECT "Team 2" AS team, AVG("T2 Runs") AS avg_runs
        FROM live_matches
        GROUP BY "Team 2"
        ORDER BY avg_runs DESC;
    """,
    "Match Status Count": """
        SELECT Status, COUNT(*) AS match_count
        FROM live_matches
        GROUP BY Status;
    """
}

choice = st.selectbox("Choose a query", list(queries.keys()))

if st.button("Run Query"):
    try:
        df = pd.read_sql(queries[choice], conn)
        st.dataframe(df)
    except Exception as e:
        st.error(f"Error running the query: {e}")
