from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
import time
import json

with open("data/details.json") as f:
    data = json.load(f)

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
# URL = 'https://www.currys.co.uk/gbuk/tv-and-home-entertainment/televisions/televisions/jvc-lt-40ca890-android-tv-40-smart-4k-ultra-hd-hdr-led-tv-with-google-assistant-10199520-pdt.html'
URL = 'https://www.currys.co.uk/gbuk/phones-broadband-and-sat-nav/mobile-phones-and-accessories/mobile-phone-cases/xqisit-samsung-galaxy-a21s-flex-case-clear-10213971-pdt.html'
driver.get(URL)

inStock = False
while not inStock:
    try:
        driver.find_element_by_xpath("//*[@id='onetrust-accept-btn-handler']").click()
        inStock = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='product-actions']/div[4]/div[1]/button")))
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
            postcode.send_keys(data["postcode"])
            time.sleep(2)
            postcode.send_keys(Keys.ENTER)
            # click free delivery
            WebDriverWait(driver, 6).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Free')]"))).click()
            # enter email
            email = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.NAME, "email")))
            email.send_keys(data["email"])
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Continue')]"))).click()
            # continue as guest
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Continue as a guest')]"))).click()

            # title
            WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.NAME, "d-title"))).click()
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Mr.')]"))).click()
            # first name
            fname = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.NAME, "fname")))
            fname.send_keys(data["firstname"])
            # surname
            lname = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.NAME, "lname")))
            lname.send_keys(data["surname"])
            # mobile number
            mobile = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='addresses']/div[2]/div[5]/div/input")))
            mobile.send_keys(data["mobile"])
            # postcode
            postcode = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.NAME, "zip")))
            postcode.send_keys(Keys.CONTROL + "a")
            postcode.send_keys(data["postcode"])
            # address line 1
            address1 = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.NAME, "address")))
            address1.send_keys(data["address1"])
            # city
            city = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.NAME, "city")))
            city.send_keys(data["city"])
            # submit
            city.send_keys(Keys.ENTER)

            # continue to enter card details
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Card')]"))).click()
            # card num
            cardNum = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, "cardNumber")))
            cardNum.send_keys("5555555555554444")
            # cardholder name
            cardName = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.NAME, "cardholderName")))
            cardName.send_keys("John Doe")
            # card exp month
            cardExpMon = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.NAME, "expiryDate.expiryMonth")))
            cardExpMon.send_keys("12")
            # card exp year
            cardExpYr = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.NAME, "expiryDate.expiryYear")))
            cardExpYr.send_keys("30")
            # CVC
            cvc = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.NAME, "securityCode")))
            cvc.send_keys("123")

            # PAY BB
            WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='submitButton']"))).click()
    except:
        if not inStock:
            print("OUT OF STOCK")
            time.sleep(5)
            driver.refresh()
        else:
            print("EXCEPTION")
        