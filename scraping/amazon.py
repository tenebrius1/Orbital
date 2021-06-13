from requests_html import HTMLSession, AsyncHTMLSession

def checkAmazonPrice(url):
    session = HTMLSession()
    r = session.get(url)
    price = r.html.find('#priceblock_ourprice', first=True)
    return price.text