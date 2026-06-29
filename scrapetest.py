from urllib.parse import urljoin
import pandas as pd
import re
import requests
from bs4 import BeautifulSoup

# =============================================================================
# 🟡 ISSUE #3 — Product descriptions appear duplicated
# =============================================================================
# Harold: (2026-06-28, Milestone 2) In the CSV output, descriptions show the
# same paragraph twice. The current code does:
#
#        items[0] = product.find(class_='sub-header')
#        product_description = items[0].find_next('p').text.strip()
#
# The find_next('p') might be picking up a description that already contains
# both the truncated "..." version AND the full version concatenated.
#
# ✅ FIX: Investigate the HTML structure. Try using find_all('p') and taking
#    just the first <p> after the sub-header, or use a more specific CSS
#    selector to target only the description paragraph.
#
# 🎯 WHY: Duplicated text inflates file size and corrupts text analysis.


def scrape_one_book(url):
    page = requests.get(url)
    soup = BeautifulSoup (page.content, 'html.parser')

    product = soup.find(id="default")
    items = product.find_all(class_= 'col-sm-6 product_main')

    book_title=(items[0].find('h1').get_text())

    raw_quantity = items[0].find(class_='instock availability').text.strip()
    quantity_available = int(re.search(r'\d+', raw_quantity).group())

    book_rating=items[0].find(class_='star-rating')['class'][1]
    rates={"One": "1", "Two": "2", "Three": "3", "Four": "4", "Five": "5"}
    review_rating= rates[book_rating]

    carousel = product.find(class_= 'carousel')
    image=(carousel.find('img') ['src'])
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
        table_data[header] = value

    universal_product_code = table_data.get ('UPC')
    price_including_tax = table_data.get ('Price (incl. tax)')
    price_excluding_tax = table_data.get ('Price (excl. tax)')
   
    product_page_url = url

    return {
            'product_page_url': product_page_url,
            'universal_product_code': universal_product_code,
            'book_title': book_title,
            'price_including_tax': price_including_tax,
            'price_excluding_tax': price_excluding_tax,
            'quantity_available': quantity_available,
            'product_description': product_description,
            'category': category,
            'review_rating': review_rating,
            'image_url': image_url,
    }
