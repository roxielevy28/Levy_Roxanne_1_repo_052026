from urllib.parse import urljoin
import pandas as pd
import requests
from bs4 import BeautifulSoup

catergory= requests.get('https://books.toscrape.com/catalogue/category/books/young-adult_21/index.html')
response= get
soup = BeautifulSoup (catergory.content, 'html.parser')

product = soup.find(id="default")

books_on_page= soup.find_all(class_= 'col-xs-6 col-sm-4 col-md-3 col-lg-3')

raw_book_link=(books_on_page[0].find('h3').find('a')['href'])
Actual_book_link= urljoin("https://books.toscrape.com/catalogue/category/books/young-adult_21/index.html", raw_book_link)
print(Actual_book_link) # i was trying to get the link for all the books on the page but i was only able to get the link for the first book. I was trying to loop through the books_on_page list but i was not able to get it to work.

in_the_event_of_other_pages= soup.find(class_='next')
for i in range(1, 3): # this catergory has 3 pages I was trying to get the link for the remaining 2 pages
    url="https://books.toscrape.com/catalogue/category/books/young-adult_21/page-"+str(i)+".html"
    next_page_links= in_the_event_of_other_pages.find('a')['href']
    actual_next_page_links= urljoin("https://books.toscrape.com/catalogue/category/books/young-adult_21/index.html", next_page_links)

print(actual_next_page_links)


