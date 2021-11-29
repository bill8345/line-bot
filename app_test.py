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

import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

line_bot_api = LineBotApi('+tTyNqBu1SKubrawrqRUa8NS5/n0MR9hwinWh6IXOgr+xrutgmkuIohx8u/p/L3yR9IE6FIeoA+1WL1EoNsXq5/+UUuYFKQUJUxoZ82+mD0CELNSwayWX88SD1eHjjCNqxaxmZDQv582JUgeXC125wdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('666d5846ce6653484b7b65a388da2e53')


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
    # 新片電影爬蟲
    movie_dit = {}
    movie_list = []
    url_movie = 'https://movies.yahoo.com.tw/'
    re_movie = requests.get(url_movie)
    soup_movie = BeautifulSoup(re_movie.text, 'html.parser')
    yahoo_movie = soup_movie.find_all('div', {'class': 'movielist_info'})
    for movie in yahoo_movie:
        movie_dit[movie.a.text] = movie.h3.text
        movie_list.append(movie.a.text)
        movie_name = '  #'.join(movie_list)
    # 新片電影爬蟲

    # 上映中電影爬蟲
    name_list = []
    onair_dit = {}
    for page in range(1, 3):
        url_onair_movie = 'https://movies.yahoo.com.tw/movie_intheaters.html?page=' + str(page)
        re_onair_movie = requests.get(url_onair_movie)
        soup_onair = BeautifulSoup(re_onair_movie.text, 'html.parser')
        onair_movie = soup_onair.find_all('div', {'class': 'release_info'})
        for movie in onair_movie:
            try:
                name = movie.find('a').text
                name = name.replace(' ', '').replace('\n', '')
                name_list.append(name)
                namelist = '#'.join(name_list)
                html_temp = movie.find('div', {'class': 'release_btn color_btnbox'})
                html_temp1 = html_temp.find('a', {'class': 'btn_s_vedio gabtn'})
                html = html_temp1['href']
                onair_dit[name] = html
            except TypeError:
                continue
    # 上映中電影爬蟲
    message_text = event.message.text
    if message_text == '新片':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=movie_name))
    elif message_text in movie_list:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=movie_dit[message_text]))
    elif message_text == '上映中':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=namelist))
    elif message_text in name_list:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=onair_dit[message_text]))
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Wrong Keyword"))

if __name__ == "__main__":
    app.run()
