from Login import Login
from Search import Search
from Output import Output

import os
import yaml

def welcome() -> None:
    print("欢迎使用作业查询系统")
    print("本系统支持通过cookie登录或通过MIS登录")
    return

def read_config() -> dict:
    with open("config.yaml", "r", encoding='utf-8') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return config

def main() -> None:

    config = read_config()

    # 欢迎界面
    welcome()

    # 登录
    my_login = Login()
    my_login.login()

    # 选择查询方式
    # 1：显示全部课程作业
    # 2：显示所有未完成作业

    search_type = input("请选择查询方式：\n1. 显示全部课程作业\n2. 显示所有未完成作业\n")
    my_search = Search(my_login.cookie)
    my_search.search(search_type)

    # 显示处理方式
    print(f"支持的处理方式：")
    for i in range(len(Output.show_methods())):
        print(f"{i}. {Output.show_methods()[i]}")

    process_type = input("请选择处理方式（留空使用config）：")
    if not process_type:
        process_type = config['process_method']
        if not process_type:
            raise Exception("未设置处理方式")
    else:
        process_type = Output.show_methods()[int(process_type)]

    my_processor = Output(my_search, method=process_type)
    output = my_processor.process()
    print(output)

    # create search_history folder
    if not os.path.exists('./search_history'):
        os.mkdir('./search_history')

    my_processor.save(f'./search_history/')

if __name__ == '__main__':
    main()