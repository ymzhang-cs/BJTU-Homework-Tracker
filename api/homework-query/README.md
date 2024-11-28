# Homework Query API

## 介绍

该文件夹是实现运行在服务器上的一个查询作业的 API，该 API 可以通过 HTTP 请求来查询作业。

可以配合 iOS 快捷指令 **BJTU智慧课程平台作业抓取** 使用。

直接导入：[iCloud 分享链接](https://www.icloud.com/shortcuts/f05b8d5d878340058750b00cbbf001dc)

或者下载指令文件：[shortcut/BJTU智慧课程平台作业抓取.shortcut](./shortcut/BJTU智慧课程平台作业抓取.shortcut)

## 部署

> [!NOTE]
> 部署前请确保已经安装了 Python 3.11 及以上版本，并且服务器开放了 5000 端口。

```bash
git clone https://github.com/ymzhang-cs/BJTU-Homework-Tracker.git
cd BJTU-Homework-Tracker/api/homework-query
pip install -r requirements.txt
python query_service.py
```

## 工作流程

请求内容：

`POST /api/homework-query`

```json
{
    "stu_id": "你的学号",
    "stu_pwd": "md5(你的智慧课程平台密码)"
}
```

返回内容：

```json
{
    "result": [
        {
            "name": "作业名称",
            "due_time": "截止日期",
            "content": "状态",
            "course_name": "课程名称"
        }
    ]
}
```

## Test

```bash
curl -X POST http://127.0.0.1:5000/api/homework-query \
    -H "Content-Type: application/json" \
    -d "{\"stu_id\": 你的学号, \"stu_pwd\": \"md5(你的智慧课程平台密码)\"}"
```