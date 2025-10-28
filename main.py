from get_library import get_library

url = "https://lubimyczytac.pl/ksiegozbior/1wLb78bNbNd"
num_pages = 1
driver_path = "/opt/homebrew/bin/chromedriver"

df = get_library(url, num_pages, driver_path)
df.to_csv("library.csv", index=False)
print("Done! Saved to library.csv")