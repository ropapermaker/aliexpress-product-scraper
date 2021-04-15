from selenium import webdriver
from selenium.webdriver.common.by import By
from lxml import html
import time
import json
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def add_to_main_list(lst, main):
    for i in lst:
        if i[0] == '/':
            main.append('https:' + i.strip())

        else: main.append(i.strip())

def get_product_specs(driver, url):

    browser = driver

    browser.get(url)

    spec = browser.find_elements_by_xpath('//span[text()="SPECIFICATIONS"]')

    # print(len(spec))

    # click specifications div element
    for s in spec:
        try:
            s.click()
        except:
            continue

    tree = html.fromstring(browser.page_source)

    titles = []
    descs = []

    for branch in  tree.xpath('//li[@class="product-prop line-limit-length"]'):
        title = branch.xpath('//span[@class="property-title"]/text()')
        desc = branch.xpath('//span[@class="property-desc line-limit-length"]/text()')

    add_to_main_list(title, titles)
    add_to_main_list(desc, descs)

    specifications = list(zip(titles, descs))
    # print(specifications)

    prods = []
    di = {}

    # transfer data to dict
    # Brand Name : AMD
    for el in specifications:
        di[el[0]] = el[1]

    return di


if __name__=='__main__':

    myUrl = 'https://www.aliexpress.com/item/1005001709341330.html?spm=a2g0o.productlist.0.0.5ef55825Ma9twS&algo_pvid=null&algo_expid=null&btsid=0bb0623316184917743688436e095d&ws_ab_test=searchweb0_0,searchweb201602_,searchweb201603_'
    
    browser = webdriver.Firefox()

    di = get_product_specs(browser, myUrl)

    print(di)
