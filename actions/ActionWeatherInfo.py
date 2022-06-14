import os
import re
import time
from dotenv import load_dotenv
from linebot.models import ImageSendMessage

import config.Logger
import logging as LOGGER

"""
    intent - 天氣資訊
    :author Gordon Fang
    :date 2022-06-12
"""

"""
    configurations
"""

load_dotenv()
LOGGER.getLogger(__name__)

"""
    全域變數
"""

CWB_URL = os.getenv('CWB_URL')

"""
    獲取氣象局雷達回波圖（衛星雲圖）
    :param str: 原始訊息
    :param pattern: 正規表達式
    :return Line 訊息封裝物件
"""

def get_cloud_image(intent: str, pattern: re) -> ImageSendMessage:
    url = f'{CWB_URL}?{time.time_ns()}'
    LOGGER.info(f'呼叫氣象局 API ; URL: {url}')
    return ImageSendMessage(
        original_content_url=url,
        preview_image_url=url)
