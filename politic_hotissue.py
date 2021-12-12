from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

import jieba
import configparser
import requests
from bs4 import BeautifulSoup
from hotissue import *
import pymongo

app = Flask(__name__)

config = configparser.ConfigParser()
config.read('config.ini')
line_bot_api = LineBotApi(config.get('line_bot','channel_token'))
handler = WebhookHandler(config.get('line_bot','channel_secret'))


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    client = pymongo.MongoClient(
        "mongodb+srv://billsyu:freemongodb1@billsyu-database.mooky.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    hot_issue = client['hotissue']
    hot_issue_col = hot_issue['hotissue_col']
    hotissue_mongodb = hot_issue_col.find_one()
    del hotissue_mongodb['_id']
    drop_list = ['選舉', '主席', '中國', '如何', '可能', '我們', '可能', '青年', '候選人', '立委', '台灣',
                 '關係', '成為', '自己', '要求', '政治', '代表', '改變', '他們', '結果', '直接', '存在', '目標', '為何', '改變',
                 '路線', '加碼', '納入', '怎麼', '黨主席', '背後', '臺灣', '影響']
    hotissue_lens = top3_hotissue(hotissue_mongodb, drop_list)
    #中央社爬蟲#
    url_cent = 'https://www.cna.com.tw/list/aipl.aspx'
    re_cent = requests.get(url_cent)
    soup_cent = BeautifulSoup(re_cent.text, 'html.parser')
    temp = soup_cent.find('ul', {'class': 'mainList imgModule'})
    temp_1 = temp.find_all('li')
    #中央社爬蟲#

    #關鍵評論網爬蟲#
    url_lens = 'https://www.thenewslens.com/category/politics'
    re_lens = requests.get(url_lens)
    soup_lens = BeautifulSoup(re_lens.text, 'html.parser')
    temp_2 = soup_lens.find_all('h2', {'class': 'title'})
    #關鍵評論網爬蟲#

    title_politic = temp_1[0].text.replace('2021', '#').split('#')[0]
    html_politic = temp_1[0].a['href']
    lens_title = temp_2[0].text.replace(' ', '')
    lens_html = temp_2[0].a['href']
    message_text = event.message.text

    if message_text == '政治':
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='*請輸入你有興趣得網路媒體*\n端傳媒\n關鍵評論網\n中央社'))

    elif message_text == '中央社':
        reply_arr_cen = []
        reply_arr_cen.append(TextSendMessage(text=title_politic))
        reply_arr_cen.append(TextSendMessage(text=html_politic))
        line_bot_api.reply_message(
            event.reply_token,
            reply_arr_cen)
    elif message_text == '關鍵評論網':
        reply_arr_lens = []
        reply_arr_lens.append(TextSendMessage(text=lens_title))
        reply_arr_lens.append(TextSendMessage(text=lens_html))
        line_bot_api.reply_message(
            event.reply_token,
            reply_arr_lens)
    elif message_text == '熱門議題':
        reply_hot = '請輸入你有興趣的網路媒體，端傳媒、關鍵評論網、中央社\n輸入格式：熱門/{網路媒體}'
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_hot))
    elif message_text == '熱門/關鍵評論網':
        reply_hot = '根據關鍵評論網政治版近一個月的文章標題分析，前三大熱門關鍵字為：\n1. {}\n2. {}\n3. {}\n'.format(hotissue_lens[0],hotissue_lens[1],hotissue_lens[2])
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_hot))
    elif message_text in hotissue_lens:
        search_para = ['https://www.thenewslens.com', '/search/',message_text, 'h2', 'class', 'title']
        reply = search(search_para[0],search_para[1],search_para[2],search_para[3],search_para[4],search_para[5])
        reply_arr = []
        reply_arr.append(TextSendMessage(text=reply[0]))
        reply_arr.append(TextSendMessage(text=reply[1]))
        line_bot_api.reply_message(
            event.reply_token,
            reply_arr)
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Wrong Keyword"))

if __name__ == "__main__":
    app.run()
