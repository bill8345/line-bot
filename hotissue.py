import requests
from bs4 import BeautifulSoup
import jieba

jieba.set_dictionary('dict1.txt')
#page_int:要爬的頁數, url:要爬的網站, page_code:頁數的api, lv1:原始碼第一層, lv2原始碼第二層, lv2原始碼第二層的名字
#最後會回傳一個字典，{關鍵字：出現次數}
def hotissue(page_int,url,page_code,lv1,lv2,lv2_lv1):
    dict_title = {}
    for x in range(1,page_int):
        url_lens = url+ page_code + str(x)
        re_lens = requests.get(url_lens)
        soup_lens = BeautifulSoup(re_lens.text, 'html.parser')
        temp_2 = soup_lens.find_all(lv1, {lv2: lv2_lv1})

        for temp_3 in temp_2:
            name_text = temp_3.text.replace(' ','').replace('「','').replace('，','').replace('」','').replace('：','').replace('？','').replace('【','').replace('】','')
            jieba_title = '\ '.join(jieba.cut(name_text, cut_all=False, HMM=False))
            list_title = jieba_title.split('\ ')
            for word in list_title:
                if word not in dict_title:
                    dict_title[word] = 1
                elif word in dict_title:
                    dict_title[word] = dict_title[word] +1
                else:
                    print('worng')

    return dict_title

#hotissue_para: hotissue function的參數, drop_list:要移除的無意義關鍵字
def top3_hotissue(hotissue_mongodb, drop_list):
    fin_dict_title = sorted(hotissue_mongodb.items(), key=lambda x:x[1],reverse=True)
    keyword = []
    for i in range(len(fin_dict_title)):
        if len(fin_dict_title[i][0]) != 1:
            keyword.append(fin_dict_title[i])
    drop_word=drop_list
    drop_temp = []
    for x in keyword:
        if x[0] in drop_word:
            drop_temp.append(x)
    for i in drop_temp:
        keyword.remove(i)
    top3_keyword = []
    for i in range(0,3):
        top3_keyword.append(keyword[i][0])
    return top3_keyword