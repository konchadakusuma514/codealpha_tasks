from flask import Flask, render_template, Response, request, jsonify
import pandas as pd
import numpy as np
import os
import io

# Import custom modular engines
from src.ml_engine import MLEngine
from src.skill_analyzer import SkillAnalyzer
from src.comparator import BenchmarkComparator
from src.analytics import AnalyticsEngine
from src.ai_advisor import AIAdvisor

app = Flask(__name__)
app.secret_key = "ai_job_intelligence_secret_key_2026"

# -------------------------------------------------------------
# 1. Setup & Load Data
# -------------------------------------------------------------
DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "ai_job_dataset.csv")

try:
    df = pd.read_csv(DATA_PATH)
    df.fillna("Not Available", inplace=True)
    DATA_LOADED = True
    print(f"✅ Loaded dataset: {len(df):,} records.")
except Exception as e:
    print(f"❌ Error loading dataset: {e}")
    DATA_LOADED = False
    df = pd.DataFrame()

# Initialize Backend Engines
if DATA_LOADED and not df.empty:
    ml_engine = MLEngine(df)
    skill_analyzer = SkillAnalyzer(df)
    comparator = BenchmarkComparator(df)
    analytics_engine = AnalyticsEngine(df)
    advisor = AIAdvisor(df)
else:
    ml_engine = None
    skill_analyzer = None
    comparator = None
    analytics_engine = None
    advisor = None

# -------------------------------------------------------------
# 2. Web Routes
# -------------------------------------------------------------
@app.route("/")
def home():
    """Executive Intelligence Dashboard"""
    if not DATA_LOADED:
        return render_template("index.html", error="Dataset not found in data/ directory.")
        
    g1, g2, g3, g4, g5, g6 = analytics_engine.generate_dashboard_charts()
    recent_jobs = df.head(12).to_dict(orient="records")
    
    # Calculate market summary KPIs
    total_jobs = len(df)
    avg_salary = int(df['salary_usd'].mean())
    highest_salary = int(df['salary_usd'].max())
    median_salary = int(df['salary_usd'].median())
    total_companies = df['company_name'].nunique() if 'company_name' in df.columns else 0
    total_countries = df['company_location'].nunique()
    total_industries = df['industry'].nunique() if 'industry' in df.columns else 0
    
    # Remote ratio calculation
    if 'remote_ratio' in df.columns:
        remote_numeric = pd.to_numeric(df['remote_ratio'], errors='coerce').fillna(0)
        remote_pct = round((remote_numeric >= 50).mean() * 100, 1)
    else:
        remote_pct = 45.0
        
    return render_template(
        "index.html",
        active_page="home",
        total_jobs=f"{total_jobs:,}",
        average_salary=f"{avg_salary:,}",
        median_salary=f"{median_salary:,}",
        highest_salary=f"{highest_salary:,}",
        total_companies=f"{total_companies:,}",
        total_countries=f"{total_countries:,}",
        total_industries=f"{total_industries:,}",
        remote_pct=remote_pct,
        jobs=recent_jobs,
        graph1=g1, graph2=g2, graph3=g3, graph4=g4, graph5=g5, graph6=g6
    )

@app.route("/dashboard", methods=["GET", "POST"])
@app.route("/predictor", methods=["GET", "POST"])
def predictor():
    """AI Salary Predictor & What-If Scenario Simulator"""
    dropdowns = ml_engine.get_dropdown_options() if ml_engine else {}
    prediction_result = None
    scenario_result = None
    
    form_data = {
        "job_title": "",
        "experience_level": "MI",
        "location": "",
        "company_size": "M",
        "remote_ratio": "100",
        "industry": "",
        "model_name": "Random Forest"
    }

    if request.method == "POST" and ml_engine:
        form_data["job_title"] = request.form.get("job_title", "")
        form_data["experience_level"] = request.form.get("experience_level", "MI")
        form_data["location"] = request.form.get("location", "")
        form_data["company_size"] = request.form.get("company_size", "M")
        form_data["remote_ratio"] = request.form.get("remote_ratio", "100")
        form_data["industry"] = request.form.get("industry", "")
        form_data["model_name"] = request.form.get("model_name", "Random Forest")
        
        try:
            prediction_result = ml_engine.predict_salary(
                job_title=form_data["job_title"],
                experience_level=form_data["experience_level"],
                location=form_data["location"],
                company_size=form_data["company_size"],
                remote_ratio=form_data["remote_ratio"],
                industry=form_data["industry"],
                model_name=form_data["model_name"]
            )
            
            scenario_result = ml_engine.simulate_career_scenarios(
                base_job=form_data["job_title"],
                base_exp=form_data["experience_level"],
                base_loc=form_data["location"],
                base_size=form_data["company_size"],
                base_remote=form_data["remote_ratio"],
                base_industry=form_data["industry"]
            )
        except Exception as e:
            prediction_result = {"error": f"Prediction failed: {str(e)}"}

    return render_template(
        "dashboard.html",
        active_page="predictor",
        dropdowns=dropdowns,
        available_models=list(ml_engine.models.keys()) if ml_engine else [],
        form_data=form_data,
        prediction=prediction_result,
        scenarios=scenario_result
    )

