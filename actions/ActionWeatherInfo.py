import os
import re
import time
from dotenv import load_dotenv
from linebot.models import ImageSendMessage

from utils.LRUCache import LRUCache
import config.Logger
import logging as LOGGER

load_dotenv()

"""
    intent - 天氣資訊
    :author Gordon Fang
    :date 2022-06-12
"""

class ActionWeatherInfo:
    """
        建構子
        :param self
        :param cache: 注入進來的快取器
    """

    def __init__(self, cache: LRUCache):
        self.CWB_URL = os.getenv('CWB_URL')
        self.cache = cache

    """
        獲取氣象局雷達回波圖（衛星雲圖）
        :param self
        :param str: 原始訊息
        :param pattern: 正規表達式
        :return Line 訊息封裝物件
    """

    def get_cloud_image(self, intent: str, pattern: re) -> ImageSendMessage:
        url = f'{self.CWB_URL}?{time.time_ns()}'
        LOGGER.info(f'呼叫氣象局 API ; URL: {url}')
        return ImageSendMessage(
            original_content_url=url,
            preview_image_url=url)
