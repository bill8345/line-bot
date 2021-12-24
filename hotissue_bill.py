import requests
from bs4 import BeautifulSoup
import jieba

jieba.set_dictionary('dict1.txt')
#page_int:要爬的頁數, url:要爬的網站, page_code:頁數的api, lv1:原始碼第一層, lv2原始碼第二層, lv2原始碼第二層的名字
#最後會回傳一個字典，{關鍵字：出現次數}
def hotissue(temp):
    dict_title = {}
    for temp_3 in temp:
        name_text = temp_3.text.replace(' ','').replace('「','').replace('，','').replace('」','').replace('：','').replace('？','').replace('【','').replace('】','').replace("\n",'').replace('\u3000','')
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

#hotissue: hotissue function的參數, drop_list:要移除的無意義關鍵字
def top3_hotissue(hotissue, drop_list):
    fin_dict_title = sorted(hotissue.items(), key=lambda x:x[1],reverse=True)
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

def search_lens(search_word):
    url = 'https://www.thenewslens.com/search/' + search_word
    re = requests.get(url)
    soup = BeautifulSoup(re.text,'html.parser')
    temp_1 = soup.find_all('h2',{'class':'title'})
    dict_fin = {}
    dict_fin['關鍵字'] = search_word
    for i in range(0,5):
        temp_list = []
        temp_list.append(temp_1[i].text.replace(' ',''))
        temp_list.append(temp_1[i].a['href'])
        dict_fin['文章'+ str(i+1)] = temp_list
    return dict_fin

def search_storm(search_word):
    url = 'https://www.storm.mg/site-search/result?q='+search_word
    re = requests.get(url)
    soup = BeautifulSoup(re.text,'html.parser')
    temp = soup.find_all('a',{'class':'card_link link_title'})
    dict_fin = {}
    dict_fin['關鍵字'] = search_word
    for i in range(0,5):
        temp_list = []
        temp_list.append(temp[i].text.replace('\n',''))
        temp_list.append('https://www.storm.mg/' + temp[i]['href'])
        dict_fin['文章'+ str(i+1)] = temp_list
    return dict_fin

def search_publicnews(search_word):
    url = 'https://news.pts.org.tw/search/'+search_word
    re = requests.get(url)
    soup = BeautifulSoup(re.text,'html.parser')
    temp_title = soup.find_all('li', {'class': 'row'})
    dict_fin = {}
    dict_fin['關鍵字'] = search_word
    for i in range(0,5):
        temp_list = []
        temp_list.append(temp_title[i].h2.text.replace('\n',''))
        temp_list.append(temp_title[i].find('h2').a['href'])
        dict_fin['文章'+ str(i+1)] = temp_list
    return dict_fin