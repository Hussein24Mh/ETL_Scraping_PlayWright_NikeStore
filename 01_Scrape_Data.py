import time
import json
from rich import print
from playwright.sync_api import sync_playwright
from selectolax.parser import HTMLParser
from dataclasses import dataclass, field


pre = 'https://www.nike.com/gb/t/'
url = 'https://www.nike.com/gb/w/mens-shoes-nik1zy7ok'

links = []
extracted_data_object = []
data_file = 'Data/Nike_Shoes.json'


def save_data():

    json_object = json.dumps([item.__dict__ for item in extracted_data_object], indent=4)

    with open(data_file, 'w') as outfile:
        outfile.write(json_object)


@dataclass
class DataRaw:
    title: str
    sup_title: str = field(default="")
    color_num: str = field(default="")
    price: str = field(default="")
    offer_price: str = field(default="")
    off_percent: str = field(default="")
    tag: str = field(default="")
    url: str = field(default="")


def parse_data(node):
    raw = DataRaw(
        title=node.css_first('div.product-card__title').text(),
        sup_title=node.css_first('div.product-card__subtitle').text(),
        color_num=node.css_first('div.product-card__count-item').text().split(" ")[0],
        url=node.css_first('a').attributes['href']
    )

    try:
        raw.price = node.css_first('div[Data-testid=product-price]').text().strip('£')
    except:
        return

    try:
        raw.offer_price = node.css_first('div[Data-testid=product-price-reduced]').text().strip('£')
    except:
        pass

    try:
        raw.off_percent = node.css_first('div.product-price__perc').text()
    except:
        pass

    try:
        raw.tag = node.css_first('div[Data-testid=product-card__messaging]').text()
    except:
        pass
    extracted_data_object.append(raw)
    print(raw)


def get_data():  # start browser work

    with sync_playwright() as playwright:

        browser = playwright.chromium.launch(headless=False, slow_mo=50)

        page = browser.new_page()

        page.goto(url)

        time.sleep(4)
        page.click('span#hf_cookie_text_cookieAccept')

        for x in range(1, 20):
            page.keyboard.press('End')
            time.sleep(2)

        # Data slicing

        html = page.inner_html('div#skip-to-products')

        tree = HTMLParser(html)

        nodes = tree.css('div.product-card__body')

        for i in range(len(nodes)):
            print(i)
            parse_data(nodes[i])

        print(len(nodes))


get_data()
save_data()
