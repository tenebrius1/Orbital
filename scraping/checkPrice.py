from scraping.amazon import checkAmazonPrice
from scraping.lazada import checkLazadaPrice
from scraping.shopee import checkShopeePrice


def checkPrice(url):
    if "lazada" in url:
        price = float("{:.2f}".format(float(checkLazadaPrice(url)[1:])))
    elif "shopee" in url:
        price = float("{:.2f}".format(float(checkShopeePrice(url)[1:])))
    elif "amazon" in url:
        price = float("{:.2f}".format(float(checkAmazonPrice(url)[2:])))
    else:
        pass

    return price
