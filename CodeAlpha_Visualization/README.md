# 🤖 AI Job Market & Career Intelligence Platform (v2.0 NextGen)

An enterprise-grade, end-to-end Machine Learning web application for AI job market intelligence, salary prediction, career path simulations, and skill gap analysis.

---

## 🌟 Key Features

### 1. 📊 Executive Market Intelligence Dashboard (`/`)
- **Real-Time KPIs**: Total Job Postings, Average Salary, 50th Percentile Median, Peak Offering, Global Remote %, and Country Counts.
- **6 Interactive Plotly Visualizations**:
  - Global AI Hiring Hubs & Average Compensation.
  - Salary Distribution Histogram with Percentile Boxplots & Median Annotations.
  - Top 10 In-Demand AI Skills by frequency.
  - Seniority Wage Curve (Entry $\to$ Mid $\to$ Senior $\to$ Executive).
  - Top Industries Market Share (Donut Chart).
  - Remote Work Arrangement vs. Average Pay Breakdown.
- **Live Search Feed**: Instant tabular filter across active job listings.

### 2. 🪄 AI Salary Predictor & Career Simulator (`/predictor`)
- **Multi-Model Regression Suite**: Supports **Random Forest**, **Gradient Boosting**, **Decision Tree**, and **Ridge Regression**.
- **Confidence Bounds**: Calculates realistic salary ranges ($\pm \text{MAE}$) for transparent estimation.
- **Feature Contribution Explainability**: Visualizes the percentage influence of Role, Experience, Location, Company Size, and Remote Status.
- **What-If Career Uplift Simulator**: Projects compensation increases for Seniority Promotions, Remote Work Transitions, Geographic Arbitrage (e.g. US/Swiss contracts), and Role Pivots.

### 3. 🎯 AI Skills Gap & Resume Matcher (`/skills`)
- **Interactive Competency Selector**: One-click skill tags or raw text/resume parser.
- **Role Compatibility Score**: Quantifies match percentage against industry standards.
- **Missing High-Impact Skills**: Identifies critical skills and calculates estimated market value boost.
- **30-60-90 Day Personalized Learning Roadmap**: Structured 3-phase curriculum tailored to your career transition.

### 4. ⚖️ Side-by-Side Benchmark Comparator (`/compare`)
- Compare **Role vs. Role** (e.g. Data Scientist vs. AI Research Scientist) or **Country vs. Country** (e.g. United States vs. Germany).
- Side-by-side metric cards: Median Salary, Interquartile Range (25th - 75th percentile), Remote Opportunity Rate, and Core Tech Stack overlap.

### 5. 🔍 Filterable Live Job Board (`/jobs`)
- Multi-faceted filter sidebar: Role, Country, Experience Tier, Remote Arrangement, and Interactive Salary Slider.
- Instant search, pagination, and persistent **Save/Bookmark** features.

### 6. 🧠 ML Model Transparency Lab (`/models`)
- Live model leaderboard ranking **Random Forest**, **Gradient Boosting**, **Decision Tree**, and **Ridge Regression** on $R^2$ accuracy, MAE, RMSE, and training latency.

### 7. 💬 Interactive AI Career Copilot ("Aria")
- Floating intelligent assistant providing real-time advice on salary negotiation, high-growth AI roles, and career pivots.

### 8. 🔌 Developer REST API & Sandbox (`/api-docs`)
- Full suite of JSON REST endpoints with an interactive in-browser Swagger-like testing console.

---

## 🛠️ Tech Stack & Architecture

- **Backend**: Python 3, Flask
- **Machine Learning**: Scikit-Learn (Random Forest, Gradient Boosting, Decision Tree, Ridge)
- **Data Engineering**: Pandas, NumPy
- **Visualizations**: Plotly.js, Plotly Express
- **Frontend**: Bootstrap 5.3, FontAwesome 6, Modern Glassmorphism CSS, Vanilla JS
- **Theme**: Persistent Dark / Light Mode

---

## 🚀 Getting Started

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python app.py
```

### 3. Open in Browser
Visit `http://127.0.0.1:5000` in your web browser.

---

## 📡 REST API Reference

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/api/predict` | `POST` | Predict expected salary with confidence interval & feature weights |
| `/api/simulate` | `POST` | Forecast salary uplifts for career scenarios |
| `/api/skills/match` | `POST` | Calculate skill compatibility & 90-day learning roadmap |
| `/api/market-stats` | `GET` | Retrieve global market summary metrics & top roles |
| `/api/advisor` | `POST` | Query the AI Career Copilot |
