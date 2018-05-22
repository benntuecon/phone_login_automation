# -*- coding: utf-8 -*-
"""
Created on Sun May 20 15:59:59 2018

@author: CHEN
"""

import os
from selenium import webdriver

def setup_driver(test=True):    
    option=webdriver.ChromeOptions()
    if not test:
        option.set_headless()
    driver = webdriver.Chrome(executable_path=os.getcwd()+"\chromedriver.exe",options=option)    
    return driver




#登入參數     帳號  密碼  操作延遲秒數  測試與否瀏覽器headless   是否操作已經存在的driver   
def login(account, password, delay=0, test=True, driver_to_take_over=None):    
    driver = setup_driver(test) if driver_to_take_over==None else driver_to_take_over
    host="https://max.maicoin.com/signin"
    driver.get(host)
    #輸入帳密
    account_textbox = driver.find_element_by_name("auth_key")
    account_textbox.send_keys(account)
    driver.implicitly_wait(delay)    
    pswd_textbox = driver.find_element_by_name('password')
    pswd_textbox.send_keys(password)
    driver.implicitly_wait(delay)
    commit_btm = driver.find_element_by_name('commit')
    commit_btm.click()    
    #輸入手機驗證
    phone_msg=input("手機驗證碼\n")
    phone_msg_testbox = driver.find_element_by_name("two_factor[otp]")
    phone_msg_testbox.send_keys(phone_msg)
    commit_btm2 = driver.find_elements_by_name("commit")
    commit_btm2[1].click()
    driver.implicitly_wait(delay)
    if driver.current_url=="https://max.maicoin.com/two_factors":
        phone_msg=input("手機驗證碼逾時，重新輸入\n")
        phone_msg_testbox.send_keys(phone_msg)
        driver.implicitly_wait(delay)
    #確認公告
    if len(driver.find_elements_by_id("announcement"))!=0:
        driver.implicitly_wait(delay)
        comfirm_btn=driver.find_element_by_xpath("//*[@id=\"announcement\"]/div/div/div[3]/button")
        comfirm_btn.click()
    driver.implicitly_wait(delay)    #make sure session cookie received
    #確認cookie
    cookies = driver.get_cookies()
    for cookie in cookies:
        if  cookie['name']=="_mlive_session" :
             s = cookies.copy()              
             return s if  test else driver             
    print("somehow session cookie is not saced")
    return 

#s = login("XXXXXXXXXXXXXXX","XXXXXXXXXXXXXXX",delay=0)
#print("test-------{0}:{1}".format(s[1]['name'],s[1]['value']))