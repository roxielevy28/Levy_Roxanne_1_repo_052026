from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

# 🎯 MILESTONE 3 — Great start! You're exploring how to get book links
#   from a category listing page. This is EXACTLY the right next step.
#   The goal is to combine this with scrapetest.py so that:
#       one script finds ALL the links, and scrapetest.py extracts the data.

url = "https://books.toscrape.com/catalogue/category/books/young-adult_21/index.html"
book= requests.get(url)
# print(category)

soup = BeautifulSoup(book.text,'html.parser')

# link from each book on the page
product = soup.find(id="default")
books_on_page= soup.find_all(class_= 'col-xs-6 col-sm-4 col-md-3 col-lg-3')

raw_book_link=(books_on_page[0].find('h3').find('a')['href'])
# 🔴 BUG: urljoin('url', ...) uses the literal string "url", not your variable.
#   You have `from urllib.parse import urljoin` at the top, so urljoin() is
#   the function from that module. The first argument should be a real URL,
#   like the one you stored in the `url` variable.
#   Fix: urljoin(url, raw_book_link)
Actual_book_link= urljoin('url', raw_book_link)
# print(Actual_book_link) # i was trying to get the link for all the books on the page but i was only able to get the link for the first book. I was trying to loop through the books_on_page list but i was not able to get it to work.

# 💡 HINT for looping over books_on_page:
#   You're on the right track! You stored all the books in `books_on_page`.
#   Now loop over them and extract each link:

#       for book_element in books_on_page:
#           link = book_element.find('h3').find('a')['href']
#           full_url = urljoin(url, link)
#           print(full_url)
#
#   Then — and this is the MILESTONE 3 key — call your book-scraper on each one:
#       scrape_one_book(full_url)

in_the_event_of_other_pages= soup.find(class_='next')
for i in range(1, 3): # this catergory has 3 pages I was trying to get the link for the remaining 2 pages
    url="https://books.toscrape.com/catalogue/category/books/young-adult_21/page-"+str(i)+".html"
    relative_link= in_the_event_of_other_pages.find('a')['href']
    absolute_link= urljoin("https://books.toscrape.com/catalogue/category/books/young-adult_21/index.html", relative_link)

print(absolute_link)



# 💡 PAGINATION THOUGHTS:
#   1. This loop starts at page 1, but page 1 IS the index page you already
#      fetched at the top. So you'll scrape page 1 twice.
#      HINT: try starting from range(2, 4) instead.
#
#   2. The loop overwrites `absolute_link` each time — after the loop ends,
#      you only have the LAST page's link. Think about collecting links
#      into a list: all_pages = [] ... all_pages.append(absolute_link)
#
#   3. When you move to the full site scrape, you'll need to handle pages
#      that DON'T have a "next" button. Check if soup.find(class_='next')
#      is None — that's how you know you're on the last page.
#
#   4. STRETCH: Right now the pagination URL is hardcoded for "young-adult".
#      Can you extract the category name from the URL or breadcrumb so it
#      works for ANY category? (Hint: check the Phase 3 site structure!)

