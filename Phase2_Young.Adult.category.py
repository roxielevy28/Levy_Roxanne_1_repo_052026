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


# 2. The `url_for_all_books_in_category` list is built but only used in the
#    loop below. Consider adding a count print so you know how many books
#    were found:
#        print(f"Found {len(url_for_all_books_in_category)} books on page 1")
#
# 3. After the final CSV save, add a confirmation:
#        print(f"✅ Saved {len(all_books)} books to young_adult.csv")
#    This way you see in the terminal that it worked.

#
#    🎯 SAME FIX NEEDED IN All_Category.py:
#        os.makedirs('csv_reports', exist_ok=True)
#        df.to_csv(f"csv_reports/{safe_name}.csv", index=False)
#
# 🎯 WHY: Keeps your project organized — code in one place, data in another.
#    Also makes it easy to delete all CSVs at once (just delete the folder)
#    without accidentally deleting your scripts.

# =============================================================================
# 📋 SUMMARY: What's documented vs what still needs actual code changes
# =============================================================================
# Harold: (2026-06-28, Milestones 2/3/4) This file has COMMENTS explaining
# every issue, but the actual code has NOT been changed yet. Here's your
# checklist of what to fix and WHERE:
#
# ┌─────┬──────────────────────────────┬─────────────────────┬──────────┐
│  #  │ Issue                        │ Fix in which file   │ Status   │
# ├─────┼──────────────────────────────┼─────────────────────┼──────────┤
│  1  │ List-wrapped CSV values      │ scrapetest.py       │ done  │
│  2  │ No error handling            │ Phase2 + All_Cat    │ ❌ TODO  │
│  3  │ Generic 'all_books.csv' name │ Phase2_Young...py   │ done  │
│  4  │ quantity_available is string │ scrapetest.py       │ done  │
│  5  │ Duplicated descriptions      │ scrapetest.py       │ done  │
│  6  │ CSVs scattered in root       │ Phase2 + All_Cat    │ ❌ TODO  │
│  7  │ 'Books' homepage in loop     │ All_Category.py     │ ❌ TODO  │
│  8  │ Image download no error hdlg │ Image_files.py      │ done  │
│  9  │ catergory_name typo          │ All_Category.py     │ ❌ TODO  │
│ 10  │ Unused variables             │ All_Category.py     │ ❌ TODO  │
└─────┴──────────────────────────────┴─────────────────────┴──────────┘
#
# 🎯 RECOMMENDED ORDER:
#    Fix #1 first (scrapetest.py) — it affects EVERYTHING downstream
#    Fix #2 next — protects all your scraping from crashes
#    Fix #6 — keeps your folder clean before you regenerate all CSVs
#    Then fix the rest in any order




