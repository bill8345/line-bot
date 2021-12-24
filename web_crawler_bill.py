import requests
from bs4 import BeautifulSoup
#from lxml import etree
import pymongo

def len_crawler(urll,page_int,page_code):
    list_title=[]
    for x in range(1,page_int):
        url = urll+ page_code  + str(x)
        re = requests.get(url)
        soup = BeautifulSoup(re.text, 'html.parser')
        temp = soup.find_all('h2', {'class': 'title'})
        for x in temp:
            list_title.append(x)
    return list_title

def pubilcnews_crawler(urll, page_int, page_code):
    list_title=[]
    for i in range(0, page_int):
        url = urll + page_code + str(i+1)
        re = requests.get(url)
        soup = BeautifulSoup(re.text, 'html.parser')
        temp = soup.find_all('li', {'class': 'd-flex'})
        for a in temp:
            list_title.append(a.h2)
    return list_title

#風傳媒
def storm_crawler(urll, page_int, page_code):
    list_title = []
    for i in range(0, page_int):
        url = urll +page_code + str(i+1)
        re = requests.get(url)
        soup = BeautifulSoup(re.text,'html.parser')
        temp = soup.find_all('a',{'class':'card_link link_title'})
        for x in temp:
            list_title.append(x)
    return list_title

#公視最新五篇
def pub_latest():
    temp_1 = pubilcnews_crawler('https://news.pts.org.tw/category/1', 2, '?page=')
    temp_2 = []
    for i in range(0,5):
        temp_3 = temp_1[i].text + '\n' +temp_1[i].a['href']
        temp_2.append(temp_3)
    join_all = '\n\n'.join(temp_2)
    dic = {}
    dic['最新五篇'] = join_all
    return dic

#關鍵評論網最新五篇
def lens_latest():
    temp_1 = len_crawler('https://www.thenewslens.com/category/politics',2,'?page=')
    temp_2 = []
    for i in range(0,5):
        temp_3 = temp_1[i].text.replace(' ','') + '\n' +temp_1[i].a['href']
        temp_2.append(temp_3)
    join_all = '\n\n'.join(temp_2)
    dic = {}
    dic['最新五篇'] = join_all
    return dic


#風傳媒最新五篇
def storm_latest():
    temp_1 = storm_crawler('https://www.storm.mg/category/118', 2, '/')
    temp_2 = []
    for i in range(0,5):
        temp_3 = temp_1[i].text.replace(' ','')+temp_1[i]['href']
        temp_2.append(temp_3)
    join_all = '\n\n'.join(temp_2)
    dic = {}
    dic['最新五篇'] = join_all
    return dic


def mongodb_upload(issue, web_name,search_result):
    client = pymongo.MongoClient("mongodb+srv://billsyu:freemongodb1@billsyu-database.mooky.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    #關鍵字_DB
    db = client[issue]
    db_col = db[web_name]
    db_col.insert_one(search_result)

def del_mongodb(web_name):
    client_bill = pymongo.MongoClient(
        "mongodb+srv://billsyu:freemongodb1@billsyu-database.mooky.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db_bill = client_bill['politic']
    db_bill_col = db_bill[web_name]
    db_bill_col.delete_many({})

