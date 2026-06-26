from urllib.parse import urljoin
import os
import requests
from bs4 import BeautifulSoup

def clean_filename(name):
    return "".join(c if c.isalnum() else "_" for c in name.lower())

def get_all_category_links():
    home_url = 'https://books.toscrape.com/index.html'
    page = requests.get(home_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    category_links = []
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
    return category_links

def get_all_book_links(cat_url):
    all_book_urls = []
    while True:
        page = requests.get(cat_url)
        soup = BeautifulSoup(page.content, 'html.parser')
        books_on_page = soup.find_all('article', class_='product_pod')
        for book_element in books_on_page:
            link = book_element.find('h3').find('a')['href']
            full_url = urljoin(cat_url, link)
            all_book_urls.append(full_url)

        next_button = soup.find(class_='next')
        if not next_button:
            break
        next_page = next_button.find('a')['href']
        cat_url = urljoin(cat_url, next_page)

    return all_book_urls

def download_image(image_url, category_type, book_title):
    name_of_folder = clean_filename(category_type)
    os.makedirs(name_of_folder, exist_ok=True)

    response = requests.get(image_url, stream=True)
    if response.status_code != 200:
        return None

    _, ext = os.path.splitext(image_url)
    if not ext:
        ext = '.jpg'

    filename = f"{clean_filename(book_title)}{ext}"
    file_path = os.path.join(name_of_folder, filename)

    with open(file_path, 'wb') as f:
        for chunk in response.iter_content(1024):
            f.write(chunk)

    return file_path
