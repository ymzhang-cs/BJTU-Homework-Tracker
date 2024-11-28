import sys
import os
# 获取当前脚本的目录路径
current_dir = os.path.dirname(os.path.abspath(__file__))
# 获取上两级目录路径
parent_dir = os.path.abspath(os.path.join(current_dir, '../../../'))
# 将上两级目录添加到 sys.path
sys.path.append(parent_dir)

import flask

app = flask.Flask(__name__)

@app.route('/api/homework-query', methods=['POST'])
def query_route():
    content = [{'title': '补交课后作业1 - 数字系统基础', 'due_time': '', 'content': '', 'course_name': '数字系统基础'}, {'title': '补交实验作业1 - 数字系统基础', 'due_time': '', 'content': '未提交的实 验作业按要求补交。', 'course_name': '数字系统基础'}, {'title': '2024必做编程作业18:YGXXGL - 面向对象程序设计与C++', 'due_time': '2024-12-22 23:00', 'content': '', 'course_name': '面向对象程序设计与C++'}, {'title': '2024必做编程作业17:YCCL - 面向对象程序设计与C++', 'due_time': '2024-12-22 23:00', 'content': '', 'course_name': '面向对象程序设计与C++'}]
    return flask.jsonify({'result': content})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)