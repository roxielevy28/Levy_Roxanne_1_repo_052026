from urllib.parse import urljoin
# Harold: (Milestone 3) Added below import — needed to build and export a DataFrame from all scraped books
import pandas as pd
import requests
from bs4 import BeautifulSoup
# Harold: (Milestone 3 → connects to Milestone 2) Importing the reusable scraper function I created in scrapetest.py
# This lets me call scrape_one_book(url) for EACH book URL and get back all its details as a dictionary
from scrapetest import scrape_one_book

category_url = "https://books.toscrape.com/catalogue/category/books/young-adult_21/index.html"

url_for_all_books_in_category=[]

page = requests.get(category_url)
soup = BeautifulSoup(page.text,'html.parser')

product = soup.find(id="default")
books_on_page= soup.find_all(class_= 'col-xs-6 col-sm-4 col-md-3 col-lg-3')

for book_element in books_on_page:
        link = book_element.find('h3').find('a')['href']
        complete_url = urljoin(category_url, link)
        url_for_all_books_in_category.append(complete_url)
    # this retrieved the link for all books on the first page
    
print(url_for_all_books_in_category)

  # this works now. i got all the links on the first page

# Harold: (Milestone 3) Restructured pagination — now it loops through ALL pages, not just page 1
# This is the 'master list' that collects EVERY book dictionary across all pages
all_books = []

# Harold: (Milestone 3, Step 1) Scrape all books on page 1 FIRST
# url_for_all_books_in_category already holds every book link from the first page
for url in url_for_all_books_in_category:
    # Harold: (connects to Milestone 2) Calling the reusable function — pass it one URL, get back a dictionary of all 10 fields
    book_data = scrape_one_book(url)
    all_books.append(book_data)

# Harold: (Milestone 3, Step 2) NOW loop through remaining pages using pagination
# 'while True' keeps going until we run out of 'next' buttons
while True:
    next_button = soup.find(class_='next')
    if not next_button:
        # Harold: No 'next' button means we've hit the last page — time to stop
        break
    
    # Harold: Build the URL for the next page (e.g., page-2.html, page-3.html, etc.)
    next_page = next_button.find("a")["href"]
    category_url = urljoin(category_url, next_page)
    
    # Harold: Fetch and parse THAT next page
    page = requests.get(category_url)
    soup = BeautifulSoup(page.text, 'html.parser')
    
    # Harold: Extract all book links from this new page, same as we did for page 1
    books_on_page = soup.find_all(class_='col-xs-6 col-sm-4 col-md-3 col-lg-3')
    for book_element in books_on_page:
        link = book_element.find('h3').find('a')['href']
        complete_url = urljoin(category_url, link)
        # Harold: Scrape each book and add it to the SAME master list (all_books keeps growing)
        book_data = scrape_one_book(complete_url)
        all_books.append(book_data)

# Harold: (Milestone 3, Step 3) Export everything to ONE CSV — all books from every page in this category
master_report = pd.DataFrame(all_books)
master_report.to_csv('all_books.csv', index=False)




