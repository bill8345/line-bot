from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import pymongo

# 其他使用到的模組
import tempfile, os
import datetime
import time
import requests
from bs4 import BeautifulSoup
from flex_bill import *
from data_process_bill import *



app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi(
    'fviqCIrURR0EdUCCIQR4/A598vqrP78GZW8kMNhjLYbixPNrswOqL++Xz/2NZbhEjybWywmAadFtVynQJJfnZzEgIaffW4QlGgJ3cMKKEMAraK9akKx3ZHr9OXi/pYiRuvoOu4gF+k90o/9J3DnqdwdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('8e19280a18ffcc35a80ee8c4e418b814')


# 監聽所有來自 /callback 的 Post Request
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
        abort(400)
    return 'OK'



# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    if 'ok' == msg:
        message = TextSendMessage(text="test succeeded")
        line_bot_api.reply_message(event.reply_token, message)
    elif '政治' == msg:
        message = web_flex()
        line_bot_api.reply_message(event.reply_token, message)
    elif '公視新聞網' == msg:
        message = public_flex()
        line_bot_api.reply_message(event.reply_token, message)
    elif '公視_關鍵字_Top1' == msg:
        message = TextSendMessage(text = hot_join(mongo_bill('politic','public')[0]))
        line_bot_api.reply_message(event.reply_token, message)
    elif '公視_關鍵字_Top2' == msg:
        message = TextSendMessage(text = hot_join(mongo_bill('politic','public')[1]))
        line_bot_api.reply_message(event.reply_token, message)
    elif '公視_關鍵字_Top3' == msg:
        message = TextSendMessage(text = hot_join(mongo_bill('politic','public')[2]))
        line_bot_api.reply_message(event.reply_token, message)
    elif '公視_Latest' == msg:
        message = TextSendMessage(text=mongo_bill('politic', 'public_latest')[0]['最新五篇'])
        line_bot_api.reply_message(event.reply_token, message)
    elif '關鍵評論網' == msg:
        message = lens_flex()
        line_bot_api.reply_message(event.reply_token, message)
    elif '關鍵評論網_關鍵字_Top1' == msg:
        message = TextSendMessage(text = hot_join(mongo_bill('politic','lens')[0]))
        line_bot_api.reply_message(event.reply_token, message)
    elif '關鍵評論網_關鍵字_Top2' == msg:
        message = TextSendMessage(text = hot_join(mongo_bill('politic','lens')[1]))
        line_bot_api.reply_message(event.reply_token, message)
    elif '關鍵評論網_關鍵字_Top3' == msg:
        message = TextSendMessage(text = hot_join(mongo_bill('politic','lens')[2]))
        line_bot_api.reply_message(event.reply_token, message)
    elif '關鍵評論網_Latest' == msg:
        message = TextSendMessage(text= mongo_bill('politic', 'lens_latest')[0]['最新五篇'])
        line_bot_api.reply_message(event.reply_token, message)
    elif '風傳媒' == msg:
        message = storm_flex()
        line_bot_api.reply_message(event.reply_token, message)
    elif '風傳媒_關鍵字_Top1' == msg:
        message = TextSendMessage(text = hot_join(mongo_bill('politic','storm')[0]))
        line_bot_api.reply_message(event.reply_token, message)
    elif '風傳媒_關鍵字_Top2' == msg:
        message = TextSendMessage(text = hot_join(mongo_bill('politic','storm')[1]))
        line_bot_api.reply_message(event.reply_token, message)
    elif '風傳媒_關鍵字_Top3' == msg:
        message = TextSendMessage(text = hot_join(mongo_bill('politic','storm')[2]))
        line_bot_api.reply_message(event.reply_token, message)
    elif '風傳媒_Latest' == msg:
        message = TextSendMessage(text=mongo_bill('politic', 'storm_latest')[0]['最新五篇'])
        line_bot_api.reply_message(event.reply_token, message)
    else:
        message = TextSendMessage(text='沒有這項指令唷～')
        line_bot_api.reply_message(event.reply_token, message)

import os

'''if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)'''
#原linebot裡面是用這個

if __name__ == "__main__":
    app.run()
