import streamlit as st

st.set_page_config(page_title="Cricbuzz LiveStats", layout="wide")

st.sidebar.title("🏏 Cricbuzz LiveStats Dashboard")
st.sidebar.write("Navigate through the features:")

st.sidebar.page_link("app.py", label="Home")
st.sidebar.page_link("pages/live_matches.py", label="📡 Live Matches")
st.sidebar.page_link("pages/top_stats.py", label="📊 Top Statistics")
st.sidebar.page_link("pages/sql_queries.py", label="🛠️ SQL Queries")
st.sidebar.page_link("pages/crud_operations.py", label="⚙️ CRUD Operations")

st.title("🏏 Cricbuzz LiveStats Dashboard")
st.write("Welcome to the interactive cricket analytics platform 🚀")



