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
import os
import datetime


app = Flask(__name__)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    returnmessage = event.message.text
    if event.message.text == "ワン":
        returnmessage = "ワンワン！"
    elif event.message.text == "松田":
        returnmessage = "清水"
    elif event.message.text == "村上":
        returnmessage = "無能"
    elif event.message.text == "今日": 
        date = datetime.date.today()
        returnDay = str(date.year) + "年" + str(date.month) + "月" + str(date.day) + "日 だワン！"
        returnmessage = returnDay
    elif event.message.text == "明日": 
        date = datetime.datetime()
        returnDay = str(date.now()+ datetime.timedelta(days = 1).year) + "年" + str(date.now()+ datetime.timedelta(days = 1).month) + "月" + str(date.now()+ datetime.timedelta(days = 1).day) + "日 だワン！"
        returnmessage = returnDay
    else:
        returnmessage = "ワン！"
    # 返信
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=returnmessage))


if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)