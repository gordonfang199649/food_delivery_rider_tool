import json
import os
import socket

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

from actions.ActionSearchImages import store_all_shop_names
from intents.IntentDispatcher import dispatch
import config.Logger
import logging as LOGGER

"""
    configurations
"""
LOGGER.getLogger(__name__)
load_dotenv()

"""
    全域變數
"""
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))
app = Flask(__name__)

"""
    call back function
"""

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    LOGGER.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        LOGGER.error("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

"""
    清除店家快取資料
"""

@app.route("/cleanShopCache", methods=['GET'])
def clean_shop_cache():
    host_name = socket.gethostname()
    ip_address = socket.gethostbyname(host_name)

    if request.remote_addr == ip_address:
        store_all_shop_names()
    else:
        abort(403)

    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

"""
    處理 Line 文字訊息
    :param event: 事件
"""

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    profile = line_bot_api.get_profile(event.source.user_id)
    LOGGER.info(f'Line 使用者 ID: {profile.user_id}')
    LOGGER.info(f'Line 使用者顯示名稱: {profile.display_name}')
    LOGGER.info(f'Line 使用者傳送訊息: {event.message.text}')

    reply_message = dispatch(intent=event.message.text)
    if reply_message is not None:
        line_bot_api.reply_message(event.reply_token, reply_message)

if __name__ == "__main__":
    store_all_shop_names()
    app.run()
