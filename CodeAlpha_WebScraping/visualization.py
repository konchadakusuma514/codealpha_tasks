import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("data/books.csv")

# Clean Price column
df["Price"] = df["Price"].astype(str).str.extract(r'(\d+\.\d+)')[0].astype(float)

# -------------------------
# Rating Distribution
# -------------------------
rating_counts = df["Rating"].value_counts()

plt.figure(figsize=(8,5))
plt.bar(rating_counts.index, rating_counts.values)
plt.title("Book Ratings Distribution")
plt.xlabel("Rating")
plt.ylabel("Number of Books")
plt.tight_layout()

plt.savefig("screenshots/rating_distribution.png")
plt.close()

# -------------------------
# Price Distribution
# -------------------------
plt.figure(figsize=(8,5))
plt.hist(df["Price"], bins=10)
plt.title("Book Price Distribution")
plt.xlabel("Price (£)")
plt.ylabel("Number of Books")
plt.tight_layout()

plt.savefig("screenshots/price_distribution.png")
plt.close()

print("✅ Both graphs generated successfully!")
print("Saved in screenshots folder.")