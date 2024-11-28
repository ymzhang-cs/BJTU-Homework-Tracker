# Homework Query API

## Description

目标是实现运行在服务器上的一个查询作业的 API，该 API 可以通过 HTTP 请求来查询作业。

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