@app.route("/skills", methods=["GET", "POST"])
def skills():
    """AI Skills Gap, Resume Matcher & 30-60-90 Day Roadmap"""
    dropdowns = ml_engine.get_dropdown_options() if ml_engine else {}
    available_skills = skill_analyzer.get_all_available_skills() if skill_analyzer else []
    result = None
    input_skills_str = ""
    target_role = ""

    if request.method == "POST" and skill_analyzer:
        raw_skills = request.form.get("user_skills", "")
        target_role = request.form.get("target_role", "")
        input_skills_str = raw_skills
        
        # Parse selected chips / text
        parsed_skills = skill_analyzer.parse_user_skills(raw_skills)
        result = skill_analyzer.evaluate_skills_gap(parsed_skills, target_role)

    return render_template(
        "skills.html",
        active_page="skills",
        available_skills=available_skills,
        job_titles=dropdowns.get("job_titles", []),
        result=result,
        input_skills_str=input_skills_str,
        target_role=target_role
    )

@app.route("/compare", methods=["GET", "POST"])
def compare():
    """Side-by-Side Role & Country Comparator"""
    dropdowns = ml_engine.get_dropdown_options() if ml_engine else {}
    comparison_type = request.form.get("compare_type", "role")
    
    val_a = request.form.get("item_a", "")
    val_b = request.form.get("item_b", "")
    comparison_data = None
    
    if request.method == "POST" and comparator:
        if comparison_type == "role":
            if not val_a and dropdowns.get("job_titles"):
                val_a = dropdowns["job_titles"][0]
            if not val_b and len(dropdowns.get("job_titles", [])) > 1:
                val_b = dropdowns["job_titles"][1]
            comparison_data = comparator.compare_roles(val_a, val_b)
        else:
            if not val_a and dropdowns.get("locations"):
                val_a = dropdowns["locations"][0]
            if not val_b and len(dropdowns.get("locations", [])) > 1:
                val_b = dropdowns["locations"][1]
            comparison_data = comparator.compare_locations(val_a, val_b)

    return render_template(
        "compare.html",
        active_page="compare",
        compare_type=comparison_type,
        job_titles=dropdowns.get("job_titles", []),
        locations=dropdowns.get("locations", []),
        val_a=val_a,
        val_b=val_b,
        comparison=comparison_data
    )

@app.route("/jobs")
def jobs():
    """Live Search & Multi-Faceted Filterable Job Board"""
    dropdowns = ml_engine.get_dropdown_options() if ml_engine else {}
    
    # Query parameters
    role_filter = request.args.get("role", "")
    loc_filter = request.args.get("location", "")
    exp_filter = request.args.get("experience", "")
    industry_filter = request.args.get("industry", "")
    remote_filter = request.args.get("remote", "")
    search_q = request.args.get("q", "").strip().lower()
    min_sal = request.args.get("min_salary", 0, type=int)
    
    filtered_df = df.copy() if DATA_LOADED else pd.DataFrame()
    
    if not filtered_df.empty:
        if role_filter:
            filtered_df = filtered_df[filtered_df['job_title'] == role_filter]
        if loc_filter:
            filtered_df = filtered_df[filtered_df['company_location'] == loc_filter]
        if exp_filter:
            filtered_df = filtered_df[filtered_df['experience_level'] == exp_filter]
        if industry_filter and 'industry' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['industry'] == industry_filter]
        if remote_filter and 'remote_ratio' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['remote_ratio'].astype(str) == str(remote_filter)]
        if min_sal > 0:
            filtered_df = filtered_df[pd.to_numeric(filtered_df['salary_usd'], errors='coerce') >= min_sal]
        if search_q:
            mask = (
                filtered_df['job_title'].astype(str).str.lower().str.contains(search_q) |
                filtered_df['company_location'].astype(str).str.lower().str.contains(search_q) |
                filtered_df['company_name'].astype(str).str.lower().str.contains(search_q) |
                filtered_df['required_skills'].astype(str).str.lower().str.contains(search_q)
            )
            filtered_df = filtered_df[mask]
            
    # Paginate (20 per page)
    page = request.args.get("page", 1, type=int)
    per_page = 20
    total_count = len(filtered_df)
    total_pages = max(1, (total_count + per_page - 1) // per_page)
    
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paged_jobs = filtered_df.iloc[start_idx:end_idx].to_dict(orient="records") if not filtered_df.empty else []
    
    return render_template(
        "jobs.html",
        active_page="jobs",
        jobs=paged_jobs,
        total_count=total_count,
        page=page,
        total_pages=total_pages,
        dropdowns=dropdowns,
        filters={
            "role": role_filter,
            "location": loc_filter,
            "experience": exp_filter,
            "industry": industry_filter,
            "remote": remote_filter,
            "q": search_q,
            "min_salary": min_sal
        }
    )

@app.route("/models")
def models_lab():
    """ML Model Benchmark & Transparency Lab"""
    metrics = ml_engine.metrics if ml_engine else {}
    return render_template(
        "models.html",
        active_page="models",
        metrics=metrics,
        dataset_size=f"{len(df):,}" if DATA_LOADED else "0",
        feature_names=ml_engine.feature_names if ml_engine else []
    )

@app.route("/api-docs")
def api_docs():
    """Interactive REST API Documentation & Playground"""
    dropdowns = ml_engine.get_dropdown_options() if ml_engine else {}
    return render_template(
        "api_docs.html",
        active_page="api_docs",
        dropdowns=dropdowns
    )

@app.route("/download")
def download_data():
    """Download dataset as CSV"""
    if not DATA_LOADED:
        return "No data available", 404
    csv_data = df.to_csv(index=False)
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=ai_job_market_report.csv"}
    )

