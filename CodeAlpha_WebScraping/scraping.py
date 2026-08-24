import requests
from bs4 import BeautifulSoup
import pandas as pd

# Base URL for all pages
base_url = "https://books.toscrape.com/catalogue/page-{}.html"

# List to store all book data
books_data = []

# Loop through all 50 pages
for page in range(1, 51):
    print(f"Scraping Page {page}...")

    url = base_url.format(page)

    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Find all book containers
        books = soup.find_all("article", class_="product_pod")

        # Extract details for each book
        for book in books:
            title = book.h3.a["title"]
            price = book.find("p", class_="price_color").text.strip()
            availability = book.find("p", class_="instock availability").text.strip()
            rating = book.find("p", class_="star-rating")["class"][1]
            link = "https://books.toscrape.com/catalogue/" + book.h3.a["href"]

            books_data.append({
                "Title": title,
                "Price": price,
                "Availability": availability,
                "Rating": rating,
                "Product Link": link
            })

    except requests.exceptions.RequestException as e:
        print(f"Error on page {page}: {e}")

# Convert list to DataFrame
df = pd.DataFrame(books_data)

# Save to CSV
df.to_csv("books.csv", index=False, encoding="utf-8")

print("\n===================================")
print("✅ SCRAPING COMPLETED SUCCESSFULLY")
print("===================================")
print(f"Total Books Scraped : {len(df)}")
print("CSV File Saved      : books.csv")

print("\nFirst 5 Books:\n")
print(df.head())