from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def checkLazadaPrice(url):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    timeout = 1

    try:
        WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'span[class=" pdp-price pdp-price_type_normal pdp-price_color_orange pdp-price_size_xl"]')))
        price = driver.find_element(
            By.CSS_SELECTOR, 'span[class=" pdp-price pdp-price_type_normal pdp-price_color_orange pdp-price_size_xl"]')
        return price.text
    except TimeoutException:
        pass
    finally:
        driver.quit()
