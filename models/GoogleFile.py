class GoogleFile:
    def __init__(self):
        self._file_id = None
        self._file_name = None

    @property
    def file_id(self) -> str:
        return self._file_id

    @file_id.setter
    def file_id(self, new_file_id: str):
        self._file_id = new_file_id

    @property
    def file_name(self) -> str:
        return self._file_name

    @file_name.setter
    def file_name(self, new_file_name: str):
        self._file_name = new_file_name
