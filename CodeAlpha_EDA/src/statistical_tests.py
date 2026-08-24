import pandas as pd
import numpy as np
from scipy import stats

def perform_defense_anova(df):
    groups = [group['Incident Resolution Time (in Hours)'].values for _, group in df.groupby('Defense Mechanism Used')]
    f_stat, p_val = stats.f_oneway(*groups)
    
    groups_loss = [group['Financial Loss (in Million $)'].values for _, group in df.groupby('Defense Mechanism Used')]
    f_stat_loss, p_val_loss = stats.f_oneway(*groups_loss)
    
    return {
        'resolution_f_stat': float(f_stat),
        'resolution_p_val': float(p_val),
        'resolution_significant': bool(p_val < 0.05),
        'loss_f_stat': float(f_stat_loss),
        'loss_p_val': float(p_val_loss),
        'loss_significant': bool(p_val_loss < 0.05)
    }

def perform_source_vuln_chi2(df):
    contingency_table = pd.crosstab(df['Attack Source'], df['Security Vulnerability Type'])
    chi2, p, dof, expected = stats.chi2_contingency(contingency_table)
    return {
        'chi2_stat': float(chi2),
        'p_val': float(p),
        'dof': int(dof),
        'significant': bool(p < 0.05),
        'contingency_table': contingency_table
    }

def calculate_correlations(df):
    num_cols = ['Financial Loss (in Million $)', 'Number of Affected Users', 
                'Incident Resolution Time (in Hours)', 'Cost_Per_User_$', 'Loss_Velocity_M_per_Hour', 'Risk_Severity_Index']
    clean_num = df[num_cols].dropna()
    return clean_num.corr()
