import requests

class Search:
    '''
    查询类，支持查询全部作业或查询未完成作业
    '''
    def __init__(self, cookie) -> None:
        self.cookie = cookie

    def search(self, search_type: int|str) -> dict:
        search_type = int(search_type)
        if search_type == 1:
            pass
        elif search_type == 2:
            pass
        else:
            raise ValueError("Invalid search type")
    
    def filter(self, unfinished_only: bool = False, course_keyword: str = None) -> bool:
        pass

    def display(self) -> None:
        pass