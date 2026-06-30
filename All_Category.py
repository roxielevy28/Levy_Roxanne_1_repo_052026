import os
from urllib.parse import urljoin
import pandas as pd
import requests
from bs4 import BeautifulSoup
from scrapetest import scrape_one_book
os.makedirs('csv_reports', exist_ok=True)

home_url = 'https://books.toscrape.com/index.html'
page = requests.get(home_url)
soup = BeautifulSoup(page.content, 'html.parser')

category_links = []
category_list = soup.find(class_='nav nav-list')
categories = category_list.find_all('a')

for category_url in categories:
    category_name = category_url.text.strip()
    link = category_url['href']
    complete_link = urljoin(home_url, link)
    category_links.append({
        "name": category_name,
        "url": complete_link
    })
print(category_links)

for category in category_links[1:]:
    try:
        cat_name = category["name"]
        cat_url = category["url"]

        all_book_urls = []
        current_url = cat_url

        while True:
            page = requests.get(current_url)
            soup = BeautifulSoup(page.text, 'html.parser')
            books_on_page = soup.find_all(class_='col-xs-6 col-sm-4 col-md-3 col-lg-3')

            for book_element in books_on_page:
                link = book_element.find('h3').find('a')['href']
                full_url = urljoin(current_url, link)
                all_book_urls.append(full_url)

            next_button = soup.find(class_="next")
            if not next_button:     
                break        

            next_page = next_button.find("a")["href"]
            current_url = urljoin(current_url, next_page)

        all_books = []
        for url in all_book_urls:
            book_data = scrape_one_book(url)
            all_books.append(book_data)

        safe_name = cat_name.lower().replace(" ", "_")
        df = pd.DataFrame(all_books)
        df.to_csv(f"csv_reports/{safe_name}.csv", index=False)
        print(f"Saved {len(all_books)} books to {safe_name}.csv")
    except Exception as e:
        print(f"  ❌ Error on {cat_name}: {e}")
        continue

