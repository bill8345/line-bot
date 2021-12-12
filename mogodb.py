from hotissue import *
import pymongo

hotissue_para = [11, 'https://www.thenewslens.com/category/politics','?page=2', 'h2', 'class', 'title']
drop_list=['選舉','主席','中國','如何','可能','我們','可能','青年','候選人','立委','台灣',
           '關係','成為','自己','要求','政治','代表','改變','他們','結果','直接','存在','目標','為何','改變',
           '路線','加碼','納入','怎麼','黨主席','背後','臺灣','影響']

client = pymongo.MongoClient("mongodb+srv://billsyu:freemongodb1@billsyu-database.mooky.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
hot_issue = client['hotissue']
hot_issue_col = hot_issue['hotissue_col']
hot_issue_col.delete_many({})

hot_issue_col.insert_one(hotissue(hotissue_para[0], hotissue_para[1], hotissue_para[2], hotissue_para[3], hotissue_para[4],hotissue_para[5]))