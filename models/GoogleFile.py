"""
    Google 雲端硬碟檔案
"""
class GoogleFile:
    """
        建構子
        :param file_id : 檔案 ID
        :param file_name : 檔案名稱
    """

    def __init__(self, file_id, file_name):
        self._file_id = file_id
        self._file_name = file_name

    """
        :return file_id : 檔案 ID
    """

    @property
    def file_id(self) -> str:
        return self._file_id

    """
        :param file_id : 檔案 ID
    """

    @file_id.setter
    def file_id(self, new_file_id: str):
        self._file_id = new_file_id

    """
        :return file_name : 檔案名稱
    """

    @property
    def file_name(self) -> str:
        return self._file_name

    """
        :param file_name : 檔案名稱
    """

    @file_name.setter
    def file_name(self, new_file_name: str):
        self._file_name = new_file_name
