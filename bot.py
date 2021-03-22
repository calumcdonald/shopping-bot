from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

CHROMEDRIVER_PATH = "chromedriver.exe"

options = Options()
# uncomment these to run completely from terminal
# options.add_argument("--headless")
# options.add_argument("--disable-gpu")
# options.add_argument("--disable-extensions")

driver = webdriver.Chrome(CHROMEDRIVER_PATH, options=options)

# out of stock product
#URL = 'https://www.currys.co.uk/gbuk/computing-accessories/components-upgrades/graphics-cards/msi-geforce-rtx-3060-12-gb-ventus-2x-graphics-card-10221051-pdt.html'
# in stock product
URL = 'https://www.currys.co.uk/gbuk/tv-and-home-entertainment/televisions/televisions/jvc-lt-40ca890-android-tv-40-smart-4k-ultra-hd-hdr-led-tv-with-google-assistant-10199520-pdt.html'
driver.get(URL)

inStock = False
while not inStock:
    try:
        driver.find_element_by_xpath("//*[@id='onetrust-accept-btn-handler']").click()
        inStock = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='product-actions']/div[4]/div[1]/button")))
        if inStock:
            print("IN STOCK")
            # add to basket
            inStock.click()
            # let basket update
            time.sleep(2)
            # straight to checkout
            driver.get("https://www.currys.co.uk/app/checkout")
            # enter post code
            postcode = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='delivery_location']/input")))
            postcode.send_keys("PA2 8RT")
            time.sleep(2)
            postcode.send_keys(Keys.ENTER)
            # click free delivery
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Free')]"))).click()
            # enter email
            email = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//input[contains(text(),'Email address')]")))
            email.send_keys("calumcdonald@gmail.com")
            postcode.send_keys(Keys.ENTER)
            
        
        # old code to go to checkout, might have to reuse this
        # care protection
        #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Continue')]"))).click()
        # go to basket
        #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Continue to basket')]"))).click()
        # checkout
        #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='root']/div/div[2]/div[2]/div/div/div/div[3]/div/div/div[2]/div/button"))).click()        
    except:
        if not inStock:
            print("OUT OF STOCK")
            time.sleep(5)
            driver.refresh()
        else:
            print("EXCEPTION")
        