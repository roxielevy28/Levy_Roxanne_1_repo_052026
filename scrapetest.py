from urllib.parse import urljoin
import pandas as pd
import requests
from bs4 import BeautifulSoup

# 🎯 MILESTONE 3 — Next step: Turn this single-book script into a REUSABLE
#   FUNCTION that you can call for any book URL. Think of it like a template:
#
#       def scrape_one_book(url):
#           page = requests.get(url)
#           ... extract all 10 fields ...
#           return { ... dictionary of results ... }
#
#   Then your Phase2 file can call this function for EVERY book it finds.
#   That's how you scale from 1 book → 1000 books without rewriting anything!

BASE_URL = "https://books.toscrape.com/catalogue/" # i added this base url variable to make it easier to reuse in the future when i scrape all the books. i can just call this variable instead of writing the url every time.
page = requests.get('https://books.toscrape.com/catalogue/set-me-free_988/index.html')
soup = BeautifulSoup (page.content, 'html.parser')

product = soup.find(id="default")

items = product.find_all(class_= 'col-sm-6 product_main')

# 💡 STYLE NOTE: You're using a mix of naming styles.
#   Python convention (PEP 8) says use snake_case for variables:
#   - book_title instead of Book_Title
#   - review_rating ✅ (already snake_case!)
#   - image_url instead of Image_URL
#   Not wrong, just inconsistent — pick one style and stick with it.
#   It'll help a lot when you start building bigger scripts!

# okay i fixed the naming convention to snake_case. i will be consistent with it from now on.

book_title=(items[0].find('h1').get_text())

quantity_available=(items[0].find(class_= 'instock availability').text.strip())

Book_rating=items[0].find(class_='star-rating')['class'][1]
rates={"One": "1", "Two": "2", "Three": "3", "Four": "4", "Five": "5"}
review_rating= rates[Book_rating]

items[0] = product.find(class_= 'carousel')
Image=(items[0].find('img') ['src'])
image_url= urljoin(BASE_URL, Image)
# i took out the hardcoded url and replaced it with the BASE_URL variable that i created at the top. this way, when i scrape all the books, i can just call the BASE_URL variable instead of writing the url every time.
items[0] = product.find(class_= 'breadcrumb')
category=items[0].find_all('a')[2].text.strip()

items[0] = product.find(class_= 'sub-header')
product_description=(items[0].find_next('p').text.strip())

info_table = product.find('table', class_='table-striped')
Table_Data = {}
for row in info_table.find_all('tr'):
    header = row.find('th').text.strip()
    value = row.find('td').text.strip()
    Table_Data[header] = value

universal_product_code = Table_Data.get ('UPC')
price_including_tax = Table_Data.get ('Price (incl. tax)')

price_excluding_tax = Table_Data.get ('Price (excl. tax)')

# ❓ GREAT QUESTION: "Where does this URL come from when I scrape ALL books?"
#   Right now you hardcoded it because you were testing with one book.
#   When you move to the week milestone (scraping all 1,000 books), you'll get
#   this URL from the LISTING PAGES instead. Here's how:
#
#   1. You fetch a listing page like:
#        https://books.toscrape.com/catalogue/category/books_1/index.html
#   2. You find all <article class="product_pod"> elements on that page
#   3. Each one has a link: <h3><a href="../../a-light-in-the-attic_1000/index.html">
#   4. You convert that relative href to an absolute URL, e.g.:
#        "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
#   5. THAT becomes the product_page_url for that book — and you pass it into
#      your scraping function to get all the other fields.
#
#   So product_page_url won't be hardcoded anymore — it will be DYNAMIC,
#   coming from each book's link on the listing page.
#   TIP: Python's `urllib.parse.urljoin(base, relative)` can help convert
#   relative URLs to absolute ones.
product_page_url = ('https://books.toscrape.com/catalogue/set-me-free_988/index.html')

book_report = pd.DataFrame(
    {
        'product_page_url': [product_page_url],
        'universal_product_code': [universal_product_code],
        'book_title': [book_title],
        'price_including_tax': [price_including_tax],
        'price_excluding_tax': [price_excluding_tax],
        'quantity_available': [quantity_available],
        'product_description': [product_description],
        'category': [category],
        'review_rating': [review_rating],
        'image_url': [image_url],
    })

print(book_report)


book_report.to_csv('Book_Report.csv')

# 🎯 MILESTONE 3 NOTE: When you scale to 1000 books, you DON'T want to create
#   a new DataFrame for each book. Instead, collect ALL book dictionaries into
#   one big list, then build ONE DataFrame at the very end:
#
#       all_books = []
#       for url in all_book_urls:
#           book_data = scrape_one_book(url)
#           all_books.append(book_data)
#       master_report = pd.DataFrame(all_books)
#       master_report.to_csv('all_books.csv', index=False)
#
#   This is much faster and cleaner than creating 1000 separate CSVs!