import streamlit as st
import requests
import pandas as pd

# API details
url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/live"
headers = {
    "X-RapidAPI-Key": "d796d360e4msh8060d58be8bed38p172e52jsn679a3df8b9d4",
    "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"
}

# Streamlit Page setup
st.set_page_config(page_title="Live Cricket Matches", layout="wide")
st.title("🏏 Live Cricket Matches")

# Fetch live matches
def get_live_matches():
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Failed to fetch data from API")
            return None
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# Display Matches
data = get_live_matches()
if data:
    matches = data.get("matches", [])
    
    if matches:
        for match in matches:
            series = match.get("seriesName", "Unknown Series")
            match_desc = match.get("matchDesc", "")
            status = match.get("status", "")
            venue = match.get("venueInfo", {}).get("ground", "Unknown Venue")
            
            st.subheader(f"{series} - {match_desc}")
            st.write(f"📍 Venue: {venue}")
            st.write(f"📢 Status: {status}")
            
            # Teams & Scores
            if "scorecard" in match:
                for innings in match["scorecard"]:
                    team = innings.get("batTeamDetails", {}).get("batTeamName", "")
                    score = innings.get("scoreDetails", {}).get("runs", 0)
                    wickets = innings.get("scoreDetails", {}).get("wickets", 0)
                    overs = innings.get("scoreDetails", {}).get("overs", 0)
                    st.write(f"**{team}** - {score}/{wickets} in {overs} overs")

            # Batsmen Info
            if "batsman" in match:
                st.write("### 🏏 Batsmen at Crease")
                df_batsmen = pd.DataFrame(match["batsman"])
                st.table(df_batsmen)

            # Bowler Info
            if "bowler" in match:
                st.write("### 🎯 Current Bowler")
                df_bowler = pd.DataFrame(match["bowler"])
                st.table(df_bowler)

            st.markdown("---")
    else:
        st.info("No live matches right now 🚫")



