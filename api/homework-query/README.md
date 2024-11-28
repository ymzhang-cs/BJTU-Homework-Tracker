# Homework Query API

## Description

目标是实现运行在服务器上的一个查询作业的API，该API可以通过HTTP请求来查询作业。

请求体内容：

`http://[server]:[port]/api/homework-query?id=[学号]&pwd=[密码]`

返回内容：

```json
[
    {
        "name": "作业名称",
        "due_time": "截止日期",
        "content": "状态",
        "course_name": "课程名称"
    }
]
```

## Test

```bash
curl -X POST http://127.0.0.1:5000/api/homework-query \
    -H "Content-Type: application/json" \
    -d "{\"stu_id\": 你的学号, \"stu_pwd\": \"你的智慧课程平台密码\"}"
```