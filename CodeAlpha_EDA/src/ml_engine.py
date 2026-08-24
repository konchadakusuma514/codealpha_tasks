import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score

class ThreatMLEngine:
    def __init__(self):
        self.features = ['Country', 'Attack Type', 'Target Industry', 'Attack Source', 'Security Vulnerability Type', 'Defense Mechanism Used']
        self.pipeline_loss = None
        self.pipeline_time = None
        self.loss_r2 = 0.0
        self.time_r2 = 0.0
        
    def train(self, df):
        X = df[self.features]
        y_loss = df['Financial Loss (in Million $)']
        y_time = df['Incident Resolution Time (in Hours)']
        
        preprocessor = ColumnTransformer(
            transformers=[
                ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), self.features)
            ]
        )
        
        # Loss Model
        self.pipeline_loss = Pipeline([
            ('preprocessor', preprocessor),
            ('regressor', RandomForestRegressor(n_estimators=75, max_depth=12, random_state=42, n_jobs=-1))
        ])
        self.pipeline_loss.fit(X, y_loss)
        pred_loss = self.pipeline_loss.predict(X)
        self.loss_r2 = r2_score(y_loss, pred_loss)
        
        # Resolution Time Model
        self.pipeline_time = Pipeline([
            ('preprocessor', preprocessor),
            ('regressor', RandomForestRegressor(n_estimators=75, max_depth=12, random_state=42, n_jobs=-1))
        ])
        self.pipeline_time.fit(X, y_time)
        pred_time = self.pipeline_time.predict(X)
        self.time_r2 = r2_score(y_time, pred_time)
        
        return {
            'loss_r2': self.loss_r2,
            'time_r2': self.time_r2
        }
        
    def predict(self, sample_dict):
        df_sample = pd.DataFrame([sample_dict])
        est_loss = float(self.pipeline_loss.predict(df_sample)[0])
        est_time = float(self.pipeline_time.predict(df_sample)[0])
        
        # Confidence bounds (~ 15% interval)
        loss_lower = max(0.5, est_loss * 0.85)
        loss_upper = min(100.0, est_loss * 1.15)
        time_lower = max(1.0, est_time * 0.85)
        time_upper = min(72.0, est_time * 1.15)
        
        return {
            'est_loss': round(est_loss, 2),
            'loss_range': (round(loss_lower, 2), round(loss_upper, 2)),
            'est_time': round(est_time, 1),
            'time_range': (round(time_lower, 1), round(time_upper, 1))
        }

    def get_feature_importances(self):
        try:
            ohe = self.pipeline_loss.named_steps['preprocessor'].named_transformers_['cat']
            feature_names = ohe.get_feature_names_out(self.features)
            importances = self.pipeline_loss.named_steps['regressor'].feature_importances_
            
            imp_df = pd.DataFrame({'Feature': feature_names, 'Importance': importances})
            imp_df = imp_df.sort_values('Importance', ascending=False).head(10)
            return imp_df
        except Exception:
            return pd.DataFrame()
