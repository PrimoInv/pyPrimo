#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: rishi
"""
import datetime
from datetime import date
from dateutil.relativedelta import relativedelta, MO, WE, FR, TH, TU


holidays = [datetime.date(2025, 2, 26),
            datetime.date(2025, 3, 14),
            datetime.date(2025, 3, 31),
            datetime.date(2025, 4, 10),
            datetime.date(2025, 4, 14),
            datetime.date(2025, 4, 18),
            datetime.date(2025, 5, 1),
            datetime.date(2025, 8, 15),
            datetime.date(2025, 8, 27),
            datetime.date(2025, 10, 2),
            datetime.date(2025, 10, 21),
            datetime.date(2025, 10, 22),
            datetime.date(2025, 11, 5),
            datetime.date(2025, 12, 25)]


months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]


def isHoliday(dt):
    exist = dt in holidays
    return exist


def GetNiftyCurrentExpiryDate(dt):
    return dt + datetime.timedelta( (3-dt.weekday()) % 7 )


def getNiftyCurrentMonthExpiryDate(dt) :
    
    wkDay = TH(-1)
    end_of_month = dt + relativedelta(day=31)
    last_expiry_day = end_of_month + relativedelta(weekday=wkDay)
    if isHoliday(last_expiry_day) :
        last_expiry_day = last_expiry_day - datetime.timedelta(days=1)
    return last_expiry_day


def getNiftyOptionsContract(dt, strike, optionType):
    wkDay = TH(-1)
    month_expiry_date = getNiftyCurrentMonthExpiryDate(dt)
    current_expiry_date  = GetNiftyCurrentExpiryDate(dt)
    if isHoliday(current_expiry_date) :
        current_expiry_date = current_expiry_date - datetime.timedelta(days=1)
        if isHoliday(current_expiry_date) :
            current_expiry_date = current_expiry_date - datetime.timedelta(days=1)
    year2Digits = str(current_expiry_date.year)[2:]
    month = current_expiry_date.month
    mStr = str(month)
    d = current_expiry_date.day
    if month_expiry_date == dt :
        print("Current expiry is monthly expiry")
        monthShort = months[month - 1]
        optionSymbol = "NIFTY" + str(year2Digits) + monthShort + str(strike) + optionType.upper() 
    else :
        year2Digits = str(current_expiry_date.year)[2:]
        month = current_expiry_date.month
        mStr = str(month)
        if month == 10:
            mStr = "O"
        elif month == 11:
            mStr = "N"
        elif month == 12:
            mStr = "D"        
        d = current_expiry_date.day
        dStr = ("0" + str(d)) if d < 10 else str(d)
        optionSymbol = "NIFTY" + str(year2Digits) + mStr + dStr + str(strike) + optionType.upper()
    
    return optionSymbol


def getNiftyWeeklyOptionToBuy(day, price) :
    nearestMultiple = 50
    strike = 0
    inputPrice = price
    remainder = inputPrice % nearestMultiple
    if remainder < int(nearestMultiple / 2):
      strike =  inputPrice - remainder
    else:
      strike =  inputPrice + (nearestMultiple - remainder)
      
    
    return getNiftyOptionsContract(day, strike - 1000 , "PE")



