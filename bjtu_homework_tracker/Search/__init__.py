import datetime

import requests

class Search:
    """
    查询类，支持查询全部作业或查询未完成作业
    """
    def __init__(self, cookie: dict, print_detail: bool = True) -> None:
        self.cookie = cookie
        self.print_detail = print_detail

        # sessionid
        self.sessionid = None

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
        self.xq = self._getXq()

    def _requestGet(self, url: str, referer_type: int, referer_info: dict = None, referer_value: str = None) -> dict:
        """
        请求GET请求
        :param url: 请求URL
        :param referer_type: 请求头中的Referer类型。0: CourseList，1: HomeWorkList，-1: 其他（填写在referer_value中）
        :param referer_info: 请求头中的Referer信息
        :param referer_value: 请求头中的Referer值
        :return: 请求响应
        """
        header = self.common_header
        if referer_type == 0:
            header["Referer"] = self.header_referer["CourseList"]
        elif referer_type == 1:
            header["Referer"] = self.header_referer["HomeWorkList"].format(**referer_info)
        elif referer_type == -1:
            header["Referer"] = referer_value
        if self.sessionid:
            header["sessionId"] = self.sessionid
        response = requests.get(url, headers=header)
        return response.json()

    def _getXq(self) -> str:
        url = "http://123.121.147.7:88/ve/back/rp/common/teachCalendar.shtml?method=queryCurrentXq"
        referer_value = "http://123.121.147.7:88/ve/back/rp/common/teachCalendar.shtml?method=queryCurrentXq"
        response = self._requestGet(url, referer_type=-1, referer_value=referer_value)
        if self.print_detail:
            print(f"当前学期: {response['result'][0]['xqCode']}")
        return response["result"][0]["xqCode"]

    def _getSessionid(self) -> str:
        url = "http://123.121.147.7:88/ve/back/coursePlatform/message.shtml?method=getArticleList"
        referer_value = "http://123.121.147.7:88/ve/back/coursePlatform/coursePlatform.shtml?method=toCoursePlatformIndex"
        response = self._requestGet(url, referer_type=-1, referer_value=referer_value)
        print(f"已获取到sessionid: {response['sessionId']}")
        return response["sessionId"]

    def _getCourseList(self) -> list:
        url = ("http://123.121.147.7:88/ve/back/coursePlatform/course.shtml?"
               "method=getCourseList&pagesize=100&page=1&xqCode={xq}").format(xq = self.xq)
        response = self._requestGet(url, referer_type=0)
        print(f"请求课程列表: {response}")
        return response["courseList"]

    def _getHomeworkList(self, course_index: int) -> list:
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
            response = self._requestGet(type_url, referer_type=1, referer_info=referer_info)
            if response['message'] == '没有数据':
                continue
            homework_list += response["courseNoteList"]

        if self.print_detail:
            print(f"已查询到{len(homework_list)}条作业")

        return homework_list

    @staticmethod
    def _filter_course_keyword(positive_keyword: list, negative_keyword: list, homework: dict) -> bool:
        for keyword in positive_keyword:
            if keyword not in homework["course_name"]:
                return False
        for keyword in negative_keyword:
            if keyword in homework["course_name"]:
                return False
        return True

    @staticmethod
    def _filter_finish_status(finish_status: str, homework: dict) -> bool:
        if finish_status == "all":
            return True
        elif finish_status == "finished":
            return homework["subStatus"] == "已提交"
        elif finish_status == "unfinished":
            return homework["subStatus"] == "未提交"
        else:
            raise ValueError("finish_status 参数错误")

    @staticmethod
    def _filter_expired(ignore_expired_n_days: int, ignore_unexpired_n_days: int, homework: dict) -> bool:
        
        """
        利用homework["end_date"]对比当前日期，判断是否已经过期太久，或者距离截止日期还很久,并且判断是否存在没有截止日期的问题   
        """
        end_time_str = homework.get("end_time", "")
        # 特判当前作业没有截止日期
        if not end_time_str:
            return True
        end_date = datetime.datetime.strptime(homework["end_time"], "%Y-%m-%d %H:%M")
        today = datetime.datetime.today()
        if end_date < today - datetime.timedelta(days=ignore_expired_n_days):
            return False
        if end_date > today + datetime.timedelta(days=ignore_unexpired_n_days):
            return False
        return True

    def search(self) -> None:
        """
        查询作业
        :return:
        """
        self.course_list = self._getCourseList()
        if self.print_detail:
            print(f"已查询到{len(self.course_list)}门课程")
            print("========================================")
            for course in self.course_list:
                print(f"{course['name']}, {course['teacher_name']}")
            print("========================================")

        for course_index in range(len(self.course_list)):
            self.homework_list += self._getHomeworkList(course_index)

    def select(self,
               course_positive_keyword: list|tuple = (),
               course_negative_keyword: list|tuple = (),
               finish_status:  str  = "unfinished",
               ignore_expired_n_days: int = 15,
               ignore_unexpired_n_days: int = 90,
               ):
        """
        选择作业
        """
        # 应用keyword筛选
        self.homework_list = [homework for homework in self.homework_list
                              if self._filter_course_keyword(course_positive_keyword, course_negative_keyword, homework)]
        # 应用finish_status筛选
        self.homework_list = [homework for homework in self.homework_list
                              if self._filter_finish_status(finish_status, homework)]
        # 应用expired筛选
        self.homework_list = [homework for homework in self.homework_list
                              if self._filter_expired(ignore_expired_n_days, ignore_unexpired_n_days, homework)]


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
                if homework[key] != "":
                    output += f"{value}: {homework[key]}\n"
                else:
                    output+= f"{value}:教师未设置{value}\n"
            output += "========================================\n"
        return output

    def display(self) -> None:
        print(self.output())
        return
