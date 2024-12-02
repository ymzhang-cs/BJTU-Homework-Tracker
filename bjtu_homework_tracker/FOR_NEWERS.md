## 面向新手的使用说明

1. 克隆仓库

    使用 `git clone https://github.com/ymzhang-cs/BJTU-Homework-Tracker.git` ，或下载ZIP后解压

2. 选择合适的环境

    推荐 Python 版本 >= 3.10，可以使用 anaconda 进行虚拟环境管理。

    这是因为 Union Type 对 `|` 的支持是从 3.10 开始的。

    [Union Type](https://docs.python.org/3/library/stdtypes.html#types-union)

3. 安装项目依赖

    在仓库目录下开启终端，切换到虚拟环境，输入：

    ```bash
    pip install -r requirements.txt
    ```

4. 运行

    ```bash
    python run.py
    ```

5. 获取 Cookie

    当需要输入 JSESSIONID 时，登录MIS，打开智慧课程平台。
    
    以Chrome为例，右击网页空白处，“检查”，右侧选择“Network”标签卡，刷新网页，点击含有shtml字样的请求，在右侧偏下找到这样的内容：
    
    ```plaintext
    cookie: JSESSIONID=xxxxxxxxxxxxxxxxx
    ```
    
    后面的 `xxxxxxxxxxxxxxxxx` 就是你的 JSESSIONID，复制粘贴到终端内继续即可。

## 参考资料

- [Downloading files from GitHub - GitHub](https://docs.github.com/en/get-started/start-your-journey/downloading-files-from-github)
- [Managing environments - Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)
- [查看、添加、修改和删除 Cookie - Google DevTools](https://developer.chrome.com/docs/devtools/application/cookies?hl=zh-cn)