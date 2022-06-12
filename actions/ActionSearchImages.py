import random
import re

from agents.ShopImageService import ShopImageService
from dotenv import load_dotenv
from os import getenv
from actions.templates.ShopNameTemplate import shop_name_template
from linebot.models import (
    FlexSendMessage, TextSendMessage, ImageSendMessage
)
from utils.LRUCache import LRUCache
import config.Logger
import logging as LOGGER

load_dotenv()
LOGGER.getLogger(__name__)

"""
    action - 搜尋圖片
    :author Gordon Fang
    :date 2022-06-11
"""

class ActionSearchImages:
    """
        建構子
        :param self
        :param cache: 注入進來的快取器
    """

    def __init__(self, cache: LRUCache):
        self.cache = cache
        self.image_service = ShopImageService()
        self.ROWS = int(getenv('ROWS'))

    """
        列出最符合關鍵字的店家名稱
        :param self
        :param str: 原始訊息
        :param pattern: 正規表達式
        :return Line 訊息封裝物件
    """

    def search_for_shop_names(self, intent: str, pattern: re) -> FlexSendMessage or TextSendMessage:
        # 取出訊息關鍵字
        matched = pattern.match(intent)

        try:
            result = list(self.image_service.list_most_matched_shop_names(shop_name=matched.group(1)))
        except Exception as e:
            LOGGER.error(e)
            return TextSendMessage(text='很抱歉，服務異常，請聯絡開發人員。')

        if len(result) > 0:
            # 搜尋結果最多取 5 筆
            # result = result[:self.ROWS]
            folder_ids = list(map(lambda field: field['id'], result))
            shop_names = list(map(lambda field: field['name'], result))

            # 將店家名稱、檔案 ID 存放快取器
            # 下次要搜尋圖片無須進入到雲端硬碟模糊搜尋，可以憑藉 檔案 ID 撈取圖片
            for idx, name in zip(folder_ids, shop_names):
                self.cache.set(key=name, value=idx)

            # 套用 Line 回覆訊息模板
            template = shop_name_template(shop_names=shop_names)
            return FlexSendMessage(alt_text='shop name', contents=template)

        return TextSendMessage(text='很抱歉，該店家無照片可使用，如果可以的話，請協助拍照，感謝您。')

    """
        列出該店家圖片
        :param self
        :param str: 原始訊息
        :param pattern: 正規表達式
        :return Line 訊息封裝物件
    """

    def list_shop_images(self, intent: str, pattern: re) -> list or TextSendMessage:
        matched = pattern.match(intent)
        shop_name = matched.group(1)
        folder_id = self.cache.get(shop_name)

        try:
            # 進入雲端硬碟搜尋店家名稱前，先看 Cache 有沒有 folder ID
            # 如果沒有再進去硬碟內搜尋
            if folder_id is None:
                result = list(self.image_service.list_most_matched_shop_names(shop_name=shop_name))
                folder_id = result[0].get('id')

            # 為配合在 Line 上面顯示圖片，需要更改檔案權限為任何人都能看到連結內容
            user_permission = {
                'type': 'anyone',
                'role': 'reader'
            }
            self.image_service.edit_file_permission(file_id=folder_id, request_body=user_permission)

            image_links = self.image_service.list_all_image_links(folder_id=folder_id)
        except Exception as e:
            LOGGER.error(e)
            return TextSendMessage(text='很抱歉，服務異常，請聯絡開發人員。')

        if len(image_links) > 0:
            image_messages = list()
            for link in image_links:
                image_messages.append(ImageSendMessage(
                    original_content_url=link,
                    preview_image_url=link))

            # 配合 Line 訊息一次只能傳 5 則，隨機挑選 5 張圖片
            random.shuffle(image_messages)
            return image_messages[:self.ROWS]

        return TextSendMessage(text='很抱歉，該店家無照片可使用，如果可以的話，請協助拍照，感謝您。')
