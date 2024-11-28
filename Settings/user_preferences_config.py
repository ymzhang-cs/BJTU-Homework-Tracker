import yaml
from Settings.abstract import Settings

# 读取自动化配置文件
class User_preference_config(Settings):

    def __init__(self, config_path: str):
        self.__config_path = config_path
        self.__config = self.__read_config()

        # 配置私有属性

        # Program Workflow
        self.__use_config_workflows = self.__config['use_config_workflows']

        # Step 1: Login
        self.__login_active = self.__config['login']['active']
        self.__mis_webdriver_path = self.__config['login']['mis']['webdriver_path']
        self.__mis_browser = self.__config['login']['mis']['browser']

        self.__cookie_JSESSIONID = self.__config['login']['cookie']['JSESSIONID']

        self.__cp_student_id = self.__config['login']['cp']['student_id']
        self.__cp_password = self.__config['login']['cp']['password']

        # Step 3: Select the homework
        self.__select_active = self.__config['select']['active']
        self.__conditions_course_positive_keyword = self.__config['select']['conditions']['course_positive_keyword']
        self.__conditions_course_negative_keyword = self.__config['select']['conditions']['course_negative_keyword']
        self.__conditions_finish_status = self.__config['select']['conditions']['finish_status']
        self.__conditions_ignore_expired_n_days = self.__config['select']['conditions']['ignore_expired_n_days']
        self.__conditions_ignore_unexpired_n_days = self.__config['select']['conditions']['ignore_unexpired_n_days']

        # Step 4: Process method
        self.__process_method = self.__config['process_method']

        # Step 5: Save record
        self.__save_record_active = self.__config['save_record']['active']
        self.__save_record_save_record_folder = self.__config['save_record']['save_record_folder']
        self.__save_record_save_record_name_type = self.__config['save_record']['save_record_name_type']
        self.__save_record_timestamp_format = self.__config['save_record']['timestamp_format']
        self.__save_record_custom_name = self.__config['save_record']['custom_name']

    def __str__(self):
        func_return = f'''
User Preference Config:
    Use Config Workflows: {self.__use_config_workflows}
    Login Active: {self.__login_active}
    MIS Webdriver Path: {self.__mis_webdriver_path}
    MIS Browser: {self.__mis_browser}
    Cookie JSESSIONID: {self.__cookie_JSESSIONID}
    CP Student ID: {self.__cp_student_id}
    CP Password: {self.__cp_password}
    Select Active: {self.__select_active}
    Conditions Course Positive Keyword: {self.__conditions_course_positive_keyword}
    Conditions Course Negative Keyword: {self.__conditions_course_negative_keyword}
    Conditions Finish Status: {self.__conditions_finish_status}
    Conditions Ignore Expired N Days: {self.__conditions_ignore_expired_n_days}
    Conditions Ignore Unexpired N Days: {self.__conditions_ignore_unexpired_n_days}
    Process Method: {self.__process_method}
    Save Record Active: {self.__save_record_active}
    Save Record Save Record Folder: {self.__save_record_save_record_folder}
    Save Record Save Record Name Type: {self.__save_record_save_record_name_type}
    Save Record Timestamp Format: {self.__save_record_timestamp_format}
    Save Record Custom Name: {self.__save_record_custom_name}
    '''
        return func_return

    def __read_config(self) -> dict:
        with open(self.__config_path, "r", encoding='utf-8') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
        return config
    
    def get_use_config_workflows(self) -> bool:
        return self.__use_config_workflows
    
    def get_login_active(self) -> str:
        return self.__login_active
    
    def get_mis_webdriver_path(self) -> str:
        return self.__mis_webdriver_path
    
    def get_mis_browser(self) -> str:
        return self.__mis_browser

    def get_cookie_JSESSIONID(self) -> str:
        return self.__cookie_JSESSIONID

    def get_cp_student_id(self) -> str:
        return self.__cp_student_id

    def get_cp_password(self) -> str:
        return self.__cp_password

    def get_select_active(self) -> bool:
        return self.__select_active

    def get_conditions_course_positive_keyword(self) -> list:
        return self.__conditions_course_positive_keyword

    def get_conditions_course_negative_keyword(self) -> list:
        return self.__conditions_course_negative_keyword

    def get_conditions_finish_status(self) -> str:
        return self.__conditions_finish_status

    def get_conditions_ignore_expired_n_days(self) -> int:
        return self.__conditions_ignore_expired_n_days

    def get_conditions_ignore_unexpired_n_days(self) -> int:
        return self.__conditions_ignore_unexpired_n_days

    def get_process_method(self) -> str:
        return self.__process_method

    def get_save_record_active(self) -> bool:
        return self.__save_record_active

    def get_save_record_folder(self) -> str:
        return self.__save_record_save_record_folder

    def get_save_record_name_type(self) -> int:
        return self.__save_record_save_record_name_type

    def get_save_record_timestamp_format(self) -> str:
        return self.__save_record_timestamp_format

    def get_save_record_custom_name(self) -> str:
        return self.__save_record_custom_name
    
    def return_login_args(self) -> dict:
        login_dict ={
                    'mis' : 
                        {
                            'webdriver_path': self.get_mis_webdriver_path(), 
                            'browser': self.get_mis_browser()
                        }, 
                      
                    'cookie':
                        {
                            'JSESSIONID': self.get_cookie_JSESSIONID()
                        },

                    'cp':
                        {
                            'student_id': self.get_cp_student_id(),
                            'password': self.get_cp_password()
                        }
                    }

        return_dict = login_dict.get(self.get_login_active(), {})
        return return_dict
    
    def return_select_args(self) -> dict:
        select_dict = {
                        'course_positive_keyword': self.get_conditions_course_positive_keyword(),
                        'course_negative_keyword': self.get_conditions_course_negative_keyword(),
                        'finish_status': self.get_conditions_finish_status(),
                        'ignore_expired_n_days': self.get_conditions_ignore_expired_n_days(),
                        'ignore_unexpired_n_days': self.get_conditions_ignore_unexpired_n_days()
                    }
        
        return select_dict

path = 'config.yaml'
user_preferences = User_preference_config(path)

if __name__ == '__main__':
    print(user_preferences)