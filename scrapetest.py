import pandas as pd
import requests
from bs4 import BeautifulSoup

page = requests.get('https://books.toscrape.com/catalogue/set-me-free_988/index.html')
soup = BeautifulSoup (page.content, 'html.parser')
# print(soup)

product = soup.find(id="default")
# print(product)

items = product.find_all(class_= 'col-sm-6 product_main')
# print(items)

Book_Title=(items[0].find('h1').get_text())
# print(Book_Title)

quantity_available=(items[0].find(class_= 'instock availability').get_text())
# print(quantity_available)

Book_rating=items[0].find(class_='star-rating')['class'][1]
rates={"One": "1", "Two": "2", "Three": "3", "Four": "4", "Five": "5"}
review_rating= rates[book_rating]
# print(review_rating)

items_1[0] = product.find(class_= 'carousel')
Image_URL=(items_1[0].find('img') ['src'])
print(Image_URL)

items_2[0] = product.find_all(class_= 'table table-striped')

universal_ product_code (upc) = items_2[0].find_
price_including_tax = items_2[0].find_
price_excluding_tax

product_page_url = ('https://books.toscrape.com/catalogue/set-me-free_988/index.html')
# print(product_page_url)

Book_Report = pd.DataFrame(
    {
    "product_page_url",
    "universal_product_code",
    "book_title",
    "price_including_tax",
    "price_excluding_tax",
    "quantity_available",
    "product_description",
    "category",
    "review_rating",
    "image_url"
    })
    print(Book_Report)