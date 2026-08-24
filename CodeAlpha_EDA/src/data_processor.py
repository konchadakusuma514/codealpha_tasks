import pandas as pd
import numpy as np

def load_and_preprocess_data(filepath='dataset/Global_Cybersecurity_Threats_2015-2024.csv'):
    df = pd.read_csv(filepath)
    
    # Feature Engineering
    # 1. Cost per Compromised User ($ / User)
    df['Cost_Per_User_$'] = (df['Financial Loss (in Million $)'] * 1e6) / df['Number of Affected Users']
    df['Cost_Per_User_$'] = df['Cost_Per_User_$'].round(2)
    
    # 2. Incident Financial Velocity ($ Millions per Hour)
    df['Loss_Velocity_M_per_Hour'] = df['Financial Loss (in Million $)'] / df['Incident Resolution Time (in Hours)']
    df['Loss_Velocity_M_per_Hour'] = df['Loss_Velocity_M_per_Hour'].round(3)
    
    # 3. Composite Risk Severity Index (RSI: 0 to 100)
    # Weights: Loss 40%, Affected Users 35%, Resolution Time 25%
    loss_norm = (df['Financial Loss (in Million $)'] - df['Financial Loss (in Million $)'].min()) / (df['Financial Loss (in Million $)'].max() - df['Financial Loss (in Million $)'].min())
    users_norm = (df['Number of Affected Users'] - df['Number of Affected Users'].min()) / (df['Number of Affected Users'].max() - df['Number of Affected Users'].min())
    time_norm = (df['Incident Resolution Time (in Hours)'] - df['Incident Resolution Time (in Hours)'].min()) / (df['Incident Resolution Time (in Hours)'].max() - df['Incident Resolution Time (in Hours)'].min())
    
    df['Risk_Severity_Index'] = ((0.40 * loss_norm + 0.35 * users_norm + 0.25 * time_norm) * 100).round(2)
    
    # 4. Severity Tier
    def categorize_severity(score):
        if score >= 75:
            return 'CRITICAL (Tier 4)'
        elif score >= 50:
            return 'HIGH (Tier 3)'
        elif score >= 25:
            return 'MEDIUM (Tier 2)'
        else:
            return 'LOW (Tier 1)'
            
    df['Severity_Tier'] = df['Risk_Severity_Index'].apply(categorize_severity)
    
    return df
