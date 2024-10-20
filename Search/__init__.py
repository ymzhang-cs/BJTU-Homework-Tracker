import requests

class Search:
    """
    查询类，支持查询全部作业或查询未完成作业
    """
    def __init__(self, cookie: dict, print_detail: bool = True) -> None:
        self.cookie = cookie
        self.print_detail = print_detail

        # 课程列表
        # 格式同 response 里的 courseList
        # [{id, name, course_num, ...}, ...]
        self.course_list = None

        # 作业列表
        # 格式同 response 里的 homeworkList
        # [{id, create_date, course_id, ...}, ...]
        self.homework_list = []

        # 通用请求头
        self.common_header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Host": "123.121.147.7:88",
            "X-Requested-With": "XMLHttpRequest",
            "Cookie": f"JSESSIONID={self.cookie['JSESSIONID']}"
        }

        # 请求头中的 Referer
        self.header_referer = {
            "CourseList": "http://123.121.147.7:88/ve/back/coursePlatform/coursePlatform.shtml?method=toCoursePlatformIndex",
            # page_id: 10460 作业 10461 课程报告 10462 实验
            # course_code: 标准课程代码
            # homework_type: 1 作业 2 课程报告 3 实验
            # xkhID: 2024-2025-1-2M302002B04
            # xq: 2024202501 （可以通过http://123.121.147.7:88/ve/back/rp/common/teachCalendar.shtml?method=queryCurrentXq得到）
            "HomeWorkList": "http://123.121.147.7:88/ve/back/coursePlatform/coursePlatform.shtml?"
                            "method=toCoursePlatform&"
                            "courseToPage={page_id}&"
                            "courseId={course_code}&"
                            "dataSource=1&cId={course_id}&"
                            "xkhId={xkhID}&"
                            "xqCode={xq}&"
                            "teacherId={teacher_id}"
        }

        # 当前学期
        self.xq = self.getXq()



    def search(self, search_type: int|str) -> list:
        """
        查询作业
        :param search_type: 查询类型，1: 显示全部课程作业 2: 显示所有未完成作业
        :return:
        """
        search_type = int(search_type)  # 1: 显示全部课程作业 2: 显示所有未完成作业
        if search_type != 1 and search_type != 2:
            raise ValueError("Invalid search type")
        
        self.course_list = self.getCourseList()
        if self.print_detail:
            print(f"已查询到{len(self.course_list)}门课程")
            print("========================================")
            for course in self.course_list:
                print(f"{course['name']}, {course['teacher_name']}")
            print("========================================")

        for course_index in range(len(self.course_list)):
            self.homework_list += self.getHomeworkList(course_index)

        if search_type == 2:
            self.filter(unfinished_only=True)

        return self.homework_list

    def requestGet(self, url: str, referer_type: int, referer_info: dict = None, referer_value: str = None) -> dict:
        header = self.common_header
        if referer_type == 0:
            header["Referer"] = self.header_referer["CourseList"]
        elif referer_type == 1:
            header["Referer"] = self.header_referer["HomeWorkList"].format(**referer_info)
        elif referer_type == -1:
            header["Referer"] = referer_value
        
        response = requests.get(url, headers=header)
        return response.json()

    def getXq(self) -> str:
        url = "http://123.121.147.7:88/ve/back/rp/common/teachCalendar.shtml?method=queryCurrentXq"
        referer_value = "http://123.121.147.7:88/ve/back/rp/common/teachCalendar.shtml?method=queryCurrentXq"
        response = self.requestGet(url, referer_type=-1, referer_value=referer_value)
        if self.print_detail:
            print(f"当前学期: {response['result'][0]['xqCode']}")
        return response["result"][0]["xqCode"]

    def getCourseList(self) -> list:
        url = ("http://123.121.147.7:88/ve/back/coursePlatform/course.shtml?"
               "method=getCourseList&pagesize=100&page=1&xqCode={xq}").format(xq = self.xq)
        response = self.requestGet(url, referer_type=0)
        return response["courseList"]

    def getHomeworkList(self, course_index: int) -> list:
        course_info = self.course_list[course_index]

        if self.print_detail:
            print(f"正在查询{course_info['name']}课程的作业")

        course_id = course_info["id"]
        # homework_type: 0 作业 1 课程报告 2 实验
        url = ("http://123.121.147.7:88/ve/back/coursePlatform/homeWork.shtml?"
               "method=getHomeWorkList&cId={course_id}&subType={homework_type}&page=1&pagesize=100")
        referer_info = {
            "page_id": None,
            "course_code": course_info["course_num"],
            "course_id": course_info["id"],
            "xkhID": course_info["fz_id"],
            "xq": course_info["xq_code"],
            "teacher_id": course_info["teacher_id"]
        }

        homework_list = []
        for homework_type, page_id in enumerate([10460, 10461, 10462]):
            type_url = url.format(course_id=course_id, homework_type=homework_type)
            referer_info["page_id"] = page_id
            response = self.requestGet(type_url, referer_type=1, referer_info=referer_info)
            if response['message'] == '没有数据':
                continue
            homework_list += response["courseNoteList"]

        if self.print_detail:
            print(f"已查询到{len(homework_list)}条作业")

        return homework_list
    
    def filter(self, unfinished_only: bool = False, course_keyword: str = None) -> None:
        if unfinished_only:
            self.homework_list = [homework for homework in self.homework_list if homework["subStatus"] == "未提交"]
        if course_keyword:
            self.homework_list = [homework for homework in self.homework_list if course_keyword in homework["course_name"]]

    def display(self) -> None:
        display_elements = {
            "course_name": "课程名称",
            "title": "作业标题",
            "content": "作业说明",
            "submitCount": "已提交人数",
            "allCount": "总人数",
            "open_date": "发布日期",
            "end_time": "截止日期",
            "subStatus": "提交状态"
        }

        for homework in self.homework_list:
            print("========================================")
            for key, value in display_elements.items():
                print(f"{value}: {homework[key]}")
            print("========================================")
        return

    def output(self) -> str:
        display_elements = {
            "course_name": "课程名称",
            "title": "作业标题",
            "content": "作业说明",
            "submitCount": "已提交人数",
            "allCount": "总人数",
            "open_date": "发布日期",
            "end_time": "截止日期",
            "subStatus": "提交状态"
        }

        output = ""
        for homework in self.homework_list:
            output += "========================================\n"
            for key, value in display_elements.items():
                output += f"{value}: {homework[key]}\n"
            output += "========================================\n"
        return output