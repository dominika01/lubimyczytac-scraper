from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time
import requests

def get_library(url, num_pages, driver_path):
    # setup chrome driver
    options = Options()
    options.add_argument("--headless")
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)
    time.sleep(5)

    # accept cookies
    try:
        accept_btn = driver.find_element(By.CSS_SELECTOR, ".banner-actions-container #onetrust-accept-btn-handler")
        accept_btn.click()
        time.sleep(2)
    except:
        pass

    # initialize lists
    titles, authors, isbns, shelves = [], [], [], []
    my_reviews, my_ratings, my_dates_read = [], [], []

    for page in range(num_pages):
        print(f"Processing page {page+1}...")
        # wait for all books to be present
        book_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".authorAllBooks__single"))
        )

        # extract outerHTML to avoid stale elements
        book_html_list = [be.get_attribute("outerHTML") for be in book_elements]

        for html in book_html_list:
            soup = BeautifulSoup(html, "html.parser")

            # basic book info
            title_el = soup.select_one(".authorAllBooks__singleTextTitle")
            author_el = soup.select_one(".authorAllBooks__singleTextAuthor")
            shelf_el = soup.select_one("div.authorAllBooks__singleTextShelfRight")

            title = title_el.get_text(strip=True) if title_el else None
            author = author_el.get_text(strip=True) if author_el else None
            shelf = shelf_el.get_text(strip=True) if shelf_el else None
            
            titles.append(title)
            authors.append(author)
            shelves.append(shelf)

            # isbn
            isbn = None
            if title_el:
                subpage_url = "https://lubimyczytac.pl" + title_el['href']
                try:
                    resp = requests.get(subpage_url)
                    sub_soup = BeautifulSoup(resp.text, "html.parser")
                    isbn_el = sub_soup.select_one("dt:-soup-contains('ISBN:') + dd")
                    if isbn_el:
                        isbn = isbn_el.get_text(strip=True)
                except:
                    isbn = None
            isbns.append(isbn)

            # rating
            rating_els = soup.select("span.listLibrary__ratingStarsNumber")
            rating = rating_els[1].get_text(strip=True) if len(rating_els) >= 2 else None
            my_ratings.append(rating)

            # review
            review_el = soup.select(".expandTextNoJS")
            review = "\n".join([r.get_text(strip=True) for r in review_el]) if review_el else None
            my_reviews.append(review)

            # date read
            date_el = soup.select_one("div.authorAllBooks__read-dates")
            date_text = None
            if date_el:
                lines = date_el.get_text(separator="\n").split("\n")
                date_text = lines[-1].strip() if len(lines) > 1 else None
            my_dates_read.append(date_text)
            
            print(f"\tAdded '{title}'")

        # open next page
        try:
            next_btn = driver.find_element(By.CSS_SELECTOR, "li.page-item.next-page a.page-link")
            driver.execute_script("arguments[0].scrollIntoView(true);", next_btn)
            driver.execute_script("arguments[0].click();", next_btn)
            time.sleep(5)  # wait for page to load
        except:
            print("No more pages.")
            break

    # build dataframe
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