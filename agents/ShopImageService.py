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

class ShopImageService:
    """
        建構子
    """

    def __init__(self):
        load_dotenv()
        self.CLIENT_SECRET_FILE = os.getenv('CLIENT_SECRET_FILE')
        self.API_NAME = os.getenv('API_NAME')
        self.API_VERSION = os.getenv('API_VERSION')
        self.SCOPES = ['https://www.googleapis.com/auth/drive']
        self.FILE_ID = os.getenv('FILE_ID')
        self.google_service_agent = Create_Service(self.CLIENT_SECRET_FILE, self.API_NAME, self.API_VERSION,
                                                   self.SCOPES)

    """
        列出最符合關鍵字的店家名稱
        :param self
        :param shop_name: 商家名稱
        :return 店家名稱
    """

    def list_most_matched_shop_names(self, shop_name: str) -> dict:
        query = f"mimeType = 'application/vnd.google-apps.folder' and name contains '{shop_name}'"
        fields = 'files(id, name)'
        return self.list_files(query=query, fields=fields)

    """
        列出圖像連結
        :param self
        :param folder_id: 商家名稱
        :return 店家圖像連結
    """

    def list_all_image_links(self, folder_id: str) -> list:
        query = f"parents = '{folder_id}' and mimeType contains 'image/'"
        fields = 'files(id, name, webContentLink)'
        images = self.list_files(query=query, fields=fields)
        return list(map(lambda field: field['webContentLink'], images))

    """
        列出符合查詢條件檔案
        :param self
        :param query: 查詢條件
        :param fields: 查詢欄位
        :return 雲端硬碟檔案
    """

    def list_files(self, query: str, fields: str) -> dict:
        LOGGER.info('準備呼叫 Google Drive API - 搜尋檔案')
        response = self.google_service_agent.files().list(q=query, spaces='drive', fields=fields).execute()
        files = response.get('files')
        page_token = response.get('nextPageToken')

        while page_token:
            response = self.google_service_agent.files().list(q=query,
                                                              spaces='drive',
                                                              fields=fields,
                                                              pageToken=page_token).execute()
            files.extend(response.get('files'))
            page_token = response.get('nextPageToken')

        LOGGER.info('Google Drive API 呼叫結束 - 搜尋檔案')

        return files

    """
        取得檔案連結
        :param self
        :param file_id: 檔案 ID
        :return 檔案連結
    """

    def get_web_view_link(self, file_id: str):
        LOGGER.info('準備呼叫 Google Drive API - 取得檔案連結')
        link = self.google_service_agent.files().get(fileId=file_id, fields='webContentLink').execute()
        LOGGER.info('Google Drive API 呼叫結束 - 取得檔案連結')
        return link

    """
        編輯檔案權限
        :param self
        :param file_id: 檔案 ID
        :param request_body: request body
        :return 檔案連結
    """

    def edit_file_permission(self, file_id: str, request_body: dict):
        LOGGER.info('準備呼叫 Google Drive API - 編輯檔案權限')
        self.google_service_agent.new_batch_http_request()
        shared_link = self.google_service_agent.permissions().create(
            fileId=file_id,
            body=request_body
        ).execute()
        LOGGER.info('Google Drive API 呼叫結束 - 編輯檔案權限')
        return shared_link
