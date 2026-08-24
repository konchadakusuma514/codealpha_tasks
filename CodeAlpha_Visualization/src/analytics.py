import pandas as pd
import numpy as np
import json
import plotly
import plotly.express as px
import plotly.graph_objects as go

class AnalyticsEngine:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        
    def generate_dashboard_charts(self):
        """Generates all interactive Plotly charts for the main dashboard"""
        if self.df.empty:
            return {}, {}, {}, {}, {}, {}
            
        # 1. Global AI Hiring Hubs & Median Salary (Bar + Continuous Palette)
        top_countries = self.df.groupby('company_location').agg(
            job_count=('job_id', 'count') if 'job_id' in self.df.columns else ('salary_usd', 'count'),
            avg_salary=('salary_usd', 'mean')
        ).reset_index().sort_values(by='job_count', ascending=False).head(10)
        
        top_countries['avg_salary_int'] = top_countries['avg_salary'].astype(int)
        
        fig1 = px.bar(
            top_countries,
            x='company_location',
            y='job_count',
            color='avg_salary_int',
            color_continuous_scale='Turbo',
            labels={'company_location': 'Country', 'job_count': 'Job Openings', 'avg_salary_int': 'Avg Salary ($)'},
            template='plotly_white'
        )
        fig1.update_layout(
            margin=dict(l=30, r=20, t=30, b=40),
            coloraxis_colorbar=dict(title="Avg Pay ($)")
        )
        graph1 = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)

        # 2. Salary Distribution with Median Line
        fig2 = px.histogram(
            self.df,
            x="salary_usd",
            nbins=35,
            color_discrete_sequence=['#0d6efd'],
            marginal="box",
            labels={'salary_usd': 'Salary (USD)'},
            template='plotly_white'
        )
        median_val = self.df['salary_usd'].median()
        fig2.add_vline(x=median_val, line_width=2, line_dash="dash", line_color="#dc3545", annotation_text=f"Median: ${int(median_val):,}")
        fig2.update_layout(margin=dict(l=30, r=20, t=30, b=40))
        graph2 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)

        # 3. Top Skills Demand vs Frequency
        if 'required_skills' in self.df.columns:
            all_skills = self.df['required_skills'].dropna().str.split(', ').explode()
            top_skills = all_skills.value_counts().head(10).reset_index()
            top_skills.columns = ['Skill', 'Demand']
            fig3 = px.bar(
                top_skills,
                x='Demand',
                y='Skill',
                orientation='h',
                color='Demand',
                color_continuous_scale='Magma',
                template='plotly_white'
            )
            fig3.update_layout(
                yaxis={'categoryorder': 'total ascending'},
                margin=dict(l=30, r=20, t=30, b=40)
            )
        else:
            fig3 = go.Figure()
        graph3 = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)

        # 4. Salary by Experience Level Progression
        exp_order = ['EN', 'MI', 'SE', 'EX']
        exp_df = self.df[self.df['experience_level'].isin(exp_order)].copy()
        if not exp_df.empty:
            exp_stats = exp_df.groupby('experience_level')['salary_usd'].agg(['mean', 'median', 'min', 'max']).reindex(exp_order).reset_index()
            exp_map = {'EN': 'Entry (0-2y)', 'MI': 'Mid (2-5y)', 'SE': 'Senior (5-8y)', 'EX': 'Executive (8y+)'}
            exp_stats['exp_label'] = exp_stats['experience_level'].map(exp_map)
            
            fig4 = px.line(
                exp_stats,
                x='exp_label',
                y='median',
                markers=True,
                line_shape='spline',
                labels={'exp_label': 'Experience Tier', 'median': 'Median Salary ($)'},
                template='plotly_white'
            )
            fig4.update_traces(line_color='#20c997', marker=dict(size=10, color='#08142d'))
            fig4.update_layout(margin=dict(l=30, r=20, t=30, b=40))
        else:
            fig4 = go.Figure()
        graph4 = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)

        # 5. Top 6 Industries Distribution (Donut Chart)
        if 'industry' in self.df.columns:
            top_inds = self.df['industry'].value_counts().head(6).reset_index()
            top_inds.columns = ['Industry', 'Count']
            fig5 = px.pie(
                top_inds,
                values='Count',
                names='Industry',
                hole=0.45,
                color_discrete_sequence=px.colors.qualitative.Prism,
                template='plotly_white'
            )
            fig5.update_layout(margin=dict(l=20, r=20, t=20, b=20))
        else:
            fig5 = go.Figure()
        graph5 = json.dumps(fig5, cls=plotly.utils.PlotlyJSONEncoder)
        
        # 6. Remote Work Ratio vs Average Salary
        if 'remote_ratio' in self.df.columns:
            remote_df = self.df.copy()
            remote_df['remote_ratio'] = pd.to_numeric(remote_df['remote_ratio'], errors='coerce')
            remote_map = {0: 'On-Site (0%)', 50: 'Hybrid (50%)', 100: 'Fully Remote (100%)'}
            remote_df['work_model'] = remote_df['remote_ratio'].map(remote_map).fillna('Hybrid (50%)')
            remote_stats = remote_df.groupby('work_model')['salary_usd'].mean().reset_index()
            
            fig6 = px.bar(
                remote_stats,
                x='work_model',
                y='salary_usd',
                color='work_model',
                labels={'work_model': 'Work Model', 'salary_usd': 'Average Salary ($)'},
                color_discrete_sequence=['#6f42c1', '#00b4ff', '#28a745'],
                template='plotly_white'
            )
            fig6.update_layout(margin=dict(l=30, r=20, t=30, b=40), showlegend=False)
        else:
            fig6 = go.Figure()
        graph6 = json.dumps(fig6, cls=plotly.utils.PlotlyJSONEncoder)

        return graph1, graph2, graph3, graph4, graph5, graph6
