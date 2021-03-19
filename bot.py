from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
CHROMEDRIVER_PATH = "chromedriver.exe"

options = Options()
options.headless = False
driver = webdriver.Chrome(CHROMEDRIVER_PATH, chrome_options=options)

driver.get('https://www.currys.co.uk/gbuk/computing-accessories/components-upgrades/graphics-cards/msi-geforce-rtx-3060-12-gb-ventus-2x-graphics-card-10221051-pdt.html')
#driver.get('https://www.currys.co.uk/gbuk/tv-and-home-entertainment/televisions/televisions/jvc-lt-40ca890-android-tv-40-smart-4k-ultra-hd-hdr-led-tv-with-google-assistant-10199520-pdt.html')

found = False
while not found:
    driver.refresh()
    stock = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "Button__StyledButton-iESSlv dJJJCD Button-dtUzzq kHUYTy")))
else:
    found = True
    driver.quit()

print("test")