import pandas as pd
from datetime import datetime

def pre_format_GR(raw_data: pd.DataFrame) -> pd.DataFrame:
    df = raw_data.copy()

    # Change column names dots to spaces
    df.columns = [col.replace(".", " ") for col in df.columns]

    # Convert ratings from 0-10 scale to 1-5 scale
    def convert_rating(r):
        if pd.isna(r) or r == "":
            return 0
        return float(r) / 2

    df["My Rating"] = df["My Rating"].apply(convert_rating)

    # Convert date format YYYY-MM-DD -> YYYY/MM/DD
    if "Date Read" in df.columns:
        df["Date Read"] = df["Date Read"].str.replace("-", "/", regex=False).fillna("")

    # Fill NaN values with empty string
    df = df.fillna("")

    return df


def GR_df_matrix(num_books: int) -> pd.DataFrame:
    columns = [
        "Book Id", "Title", "Author", "Author l - f", "Additional Authors", "ISBN", "ISBN13",
        "My Rating", "Average Rating", "Publisher", "Binding", "Number of Pages",
        "Year Published", "Original Publication Year", "Date Read", "Date Added",
        "Bookshelves", "Bookshelves with positions", "Exclusive Shelf", "My Review",
        "Spoiler", "Private Notes", "Read Count", "Owned Copies"
    ]
    return pd.DataFrame("", index=range(num_books), columns=columns)


def goodreads_data(book_data: pd.DataFrame) -> pd.DataFrame:
    num_books = len(book_data)
    GD_df = GR_df_matrix(num_books)

    # Copy matching columns
    for col in set(book_data.columns).intersection(GD_df.columns):
        GD_df[col] = book_data[col]

    # Process shelves
    shelf_map = {
        "Przeczytane": "read",
        "Chcę przeczytać": "to-read",
        "Teraz czytam": "currently-reading"
    }

    exclusive_list = []
    bookshelves_list = []
    owned_list = []

    for shelves in GD_df["Exclusive Shelf"]:
        if not shelves:
            exclusive_list.append("")
            bookshelves_list.append("")
            owned_list.append(0)
            continue

        parts = [p.strip() for p in shelves.split(",") if p.strip()]
        exclusive = shelf_map.get(parts[0], parts[0])
        extras = [p for p in parts[1:] if p != "Posiadam"]
        owned = 1 if "Posiadam" in parts[1:] else 0

        exclusive_list.append(exclusive)
        bookshelves_list.append(", ".join(extras))
        owned_list.append(owned)

    GD_df["Exclusive Shelf"] = exclusive_list
    GD_df["Bookshelves"] = bookshelves_list
    GD_df["Owned Copies"] = owned_list

    # Add positions for to-read and currently-reading
    status_list = [""] * num_books
    to_read_counter = 1
    reading_counter = 1
    for i in reversed(range(num_books)):
        shelf = GD_df.loc[i, "Exclusive Shelf"]
        if shelf == "to-read":
            status_list[i] = f"to-read (#{to_read_counter})"
            to_read_counter += 1
        elif shelf == "currently-reading":
            status_list[i] = f"currently-reading (#{reading_counter})"
            reading_counter += 1
    GD_df["Bookshelves with positions"] = status_list

    # Read count
    GD_df["Read Count"] = GD_df["Exclusive Shelf"].apply(lambda x: 1 if x in ["read", "currently-reading"] else 0)

    # Set Date Added to today
    GD_df["Date Added"] = datetime.today().strftime("%Y/%m/%d")

    return GD_df


def transform_goodreads_format(raw_data: pd.DataFrame) -> pd.DataFrame:
    formatted = pre_format_GR(raw_data)
    gd_df = goodreads_data(formatted)
    return gd_df
