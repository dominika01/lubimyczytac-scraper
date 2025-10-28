from get_library import get_library
from goodreads_formatter import transform_goodreads_format

url = "/profile/url"
num_pages = 17
driver_path = "/chromedriver/path"

df = get_library(url, num_pages, driver_path)
df.to_csv("library.csv", index=False)
print("Done! Saved to library.csv")

print(f"/nTransforming to goodreads format...")
gr_df = transform_goodreads_format(df)
gr_df.to_csv("gr_library.csv", index=False)
print("Done! Saved to gr_library.csv")