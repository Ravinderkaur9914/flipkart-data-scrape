import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.flipkart.com/search?q=laptop"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

resp = requests.get(url, headers=headers)
soup = BeautifulSoup(resp.text, "html.parser")

names = []
sale_prices = []
mrp_prices = []
offers = []
reviews = []

# Flipkart uses "_1AtVbE" for wrappers, and inside that many product cards use "a" with title attr
cards = soup.find_all("div", class_="_1AtVbE")

for c in cards:
    # Find product link with title
    a = c.find("a", attrs={"title": True})
    if not a:
        continue
    name = a["title"].strip()
    names.append(name)

    # Sale price
    sale = c.find("div", class_="_30jeq3")
    sale_prices.append(sale.text.strip() if sale else "N/A")

    # MRP / old price (if any)
    mrp = c.find("div", class_="_3I9_wc")
    mrp_prices.append(mrp.text.strip() if mrp else "N/A")

    # Offer (discount %)
    off = c.find("div", class_="_3Ay6Sb")
    offers.append(off.text.strip() if off else "N/A")

    # Reviews / rating
    rev = c.find("span", class_="_2_R_DZ")
    reviews.append(rev.text.strip() if rev else "N/A")

df = pd.DataFrame({
    "Name of Product": names,
    "Total Price (MRP)": mrp_prices,
    "Sale Price": sale_prices,
    "Offers": offers,
    "Reviews": reviews
})

df.to_excel("Flipkart_Laptops.xlsx", index=False)
print("Rows scraped:", len(df))
print(df.head())
