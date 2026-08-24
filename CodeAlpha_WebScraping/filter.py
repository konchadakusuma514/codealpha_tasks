import pandas as pd

df = pd.read_csv("data/books.csv")

print("\nAvailable Ratings:")
print("One")
print("Two")
print("Three")
print("Four")
print("Five")

rating = input("\nEnter Rating: ")

filtered = df[df["Rating"].str.lower() == rating.lower()]

if filtered.empty:
    print("\nNo books found.")
else:
    print(filtered[["Title", "Price", "Rating"]])

    filtered.to_csv("data/filtered_books.csv", index=False)

    print("\nFiltered books saved to data/filtered_books.csv")