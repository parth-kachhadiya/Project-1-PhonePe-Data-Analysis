# **📊 PhonePe Pulse Interactive Dashboard**

An advanced interactive business intelligence dashboard built using **Python**, **Streamlit**, **Plotly**, and **Pandas** to analyze PhonePe Pulse data across user growth, transaction behavior, regional adoption, insurance ecosystem, and strategic business insights.

---

# 🚀 Project Overview

This project transforms raw PhonePe Pulse datasets into a fully interactive analytics dashboard capable of:

- tracking platform growth
- analyzing user engagement
- understanding transaction behavior
- identifying regional adoption trends
- exploring insurance ecosystem growth
- detecting strategic opportunities and anomalies

The dashboard is designed with:
- modular architecture
- dynamic drill-down exploration
- interactive visualizations
- business storytelling
- recruiter-friendly UI/UX

---

# 🧠 Key Features

## ✅ Interactive Dashboard
Built using Streamlit with:
- dynamic filters
- drill-down exploration
- responsive layout
- interactive Plotly charts

---

## ✅ Business Intelligence Focus
The dashboard is not just descriptive analytics.

It focuses on:
- growth analysis
- engagement analysis
- behavioral insights
- hotspot detection
- strategic opportunities
- anomaly detection

---

## ✅ Modular Architecture
The project follows a scalable section-wise architecture.

```text
Project-1 PhonePe Data Analysis/
│
├── CSVs/
|   ├── Aggregated_insurance.csv
|   ├── Aggregated_transaction.csv
|   ├── Aggregated_user.csv
|   ├── Map_insurance.csv
|   ├── Map_map.csv
|   ├── Map_user.csv
|   ├── Top_insurance.csv
|   ├── Top_map.csv
|   └── Top_top.csv
|
├── dashboard/
|   ├── sections/
│   |    ├── section1_platform_growth.py
│   |    ├── section2_user_behavior.py
│   |    ├── section3_regional_adoption.py
│   |    ├── section4_insurance_ecosystem.py
│   |    └── section5_strategic_insights.py
│   |
|   ├── utils/
|   |    └── preprocessing.py
|   |
|   └── app.py
|
├── database/
│   └── phonepe_data.db
│
├── jupyter_notebooks/
|   ├── utils/
|   |    └── Graph_Helpers
|   |         ├── insuranceGrowth.py
|   |         ├── platformGrowth.py
|   |         ├── regionHelper.py
|   |         ├── strategicInsights.py
|   |         └── userPaymentBehaviour.py
|   |
|   ├── insuranceGrowth.ipynb
|   ├── Platform-Growth-Analysis.ipynb
|   ├── regionAnalysis.ipynb
|   ├── strategicInsights.ipynb
|   └── userPaymentBehaviour.ipynb
|   
├── app.py
├── generate_CSVs_from_db.py
├── extract_to_db.py
└── README.md
```

---

# 📌 Dashboard Sections

# SECTION 1 — PhonePe Platform Growth

Analyze overall platform expansion across India.

### Included Analysis
- User Growth Trend
- Transaction Growth Trend
- Year-over-Year (YoY) Growth
- Quarter-over-Quarter (QoQ) Growth

### Key Insights
- Platform scalability
- Transaction acceleration
- User adoption trends

---

# SECTION 2 — User & Payment Behavior

Understand how users interact with PhonePe.

### Included Analysis
- Transaction Type Analysis
- Average Transaction Value (ATV)
- Budget vs Premium Smartphone Adoption
- User Engagement Trend

### Key Insights
- Dominant payment categories
- Spending behavior
- Smartphone ecosystem analysis
- User interaction patterns

---

# SECTION 3 — Regional Adoption

Analyze state-wise and district-wise adoption.

### Included Analysis
- Top Performing States
- Top Performing Districts
- Emerging Growth Districts
- Engagement Ratio Analysis
- Growth Hotspots
- Interactive State District Explorer

### Key Insights
- Regional penetration
- Emerging markets
- User engagement by region
- Adoption hotspots

---

# SECTION 4 — Insurance Ecosystem

Explore insurance adoption through PhonePe.

### Included Analysis
- Insurance Transaction Growth
- Insurance Amount Growth
- Insurance ATV Analysis
- Insurance Penetration Analysis
- Hot Quarter of Buying Insurance
- Interactive Insurance State Explorer

### Key Insights
- Insurance adoption growth
- Regional insurance penetration
- Quarterly buying patterns
- State-wise insurance trends

---

# SECTION 5 — Strategic Insights

Business-focused strategic intelligence layer.

### Included Analysis
- Potential User Segments
- Potential Growth Regions
- Unusual Transaction Pattern Detection
- High-Value vs High-Frequency Regions

### Key Insights
- Engagement gaps
- Hidden growth opportunities
- Premium transaction regions
- Anomaly detection

---

# 📈 Interactive Features

The dashboard includes:
- dynamic state selection
- district-level drilldowns
- hover insights
- zoomable charts
- runtime graph updates
- interactive exploration modules

---

# 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core Programming |
| Streamlit | Interactive Dashboard |
| Plotly | Interactive Visualizations |
| Pandas | Data Processing |
| NumPy | Numerical Operations |

---

# 📂 Datasets Used

The project uses multiple PhonePe Pulse datasets including:

- Aggregated User
- Aggregated Transaction
- Aggregated Insurance
- Map User
- Map Transaction
- Map Insurance
- Top Insurance
- Top Map
- Top User

---

# ⚠️ Important Data Handling Rules

## 1. India Rows
Rows where:
```python
State == 'India'
```

represent nationwide aggregated statistics.

These rows are:
- included for national analysis
- excluded for regional analysis

---

## 2. Aggregated User Table
`Registered_users` and `App_opens` are repeated across brands.

Therefore:
```python
MAX()
```
aggregation is used instead of `SUM()`.

---

## 3. Map User Table
`Registered_users` and `App_opens` are district-level observations.

Therefore:
```python
SUM()
```
aggregation is used.

---

## 4. Missing App Opens
In `map_user`:

From:
- 2018-Q1 → 2019-Q1

`App_opens = 0`

is treated as:
```python
NaN
```

instead of actual zero engagement.

---

# ▶️ How to Run the Project

## 1. Clone Repository

```bash
git clone <your_repo_url>
```

---

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 3. Run Streamlit App

```bash
streamlit run app.py
```

---

# 📸 Dashboard Preview

## Features Included
- KPI Cards
- Interactive Charts
- Dynamic Explorers
- Section-wise Analytics
- Drill-down Analysis
- Business Insights

---

# 🎯 Project Goals

This project aims to demonstrate:
- advanced data analysis
- business intelligence dashboarding
- interactive visualization design
- analytical storytelling
- modular dashboard architecture

---

# 📌 Future Improvements

Potential future enhancements:
- Geo-spatial map visualizations
- Forecasting models
- Machine learning insights
- User segmentation clustering
- Real-time API integration
- Advanced filtering system

---

# 👨‍💻 Author

Developed as an end-to-end interactive analytics and business intelligence project using PhonePe Pulse data.

---

# ⭐ Final Note

This project combines:
- data analytics
- interactive visualization
- business intelligence
- dashboard engineering

to create a production-style analytical application capable of generating actionable insights from large-scale financial transaction datasets.
