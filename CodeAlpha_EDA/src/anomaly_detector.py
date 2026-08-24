import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

def detect_threat_anomalies(df, contamination=0.03):
    features = ['Financial Loss (in Million $)', 'Number of Affected Users', 'Incident Resolution Time (in Hours)', 'Risk_Severity_Index']
    clean_df = df.dropna(subset=features).copy()
    
    iso = IsolationForest(contamination=contamination, random_state=42)
    clean_df['Anomaly_Label'] = iso.fit_predict(clean_df[features])
    clean_df['Is_Anomaly'] = clean_df['Anomaly_Label'] == -1
    
    return clean_df
