from get_library import get_library
from goodreads_formatter import transform_goodreads_format

url = "https://lubimyczytac.pl/ksiegozbior/1wLb78bNbNd"
num_pages = 17
driver_path = "/opt/homebrew/bin/chromedriver"
half_stars = False # for sites like Storygraph that accept half stars 

df = get_library(url, num_pages, driver_path)
df.to_csv("library.csv", index=False)
print("Done! Saved to library.csv")

print(f"/nTransforming to goodreads format...")
gr_df = transform_goodreads_format(df, half_stars)
gr_df.to_csv("gr_library.csv", index=False)
print("Done! Saved to gr_library.csv")