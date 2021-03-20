from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

CHROMEDRIVER_PATH = "chromedriver.exe"

options = Options()
#uncomment these to run completely from terminal
#options.add_argument("--headless")
#options.add_argument("--disable-gpu")
#options.add_argument("--disable-extensions")

driver = webdriver.Chrome(CHROMEDRIVER_PATH, chrome_options=options)

#out of stock product
#driver.get('https://www.currys.co.uk/gbuk/computing-accessories/components-upgrades/graphics-cards/msi-geforce-rtx-3060-12-gb-ventus-2x-graphics-card-10221051-pdt.html')
#in stock product
driver.get('https://www.currys.co.uk/gbuk/tv-and-home-entertainment/televisions/televisions/jvc-lt-40ca890-android-tv-40-smart-4k-ultra-hd-hdr-led-tv-with-google-assistant-10199520-pdt.html')

found = False
while not found:
    try:
        add_to_basket = driver.find_elements_by_xpath("//*[@id='product-actions-touch']/div[4]/div[1]/button")[0]
        print("IN STOCK")
        found = True
        driver.quit()
    except:
        print("OUT OF STOCK")
        time.sleep(5)
        driver.refresh()