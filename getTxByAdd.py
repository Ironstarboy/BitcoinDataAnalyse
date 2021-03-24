import requests
from requests.adapters import HTTPAdapter
import json
import pandas as pd
import requests
from requests.adapters import HTTPAdapter
import pymongo
import json
import threadpool
import time
import datetime
import lxml
import csv
import json
from queue import Queue
from re import findall

###根据地址获取相关交易，经匹配，可能存在一些交易缺失

def tx_crawler_by_add(address):
    url = 'https://api.blockchain.info/haskoin-store/btc/address/'+address+'/transactions/full'
    headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
    }
    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=9))
    s.mount('https://', HTTPAdapter(max_retries=9))
    error_l = []
    try:
        tx_details=s.get(url, headers=headers, timeout=(50,160))
        if tx_details.status_code == 200:
            tx_contents=json.loads(tx_details.text)
            if tx_contents and len(tx_contents) > 2:
                analysis_data(tx_contents)
                print("···该地址数据已加载···", address, len(tx_contents))
                return tx_contents
            # insert_mongo_tx(tx_content)
        # else:
        #     print("Transaction Data Error", address)
        #     error_l.append(address)
    except Exception as e:
        pass

def analysis_data(tx_contents):
    global q1
    global q2
    for tx_content in tx_contents:
        for input in tx_content['inputs']:
            tx_in_list = [tx_content['txid'], tx_content['time'], input['address'], input['value']]
            q1.put(tx_in_list)
        for output in tx_content['outputs']:
            tx_out_list = [tx_content['txid'], tx_content['time'], output['address'], output['value']]
            q2.put(tx_out_list)


def start(addlist):
    # 构造线程池
    pool = threadpool.ThreadPool(100)
    reques = threadpool.makeRequests(tx_crawler_by_add, addlist)
    [pool.putRequest(req) for req in reques]
    pool.wait()

def write_data():
    with open('tx_in_sample1_20_f.csv', 'w', newline='')as f:
        writer = csv.writer(f)
        writer.writerow(['txid', 'time', 'input_address', 'input_value'])
        while True:
            tx = q1.get()
            if tx == 'end':
                break
            writer.writerow(tx)
    with open('tx_out_sample1_20_f.csv', 'w', newline='')as f:
        writer = csv.writer(f)
        writer.writerow(['txid', 'time', 'output_address', 'output_value'])
        while True:
            tx = q2.get()
            if tx == 'end':
                break
            writer.writerow(tx)

if __name__ == '__main__':
    # adddf = pd.read_csv('aq.csv')
    q1 = Queue()
    q2 = Queue()
    adddf = pd.read_csv('data_sample1_20_new1.csv')
    tx_in_list=[]
    tx_out_list = []
    print("数据采集开始，当前时间{}···".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    start(list(adddf['address'].unique()))
    q1.put('end')
    q2.put('end')
    write_data()
    print("数据采集完成，当前时间{}···".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))


