# Price Monitoring System
This project is a beta version of a price monitoring system for Books to Scrape.
The application extracts book product information from the Books to Scrape website, saves the extracted data into CSV files, and extract the associated book cover images that can be saved locally.

## Project Overview
The program can:

- Extract product data from a single book page.

- Extract product data from all books in one selected category.

- Extract product data from all books across all categories.

- Generate one CSV file per category.

- Extract book cover images that can be saved locally.

- Handle pagination automatically.

## Extracted Data
For each book, the scraper extracts the following fields:
- product_page_url
- universal_product_code
- book_title
- price_including_tax
- price_excluding_tax
- quantity_available
- product_description
- category
- review_rating
- image_url

## Project Structure
The repository contains the application code, setup files, and documentation.
Example structure:
```text
Levy_Roxanne_Price_Monitoring_System_052026/
    README.md
    requirements.txt
    .gitignore
    scrapetest.py
    Phase2_Young.Adult.category.py
    All_category.py
    Image_files.py