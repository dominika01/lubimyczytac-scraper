from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

def make_library(url, num_pages, driver_path):
    # --- Setup Chrome ---
    options = Options()
    options.add_argument("--headless")
    service = Service(driver_path)

    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)
    time.sleep(5)  # Wait for page to load

    # Accept cookies
    try:
        accept_btn = driver.find_element(By.CSS_SELECTOR, ".banner-actions-container #onetrust-accept-btn-handler")
        accept_btn.click()
        time.sleep(2)
    except:
        pass

    # Initialize lists
    titles, authors, isbns, shelves = [], [], [], []
    my_reviews, my_ratings, my_dates_read = [], [], []

    for page in range(num_pages):
        soup = BeautifulSoup(driver.page_source, "html.parser")
        book_elements = soup.select(".authorAllBooks__single")

        for book in book_elements:
            # Title, Author, Shelf
            title_el = book.select_one(".authorAllBooks__singleTextTitle")
            author_el = book.select_one(".authorAllBooks__singleTextAuthor")
            shelf_el = book.select_one("div.authorAllBooks__singleTextShelfRight")
            
            title = title_el.get_text(strip=True) if title_el else None
            author = author_el.get_text(strip=True) if author_el else None
            shelf = shelf_el.get_text(strip=True) if shelf_el else None

            titles.append(title)
            authors.append(author)
            shelves.append(shelf)

            # Subpage URL for ISBN
            subpage_url = "https://lubimyczytac.pl" + title_el['href'] if title_el else None
            isbn = None
            if subpage_url:
                driver.get(subpage_url)
                sub_soup = BeautifulSoup(driver.page_source, "html.parser")
                isbn_el = sub_soup.select_one("dt:-soup-contains('ISBN:') + dd")
                isbn = isbn_el.get_text(strip=True) if isbn_el else None
            isbns.append(isbn)
            driver.back()
            time.sleep(1)

            # Rating
            rating_el = book.select_one("span.listLibrary__ratingStarsNumber")
            my_ratings.append(rating_el.get_text(strip=True) if rating_el else None)

            # Review
            review_el = book.select(".expandTextNoJS")
            review = "\n".join([r.get_text(strip=True) for r in review_el]) if review_el else None
            my_reviews.append(review)

            # Date Read
            date_el = book.select_one("div.authorAllBooks__read-dates")
            if date_el:
                # The date is after the <br> tag
                date_text = date_el.get_text(separator="\n").split("\n")[-1].strip()
                my_dates_read.append(date_text if date_text else None)
            else:
                my_dates_read.append(None)

        # Go to next page
        try:
            next_btns = driver.find_elements(By.CSS_SELECTOR, ".next-page a.page-link")
            if next_btns:
                print('next page')
                next_btns[0].click()
                time.sleep(5)
        except:
            break

    # Build DataFrame
    df = pd.DataFrame({
        "Title": titles,
        "Author": authors,
        "ISBN": isbns,
        "My Rating": my_ratings,
        "Date Read": my_dates_read,
        "Exclusive Shelf": shelves,
        "My Review": my_reviews
    }).drop_duplicates()

    driver.quit()
    return df

# --- Usage ---
url = "https://lubimyczytac.pl/ksiegozbior/1wLb78bNbNd"
num_pages=3
driver_path = "/opt/homebrew/bin/chromedriver"
df = make_library(url, num_pages, driver_path)
df.to_csv("library.csv", index=False)