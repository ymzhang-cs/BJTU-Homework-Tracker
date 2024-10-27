from Login import Login
from Search import Search
from Output_Processor import OutputProcessor
import yaml

def welcome() -> None:
    print("欢迎使用作业查询系统")
    print("本系统支持通过cookie登录或通过MIS登录")
    return

def read_config() -> dict:
    with open("config.yaml", "r") as f:
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
    output = my_search.output()

    my_processor = OutputProcessor(output)
    output = my_processor.process(method='plain_text')
    print(output)

    if config["save_history"]:
        with open(config["history_file"], "w", encoding='utf-8') as f:
            f.write(output)

    pass

if __name__ == '__main__':
    main()