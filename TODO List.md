# TODO List — Milestone 3

Hey! I've looked through your work and here's everything I think you should tackle next. Some are quick fixes, some are bigger challenges — take them in order.

---

## 1. Fix `urljoin('url', ...)` (Phase2 file) 🔴

On line 17 of `Phase2_Young.Adult.category.py`, you wrote:

```python
Actual_book_link = urljoin('url', raw_book_link)
```

The first argument is the literal string `"url"`, not your variable `url`. That means it's trying to join against the text "url" instead of the actual URL. Fix it to:

```python
Actual_book_link = urljoin(url, raw_book_link)
```

## 2. Loop through ALL books on the page, not just the first one (Phase2 file) 🟡

You're only grabbing `books_on_page[0]`. You already have a list of every book on the page — now loop over them! Something like:

```python
for book_element in books_on_page:
    link = book_element.find('h3').find('a')['href']
    full_url = urljoin(url, link)
    print(full_url)
```

Once that's working, take it further — instead of printing, call your book-scraper:

```python
book_data = scrape_one_book(full_url)
```

## 3. Fix the pagination loop (Phase2 file) 🟡

A couple of things here:

- **You're scraping page 1 twice.** Your loop starts at `range(1, 3)` but page 1 is the index page you already fetched at the top. Try `range(2, 4)` instead.
- **You're overwriting `absolute_link`.** After the loop, you only have the last page saved. Collect them into a list instead:
  ```python
  all_page_links = []
  all_page_links.append(absolute_link)
  ```
- **Think about detecting the last page.** What if a category only has 1 page? Your loop runs 1–3 regardless. Check if `soup.find(class_='next')` returns `None` — that's how you know you're done.

## 4. Refactor `scrapetest.py` into a reusable function 🎯

This is the big one for Milestone 3. Right now your book-scraper runs top-to-bottom for one hardcoded book. Wrap it in a function so `Phase2` can call it for every link:

```python
def scrape_one_book(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    # ... all your extraction code ...
    return {
        'product_page_url': url,
        'Book_Title': title,
        # ... etc ...
    }
```

## 5. Scale the DataFrame — collect first, export once 🎯

Right now you create one DataFrame per book. For 1,000 books you'd have 1,000 CSVs. Instead, collect everything into one list and build a single DataFrame at the end:

```python
all_books = []
for url in all_book_urls:
    book_data = scrape_one_book(url)
    all_books.append(book_data)

master_report = pd.DataFrame(all_books)
master_report.to_csv('all_books.csv', index=False)
```

## 6. Fix inconsistent naming 🟢

You're mixing styles:

| ✅ Good (snake_case) | 🔄 Needs changing |
|---|---|
| `review_rating` | `Book_Title` → `book_title` |
| `Table_Data` | `Image_URL` → `image_url` |
| | `Book_Report` → `book_report` |

Python convention is `snake_case` — pick it and stick with it. Not critical, but it'll help when your scripts get bigger.

## 7. Rename `import requests.py` 🟡

This filename conflicts with the `requests` library itself. When you write `import requests` in another file, Python might get confused and try to import *this file* instead of the real library. Rename it to something like `book_scraper_v1.py`.

## 8. Clean up `new_file.py` 🟢

This file just contains `'pip install pandas'` — looks like a note-to-self that got saved as a .py file. You can delete it.

## 9. Store shared URLs in one place 🟢

You're using `"https://books.toscrape.com/catalogue/"` in multiple places across multiple files. If the site ever changes, you'd need to hunt down every occurrence. Store it in one variable:

```python
BASE_URL = "https://books.toscrape.com/catalogue/"
```

---

## Stretch challenge 🌟

Right now your pagination URL is hardcoded for the Young Adult category. Can you extract the category name dynamically so it works for any category on the site? (Hint: check the Phase 3 site structure — you'll need to scrape the main page to find ALL categories first.)

---

You've got a really solid foundation — the single-book scraper works correctly, and you're asking the right questions about how to scale up. Most of these are small steps from where you are now. You've got this!
