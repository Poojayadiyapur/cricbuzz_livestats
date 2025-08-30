import streamlit as st

st.title("🏏 Cricbuzz Live Stats Dashboard")
st.write("""
Welcome to the **Cricbuzz Live Stats Dashboard** 🎉  

This project uses **Streamlit** to display live cricket statistics with interactive visualizations.  
Navigate through the sidebar to explore detailed stats like:
- 📊 Top Player Stats  
- 🏏 Match Summaries  
- 🌍 Team Comparisons  
- ⚡ Live Updates (if integrated)
""")

# Tools used
st.header("🛠 Tools & Technologies")
st.write("""
- **Python** 🐍  
- **Streamlit** for UI  
- **Pandas / NumPy** for data handling  
- **Matplotlib / Plotly** for charts  
- **BeautifulSoup / API** (if you scrape live data)  
""")

# Instructions for navigation
st.header("📖 Instructions")
st.write("""
1. Use the **sidebar** on the left to navigate between pages.  
2. Each page displays different cricket-related insights.  
3. Data will update automatically (if live data is connected).  
""")

st.header("📂 Documentation & Project Structure")
st.write("""
- Project Documentation: [Click here](https://github.com/Poojayadiyapur/cricbuzz_livestats)  
- Folder Structure:  cricbuzz_livestats/
├── Home.py
├── pages/
│ ├── 1_Live_Scores.py
│ ├── 2_Player_Stats.py
│ └── 3_Team_Stats.py
├── data/
└── utils/
         """)


