from requests_html import HTMLSession, AsyncHTMLSession


def checkAmazonPrice(url):
    found = False
    while not found:
        try:
            session = HTMLSession()
            r = session.get(url)
            price_html = r.html.find('#priceblock_ourprice', first=True)
            price = price_html.text
            found = True
            return price
        except AttributeError:
            pass
