from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
import time
from datetime import datetime
import json

with open("data/details.json") as f:
    data = json.load(f)

with open("data/products.json") as f:
    products = json.load(f)

product = products['MSI_RTX3060_VENTUS_2X_OC']

CHROMEDRIVER_PATH = "chromedriver.exe"

options = Options()
# uncomment these to run completely from terminal
options.add_argument("--headless")
options.add_argument("--disable-extensions")

driver = webdriver.Chrome(CHROMEDRIVER_PATH, options=options)
driver.get(product['url'])

def print_to_log(content):
    print(content)
    f = open("stock_log.txt", "a")
    f.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ': ' + content + '\n')
    f.close()

def refresh():
    driver.delete_all_cookies()
    driver.get(product['url'])

checked_out = False
def try_to_checkout():
    try:
        # straight to checkout
        driver.get("https://www.currys.co.uk/app/checkout")
        # enter post code
        try:
            postcode = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='delivery_location']/input")))
            postcode.send_keys(data["postcode"])
            time.sleep(2)
            postcode.send_keys(Keys.ENTER)
        except:
            pass
        # click free delivery
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//button[contains(text(),'Free')]"))).click()
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
        cardNum.send_keys(data["cardnum"])
        # cardholder name
        cardName = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.NAME, "cardholderName")))
        cardName.send_keys(data["cardholdername"])
        # card exp month
        cardExpMon = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.NAME, "expiryDate.expiryMonth")))
        cardExpMon.send_keys(data["cardexpmonth"])
        # card exp year
        cardExpYr = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.NAME, "expiryDate.expiryYear")))
        cardExpYr.send_keys(data["cardexpyear"])
        # cvv
        cvv = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.NAME, "securityCode")))
        cvv.send_keys(data["cvv"])

        # SEND THE DOLLA
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='submitButton']"))).click()
        print_to_log('CHECKING OUT...')
        
        try:
            WebDriverWait(driver, 45).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(),'Card')]")))
            print_to_log('COULD NOT CHECKOUT')
            refresh()
        except:
            checked_out = True
    except:
        print_to_log('EXCEPTION')
        refresh()

while not checked_out:
    try:
        # click off of cookie notice
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='onetrust-accept-btn-handler']"))).click()
        price = driver.find_element_by_xpath("//*[@id='product-actions']/div[2]/div/div/span").text
        # if price is what Currys says
        #price[1:len(price)] == product['price']
        # if price is below 450
        price = float(price[1:len(price)])
        if(price <= 450):
            add_to_basket = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='product-actions']/div[4]/div[1]/button")))
            # code won't get past here if it's out of stock
            print_to_log('IN STOCK')
            add_to_basket.click()
            # let basket update
            time.sleep(2)
            
            try_to_checkout()
        else:
            print_to_log('INCORRECT PRICE ' + '(' + str(price) + ')')
            time.sleep(5)
            refresh()
    except:
        print("OUT OF STOCK")
        time.sleep(1)
        refresh()

print_to_log('BINGO.')
driver.quit()