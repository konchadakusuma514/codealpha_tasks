import pandas as pd
import numpy as np

class BenchmarkComparator:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        
    def compare_roles(self, role_a: str, role_b: str):
        """Compare 2 job roles side-by-side on key metrics"""
        df_a = self.df[self.df['job_title'] == role_a]
        df_b = self.df[self.df['job_title'] == role_b]
        
        return {
            "entity_type": "Role",
            "item_a": self._compute_metrics(df_a, role_a),
            "item_b": self._compute_metrics(df_b, role_b)
        }

    def compare_locations(self, loc_a: str, loc_b: str):
        """Compare 2 countries/locations side-by-side"""
        df_a = self.df[self.df['company_location'] == loc_a]
        df_b = self.df[self.df['company_location'] == loc_b]
        
        return {
            "entity_type": "Location",
            "item_a": self._compute_metrics(df_a, loc_a),
            "item_b": self._compute_metrics(df_b, loc_b)
        }

    def _compute_metrics(self, sub_df: pd.DataFrame, label: str):
        if sub_df.empty:
            return {
                "name": label,
                "total_jobs": 0,
                "median_salary": "$0",
                "avg_salary": "$0",
                "min_salary": "$0",
                "max_salary": "$0",
                "q25_salary": "$0",
                "q75_salary": "$0",
                "remote_pct": "0%",
                "top_skills": [],
                "top_industries": []
            }
            
        salaries = pd.to_numeric(sub_df['salary_usd'], errors='coerce').dropna()
        median_sal = int(salaries.median()) if not salaries.empty else 0
        avg_sal = int(salaries.mean()) if not salaries.empty else 0
        min_sal = int(salaries.min()) if not salaries.empty else 0
        max_sal = int(salaries.max()) if not salaries.empty else 0
        q25_sal = int(salaries.quantile(0.25)) if not salaries.empty else 0
        q75_sal = int(salaries.quantile(0.75)) if not salaries.empty else 0
        
        # Remote percentage
        if 'remote_ratio' in sub_df.columns:
            remotes = pd.to_numeric(sub_df['remote_ratio'], errors='coerce').fillna(0)
            remote_pct = round((remotes >= 50).mean() * 100, 1)
        else:
            remote_pct = 50.0
            
        # Top skills
        if 'required_skills' in sub_df.columns:
            skills = sub_df['required_skills'].dropna().str.split(', ').explode()
            top_skills = skills.value_counts().head(6).index.tolist()
        else:
            top_skills = []
            
        # Top industries
        if 'industry' in sub_df.columns:
            inds = sub_df['industry'].dropna().value_counts().head(3).to_dict()
        else:
            inds = {}
            
        return {
            "name": label,
            "total_jobs": f"{len(sub_df):,}",
            "median_salary": f"${median_sal:,}",
            "median_raw": median_sal,
            "avg_salary": f"${avg_sal:,}",
            "avg_raw": avg_sal,
            "min_salary": f"${min_sal:,}",
            "max_salary": f"${max_sal:,}",
            "q25_salary": f"${q25_sal:,}",
            "q75_salary": f"${q75_sal:,}",
            "salary_spread": f"${q25_sal:,} - ${q75_sal:,}",
            "remote_pct": f"{remote_pct}%",
            "top_skills": top_skills,
            "top_industries": inds
        }
