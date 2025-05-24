#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: rishi
"""

from kiteconnect import KiteConnect
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import os
from pyotp import TOTP
import logging


def autologin(keyFile):
    token_file = keyFile
    print(token_file)
    key_secret = open(token_file, 'r').read().split()
    print(key_secret[0])
    print(key_secret[4])
    kite = KiteConnect(api_key=key_secret[0])
    service = webdriver.chrome.service.Service('./chromedriver_linux64/chromedriver')
    service.start()
    options = Options()
    #options.add_argument("--headless")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")

    driver = webdriver.Remote(service.service_url, options=options)
    driver.get(kite.login_url())
    time.sleep(1)
    username = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div/div/div[2]/form/div[1]/input')
    password = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div/div/div[2]/form/div[2]/input')
    username.send_keys(key_secret[2])
    password.send_keys(key_secret[3])
    driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div/div/div[2]/form/div[4]/button').click()
    time.sleep(1)
    totp = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div/div/div[2]/form/div[1]/input')
    print(key_secret[4])
    totp_token = TOTP(key_secret[4])
    token = totp_token.now()
    print(token)
    totp.send_keys(token)
    driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div/div/div[2]/form/div[2]/button').click()
    time.sleep(1)
    print(driver.current_url)
    request_token=driver.current_url.split('request_token=')[1][:32]
    print(request_token)
    with open('request_token.txt', 'w') as f :
        f.write(request_token)
    driver.quit()    

    request_token = open("request_token.txt", 'r').read()
    key_secret = open(keyFile, 'r').read().split()
    kite = KiteConnect(key_secret[0])
    data = kite.generate_session(request_token, key_secret[1])
    with open('access_token.txt', 'w') as file :
        file.write(data['access_token'])
        
    kite.set_access_token(data['access_token'])
    return kite