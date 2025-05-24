#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  5 14:35:44 2021

@author: rishi
"""

from kiteconnect import KiteConnect
from selenium import webdriver
import pandas as pd
import time

def autologin():
    token_file = "key.txt"
    key_secret = open(token_file, 'r').read().split()
    kite = KiteConnect(api_key=key_secret[0])
    service = webdriver.chrome.service.Service('./chromedriver')
    service.start()
    options = webdriver.ChromeOptions()
    