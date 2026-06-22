from urllib.parse import urljoin
import pandas as pd
import requests
from bs4 import BeautifulSoup

# 🎯 MILESTONE 3 — Next step: Turn this single-book script into a REUSABLE
#   FUNCTION that you can call for any book URL. Think of it like a template:
#
#       def scrape_one_book(url):  ******* i made these changes*******
#           page = requests.get(url)
#           ... extract all 10 fields ...
#           return { ... dictionary of results ... }
#
#   Then your Phase2 file can call this function for EVERY book it finds.
#   That's how you scale from 1 book → 1000 books without rewriting anything!

# i removed the base url and the category url, should i have kept those or not since im making a resusable ink
def scrape_one_book(url):
    page = requests.get(url)
    soup = BeautifulSoup (page.content, 'html.parser')

    product = soup.find(id="default")
    items = product.find_all(class_= 'col-sm-6 product_main')

    # 💡 STYLE NOTE: You're using a mix of naming styles.
    #   Python convention (PEP 8) says use snake_case for variables:
    
    # ***** okay i fixed the naming convention to snake_case. i will be consistent with it from now on.*****
    book_title=(items[0].find('h1').get_text())

    quantity_available=(items[0].find(class_= 'instock availability').text.strip())

    book_rating=items[0].find(class_='star-rating')['class'][1]
    rates={"One": "1", "Two": "2", "Three": "3", "Four": "4", "Five": "5"}
    review_rating= rates[book_rating]

    items[0] = product.find(class_= 'carousel')
    image=(items[0].find('img') ['src'])
    image_url= urljoin(url, image)

    items[0] = product.find(class_= 'breadcrumb')
    category=items[0].find_all('a')[2].text.strip()

    items[0] = product.find(class_= 'sub-header')
    product_description=(items[0].find_next('p').text.strip())

    info_table = product.find('table', class_='table-striped')
    table_data = {}
    for row in info_table.find_all('tr'):
        header = row.find('th').text.strip()
        value = row.find('td').text.strip()
        # Harold: (Milestone 2 typo fix) The original line had 'table_dataable_Data' — a typo mixing
        # my variable name 'table_data' with 'Data' from the table header. Python saw this as a BRAND NEW
        # variable instead of writing into my dictionary. Fix: use the actual variable name 'table_data'
        table_data[header] = value

    universal_product_code = table_data.get ('UPC')
    price_including_tax = table_data.get ('Price (incl. tax)')
    # Harold: (Milestone 2 typo fix) 'table_dataata' was another typo — a double 'ata' tacked on.
    # Same root cause as above: the real dictionary is called 'table_data' (defined on line 48).
    price_excluding_tax = table_data.get ('Price (excl. tax)')

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
    # Harold: (Milestone 2 fix + connects to Milestones 3 & 4) The old line had '*****' as pseudo-comment
    # markers (not valid Python syntax) and hardcoded ONE book's URL. That defeats the purpose of making
    # this a reusable function! Now that this function takes 'url' as a parameter, I should use THAT url.
    # When Phase2 (Milestone 3) or All_Catergory.py (Milestone 4) calls scrape_one_book(some_url),
    # 'some_url' is what gets passed in as 'url' here — and that's the product_page_url for that book.
    product_page_url = url

    return {
            # Harold: product_page_url now uses the 'url' parameter (Milestone 2 fix)
            'product_page_url': [product_page_url],
            # Harold: The remaining fields come from my extraction logic above (Milestone 2 original)
            'universal_product_code': [universal_product_code],
            'book_title': [book_title],
            'price_including_tax': [price_including_tax],
            'price_excluding_tax': [price_excluding_tax],
            'quantity_available': [quantity_available],
            'product_description': [product_description],
            'category': [category],
            'review_rating': [review_rating],
            'image_url': [image_url],
    }

# ********I belive i added all the changes to make this a reusable function********
# 🎯 MILESTONE 3 NOTE: When you scale to 1000 books, you DON'T want to create
#   a new DataFrame for each book. Instead, collect ALL book dictionaries into
#   one big list, then build ONE DataFrame at the very end:
#