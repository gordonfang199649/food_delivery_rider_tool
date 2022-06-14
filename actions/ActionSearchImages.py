import random
import re

from agents.ShopImageService import (
    edit_file_permission, list_most_matched_shop_names, list_all_image_links, list_files
)
from dotenv import load_dotenv
from os import getenv
from actions.templates.ShopNameTemplate import shop_name_template
from linebot.models import (
    FlexSendMessage, TextSendMessage, ImageSendMessage
)
import config.Logger
import logging as LOGGER

from models.GoogleFile import GoogleFile

"""
    action - 搜尋圖片
    :author Gordon Fang
    :date 2022-06-11
"""

"""
    configurations
"""
load_dotenv()
LOGGER.getLogger(__name__)

"""
    全域變數
"""
ROWS = int(getenv('ROWS'))
shop_cache = list()

"""
    暫存店家名稱、檔案 ID 作為快取
    1. web server 啟動之時執行
    2. 清除快取
    3. 進入 Google 雲端硬碟撈取所有的資料夾
    4. 將結果儲存到快取，以利加快後續查詢
    5. 設置排程定點清除
"""

def store_all_shop_names():
    shop_cache.clear()
    folders = list_files(query="mimeType = 'application/vnd.google-apps.folder'", fields='files(id, name)')
    shop_cache.extend(map(lambda folder: GoogleFile(folder.get('id'), folder.get('name')), folders))

"""
    列出最符合關鍵字的店家名稱
    
    :param str: 原始訊息
    :param pattern: 正規表達式
    :return Line 訊息封裝物件
"""

def search_for_shop_names(intent: str, pattern: re) -> FlexSendMessage or TextSendMessage:
    # 取出訊息關鍵字
    matched = pattern.match(intent)
    shop_name = matched.group(1)

    # 從快取篩選使用者可能是想要查詢的店家名稱
    filtered_shops = list(filter(lambda shop: shop_name in shop.file_name, shop_cache))
    result = list(map(lambda shop: shop.file_name, filtered_shops))

    try:
        # 找不到店家進入雲端硬碟搜尋
        if len(result) < 1:
            result = list(list_most_matched_shop_names(shop_name=shop_name))
    except Exception as e:
        LOGGER.error(e)
        return TextSendMessage(text='很抱歉，服務異常，請聯絡開發人員。')

    if len(result) > 0:
        # 套用 Line 回覆訊息模板
        template = shop_name_template(shop_names=result)
        return FlexSendMessage(alt_text='shop name', contents=template)

    return TextSendMessage(text='很抱歉，該店家無照片可使用，如果可以的話，請協助拍照，感謝您。')

"""
    列出該店家圖片
    
    :param str: 原始訊息
    :param pattern: 正規表達式
    :return Line 訊息封裝物件
"""

def list_shop_images(intent: str, pattern: re) -> list or TextSendMessage:
    matched = pattern.match(intent)
    shop_name = matched.group(1)
    folder_id = None

    # 篩選欲查詢店家是否在 Cache
    filtered_shops = filter(lambda shop: shop_name == shop.file_name, shop_cache)
    if filtered_shops is not None:
        folder_id = list(filtered_shops)[0].file_id

    try:
        # 進入雲端硬碟搜尋店家名稱前，先看 cache 有沒有 folder ID
        # 如果沒有再進去硬碟內搜尋
        if folder_id is None:
            result = list(list_most_matched_shop_names(shop_name=shop_name))
            folder_id = result[0].get('id')

        # 為配合在 Line 上面顯示圖片，需要更改檔案權限為任何人都能看到連結內容
        user_permission = {
            'type': 'anyone',
            'role': 'reader'
        }
        edit_file_permission(file_id=folder_id, request_body=user_permission)

        image_links = list_all_image_links(folder_id=folder_id)
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
        return image_messages[:ROWS]

    return TextSendMessage(text='很抱歉，該店家無照片可使用，如果可以的話，請協助拍照，感謝您。')
