import sys
import os
# 获取当前脚本的目录路径
current_dir = os.path.dirname(os.path.abspath(__file__))
# 获取上两级目录路径
parent_dir = os.path.abspath(os.path.join(current_dir, '../../'))
# 将上两级目录添加到 sys.path
sys.path.append(parent_dir)

import logging
from logging.handlers import RotatingFileHandler
import flask
import datetime
import bs4


from Login import Login
from Search import Search

log_name = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

# Configure logging
if not os.path.exists('./logs'):
    os.mkdir('./logs')
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('homework_query')
handler = RotatingFileHandler(f'./logs/{log_name}.log', maxBytes=10000, backupCount=1)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Configure Flask logger to use the same handler
flask_logger = logging.getLogger('werkzeug')
flask_logger.setLevel(logging.INFO)
flask_logger.addHandler(handler)

def homework_dict_process(homework_list: list) -> list:
    """
    处理作业信息字典
    :param homework_list: 作业信息字典
    :return: 处理后的作业信息字典
    """
    result = []
    for homework in homework_list:
        content_plain_text = bs4.BeautifulSoup(homework['content'], 'html.parser').get_text()
        result.append({
            'title': homework['title'] + ' - ' + homework['course_name'],
            # 如果没有截止时间则显示NAT，因为在编辑快捷指令需要有一个特殊值来判断
            'due_time': homework['end_time'] if homework['end_time'] else 'NAT',
            # 如果没有详情则显示没有详情，因为在编辑快捷指令时发现不能为空
            'content': content_plain_text if content_plain_text else '没有详情',
            'course_name': homework['course_name']
        })
    return result

def query(stu_id: int, stu_pwd: str) -> list:
    # login with student id and password
    my_login = Login('cp')
    my_login.login(student_id=stu_id, password=f'hash:{stu_pwd}')

    # fetch homework
    my_search = Search(my_login.cookie)
    my_search.search()

    # select homework
    select_args = {
        'course_positive_keyword': [],
        'course_negative_keyword': [],
        'finish_status': 'unfinished',
        'ignore_expired_n_days': 15,
        'ignore_unexpired_n_days': 90
    }
    my_search.select(**select_args)

    # process homework
    result = homework_dict_process(my_search.homework_list)
    return result

app = flask.Flask(__name__)

@app.route('/api/homework-query', methods=['POST'])
def query_route():
    data = flask.request.get_json()
    stu_id = data.get('stu_id', None)
    stu_pwd = data.get('stu_pwd', None)
    if stu_id is None or stu_pwd is None:
        logger.error('Missing parameters')
        return flask.jsonify({'error': 'missing parameters'}), 400
    try:
        result = query(stu_id, stu_pwd)
        logger.info('Query successful')
        logger.info(result)
        return flask.jsonify({'result': result})
    except Exception as e:
        logger.exception('Query failed')
        return flask.jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    