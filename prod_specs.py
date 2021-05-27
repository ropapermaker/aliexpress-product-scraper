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

    browser.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)

    time.sleep(1)

    tree = html.fromstring(browser.page_source)

    # product image
    img_link = tree.xpath('//img[@class="magnifier-image"]/@src')

    # get description of product
    p = tree.xpath('//div[@class="product-description"]//*[self::p or self::span]/text()')

    # add all paragraphs to a single string
    paragraph = ''
    for par in p:
        paragraph += ' ' + par


    # ########################################################################
    # # reviews
    # rev = browser.find_elements_by_xpath('//span[text()="CUSTOMER REVIEWS"]')

    # # click customer reviews div element
    # for r in rev:
    #     try:
    #         r.click()
    #     except:
    #         continue
    
    # # reviews dont get shown in page_source
    # # tree = html.fromstring(browser.page_source)
    # # with open("review_output.txt", "w") as revie:
    # #     textRev = browser.page_source
    # #     revie.write(textRev)

    # customer_names = []
    # ratings = []
    # reviews = []

    # # returns nothing?
    # customer_name = tree.xpath('//a[@name="member_detail"]/text()')
    # rating = tree.xpath('//span[@class="star-view"]//span/@style')
    # review = tree.xpath('//dt[@class="buyer-feedback"]//span/text()')

    # add_to_main_list(customer_name, customer_names)
    # add_to_main_list(rating, ratings)
    # add_to_main_list(review, reviews)

    # print(customer_name)
    # print(rating)
    # print(review)
    
    

    # for el in ratings:
    #     if el == 'width:100%':
    #         el = '5'
    #     elif el == 'width:80%':
    #         el = '4'
    #     elif el == 'width:60%':
    #         el = '3'
    #     elif el == 'width:40%':
    #         el = '2'
    #     elif el == 'width:20%':
    #         el = '1'
        
    # customer_reviews = list(zip(customer_names, ratings, reviews))

    ########################################################################
    # fake reviews
    review1 = {'customer_name':'John Doe1', 'rating':4.5, 'review':'Good Product!'}
    review2 = {'customer_name':'John Doe2', 'rating':4.6, 'review':'Good Product!'}
    review3 = {'customer_name':'John Doe3', 'rating':4.3, 'review':'Good Product!'}
    review4 = {'customer_name':'John Doe4', 'rating':4.1, 'review':'Good Product!'}
    review5 = {'customer_name':'John Doe5', 'rating':4.8, 'review':'Good Product!'}
    review6 = {'customer_name':'John Doe6', 'rating':4.5, 'review':'Good Product!'}
    review7 = {'customer_name':'John Doe7', 'rating':4.6, 'review':'Good Product!'}
    review8 = {'customer_name':'John Doe8', 'rating':4.3, 'review':'Good Product!'}
    review9 = {'customer_name':'John Doe9', 'rating':4.1, 'review':'Good Product!'}
    review10 = {'customer_name':'John Doe10', 'rating':4.8, 'review':'Good Product!'}
    reviews = [review1, review2, review3, review4, review5, review6, review7, review8, review9, review10]
    # print(reviews)


    ########################################################################
    # specifications

    spec = browser.find_elements_by_xpath('//span[text()="SPECIFICATIONS"]')

    # click specifications div element
    for s in spec:
        try:
            s.click()
        except:
            continue

    tree = html.fromstring(browser.page_source)

    titles = []
    descs = []

    for branch in tree.xpath('//li[@class="product-prop line-limit-length"]'):
        title = branch.xpath('//span[@class="property-title"]/text()')
        desc = branch.xpath('//span[@class="property-desc line-limit-length"]/text()')

    add_to_main_list(title, titles)
    add_to_main_list(desc, descs)

    specifications = list(zip(titles, descs))

    prods = []
    di = {}

    # transfer data to dict
    # Brand Name : AMD
    for el in specifications:
        di[el[0]] = el[1]

    return img_link[0], di, paragraph, reviews


if __name__=='__main__':

    myUrl = 'https://www.aliexpress.com/item/1005002034735478.html?algo_pvid=null&algo_expid=null&btsid=0bb0624316208156933138158e193b&ws_ab_test=searchweb0_0,searchweb201602_,searchweb201603_'
    
    browser = webdriver.Firefox()

    link, di, description, reviews = get_product_specs(browser, myUrl)

    print(di)
    print(link)
    print(description)
    print(reviews)