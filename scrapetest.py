import pandas as pd
import requests
from bs4 import BeautifulSoup

# ✅ Good start! You've imported the libraries and fetched the page.
# TIP: Instead of printing the whole soup, try using your browser's "Inspect Element"
#   on the book page to see the HTML structure. Look at the class names carefully.

page = requests.get('https://books.toscrape.com/catalogue/set-me-free_988/index.html')
soup = BeautifulSoup (page.content, 'html.parser')
# print(soup)  # ← You can comment this out once you know the structure

# ❓ HINT: The id "default" wraps the whole page content. That's fine as a starting
#   point, but you can also search directly for the elements you need from `soup`.
product = soup.find(id="default")
# print(product)

# ✅ You found the right class for the product info section!
items = product.find_all(class_= 'col-sm-6 product_main')
# print(items)

# ⚠️ SYNTAX: Missing closing `)` on both lines below — Python will throw an error.
#   Every opening `(` needs a matching `)`.
# ❓ HINT: `find()` returns the *element*. To get the text inside it, you need
#   to use `.text` or `.get_text()` on the result. Try printing the element first,
#   then figure out how to extract just the text.
print(items[0].find(class_= 'instock availability').get_text())
print(items[0].find(class_= 'star-rating Five').get_text())

# ⚠️ SYNTAX: Missing closing `]` on both lines — brackets must match parentheses.
# ❓ HINT: The star-rating is stored in the class name itself (e.g. "star-rating Five").
#   The number of stars is the *second class* on that `<p>` tag. Think about how
#   to read the class attribute from the element to get the word "Five", then
#   convert that word to a number.
quantity_available = [items[0].find(class_= 'instock availability')]
review_rating = [items[0].find(class_= 'star-rating Five')]


# ✅ You found the right table! It has all the price/UPC info you need.
# ❓ HINT: The table has rows (`<tr>`) with headers (`<th>`) and data (`<td>`).
#   Each row is a key-value pair. For example, the row with "Price (excl. tax)"
#   in the `<th>` has the actual price in the `<td>` next to it.
#   Try: loop through all `<tr>` elements and print each `<th>` and `<td>` pair.
items_2[0] = product.find_all(class_= 'table table-striped')

# ⚠️ SYNTAX: `items[2]` should probably be `items_2[0]` — check your variable names.
#   Also, the `find(class_= '')` has an empty class name. What class or tag are you
#   actually looking for inside the table?
print(items[2].find(class_= '')

# ⚠️ SYNTAX: Variable names cannot contain spaces. Also, `find_` is incomplete —
#   `find()` needs arguments. You need to figure out *which* `<td>` contains each
#   piece of data. Think about using the `<th>` text (like "UPC", "Price (excl. tax)")
#   to locate the right row, then grab the `<td>` next to it.
universal_ product_code (upc) = items_2[0].find_
price_including_tax = items_2[0].find_
price_excluding_tax

print(quantity_available)
print(review_rating)

# ⚠️ SYNTAX: `pd` is not imported. You need `import pandas as pd` at the top.
# ⚠️ SYNTAX: A DataFrame needs a dictionary with *key: value* pairs, not just a
#   set of strings. Example: {"column_name": [value1, value2]}
# ❓ HINT: You still need to extract these fields from the page:
#   - book_title: look inside the `<h1>` in `product_main`
#   - product_description: look for the `<div>` with id="product_description",
#     then get the text from the `<p>` tag that follows it
#   - category: look at the breadcrumb `<ul class="breadcrumb">` — which `<a>`
#     link is the category (not "Home" or "Books")?
#   - image_url: look for the `<img>` tag inside `<div class="item active">`
#   - product_page_url: this is just the URL you used in requests.get()
 data ["product_page_url"]= https://books.toscrape.com/catalogue/set-me-free_988/index.html
Book_Report = pd.DataFrame(
    {
    "product_page_url",
    "universal_product_code",
    "book_title",
    "price_including_tax",
    "price_excluding_tax",
    "quantity_available",
    "product_description",
    "category",
    "review_rating",
    "image_url"
    })
    print(Book_Report)