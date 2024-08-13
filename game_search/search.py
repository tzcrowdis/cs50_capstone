'''
Each search function needs to get and return these in a json format:
Title
Price
Description
Image
'''
import time
import requests
from bs4 import BeautifulSoup

# webdriver to handle scraping dynamic webpages
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import unicodedata

from re import sub
from decimal import Decimal


def game_search(name):

    # search individual game retailers
    steam_result = steam_search(name)
    abandonware_result = abandonware_search(name)
    gog_result = gog_search(name)

    # abandonware is more likely to get bad results so force to end
    result_list = [steam_result, gog_result]
    
    # sort ascending by price with bubble sort
    n = len(result_list)
    for i in range(n):
        already_sorted = True

        for j in range(n - i - 1):
            # if price doesnt exist then call it free
            try:
                current = list(result_list[j].values())[0]['price']
            except:
                current = "free"
    
            try:
                next = list(result_list[j + 1].values())[0]['price']
            except:
                next = "free"

            # if both contain free do nothing
            if "free" in current.lower():
                break
            
            # if next is free then swap
            if "free" in next.lower():
                result_list[j], result_list[j + 1] = result_list[j + 1], result_list[j]
                already_sorted = False
            else:
                # neither free so convert from $ to decimal
                current = Decimal(sub(r'[^\d.]', '', current))
                next = Decimal(sub(r'[^\d.]', '', next))

                # swap if out of order
                if current > next:
                    result_list[j], result_list[j + 1] = result_list[j + 1], result_list[j]
                    already_sorted = False

        if already_sorted:
            break
    
    #forcing to end of list
    result_list.append(abandonware_result)

    # convert from list of dictionaries to one dictionary
    results = {}
    for result in result_list:
        results[list(result.keys())[0]] = list(result.values())[0]
    
    return results

def steam_search(name):
    
    try:
        # get the search page
        search_page = requests.get("https://store.steampowered.com/search/?term=" + name + "&category1=998&ndl=1")
        soup = BeautifulSoup(search_page.content, "html.parser")

        # go to link from top result
        top_result = soup.select("#search_resultsRows > a:nth-child(1)")
        page_link = top_result[0]['href']

        # get details from game page
        game_page = requests.get(page_link)
        soup = BeautifulSoup(game_page.content, "html.parser")

        title = soup.find("div", class_="apphub_AppName").get_text()

        #handle discount price
        try:
            price = soup.find("div", class_="game_purchase_price price").get_text()
        except:
            price = soup.find("div", class_="discount_final_price").get_text()

        description = soup.find("div", class_="game_description_snippet").get_text()
        image = soup.find("img", class_="game_header_image_full")['src']
        link = page_link

        # remove all control characters
        title = remove_control_characters(title)
        price = remove_control_characters(price)
        description = remove_control_characters(description)

        '''
        # test variables
        title = "Test"
        price = "$45.00"
        description = "testing\ntesting\ntesting testing testing testing testing testing testing\ntesting\ntesting testing testing testing testing testing testing\ntesting\ntesting testing testing testing testing testing testing\ntesting\ntesting testing testing testing testing testing testing\ntesting\ntesting testing testing testing testing testing testing\ntesting\ntesting testing testing testing testing testing testing\ntesting\ntesting testing testing testing testing testing testing\ntesting\ntesting testing testing testing testing testing"
        image = "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/275850/header_alt_assets_24.jpg"
        link = "https://www.google.com/"
        '''

        return { "steam" :{
            "title": title,
            "price": price,
            "description": description,
            "image": image,
            "link": link
        }}
    except Exception as e:
        print("Error while accessing Steam:")
        print(e)
        return {"error": e}


def abandonware_search(name):
    
    try:
        # get the search page
        search_page = requests.get("https://www.myabandonware.com/search/q/" + name)
        soup = BeautifulSoup(search_page.content, "html.parser")

        # go to link from top result
        top_result = soup.find("a", class_="name c-item-game__name")
        page_link = "https://www.myabandonware.com" + top_result['href']

        # get details from game page
        game_page = requests.get(page_link)
        soup = BeautifulSoup(game_page.content, "html.parser")

        try:
            title = soup.select("#content > div:nth-child(2) > h2")[0].get_text()
        except:
            title = soup.select("#gaff > div:nth-child(1) > h2")[0].get_text()
        
        image = "https://www.myabandonware.com" + soup.select("#screentabs > div > a:nth-child(1) > picture > img")[0]['src']
        link = page_link

        try:
            # standard single paragraph desc.
            description = soup.select("#content > div:nth-child(5) > p")[0].get_text()
        except:
            try:
                # gaff for some reason
                description = soup.select("#gaff > div:nth-child(4) > div")[0].get_text()
            except:
                # multi paragraph desc.
                description = soup.select("#content > div:nth-child(5) > div")[0].get_text()

        # remove all control characters
        title = remove_control_characters(title)
        description = remove_control_characters(description)

        '''# test variables
        title = "Test"
        description = "testing"
        image = "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/275850/header_alt_assets_24.jpg"
        link = "https://www.google.com/"'''

        return { "abandonware": {
            "title": title,
            "description": description,
            "image": image,
            "link": link
        }}
    except Exception as e:
        print("Error while accessing MyAbandonware:")
        print(e)
        return {"error": e}
    

def gog_search(name):
    
    try:
        # options to avoid cumbersome logging and hide browser popup
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument('log-level=3')
        driver = webdriver.Chrome(options=options)

        # get the search page
        driver.get("https://www.gog.com/en/games?query=" + name)

        # wait for results to load
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#Catalog > div > div.catalog__display-wrapper.catalog__grid-wrapper > filter-clearing-list > div > div > filter-clearing-item > div")))
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # go to link from top result
        top_result = soup.select("#Catalog > div > div.catalog__display-wrapper.catalog__grid-wrapper > paginated-products-grid > div > product-tile > a")
        page_link = top_result[0]['href']

        # get details from game page
        driver.get(page_link)
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, "html.parser")

        title = soup.find("h1", class_="productcard-basics__title").get_text()
        price = soup.find("span", class_="product-actions-price__final-amount _price ng-binding").get_text()
        description = soup.find("div", class_="description").get_text()
        image = soup.select("head > meta:nth-child(6)")[0]['content']
        link = page_link

        # remove all control characters
        title = remove_control_characters(title)
        price = remove_control_characters(price)
        description = remove_control_characters(description)

        driver.close()

        '''# test variables
        title = "Test"
        price = "$25.00"
        description = "testing"
        image = "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/275850/header_alt_assets_24.jpg"
        link = "https://www.google.com/"'''

        return { "gog": {
            "title": title,
            "price": price,
            "description": description,
            "image": image,
            "link": link
        }}
    except Exception as e:
        '''driver.close()'''

        print("Error while accessing GOG:")
        print(e)
        return {"error": e}
    

# removes characters like \t and \n to avoid unwanted formatting
def remove_control_characters(s):
    return "".join(ch for ch in s if unicodedata.category(ch)[0]!="C")