from urllib.parse import urljoin
import pandas as pd
import requests
from bs4 import BeautifulSoup
from scrapetest import scrape_one_book

# =============================================================================
# 🔴 ISSUE #1 — 'Books' homepage scraped as a category (wrong!)
# =============================================================================
# Harold: (2026-06-28, Milestone 4) The sidebar navigation on books.toscrape.com
# has "Books" as the FIRST link — but that's the HOMEPAGE, not a real category.
# Your loop scrapes it anyway, producing books.csv (all 1000 books) which is
# a duplicate of what every other category already covers.
#
# ✅ FIX: Skip the first item in the loop. Change:
#        for category in category_links:
#    To:
#        for category in category_links[1:]:
#
# 🎯 WHY: Without this fix, you waste time re-scraping all 1000 books AND
#    you get a misleading books.csv that isn't a real category.

# =============================================================================
# 🔴 ISSUE #2 — NO ERROR HANDLING: One bad category crashes everything
# =============================================================================
# Harold: (2026-06-28, Milestone 4) This loop runs through 50 categories. If
# ONE category fails (network error, unexpected HTML, etc.), the entire script
# crashes and you lose ALL categories you already scraped and saved.
#
# ✅ FIX: Wrap the entire category loop body in try/except:
#
#        for category in category_links[1:]:
#            try:
#                cat_name = category["name"]
#                cat_url  = category["url"]
#                ... (all the scraping logic) ...
#                df.to_csv(f"csv_reports/{safe_name}.csv", index=False)
#            except Exception as e:
#                print(f"  ❌ Failed on {cat_name}: {e}")
#                continue
#
# 🎯 WHY: With 50 categories, the chance of at least one failure is very high.
#    This way you get 49 good CSVs instead of 0.

# =============================================================================
# 🟡 ISSUE #3 — CSVs saved to root folder (needs subfolder)
# =============================================================================
# Harold: (2026-06-28, Milestone 4) Same as Phase2 — all 50 CSV files are
# dumped in the project root, mixed with your Python scripts.
#
# ✅ FIX: Add `import os` at the top, then before the loop add:
#        os.makedirs('csv_reports', exist_ok=True)
#    And change the save line to:
#        df.to_csv(f"csv_reports/{safe_name}.csv", index=False)

# =============================================================================
# 🟢 ISSUE #4 — Minor cleanup: typo and unused variable
# =============================================================================
# Harold: (2026-06-28, Milestone 4) Two small things:
#
# 1. TYPO: `catergory_name` should be `category_name` (appears on line 22)
#    Fix: rename it everywhere in this file.
#
# 2. UNUSED VARIABLE: `page_content = soup.find(id="default")` on line 19
#    is never used anywhere in this file. Delete it.
#
# 3. DUPLICATE: `all_book_urls = []` appears twice (lines 33 and 36).
#    Remove the second one.

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

for category in category_links[1:]:
     try:
     cat_name = category["name"]
     cat_url  = category["url"]
     ... (all the scraping logic) ...
     df.to_csv(f"csv_reports/{safe_name}.csv", index=False)
     except Exception as e:
     print(f"  ❌ Failed on {cat_name}: {e}")
     continue

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



# =============================================================================
# 🎯 HAROLD'S MILESTONE 4 GUIDE — Scrape ALL books from ALL categories
# =============================================================================
# The code above works — it gets you a list of every category and its URL. ✅
# Now you need to visit each category, scrape every book in it, and save the
# results to a SEPARATE CSV file for each category.
#
# Here's a plan to follow. Try uncommenting and building this step by step:
#
# ---------------------------------------------------------------------------
# Harold: (Milestone 4, Step 1) — LOOP through each category from the list
# ---------------------------------------------------------------------------

#
# ---------------------------------------------------------------------------
# Harold: (Milestone 4, Step 2 — same logic as Milestone 3 Phase2) FETCH first page, collect book links
# ---------------------------------------------------------------------------
#   
#
# ---------------------------------------------------------------------------
# Harold: (Milestone 4, Step 3 — pagination, same pattern as Phase2) Click 'next' until no more pages
# ---------------------------------------------------------------------------
#     while True:
#         next_button = soup.find(class_='next')
#         if not next_button:
#             break
#         next_page = next_button.find("a")["href"]
#         cat_url = urljoin(cat_url, next_page)
#
#         page = requests.get(cat_url)
#         soup = BeautifulSoup(page.text, 'html.parser')
#         books_on_page = soup.find_all(class_='col-xs-6 col-sm-4 col-md-3 col-lg-3')
#
#         for book_element in books_on_page:
#             link = book_element.find('h3').find('a')['href']
#             full_url = urljoin(cat_url, link)
#             all_book_urls.append(full_url)
#
# ---------------------------------------------------------------------------
# Harold: (Milestone 4, Step 4 — connects to Milestone 2!) Call scrape_one_book() for EVERY book URL
# ---------------------------------------------------------------------------
#     all_books = []
#     for url in all_book_urls:
#         # Harold: This is the function I built in scrapetest.py (Milestone 2) — one call, all 10 fields back
#         book_data = scrape_one_book(url)
#         all_books.append(book_data)
#
# ---------------------------------------------------------------------------
# Harold: (Milestone 4, Step 5) SAVE each category to its OWN CSV file
# ---------------------------------------------------------------------------
#     safe_name = cat_name.lower().replace(" ", "_")
#     df = pd.DataFrame(all_books)
#     df.to_csv(f"{safe_name}.csv", index=False)
#     print(f"  ✅ Saved {len(all_books)} books to {safe_name}.csv")
#
# ---------------------------------------------------------------------------
# 💡 HAROLD'S TIPS
# ---------------------------------------------------------------------------
# - Category names from the sidebar include "Books" as the first item and
#   the genre "Poetry" may appear. You already handled those in your loop.
# - Use safe_name = cat_name.lower().replace(" ", "_") to avoid filename errors.
# - Harold: (Milestone 4, error handling) If a category fails, wrap the inner code
#   in try/except so one failure doesn't crash the WHOLE script:
#
#       try:
#           ... scraping logic ...
#       except Exception as e:
#           print(f"  ❌ Error on {cat_name}: {e}")
#
# - Harold: (Milestone 4, testing tip) Test with ONE category first!
#   Add 'break' after the first category to verify it works before looping all 50:
#
#       for category in category_links:
#           ... all the code ...
#           break   # ← remove this once the first category works
#
# =============================================================================

