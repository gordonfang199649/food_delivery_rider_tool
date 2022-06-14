import os

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage
)
from dotenv import load_dotenv

from intents.IntentDispatcher import IntentDispatcher
from utils.LRUCache import LRUCache
import config.Logger
import logging as LOGGER

LOGGER.getLogger(__name__)
load_dotenv()
cache = LRUCache(10)
app = Flask(__name__)

line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))

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
    LOGGER.info(f'Line 使用者 ID: {event.source.user_id}')
    LOGGER.info(f'Line 使用者傳送訊息: {event.message.text}')
    dispatcher = IntentDispatcher()
    reply_message = dispatcher.dispatch(intent=event.message.text, cache=cache)
    if reply_message is not None:
        line_bot_api.reply_message(event.reply_token, reply_message)

if __name__ == "__main__":
    app.run()