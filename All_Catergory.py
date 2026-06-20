from urllib.parse import urljoin
import pandas as pd
import requests
from bs4 import BeautifulSoup

home_url= ('https://books.toscrape.com/index.html')
page = requests.get(home_url)
soup = BeautifulSoup(page.content, 'html.parser')

category_links = []
page_content = soup.find(id="default")
category_list = soup.find(class_='nav nav-list')
categories = category_list.find_all('a')

for category_url in categories:
    catergory_name= category_url.text.strip()
    link = category_url['href']
    complete_link = urljoin(home_url, link)
    category_links.append({
        "name": catergory_name,
        "url": complete_link
    })
print(category_links)

