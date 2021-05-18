from selenium import webdriver
from lxml import html
import time
import json
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from prod_specs import get_product_specs

##################################################################################################
##################################################################################################
# variables to change according to preferences
myUrl = 'https://www.aliexpress.com/category/702/laptops.html?spm=a2g0o.home.104.10.650c2145mik6Dq'
output_file = 'laptops.json'
##################################################################################################
##################################################################################################

def add_to_main_list(lst, main):
    for i in lst:
        if i[0] == '/':
            main.append('https:' + i.strip())

        else: main.append(i.strip())


profile = webdriver.FirefoxProfile('./7t2bdg4x.Selenium_AL')
browser = webdriver.Firefox(profile)

# list of attributes to help in storing values as tuples
titles = []
stores = []
prices = []
reviews = []
nb_solds = []
thumbnail_links = []
prod_links = []

print('Finding products, please wait')

for page_nb in range(1, 2):

    browser.get(myUrl + '&page={}'.format(page_nb))

    # scroll down page slowly to wait for hidden products to show
    start_time = time.time()
    seconds = 5

    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time

        browser.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
        time.sleep(0.5)

        if elapsed_time > seconds:
            break

    # get html content
    tree = html.fromstring(browser.page_source)

    # get data
    title = tree.xpath('//a[@class="item-title"]/@title')
    store = tree.xpath('//a[@class="store-name"]/text()')
    price = tree.xpath('//span[@class="price-current"]/text()')
    review = tree.xpath('//span[@class="rating-value"]/text()')
    nb_sold = tree.xpath('//a[@class="sale-value-link"]/text()')
    thumbnail_link = tree.xpath('//img[@class="item-img"]/@src')
    prod_link = tree.xpath('//a[@class="item-title"]/@href')

    # append collected data from iteration to the main list
    add_to_main_list(title, titles)
    add_to_main_list(store, stores)
    add_to_main_list(price, prices)
    add_to_main_list(review, reviews)
    add_to_main_list(nb_sold, nb_solds)
    add_to_main_list(thumbnail_link, thumbnail_links)
    add_to_main_list(prod_link, prod_links)


products = list(zip(titles, stores, prices, reviews, nb_solds, thumbnail_links, prod_links))
# print(products)

prods = []
di = {}

# transfer data to dict
for el in products:
    di['title'], di['store'], di['price'], di['review'], di['nb_sold'], di['thumbnail_link'], di['prod_link'] = el
    prods.append(di)
    di = {}

# get product specifications
prod_no = 1
prod_total = len(prods)
print('Found {} products'.format(len(prods)))

for prod in prods:
    link = prod['prod_link']
    specs = get_product_specs(browser, link)
    prod['image_link'], prod['specifications'], prod['description'], prod['reviews'] = specs

    print('Scraped {}/{} of products'.format(prod_no, prod_total))
    prod_no += 1

browser.close()

#print(prods)
print('Finished scraping {} products'.format(len(prods)))
with open(output_file, 'w', encoding='utf8') as fout:
    json.dump(prods, fout, ensure_ascii=False)