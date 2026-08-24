from flask import Flask, render_template, request, send_file, redirect, url_for
import pandas as pd
import math
import os
import random

app = Flask(__name__)

# -----------------------------
# Configuration
# -----------------------------
BOOKS_PER_PAGE = 20
CSV_PATH = "data/books.csv"

# Ensure data directory exists for exports
os.makedirs("data", exist_ok=True)

# -----------------------------
# Load Dataset
# -----------------------------
df = pd.read_csv(CSV_PATH)

# Clean Price Column
df["Price"] = (
    df["Price"]
    .astype(str)
    .str.extract(r'(\d+\.\d+)')[0]
    .astype(float)
)

# -----------------------------
# Convert Rating to Number
# -----------------------------
rating_map = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}
df["Rating Number"] = df["Rating"].map(rating_map)

# -----------------------------
# Home Page
# -----------------------------
@app.route("/")
def home():
    books = df.copy()

    # Search
    search = request.args.get("search","")
    if search:
        books = books[books["Title"].str.contains(search, case=False, na=False)]

    # Rating Filter
    rating = request.args.get("rating","")
    if rating and rating!="All":
        books = books[books["Rating"]==rating]

    # Price Filter
    min_price = request.args.get("min_price","")
    max_price = request.args.get("max_price","")

    if min_price:
        books = books[books["Price"]>=float(min_price)]
    if max_price:
        books = books[books["Price"]<=float(max_price)]

    # Sort
    sort = request.args.get("sort","")
    if sort=="low":
        books=books.sort_values("Price")
    elif sort=="high":
        books=books.sort_values("Price", ascending=False)
    elif sort=="title":
        books=books.sort_values("Title")
    elif sort=="rating":
        books=books.sort_values("Rating Number", ascending=False)

    # Statistics
    total_books = len(books)
    average_price = round(books["Price"].mean(),2) if len(books)>0 else 0
    highest_price = round(books["Price"].max(),2) if len(books)>0 else 0
    lowest_price = round(books["Price"].min(),2) if len(books)>0 else 0
    five_star = len(books[books["Rating"]=="Five"])
    four_star = len(books[books["Rating"]=="Four"])
    in_stock = len(books[books["Availability"].str.contains("In stock", case=False)])
    average_rating = round(books["Rating Number"].mean(),2) if len(books)>0 else 0

    # Pagination
    page = request.args.get("page", default=1, type=int)
    total_pages = max(1, math.ceil(total_books/BOOKS_PER_PAGE))
    start = (page-1)*BOOKS_PER_PAGE
    end = start+BOOKS_PER_PAGE
    
    books_page = books.iloc[start:end].copy()
    books_page["ID"] = books_page.index

    return render_template(
        "index.html",
        books=books_page.to_dict(orient="records"),
        total_books=total_books,
        average_price=average_price,
        highest_price=highest_price,
        lowest_price=lowest_price,
        five_star=five_star,
        four_star=four_star,
        in_stock=in_stock,
        average_rating=average_rating,
        page=page,
        total_pages=total_pages,
        search=search,
        rating=rating,
        sort=sort,
        min_price=min_price,
        max_price=max_price
    )

# ----------------------------------
# Download CSV
# ----------------------------------
@app.route("/download")
def download():
    return send_file(CSV_PATH, as_attachment=True, download_name="books_dataset.csv")

# ----------------------------------
# Download Excel
# ----------------------------------
@app.route("/download_excel")
def download_excel():
    excel_path = "data/books.xlsx"
    df.to_excel(excel_path, index=False)
    return send_file(excel_path, as_attachment=True)

# ----------------------------------
# Download JSON
# ----------------------------------
@app.route("/download_json")
def download_json():
    json_path = "data/books.json"
    df.to_json(json_path, orient="records", indent=4)
    return send_file(json_path, as_attachment=True)

# ----------------------------------
# Random Book Feature
# ----------------------------------
@app.route("/random")
def random_book():
    random_idx = random.choice(df.index.tolist())
    return redirect(url_for('details', index=random_idx))

# ----------------------------------
# Book Details
# ----------------------------------
@app.route("/book/<int:index>")
def details(index):
    if index not in df.index:
        return redirect(url_for("home"))
    book = df.loc[index]
    return render_template("details.html", book=book, id=index)

# ----------------------------------
# About Page
# ----------------------------------
@app.route("/about")
def about():
    return render_template("about.html")

# ----------------------------------
# Charts Page (UPDATED WITH MORE INSIGHTS)
# ----------------------------------
@app.route("/charts")
def charts():
    rating_counts = df["Rating"].value_counts().to_dict()
    average_price = round(df["Price"].mean(),2)
    highest_price = round(df["Price"].max(),2)
    lowest_price = round(df["Price"].min(),2)
    avg_price_by_rating = df.groupby("Rating")["Price"].mean().round(2).to_dict()
    availability_counts = df["Availability"].apply(
        lambda x: "In Stock" if "in stock" in str(x).lower() else "Out of Stock"
    ).value_counts().to_dict()
    
    # Base Data for all charts
    all_prices = df["Price"].tolist()
    all_titles = df["Title"].tolist()
    all_ratings = df["Rating Number"].tolist()
    
    # NEW DATA: Title Lengths (for 3D Chart)
    title_lengths = df["Title"].str.len().tolist()

    # NEW DATA: Dynamic Insights
    most_common_rating = str(df["Rating"].mode()[0])
    cheapest_book = df.loc[df["Price"].idxmin()]["Title"]
    expensive_book = df.loc[df["Price"].idxmax()]["Title"]
    
    # Top 10 Most Expensive Books
    top_10 = df.nlargest(10, 'Price')
    top_titles = top_10['Title'].tolist()
    top_prices = top_10['Price'].tolist()

    return render_template(
        "charts.html",
        rating_counts=rating_counts,
        average_price=average_price,
        highest_price=highest_price,
        lowest_price=lowest_price,
        avg_price_by_rating=avg_price_by_rating,
        availability_counts=availability_counts,
        all_prices=all_prices,
        all_titles=all_titles,
        all_ratings=all_ratings,
        title_lengths=title_lengths,
        most_common_rating=most_common_rating,
        cheapest_book=cheapest_book,
        expensive_book=expensive_book,
        top_titles=top_titles,
        top_prices=top_prices
    )

# ----------------------------------
# Error Page
# ----------------------------------
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# ----------------------------------
# Run
# ----------------------------------
if __name__=="__main__":
    app.run(debug=True)