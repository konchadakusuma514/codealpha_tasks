import pandas as pd
import numpy as np

def generate_defense_recommendations(df, target_industry, attack_type):
    subset = df[(df['Target Industry'] == target_industry) & (df['Attack Type'] == attack_type)]
    if subset.empty:
        subset = df[df['Attack Type'] == attack_type]
        
    summary = subset.groupby('Defense Mechanism Used').agg(
        Avg_Loss=('Financial Loss (in Million $)', 'mean'),
        Avg_Resolution_Time=('Incident Resolution Time (in Hours)', 'mean'),
        Incident_Count=('Financial Loss (in Million $)', 'count')
    ).reset_index()
    
    max_loss = summary['Avg_Loss'].max() if summary['Avg_Loss'].max() > 0 else 1
    max_time = summary['Avg_Resolution_Time'].max() if summary['Avg_Resolution_Time'].max() > 0 else 1
    
    summary['Efficacy_Score'] = (
        (1 - (summary['Avg_Loss'] / max_loss)) * 50 + 
        (1 - (summary['Avg_Resolution_Time'] / max_time)) * 50
    ).round(1)
    
    summary = summary.sort_values('Efficacy_Score', ascending=False)
    return summary
