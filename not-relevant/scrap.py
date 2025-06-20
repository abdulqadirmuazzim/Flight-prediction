import requests
from bs4 import BeautifulSoup
import pandas as pd

# has 3 pages
url1 = "https://foreteconline.com/page/page_/?s=HP+PC&product_cat=0&post_type=product"

# has 6 pages
url2 = "https://foreteconline.com/page/page_/?s=HP+Printer&product_cat=0&post_type=product&v=330a840f8637"


def scrap_site(url):
    res = requests.get(url)

    soup1 = BeautifulSoup(res.text, "html.parser")

    result1 = soup1.find_all(
        "div", attrs={"class": "product-inner product-item__inner"}
    )

    titles = []
    prices = []

    for a in result1:
        # title
        name = str(a.select_one(".woocommerce-loop-product__title").text).encode()
        name = str(name).strip("b'")
        # price
        price = str(a.select_one("bdi").get_text("</span>").split("</span>")[1])
        price = int(float(price.replace(",", "")))
        titles.append(name)
        prices.append(price)

    frame = pd.DataFrame({"Name": titles, "Prices": prices})

    return frame


def scrap_pages(url, page_nums, csv_name):

    pages = []

    for page in range(1, page_nums + 1):
        print(f"Scraping page {page}...")
        url = url2.replace("page_", f"{page}")
        frame = scrap_site(url)
        pages.append(frame)

    file = pd.concat(pages).reset_index(drop=True)
    file.to_csv(csv_name, index=False)


# laptops
scrap_pages(url1, 3, "Laptops.csv")
# printers
scrap_pages(url2, 6, "Printers.csv")
