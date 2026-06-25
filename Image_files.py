from urllib.parse import urljoin
import pandas as pd
import requests
import os
from bs4 import BeautifulSoup
from scrapetest import scrape_one_book

home_url = 'https://books.toscrape.com/index.html'
page = requests.get(home_url)
soup = BeautifulSoup(page.content, 'html.parser')

category_links = []
page_content = soup.find(id="default")
category_list = soup.find(class_='nav nav-list')
categories = category_list.find_all('a')

for category_url in categories:
    catergory_name = category_url.text.strip()
    link = category_url['href']
    complete_link = urljoin(home_url, link)
    category_links.append({
        "name": catergory_name,
        "url": complete_link
    })
print(category_links)

for category in category_links:
     cat_name = category["name"]
     cat_url  = category["url"]
     print(f"Scraping category: {cat_name}")

     all_book_urls = []
     page = requests.get(cat_url)
     soup = BeautifulSoup(page.text, 'html.parser')
     books_on_page = soup.find_all(class_='col-xs-6 col-sm-4 col-md-3 col-lg-3')
     all_book_urls = []

     for book_element in books_on_page:
         link = book_element.find('h3').find('a')['href']
         full_url = urljoin(cat_url, link)
         all_book_urls.append(full_url)
         
     while True:
        next_button = soup.find(class_="next")
        if not next_button:
            break
        next_page = next_button.find("a")["href"]
        cat_url = urljoin(cat_url, next_page)
        page = requests.get(cat_url)
        soup = BeautifulSoup(page.text, "html.parser")
        books_on_page = soup.find_all(class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")
        for book_element in books_on_page:
            link = book_element.find("h3").find("a")["href"]
            full_url = urljoin(cat_url, link)
            all_book_urls.append(full_url)
     all_books = []
     for url in all_book_urls:
        book_data = scrape_one_book(url)
        all_books.append(book_data)
     safe_name = cat_name.lower().replace(" ", "_")
     df = pd.DataFrame(all_books)
     df.to_csv(f"{safe_name}.csv", index=False)
     print(f"Saved {len(all_books)} books to {safe_name}.csv")

