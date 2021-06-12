from environs import Env
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Set up environ
env = Env()
env.read_env()

def checkShopeePrice(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-software-rasterizer')
    options.add_argument('--log-level=2')
    options.binary_location = env.str('GOOGLE_CHROME_BIN')
    driver = webdriver.Chrome(executable_path=env.str('CHROMEDRIVER_PATH'),options=options)
    driver.get(url)
    timeout = 1

    try:
        found = False
        price = None
        while not found:
            try:
                WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, 'div[class="_3e_UQT"]')))
            except TimeoutException:
                driver.refresh()
                continue
            price = driver.find_element(
                By.CSS_SELECTOR, 'div[class="_3e_UQT"]')
            found = True
        return price.text
    except TimeoutException:
        pass
    finally:
        driver.quit()
