# -*- coding=utf-8 -*-
import time
import logging
from datetime import datetime
from beem.market import Market
from beem.account import Account

hive_name = ""
account = Account(hive_name)
sleep_time = 30
diff_threshold = 1.2

def func1(hive_hbd, hive_usdt):
    return abs(hive_hbd-hive_usdt) / max(hive_hbd, hive_usdt) * 100

def getHiveHBDPrice():
    try:
        market = Market("HBD:HIVE")
        t = market.ticker()
        latest = t['latest']
        hive_hbd = float(latest['price']) # convert decimal to float
        return hive_hbd
    except Exception as e:
        print (e)

def getHiveUSDPrice():
    try:
        market = Market("HBD:HIVE")
        hive_usd = market.hive_usd_implied()
        return hive_usd
    except Exception as e:
        print (e)

def main():
    mode = 0
    log_format = "%(asctime)s - %(levelname)s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(fmt=log_format, datefmt=date_format)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler("output.log")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    #market = Market("HBD:HIVE")
    while True:
        hive_hbd = getHiveHBDPrice()
        hive_usd = getHiveUSDPrice()
        if hive_hbd is None or hive_usd is None:
            logger.info(f"Get price from market failed, sleep {sleep_time} seconds ...")
            time.sleep(sleep_time)
            continue
        diff = func1(hive_hbd, hive_usd)
        #diff smaller than diff_threshold
        if diff < diff_threshold:
            dt = datetime.fromtimestamp(int(time.time()))
            if mode != 1 or dt.minute==0 and dt.second==0:
                mode = 1
                logger.info(f"Normal HIVE/HBD: {hive_hbd}, HIVE/USDT: {hive_usd} | {diff}")
        elif hive_hbd < hive_usd:
            mode = 2
            logger.info(f"Alert HIVE/HBD: {hive_hbd}, HIVE/USDT: {hive_usd} | Hive will rise: {diff}")
        else:
            mode = 2
            logger.info(f"Alert HIVE/HBD: {hive_hbd}, HIVE/USDT: {hive_usd} | Hive will drop: {diff}")
        time.sleep(sleep_time)

if __name__ == "__main__":
    main()

