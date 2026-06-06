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
review_rating= rates[Book_rating]
# print(review_rating)

items_1[0] = product.find(class_= 'carousel')

Image_URL=(items_1[0].find('img') ['src'])
print(Image_URL)

items_2[0] = product.find(class_= 'breadcrumb')
category=items_2[0].find(href='../category/books/young-adult_21/index.html') ['href'] [1]
print(category)

items_3[0] = product.find(class_= 'sub-header')
product_description=(items_3[0].find('p').get_text())
print(product_description)

info_table = soup.find('table', class_='table-striped')
Table_Data= {}
for row in info_table.find_all('tr'):
header = row.find('th').text.strip()
value = row.find('td').text.strip()
Table_Data[header] = value

universal_product_code (upc) = Table_Data.get ('UPC')
price_including_tax = Table_Data.get ('Price (incl. tax)')
price_excluding_tax =Table_Data.get ('Price (excl. tax)')
print(universal_product_code (upc))
print(price_including_tax)
print(price_excluding_tax)

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
Book_Report.to.to_csv(Book_Report.csv)