# -------------------------------------------------------------
# 3. REST API Endpoints
# -------------------------------------------------------------
@app.route("/api/predict", methods=["POST"])
def api_predict():
    """
    JSON API for salary prediction.
    Accepts: {
        "job_title": "Data Scientist",
        "experience_level": "MI",
        "location": "United States",
        "company_size": "M",
        "remote_ratio": 100,
        "industry": "Technology",
        "model_name": "Random Forest"
    }
    """
    if not ml_engine:
        return jsonify({"status": "error", "message": "ML Engine not ready."}), 500
        
    try:
        data = request.get_json(force=True)
        res = ml_engine.predict_salary(
            job_title=data.get("job_title"),
            experience_level=data.get("experience_level", "MI"),
            location=data.get("location"),
            company_size=data.get("company_size", "M"),
            remote_ratio=data.get("remote_ratio", 100),
            industry=data.get("industry"),
            model_name=data.get("model_name", "Random Forest")
        )
        if not res:
            return jsonify({"status": "error", "message": "Prediction failed. Check input values."}), 400
            
        return jsonify({"status": "success", "data": res}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route("/api/simulate", methods=["POST"])
def api_simulate():
    """Simulate career moves and salary uplifts"""
    if not ml_engine:
        return jsonify({"status": "error", "message": "ML Engine not ready."}), 500
    try:
        data = request.get_json(force=True)
        res = ml_engine.simulate_career_scenarios(
            base_job=data.get("job_title"),
            base_exp=data.get("experience_level", "MI"),
            base_loc=data.get("location"),
            base_size=data.get("company_size", "M"),
            base_remote=data.get("remote_ratio", 100),
            base_industry=data.get("industry")
        )
        return jsonify({"status": "success", "data": res}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route("/api/skills/match", methods=["POST"])
def api_skills_match():
    """Skill gap analyzer endpoint"""
    if not skill_analyzer:
        return jsonify({"status": "error", "message": "Skill Analyzer not ready."}), 500
    try:
        data = request.get_json(force=True)
        raw_skills = data.get("skills", "")
        target_role = data.get("target_role", "")
        
        if isinstance(raw_skills, list):
            parsed = raw_skills
        else:
            parsed = skill_analyzer.parse_user_skills(str(raw_skills))
            
        res = skill_analyzer.evaluate_skills_gap(parsed, target_role)
        return jsonify({"status": "success", "data": res}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route("/api/advisor", methods=["POST"])
def api_advisor():
    """AI Career Advisor Chat Copilot"""
    if not advisor:
        return jsonify({"status": "error", "message": "Advisor not ready."}), 500
    try:
        data = request.get_json(force=True)
        user_query = data.get("query", "")
        answer = advisor.respond_to_query(user_query)
        return jsonify({"status": "success", "response": answer}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route("/api/market-stats", methods=["GET"])
def api_market_stats():
    """Market summary statistics"""
    if not DATA_LOADED:
        return jsonify({"status": "error", "message": "Data not loaded."}), 500
        
    return jsonify({
        "status": "success",
        "total_jobs": len(df),
        "average_salary_usd": round(df['salary_usd'].mean(), 2),
        "median_salary_usd": round(df['salary_usd'].median(), 2),
        "highest_salary_usd": round(df['salary_usd'].max(), 2),
        "unique_companies": int(df['company_name'].nunique()) if 'company_name' in df.columns else 0,
        "unique_countries": int(df['company_location'].nunique()),
        "top_roles": df['job_title'].value_counts().head(5).to_dict()
    }), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)