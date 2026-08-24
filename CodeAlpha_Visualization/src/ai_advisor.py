import pandas as pd
import numpy as np

class AIAdvisor:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        
    def respond_to_query(self, query: str):
        q = (query or "").lower().strip()
        
        if not q:
            return "Hello! I am Aria, your AI Job Market Copilot. Ask me anything about compensation trends, in-demand skills, negotiation strategies, or career transitions."
            
        # Top skills
        if any(k in q for k in ["skill", "learn", "stack", "technology", "tool"]):
            return (
                "💡 **Top In-Demand AI Skills in 2026:**\n\n"
                "1. **Core ML / DL**: PyTorch, Deep Learning, Transformer Architectures.\n"
                "2. **MLOps & Infrastructure**: Docker, Kubernetes, AWS/GCP, MLflow, CI/CD.\n"
                "3. **Data Engineering & Scale**: SQL, Spark, Python, Vector DBs.\n"
                "4. **Productization**: LangChain, LLM Fine-Tuning, API Development.\n\n"
                "👉 *Pro-Tip:* Candidates possessing both PyTorch and Kubernetes/MLOps command an estimated +18% to +25% salary premium over pure model developers."
            )
            
        # Highest paying roles
        if any(k in q for k in ["highest", "top pay", "best salary", "most money", "rich"]):
            top_roles = self.df.groupby('job_title')['salary_usd'].median().sort_values(ascending=False).head(4)
            roles_text = "\n".join([f"- **{r}**: ~${int(s):,} Median Base" for r, s in top_roles.items()])
            return (
                f"🚀 **Top Highest-Paying AI Roles:**\n\n{roles_text}\n\n"
                "Specialized technical leadership (such as AI Architect & Head of AI) combines strategic system design with production machine learning pipelines."
            )
            
        # Negotiation
        if any(k in q for k in ["negotiat", "offer", "counter", "raise", "bargain"]):
            return (
                "🎯 **AI Salary Negotiation Playbook:**\n\n"
                "1. **Anchor with Market Percentiles**: Never state a single number first. Use the 75th percentile market benchmark from our Predictor as your target range.\n"
                "2. **Highlight Business Impact**: Frame your ML experience around business metrics (e.g., latency reduction, cost per token savings, revenue lift).\n"
                "3. **Negotiate Total Compensation**: If base salary is capped, negotiate sign-on bonuses, equity/RSUs, remote flexibility, and learning stipends.\n"
                "4. **Leverage Competing Offers**: Mention ongoing interviews professionally to create positive urgency."
            )
            
        # Remote work
        if any(k in q for k in ["remote", "wfh", "hybrid", "work from home", "relocat"]):
            return (
                "🌍 **Remote AI Compensation Insights:**\n\n"
                "- Fully Remote (100%) roles comprise over 38% of global AI postings.\n"
                "- US and Swiss companies offering remote global contracts pay significantly above local regional medians (Geographic Arbitrage).\n"
                "- Ensure your GitHub portfolio highlights asynchronous communication, Dockerized reproducibility, and automated cloud deployments."
            )
            
        # Experience / Seniority
        if any(k in q for k in ["junior", "entry", "senior", "experience", "lead", "promotion"]):
            return (
                "📈 **Career Ladder & Seniority Multipliers:**\n\n"
                "- **Entry-Level (EN)**: Focus on clean code, SQL proficiency, baseline PyTorch models, and end-to-end GitHub projects.\n"
                "- **Mid-Level (MI)**: Focus on model monitoring, Docker containers, data pipelines, and production deployments.\n"
                "- **Senior/Executive (SE/EX)**: Focus on distributed training, ML architecture trade-offs, team mentorship, and ROI-driven product delivery."
            )
            
        # General default guidance
        return (
            "🤖 **AI Career Market Insight:**\n\n"
            "The AI and Data Science sector remains one of the highest-velocity hiring markets globally. "
            "To maximize your compensation:\n"
            "1. Use our **AI Salary Predictor** to benchmark your expected market rate.\n"
            "2. Run the **Skills Gap Analyzer** to discover missing high-value technologies.\n"
            "3. Explore the **Live Job Board** for active openings matching your criteria."
        )
