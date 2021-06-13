from requests_html import HTMLSession

def checkShopeePrice(url):
    found = False
    while not found:
        try:
            session = HTMLSession()
            r = session.get(url)
            r.html.render()
            price_html = r.html.find('._3e_UQT', first=True)
            price = price_html.text
            found = True
            return price
        except AttributeError:
            pass