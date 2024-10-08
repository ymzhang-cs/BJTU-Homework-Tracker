import requests

class Search:
    '''
    查询类，支持查询全部作业或查询未完成作业
    '''
    def __init__(self, cookie) -> None:
        self.cookie = cookie
        self.course_list = None
        self.homework_list = dict()

        self.common_header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Host": "123.121.147.7:88",
            "X-Requested-With": "XMLHttpRequest"
        }

        self.header_referer = {
            "CourseList": "http://123.121.147.7:88/ve/back/coursePlatform/coursePlatform.shtml?method=toCoursePlatformIndex",
            # page_id: 10460 作业 10461 课程报告 10462 实验
            # course_code: 标准课程代码
            # homework_type: 1 作业 2 课程报告 3 实验
            # xkhID: 2024-2025-1-2M302002B04
            # xq: 2024202501 （可以通过http://123.121.147.7:88/ve/back/rp/common/teachCalendar.shtml?method=queryCurrentXq得到）
            "HomeWorkList": "http://123.121.147.7:88/ve/back/coursePlatform/coursePlatform.shtml?method=toCoursePlatform&courseToPage={page_id}&courseId={course_code}&dataSource=1&cId={course_id}&xkhId={xkhID}&xqCode={xq}&teacherId={teacher_id}"
        }

        # add cookie
        self.common_header["Cookie"] = f"JSESSIONID={self.cookie['JSESSIONID']}"

    def search(self, search_type: int|str) -> dict:
        search_type = int(search_type)  # 1: 显示全部课程作业 2: 显示所有未完成作业
        if search_type != 1 and search_type != 2:
            raise ValueError("Invalid search type")
        
        self.course_list = self.getCourseList()
        for course_id, course_info in self.course_list.items():
            self.homework_list += self.getHomeworkList(course_id)

        if search_type == 2:
            self.filter(unfinished_only=True)

        return self.homework_list

    def requestGet(self, url: str, header_type: int, referer_info: dict = None) -> dict:
        header = self.common_header
        if header_type == 0:
            header["Referer"] = self.header_referer["CourseList"]
        elif header_type == 1:
            header["Referer"] = self.header_referer["HomeWorkList"].format(**referer_info)
        
        response = requests.get(url, headers=header)
        return response.json()

    def getCourseList(self) -> dict:
        pass

    def getHomeworkList(self, course_id: str) -> dict:
        pass
    
    def filter(self, unfinished_only: bool = False, course_keyword: str = None) -> None:
        pass

    def display(self) -> None:
        pass