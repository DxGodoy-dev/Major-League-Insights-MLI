# ⚾ Major League Insights (MLI)
### Advanced Statistical Engine for MLB Performance Analytics & Forecasting

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0+-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![MLB API](https://img.shields.io/badge/API-MLB_Stats-red?style=for-the-badge)](https://github.com/toddrob99/MLB-StatsAPI)

**MLI** is a high-performance data engine designed to automate the extraction and analysis of Major League Baseball (MLB) datasets. It transforms raw play-by-play data into actionable intelligence, focusing on momentum shifts, head-to-head (H2H) history, and rolling performance averages.

---

### 📉 Analytical Capabilities
The system implements professional-grade sports metrics to identify value and trends:

* **Rolling Performance Windows:** Calculates scoring averages across specific intervals (Last 15, 10, and 5 games) to detect team momentum and "hot streaks."
* **Advanced H2H Mapping:** Deep-dives into historical matchups between specific teams to identify psychological or tactical advantages regardless of Home/Away status.
* **Scoring Distribution Analysis:** Segregates Home vs. Away performance using vectorized logic to account for stadium-specific factors.
* **Automated Scouting Reports:** Generates comprehensive daily reports for every scheduled game, providing a 360-degree view of the matchup.

---

### 🛠️ Technical Architecture
This engine is built on a modern data stack with a focus on efficiency:

1. **Extraction (API)**: Real-time consumption of MLB official data via `statsapi`, handling dynamic team lookups and schedule fetching.
2. **Transformation (Pandas)**: 
    * **Vectorized Scoring**: Efficiently calculates runs-for/runs-against using `lambda` functions and boolean masking.
    * **Momentum Logic**: Implements `.tail()` and `.mean()` operations over sorted time-series data to provide accurate trend analysis.
3. **Storage & I/O**: Automated hierarchy of reports organized by date and matchup using `Pathlib` for cross-platform compatibility.

---

### 🔄 Data Flow Pipeline

1. **Ingestion**: Fetching live season schedules and team IDs via MLB API.
2. **Processing**: Normalizing game records and applying statistical rolling windows.
3. **Analysis**: Executing Head-to-Head win-loss logic and run-average calculations.
4. **Delivery**: Exporting timestamped, human-readable scouting reports in `/reports`.

---

### 📂 Repository Structure
```text
Major-League-Insights-MLI/
├── reports/            # Auto-generated daily matchups (.txt)
├── main.py             # Analytics engine & Rolling windows logic
├── requirements.txt    # Data stack (Pandas, Statsapi)
└── LICENSE             # MIT License
```

---

### 📊 Sample Intelligence Report
The engine outputs structured scouting reports for immediate analysis:
```text
============================================================
 MAJOR LEAGUE INSIGHTS: YANKEES vs DODGERS 
============================================================

--- LEAGUE RUN AVERAGES (TOTAL) ---
Yankees: All: 9.12 | L15: 10.40 | L10: 11.20 | L5: 9.80
Dodgers: All: 8.45 | L15: 7.90  | L10: 8.10  | L5: 8.60

--- HEAD-TO-HEAD (H2H) HISTORY ---
Combined Total Avg : L10: 9.50, L5: 10.20
Yankees W-L        : L10: 6-4, L5: 4-1
```

---

---

### 🚀 Setup & Execution

1. **Install Dependencies:**
```bash
pip install pandas statsapi
```

2. **Run Daily Analysis:**
```bash
python main.py
```

*The system will automatically detect today's games and generate reports in the `/reports` folder.*

---

### 🧠 Engineering Mindset: Why MLI?
Traditional sports apps show you the "what" (scores). MLI shows you the "how" and "why" by applying **Data Engineering** principles to sports. It demonstrates:
1. **Handling of Large-Scale Datasets:** Processing thousands of season games in seconds using vectorized operations.
2. **Feature Engineering:** Creating new metrics (Rolling Averages) from raw game scores to identify performance momentum.
3. **Real-world API Integration:** Mastering complex third-party endpoints to build a reliable and automated data tool.

---
<p align="center">
  <b>Developed by Daniel Godoy</b><br>
  <i>Data Engineer & Python Specialist | MLB Analytics Enthusiast</i>
</p>

> [!NOTE]
> This tool is intended for research purposes. It is an independent project and is not affiliated with Major League Baseball (MLB).