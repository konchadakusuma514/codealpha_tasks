# 🌐 Complete Step-by-Step Cloud Deployment Guide
## How to Host Your CyberShield Dashboard Online for Free (Shareable URL)

This guide shows you how to host your Streamlit Web Application on **Streamlit Community Cloud** (100% free, forever, with your own public `.streamlit.app` link) so you can share it with your internship mentors, recruiters, and LinkedIn connections.

---

### ⏱️ Prerequisites (Takes ~3 minutes)
1. A free account on [GitHub.com](https://github.com).
2. A free account on [Streamlit Community Cloud](https://share.streamlit.io).

---

### Step 1: Upload Your Project to GitHub

1. Open your terminal in the project folder:
   ```bash
   cd "C:\Users\Konchada Kusuma\.gemini\antigravity\scratch\cybershield-eda"
   ```

2. Initialize Git and commit the files:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: CyberShield SOC Analytics EDA Platform"
   ```

3. Create a new repository on GitHub:
   - Go to [github.com/new](https://github.com/new).
   - Repository name: `cybershield-eda` (or `cybersecurity-threat-eda`).
   - Keep it **Public**.
   - Click **Create repository**.

4. Push your code to GitHub:
   ```bash
   git remote add origin https://github.com/<YOUR_GITHUB_USERNAME>/cybershield-eda.git
   git branch -M main
   git push -u origin main
   ```

---

### Step 2: Deploy to Streamlit Community Cloud (1-Click)

1. Go to [share.streamlit.io](https://share.streamlit.io) and log in with your GitHub account.
2. Click **"New app"** (or **"Create app"**).
3. Fill in the three fields:
   - **Repository:** `<YOUR_GITHUB_USERNAME>/cybershield-eda`
   - **Branch:** `main`
   - **Main file path:** `app.py`
4. Click **"Deploy!"** 🚀

Streamlit will automatically detect `requirements.txt`, install all libraries (pandas, plotly, scikit-learn, scipy), and launch your dashboard at a live URL like:
`https://cybershield-soc.streamlit.app`

---

### Step 3: Add the Live Link to Your Internship Submission & Resume
- In your internship report or email submission, add:
  > **Live Interactive SOC Dashboard:** [https://your-app-name.streamlit.app](https://your-app-name.streamlit.app)  
  > **GitHub Repository & Notebook:** [https://github.com/your-username/cybershield-eda](https://github.com/your-username/cybershield-eda)
