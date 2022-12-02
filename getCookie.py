from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import pickle

PATH = "chromedriver.exe"
options = webdriver.ChromeOptions()
options.headless = False
driver = webdriver.Chrome(executable_path=PATH, options=options)
dirPath = ""
tiktokCookiePath = "tiktokCookie.txt"
instagramCookiePath = "instagramCookie.txt"
facebookCookiePath = "facebookCookie.txt"

def getCookieTiktok():
    driver.get("https://www.tiktok.com/")
    # login = driver.find_element_by_xpath("//button[@data-e2e='top-login-button']")
    # login.click()
    # time.sleep(2)
    # qr = driver.find_element_by_xpath("//a[@href='/login/qrcode']")
    # qr.click()
    time.sleep(60)
    save_cookie(driver,tiktokCookiePath)
    print("COokie saved")
    driver.implicitly_wait(2)

def save_cookie(driver, path):
    with open(path, 'wb') as filehandler:
        pickle.dump(driver.get_cookies(), filehandler)

def getCookieInstagram():
    driver.get("https://www.instagram.com/")
    time.sleep(60)
    save_cookie(driver,instagramCookiePath)
    print("COokie saved")
    driver.implicitly_wait(2)

def getCookieFacebook():
    driver.get("https://www.facebook.com/")
    time.sleep(60)
    save_cookie(driver,facebookCookiePath)
    print("COokie saved")
    driver.implicitly_wait(2)

getCookieInstagram()
# getCookieTiktok()
# getCookieFacebook()