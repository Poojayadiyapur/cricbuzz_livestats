import streamlit as st
import pandas as pd


st.title("⚙️ CRUD Operations")
st.write("Here you can Create, Read, Update, and Delete records.")

# Example buttons
if st.button("Create"):
    st.success("Create operation triggered!")

if st.button("Read"):
    st.info("Read operation triggered!")

if st.button("Update"):
    st.warning("Update operation triggered!")

if st.button("Delete"):
    st.error("Delete operation triggered!")

st.title("⚙️ CRUD Operations - Player & Match Stats")

# Simulated data 
if "players" not in st.session_state:
    st.session_state.players = pd.DataFrame([
        {"id": 1, "name": "Virat Kohli", "role": "Batsman", "runs": 12000},
        {"id": 2, "name": "Jasprit Bumrah", "role": "Bowler", "runs": 300},
    ])

df = st.session_state.players

# Create 
st.subheader("➕ Add New Player")
with st.form("add_player_form"):
    name = st.text_input("Player Name")
    role = st.selectbox("Role", ["Batsman", "Bowler", "All-Rounder", "Wicket-Keeper"])
    runs = st.number_input("Runs", min_value=0, step=1)
    submitted = st.form_submit_button("Add Player")

    if submitted:
        new_id = df["id"].max() + 1 if not df.empty else 1
        new_row = {"id": new_id, "name": name, "role": role, "runs": runs}
        st.session_state.players = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        st.success(f"✅ Player {name} added!")

#  Read 
st.subheader("📋 Current Players")
st.dataframe(st.session_state.players, use_container_width=True)

#  Update 
st.subheader("✏️ Update Player Runs")
player_to_update = st.selectbox("Select Player", df["name"])
new_runs = st.number_input("New Runs", min_value=0, step=1)
if st.button("Update Runs"):
    st.session_state.players.loc[df["name"] == player_to_update, "runs"] = new_runs
    st.success(f"✅ Runs updated for {player_to_update}!")

#  Delete 
st.subheader("🗑️ Delete Player")
player_to_delete = st.selectbox("Select Player to Delete", df["name"])
if st.button("Delete Player"):
    st.session_state.players = df[df["name"] != player_to_delete]
    st.warning(f"❌ Player {player_to_delete} deleted!")
