from cgitb import handler
from flask import Flask,request,abort
from linebot import LineBotApi,WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent,TextMessage,TextSendMessage
import os

app = Flask(__name__)

#環境変数取得
CHANNEL_ACCESS_TOKEN = os.environ["Wx/hKbTLBMB0OyOnn0ywZA3OZcSDGfNmMqgjAaCvtNCvEeNvFRVPFB5HJmKccUASEf+iwAt+1AemtADcooLSW2HL6+kLZefLz+ULwMblOoZ1YsBJoJsTDpSNSjjtBLQQnwp7Lgl7Qdy7fcQwfQujogdB04t89/1O/w1cDnyilFU="]
CHANNEL_SECRET = os.environ["a05d3c2571855c280b89c81e73d67379"]

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

@app.route("/callback",methods=['POST'])
def callback():
    #get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    #get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body:" + body)

    #handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

if __name__ == "__main__":
    #app,run()
    port = int(os.getenv("PORT",5000))
    app.run(host="0,0,0,0", port=port)
        