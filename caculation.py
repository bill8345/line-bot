from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *


# 其他使用到的模組
import tempfile, os
import pymongo
import billing_mongodb as py
client = pymongo.MongoClient(
        "mongodb+srv://billsyu:freemongodb1@billsyu-database.mooky.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi(
    'tcwe5/mT32qYrgCZrXLH2oYMnphC+EHECHanN+nZEVKNGSgEVugg7R/gwnebRQGtR9IE6FIeoA+1WL1EoNsXq5/+UUuYFKQUJUxoZ82+mD1IPZfvukA6K4ScEEVvr+vPwaeK4X5Fxs74GhtyxNXOCgdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('666d5846ce6653484b7b65a388da2e53')


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
    if int(msg) >= 0:
        temp_1 = py.count('billing', 'count', 'posi')
        temp_2 = py.count('billing', 'count', 'nega')
        temp_1.append(int(msg))
        base_1 = 0
        base_2 = 0
        for i in temp_1:
            base_1 += i
        for x in temp_2:
            base_2 += x
        py.update('billing', 'count', temp_1, temp_2)
        total_count = '目前結算'+str(base_1+base_2)
        message = TextSendMessage(text=total_count)
        line_bot_api.reply_message(event.reply_token, message)
    elif int(msg)<0:
        temp_1 = py.count('billing', 'count', 'posi')
        temp_2 = py.count('billing', 'count', 'nega')
        temp_2.append(int(msg))
        base_1 = 0
        base_2 = 0
        for i in temp_1:
            base_1 += i
        for x in temp_2:
            base_2 += x
        total_count = '目前結算 ' + str((base_1 + base_2))
        py.update('billing', 'count', temp_1, temp_2)
        message = TextSendMessage(text=total_count)
        line_bot_api.reply_message(event.reply_token, message)
    else:
        None

'''if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)'''
#原linebot裡面是用這個

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)