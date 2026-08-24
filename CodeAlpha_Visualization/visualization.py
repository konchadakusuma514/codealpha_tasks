import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Create charts folder if it doesn't exist
os.makedirs("static/charts", exist_ok=True)

# Load dataset
df = pd.read_csv("data/ai_job_dataset.csv")

print("=" * 60)
print("DATASET SHAPE")
print(df.shape)

print("\n" + "=" * 60)
print("COLUMN NAMES")
for col in df.columns:
    print(col)

print("\n" + "=" * 60)
print("DATA TYPES")
print(df.dtypes)

print("\n" + "=" * 60)
print("MISSING VALUES")
print(df.isnull().sum())

print("\n" + "=" * 60)
print("FIRST 5 ROWS")
print(df.head())

# -----------------------------
# Generate Charts for Dashboard
# -----------------------------
print("\n" + "=" * 60)
print("Generating visualizations...")

sns.set_theme(style="whitegrid")

# 1. Top Hiring Countries
plt.figure(figsize=(8, 5))
top_countries = df['company_location'].value_counts().head(10)
sns.barplot(x=top_countries.values, y=top_countries.index, palette='viridis')
plt.title('Top 10 Hiring Countries', fontsize=14)
plt.xlabel('Number of Jobs')
plt.ylabel('Country')
plt.tight_layout()
plt.savefig('static/charts/country.png', dpi=300)
plt.close()

# 2. Salary Distribution
plt.figure(figsize=(8, 5))
sns.histplot(df['salary_usd'], bins=30, kde=True, color='#0d6efd')
plt.title('Salary Distribution (USD)', fontsize=14)
plt.xlabel('Salary (USD)')
plt.ylabel('Frequency')
plt.tight_layout()
plt.savefig('static/charts/salary.png', dpi=300)
plt.close()

# 3. Top Skills
plt.figure(figsize=(8, 5))
all_skills = df['required_skills'].str.split(', ').explode()
top_skills = all_skills.value_counts().head(10)
sns.barplot(x=top_skills.values, y=top_skills.index, palette='magma')
plt.title('Top 10 In-Demand AI Skills', fontsize=14)
plt.xlabel('Frequency')
plt.ylabel('Skill')
plt.tight_layout()
plt.savefig('static/charts/skills.png', dpi=300)
plt.close()

print("Charts successfully saved in static/charts/!")