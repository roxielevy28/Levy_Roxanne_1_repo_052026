from urllib.parse import urljoin
import pandas as pd
import requests
from bs4 import BeautifulSoup

# ✅ GREAT PROGRESS! You've addressed almost all of the previous comments:
#   - Fixed all syntax errors (missing ), ], etc.)
#   - Added pandas import
#   - Used .get_text() to extract text from elements
#   - Used the star-rating class trick to get the rating word
#   - Built a dictionary from the table rows — excellent approach!
#   - DataFrame now uses proper key: value syntax#

page = requests.get('https://books.toscrape.com/catalogue/set-me-free_988/index.html')
soup = BeautifulSoup (page.content, 'html.parser')

product = soup.find(id="default")

items = product.find_all(class_= 'col-sm-6 product_main')

# ✅ Nice — you extracted the title correctly using .get_text()
Book_Title=(items[0].find('h1').get_text())

# ✅ Availability text extracted. TIP: the text has extra whitespace/newlines.
#   Consider using .strip() to clean it up.
quantity_available=(items[0].find(class_= 'instock availability').text.strip())

# ✅ Clever approach! Reading the class attribute to get "Five", then mapping to "5"
Book_rating=items[0].find(class_='star-rating')['class'][1]
rates={"One": "1", "Two": "2", "Three": "3", "Four": "4", "Five": "5"}
review_rating= rates[Book_rating]

# ✅ Image URL extracted. TIP: the src is a relative path like "../../media/..."
#   You may want to convert it to an absolute URL. Think about joining it with
#   the base URL: "https://books.toscrape.com/catalogue/"
items[0] = product.find(class_= 'carousel')
Image=(items[0].find('img') ['src'])
Image_URL= urljoin("https://books.toscrape.com/catalogue/", Image)
# ⚠️ BUG: This only works for THIS specific book (hardcoded href).
#   What if you scrape a different book? The category href will be different.
#   TIP: The breadcrumb has the structure Home > Books > Category.
#   Instead of searching for a specific href, try getting the 3rd <a> tag
#   from the breadcrumb list (index [2]), or get the text of the last <a>
#   before the active <li>.
items[0] = product.find(class_= 'breadcrumb')
category=items[0].find_all('a')[2].text.strip()

# ✅ Product description extracted. Good use of find_next('p')!
#   (In the other file you used .find('p') which didn't work — this is correct.)
items[0] = product.find(class_= 'sub-header')
product_description=(items[0].find_next('p').text.strip())

# ✅ Excellent! Looping through table rows and building a dictionary is a
#   much cleaner approach than trying to find each cell individually.
info_table = product.find('table', class_='table-striped')
Table_Data = {}
for row in info_table.find_all('tr'):
    header = row.find('th').text.strip()
    value = row.find('td').text.strip()
    Table_Data[header] = value

universal_product_code = Table_Data.get ('UPC')
price_including_tax = Table_Data.get ('Price (incl. tax)')

# ⚠️ BUG: Both price variables are reading 'Price (incl. tax)'!
#   price_excluding_tax should read 'Price (excl. tax)' instead.
#   This is why both prices show the same value.
price_excluding_tax = Table_Data.get ('Price (excl. tax)')

product_page_url = ('https://books.toscrape.com/catalogue/set-me-free_988/index.html')

# ⚠️ BUG: DataFrame with scalar values needs an index parameter.
#   Try adding: index=[0]
#   Each value is a single scalar, so pandas doesn't know how many rows to make.
Book_Report = pd.DataFrame(
    {
        'product_page_url': [product_page_url],
        'universal_product_code': [universal_product_code],
        'Book_Title': [Book_Title],
        'price_including_tax': [price_including_tax],
        'price_excluding_tax': [price_excluding_tax],
        'quantity_available': [quantity_available],
        'product_description': [product_description],
        'category': [category],
        'review_rating': [review_rating],
        'image_url': [Image_URL],
    })

print(Book_Report)

# ⚠️ BUG: to_csv needs a filename string. Book_Report is a DataFrame variable,
#   not a string. Try: Book_Report.to_csv('Book_Report.csv')
Book_Report.to_csv('Book_Report.csv')
