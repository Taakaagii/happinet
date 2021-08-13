from types import SimpleNamespace
from common import XpathGetter
from common import getTimer
import chromedriver_binary
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import tweepy
# import random
import datetime
from selenium.webdriver.support.ui import Select
# from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from concurrent import futures


landingUrl = 'https://www.happinetonline.com/ec/cmShopTopPage1.html'

searchUrl = {
    '蒼空ストリーム':'https://www.happinetonline.com/ec/pro/disp/1/10874990?sFlg=2'
    #,'I':'https://www.happinetonline.com/ec/pro/disp/1/10875289?sFlg=0'
    ,'フュージョンアーツ':'https://www.happinetonline.com/ec/pro/disp/1/10878887?sFlg=2'
    ,'25THアニバーサリー':'https://www.happinetonline.com/ec/pro/disp/1/10878890?sFlg=2'
    # ,'V':'https://www.happinetonline.com/ec/pro/disp/1/10875289?sFlg=0'
    ,'PS5　ディスクエディション':'https://www.happinetonline.com/ec/pro/disp/1/10856443?sFlg=2'
    ,'PS5　デジタルエディション':'https://www.happinetonline.com/ec/pro/disp/1/10856444?sFlg=2'
    #,'テスト用':'https://www.happinetonline.com/ec/pro/disp/1/10875289?sFlg=0'
    }

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    ,'Accept-Encoding': 'gzip, deflate, br'
    ,'Accept-Language': 'ja,en-US;q=0.9,en;q=0.8'
    ,'Cache-Control': 'max-age=0'
    ,'Connection': 'keep-alive'
    ,'Cookie': 'JSESSIONID=982501E29279EF857325B40E65990196; subShopId=1; cartId=mnP0MY9Pp4tV4XndIWOg4k8YzEfQhA0U; LASTPRODUCTCOOKIEID=34022895812463413242942478881673344894486854505130103481623454190417166573846345495006699818671460825226110670510537575822716266; TIMEOUT_KEY_COOKIE=TIMEOUT_KEY_COOKIE; SKEY=6f2GtRa2Q8fugAAPYIX6eN9UM3uSWK1X'
    ,'Host': 'www.happinetonline.com'
    ,'Referer': 'https://www.happinetonline.com/ec/Facet?inputKeywordFacet=%E8%92%BC%E7%A9%BA%E3%82%B9%E3%83%88%E3%83%AA%E3%83%BC%E3%83%A0&kclsf=AND'
    ,'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"'
    ,'sec-ch-ua-mobile': '?0'
    ,'Sec-Fetch-Dest': 'empty'
    ,'Sec-Fetch-Mode': 'cors'
    ,'Sec-Fetch-Site': 'none'
    # ,'Sec-Fetch-User': '?1'
    # ,'Upgrade-Insecure-Requests': '1'
    ,'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
    }

getter = XpathGetter()
getTimer = getTimer()

class seleniumOpe:

    def __init__(self):
        # Selenium生成
        options = Options()
        options.add_argument('--no-sandbox')

        # 最終的にheadless
        # options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--lang=ja-JP')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-application-cache')
        options.add_argument("start-maximized")
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36') 
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option( "prefs",{'profile.managed_default_content_settings.javascript': 2})
        
        chrome_prefs = {}
        options.experimental_options["prefs"] = chrome_prefs
        chrome_prefs['chrome.page.customHeaders.referrer'] = 'https://order.yodobashi.com/yc/login/order/index.html?lg=1'  
        
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(landingUrl)
        self.wait = WebDriverWait(self.driver, 5); 

    def search(self):

        while True:
            # rt = requests.get(searchUrl['S'], headers=headers)
            #rt = requests.get(searchUrl['T'], headers=headers)
            #print(rt.content)  
            #xpath1 = getter.find_by_xpath(rt.content, '//*[@id="cartOn"]')

            for key, value in searchUrl.items():
                self.driver.get(value)
                rt = self.driver.find_elements_by_xpath('//*[@id="cartOn"]')
            # , attrs={'style':'display:block'}

            #if xpath1[0].attrib['style'] != 'display:none':
                if rt[0].get_attribute('style') != 'display: none;':
                    self.selectQty()
                    self.addCart()
                    self.popupAddCart()
                    self.preChkOut()
                    self.login()
                    self.checkOut()
                    self.quit()
                    exit()
                
                print('{0}が監視しました。在庫なしです。'.format(key))

            print('再検索かけます。')
            time.sleep(10)

    def addCart(self):
        addCart = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="cartButtonOn"]')))
        addCart.click()

    def popupAddCart(self):
        popAddCart = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="review"]/div/a[2]')))
        popAddCart.click()


    def selectQty(self):
        select = Select(self.driver.find_element_by_xpath('//*[@id="cartbox_right"]/div[2]/div[1]/select'))
        select.select_by_index(len(select.options)-1)
    
    def preChkOut(self):
        preChk = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="cart"]/form/section/div[2]/a[2]')))
        preChk.click()

    def login(self):
        ID = self.driver.find_element_by_xpath('//*[@id="userId"]')
        PASS = self.driver.find_element_by_xpath('//*[@id="password"]')

        ID.click()
        ID.send_keys('！！')
        PASS.click()
        PASS.send_keys('！！')
        loginBtn = self.driver.find_element_by_xpath('//*[@id="login"]/section[1]/div/button')
        time.sleep(3)
        loginBtn.click()

    def checkOut(self):
        chkBtn = self.driver.find_element_by_xpath('//*[@id="orderButton"]')
        chkBtn.click()

    def quit(self):
        self.driver.quit()

driver = seleniumOpe()
driver.search()

