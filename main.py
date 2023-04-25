from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

nowTime = ''
PASSWORD = os.getenv("PASSWORD")
USERNAME = os.getenv("USERNAME")

def getURL(brand, currentlyPageNumber):
    try:

        if brand == "Loreal":
            url = 'https://www.lookfantastic.com/brands/l-oreal-professionnel/all-l-oreal-professionnel.list?pageNumber={}'.format(currentlyPageNumber)
        elif brand == "Kerastase":
            url = 'https://www.lookfantastic.com/brands/kerastase/all-kerastase.list?pageNumber={}'.format(currentlyPageNumber)
        elif brand == "Ghd":
            url = 'https://www.lookfantastic.com/health-beauty/ghd/view-all-ghd.list?pageNumber={}'.format(currentlyPageNumber)
        elif brand == "Cerave":
            url = 'https://www.lookfantastic.com/brands/cerave/view-all.list?pageNumber={}'.format(currentlyPageNumber)
        elif brand == "Purelogy":
            url = 'https://www.lookfantastic.com/brands/pureology/all-pureology.list?pageNumber={}'.format(currentlyPageNumber)
        elif brand == "Olaplex":
            url = 'https://www.lookfantastic.com/brands/olaplex/view-all.list?pageNumber={}'.format(currentlyPageNumber)
        elif brand == "Kms":
            url = 'https://www.lookfantastic.com/brands/kms/view-all.list?pageNumber={}'.format(currentlyPageNumber)
        elif brand == "Nioxin":
            url = 'https://www.lookfantastic.com/brands/nioxin/view-all.list?pageNumber={}'.format(currentlyPageNumber)
        else:
            with open("./log.txt", "a") as file:
                file.write("Wrong brand name.\n")

        return url

    except:
        print("An error occurred in 'getURL' .")


def getProductFeatures(brand, pageNumber):
    product_prices = []
    # product_RRP_prices = []
    product_names = []
    currentlyPageNumber = 1

    while (currentlyPageNumber < (pageNumber + 1)):
        url = getURL(brand, currentlyPageNumber)
        response = requests.get(url)
        html_content = response.content

        soup = BeautifulSoup(html_content, 'html.parser')

        products = soup.select("ul.productListProducts_products li")

        for product in products:
            product_prices.append(product.find("span", class_="productBlock_priceValue").text)
            product_names.append(product.find("h3", class_="productBlock_productName").text)
            #rrp_price = product.find("span", class_="productBlock_rrpValue")
            #if rrp_price:
            #    product_RRP_prices.append(rrp_price.text)
            #else:
            #    product_RRP_prices.append("--")

        currentlyPageNumber += 1

    # return product_prices, product_RRP_prices, product_names
    return product_prices, product_names


def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def saveData(brand, product_names, product_prices, time):
    global PASSWORD
    global USERNAME
    cluster = MongoClient(f"mongodb+srv://{USERNAME}:"+PASSWORD+"@cluster0.sinfgx1.mongodb.net/test")
    db = cluster["database_web_scraping"]
    collection = db[brand]

    for product_name, product_price in zip(product_names, product_prices):
        try:
            result = collection.update_one({'ProductName': product_name}, {'$set': {time: product_price}})
            if result.modified_count > 0:
                pass
            else:
                with open("./log.txt", "a") as file:
                    file.write(f"{product_name} not founded.\n".format(product_name))
        except Exception as e:
            with open("./log.txt", "a") as file:
                file.write(f"{product_name} update error: {e}")


# def getDataFrame(product_prices, product_RRP_prices, product_names):
#     dataFrame = pd.DataFrame()
#     dataFrame["Product Name"] = product_names
#     # dataFrame["Product RRP Price"] = product_RRP_prices
#     dataFrame["Product Price"] = product_prices
#
#     return dataFrame

def saveTime(nowTime):
    global PASSWORD
    global USERNAME
    cluster = MongoClient(f"mongodb+srv://{USERNAME}:" + PASSWORD + "@cluster0.sinfgx1.mongodb.net/test")
    db = cluster["database_web_scraping"]

    timeCollection = db["Time"]
    myTimeDict = {"recordTime": nowTime}
    timeCollection.insert_one(myTimeDict)

    with open("./log.txt", "a") as file:
        file.write(f"time : {nowTime}\n".format(nowTime))


def main():
    brands = {"Loreal": 3, "Kerastase": 6, "Ghd": 2, "Cerave": 2,
              "Purelogy": 2, "Olaplex": 2, "Kms": 2, "Nioxin": 2}

    global nowTime
    nowTime = get_current_time()
    saveTime(nowTime)

    for brand, pageNumber in brands.items():
        # product_prices, product_RRP_prices, product_names = getProductFeatures(brand, pageNumber)
        product_prices, product_names = getProductFeatures(brand, pageNumber)
        product_names = [name.strip() for name in product_names]
        # dataframe = getDataFrame(product_prices, product_RRP_prices, product_names)
        saveData(brand, product_names, product_prices, nowTime)
        with open("./log.txt", "a") as file:
            file.write(f"{brand} is saved.".format(brand))

main()
