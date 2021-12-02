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

import configparser
import requests
from bs4 import BeautifulSoup

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
    temp_1 = soup_lens.find('h2', {'class': 'title'})
    #關鍵評論網爬蟲#


    politic_url = '*請輸入你有興趣得網路媒體*\n端傳媒\n關鍵評論網\n中央社'
    title_politic = temp_1[0].text.replace('2021', '#').split('#')[0]
    html_politic = temp_1[0].a['href']
    lens_title = temp_1.text.replace(' ', '')
    lens_html = temp_1.a['href']
    message_text = event.message.text

    if message_text == '政治':
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=politic_url))

    elif message_text == '中央社':
        reply_arr_cen = []
        reply_arr_cen.append(TextSendMessage(text=title_politic))
        reply_arr_cen.append(TextSendMessage(text=html_politic))
        line_bot_api.reply_message(
            event.reply_token,
            reply_arr)
    elif message_text == '關鍵評論網':
        reply_arr_lens = []
        reply_arr_lens.append(TextSendMessage(text=lens_title))
        reply_arr_lens.append(TextSendMessage(text=lens_html))
        line_bot_api.reply_message(
            event.reply_token,
            reply_arr)
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Wrong Keyword"))

if __name__ == "__main__":
    app.run()
