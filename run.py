import datetime

from Login import Login
from Search import Search
from Output import Output

from Settings.user_preferences_config import user_preferences

import os
import yaml

def welcome(use_config_workflows: bool) -> None:
    print("欢迎使用作业查询系统")
    print("本系统支持通过cookie登录、通过课程平台默认密码登录或通过MIS登录")
    print("当前模式：", "使用config" if use_config_workflows else "手动选择")
    return

def main() -> None:

    # 初始化：读取配置文件
    use_config_workflows = user_preferences.get_use_config_workflows()

    # 欢迎界面
    welcome(use_config_workflows)

    # Step 1. 登录
    # 初始化配置变量
    login_method = None
    login_args = None
    if use_config_workflows:
        login_method = user_preferences.get_login_active()
        login_args = user_preferences.return_login_args()

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
        select_status = user_preferences.get_select_active()
        if select_status:
            select_args = user_preferences.return_select_args()
            my_search.select(**select_args)
        else:
            print("提示：配置文件中未启用筛选条件")
    else:
        print("提示：命令行模式将使用默认配置筛选")
        my_search.select()


    # Step 4. 处理
    process_type = None
    if use_config_workflows:
        process_type = user_preferences.get_process_method()
    else:
        print("支持的处理方式：", Output.show_methods())
        process_type = input("请选择处理方式：")
        if not process_type:
            raise Exception("未设置处理方式")
    my_processor = Output(my_search, method=process_type)
    output = my_processor.process()
    print(output)

    # Step 5. 保存
    save = user_preferences.get_save_record_active()
    save_path = user_preferences.get_save_record_folder()
    save_name = user_preferences.get_save_record_custom_name()
    name_type = user_preferences.get_save_record_name_type()

    if use_config_workflows:
        if name_type == 1:
            save_name = datetime.datetime.now().strftime(user_preferences.get_save_record_timestamp_format())
        elif name_type == 2:
            save_name = user_preferences.get_save_record_custom_name()
        else:
            raise Exception("未知的保存方式")
    else:
        save = input("\n========= 需要注意 =========\n如果您选择了用html展示，不管您是否选择保存，都会生成html文件！\n是否保存？请您选择(y/n)：")
        if save == 'y':
            save = True
            save_path = input("请输入保存路径：")
            save_name = input("请输入保存文件名：")
        else:
            save = False

    # 如果是html文件，就要特判
    if process_type == 'html':
        save = True

    # 只有保存才会调用
    if save:
        my_processor.save(save_path, save_name)    

if __name__ == '__main__':
    main()