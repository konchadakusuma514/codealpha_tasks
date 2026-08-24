# 🛡️ CyberShield Global SOC Analytics & Threat Intelligence Platform
> **Enterprise Exploratory Data Analysis (EDA) & Machine Learning Platform for Cybersecurity Intelligence (2015–2024)**

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python)](https://www.python.org/)
[![Streamlit App](https://img.shields.io/badge/Streamlit-App-FF4B4B.svg?logo=streamlit)](https://streamlit.io/)
[![Plotly Interactive](https://img.shields.io/badge/Plotly-Interactive%20Charts-3F4F75.svg?logo=plotly)](https://plotly.com/)
[![Scikit-Learn ML](https://img.shields.io/badge/Scikit--Learn-Machine%20Learning-F7931E.svg?logo=scikitlearn)](https://scikit-learn.org/)

---

## 📌 Project Overview
CyberShield is a comprehensive **Exploratory Data Analysis (EDA)** and **Threat Intelligence Web Application** built for enterprise security operations centers (SOC) and cybersecurity analysts. 

The platform analyzes **3,500 enterprise security incidents** across 10 global regions and 7 critical infrastructure sectors between 2015 and 2024, uncovering multi-dimensional threat dynamics, quantifying financial exposure, evaluating defense mechanisms, and deploying predictive machine learning impact models.

---

## 🌟 Key Features & Innovations

### 1. 🔍 Advanced Domain Feature Engineering
- **Risk Severity Index (RSI: 0–100)**: A composite multi-factor score balancing Financial Loss (40%), Affected User Base (35%), and Incident Resolution Time (25%).
- **Cost per Compromised User ($/User)**: Normalizes damage relative to enterprise size and affected customer base.
- **Incident Financial Velocity ($M / Hour)**: Quantifies the financial burn rate during active incident triage.
- **Severity Tier Classification**: Categorizes threats into Tier 1 (Low) through Tier 4 (Critical).

### 2. 🌀 Attack Pipeline & Sankey Vector Analysis
- Multi-tier **Sankey Flow Diagram** tracing the complete attack chain:
  $$\text{Threat Actor} \longrightarrow \text{Vulnerability} \longrightarrow \text{Attack Vector} \longrightarrow \text{Defense} \longrightarrow \text{Target Sector}$$
- Multi-level **Sunburst & Treemap Visualizations** for hierarchical industry drill-downs.

### 3. 🔬 Inferential Statistics & Hypothesis Testing
- **One-Way ANOVA**: Formally testing whether Defense Mechanisms produce statistically significant reductions in incident resolution time ($p < 0.05$).
- **Chi-Square Test of Independence**: Testing associative patterns between Threat Actor Groups and Exploited Vulnerability Types.
- **Pearson & Spearman Correlation Heatmaps**: Identifying relationships among engineered metrics.

### 4. 🤖 Machine Learning Impact Simulator
- Live-trained **Random Forest Regressors** predicting:
  - Estimated Financial Loss ($ Millions) with 85% confidence intervals.
  - Incident Resolution Time (Hours).
- Automated **Feature Importance Attribution** highlighting the primary drivers of financial damage.

### 5. 🛡️ SOC Intelligent Defense Strategy Advisor
- Recommends the highest-ROI defense mechanism for specific industries and attack profiles based on historical mitigation efficacy scores.

### 6. 🚨 Unsupervised Anomaly Detection (Isolation Forest)
- Automatically flags outlier "Black Swan" cyber events featuring catastrophic losses and unprecedented downtime.

---

## 📂 Project Architecture

```
cybershield-eda/
├── dataset/
│   └── Global_Cybersecurity_Threats_2015-2024.csv   # Cleaned 3,500 incident records
├── src/
│   ├── __init__.py
│   ├── data_processor.py      # Feature engineering & RSI calculation
│   ├── statistical_tests.py   # ANOVA, Chi-Square & correlation engines
│   ├── ml_engine.py           # Random Forest ML impact predictor
│   ├── defense_advisor.py     # Heuristic defense recommendation engine
│   └── anomaly_detector.py    # Isolation Forest anomaly detection
├── app.py                     # Master Streamlit SOC Dashboard
├── eda_cybersecurity_report.ipynb # Complete Jupyter Notebook for submission
├── create_notebook.py         # Notebook generator utility
├── requirements.txt           # Python dependencies
├── DEPLOYMENT_GUIDE.md        # Step-by-step free web hosting instructions
├── INTERNSHIP_PRESENTATION_GUIDE.md # Interview defense & presentation talking points
└── README.md                  # Project documentation
```

---

## 🚀 Quick Start Guide

### 1. Clone or Open the Repository
```bash
git clone https://github.com/your-username/cybershield-eda.git
cd cybershield-eda
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Streamlit SOC Web Application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 🌐 Free Cloud Deployment (Streamlit Community Cloud)
You can deploy this dashboard to the web for free in 2 minutes so your internship evaluator can interact with it live:
1. Push this project to GitHub.
2. Visit [share.streamlit.io](https://share.streamlit.io) and link your GitHub account.
3. Select your repository, set the main file path to `app.py`, and click **Deploy**!
*(See `DEPLOYMENT_GUIDE.md` for detailed instructions).*

---

## 👤 Author & Credits
- **Author:** Kusuma
- **Project:** Task 2 (Exploratory Data Analysis)
- **Domain:** Cybersecurity & SOC Threat Intelligence
