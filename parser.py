import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium
from shutil import which
from scrapy_selenium import SeleniumRequest
from scrapy.selector import Selector
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
        
#from selenium.webdriver.chrome.options import Options                                                                                                                                              
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import re
import psycopg2
from datetime import datetime
import json
import logging
import requests


def scrape_site(SAMPLE_URL):
    #return 0
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument("window-size=1920x1080")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')   
    # options.add_argument('--disable-dev-shm-usage') # Not used but can be an option
    driver = webdriver.Chrome(options=options)

    driver.get(SAMPLE_URL)


    #time.sleep(5)


    #for t in range(10):
    #    driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)

    #for t in range(10):
    #    time.sleep(1)
    #    driver.find_element_by_css_selector('.additional_data').click()

    #src = driver.page_source
    #parser = BeautifulSoup(src, "html.parser")

    result = parse_result(driver,SAMPLE_URL)
    driver.close()

    return result



def load_data(jk,bld,flat_no,square,floor,price,year):
    result = ''
    try:
        headers = {}
        url = "http://api:3000/handle_flat"
        payload = {"jk":jk,"bld":bld,"flat_no":flat_no,"square":square,"floor":floor,"price":price,"year":year}
        s = requests.session()
        s.keep_alive = False
        return requests.request("POST", url, headers=headers, data=payload)

        #connection = psycopg2.connect(user="roman",password="5KNfb^tU9#Zn2ESD",host="db",port="5432",database="postgres")
        #cursor = connection.cursor()
        #cursor.execute("insert into flats  values ('"+jk+"','"+bld+"','"+flat_no+"',"+square+","+floor+","+price+","+str(year)+",'"+str(datetime.now())+"') on CONFLICT(name, building, flat_number)     DO update set price=excluded.price,last_update='"+str(datetime.now())+"';")
        #connection.commit()
    except Exception as error :
        return str(error)
        result +=str(error)+'\n'
        #filename = f'/home/rpolovkov/parklegend/quotes-{page}.html'
        #with open(filename, 'a') as f:
        #    #print ("Error while fetching data from PostgreSQL", error)
        #    f.write("Error while fetching data from PostgreSQL"+ str(error))
    #finally:
        #closing database connection.
        #if (connection):
        #    cursor.close()
        #    connection.close()
    return result
def wait_n_seconds(driver,n):
    try:
        WebDriverWait(driver, n).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "loadMore__100_uH")))
     
    except selenium.common.exceptions.TimeoutException:
        print('1')
def accept_cookies(driver):
    try:           
        cookies = WebDriverWait(driver, 3).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "cookie-message__button")))[0]
        #cookies.find_elements_by_class_name("v3-btn")[0].click()
        cookies.click()
        #ActionChains(driver).move_to_element(driver.find_element(By.CLASS_NAME,"cookie-message__button")).click().perform()
    except selenium.common.exceptions.TimeoutException:

        print('1') 
    except Exception as ex:
        print(ex)
def parse_card(card):
    today = datetime.today()
    url = card.get_attribute("href") 
    lines = card.text.split('\n')
    jk = lines[0]
    bld = lines[2]
    flat_no = f'{lines[3]} {url}'
    square = lines[5].split(' ')[0].replace(',','.')
    floor  = lines[7].split('/')[0]
    price = lines[10].replace(' ','').replace('₽','').replace('от','')
    year = 0                     
    if 'Сдан' in lines[9]:       
        year = today.year        
    else:                        
        year = lines[9].split(' ')[2]                         
    print(f'{jk},{bld},{flat_no},{square},{floor},{price},{year}')
    #result += str(load_data(jk,bld,flat_no,square,floor,price,year))

def get_pages_count(driver):
    pages = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "pagination__page")))
    return pages[len(pages)-1].text

