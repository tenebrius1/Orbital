from requests_html import HTMLSession


def checkLazadaPrice(url):
    found = False
    while not found:
        try:
            session = HTMLSession()
            r = session.get(url)
            price_html = r.html.find(
                'span.pdp-price.pdp-price_type_normal.pdp-price_color_orange.pdp-price_size_xl', first=True)
            price = price_html.text
            found = True
            return price
        except AttributeError:
            pass
