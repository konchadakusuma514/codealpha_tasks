import pandas as pd

# Load the dataset
df = pd.read_csv("data/books.csv")

while True:
    print("\n" + "=" * 50)
    print("BOOK SEARCH SYSTEM")
    print("=" * 50)

    book_name = input("Enter book title to search (or type 'exit' to quit): ")

    if book_name.lower() == "exit":
        print("Thank you for using Book Search!")
        break

    result = df[df["Title"].str.contains(book_name, case=False, na=False)]

    if result.empty:
        print("\n❌ No books found!")
    else:
        print(f"\n✅ Found {len(result)} book(s):\n")
        print(result[["Title", "Price", "Rating", "Availability"]].to_string(index=False))