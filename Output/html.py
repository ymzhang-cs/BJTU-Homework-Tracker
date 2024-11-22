from Output.abstract import OutputProcessor
from Search import Search

import datetime
import webbrowser
import os
import bs4

from GLOBAL import GLOBAL_CONFIG

class Html(OutputProcessor):
    def __init__(self, search: Search) -> None:
        html = search.output()
        self.html = html.split('\n')
        self.html_head = """
<!DOCTYPE html>
<html>

    <head>
        <style>
            body {
                font-family: Arial, sans-serif;
            }

        .course-container {
                display: flex;
                flex-wrap: wrap;
                justify-content: space-between;
            }

        .course-card {
                width: 45%;
                background-color: #f5f5f5;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                margin-bottom: 20px;
            }

        .course-card div {
                margin-bottom: 15px;
            }

        .course-card label {
                font-weight: bold;
            }

        .course-card img {
                height: auto;
                max-width: 50%;
            }
        </style>
    </head>

<body>
    <div class="course-container">
        """

        self.html_tail = """
    </div>
</body>

</html>
        """

    def __str__(self) -> str:
        return self.process()
    
    def process(self) -> str:
        output = ""
        output += self.html_head

        # 因为plain_text中存在 '========' 行，所以需要一个标志位来判断是否需要添加div
        now_equal_flag = 1

        for homework in self.html:

            # 判断字符串是否为空
            if not homework:
                continue

            homework = homework.strip()
            if homework[0] == "=":
                if now_equal_flag == 1:
                    output += "<div class=\"course-card\">\n"
                    now_equal_flag = 2
                elif now_equal_flag == 2:
                    output += "</div>\n"
                    now_equal_flag = 1
            else:
                # 确保里面存在冒号 是合法的
                if ':' in homework:
                    parts = homework.split(":", 1)
                    label = parts[0]
                    content = parts[1] if len(parts) > 1 else ""
                    output += f'<div><label>{label}: </label><span>{content}</span></div>\n'
                else:
                    continue

        output += self.html_tail

        soup = bs4.BeautifulSoup(output, 'html.parser')
        self.output = soup.prettify()

        func_return = "已处理完成"
        return func_return

    def save(self, path: str, name: str) -> None:
        '''
        需要注意 如果用户选择用html 就不得不选择保存html文件的办法
        '''
        # create save folder   
        if not os.path.exists(path):
            os.mkdir(path)

        full_path = os.path.join(path, name + '.html')
        
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(self.output)

        html_full_path = os.path.join(os.getcwd(), full_path)

        webbrowser.open(html_full_path)
        
        print("========= 再次提醒 =========\n无论您在上次选择中是否选择保存，都会生成html文件！")
        print(f"文件已保存至：{html_full_path}")

        return
    
if __name__ == "__main__":
    pass