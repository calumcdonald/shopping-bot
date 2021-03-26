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

with open("data/products.json") as f:
    products = json.load(f)

CHROMEDRIVER_PATH = "chromedriver.exe"

options = Options()
# uncomment these to run completely from terminal
# options.add_argument("--headless")
# options.add_argument("--disable-extensions")

driver = webdriver.Chrome(CHROMEDRIVER_PATH, options=options)

driver.get(products['phone_case']['url'])

inStock = False
while not inStock:
    try:
        # click off of cookie notice
        driver.find_element_by_xpath("//*[@id='onetrust-accept-btn-handler']").click()
        inStock = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='product-actions']/div[4]/div[1]/button")))
        if inStock:
            print("IN STOCK")
            # add to basket
            inStock.click()
            # print("ADDED TO BASKET")
            # let basket update
            time.sleep(2)
            # straight to checkout
            driver.get("https://www.currys.co.uk/app/checkout")

            # enter post code
            postcode = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='delivery_location']/input")))
            postcode.send_keys(data["postcode"])
            time.sleep(2)
            postcode.send_keys(Keys.ENTER)
            # print("POST CODE ENTERED")
            # click free delivery
            WebDriverWait(driver, 7).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Free')]"))).click()
            # print("DELIVERY SELECTED")
            # enter email
            email = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.NAME, "email")))
            email.send_keys(data["email"])
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Continue')]"))).click()
            # print("EMAIL ENTERED")
            # continue as guest
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Continue as a guest')]"))).click()
            # print("CONTINUING AS GUEST")

            # title
            WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.NAME, "d-title"))).click()
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Mr.')]"))).click()
            # print("TITLE SELECTED")
            # first name
            fname = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.NAME, "fname")))
            fname.send_keys(data["firstname"])
            # print("FIRST NAME ENTERED")
            # surname
            lname = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.NAME, "lname")))
            lname.send_keys(data["surname"])
            # print("SURNAME ENTERED")
            # mobile number
            mobile = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='addresses']/div[2]/div[5]/div/input")))
            mobile.send_keys(data["mobile"])
            # print("MOBILE ENTERED")
            # postcode
            postcode = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.NAME, "zip")))
            postcode.send_keys(Keys.CONTROL + "a")
            postcode.send_keys(data["postcode"])
            # print("POSTCODE ENTERED")
            # address line 1
            address1 = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.NAME, "address")))
            address1.send_keys(data["address1"])
            # print("ADDRESS LINE 1 ENTERED")
            # city
            city = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.NAME, "city")))
            city.send_keys(data["city"])
            # print("CITY ENTERED")
            # submit
            city.send_keys(Keys.ENTER)

            # continue to enter card details
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Card')]"))).click()
            # print("CARD PAYMENT SELECTED")
            # card num
            cardNum = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, "cardNumber")))
            cardNum.send_keys(data["testcardnum"])
            # print("CARD NUMBER ENTERED")
            # cardholder name
            cardName = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.NAME, "cardholderName")))
            cardName.send_keys(data["testcardholdername"])
            # print("CARDHOLDER NAME ENTERED")
            # card exp month
            cardExpMon = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.NAME, "expiryDate.expiryMonth")))
            cardExpMon.send_keys(data["testexpmonth"])
            # print("EXPIRY MONTH ENTERED")
            # card exp year
            cardExpYr = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.NAME, "expiryDate.expiryYear")))
            cardExpYr.send_keys(data["testexpyear"])
            # print("EXPIRY YEAR ENTERED")
            # cvv
            cvc = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.NAME, "securityCode")))
            cvc.send_keys(data["testcvv"])
            # print("CVV ENTERED")

            # SEND THE DOLLA
            WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='submitButton']"))).click()
            print("CHECKING OUT...")
    except:
        if not inStock:
            print("OUT OF STOCK")
            time.sleep(5)
            driver.refresh()
        else:
            print("EXCEPTION")
            inStock = False
            driver.delete_all_cookies()
            driver.get(product['url'])