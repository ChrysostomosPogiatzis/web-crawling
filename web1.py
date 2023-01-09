from bs4 import BeautifulSoup
import requests
import json
import time

#product_data
product_tag='div'
class_of_product='sg-col sg-col-4-of-12 sg-col-8-of-16 sg-col-12-of-20 s-list-col-right'

#title_data
title_tag='span'
class_of_tile='a-size-medium a-color-base a-text-normal'


def amazon_link(URL):
    #with out HEADERS we cant access amazon content
    HEADERS = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})
    page = requests.get( URL, headers=HEADERS )

    #get amazon page content
    soup = BeautifulSoup( page.content , 'html.parser')
    #find in the amazon page content the product_tag ('div') and the class_of_product('sg-col sg-col-4-of-12 sg-col-8-of-16 sg-col-12-of-20 s-list-col-right')
    products = soup.find_all(product_tag, class_=class_of_product)

    #soup.find_all make an array of products so we have to access each one indivitualy to get the tile by looping thou the products
    for product in products:
        print("-------------- start of product")
        print(product)
        #get product  content and search for the title_tag(span) and the class_of_tile(a-size-medium a-color-base a-text-normal)
        name = product.find(title_tag, class_=class_of_tile)
        print("-------------- product name")
        #.text get the text from the span tag
        print(name.text)

        print("-------------- end of product")


URL='https://www.amazon.com/s?k=projector&crid=3UDLKNC2MZDWM&sprefix=projecto%2Caps%2C291&ref=nb_sb_noss_2'
amazon_link(URL)