def parse_result(driver, response):

        driver.get(response)
        result = '' 
        #page="temp"
        #filename = f'/home/rpolovkov/parklegend/quotes-{page}.html'
        wait_n_seconds(driver,5)
        accept_cookies(driver)

        n = int(get_pages_count(driver))

        elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "flat-card")))
        for card in elements:
            parse_card(card)

        i = 1
        while i<n:
            i+=1
            response = response.replace(f'page={str(i-1)}',f'page={str(i)}')
            driver.get(response)
            wait_n_seconds(driver,5)
            elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "flat-card")))
            for card in elements:
                parse_card(card)

            

        return ''
        #with open(filename, 'a') as f:
        print(driver.find_element(By.CLASS_NAME,"flat-card").text)
        element = driver
        number = 0
        i=0
        try:
            while 1==1:
                click_more = driver.find_element(By.CLASS_NAME,"flat-list__loadmore")
                click_more.click()
                try:
                    try:
                        i+=1
                        WebDriverWait(driver, 1).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "flat-card__")))
                    except selenium.common.exceptions.TimeoutException:
                        print("Timeout")
                    except selenium.common.exceptions.NoSuchElementException:
                        print("No such element")
                    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "flat-card")))
                except Exception:
                    print("timeout")
        except Exception as ex:
            print(str(ex))
            print ("Fail")
        return ''
        element = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "flat-card")))
        #element = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "flat-card")))
        #self.driver.implicitly_wait(10)
        jk_name=''
        load_data_var=''
        ddict = {}
        try:
            today = datetime.today()
            url = text.get_attribute("href") 
            text=element[0].text
            lines = text.split('\n')
            jk = lines[0]
            print(jk)
            second = lines[1].split(',')
            bld = f'{lines[2]}'
            print(bld)
            flat_no = f'{lines[3]} {url}'
            print(flat_no)
            square = lines[5].split(' ')[0].replace(',','.')
            print(square)
            floor  = lines[7].split('/')[0]
            print(floor)
            i = 3

            price = lines[10].replace(' ','').replace('₽','').replace('от','')
            print(price)
            year = 0
            if 'Сдан' in lines[9]:
                year = today.year
            else:
                year = lines[9].split(' ')[2]
            result += str(load_data(jk,bld,flat_no,square,floor,price,year))
            print(year)
            print (jk)
        except Exception as ex:
            print('firstelement'+str(ex))
        try:
            for text in element[1:]:
                try:
                    txt = text.text.replace("\r","")
                    #f.write(txt)
                    today = datetime.today()
                    url = text.get_attribute("href") 
                    text = text.text
                    lines = text.split('\n')
                    jk = lines[0]
                    print(jk)
                    second = lines[1].split(',')
                    bld = f'{lines[2]}'
                    print(bld)
                    flat_no = f'{lines[3]} {url}'
                    print(flat_no)
                    square = lines[5].split(' ')[0].replace(',','.')
                    print(square)
                    floor  = lines[7].split('/')[0]
                    print(floor)
                    i = 3

                    price = lines[10].replace(' ','').replace('₽','').replace('от','')
                    print(price)
                    year = 0
                    if 'Сдан' in lines[9]:
                        year = today.year
                    else:
                        year = lines[9].split(' ')[2]
                    print(year)
                    load_data_var+=",('"+jk+"','"+bld+"','"+flat_no+"',"+square+","+floor+","+price+",2023,'"+"2022-02-26"+"')"
                    try:
                        print(f'{jk},{bld},{flat_no},{square},{floor},{price},2023')
                        result += str(load_data(jk,bld,flat_no,square,floor,price,'2023'))
                    except Exception as ex:
                        print("exception_dict" +str(ex))

                    #self.load_data(jk,bld,flat_no,square,floor,price,2023)
                except Exception as err:
                    print(f"Unexpected {err=}, {type(err)=}")
        except Exception as ex:
            print(str(ex))
        #return
        print(load_data_var)
        #load_data_var=load_data_var[:-1]
        #self.load_data_batch(ddict)
        print("jk_name: "+jk_name)
        return result

