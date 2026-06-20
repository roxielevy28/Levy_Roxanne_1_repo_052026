from urllib.parse import urljoin
import pandas as pd
import requests
from bs4 import BeautifulSoup

home_url= ('https://books.toscrape.com/index.html')
page = requests.get(home_url)
soup = BeautifulSoup(page.content, 'html.parser')

category_links= []
page_content= soup.find(id="default")
category_list = soup.find(class_= 'nav nav-list')
categories= category_list.find_all('a')
print(categories)
for category_url in categories:
    relative_link = category_url['href']
    complete_link = urljoin(home_url, relative_link)
    category_links.append(complete_link)
print(category_links)

