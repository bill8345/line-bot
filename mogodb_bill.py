from hotissue_bill import *
from web_crawler_bill import *
import pymongo

#要人工移除的關鍵字
drop_list=['選舉','主席','中國','如何','可能','我們','可能','青年','候選人','立委','台灣',
           '關係','成為','自己','要求','政治','代表','改變','他們','結果','直接','存在','目標','為何','改變',
           '路線','加碼','納入','怎麼','黨主席','背後','臺灣','影響','投到','二讀','觀點']

#公視 1.爬蟲 2.關鍵字分析 3.搜尋關鍵字5篇 4.清空mongodb 5.上傳關鍵字mongodb 6.上傳最新五篇

no1_public = pubilcnews_crawler('https://news.pts.org.tw/category/1', 10, '?page=')
no2_public = top3_hotissue(hotissue(no1_public), drop_list)

del_mongodb('public')
for i in range(0,3):
    no3_public = search_publicnews(no2_public[i])
    mongodb_upload('politic', 'public', no3_public)

del_mongodb('public_latest')
mongodb_upload('politic', 'public_latest', pub_latest())



#關鍵評論網 1.爬蟲 2.關鍵字分析 3.搜尋關鍵字5篇 4.清空mongodb 5.上傳mongodb

no1_lens = len_crawler('https://www.thenewslens.com/category/politics',8,'?page=')
no2_lens = top3_hotissue(hotissue(no1_public), drop_list)

del_mongodb('lens')
for i in range(0,3):
    no3_lens = search_lens(no2_lens[i])
    mongodb_upload('politic', 'lens', no3_lens)

del_mongodb('lens_latest')
mongodb_upload('politic', 'lens_latest', lens_latest())

#風傳媒 1.爬蟲 2.關鍵字分析 3.搜尋關鍵字5篇 4.清空mongodb 5.上傳mongodb

no1_storm = storm_crawler('https://www.storm.mg/category/118', 50, '/')
no2_storm = top3_hotissue(hotissue(no1_storm), drop_list)

del_mongodb('storm')
for i in range(0,3):
    no3_storm = search_storm(no2_storm[i])
    mongodb_upload('politic', 'storm', no3_storm)

del_mongodb('storm_latest')
mongodb_upload('politic', 'storm_latest', storm_latest())
