import pandas as pd

# Read the CSV file
df = pd.read_csv("data/books.csv")

# Display basic information
print("=" * 60)
print("          BOOK DATA ANALYSIS")
print("=" * 60)

# Total number of books
print(f"\n📚 Total Books: {len(df)}")

# Clean the Price column
# Keep only numbers and decimal point
df["Price"] = df["Price"].astype(str).str.extract(r'(\d+\.\d+)')[0].astype(float)

# Average Price
print(f"\n💰 Average Price: £{df['Price'].mean():.2f}")

# Highest Price
print(f"\n💎 Highest Price: £{df['Price'].max():.2f}")

# Lowest Price
print(f"\n🪙 Lowest Price: £{df['Price'].min():.2f}")

# Rating Counts
print("\n⭐ Rating Counts:")
print(df["Rating"].value_counts())

# Availability Counts
print("\n📦 Availability Counts:")
print(df["Availability"].value_counts())

# Top 10 Most Expensive Books
print("\n🔝 Top 10 Most Expensive Books:")
top10 = df.sort_values(by="Price", ascending=False)[["Title", "Price"]].head(10)
print(top10)

# Save cleaned dataset
df.to_csv("data/cleaned_books.csv", index=False)

print("\n" + "=" * 60)
print("✅ Analysis Completed Successfully!")
print("📁 Cleaned dataset saved as: data/cleaned_books.csv")
print("=" * 60)