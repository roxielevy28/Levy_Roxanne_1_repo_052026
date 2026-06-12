from urllib.parse import urljoin
import pandas as pd
import requests
from bs4 import BeautifulSoup

catergory= requests.get('https://books.toscrape.com/catalogue/category/books/young-adult_21/index.html')
# print(catergory)

soup = BeautifulSoup(catergory.text,'html.parser')

# link from each book on the page
product = soup.find(id="default")
books_on_page= soup.find_all(class_= 'col-xs-6 col-sm-4 col-md-3 col-lg-3')

raw_book_link=(books_on_page[0].find('h3').find('a')['href'])
Actual_book_link= urljoin("https://books.toscrape.com/catalogue/category/books/young-adult_21/index.html", raw_book_link)
print(Actual_book_link) # i was trying to get the link for all the books on the page but i was only able to get the link for the first book. I was trying to loop through the books_on_page list but i was not able to get it to work.

for i in range(1, 3): # this catergory has 3 pages I was trying to get the link for the remaining 2 pages
    url="https://books.toscrape.com/catalogue/category/books/young-adult_21/page-"+str(i)+".html"
    response = requests.get(url)
    soup = BeautifulSoup(response.text,'html.parser')
    next_page_link= soup.find(class_='next').get('a')['href']
    absolute_link= urljoin("https://books.toscrape.com/catalogue/category/books/young-adult_21/index.html", next_page_link)
    url= absolute_link
    
print(url)

