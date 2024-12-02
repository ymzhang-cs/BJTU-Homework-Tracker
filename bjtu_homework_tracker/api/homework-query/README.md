# Homework Query API

## 介绍

该文件夹是实现运行在服务器上的一个查询作业的 API，该 API 可以通过 HTTP 请求来查询作业。

可以配合 iOS 快捷指令 **BJTU智慧课程平台作业抓取** 使用。

快捷指令导入链接：[iCloud 分享链接](https://www.icloud.com/shortcuts/5036d3c15f824fdf9a4b03d7a6de6828)

## 开始使用

1. 点击上方的导入链接，导入快捷指令到你的 iOS 设备。如果遇到问题，参见 [导入教程](https://www.rcuts.com/382.html)。
2. 找到该快捷指令，点击右上角“…”，参照注释配置你的学号和密码，然后运行该指令。

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