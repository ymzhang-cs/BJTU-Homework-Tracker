import datetime

from Login import Login
from Search import Search
from Output import Output

import os
import yaml

def welcome(use_config_workflows: bool) -> None:
    print("欢迎使用作业查询系统")
    print("本系统支持通过cookie登录或通过MIS登录")
    print("当前模式：", "使用config" if use_config_workflows else "手动选择")
    return

def read_config() -> dict:
    with open("config.yaml", "r", encoding='utf-8') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return config

def main() -> None:

    # 初始化：读取配置文件
    config = read_config()
    use_config_workflows = config['use_config_workflows']

    # 欢迎界面
    welcome(use_config_workflows)

    # Step 1. 登录
    # 初始化配置变量
    login_method = None
    login_args = None
    if use_config_workflows:
        login_method = config['login']['active']
        login_args = config['login'][login_method]

    # 初始化登录类
    my_login = Login(login_method)

    # 登录
    if use_config_workflows:
        my_login.login(**login_args)
    else:
        my_login.user_select_method()
        my_login.login()

    # Step 2. 选择查询方式
    # 初始化查询类
    my_search = Search(my_login.cookie)
    # 查询
    my_search.search()

    # Step 3. 课程筛选
    if use_config_workflows:
        select_status = config['select']['active']
        if select_status:
            select_args = config['select']['conditions']
            my_search.select(**select_args)
        else:
            print("提示：配置文件中未启用筛选条件")
    else:
        print("提示：命令行模式将使用默认配置筛选")
        my_search.select()


    # Step 4. 处理
    process_type = None
    if use_config_workflows:
        process_type = config['process_method']
    else:
        print("支持的处理方式：", Output.show_methods())
        process_type = input("请选择处理方式：")
        if not process_type:
            raise Exception("未设置处理方式")
    my_processor = Output(my_search, method=process_type)
    output = my_processor.process()
    print(output)

    # Step 5. 保存
    save = True
    save_path = './search_history/'
    save_name = None

    if use_config_workflows:
        save_args = config['save_record']
        save = save_args['active']
        save_path = save_args['save_record_folder']
        name_type = save_args['save_record_name_type']
        if name_type == 1:
            save_name = datetime.datetime.now().strftime(save_args['timestamp_format'])
        elif name_type == 2:
            save_name = save_args['custom_name']
        else:
            raise Exception("未知的保存方式")
    else:
        save = input("是否保存？(y/n)")
        if save == 'y':
            save_path = input("请输入保存路径：")
            save_name = input("请输入保存文件名：")

    # create search_history folder
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    my_processor.save(f'./search_history/', save_name)

if __name__ == '__main__':
    main()