#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: rishi
"""
import os



path = os.path.dirname(os.path.abspath(__file__))
cwd = os.chdir(path)
from zerodha_login import *
from access import *
from trade_runner import TradeRunner

from utility import *
import logging 
import pandas as pd
import datetime







FORMAT = '%(asctime)s:%(levelname)s:%(message)s'
placeProtectionTime = datetime.time(9, 20, 00)
buyHedgeTime = datetime.time(15, 15, 00)


def placeProtection(mt) :    
    positions = mt.all_position_book()
    orderPlacementStatus = True
    print("Current positions : ")
    i = 1
    for position in positions['data']:
        print("Position ", i , " Instrument : ", position['trading_symbol'],"Token :",  position['instrument_token'], "LTP : ", position['ltp'])
        base = 0.5
        slPrice = round(base * round((round(position['ltp'] * 2, 1)/base)), 1)
        i = i + 1
        print ("Placing SL Limit order at 50 % of ltp at " , slPrice, "for ", position['trading_symbol'], "qty : ", position['cf_sell_quantity']) 
        
        orderStatus = mt.place_order(position['exchange'], position['instrument_token'], "BUY", "SL", "NRML", round(slPrice*1.1), position['cf_sell_quantity'], 0, round(slPrice), 0, "DAY", 0)
        print (position['exchange'], position['instrument_token'], position['trading_symbol'], mt.order_history( orderStatus['data']['oms_order_id'])['data'][0]['status'])
        if mt.order_history( orderStatus['data']['oms_order_id'])['data'][0]['status'] == 'rejected' :
           orderPlacementStatus = False 
        if i == 9 :
            break
    
    return orderPlacementStatus


def buyNiftyHedge(kite, mt) :
    day  = datetime.date.today()
    instrument = "NSE:NIFTY 50"
    instrumentLTP = kite.ltp(instrument)
    print("Current nifty spot price on", datetime.datetime.now() , "is :" , instrumentLTP[instrument]['last_price'])
    #fetch the 1000 poit down weekly contract
    optionToBuy = getNiftyWeeklyOptionToBuy(day, int(instrumentLTP[instrument]['last_price']))
    print("Hedge to buy ", optionToBuy)
    ltp = kite.ltp("NFO:" + optionToBuy)["NFO:" + optionToBuy]["last_price"]
    print ("Hedge LTP is ", ltp)
    print("Placing Order ")
    mtToken = mt.search_script(optionToBuy)['result'][0]['token']
    order_Status = mt.place_order("NFO", mtToken, "BUY", "MARKET", "MIS", 0, 75, 0, 0, 0, "DAY", 0)
    


def start() :
    print(path)
    kite = None
    kite = autologin("key.txt")
    if None == kite :
        print("Failed to log in to zerodha")
        logging.info("Failed to log in to zerodha") 
        #return
    
    print("Logged in to zerodha")
    logging.info("Logged in to zerodha")

    URL = 'https://masterswift-beta.mastertrust.co.in'
    # Initialise Access
    access = Access()

    # Initialise trade-runner
    mt = None
    mt = TradeRunner(access, URL)
    if None == mt :
        print("Failed to log in to Mastertrust")
        logging.info("Failed to log in to Mastertrust") 
        #return
    access = mt.header_s(access) 
    print("Logged in to MasterTrust")
    logging.info("Logged in to MasterTrust")
    
    rc = False
    hedgeBuy = False
    
    """
    while(True) :
        
        if (datetime.datetime.now().time() > placeProtectionTime) and rc == False :
            #TODO : Add failure handling
            placeProtection(mt)
            rc = True
        
        if (datetime.datetime.now().time() > buyHedgeTime) and hedgeBuy == False :
            #TODO : Add failure handling
            buyNiftyHedge(kite, mt)
            hedgeBuy = True

"""

if __name__=="__main__":
    try :
        logging.basicConfig(filename="LOG"+str(datetime.datetime.today())+".txt", format=FORMAT, level=logging.INFO)
        logging.info("============Start============")
        start()
        
    except KeyboardInterrupt:
        print ("INTERUPPT")
        raise