from selenium import webdriver
from lxml import html
from time import sleep
import json

def add_to_main_list(lst, main):
    for i in lst:
        main.append(i.strip())


browser = webdriver.Firefox()

productsList = []

# category link
myUrl = 'https://www.aliexpress.com/category/708042/cpus.html?spm=a2g0o.home.104.5.650c2145dEszAb'

# list of attributes to help in storing values as tuples
titles = []
stores = []
prices = []
reviews = []
nb_solds = []
img_links = []
store_links = []
shippings = []

for page_nb in range(1, 4):

    browser.get(myUrl + '&page={}'.format(page_nb))
    tree = html.fromstring(browser.page_source)
    browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    sleep(1)

    for product_tree in tree.xpath('//ul[@class="list-items"]'):
        title = product_tree.xpath('.//a[@class="item-title"]/@title')
        store = product_tree.xpath('.//a[@class="store-name"]/text()')
        price = product_tree.xpath('.//span[@class="price-current"]/text()')
        review = product_tree.xpath('.//span[@class="rating-value"]/text()')
        nb_sold = product_tree.xpath('.//a[@class="sale-value-link"]/text()')
        img_link = product_tree.xpath('.//img[@class="item-img"]/@src')

    add_to_main_list(title, titles)
    add_to_main_list(store, stores)
    add_to_main_list(price, prices)
    add_to_main_list(review, reviews)
    add_to_main_list(nb_sold, nb_solds)
    # for images only; append 'https:'
    for i in img_link:
        img_links.append('https:' + i.strip())

    #print(title)
    
    #products = list(zip(title, store, price, review, nb_sold))
    #productsList.append(products)

browser.close()
products = list(zip(titles, stores, prices, reviews, nb_solds, img_links))
#print(products)

prods = []
di = {}
for el in products:
    di['title'], di['store'], di['price'], di['review'], di['nb_sold'], di['img_link']= el
    prods.append(di)
    di = {}

print(prods)
with open('output.json', 'w') as fout:
    json.dump(prods , fout)