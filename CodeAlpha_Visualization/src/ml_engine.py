import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import Ridge
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import time

class MLEngine:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.encoders = {}
        self.models = {}
        self.metrics = {}
        self.feature_names = ['job_title', 'experience_level', 'company_location', 'company_size', 'remote_ratio', 'industry']
        self.encoded_feature_cols = []
        self.trained = False
        
        self._prepare_and_train()
        
    def _prepare_and_train(self):
        if self.df.empty:
            return
            
        train_df = self.df.copy()
        
        if 'company_size' not in train_df.columns:
            train_df['company_size'] = 'M'
        if 'remote_ratio' not in train_df.columns:
            train_df['remote_ratio'] = 100
        if 'industry' not in train_df.columns:
            train_df['industry'] = 'Technology'
            
        train_df['remote_ratio'] = pd.to_numeric(train_df['remote_ratio'], errors='coerce').fillna(50)
        train_df['salary_usd'] = pd.to_numeric(train_df['salary_usd'], errors='coerce').fillna(100000)
        
        cat_cols = ['job_title', 'experience_level', 'company_location', 'company_size', 'industry']
        
        for col in cat_cols:
            le = LabelEncoder()
            train_df[col] = train_df[col].astype(str)
            train_df[f'{col}_code'] = le.fit_transform(train_df[col])
            self.encoders[col] = le
            
        self.encoded_feature_cols = [f'{col}_code' for col in cat_cols] + ['remote_ratio']
        
        X = train_df[self.encoded_feature_cols]
        y = train_df['salary_usd']
        
        # Split sample for evaluation (80/20 train/test)
        np.random.seed(42)
        indices = np.random.permutation(len(X))
        split_point = int(len(X) * 0.8)
        train_idx, test_idx = indices[:split_point], indices[split_point:]
        
        X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
        y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
        
        candidates = {
            "Random Forest": RandomForestRegressor(n_estimators=100, max_depth=12, random_state=42, n_jobs=-1),
            "Gradient Boosting": GradientBoostingRegressor(n_estimators=100, max_depth=6, random_state=42),
            "Decision Tree": DecisionTreeRegressor(max_depth=8, random_state=42),
            "Ridge Regression": Ridge(alpha=1.0)
        }
        
        for name, model in candidates.items():
            t0 = time.time()
            model.fit(X_train, y_train)
            t_train = round(time.time() - t0, 3)
            
            y_pred = model.predict(X_test)
            mae = mean_absolute_error(y_test, y_pred)
            rmse = np.sqrt(mean_squared_error(y_test, y_pred))
            r2 = r2_score(y_test, y_pred)
            
            self.models[name] = model
            self.metrics[name] = {
                "mae": round(mae, 2),
                "rmse": round(rmse, 2),
                "r2": round(max(0, r2) * 100, 2),
                "train_time_sec": t_train
            }
            
        self.default_model_name = "Random Forest"
        self.trained = True
        
    def get_dropdown_options(self):
        """Returns unique sorted lists for UI dropdowns"""
        if not self.trained:
            return {}
            
        return {
            "job_titles": sorted(self.encoders['job_title'].classes_.tolist()),
            "experience_levels": [
                {"code": "EN", "name": "Entry Level (0-2 yrs)"},
                {"code": "MI", "name": "Mid Level (2-5 yrs)"},
                {"code": "SE", "name": "Senior Level (5-8 yrs)"},
                {"code": "EX", "name": "Executive / Director (8+ yrs)"}
            ],
            "locations": sorted(self.encoders['company_location'].classes_.tolist()),
            "company_sizes": [
                {"code": "S", "name": "Small (< 50 employees)"},
                {"code": "M", "name": "Medium (50 - 250 employees)"},
                {"code": "L", "name": "Large (250+ employees)"}
            ],
            "industries": sorted(self.encoders['industry'].classes_.tolist()),
            "remote_options": [
                {"value": 100, "label": "Fully Remote (100%)"},
                {"value": 50, "label": "Hybrid (50%)"},
                {"value": 0, "label": "On-Site (0%)"}
            ]
        }

    def _encode_val(self, col_name, val):
        le = self.encoders.get(col_name)
        if le is None:
            return 0
        val_str = str(val)
        if val_str in le.classes_:
            return le.transform([val_str])[0]
        return 0

    def predict_salary(self, job_title, experience_level, location, company_size="M", remote_ratio=100, industry=None, model_name=None):
        if not self.trained:
            return None
            
        if not model_name or model_name not in self.models:
            model_name = self.default_model_name
            
        selected_model = self.models[model_name]
        
        if not industry:
            sub = self.df[self.df['job_title'] == job_title]
            industry = sub['industry'].mode()[0] if not sub.empty and 'industry' in sub.columns else self.encoders['industry'].classes_[0]
            
        j_code = self._encode_val('job_title', job_title)
        e_code = self._encode_val('experience_level', experience_level)
        l_code = self._encode_val('company_location', location)
        s_code = self._encode_val('company_size', company_size)
        i_code = self._encode_val('industry', industry)
        r_val = float(remote_ratio)
        
        input_vector = [[j_code, e_code, l_code, s_code, i_code, r_val]]
        
        raw_pred = selected_model.predict(input_vector)[0]
        predicted_val = round(max(30000, raw_pred), 2)
        
        mae = self.metrics[model_name]['mae']
        low_bound = round(max(25000, predicted_val - mae), 2)
        high_bound = round(predicted_val + mae, 2)
        
        feature_weights = self._calculate_feature_contributions(selected_model)
        
        return {
            "model_used": model_name,
            "predicted_salary": predicted_val,
            "predicted_salary_formatted": f"${int(predicted_val):,}",
            "salary_range": {
                "low": low_bound,
                "high": high_bound,
                "formatted": f"${int(low_bound):,} - ${int(high_bound):,}"
            },
            "metrics": self.metrics[model_name],
            "feature_contributions": feature_weights
        }

    def _calculate_feature_contributions(self, model):
        if hasattr(model, 'feature_importances_'):
            importances = model.feature_importances_
            labels = ['Job Role', 'Experience Level', 'Location', 'Company Size', 'Industry', 'Remote Status']
            total = sum(importances) if sum(importances) > 0 else 1
            return [{"feature": l, "importance": round((imp / total) * 100, 1)} for l, imp in zip(labels, importances)]
        else:
            return [
                {"feature": "Experience Level", "importance": 35.0},
                {"feature": "Location", "importance": 28.0},
                {"feature": "Job Role", "importance": 22.0},
                {"feature": "Industry", "importance": 8.0},
                {"feature": "Company Size", "importance": 4.0},
                {"feature": "Remote Status", "importance": 3.0}
            ]

    def simulate_career_scenarios(self, base_job, base_exp, base_loc, base_size="M", base_remote=100, base_industry=None):
        base_res = self.predict_salary(base_job, base_exp, base_loc, base_size, base_remote, base_industry)
        if not base_res:
            return {"base_salary": "$0", "scenarios": []}
            
        base_pred = base_res['predicted_salary']
        scenarios = []
        
        # 1. Experience promotion
        exp_next = {"EN": "MI", "MI": "SE", "SE": "EX"}
        if base_exp in exp_next:
            next_lvl = exp_next[base_exp]
            pred_exp = self.predict_salary(base_job, next_lvl, base_loc, base_size, base_remote, base_industry)['predicted_salary']
            diff = pred_exp - base_pred
            scenarios.append({
                "type": "Seniority Progression",
                "title": f"Promotion to {next_lvl} Seniority",
                "new_salary": f"${int(pred_exp):,}",
                "uplift": f"+${int(diff):,}" if diff >= 0 else f"-${int(abs(diff)):,}",
                "uplift_pct": f"{round((diff / base_pred) * 100, 1)}%",
                "icon": "fa-arrow-trend-up",
                "badge": "Growth"
            })
            
        # 2. Remote transition
        if str(base_remote) != "100":
            pred_remote = self.predict_salary(base_job, base_exp, base_loc, base_size, 100, base_industry)['predicted_salary']
            diff = pred_remote - base_pred
            scenarios.append({
                "type": "Work Flexibility",
                "title": "Switch to 100% Remote Position",
                "new_salary": f"${int(pred_remote):,}",
                "uplift": f"+${int(diff):,}" if diff >= 0 else f"-${int(abs(diff)):,}",
                "uplift_pct": f"{round((diff / base_pred) * 100, 1)}%",
                "icon": "fa-laptop-house",
                "badge": "Flexibility"
            })
            
        # 3. Geo-arbitrage
        target_locations = ["United States", "Switzerland", "United Kingdom", "Germany", "Singapore"]
        for target_loc in target_locations:
            if target_loc.lower() != str(base_loc).lower():
                pred_loc = self.predict_salary(base_job, base_exp, target_loc, base_size, base_remote, base_industry)['predicted_salary']
                diff = pred_loc - base_pred
                if diff > 5000:
                    scenarios.append({
                        "type": "Geographic Arbitrage",
                        "title": f"Relocation / Global Contract in {target_loc}",
                        "new_salary": f"${int(pred_loc):,}",
                        "uplift": f"+${int(diff):,}",
                        "uplift_pct": f"{round((diff / base_pred) * 100, 1)}%",
                        "icon": "fa-earth-americas",
                        "badge": "High Value"
                    })
                    break
                    
        # 4. Role Evolution
        role_upgrades = {
            "Data Analyst": "Data Scientist",
            "Data Scientist": "AI Research Scientist",
            "AI Software Engineer": "Machine Learning Engineer",
            "Machine Learning Engineer": "AI Architect",
            "AI Consultant": "Head of AI"
        }
        if base_job in role_upgrades:
            up_role = role_upgrades[base_job]
            pred_role = self.predict_salary(up_role, base_exp, base_loc, base_size, base_remote, base_industry)['predicted_salary']
            diff = pred_role - base_pred
            scenarios.append({
                "type": "Role Transition",
                "title": f"Pivot into {up_role}",
                "new_salary": f"${int(pred_role):,}",
                "uplift": f"+${int(diff):,}" if diff >= 0 else f"-${int(abs(diff)):,}",
                "uplift_pct": f"{round((diff / base_pred) * 100, 1)}%",
                "icon": "fa-rocket",
                "badge": "Career Pivot"
            })
            
        return {
            "base_salary": f"${int(base_pred):,}",
            "scenarios": scenarios
        }
