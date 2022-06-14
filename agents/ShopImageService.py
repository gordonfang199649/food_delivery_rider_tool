import json
import logging
import os

from dotenv import load_dotenv
from agents.Google import Create_Service
import config.Logger
import logging as LOGGER

"""
    雲端硬碟圖庫處理服務
    :author Gordon Fang
    :date 2022-06-05
"""

"""
    configurations
"""

load_dotenv()
logging.getLogger(__name__)

"""
    全域變數
"""

CLIENT_SECRET_FILE = os.getenv('CLIENT_SECRET_FILE')
API_NAME = os.getenv('API_NAME')
API_VERSION = os.getenv('API_VERSION')
SCOPES = [os.getenv('SCOPES')]
google_service_agent = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

"""
    列出最符合關鍵字的店家名稱
    :param shop_name: 商家名稱
    :return 店家名稱
"""

def list_most_matched_shop_names(shop_name: str) -> dict:
    query = f"mimeType = 'application/vnd.google-apps.folder' and name contains '{shop_name}'"
    fields = 'files(id, name)'
    return list_files(query=query, fields=fields)

"""
    列出圖像連結
    :param folder_id: 商家名稱
    :return 店家圖像連結
"""

def list_all_image_links(folder_id: str) -> list:
    query = f"parents = '{folder_id}' and mimeType contains 'image/'"
    fields = 'files(id, name, webContentLink)'
    images = list_files(query=query, fields=fields)
    return list(map(lambda field: field['webContentLink'], images))

"""
    列出符合查詢條件檔案
    :param query: 查詢條件
    :param fields: 查詢欄位
    :return 雲端硬碟檔案
"""

def list_files(query: str, fields: str) -> dict:
    LOGGER.info(f'Google 雲端硬碟檔案查詢條件: {query}')
    LOGGER.info(f'Google 雲端硬碟檔案查詢欄位: {fields}')
    LOGGER.info('準備呼叫 Google Drive API - 搜尋檔案')
    response = google_service_agent.files().list(q=query, spaces='drive', fields=fields).execute()
    files = response.get('files')
    page_token = response.get('nextPageToken')

    while page_token:
        response = google_service_agent.files().list(q=query,
                                                     spaces='drive',
                                                     fields=fields,
                                                     pageToken=page_token).execute()
        files.extend(response.get('files'))
        page_token = response.get('nextPageToken')

    LOGGER.info('Google Drive API 呼叫結束 - 搜尋檔案')

    return files

"""
    取得檔案連結
    :param file_id: 檔案 ID
    :return 檔案連結
"""

def get_web_view_link(file_id: str):
    LOGGER.info('準備呼叫 Google Drive API - 取得檔案連結')
    link = google_service_agent.files().get(fileId=file_id, fields='webContentLink').execute()
    LOGGER.info('Google Drive API 呼叫結束 - 取得檔案連結')
    return link

"""
    編輯檔案權限
    :param file_id: 檔案 ID
    :param request_body: request body
    :return 檔案連結
"""

def edit_file_permission(file_id: str, request_body: dict):
    LOGGER.info('準備呼叫 Google Drive API - 編輯檔案權限')
    google_service_agent.new_batch_http_request()
    shared_link = google_service_agent.permissions().create(
        fileId=file_id,
        body=request_body
    ).execute()
    LOGGER.info('Google Drive API 呼叫結束 - 編輯檔案權限')
    return shared_link
