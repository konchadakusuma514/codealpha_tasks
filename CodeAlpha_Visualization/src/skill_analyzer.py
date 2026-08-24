import pandas as pd
import numpy as np
import re

class SkillAnalyzer:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.role_skills_map = {}
        self.skill_salary_premiums = {}
        self._analyze_skills()
        
    def _analyze_skills(self):
        if self.df.empty or 'required_skills' not in self.df.columns:
            return
            
        # Extract skills per role
        for role, group in self.df.groupby('job_title'):
            skills_series = group['required_skills'].dropna().str.split(', ').explode()
            top_skills = skills_series.value_counts().head(12)
            self.role_skills_map[role] = {
                "core_skills": top_skills.index.tolist()[:6],
                "bonus_skills": top_skills.index.tolist()[6:12],
                "all_frequent": top_skills.to_dict()
            }
            
        # Calculate skill salary premiums across the dataset
        all_skills_expanded = self.df.assign(
            skill=self.df['required_skills'].dropna().str.split(', ')
        ).explode('skill')
        
        overall_median = self.df['salary_usd'].median()
        
        skill_medians = all_skills_expanded.groupby('skill')['salary_usd'].agg(['median', 'count'])
        # Filter skills with at least 15 occurrences
        skill_medians = skill_medians[skill_medians['count'] >= 15]
        
        for skill_name, row in skill_medians.iterrows():
            premium = max(0, row['median'] - overall_median)
            self.skill_salary_premiums[skill_name] = {
                "median_salary": int(row['median']),
                "premium": int(premium),
                "count": int(row['count'])
            }
            
    def get_all_available_skills(self):
        if not self.skill_salary_premiums:
            return ["Python", "PyTorch", "TensorFlow", "SQL", "Docker", "Kubernetes", "AWS", "MLOps", "NLP", "Computer Vision", "Git", "Tableau", "Spark", "Deep Learning", "GCP", "Azure"]
        return sorted(list(self.skill_salary_premiums.keys()))

    def parse_user_skills(self, raw_input):
        """Parse raw text, comma-separated list, or resume snippet into identified skills"""
        if not raw_input:
            return []
            
        available = self.get_all_available_skills()
        found = set()
        
        # Exact or case-insensitive word boundary search
        for skill in available:
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, raw_input, re.IGNORECASE):
                found.add(skill)
                
        # Also check comma split
        parts = [p.strip() for p in raw_input.split(',') if p.strip()]
        for p in parts:
            for skill in available:
                if p.lower() == skill.lower():
                    found.add(skill)
                    
        return sorted(list(found))

    def evaluate_skills_gap(self, user_skills, target_role):
        """Calculate match percentage, missing skills, salary boost, and personalized roadmap"""
        role_data = self.role_skills_map.get(target_role)
        if not role_data:
            # Fallback
            all_target = ["Python", "PyTorch", "SQL", "MLOps", "Docker", "AWS", "Deep Learning"]
            core = all_target[:4]
            bonus = all_target[4:]
        else:
            core = role_data["core_skills"]
            bonus = role_data["bonus_skills"]
            all_target = core + bonus
            
        user_skills_set = set([s.lower() for s in user_skills])
        
        matched_core = [s for s in core if s.lower() in user_skills_set]
        matched_bonus = [s for s in bonus if s.lower() in user_skills_set]
        missing_core = [s for s in core if s.lower() not in user_skills_set]
        missing_bonus = [s for s in bonus if s.lower() not in user_skills_set]
        
        total_weight = len(core) * 1.5 + len(bonus) * 1.0
        score_achieved = len(matched_core) * 1.5 + len(matched_bonus) * 1.0
        match_pct = round((score_achieved / total_weight) * 100, 1) if total_weight > 0 else 0
        match_pct = min(100, max(10, match_pct))
        
        # Calculate potential salary boost from missing high-value skills
        est_boost = 0
        for s in missing_core:
            est_boost += self.skill_salary_premiums.get(s, {}).get("premium", 5000) * 0.4
        for s in missing_bonus:
            est_boost += self.skill_salary_premiums.get(s, {}).get("premium", 3000) * 0.2
            
        est_boost = int(round(est_boost, -2))
        
        # Generate 30-60-90 Day Upskilling Roadmap
        roadmap = self._generate_roadmap(missing_core, missing_bonus, target_role)
        
        return {
            "target_role": target_role,
            "match_percentage": match_pct,
            "matched_skills": [s for s in user_skills if s.lower() in [x.lower() for x in all_target]],
            "missing_core_skills": missing_core,
            "missing_bonus_skills": missing_bonus,
            "estimated_salary_boost": f"+${est_boost:,}" if est_boost > 0 else "+$0",
            "roadmap": roadmap
        }

    def _generate_roadmap(self, missing_core, missing_bonus, target_role):
        p1_skills = missing_core[:2] if missing_core else ["Advanced Architecture", "System Design"]
        p2_skills = missing_core[2:] + missing_bonus[:1] if len(missing_core) > 2 or missing_bonus else ["Production CI/CD Pipelines"]
        p3_skills = missing_bonus[1:3] if len(missing_bonus) > 1 else ["Distributed Training & Benchmarking"]
        
        return [
            {
                "phase": "Phase 1: Days 1 - 30 (Foundation & High Priority)",
                "focus": f"Master critical core requirements: {', '.join(p1_skills)}",
                "milestones": [
                    f"Build 2 end-to-end benchmark projects incorporating {', '.join(p1_skills)}.",
                    "Review official documentation and complete hands-on practical lab modules.",
                    "Implement unit testing and automated evaluation metrics for ML pipelines."
                ]
            },
            {
                "phase": "Phase 2: Days 31 - 60 (Deployment & Tooling)",
                "focus": f"Bridge workflow gaps: {', '.join(p2_skills)}",
                "milestones": [
                    f"Integrate {', '.join(p2_skills)} into scalable Dockerized microservices.",
                    "Set up cloud infrastructure (AWS/GCP/Azure) with automated experiment tracking.",
                    "Publish GitHub repository with clean documentation and reproducible README."
                ]
            },
            {
                "phase": "Phase 3: Days 61 - 90 (Portfolio & Interview Mastery)",
                "focus": f"Specialize with advanced bonus skills: {', '.join(p3_skills)}",
                "milestones": [
                    f"Deploy live demo showcasing {', '.join(p3_skills)} with cloud monitoring.",
                    f"Tailor resume with quantified achievements targeting {target_role} vacancies.",
                    "Conduct mock behavioral and system architecture technical interviews."
                ]
            }
        ]
