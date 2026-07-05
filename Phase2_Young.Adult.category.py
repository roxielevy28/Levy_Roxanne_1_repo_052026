from urllib.parse import urljoin
import pandas as pd
import os
import requests
from bs4 import BeautifulSoup
from scrapetest import scrape_one_book

category_url = "https://books.toscrape.com/catalogue/category/books/young-adult_21/index.html"

url_for_all_books_in_category=[]

page = requests.get(category_url)
soup = BeautifulSoup(page.text,'html.parser')

books_on_page= soup.find_all(class_= 'col-xs-6 col-sm-4 col-md-3 col-lg-3')

for book_element in books_on_page:
        link = book_element.find('h3').find('a')['href']
        complete_url = urljoin(category_url, link)
        url_for_all_books_in_category.append(complete_url)
    
print(url_for_all_books_in_category)

all_books = []

for url in url_for_all_books_in_category:
    try:
        book_data = scrape_one_book(url)
        all_books.append(book_data)
    except Exception as e:
        print(f"  ⚠️ Skipped {url}: {e}")
        continue

while True:
    next_button = soup.find(class_='next')
    if not next_button:
        break
    
    next_page = next_button.find("a")["href"]
    category_url = urljoin(category_url, next_page)
    
    page = requests.get(category_url)
    soup = BeautifulSoup(page.text, 'html.parser')
    
    books_on_page = soup.find_all(class_='col-xs-6 col-sm-4 col-md-3 col-lg-3')
    for book_element in books_on_page:
        link = book_element.find('h3').find('a')['href']
        complete_url = urljoin(category_url, link)
        book_data = scrape_one_book(complete_url)
        all_books.append(book_data)

master_report = pd.DataFrame(all_books)
os.makedirs('csv_reports', exist_ok=True)
master_report.to_csv('csv_reports/young_adult.csv', index=False)




